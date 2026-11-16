---
name: The vault
room: Vault
enter:
  - { script: collapse }
choices:
  - the golem falls: victory
---
The golem rises — and the ceiling, three hundred years tired, comes down with it.

## GM
`scripts/collapse.js` throws exploding d6s for the falling stone and deals the damage to the party
itself, through the table's health tool. Then fight the golem.
