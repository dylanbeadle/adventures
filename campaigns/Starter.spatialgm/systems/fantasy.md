---
# A rule set renames things at the table. It never changes how the table works.
name: Fantasy (generic)
health: HP                 # what health is called
conditions:                # the order matters: up to 32, each "Name: symbol" (an SF Symbol)
  - Down: arrow.down.to.line
  - Poisoned: { symbol: drop.fill, attacks: worse }
  - Stunned: { symbol: sparkles, skips-turn: yes, attacked: better }
  - Blessed: { symbol: sun.max.fill, checks: +1, attacks: +1 }
  - Concentrating: brain.head.profile
movement: { speed: 40 }   # feet in a turn for a creature whose file says nothing (5 ft to a square)
hero-facts: [Ancestry, Class, Level]   # what a hero's name plate says, in order
resources:                 # what heroes spend (each "Name: symbol"); their maxima are in the hero's file
  - Spell slots: sparkles
  - Second wind: bolt.heart
  - Daggers: arrow.up.right
at-zero-health: Down       # the condition that means "out of the fight"
rolls:                     # saved rolls in the dice bag: name: dice
  Advantage: 2d20
  Disadvantage: 2d20
  Fireball: 8d6
  Ability Scores: 4d6
  Percentile: d100
license: CC0-1.0            # free to use, change and share
author: Spatial GM
stats:                     # what creatures may set (stats: { str: 2 } in a creature file)
  str: { name: Strength }
  dex: { name: Dexterity }
  wits: { name: Wits }
  armour: { name: Armour, default: 10 }
checks:                    # rolls that add a creature's stats; the GM gives the target number
  test:
    roll: d20 + @stat      # @stat: the stat the GM names ("a Dexterity test")
    vs: target
    rows:
      natural 20: A triumph — it works, and something more.
      natural 1: A disaster — it fails, and something goes wrong.
      target+: Success.
      else: Failure.
  attack:
    roll: d20 + str
    vs: armour
    rows:
      natural 20: { text: Critical hit — double the damage dice., hit: double }
      target+: { text: Hit., hit: yes }
      else: Miss.
  death-save:
    roll: d20
    rows:
      natural 20: { text: Back on your feet with 1 HP., heal: 1, to: active }
      natural 1: { text: Two failures., dying: fail, by: 2 }
      10+: { text: A success., dying: success }
      else: { text: A failure., dying: fail }
combat:
  attack: attack
  reach: 5 ft
  better: 2d20kh1
  worse: 2d20kl1
  far: worse
  dying: { roll: death-save, stable: 3, dead: 3 }
---
The rules a GM follows with this rule set. Rolls are made at the table: players throw their own
dice, the GM (or the story engine) rolls for the world.

## Checks
When the outcome is uncertain and down to a character, ask the player to roll `test` with the stat
that fits — Strength to force or lift, Dexterity to sneak, climb or dodge, Wits to notice, know or
talk — against a target: 10 is easy, 13 hard, 16 very hard. Without a stat that fits, use the
lowest of the three.

## Attacks
Roll `attack` against the target's Armour. On a hit roll the weapon's damage: d6 for most weapons,
d8 for big ones, d4 for a dagger or a sling. A creature at 0 health is down.
