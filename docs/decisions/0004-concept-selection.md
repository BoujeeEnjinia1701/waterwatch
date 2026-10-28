---
doc_id: WWT-DDR-004
title: WaterWatch concept selection
project: WaterWatch
doc_type: Design decision record
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: concept selection among options A, B and C (WWT-OPT-001); proposed, awaiting Amish"
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Decided by Amish (2026-10-25, "i concur with your recommendations"): D1 option A, D2 shared photometer'
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** Decided by Amish, 2026-10-25 ("i concur with your recommendations"): D1, option A carried forward, and D2, the shared DPD photometer per operator as the monthly reference, both as recommended.

## Context

Kit 1.8 asks every idea for at least two concepts with different working principles, scored against the same user requirements before one is carried forward (STANDARDS section 21), and kit 1.9 asks for every option to be modelled to the repo's detail level (Amish, 2026-10-24: "Detail every option"). WaterWatch was designed before kit 1.8, so its current design is option A and is not redesigned without Amish's go. Two alternatives were defined with principles different from A's reagent-free amperometric flow cell: B, reagent DPD colorimetry in a cuvette analyser; C, potentiometric (ORP and pH) probes in the riser, reading during draws. All three are modelled to D3 in `cad/src/model.py` and pass the fidelity check (`cad/fidelity.json`).

## Options

Table 1. Options and scores (WWT-OPT-001, Table 2; maximum 245).

| Option | Working principle | Score | Strength | Weakness |
| --- | --- | --- | --- | --- |
| A. Timed-flush flow cell on its own pole | Hourly 90 s flush through a dark flow cell; 860 nm nephelometer and membrane-free amperometric chlorine sensor, no reagent | 196 | No chemicals, one tee on the riser, designed and calculated to TRL 3, USD 325 | Sensor drift over a month unknown (WWT-STM-001 S12, S14) |
| B. Reagent colorimetric analyser cabinet | Hourly sample in a cuvette, DPD reagent dosed by two pumps, read at 515 nm and 860 nm | 167 | The reference chemistry; reading independent of electrode drift and pH | Reagent resupply and heat life, chemical drain, pumps and tubing, cost about USD 380 to 450 (estimate) |
| C. In-riser probe manifold | ORP, pH, temperature and turbidity probes in a manifold cut into the riser, read during draws; no flushing | 155 | No water used, no pole, lightest | Loose chlorine estimate, electrodes in the drinking water path, riser cut, no readings when nobody draws |

## Recommendation (decided by Amish, 2026-10-25, as recommended)

- **D1. Carry option A forward.** It scores highest by 29 points (B is 15 % below, outside the 10 % band), adds no chemical, and leaves the tapstand unchanged but for one tee. Options B and C stay in the model as alternatives; B is the fallback if the TRL 4 drift test fails.
- **D2. Graft option B's best idea onto A:** a shared handheld DPD photometer per operator as the monthly calibration reference instead of the colour comparator, to cut the largest error term at low residual (±0.07 mg/L, WWT-CAL-001 E3). It is outside the unit cost (about USD 380 to 600 per operator for a cited instrument, WWT-MKT-001). If accepted, WWT-CAL-001 section E is re-run with the photometer's stated accuracy and PR-001 and PR-010 are reviewed.
- **Alternative to D1:** choose B now and redesign around the cuvette analyser, accepting reagent logistics for a reading that does not depend on the unproven sensor. Not recommended before the drift test, which would answer the question for about the cost of one bench setup.

## Consequences

- D1 accepted on 2026-10-25: `concept_chosen` in `project.yaml` is A; nothing else changes.
- D2 accepted on 2026-10-25: the operator's calibration kit holds the photometer and the build plan's first chlorine check reads against it; WWT-CAL-001 section E is rerun with its accuracy (E12) and PR-001 and PR-010 are reviewed (WWT-PRS-001 v0.8); the unit does not change.
- If B is chosen, the precis, requirements, calculations, BOM, drawing and build plan are redone for B (a new TRL 3 step).
