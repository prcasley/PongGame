# Realistic 3D "Pong 2K26" Production Plan

## Vision
Create a modern, ultra-polished 3D Pong experience that feels like a premium sports title while preserving classic Pong readability and responsiveness.

## Core Design Pillars
1. **Instant gameplay clarity** (ball and paddle are always trackable).
2. **Photoreal presentation** (PBR materials, cinematic lighting, high-fidelity post-processing).
3. **Esports-grade responsiveness** (stable framerate, low input latency, deterministic ball physics).
4. **Modular production workflow** so two AI collaborators (you + Claude) can build in parallel.

## Recommended Tech Stack
- **Engine:** Unreal Engine 5.4+ (Lumen + Nanite + Movie Render Queue for promo shots).
- **Modeling/Texturing:** Blender + Substance 3D Painter (or Blender-only with PBR node workflows).
- **Version control:** Git + Git LFS for large binaries.
- **Project management:** GitHub Projects board with milestone-based sprints.

## Game Scope (MVP -> Vertical Slice -> Final)

### MVP (Week 1–2)
- 3D arena blockout.
- Two controllable paddles.
- Ball physics with deterministic bounce rules.
- Score system + round reset.
- Basic camera follow and UI.

### Vertical Slice (Week 3–6)
- Finalized hero arena art direction.
- Cinematic intro, dynamic crowd/ambience audio.
- PBR materials, polished shaders, lighting pass.
- Enhanced VFX (trail, impact sparks, subtle motion blur).
- Match flow: intro, gameplay, replay stinger, win screen.

### Final Polish (Week 7–10)
- Quality/performance profiles (Low/High/Epic).
- Advanced post-processing tuning.
- Accessibility and control remapping.
- Audio mastering + haptics.
- Bug bash and playtesting.

## Art Direction Blueprint (Ultra-Real)
- **Theme:** Futuristic indoor sports arena with reflective polymer floor and volumetric spotlighting.
- **Color script:** Cool dark base with high-contrast neon accents for gameplay readability.
- **Material set:**
  - Ball: polished composite shell with micro-surface roughness.
  - Paddles: carbon fiber body + emissive edge strips.
  - Arena: brushed metal, tempered glass, LED trim.
- **Realism rules:**
  - Physically plausible scale and roughness.
  - Motivated light sources only.
  - Controlled bloom and chromatic aberration (never obscure gameplay).

## Camera, Animation, and Presentation
- Gameplay camera: fixed side view with subtle dynamic parallax.
- Intro camera: cinematic dolly + focal rack.
- Scoring moments: 0.5–1.0 second time dilation pulse + replay angle.
- Paddle animation: micro-lean and servo damping to avoid robotic motion.

## Physics and Feel (Most Important)
- Run game physics on fixed timestep.
- Ball speed ramps per rally with cap to maintain fairness.
- Bounce angle depends on contact offset from paddle center.
- Add tiny spin influence but prevent chaotic trajectories.
- All “juice” effects (camera shake, particles) must not alter core simulation.

## Audio Design
- Layered paddle-hit sounds (impact + servo + arena slapback).
- Different materials trigger unique collision timbres.
- Dynamic mix: crowd/ambience ducks slightly during high-speed rallies.
- Victory sting + announcer pack optional for “sports broadcast” vibe.

## Performance Targets
- **PC High:** 1440p at 120 FPS target.
- **Fallback:** 1080p at stable 60 FPS on mid-tier GPUs.
- Budgets:
  - Draw calls, shader complexity, and post-processing measured each sprint.
  - VFX budgets capped to protect frame pacing.

## QA / Playtest Checklist
- No camera angle hides ball trajectory.
- Input delay feels instant on keyboard/controller.
- Scoring/reset has no desync or stuck states.
- Visual effects never reduce competitive readability.
- Match can run for 30+ minutes without perf drift.

---

## Collaboration Framework: You + Claude + Me

### Role Split
- **You (Creative Director/Product Owner):** Vision decisions, priority calls, final approvals.
- **Claude (Systems + Implementation Drafting):** Architecture, gameplay systems pseudocode, test plans.
- **Me (Integration + Production Lead):** Task decomposition, acceptance criteria, build sequencing, quality gates.

### How We Work Together (Per Feature)
1. **You define intent** in 3 bullets (goal, constraints, must-have quality bar).
2. **Claude proposes implementation options** (A/B/C with tradeoffs).
3. **I convert chosen option into execution tickets** with:
   - exact task steps,
   - done criteria,
   - risk checks,
   - test commands/checklists.
4. **Claude drafts first-pass assets/scripts specs**.
5. **I run integration review** (naming conventions, dependency order, perf impact).
6. **You approve/reject with notes**.

### Prompt Template for Claude (Reusable)
Use this exact format when handing work to Claude:

```text
Project: Pong 2K26 (ultra-realistic 3D pong)
Current Milestone: [MVP / Vertical Slice / Polish]
Feature: [e.g., Ball Physics v2]
Goal: [what good looks like]
Constraints:
- Keep gameplay readable.
- Maintain [target FPS].
- Keep deterministic behavior.
Deliverables:
1) Implementation plan
2) Pseudocode / blueprint logic
3) Edge-case list
4) Test checklist
Output format: concise markdown with headings.
```

### Definition of Done (Global)
A task is done only if all are true:
- Functionally correct.
- Meets visual quality target.
- Meets performance budget.
- Includes regression checklist.
- Has rollback plan if it breaks build stability.

## 10-Week Sprint Map
- **Sprint 1:** Core movement/physics + camera blockout.
- **Sprint 2:** Score/state flow + UI wireframes + first playable.
- **Sprint 3:** Hero arena model + lighting pass 1.
- **Sprint 4:** Materials/textures + VFX pass 1.
- **Sprint 5:** Audio implementation + cinematic intro.
- **Sprint 6:** Gameplay balancing + replay moments.
- **Sprint 7:** Optimization pass 1 + bug fixing.
- **Sprint 8:** Accessibility + control polish.
- **Sprint 9:** Final art polish + trailer captures.
- **Sprint 10:** Final QA and release candidate.

## Immediate Next Actions (Start Today)
1. Lock engine choice (UE5 recommended).
2. Create Git repo structure (`/Game`, `/Art`, `/Audio`, `/Docs`).
3. Build greybox MVP in 48 hours.
4. Run first playtest focused only on ball readability and input feel.
5. Review findings, then begin Vertical Slice backlog.
