// Candlelight: warm embers drifting up from the table.
//
// The .reality supplies the emitter and the two point lights; this file is what
// configures them, because particle parameters cannot be authored in USD.
// Everything here is a scalar so it round-trips through the bridge unambiguously.

const RealityKit = require("RealityKit");

const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const LIGHT = RealityKit.PointLightComponent.Type;


// The tuning surface the app reads: each entry becomes a slider. Values drive
// the emitter and the two candle lights below; the defaults keep the look.
const TUNING = {
  "LightIntensity": {
    "label": "Candlelight",
    "description": "How bright the two candle flames burn.",
    "min": 100,
    "max": 2000,
    "step": 10,
    "value": 900
  },
  "Flicker": {
    "label": "Flicker",
    "description": "How much the candlelight wavers.",
    "min": 0,
    "max": 0.7,
    "step": 0.01,
    "value": 0.35
  },
  "EmberRate": {
    "label": "Ember rate",
    "description": "How many embers drift up each second.",
    "min": 0,
    "max": 120,
    "step": 1,
    "value": 34
  },
  "EmberSpeed": {
    "label": "Ember speed",
    "description": "How quickly the embers rise.",
    "min": 0,
    "max": 1.5,
    "step": 0.01,
    "value": 0.35
  },
  "EmberLife": {
    "label": "Ember life",
    "description": "How long each ember lives, in seconds.",
    "min": 0.5,
    "max": 10,
    "step": 0.1,
    "value": 4.5
  }
};

const BASE = TUNING.LightIntensity.value;

this.didAdd = function () {
  const emitter = this.entity.getComponent(EMITTER);
  console.log("candlelight: emitter " + (emitter ? "found" : "missing"));
  if (!emitter) { return; }

  emitter.isEmitting = true;
  emitter.speed = TUNING.EmberSpeed.value;
  emitter.speedVariation = 0.15;
  // Enums are values on the type, not strings: a string silently does nothing.
  emitter.emitterShape = RealityKit.ParticleEmitterComponent.EmitterShape.box;
  emitter.birthDirection = RealityKit.ParticleEmitterComponent.BirthDirection.world;
  emitter.emitterShapeSize.x = 0.8;
  emitter.emitterShapeSize.y = 0.25;
  emitter.emitterShapeSize.z = 0.8;
  emitter.mainEmitter.birthRate = TUNING.EmberRate.value;
  emitter.mainEmitter.lifeSpan = TUNING.EmberLife.value;
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

  const range = TUNING.Flicker.value;
  s.flicker += (Math.random() - 0.5) * range * 0.714;
  s.flicker = Math.max(-range, Math.min(range, s.flicker));
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
