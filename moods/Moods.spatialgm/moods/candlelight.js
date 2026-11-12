// Candlelight: warm embers drifting up from the table.
//
// The .reality supplies the emitter and the two point lights; this file is what
// configures them, because particle parameters cannot be authored in USD.
// Everything here is a scalar so it round-trips through the bridge unambiguously.

const RealityKit = require("RealityKit");

const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const LIGHT = RealityKit.PointLightComponent.Type;

const BASE = 900;

this.didAdd = function () {
  const emitter = this.entity.getComponent(EMITTER);
  console.log("candlelight: emitter " + (emitter ? "found" : "missing"));
  if (!emitter) { return; }

  emitter.isEmitting = true;
  emitter.speed = 0.35;
  emitter.speedVariation = 0.15;
  // Enums are values on the type, not strings: a string silently does nothing.
  emitter.emitterShape = RealityKit.ParticleEmitterComponent.EmitterShape.box;
  emitter.birthDirection = RealityKit.ParticleEmitterComponent.BirthDirection.world;
  emitter.emitterShapeSize.x = 0.8;
  emitter.emitterShapeSize.y = 0.25;
  emitter.emitterShapeSize.z = 0.8;
  emitter.mainEmitter.birthRate = 34;
  emitter.mainEmitter.lifeSpan = 4.5;
  this.entity.setComponent(emitter);

  this.state = { t: 0, flicker: 0 };
};

this.update = function (deltaTime) {
  const s = this.state;
  if (!s) { return; }

  // A slow, irregular breathing on the two candle lights.
  s.t += deltaTime;
  if (s.t < 0.08) { return; }
  s.t = 0;

  s.flicker += (Math.random() - 0.5) * 0.25;
  s.flicker = Math.max(-0.35, Math.min(0.35, s.flicker));
  const intensity = BASE * (1 + s.flicker);

  const scene = this.entity.scene;
  const left = scene ? scene.findEntity("GlowLeft") : null;
  const right = scene ? scene.findEntity("GlowRight") : null;
  for (const candle of [left, right]) {
    if (!candle) { continue; }
    const light = candle.getComponent(LIGHT);
    if (!light) { continue; }
    light.intensity = intensity;
    candle.setComponent(light);
  }
};
