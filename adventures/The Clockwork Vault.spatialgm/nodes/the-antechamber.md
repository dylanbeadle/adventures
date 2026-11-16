---
name: The antechamber
room: Antechamber
choices:
  - pick the lock: { script: lockpick-pool }
  - go through, once it's open: gear-hall
---
The brass door has no handle — only a lock of a hundred tumblers, and a dwarven word engraved
above it: *Patience.*

## GM
"Pick the lock" runs `scripts/lockpick-pool.js`: the GM Screen asks you to throw the pool. Every
5 or 6 is a success; with none, you may push once (the 1s stay). Two or more opens the door;
otherwise the Alarm rises. Pick again as often as you like — the Alarm is the cost.
