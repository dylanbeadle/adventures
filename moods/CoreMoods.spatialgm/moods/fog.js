// Fog: a low sea of cold mist. The work is in the scene's Shader Graph — three
// drifting noise fields, two swells wandering through each other, and a hard
// falloff at the room's edge so the mesh has no boundary. This file only sets
// the room's acoustics and keeps the script anchor's emitter quiet.

const RealityKit = require("RealityKit");

const PARTICLES = RealityKit.ParticleEmitterComponent.Type;
const REVERB = RealityKit.ReverbComponent.Type;

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
