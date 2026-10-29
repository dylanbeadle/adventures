---
# The campaign's settings. Every other file lives in a folder next to this one.
format: 2
name: Demo Campaign
id: 5a1e7ab1-0000-4000-8000-000000000001   # written by the app; leave it alone
uses-rule-set: fantasy            # which file in rule-sets/ the table starts with
first-encounter: goblin-warren
template: true             # offered under New from Template
cover: cover.png
summary: A goblin warren ambush and the haunted ruins of Vell's Strongbox.
instruments: media/instruments/orchestra.sf2   # the SoundFont the music plays on (GeneralUser GS, see its licence)
opens-first: true          # the headset opens this campaign when nothing else was open
license: CC0-1.0           # free to use, change and share
author: Spatial GM
oracle: simple-oracle      # answers what the adventure doesn't say (oracles/); "none" for no oracle
first-node: the-letter     # the story starts here (nodes/)
gm: person                 # who runs the table: person, assist (the AI suggests) or ai
monsters: auto             # C3: auto, ai or gm (D136)
global-trackers:           # numbers the story keeps (start, min-value, max-value); everyone sees them
  alarm: { name: Alarm, start: 0, min-value: 0, max-value: 4 }
  torches: { name: Torches, start: 6, min-value: 0, max-value: 6 }
  strongbox: { name: Strongbox found, max-value: 1 }
lists:
  clues: { name: Clues }
on:                        # when this happens: a ## section below to follow, or effects to run
  round-start: [{ adjust: torches, by: -1, every: 10 }]
  global-tracker-empty torches: Darkness
  party-down: [{ goto: captured }]
  foes-down: [{ if: "visited showdown", goto: victory }]
  creature-half Goblin Boss: [{ adjust: alarm, by: 2 }]
  combat-end: [{ roll: goblin-loot }]
avoid: [harm to animals shown in detail]
---
# Demo Campaign

![Cover](cover.png)

Built into Spatial GM so there is always something to play: a goblin warren under a rainy hillside, and an ambush on the forest road.

This campaign is also a solo adventure, **Vell's Strongbox**: open the GM Screen's Story page and
follow the nodes, or let the AI GM run it. The heroes sneak into the goblin warren to bring back a
merchant's strongbox before the goblins notice them.

## Darkness
The last torch gutters out. Until the heroes find light, every check is one harder (+2 to its
target), and the goblins, who see in the dark, act first in every round.
