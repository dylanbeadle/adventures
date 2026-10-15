---
base: goblin               # starts as a goblin; only what differs is written here
speed: 30 ft              # feet in a turn (the rule set's movement: speed when left out)
health: 9
color: orange
stats: { dex: 3 }          # stats merge by name: str and wits come from the goblin
tactics: { keep: 4 }
rolls:                     # so do rolls: the goblin's Stab stays, and it gains a Shoot
  Shoot: d20 + dex → d6 range 30/120
---
Stays at the back and shoots from the dark. Hides again after every shot.
