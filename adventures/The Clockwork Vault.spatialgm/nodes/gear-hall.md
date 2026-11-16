---
name: The gear hall
room: Gear Hall
enter:
  - { place: [1 clockwork-sentinel], near: party, times: ceil(party / 2) + tracker(alarm) / 3 }
choices:
  - into the steam gallery: steam-gallery
  - north, to the vault: the-vault-door
tasks:
  - turn a gear:
      roll: test, attribute: str, difficulty: 13
      rows:
        difficulty+: { text: The gear grinds a notch round. Somewhere a shutter lifts., adjust: gears, by: 1 }
        else: { text: The gear slips and clangs., adjust: alarm, by: 1 }
---
The alcoves are empty now. The figures that stood in them are turning their heads.

## GM
The sentinels that wake: one for every two heroes, rounded up, plus one for every 3 Alarm. Turning
gears makes the Steam Gallery worse (see its node) but opens the vault door.
