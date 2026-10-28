# Generates Source/Presets.inc (~350 instrument sounds). Edit and run: python generate_presets.py
import copy
# osc = [wave, ratio, cents, gain]
def B(name, oscs, f, q, a, d, s, r, fe, vh=0, vc=0, dr=0, ps=0, pt=.1, nz=0, tr=0):
    return dict(name=name, o=[list(x) for x in oscs], f=f, q=q, a=a, d=d, s=s, r=r, fe=fe,
                vh=vh, vc=vc, dr=dr, ps=ps, pt=pt, nz=nz, tr=tr)
PADS = [
 B("Dusk Pad",[("Saw",1,-9,.5),("Saw",1,9,.5),("Sine",.5,0,.6)],550,1,.9,.6,.8,2,500),
 B("Choir Haze",[("Saw",1,-14,.4),("Saw",1,14,.4),("Sq",1,0,.15)],900,5,1.1,.5,.7,2.2,300,5,8),
 B("Horror Strings",[("Saw",1,-20,.4),("Saw",1,20,.4),("Saw",2,0,.15)],1300,1,.6,.5,.9,1.5,900,5.5,12),
 B("Cold Glass Pad",[("Tri",1,-6,.5),("Tri",2,6,.3),("Sine",3,0,.1)],2500,1,1.4,.8,.7,2.5,1200),
 B("Smoke Pad",[("Saw",1,-11,.4),("Sq",.5,0,.35),("Saw",1,11,.4)],380,2,1.6,.7,.8,3,350),
 B("Lofi Warble",[("Tri",1,-8,.5),("Saw",1,8,.3),("Sine",.5,0,.5)],800,1,.5,.6,.7,1.6,250,1.8,25),
]
LEADS = [
 B("Saw Lead",[("Saw",1,-7,.5),("Saw",1,7,.5)],3500,1.5,.01,.2,.8,.25,1500,5.5,6),
 B("Square Lead",[("Sq",1,0,.6),("Sq",1,8,.3)],2500,1,.01,.1,.85,.2,800,5.5,8),
 B("Supersaw Lead",[("Saw",1,-18,.4),("Saw",1,0,.4),("Saw",1,18,.4)],5000,1,.02,.3,.8,.4,1500),
 B("Sine Lead",[("Sine",1,0,.9),("Sine",2,0,.1)],6000,.7,.02,.1,.9,.3,0,5.5,5),
 B("Pulse Lead",[("Pulse",1,0,.7),("Pulse",1,7,.4)],2800,1.5,.01,.15,.8,.25,1200,5,8),
 B("Screech Lead",[("Saw",1,0,.6),("Sq",2,5,.3)],4500,5,.01,.2,.85,.3,2500,6,15),
 B("Flute Lead",[("Sine",1,0,.9),("Tri",2,0,.15)],3500,.7,.07,.1,.8,.3,0,5.5,7),
 B("Whistle Lead",[("Sine",1,0,1),("Sine",2,0,.05)],5000,.7,.12,.1,.9,.25,0,6,10),
]
PLUCKS = [
 B("Dark Pluck",[("Tri",1,0,.7),("Saw",1,6,.3)],900,2,.005,.35,0,.4,2800),
 B("Harp Pluck",[("Tri",1,0,.7),("Sine",2,0,.3),("Sine",3,0,.1)],3000,.7,.003,.7,0,.6,1500),
 B("Trap Pluck",[("Saw",1,-5,.5),("Saw",1,5,.5)],1500,2,.004,.25,.15,.3,3500),
 B("Saw Pluck",[("Saw",1,-6,.5),("Saw",1,6,.5)],1200,2,.003,.22,0,.25,3000),
 B("Square Pluck",[("Sq",1,0,.6),("Tri",1,0,.3)],1000,2,.003,.25,0,.3,2500),
 B("Soft Pluck",[("Tri",1,0,.8),("Sine",2,0,.2)],2200,.7,.008,.5,0,.5,800),
 B("Bright Pluck",[("Saw",1,0,.5),("Sq",2,0,.15)],3500,1,.002,.18,0,.25,3500),
]
BASSES = [  # tr=-12: plays one octave down
 B("808 Sub",[("Sine",1,0,1)],800,.7,.003,2,.2,.25,0,0,0,0,8,.035,0,-12),
 B("808 Long",[("Sine",1,0,1)],800,.7,.003,3.5,.35,.5,0,0,0,0,5,.05,0,-12),
 B("808 Dirty",[("Sine",1,0,.9),("Tri",2,0,.2)],1500,.7,.003,1.8,.2,.3,0,0,0,.5,10,.03,0,-12),
 B("Sub Bass",[("Sine",1,0,1)],800,.7,.01,.1,.95,.15,0,0,0,0,0,.1,0,-12),
 B("Reese Bass",[("Saw",1,-14,.5),("Saw",1,14,.5),("Sine",.5,0,.5)],500,1.5,.01,.3,.9,.2,300,0,0,0,0,.1,0,-12),
 B("Saw Bass",[("Saw",1,0,.7),("Sq",.5,0,.4)],700,2,.005,.3,.6,.15,900,0,0,0,0,.1,0,-12),
 B("Growl Bass",[("Saw",1,-9,.5),("Sq",1,9,.4)],900,4,.01,.25,.7,.15,1500,7,30,.6,0,.1,0,-12),
 B("Pluck Bass",[("Tri",1,0,.7),("Saw",1,0,.3)],600,2,.003,.25,0,.2,1500,0,0,0,0,.1,0,-12),
]
KEYS = [
 B("Memphis Keys",[("Sine",1,0,.8),("Tri",2,0,.25),("Sq",.5,0,.1)],2200,.8,.01,.9,.12,.6,900),
 B("Sad Piano",[("Tri",1,0,.7),("Sine",2,0,.35),("Sine",3,3,.15)],2400,.7,.006,1.2,.05,.5,1200),
 B("Music Box",[("Sine",1,0,.6),("Sine",4,0,.25),("Sine",6,0,.1)],7000,.7,.003,.9,0,.8,0),
 B("Rhodes",[("Sine",1,0,.8),("Tri",2,0,.25),("Sine",4,0,.15)],2800,.7,.006,1.1,.1,.6,600),
 B("Organ",[("Sine",1,0,.5),("Sine",2,0,.35),("Sine",3,0,.2)],4000,.7,.01,.1,.95,.15,0,6,3),
]
BELLS = [
 B("Ice Bell",[("Sine",1,0,.7),("Sine",2.76,0,.3),("Sine",5.4,0,.12)],6000,.7,.004,1.4,0,1.2,0),
 B("Eerie Bell",[("Sine",1,0,.6),("Sine",2.4,0,.3),("Sine",3.8,5,.2)],4000,.7,.01,2,0,2.5,0,.5,8),
 B("Glass Bell",[("Sine",1,0,.6),("Sine",3.2,0,.3),("Sine",6.1,0,.12)],7000,.7,.003,1.8,0,1.5,0),
 B("Church Bell",[("Sine",1,0,.5),("Sine",2.4,0,.4),("Sine",4.1,0,.25)],3500,.7,.005,3,0,3.5,0),
]
SYNTHS = [
 B("Supersaw Chord",[("Saw",1,-20,.4),("Saw",1,0,.4),("Saw",1,20,.4)],3000,1,.03,.4,.8,.6,1500),
 B("Poly Saw",[("Saw",1,-6,.5),("Saw",1,6,.5)],1800,1,.02,.3,.8,.4,800),
 B("Square Poly",[("Sq",1,-5,.4),("Sq",1,5,.4),("Tri",1,0,.3)],1600,1,.02,.3,.8,.4,700),
 B("Brass Stab",[("Saw",1,-7,.5),("Saw",1,7,.5),("Sq",1,0,.1)],700,1.5,.04,.3,.7,.3,2200),
 B("Analog Stack",[("Saw",1,-9,.4),("Sq",1,9,.3),("Saw",.5,0,.4)],1400,1.5,.03,.35,.7,.4,1200),
 B("Strings",[("Saw",1,-12,.4),("Saw",1,12,.4),("Saw",2,5,.15)],1800,1,.35,.3,.85,.8,700,5,6),
]
FX = [
 B("Dark Drone",[("Saw",.5,-8,.5),("Saw",.25,0,.3),("Sine",.5,0,.4)],300,2,2.5,1,.9,3,200,.3,10,0,0,.1,.02),
 B("Wind",[("Sine",1,0,.05)],1200,4,1.5,1,.9,2.5,800,.2,0,0,0,.1,.5),
 B("Ghost Choir",[("Saw",1,-10,.3),("Tri",2,8,.2)],1400,6,1.2,.5,.8,2.5,500,4.5,12,0,0,.1,.03),
 B("Rise Noise",[("Saw",1,0,.2)],500,3,3,1,1,.6,6000,0,0,0,0,.1,.4),
]
def add_sub(p, g):
    if len(p["o"]) < 3: p["o"].append(["Sine", .5, 0, g])
    else:
        i = min(range(3), key=lambda k: p["o"][k][3]); p["o"][i] = ["Sine", .5, 0, g]
def widen(p):
    for i, o in enumerate(p["o"]):
        if o[0] != "Sine": o[2] = o[2] * 1.9 if o[2] else (-7 if i % 2 == 0 else 7)
def octs(p, m):
    for o in p["o"]: o[1] *= m
def grit(p, fa): p.update(q=min(p["q"] + 2.5, 8), fe=p["fe"] * fa + 500, dr=min(p["dr"] + .35, 1.2))
def cut(p, k): p["f"] *= k
M = dict(
 Dark=lambda p: (cut(p, .55), p.update(fe=p["fe"] * .7)),
 Bright=lambda p: cut(p, 1.8),
 Wide=widen,
 Slow=lambda p: p.update(a=p["a"] * 2, r=p["r"] * 1.5),
 Ghost=lambda p: p.update(f=p["f"] * .7, r=p["r"] * 2, vh=4, vc=10),
 Tape=lambda p: p.update(vh=1.8, vc=22),
 Sub=lambda p: add_sub(p, .6),
 OctUp=lambda p: octs(p, 2),
 OctDown=lambda p: octs(p, .5),
 Gritty=lambda p: grit(p, 1.8),
 Hollow=lambda p: (cut(p, .8), [o.__setitem__(0, "Sq") for o in p["o"] if o[0] == "Saw"]),
 Evolving=lambda p: p.update(fe=p["fe"] * 2 + 800, vh=.4, vc=14, a=p["a"] * 1.5),
 Long=lambda p: p.update(d=p["d"] * 1.9, r=p["r"] * 1.8),
 Short=lambda p: p.update(d=p["d"] * .45, r=p["r"] * .5),
 Soft=lambda p: p.update(a=max(p["a"] * 4, .03), f=p["f"] * .6),
 Warble=lambda p: p.update(vh=5, vc=18),
)
NAMES = {"OctUp": "Octave Up", "OctDown": "Octave Down"}
def mods(*keys): return [("", lambda p: None)] + [(NAMES.get(k, k), M[k]) for k in keys]
CATS = [
 ("Pad", PADS, mods("Dark","Bright","Wide","Slow","Ghost","Tape","Sub","OctUp","Gritty","Hollow","Evolving")),
 ("Lead", LEADS, mods("Dark","Bright","Wide","Soft","OctUp","Warble","Gritty")),
 ("Pluck", PLUCKS, mods("Dark","Bright","Long","Short","Wide","OctUp","Gritty")),
 ("Bass", BASSES, mods("Dark","Bright","Gritty","Long","Short")),
 ("Keys", KEYS, mods("Dark","Bright","Soft","Long","Warble")),
 ("Bell", BELLS, mods("Dark","Bright","Long","Short","OctUp")),
 ("Synth", SYNTHS, mods("Dark","Bright","Wide","Soft","OctUp","OctDown","Gritty")),
 ("FX", FX, mods("Dark","Bright","Long")),
]
def line(cat, base, mod, p):
    name = f"{cat} - {base}" + (f" {mod}" if mod else "")
    oscs = ",".join("{%s,%.3ff,%.3ff,%.3ff}" % tuple(o) for o in p["o"])
    return '{"%s",{%s},%.1ff,%.2ff,%.3ff,%.3ff,%.3ff,%.3ff,%.1ff,%.2ff,%.1ff,%.2ff,%.1ff,%.3ff,%.2ff,%.1ff},' % (
        name, oscs, min(p["f"], 18000), min(p["q"], 8), p["a"], p["d"], p["s"], p["r"], p["fe"],
        p["vh"], p["vc"], p["dr"], p["ps"], p["pt"], p["nz"], p["tr"])
out = []
for cat, bases, ml in CATS:
    n0 = len(out)
    for b in bases:
        for mod, fn in ml:
            p = copy.deepcopy(b); fn(p); out.append(line(cat, b["name"], mod, p))
    print(cat, len(out) - n0)
open("Source/Presets.inc", "w").write("\n".join(out) + "\n")
print("total", len(out))
