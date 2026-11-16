// name: Lockpick pool
// summary: Throw a pool of d6s for the best-handed hero; 5s and 6s are successes; push once; two opens the door.
// license: CC0-1.0
// author: Spatial GM
//
// The GM throws (seat 0), so it works at a table of one. Change `seat: 0` to 1–4 for a player.

const hands = facts.party.heroes.map((h) => ({ name: h.name, dex: h.attributes.dex ?? 0 }));
const best = hands.reduce((a, b) => (b.dex > a.dex ? b : a), hands[0] ?? { name: "someone", dex: 0 });
const size = Math.max(1, 2 + best.dex);

const first = await dice.throw(size + "d6", { seat: 0, why: best.name + " works the tumblers" });
let hits = first.dice.filter((d) => d >= 5).length;
let pushed = false;
if (hits === 0) {
  // A push rerolls everything that isn't a 1. It costs Alarm whatever happens.
  const again = first.dice.filter((d) => d !== 1).length;
  if (again > 0) {
    const second = await dice.throw(again + "d6", { seat: 0, why: best.name + " pushes their luck" });
    hits = second.dice.filter((d) => d >= 5).length;
    pushed = true;
    await tools.counter({ counter: "alarm", by: 1 });
  }
}

if (hits >= 2) {
  await tools.door({ target: "N24", to: "open" });
  await tools.say({ text: best.name + " hears the last tumbler fall. The brass door swings open.", to: "everyone" });
} else {
  await tools.counter({ counter: "alarm", by: 1 });
  await tools.say({ text: "Something deep in the vault clicks awake. (Alarm +1)", to: "everyone" });
}
return { hero: best.name, pool: size, hits, pushed, opened: hits >= 2 };
