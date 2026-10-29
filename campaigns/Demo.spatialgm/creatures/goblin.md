---
speed: 30 ft              # feet in a turn (the rule set's movement: speed when left out)
max-value: { health: 7 }
voice: beast-growl
color: red                 # monsters need no "side": they're run by the GM (or the bot)
tags: [goblin]
attributes: { str: 0, dex: 2, wits: 0 }
tactics: { flee: friends-half }
actions:                     # an attack, then (after →) the damage it does; shown as buttons on its card
  Stab: d20 + dex → d4 + str
---
Small, sneaky and cowardly alone; bold in a crowd. Runs when its friends start falling.
