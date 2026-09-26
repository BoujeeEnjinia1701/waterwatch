---
doc_id: WWT-DDR-002
title: WaterWatch recommendations accepted
project: WaterWatch
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items D11 to D14; items O1 to O3 remain proposed

## Context

After the TRL 3 session, `docs/REVIEW.md` (session 2026-09-25, TRL 3) listed two new items awaiting Amish, each with a recommendation (the R1 target and the pH probe trigger), and two suggestions offered with a recommendation to adopt them (a 15 min confirming reading and casting the footing on a survey visit). On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided in favor of that recommendation; where several options were offered, the recommended option is the decision. Items with no recommendation stay open. The items D1 to D10 in WWT-DDR-001 were already decided and are unchanged. TRL 4 remains on hold by Amish's instruction, and nothing here authorizes building, testing or purchasing.

## Decision

*Table 1. Newly decided items and what changed in the repo.*

| # | Item | Decision | What changed |
| --- | --- | --- | --- |
| D11 | R1 free chlorine target | Option (b): relax R1 from ±0.1 mg/L below 1.0 mg/L and ±15 % above to ±0.2 mg/L or ±25 %, whichever is greater. Decided by Amish, 2026-09-25: go with recommendation. | WWT-REQ-001 v0.4, R1 target restated. WWT-CAL-001 v0.2, section E: cases meeting R1 at zero drift rise from 2 of 8 to 8 of 8 (with D12); room for drift from 0.038 to 0.130 mg/L. R1 moves from not met to at risk; R10 from not met to at risk (drift allowance about 0.13 mg/L per month, was 0.04). |
| D12 | pH probe trigger | Fit the pH probe variant at sites whose pH is above 7.5 or moves more than 0.2 between visits; site pH (WWT-DDR-001, D2) elsewhere. Decided by Amish, 2026-09-25: go with recommendation. | Design change: the cell lid gains a spare 12 mm port with a blanking plug (`cad/src/model.py`, STEP and STL re-exported; WWT-DWG-001 Rev P1 to P2; BOM item 9 $12 to $13, total $282 to $283). WWT-REQ-001 v0.4, R12 restated: the pH probe (about $60 to $100, estimate) is priced per variant site, outside the $300 base-unit budget; a variant unit costs about $343 to $383. `budget_usd` stays at $300. |
| D13 | Confirming reading | Firmware rule: after a first threshold crossing, take the confirming reading 15 min later instead of at the next hour. Decided by Amish, 2026-09-25: go with recommendation. | WWT-REQ-001 v0.4, R5 restated; WWT-PRC-001 v0.4, How it works. WWT-CAL-001 v0.2, H2 and H3: worst case from event to SMS 122 min to 77 min, at 9.7 mWh and 0.75 L per event. Recorded as a rule; firmware beyond a sketch is TRL 4 work and is on hold. |
| D14 | Footing on the survey visit | Dig and cast the pole footing, with the pole set, on the survey visit before installation day. Decided by Amish, 2026-09-25: go with recommendation. | WWT-REQ-001 v0.4, R11 restated as 2 h on installation day. WWT-CAL-001 v0.2, J2: installation day critical path 140 min to 65 min. R11 moves from at risk to met on paper. |

No pitch, problem or `budget_usd` change was recommended, so `project.yaml` is unchanged; `trl` and `trl_target` stay at 3.

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and region (WWT-DDR-001, O1). Community designs pick co-design partners per area later. | Proposed, awaiting Amish |
| O2 | Alert language and recipients beyond the R13 rule; no recommendation was made. | Proposed, awaiting Amish |
| O3 | Data ownership and access; no recommendation was made. | Proposed, awaiting Amish |

## Consequences

- Requirement status (WWT-CAL-001 v0.2): 0 not met, 4 at risk (R1, R10, R2, R9), 6 met on paper, 3 met by design. Before: 2 not met, 3 at risk, 5 met on paper, 3 met by design.
- At 40 °C, 1.5 mg/L free chlorine at pH 7.5 with site pH misses the relaxed R1 by 0.006 mg/L (WWT-CAL-001, E7). Warm-water sites near pH 7.5 are candidates for the pH probe under the same rule.
- Controlled documents revised: WWT-PRC-001 v0.4, WWT-REQ-001 v0.4, WWT-CAL-001 v0.2, WWT-DDR-001 v0.2; drawing WWT-DWG-001 Rev P2; concept media regenerated.
- No cross-repo action arises from these items.
- R1 and R10 now hinge on the chlorine sensor's drift, which only a bench test can settle. That is TRL 4 work and is on hold.
