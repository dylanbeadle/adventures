// Storm: rain through the room. The flash is the room itself — the app runs it
// because the passthrough tint is the app's to drive, not a script's.
//
// The .reality supplies Rain, Strike (a point light) and ColdFront (a directional
// light); this file configures the emitter.

const RealityKit = require("RealityKit");
const Math3D = require("Math3D");

const EMITTER = RealityKit.ParticleEmitterComponent.Type;
const PRESETS = RealityKit.ParticleEmitterComponent.Presets;


// The tuning surface the app reads: each entry becomes a slider. The defaults
// keep the storm's look; the app owns the flash and the thunder.
const TUNING = {
  "RainRate": {
    "label": "Rain rate",
    "description": "How many raindrops fall each second.",
    "min": 50,
    "max": 2000,
    "step": 10,
    "value": 700
  },
  "RainLife": {
    "label": "Rain life",
    "description": "How long each drop lasts, in seconds.",
    "min": 0.5,
    "max": 6,
    "step": 0.1,
    "value": 2.2
  },
  "RainArea": {
    "label": "Rain area",
    "description": "How wide the rain falls across the room, in metres.",
    "min": 1,
    "max": 8,
    "step": 0.1,
    "value": 4
  },
  "FlashOpacity": {
    "label": "Flash opacity",
    "description": "How white the lightning flash is; 0 is invisible, 1 is solid white.",
    "min": 0,
    "max": 1,
    "step": 0.01,
    "value": 0.55
  },
  "FlashDuration": {
    "label": "Flash duration",
    "description": "How long the double white flash lasts, in seconds.",
    "min": 0.1,
    "max": 2,
    "step": 0.05,
    "value": 1.05
  },
  "FlashInterval": {
    "label": "Flash interval",
    "description": "Seconds between lightning strikes.",
    "min": 1,
    "max": 30,
    "step": 0.5,
    "value": 6
  }
};

this.didAdd = function () {
  // A preset carries an image, a colour and a downward velocity; a bare emitter
  // from USD points its plane's normal up and spawns in a 10 cm square.
  this.entity.setComponent(PRESETS.rain);

  const rain = this.entity.getComponent(EMITTER);
  if (rain) {
    rain.isEmitting = true;
    rain.emitterShape = RealityKit.ParticleEmitterComponent.EmitterShape.plane;
    rain.emitterShapeSize = new Math3D.Vector3(TUNING.RainArea.value, 0.1, TUNING.RainArea.value);
    rain.mainEmitter.birthRate = TUNING.RainRate.value;
    rain.mainEmitter.lifeSpan = TUNING.RainLife.value;
    this.entity.setComponent(rain);
    console.log("storm: rain configured");
  }
};

this.update = function (deltaTime) {};
