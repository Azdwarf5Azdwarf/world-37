// tickspeak.js — rosten, delad av strip.html och config.html
// Samma varden som robot/w4k7px.py. Andra dem bara pa ett stalle.

export const LJUD = {
  TICK_HZ: 1900,   // - tick, ljus klick
  TOCK_HZ: 780,    // _ tock, mork klick
  SYMBOL_MS: 45,   // langd pa en klick
  GAP_SYM_MS: 55,  // tystnad i samma bokstav
  GAP_BOK_MS: 210, // tystnad mellan bokstaver
  GAP_ORD_MS: 520, // tystnad mellan ord
};

export const STANDARD = {
  TICK_MS: 10000,  // en kolumn = en tick
  MAX_GRON: 6,     // lyckade verktygsanrop per tick = full gron
  MAX_ROD: 2,      // fel per tick = full rod
  MAX_BLA: 1,      // vante-handelser per tick = full bla
};

let ac = null;

export function vacka() {
  if (!ac) ac = new AudioContext();
  ac.resume();
  return ac;
}

function klick(t0, hz) {
  const o = ac.createOscillator(), g = ac.createGain();
  o.frequency.value = hz;
  o.connect(g); g.connect(ac.destination);
  const d = LJUD.SYMBOL_MS / 1000;
  g.gain.setValueAtTime(0, t0);
  g.gain.linearRampToValueAtTime(0.25, t0 + 0.004);
  g.gain.exponentialRampToValueAtTime(0.001, t0 + d);
  o.start(t0); o.stop(t0 + d);
}

/** Spelar ett monster: "-_-" = en bokstav, ["--","-_-"] = ett ord. */
export function saga(monster) {
  if (!ac) return;
  const bokstaver = Array.isArray(monster) ? monster : [monster];
  let t = ac.currentTime + 0.02;
  bokstaver.forEach((bok, bi) => {
    if (bi) t += LJUD.GAP_BOK_MS / 1000;
    [...bok].forEach((sym, si) => {
      if (si) t += LJUD.GAP_SYM_MS / 1000;
      klick(t, sym === '-' ? LJUD.TICK_HZ : LJUD.TOCK_HZ);
      t += LJUD.SYMBOL_MS / 1000;
    });
  });
}

/** Hamtar Claude Altairs alfabet fran robot/w4k7px.py via servern. */
export async function alfabet() {
  try { return await (await fetch('/alfabet.json')).json(); }
  catch (e) { return {}; }
}

/** Troskelvarden fran disk, med standard som botten. */
export async function installningar() {
  try {
    const sparat = await (await fetch('/installningar.json')).json();
    return { ...STANDARD, ...sparat };
  } catch (e) { return { ...STANDARD }; }
}

export async function spara(inst) {
  await fetch('/installningar.json', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(inst),
  });
}

/** Kanalvarde 0-1 -> en symbol. Tva nivaer, som alfabetet. */
export const sym = v => v >= 0.5 ? '-' : '_';
