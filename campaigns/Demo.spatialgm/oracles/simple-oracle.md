---
# A GM emulator: it answers what nobody wrote down. A campaign uses it with "oracle: simple-oracle"
# in campaign.md (the default is "oracle: none").
name: Simple Oracle
license: CC0-1.0           # free to use, change and share
author: Spatial GM
counters:
  chaos: { name: Chaos, start: 5, min: 1, max: 9, shown: everyone }
lists:
  threads: { name: Threads, max: 25 }
  characters: { name: Characters, max: 25 }
tables:
  answer:                  # the fate question: roll it with a modifier for how likely it is
    name: Answer
    roll: d6
    rows:
      1-: No, and…
      2: No.
      3: No, but…
      4: Yes, but…
      5: Yes.
      6+: Yes, and…
  event-focus:
    name: Event focus
    roll: d10
    rows:
      1-3: A thread moves → { pick: threads }
      4-6: Someone acts → { pick: characters }
      7-8: Something new → @action @subject
      9: An ending comes closer → { adjust: chaos, by: 1 }
      10: A thread resolves itself → { pick: threads }
  action:
    name: Action
    roll: d10
    rows: { 1: Seek, 2: Guard, 3: Betray, 4: Help, 5: Break, 6: Hide, 7: Hunt, 8: Bargain, 9: Flee, 10: Reveal }
  subject:
    name: Subject
    roll: d10
    rows: { 1: a secret, 2: a stranger, 3: food, 4: the past, 5: a weapon, 6: the law, 7: a home, 8: a debt, 9: a map, 10: the dead }
on:
  scene-start: Scene start
  scene-end: Scene end
---
Use this oracle when a question has no answer in the adventure: the players ask, the oracle
answers, and the GM (or the AI GM) turns the answer into what happens. It never overrides the
adventure: an adventure's own table with the same name replaces the oracle's.

## Fate question
Ask the player for a yes/no question about the world and how likely it is. Roll `answer`: +1 if
likely, +2 if very likely, −1 if unlikely, −2 if very unlikely. "And" adds something to the answer;
"but" takes something away. With chaos at 7 or more, a roll of 1 or 6 also brings a random event:
roll `event-focus`.

## Scene start
Say what the players expect the scene to be. Roll a d10: at or below `chaos`, the scene is
different — roll `event-focus` and change the scene to fit the result.

## Scene end
Ask: was the scene more under the party's control, or less? Less: `chaos` +1. More: `chaos` −1. Add
any new thread or character to their list; strike any that ended.

## Random event
When something surprising should happen (an answer with "and" at high chaos, a scene that changes),
roll `event-focus`, then read the result in the light of what's happening: who is acting, and what
they want.
