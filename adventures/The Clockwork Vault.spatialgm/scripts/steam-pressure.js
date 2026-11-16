// name: Steam pressure
// summary: Scalding damage each round, looked up by gears turned and by Alarm.
// license: CC0-1.0
// author: Spatial GM
//
// Read as a number by the Steam Gallery's condition: tick-damage: script(steam-pressure).
// A table a roll can't say: two keys, and a die only when the pressure is high.

const pressure = [
  //  Alarm: 0-1  2-3  4-6
  [1, 1, 2], // 0 gears
  [1, 2, 3], // 1 gear
  [2, 3, 4], // 2 gears
  [3, 4, 6], // 3 gears
];
const gears = Math.min(3, facts.trackers.gears ?? 0);
const alarm = facts.trackers.alarm ?? 0;
const column = alarm <= 1 ? 0 : alarm <= 3 ? 1 : 2;
const base = pressure[gears][column];
// High pressure surges: a seeded random number, so a save replays the same steam.
return base >= 4 ? base + Math.floor(Math.random() * 3) : base;
