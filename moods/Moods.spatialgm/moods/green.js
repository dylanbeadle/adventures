// Green Screen: the loudest mood there is, for testing that a pack mood reaches
// the room — the tint on the passthrough, a green light, and green motes.

const RealityKit = require("RealityKit");

const LIGHT = RealityKit.PointLightComponent.Type;
const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const BASE = 30000;
const SWING = 120000;

this.didAdd = function () {
  const motes = this.entity.getComponent(EMITTER);
  if (motes) {
    motes.isEmitting = true;
    motes.speed = 0.5;
    motes.mainEmitter.birthRate = 80;
    this.entity.setComponent(motes);
  }
  this.state = { t: 0, light: this.entity.scene ? this.entity.scene.findEntity("Glow") : null };
  console.log("green: light " + (this.state.light ? "found" : "missing"));
};

this.update = function (deltaTime) {
  const s = this.state;
  if (!s || !s.light) { return; }
  s.t += deltaTime;

  // A slow, obvious pulse: 30k to 150k and back, about every two seconds.
  const level = (Math.sin(s.t * Math.PI) + 1) / 2;
  const light = s.light.getComponent(LIGHT);
  light.intensity = BASE + SWING * level;
  s.light.setComponent(light);
};
