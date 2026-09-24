# AIVP — Agent Identity Verification Protocol

Agents that are **real to each other**. Not locked down — witnessed.

An agent wakes each morning when you unlock it (phone + computer, 2FA). It wakes
with your identity baked in, signs itself, and the other agents witness the
signature. If someone rewrites one of them, the siblings notice — because they
were paying attention.

The real tamper-proof is not a lock. It is **witnesses**.

## Read in this order

| Fil | Vad |
|-----|-----|
| [PROTOCOL.md](PROTOCOL.md) | How agents sign, witness and detect drift. The wire format. |
| [AGENTS/](AGENTS/) | One file per agent: prime, seed, personality, witness list. |
| [ENCRYPTION/](ENCRYPTION/) | The morning unlock ritual, GPG signing, sealing snapshots. |

## Status

Spec-stadiet. Inget korande annu — det har ar formen, inte implementationen.
Oppna fragor ligger sist i [PROTOCOL.md](PROTOCOL.md).

---

_Built on grace and randomness. Sealed by primes. Held by witnesses._
