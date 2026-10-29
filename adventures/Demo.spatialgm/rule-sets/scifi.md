---
name: Sci-fi
health: Integrity
experience: XP              # what experience is called (the GM's XP control shows with it)
conditions:
  - Down: arrow.down.to.line
  - Burning: flame.fill
  - Suppressed: exclamationmark.triangle.fill
  - Shielded: shield.fill
  - Marked: scope
movement: { speed: 40 }   # feet in a turn for a creature whose file says nothing (5 ft to a square)
at-zero-health: Down
rolls:                     # saved rolls in the dice bag: name: dice
  Advantage: 2d20
  Disadvantage: 2d20
  Fireball: 8d6
  Ability Scores: 4d6
  Percentile: d100
license: CC0-1.0            # free to use, change and share
author: Spatial GM
---
