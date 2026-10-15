---
# A keyed scene: it happens by itself when its event fires.
name: The warren wakes
when: counter-full alarm   # when the Alarm counter reaches its most
interrupt: yes             # at once, not "at the next good moment"
enter:
  - { place: [2 goblin], near: party }
choices:
  - fight: showdown
  - run for the door: { if: "strongbox", goto: escape, else: captured }
---
A horn blares. Doors bang open all through the warren, and goblins pour out with torches and
spears.
