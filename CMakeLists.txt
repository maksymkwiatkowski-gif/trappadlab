cmake_minimum_required(VERSION 3.22)
project(TrapPadLab VERSION 1.0.0)

include(FetchContent)
FetchContent_Declare(JUCE
  GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
  GIT_TAG 8.0.6
  GIT_SHALLOW ON)
FetchContent_MakeAvailable(JUCE)

juce_add_plugin(TrapPadLab
  COMPANY_NAME "TrapLab"
  IS_SYNTH TRUE
  NEEDS_MIDI_INPUT TRUE
  NEEDS_MIDI_OUTPUT FALSE
  PLUGIN_MANUFACTURER_CODE Trpl
  PLUGIN_CODE Tpl1
  FORMATS VST3 Standalone
  PRODUCT_NAME "Trap Pad Lab"
  COPY_PLUGIN_AFTER_BUILD FALSE)

target_sources(TrapPadLab PRIVATE Source/TrapPadLab.cpp)
target_compile_definitions(TrapPadLab PUBLIC JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0 JUCE_VST3_CAN_REPLACE_VST2=0)
target_link_libraries(TrapPadLab
  PRIVATE juce::juce_audio_utils juce::juce_dsp
  PUBLIC juce::juce_recommended_config_flags juce::juce_recommended_warning_flags)
