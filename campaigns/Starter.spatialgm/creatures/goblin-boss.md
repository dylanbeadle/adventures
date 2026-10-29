---
speed: 30 ft              # feet in a turn (the rule set's movement: speed when left out)
max-value: { health: 15 }
voice: beast-growl
color: dark-red
tags: [goblin, boss]
attributes: { str: 2, dex: 1, wits: 1, armour: 12 }
tactics: { attacks: 2, target: weakest, by: ai }
actions:                     # an attack, then (after →) the damage it does; shown as buttons on its card
  Cleaver: d20 + str → d8 + 2
---
Taps a rusty cleaver on its knee and grins. **Two swings a turn.** Shouts for help as soon as it's hurt.
