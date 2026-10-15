---
# This table has the same name as the oracle's event-focus, so in this campaign it replaces it:
# random events happen in the warren's own way.
name: Event focus (the warren)
roll: d10
rows:
  1-2: A goblin patrol passes nearby → { adjust: alarm, by: 1 }
  3-4: The boss shouts for someone → { draw: warren-noises }
  5-6: Someone acts → { pick: characters }
  7-8: Something new → @action @subject
  9: A torch sputters → { adjust: torches, by: -1 }
  10: A thread moves → { pick: threads }
license: CC0-1.0
author: Spatial GM
---
Roll when the oracle calls for a random event while the heroes are inside the warren.
