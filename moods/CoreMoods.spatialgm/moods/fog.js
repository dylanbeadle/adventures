// Fog: a low sea of cold mist. The work is in the scene's Shader Graph — three
// drifting noise fields, two swells wandering through each other, and a hard
// falloff at the room's edge so the mesh has no boundary. This file only sets
// the room's acoustics and keeps the script anchor's emitter quiet.

const RealityKit = require("RealityKit");

const PARTICLES = RealityKit.ParticleEmitterComponent.Type;
const REVERB = RealityKit.ReverbComponent.Type;


// The tuning surface: the tuner reads this block from the live script and shows
// one slider per entry. These two are also float inputs on the FogMat Shader
// Graph, so they are written straight to the material.
const TUNING = {
  "Density": {
    "label": "Density",
    "description": "How thick the sea of mist sits.",
    "min": 0,
    "max": 1,
    "step": 0.005,
    "value": 0.15
  },
  "Billow": {
    "label": "Billow",
    "description": "How much the mist's surface swells.",
    "min": 0,
    "max": 1,
    "step": 0.005,
    "value": 0.06
  }
};

this.didAdd = function () {
  const bank = this.entity;
  const parent = bank.parent;
  const veil = parent ? parent.findEntity("FogVeil") : null;

  const emitter = bank.getComponent(PARTICLES);
  if (emitter) {
    emitter.isEmitting = false;
    bank.setComponent(emitter);
  }

  // Fog damps a room: the sounds the app plays into it come back close and dry.
  const room = parent ? parent.findEntity("Room") : bank.scene.findEntity("Room");
  if (room) {
    const reverb = room.getComponent(REVERB);
    if (reverb) {
      reverb.reverb = RealityKit.Reverb.mediumRoomDry;
      room.setComponent(reverb);
      console.log("fog: reverb mediumRoomDry");
    }
  }
  console.log("fog: ready" + (veil ? ", veil" : ""));
};

this.update = function (deltaTime) {};
