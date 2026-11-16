---
name: The steam gallery
room: Steam Gallery
enter:
  - { condition: Scalded, to: party, until: 3 rounds, tick-damage: script(steam-pressure) }
choices:
  - back to the gear hall: gear-hall
---
The vents breathe in time with the gears overhead. Every breath is hotter than the last.

## GM
Scalded deals damage at the start of each of the next three rounds. How much is looked up by
`scripts/steam-pressure.js` from two keys: gears turned, and the Alarm.
