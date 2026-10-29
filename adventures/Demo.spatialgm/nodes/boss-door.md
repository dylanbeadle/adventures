---
name: The boss's door
room: Boss Lair
enter:
  - { cutscene: the-boss-awakens }
choices:
  - fight the boss: showdown
  - run: { if: "strongbox", goto: escape, else: guard-post }
---
A throne of lashed-together shields faces the door. The goblin on it grins, and taps a rusty
cleaver on its knee.
