---
format: 2
name: The Clockwork Vault
id: 16910be7-0a79-4e0e-8a69-765685996dc3   # written by the app; leave it alone
uses-rule-set: fantasy
first-encounter: the-vault
first-node: the-antechamber
gm: person
oracle: none
colors:
  blue: "#3373F2"
  purple: "#9959E6"
  green: "#33B366"
  gold: "#F2BF33"
  orange: "#F28026"
license: CC0-1.0
author: Spatial GM
global-trackers:
  alarm: { name: Alarm, start: 0, min-value: 0, max-value: 6 }
  gears: { name: Gears turned, start: 0, min-value: 0, max-value: 3 }
on:
  global-tracker-full alarm: Lockdown
---
A short showcase of **rule scripts** (`scripts/`) and **formulas that read the table**, built to try
on Vision Pro. Three heroes break into a dwarven vault whose machinery still runs.

What to look for, in play order:

1. **The lock** (Antechamber): a script asks *you* to throw a pool of dice, counts the 5s and 6s,
   lets you push once, then opens the door or raises the Alarm through the table's own tools.
2. **The sentinels** (Gear Hall): how many wake is a formula — one for every two heroes, rounded up,
   plus more as the Alarm climbs (`times: ceil(party / 2) + tracker(alarm) / 3`).
3. **The steam** (Steam Gallery): a condition that hurts every round, by an amount a script looks up
   from two keys — how many gears are turned and how loud the Alarm is.
4. **The collapse** (Vault): a script throws exploding dice and deals the damage itself.

Run it as the GM from the GM Screen's Story page, or set **gm: ai** above and ask the AI GM to
"run the lockpick script".

## Lockdown
Every shutter in the vault slams down. The sentinels stop pretending to be furniture.
