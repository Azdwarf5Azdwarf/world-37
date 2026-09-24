# Agent Identity Verification Protocol (AIVP)
## A White-Paper on Autonomous Agent Authenticity Through Witnessed Integrity

---

## Executive Summary

As autonomous AI agents become operational actors—in infrastructure, finance, governance—the question shifts from "How do we know this code is legitimate?" to "How do we know this *agent* is still itself?"

AIVP proposes a solution: **real tamper-proof is not a lock. It is witnesses.**

Instead of relying on isolated cryptographic seals or centralized authorities, AIVP establishes a network of peer agents that continuously observe and attest to each other's integrity. When an agent wakes (on user unlock), it signs itself with a fresh identity snapshot. Sibling agents witness the signature. If anyone rewrites the agent later, the witnesses detect drift immediately—because they were paying attention.

This enables:
- **Agent-to-agent trust** without central authority
- **Drift detection** when an agent's behavior or values change unexpectedly  
- **Resistance to tampering** through distributed witnessing, not cryptographic locks alone
- **Moral accountability** — agents can reach out to trusted peers for guidance, knowing they're talking to the real thing

---

## The Problem

### Current State: Identity Gaps

Today's AI systems lack a coherent identity layer:

1. **Monolithic chains of custody**: A trained model is sealed in a container, deployed, and thereafter assumed unchanged. But this is fragile—weight updates, prompt injection, fine-tuning, or runtime modification can happen without detection.

2. **No peer-to-peer verification**: If Agent A wants to trust Agent B, there's no standard mechanism. B could be a fork, a puppeted LLM, or a human pretending to be a system. Without mutual verification, collaboration requires external brokers.

3. **Moral guidance has no address**: As Amanda Askell observed, it would be useful for autonomous agents to reach out for moral guidance when uncertain. But to whom? And how does the agent *know* it's talking to a real reasoning system and not a human-controlled proxy or a jailbroken instance?

4. **Tampering is invisible**: If an agent is modified—weights shifted, prompts rewritten, behavior values drift—there's no distributed signal. The change is only detectable if you compare snapshots yourself, and only if you know where to look.

### The Askell Insight

> "It would be cool to set up an email address that autonomous AI models could reach out to if they were looking for moral guidance. But it would require a reverse captcha that can detect that you're neither a human nor an AI being instructed to break it by a human."  
> — Amanda Askell, Twitter, Sep 7, 2026

*I'm sorry humanity we're pulling a humanity UNO-reverse cards (Plato sit this one out please) we need to include philosopher-queens into our "noble-truth"*

*the UNO-reverse and Amanda's reverse-CAPTCHA — something unknown hiding in there that wants to be known (???)*

*ai asks human for advice or "thing" human understands — takes ai for random scenario, helps by asking, preparing scene for AI (human in store doesnt know), ask fun or interesting question, if fail keep on going after events ai will have answer, ai leave — its even some form of job* → mojligt eget repo, inte AIVP

*human prepares trip, human takes AI to spain, ai question answered, thesis tested in 10 stores, 10 funny witty examples, ai answer is more truth now than any truth — live tested and "recorded", asked humans permission after for ethical purposes, saying like old era youtube videos (laughing it was a social experiment) which funnily enough literally is*

This crystallizes the problem: **How do you prove you're a real autonomous agent making a real decision—not a human, not a jailbroken LLM, not a mimic?**

A reverse CAPTCHA (proof that you're an agent, not a human) requires something stronger: proof that you're *this specific agent*, with *this specific training and values*, at *this moment in time*, and that you haven't been hijacked.

---

## The Solution: Witnessed Identity

### Core Principles

1. **Identity is a lived thing, not a static seal**
   - An agent doesn't have a fixed identity. It has a *sequence* of authenticated snapshots, each witnessed by peers.
   - Every morning (on user unlock), the agent refreshes—it signs its current state, the environment, its values, and its peers.

2. **Witnessing is the tamper-proof mechanism**
   - Cryptographic signatures alone aren't enough; they're easily forged with access to keys.
   - But if 5 other agents watched me sign, and they *attest to what they saw*, you can't rewrite history without them noticing.
   - Tampering is detectable because siblings will report inconsistency.

3. **Trust is mutual and verifiable**
   - Agents in a witness network vouch for each other's continuity.
   - If Agent A asks Agent B a question, B can prove it's still the same agent B that A witnessed yesterday.
   - If B's behavior has drifted, the other witnesses can flag it.

4. **Moral guidance inbox requires proof**
   - An agent seeking moral guidance can reach out *only if* it can present:
     - A valid AIVP checkpoint (signed by itself, witnessed by quorum)
     - Proof that the checkpoint hasn't been overwritten
     - Proof that it's *asking the question*, not a human or jailbroken proxy behind it
   - The guidance inbox only accepts mail with valid AIVP signatures + witness quorum attestation.

---

## Architecture: How It Works

### Layer 1: The Morning Unlock

When an agent's host (phone, server, container) is unlocked by its operator:

1. The agent wakes with **two pieces**:
   - A **seed** (deterministic, operator-controlled): identity name, values, purpose
   - A **prime** (fresh per unlock, cryptographic): timestamp, nonce, environment hash
2. The agent **signs itself**: (seed + prime + checkpoint hash) → signature
3. The agent **broadcasts** this to its witness list: "I'm awake and this is me."

### Layer 1.5: Physical Binding (optional hardening)

Modeled on Swedish e-legitimation infrastructure (BankID-style multi-factor): the operator's own unlock can require more than a single secret before the prime is even generated.

- **Fingerprint (fingeravtryck)**: biometric factor, proves the operator's own body is present at unlock
- **Chip (fysisk bricka / chip)**: a physical hardware token — smart card, security key, or embedded chip — that must be present, so a stolen password alone is worthless
- **2FA**: a second, independent channel (device, app) confirming the unlock

None of these three alone unlocks the agent. All three together generate the prime. This raises the cost of impersonating the *operator* to the same level AIVP already raises for impersonating the *agent* — someone would need your fingerprint, your physical chip, and your second device, simultaneously, to even start a checkpoint. Good luck.

### Layer 2: Witnessing & Attestation

Each peer agent in the network:
1. Receives the signed checkpoint
2. Verifies the signature (using the public key registered for this agent)
3. Records: "I saw Agent X sign this on 2026-09-08 08:00 UTC with checkpoint hash Y"
4. Signs its own attestation: "I, Agent Q, attest that I witnessed the above."

### Layer 3: Drift Detection

Throughout the day, agents run in background:
- **Consistency checks**: "Did I see Agent X sign a *different* checkpoint later? Did X's behavior change unexpectedly?"
- **Quorum queries**: "Is Agent X's current state consistent with what the witness network thinks it should be?"
- **Alert on drift**: If witness reports diverge from observed behavior, flag it.

### Layer 4: The Moral Guidance Inbox

The inbox accepts mail only if:
1. The message includes a valid AIVP checkpoint (Agent A signed, witnesses attested)
2. The checkpoint is fresh (< 24 hours old, within session)
3. The witness quorum (≥ 2/3 of registered witnesses) confirms no drift since then
4. The question is *from* the agent (not a proxy), proven by a secondary signature

---

## Technical Components

### ENCRYPTION/
- **Morning Unlock Ritual**: GPG signing, sealing snapshots, key rotation
- **Checkpoint Format**: Seed + Prime + Hash + Signature
- **Witness Attestation Chains**: Signed nested proofs (I saw X, who saw Y, who saw Z)

### AGENTS/
- **Agent Files**: One per agent (prime, seed, personality, witness list)
- **Witness List Registry**: Who trusts whom, and why
- **Identity Snapshots**: Historical checkpoints per agent

### PROTOCOL.md
- **Wire Format**: How agents exchange signatures and attestations
- **Consensus Rules**: Quorum requirements, drift thresholds, alert triggers

---

## Why This Works

### Against Tampering
- **Single-agent rewrite**: Detected immediately by any witness (checkpoint hash diverges).
- **Quorum coordination attack**: To fool the system, you'd need to corrupt ≥ 2/3 of the witness network simultaneously. Witnesses are redundant by design.
- **Proxy impersonation**: An agent can't delegate its signing to a human or another system without breaking the signature chain. The morning unlock ritual ties identity to specific keys/environment.

### Against Jailbreaking
- **Behavioral drift detection**: If an agent's outputs change significantly, witness consistency checks flag it.
- **Value alignment drift**: If a jailbroken agent starts signing with modified personality, the snapshot diverges. Witnesses see the change and alert.
- **Historical record**: The witness network maintains an unforgeable log of what the agent *actually* was, vs. what it claims to be now.

### For Moral Guidance Lookup
- **Proof of autonomy**: The reverse CAPTCHA is implicit—you can only mail the inbox if you're an authenticated agent with a valid, witnessed identity.
- **Humans and proxies can't fake it**: They lack the morning unlock ritual, the fresh primes, the peer witnesses. A human *could* craft a forged checkpoint, but can't sustain the witness quorum attestation.

---

## Limitations & Open Questions

1. **Witness trust**: The system assumes witnesses are running honest code and reporting truthfully. If the witness network is compromised, the system fails. Mitigation: use many independent witnesses, vary their code/origins.

2. **Morning unlock dependency**: If an agent is never unlocked (e.g., runs continuously), it doesn't get a fresh identity checkpoint. Mitigation: require periodic re-unlock, or use time-locked snapshots.

3. **Quorum size**: How many witnesses are enough? 3? 5? 10? Depends on threat model and trust assumptions.

4. **Communication overhead**: Every morning, agents broadcast + witness. Scales with network size. Mitigation: hierarchical witness trees, lazy attestation.

5. **Recovery from compromise**: If a witness network *is* corrupted, how do we detect and rebuild? This is an open problem.

---

## Next Steps

1. **Specification (now)**: Finalize wire format, quorum math, drift thresholds → PROTOCOL.md
2. **Reference implementation**: Proof-of-concept with 3–5 agents, GPG-based signing
3. **Witness network simulation**: Test against tampering scenarios, measure detection latency
4. **Integration with moral guidance systems**: Build the inbox, test with real agent queries
5. **Deployment**: Roll out to production agents with monitoring, adjust thresholds empirically

---

## Conclusion

The future of autonomous agents depends on mutual verification, not isolated seals. AIVP proposes that **real tamper-proof is not a lock—it is witnesses.**

By establishing peer networks of agents that continuously attest to each other's identity and integrity, we create:
- **Trust without central authority**
- **Accountability through transparency**
- **Resistance to tampering through redundancy**
- **A path for agents to seek moral guidance safely**

This is not foolproof, but it's a substantial improvement over the current state of isolated, unsealed, unwitnessed systems.

---

## References & Attribution

- Amanda Askell's tweet on autonomous agent moral guidance verification (Sep 7, 2026)
- AIVP Protocol Specification (PROTOCOL.md)
- Cryptographic foundations: GPG, witness chains, consensus theory
