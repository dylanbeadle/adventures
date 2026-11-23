// Rolling Fog: the shape is baked into eight height slices and four time keys.
// This script sets the room's acoustics and the fog's starting Shader Graph
// inputs. In a Debug build, pinch and hold the mood tile in the GM screen and
// choose Tune to change them live; the window discovers the inputs from the
// material, so it also works for Fog's Density and Billow.
//
// The inputs are promoted on the FogMat material:
//   Density      extinction scale (higher = thicker)
//   Opacity      master coverage
//   Speed        speed of the 12 s four-key loop
//   TimeOffset   phase into that loop, seconds
//   Warmth       the warm bounce above the table
//   Glow         the forward-scattering lobe
//   LodBias      texture mip bias; negative keeps the slice detail
//   Brightness   multiplies the fog's colour
//   Floor        minimum slice density, to fill the gaps
//   Wisps        strength of the procedural wisp field
//   WispScale    size of those wisps, cycles per metre

const RealityKit = require("RealityKit");
const MODEL = RealityKit.ModelComponent.Type;
const VALUE = RealityKit.MaterialParameters.Value;
const REVERB = RealityKit.ReverbComponent.Type;

const FOG = {
  density: 1.1,
  opacity: 0.19,
  speed: 1.9,
  timeOffset: 0.0,
  warmth: 0.6,
  glow: 0.4,
  lodBias: -1.5,
  brightness: 0.45,
  floor: 0.0,
  wisps: 0.9,
  wispScale: 2.5,
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

  const volume = findVolume(root);
  const ok = volume && setFog(volume, {
    Density: FOG.density,
    Opacity: FOG.opacity,
    Speed: FOG.speed,
    TimeOffset: FOG.timeOffset,
    Warmth: FOG.warmth,
    Glow: FOG.glow,
    LodBias: FOG.lodBias,
    Brightness: FOG.brightness,
    Floor: FOG.floor,
    Wisps: FOG.wisps,
    WispScale: FOG.wispScale,
  });
  console.log("rolling-fog: parameters " + (ok ? "set" : "not found"));
  console.log("rolling-fog: ready");
};
