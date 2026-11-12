// Storm: rain through the room, and a flash of lightning.
//
// The .reality supplies Rain (an emitter), Flash (an emissive sphere, hidden at
// first), Strike (a point light) and ColdFront (a directional light).
//
// The flash is geometry, not a light: in a mixed immersive space the passthrough
// tint is the app's alone, and a virtual light lights nothing but virtual geometry.

const RealityKit = require("RealityKit");
const Math3D = require("Math3D");

const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const PRESETS = RealityKit.ParticleEmitterComponent.Presets;

const HIDDEN = 0.001;
const FLASHES = [
  { at: 0.00, scale: 1.00 },
  { at: 0.07, scale: 0.30 },
  { at: 0.18, scale: 0.80 },
  { at: 0.26, scale: HIDDEN },
];

this.didAdd = function () {
  // A preset carries an image, a colour and a downward velocity; a bare emitter
  // from USD points its plane's normal up and spawns in a 10 cm square.
  this.entity.setComponent(PRESETS.rain);

  const rain = this.entity.getComponent(EMITTER);
  if (rain) {
    rain.isEmitting = true;
    rain.emitterShape = RealityKit.ParticleEmitterComponent.EmitterShape.plane;
    rain.emitterShapeSize = new Math3D.Vector3(4, 0.1, 4);
    rain.mainEmitter.birthRate = 700;
    rain.mainEmitter.lifeSpan = 2.2;
    this.entity.setComponent(rain);
    console.log("storm: rain configured");
  }

  const root = this.entity.parent;
  this.state = { t: 0, next: 1.5, step: null, at: 0, flash: root ? root.findEntity("Flash") : null };
  this.hide = function () {
    if (this.state.flash) this.state.flash.scale = new Math3D.Vector3(HIDDEN, HIDDEN, HIDDEN);
  };
  this.hide();
  console.log("storm: flash " + (this.state.flash ? "found" : "missing"));
};

this.update = function (deltaTime) {
  const s = this.state;
  if (!s) { return; }

  if (s.step !== null) {
    s.at += deltaTime;
    while (s.step < FLASHES.length && s.at >= FLASHES[s.step].at) {
      const scale = FLASHES[s.step].scale;
      if (s.flash) {
        s.flash.scale = new Math3D.Vector3(scale, scale, scale);
      }
      s.step += 1;
    }
    if (s.step >= FLASHES.length) { s.step = null; }
    return;
  }

  s.t += deltaTime;
  if (s.t < s.next) { return; }
  s.t = 0;
  s.next = 4.0 + Math.random() * 6.0;
  s.step = 0;
  s.at = 0;
};
