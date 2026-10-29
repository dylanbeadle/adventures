---
# A rule set renames things at the table. It never changes how the table works.
name: Fantasy (generic)
health: HP                 # what health is called
experience: XP              # what experience is called (the GM's XP control shows with it)
conditions:                # the order matters: up to 32, each "Name: icon" (an SF Symbol)
  - Down: arrow.down.to.line
  - Poisoned: { icon: drop.fill, attacks: worse }
  - Stunned: { icon: sparkles, skips-turn: yes, attacked: better }
  - Blessed: { icon: sun.max.fill, tasks: +1, attacks: +1 }
  - Concentrating: brain.head.profile
movement: { speed: 40 }   # feet in a turn for a creature whose file says nothing (5 ft to a square)
plate: [ancestry, class, level]   # the attributes a hero's name plate shows, in order
trackers:                  # what heroes spend, by id (each "id: Name" or "id: { name, icon }"); their maxima are in the hero's file
  spell_slots: { name: Spell slots, icon: sparkles }
  second_wind: { name: Second wind, icon: bolt.heart }
  daggers: { name: Daggers, icon: arrow.up.right }
at-zero-health: Down       # the condition that means "out of the fight"
rolls:                     # saved rolls in the dice bag: name: dice
  Advantage: 2d20
  Disadvantage: 2d20
  Fireball: 8d6
  Ability Scores: 4d6
  Percentile: d100
license: CC0-1.0            # free to use, change and share
author: Spatial GM
attributes:                     # what creatures may set (attributes: { str: 2 } in a creature file)
  str: { name: Strength }
  dex: { name: Dexterity }
  wits: { name: Wits }
  armour: { name: Armour, default: 10 }
  ancestry: Ancestry
  class: Class
  level: Level
tasks:                     # rolls that add a creature's attributes; the GM gives the difficulty
  test:
    roll: d20 + @attribute # @attribute: the attribute the GM names ("a Dexterity test")
    vs: difficulty
    rows:
      natural 20: A triumph — it works, and something more.
      natural 1: A disaster — it fails, and something goes wrong.
      difficulty+: Success.
      else: Failure.
  attack:
    roll: d20 + str
    vs: armour
    rows:
      natural 20: { text: Critical hit — double the damage dice., hit: double }
      difficulty+: { text: Hit., hit: yes }
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
