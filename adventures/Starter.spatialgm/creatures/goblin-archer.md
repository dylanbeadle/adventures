---
base: goblin               # starts as a goblin; only what differs is written here
speed: 30 ft              # feet in a turn (the rule set's movement: speed when left out)
max-value: { health: 9 }
color: orange
attributes: { dex: 3 }                   # attributes merge by id: str and wits come from the goblin
tactics: { keep: 4 }
actions:                     # so do rolls: the goblin's Stab stays, and it gains a Shoot
  Shoot: d20 + dex → d6 range 30/120
---
Stays at the back and shoots from the dark. Hides again after every shot.
