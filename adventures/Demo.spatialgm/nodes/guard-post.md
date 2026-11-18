---
name: The guard post
room: Guard Post
enter:
  - { draw: warren-noises }
choices:
  - go west, to the barracks: barracks
  - go east, to the storeroom: storeroom
  - go north, to the big door: boss-door
tasks:
  - slip past the guard:
      roll: test, attribute: dex, difficulty: 13
      rows:
        difficulty+: { text: The goblin snores on. }
        else: The goblin opens one eye. → [{ adjust: alarm, by: 1 }, { condition: Asleep, to: Goblin, off: true }]
---
A guttering brazier lights an overturned table and a half-eaten rat on a stick.

## GM
The goblin starts Asleep (its condition on the board says how it is now: narrate from that). If the heroes fight the guard, it wakes: take Asleep off and run it at the table (initiative); its friends in the barracks wake
on the second round (Alarm +1). Doors lead west, east and north.
