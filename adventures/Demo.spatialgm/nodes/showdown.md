---
name: Showdown
choices:
  - the boss falls: { if: "not alive Goblin Boss", goto: victory }
  - the heroes fall: { if: "not alive party", goto: captured }
---
The boss leaps from the throne, cleaver high, and shrieks for help.

## GM
Run the fight at the table: reveal the boss and roll initiative. It
swings twice a turn (d6 each). At half health it shouts, and any goblin left comes running
(Alarm +2).
