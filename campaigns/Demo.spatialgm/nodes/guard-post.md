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
        else: { text: The goblin opens one eye., adjust: alarm, by: 1 }
---
A guttering brazier lights an overturned table and a half-eaten rat on a stick. A goblin dozes
against the wall, spear across its knees.

## GM
If the heroes fight the guard, run it at the table (initiative); its friends in the barracks wake
on the second round (Alarm +1). Doors lead west, east and north.
