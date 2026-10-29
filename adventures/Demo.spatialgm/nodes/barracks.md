---
name: The barracks
room: Barracks
tasks:
  - search the pallets:
      roll: test, attribute: wits, difficulty: 10
      rows:
        difficulty+: { text: Under the warm pallet, a small iron key., add: { list: clues, entry: the chest key } }
        else: { text: Straw, bones and fleas. Something stirs in the dark., roll: wandering-goblins }
choices:
  - back to the guard post: guard-post
---
Straw pallets crowd the floor. It smells of wet dog and old stew. One pallet is still warm.
