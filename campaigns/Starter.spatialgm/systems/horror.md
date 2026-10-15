---
name: Horror
health: Health
conditions:
  - Unconscious: arrow.down.to.line
  - Bleeding: drop.fill
  - Frightened: eye.trianglebadge.exclamationmark
  - Hidden: eye.slash.fill
  - Shaken: waveform.path.ecg
movement: { speed: 40 }   # feet in a turn for a creature whose file says nothing (5 ft to a square)
at-zero-health: Unconscious
rolls:                     # saved rolls in the dice bag: name: dice
  Advantage: 2d20
  Disadvantage: 2d20
  Fireball: 8d6
  Ability Scores: 4d6
  Percentile: d100
license: CC0-1.0            # free to use, change and share
author: Spatial GM
---
