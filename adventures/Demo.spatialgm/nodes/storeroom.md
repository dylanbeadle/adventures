---
name: The storeroom
room: Storeroom
choices:
  - unlock the chest with the key: { if: "has clues the chest key", goto: strongbox, else: locked }
  - back to the guard post: guard-post
tasks:
  - force the lock:
      roll: test, attribute: str, difficulty: 14
      rows:
        difficulty+: strongbox
        else: { text: The lock holds and clangs like a bell., adjust: alarm, by: 2 }
---
Stolen crates are stacked to the ceiling: grain, lamp oil, and a small locked chest stamped with a
merchant's seal.
