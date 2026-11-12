// Storm: rain through the room. The flash is the room itself — the app runs it
// because the passthrough tint is the app's to drive, not a script's.
//
// The .reality supplies Rain, Strike (a point light) and ColdFront (a directional
// light); this file configures the emitter.

const RealityKit = require("RealityKit");
const Math3D = require("Math3D");

const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const PRESETS = RealityKit.ParticleEmitterComponent.Presets;

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
};

this.update = function (deltaTime) {};
