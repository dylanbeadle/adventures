// Storm: rain through the room and a double flash every few seconds.
//
// Attached to the "Rain" entity. The .reality supplies Rain, Strike (a point
// light) and ColdFront (a directional light); this file configures the emitter
// and runs the lightning.

const RealityKit = require("RealityKit");

const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const LIGHT = RealityKit.PointLightComponent.Type;
const Shape = RealityKit.ParticleEmitterComponent.EmitterShape;

const STRIKE = 260000;
const FLASHES = [
  { at: 0.00, level: 1.0 },
  { at: 0.07, level: 0.1 },
  { at: 0.18, level: 0.8 },
  { at: 0.26, level: 0.0 },
];

this.didAdd = function () {
  const rain = this.entity.getComponent(EMITTER);
  if (rain) {
    rain.isEmitting = true;
    rain.speed = 9.0;
    rain.speedVariation = 2.0;
    rain.emitterShape = Shape.plane;
    rain.mainEmitter.birthRate = 420;
    rain.mainEmitter.lifeSpan = 2.4;
    this.entity.setComponent(rain);
    console.log("storm: rain configured");
  }
  this.state = { t: 0, next: 3.0, sequence: null, sequenceAt: 0, settled: null };
};

this.update = function (deltaTime) {
  const s = this.state;
  if (!s) { return; }

  const strike = this.entity.scene ? this.entity.scene.findEntity("Strike") : null;

  // Mid-flash: walk the levels.
  if (s.sequence !== null) {
    s.sequenceAt += deltaTime;
    while (s.sequence < FLASHES.length && s.sequenceAt >= FLASHES[s.sequence].at) {
      if (strike) {
        const light = strike.getComponent(LIGHT);
        if (light) {
          light.intensity = STRIKE * FLASHES[s.sequence].level;
          strike.setComponent(light);
        }
      }
      s.sequence += 1;
    }
    if (s.sequence >= FLASHES.length) { s.sequence = null; }
    return;
  }

  s.t += deltaTime;
  if (s.t < s.next) { return; }
  s.t = 0;
  s.next = 4.0 + Math.random() * 6.0;
  s.sequence = 0;
  s.sequenceAt = 0;
};
