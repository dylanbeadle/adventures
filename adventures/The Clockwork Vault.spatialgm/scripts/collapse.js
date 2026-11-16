// name: Collapse
// summary: Exploding d6s of falling stone, dealt to the whole party.
// license: CC0-1.0
// author: Spatial GM

// One die per gear turned, at least two; a 6 explodes (throw another), up to ten extra dice.
let pool = Math.max(2, facts.trackers.gears ?? 0);
let total = 0;
let thrown = [];
let extra = 0;
while (pool > 0 && extra <= 10) {
  const roll = await dice.throw(pool + "d6", { why: "the ceiling comes down" });
  thrown = thrown.concat(roll.dice);
  total += roll.total;
  pool = roll.dice.filter((d) => d === 6).length;
  extra += pool;
}
await tools.health({ target: "party", by: -total });
await tools.say({ text: "Stone thunders down: " + thrown.join(", ") + " — " + total + " damage to everyone.", to: "everyone" });
return { dice: thrown, total };
