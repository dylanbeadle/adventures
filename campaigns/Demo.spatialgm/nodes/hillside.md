---
name: The hillside
encounter: goblin-warren   # set this encounter up on entering, if it isn't already
room: Entrance             # and reveal this room
choices:
  - walk straight in: { adjust: alarm, by: 1, goto: guard-post }
tasks:                     # rolled by the player (or the engine): rows say where each result leads
  - sneak up to the north door:
      roll: test, attribute: dex, difficulty: 12
      rows:
        difficulty+: guard-post
        else: { text: A loose stone clatters down the slope., adjust: alarm, by: 1, goto: guard-post }
---
Rain drips through a crack in the hillside. Muddy boot prints, small and many, lead north to a
door of lashed planks. Light flickers behind it.

## GM
Each point of Alarm makes the goblins harder to surprise. At 4, the warren wakes.
