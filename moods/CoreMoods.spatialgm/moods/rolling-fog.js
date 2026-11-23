// Rolling Fog: the shape is baked into eight height slices and four time keys.
// This script sets the room's acoustics and drives the fog's Shader Graph
// inputs, so the look can be tuned here instead of rebuilding the scene.
//
// The inputs are promoted on the FogMat material:
//   Density      extinction scale (higher = thicker). 2.6
//   Opacity      master coverage. 1.0
//   Speed        speed of the 12 s four-key loop. 1.0
//   TimeOffset   phase into that loop, seconds. 0
//   Warmth       the warm bounce above the table. 1.0
//   Glow         the forward-scattering lobe. 1.0
//
// Density and Warmth breathe slowly, so the fog keeps moving even where the
// four baked keys are at their quietest.

const RealityKit = require("RealityKit");
const MODEL = RealityKit.ModelComponent.Type;
const VALUE = RealityKit.MaterialParameters.Value;
const REVERB = RealityKit.ReverbComponent.Type;

const FOG = {
  density: 2.6,
  opacity: 1.0,
  speed: 1.0,
  timeOffset: 0.0,
  warmth: 1.0,
  glow: 1.0,
};

const BREATHE = {
  density: 0.035,     // ±3.5 %
  warmth: 0.08,       // ±8 %
  period: 27.0,       // seconds
  every: 0.25,        // how often the material is written, seconds
};

function findVolume(entity) {
  return entity.findEntity("FogVolume") ||
    (entity.parent ? entity.parent.findEntity("FogVolume") : null);
}

function findRoom(entity) {
  return entity.findEntity("Room") ||
    (entity.parent ? entity.parent.findEntity("Room") : null);
}

// The bridge hands out copies: change the material, put it back into an array,
// and set the whole ModelComponent again. Setting materials[0] alone does not
// reach RealityKit.
function setFog(volume, values) {
  if (!volume) return false;
  const model = volume.getComponent(MODEL);
  if (!model || !model.materials || model.materials.length === 0) return false;
  try {
    const material = model.materials[0];
    for (const name in values) {
      material.setParameter(name, VALUE.float(values[name]));
    }
    model.materials = [material];
    volume.setComponent(model);
    return true;
  } catch (error) {
    console.log("rolling-fog: could not set parameters — " + error);
    return false;
  }
}

this.didAdd = function () {
  const root = this.entity;
  const room = findRoom(root);
  if (room) {
    const reverb = room.getComponent(REVERB);
    if (reverb) {
      reverb.reverb = RealityKit.Reverb.mediumRoomDry;
      room.setComponent(reverb);
      console.log("rolling-fog: reverb mediumRoomDry");
    }
  }

  this.state = this.state || {};
  this.state.time = 0;
  this.state.since = 0;
  this.state.volume = findVolume(root);
  this.state.warned = false;

  const ok = this.state.volume && setFog(this.state.volume, {
    Density: FOG.density,
    Opacity: FOG.opacity,
    Speed: FOG.speed,
    TimeOffset: FOG.timeOffset,
    Warmth: FOG.warmth,
    Glow: FOG.glow,
  });
  console.log("rolling-fog: parameters " + (ok ? "set" : "not found"));
  console.log("rolling-fog: ready");
};

this.update = function (deltaTime) {
  const state = this.state;
  if (!state) return;
  state.time += deltaTime;

  if (!state.volume) state.volume = findVolume(this.entity);
  if (!state.volume) return;

  state.since += deltaTime;
  if (state.since < BREATHE.every) return;
  state.since = 0;

  const phase = state.time * 2 * Math.PI / BREATHE.period;
  const ok = setFog(state.volume, {
    Density: FOG.density * (1 + BREATHE.density * Math.sin(phase)),
    Warmth: FOG.warmth * (1 + BREATHE.warmth * Math.sin(phase * 0.7 + 1.3)),
  });
  if (!ok && !state.warned) {
    state.warned = true;
    console.log("rolling-fog: no ShaderGraphMaterial to breathe");
  }
};
