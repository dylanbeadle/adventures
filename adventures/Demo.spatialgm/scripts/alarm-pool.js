// name: Alarm pool
// summary: Throw a d6 for each torch still burning; every 6 raises the alarm by one.
// license: CC0-1.0
// author: Spatial GM
//
// A rule script (Docs/CampaignFiles.md, section 10): the story runs it with { script: alarm-pool },
// the AI GM with its run_script tool. It reads the table as `facts`, throws dice with `dice.throw`
// and changes the story with `tools`.

const torches = facts.trackers.torches ?? 0;
console.log("Alarm pool: checking", torches, "torches");
if (torches === 0) return { sixes: 0, alarm: facts.trackers.alarm };

const thrown = await dice.throw(torches + "d6", { why: "the torches draw attention" });
const sixes = thrown.dice.filter((d) => d === 6).length;
const alarm = sixes > 0 ? (await tools.counter({ counter: "alarm", by: sixes })).new : facts.trackers.alarm;
return { sixes, alarm };
