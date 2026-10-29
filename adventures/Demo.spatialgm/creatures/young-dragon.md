---
size: large                # tiny, small, medium, large, huge or gargantuan
speed: 80 ft              # feet in a turn (the rule set's movement: speed when left out)
max-value: { health: 60 }
voice: giant
color: dark-red
tags: [dragon, boss]
overhang: true                # the built-in mini grows wings
attributes: { str: 4, dex: 1, wits: 2, armour: 14 }
actions:
  Breath: 3d6 range 30 area: cone 6 save: test dex vs 13
---
Young, vain and very dangerous. Breathes fire in a long line, then flies out of reach to watch.
