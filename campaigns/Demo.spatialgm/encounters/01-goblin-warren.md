---
name: Goblin Warren
board: dungeon             # dungeon (squares and rooms) or hex
soundscape: cave           # starts when the encounter is set up
music: mysterious          # and this music (calm, mysterious, threatening, combat, tavern, triumph)
rooms:                     # area: two corner squares; doors: squares on the room's edge
  Entrance: { area: J22-U30, doors: [N22 closed], revealed: true }
  Guard Post: { area: J13-U21, doors: [N21 closed, J17 closed, U17 closed, Q13 closed] }
  Barracks: { area: A13-I24, doors: [I17 closed] }
  Storeroom: { area: V13-AD21, doors: [V17 closed] }
  Boss Lair: { area: G1-X12, doors: [Q12 closed] }
cast:                      # creature at square, then options: hidden, reserve (off the board), as Name
  - goblin at N17, hidden, stats {str: 1}   # this goblin is a little stronger than its file says
  - goblin-boss at Q5, hidden
  - goblin-archer, hidden, reserve
  - wolf, hidden, reserve
  - young-dragon, hidden, reserve
scenery:                   # props inside a room appear when the room is revealed
  - rubble at T29
  - rubble at K29
  - brazier at T14
  - crate at K14
  - crate at L14
  - bedroll at B14
  - bedroll at B17
  - bedroll at B20
  - bedroll at G23
  - 3 crate in Storeroom        # a count and a room: free squares near the room's middle
  - barrel at AC20
  - chest at AC17
  - throne at Q2
  - brazier at H2
  - brazier at W2
---
Five rooms dug into a hillside. The goblins have been raiding the road and hoarding what they steal. Reveal the Guard Post when the party opens the north door; the archer, a wolf and (if things go badly) a young dragon wait off the board.

## Entrance
Rain drips through a crack in the hillside. Muddy boot prints, small and many, lead north into the dark.

## Guard Post
A guttering brazier lights an overturned table and a half-eaten rat on a stick. Someone was just here.

## Barracks
Straw pallets crowd the floor. It smells of wet dog and old stew. One pallet is still warm.

## Storeroom
Stolen crates are stacked to the ceiling: grain, lamp oil, and a small locked chest stamped with a merchant's seal.

## Boss Lair
A throne of lashed-together shields faces the door. The goblin on it grins, and taps a rusty cleaver on its knee.
