#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_audio_utils/juce_audio_utils.h>
#include <juce_dsp/juce_dsp.h>
#include <atomic>
#include <cmath>
#include <vector>

namespace {
enum Wave { Sine, Tri, Saw, Sq, Pulse };
struct Osc { Wave w; float ratio, cents, gain; };
struct Preset {
    const char* name;
    Osc o[3];
    float cutoff, q, a, d, s, r, fenv, vibHz, vibCents, drive, pitchSt, pitchTau, noise, tr;
};

// name, oscillators {wave, ratio, cents, gain}, cutoff, Q, A, D, S, R, filterEnv, vibHz, vibCents,
// drive, pitchEnvSemitones, pitchEnvTime, noise, transposeSemitones  (see Presets.inc, made by generate_presets.py)
const Preset presets[] = {
#include "Presets.inc"
};
constexpr int NP = (int)(sizeof(presets) / sizeof(presets[0]));
const std::vector<std::vector<int>> chords{{0}, {0,3,7}, {0,3,7,10}, {0,3,7,10,14}};

struct Sound : juce::SynthesiserSound {
    bool appliesToNote(int) override { return true; }
    bool appliesToChannel(int) override { return true; }
};

class Voice : public juce::SynthesiserVoice {
public:
    Voice(std::atomic<float>* pr, std::atomic<float>* br) : presetP(pr), brightP(br) {}
    bool canPlaySound(juce::SynthesiserSound* s) override { return dynamic_cast<Sound*>(s) != nullptr; }

    void prep(double sr, int bs) {
        juce::dsp::ProcessSpec sp{sr, (juce::uint32) bs, 1};
        filt.prepare(sp);
        filt.setType(juce::dsp::StateVariableTPTFilterType::lowpass);
    }
    void startNote(int midi, float vel, juce::SynthesiserSound*, int) override {
        p = &presets[juce::jlimit(0, NP - 1, (int) presetP->load())];
        hz = (float) juce::MidiMessage::getMidiNoteInHertz(midi + (int) p->tr);
        level = vel * 0.35f; t = 0; lfo = 0; cnt = 0;
        mult = std::exp2((brightP->load() - 0.5f) * 4.f);
        for (auto& x : ph) x = 0;
        filt.reset(); filt.setResonance(p->q);
        adsr.setSampleRate(getSampleRate());
        adsr.setParameters({p->a, p->d, p->s, p->r});
        adsr.noteOn();
    }
    void stopNote(float, bool allowTailOff) override {
        if (allowTailOff) adsr.noteOff();
        else { adsr.reset(); clearCurrentNote(); }
    }
    void pitchWheelMoved(int) override {}
    void controllerMoved(int, int) override {}

    void renderNextBlock(juce::AudioBuffer<float>& out, int start, int num) override {
        if (p == nullptr || !isVoiceActive()) return;
        const float sr = (float) getSampleRate();
        const float twoPi = juce::MathConstants<float>::twoPi;
        for (int i = 0; i < num; ++i) {
            if ((cnt++ & 31) == 0) {
                float shape = t < p->a ? t / p->a : std::exp(-(t - p->a) / 0.6f);
                filt.setCutoffFrequency(juce::jlimit(40.f, 18000.f, (p->cutoff + p->fenv * shape) * mult));
                float vib = p->vibCents * std::sin(twoPi * lfo);
                lfo += p->vibHz * 32.f / sr; lfo -= std::floor(lfo);
                const float pm = std::exp2(p->pitchSt * std::exp(-t / juce::jmax(p->pitchTau, 0.001f)) / 12.f);
                for (int k = 0; k < 3; ++k)
                    inc[k] = hz * pm * p->o[k].ratio * std::exp2((p->o[k].cents + vib) / 1200.f) / sr;
            }
            t += 1.f / sr;
            float s = 0;
            for (int k = 0; k < 3; ++k) {
                const auto& o = p->o[k];
                if (o.gain == 0) continue;
                ph[k] += inc[k]; ph[k] -= std::floor(ph[k]);
                float v;
                switch (o.w) {
                    case Sine: v = std::sin(twoPi * ph[k]); break;
                    case Tri:  v = 4.f * std::abs(ph[k] - .5f) - 1.f; break;
                    case Saw:  v = 2.f * ph[k] - 1.f; break;
                    case Pulse: v = ph[k] < .25f ? 1.f : -1.f; break;
                    default:   v = ph[k] < .5f ? 1.f : -1.f; break;
                }
                s += v * o.gain * 0.55f;
            }
            s += p->noise * (rnd.nextFloat() * 2.f - 1.f);
            s = filt.processSample(0, s);
            if (p->drive > 0.f) s = std::tanh(s * (1.f + p->drive * 6.f)) * 0.7f;
            s *= adsr.getNextSample() * level;
            for (int c = 0; c < out.getNumChannels(); ++c) out.addSample(c, start + i, s);
            if (!adsr.isActive()) { clearCurrentNote(); break; }
        }
    }
private:
    std::atomic<float>* presetP; std::atomic<float>* brightP;
    const Preset* p = nullptr;
    juce::ADSR adsr;
    juce::dsp::StateVariableTPTFilter<float> filt;
    float hz = 440, level = 0, t = 0, lfo = 0, mult = 1, ph[3] = {0, 0, 0}, inc[3] = {0, 0, 0};
    int cnt = 0;
    juce::Random rnd;
};

juce::AudioProcessorValueTreeState::ParameterLayout layout() {
    juce::StringArray names; for (auto& p : presets) names.add(p.name);
    juce::AudioProcessorValueTreeState::ParameterLayout l;
    l.add(std::make_unique<juce::AudioParameterChoice>(juce::ParameterID{"preset", 1}, "Sound", names, 0));
    l.add(std::make_unique<juce::AudioParameterChoice>(juce::ParameterID{"chord", 1}, "Chord",
          juce::StringArray{"Single", "Minor", "Minor 7", "Minor 9"}, 0));
    l.add(std::make_unique<juce::AudioParameterFloat>(juce::ParameterID{"bright", 1}, "Brightness", 0.f, 1.f, .5f));
    l.add(std::make_unique<juce::AudioParameterFloat>(juce::ParameterID{"reverb", 1}, "Reverb", 0.f, 1.f, .4f));
    l.add(std::make_unique<juce::AudioParameterFloat>(juce::ParameterID{"volume", 1}, "Volume", 0.f, 1.f, .7f));
    return l;
}
} // namespace

class TrapPadLab : public juce::AudioProcessor {
public:
    TrapPadLab() : AudioProcessor(BusesProperties().withOutput("Output", juce::AudioChannelSet::stereo(), true)),
                   apvts(*this, nullptr, "STATE", layout()) {
        auto* pr = apvts.getRawParameterValue("preset");
        auto* br = apvts.getRawParameterValue("bright");
        for (int i = 0; i < 16; ++i) synth.addVoice(new Voice(pr, br));
        synth.addSound(new Sound());
        for (auto& c : chordAt) c = 0;
    }
    const juce::String getName() const override { return "Trap Pad Lab"; }
    bool acceptsMidi() const override { return true; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 3.0; }
    int getNumPrograms() override { return NP; }
    int getCurrentProgram() override { return (int) apvts.getRawParameterValue("preset")->load(); }
    void setCurrentProgram(int i) override {
        if (auto* p = apvts.getParameter("preset")) p->setValueNotifyingHost(p->convertTo0to1((float) i));
    }
    const juce::String getProgramName(int i) override { return presets[juce::jlimit(0, NP - 1, i)].name; }
    void changeProgramName(int, const juce::String&) override {}

    void prepareToPlay(double sr, int bs) override {
        synth.setCurrentPlaybackSampleRate(sr);
        for (int i = 0; i < synth.getNumVoices(); ++i)
            if (auto* v = dynamic_cast<Voice*>(synth.getVoice(i))) v->prep(sr, bs);
        reverb.setSampleRate(sr); reverb.reset();
    }
    void releaseResources() override {}
    bool isBusesLayoutSupported(const BusesLayout& l) const override {
        return l.getMainOutputChannelSet() == juce::AudioChannelSet::stereo();
    }

    void processBlock(juce::AudioBuffer<float>& buf, juce::MidiBuffer& midi) override {
        juce::ScopedNoDenormals nd;
        buf.clear();
        const int ch = juce::jlimit(0, 3, (int) apvts.getRawParameterValue("chord")->load());
        juce::MidiBuffer out;
        for (const auto meta : midi) {
            auto m = meta.getMessage(); int pos = meta.samplePosition;
            if (m.isNoteOn()) {
                chordAt[m.getNoteNumber()] = ch;
                for (int off : chords[ch]) { int n = m.getNoteNumber() + off;
                    if (n < 128) out.addEvent(juce::MidiMessage::noteOn(m.getChannel(), n, m.getVelocity()), pos); }
            } else if (m.isNoteOff()) {
                for (int off : chords[chordAt[m.getNoteNumber()]]) { int n = m.getNoteNumber() + off;
                    if (n < 128) out.addEvent(juce::MidiMessage::noteOff(m.getChannel(), n, m.getVelocity()), pos); }
            } else out.addEvent(m, pos);
        }
        synth.renderNextBlock(buf, out, 0, buf.getNumSamples());

        const float rv = apvts.getRawParameterValue("reverb")->load();
        juce::Reverb::Parameters rp;
        rp.roomSize = 0.85f; rp.damping = 0.5f; rp.width = 1.f;
        rp.wetLevel = rv * 0.45f; rp.dryLevel = 1.f - rv * 0.25f;
        reverb.setParameters(rp);
        reverb.processStereo(buf.getWritePointer(0), buf.getWritePointer(1), buf.getNumSamples());
        buf.applyGain(apvts.getRawParameterValue("volume")->load());
    }

    bool hasEditor() const override { return true; }
    juce::AudioProcessorEditor* createEditor() override { return new juce::GenericAudioProcessorEditor(*this); }
    void getStateInformation(juce::MemoryBlock& d) override {
        if (auto x = apvts.copyState().createXml()) copyXmlToBinary(*x, d);
    }
    void setStateInformation(const void* d, int n) override {
        if (auto x = getXmlFromBinary(d, n))
            if (x->hasTagName(apvts.state.getType())) apvts.replaceState(juce::ValueTree::fromXml(*x));
    }
private:
    juce::AudioProcessorValueTreeState apvts;
    juce::Synthesiser synth;
    juce::Reverb reverb;
    int chordAt[128];
};

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter() { return new TrapPadLab(); }
