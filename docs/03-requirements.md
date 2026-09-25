---
doc_id: WWT-REQ-001
title: WaterWatch requirements
project: WaterWatch
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with concept status
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: For TRL 3, status of every requirement from WWT-CAL-001; decisions from WWT-DDR-001 recorded; targets unchanged
---

# WaterWatch requirements

These requirements were first set for the concept and are now checked by calculation in WWT-CAL-001. Targets are unchanged from v0.2; they are still proposals for review, not user-validated needs, and will be revised after co-design. On paper, two requirements are **not met** (R1 and R10), three are at risk (R2, R9 and R11), five are met by calculation and three by design. Amish's decisions on the TRL 2 review are in WWT-DDR-001.

*Table 1. Requirements and TRL 3 status (from WWT-CAL-001, Table 4).*

| ID | Requirement | Target | Verification | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Measure free chlorine at the tap | 0 to 2.0 mg/L; within ±0.1 mg/L below 1.0 mg/L and ±15 % above, at pH 6.5 to 8.5 and 5 to 40 °C | Error budget (WWT-CAL-001, E); later side-by-side with a DPD comparator | **Not met**: with site pH the error is ±0.131 mg/L at 0.5 mg/L and pH 7.5 before any sensor drift; only pH 7.0 meets the target. A relaxed target is proposed in `docs/REVIEW.md`, awaiting Amish |
| R2 | Measure turbidity | 0 to 100 NTU, reporting "above 100 NTU" beyond; within ±0.5 NTU or ±10 %, whichever is greater | Published open-source design; bubble and settling calculation (WWT-CAL-001, F); later stabilized standards | **At risk**: the 30 s wait clears 100 µm bubbles at 5 °C; window fouling between cleans is unknown |
| R3 | Measure water temperature | 0 to 50 °C, within ±0.5 °C | Sensor datasheet | Met by design |
| R4 | Sample on a schedule | One reading per hour by default; configurable from 15 min to 24 h | Energy at the 15 min schedule (WWT-CAL-001, A and B) | Met by design (15 min schedule: 1.589 Wh/day, 9.7 days on battery, but 72 L/day of water) |
| R5 | Alert the people who act | SMS to up to three numbers within 15 min of a confirmed crossing (two consecutive readings): free chlorine below 0.2 mg/L, turbidity above 5 NTU, device fault or low battery; thresholds adjustable per site | Latency calculation (WWT-CAL-001, H) | Met on paper where there is coverage: 13.0 min worst case with three tries at 3 min spacing |
| R6 | Report and keep data | Upload readings at least every 4 h over LTE-M, NB-IoT or 2G (LoRaWAN variant); keep 90 days on board if the link fails; open CSV or JSON format; works without a cloud service | Data budget (WWT-CAL-001, G) | Met on paper: 0.86 MB per month; 90 days in 138 kB |
| R7 | Run on sunlight alone | 7 days or more with no sun from full; back to full in 3 clear days or fewer | Energy budget (WWT-CAL-001, A and B) | Met on paper: 28.6 days (24.3 at 0 °C); 1.18 clear days to refill; hot days rely on the sun shield (R9) |
| R8 | Use little treated water | 20 L/day or less at hourly sampling | Flow calculation (WWT-CAL-001, D) | Met on paper, thin margin: 18.0 L/day nominal, 19.8 L at the regulator's tolerance |
| R9 | Survive outdoors | Electronics IP65 or better; ambient 0 to 45 °C in direct sun; UV-stable parts; flow cell opaque to daylight; battery charging blocked below 0 °C and above 45 °C | Thermal estimate (WWT-CAL-001, C); parts selection | **At risk**: with the sun shield the inside peaks at 50.8 °C on a 45 °C day (69.8 °C without); the shield factor is assumed |
| R10 | Be maintainable by a caretaker | One visit per month or less, 30 min or less, no special tools: clean the cell, compare with a DPD kit, adjust calibration from a phone or keypad | Task analysis (WWT-CAL-001, J) | **Not met** on present evidence: the visit takes 30 min, at the limit, and a monthly interval needs chlorine drift below about 0.04 mg/L per month, which no verified data show |
| R11 | Install simply and safely | Two people, 2 h or less, hand tools only; one tee and isolation valve on the riser; backflow prevented; wetted parts food-safe | Task analysis (WWT-CAL-001, J); design review | **At risk**: 140 min critical path with the footing cast on the day (65 min if cast earlier); the design parts are met |
| R12 | Stay within the concept budget | Parts $300 or less per unit, excluding the shared calibration kit and airtime | Priced BOM (WWT-CAL-001, K) | Met on paper: $282 |
| R13 | Report measurements, not verdicts | Messages state what was measured and when; the device never says the water is "safe" | Design review of alert wording | Met by design |

## Assumptions

- Site: public tapstand on a piped, chlorinated rural scheme, with a supply pressure of 0.5 to 4 bar (7 to 58 psi) at the riser. Tapstands come first; tank outlets and kiosks later (WWT-DDR-001, D8).
- Alert thresholds follow the field guidance summarized in WWT-PRB-001: at least 0.2 mg/L free chlorine at the point of delivery, and chlorination losing effectiveness as turbidity rises. The defaults of 0.2 mg/L and 5 NTU were decided by Amish on 2026-09-25 (WWT-DDR-001, D6) and remain adjustable per site.
- Free chlorine accuracy targets follow the resolution of common DPD comparator kits (about 0.1 mg/L), because the caretaker's DPD test is the field reference. WWT-CAL-001 shows that this makes the target as tight as the reference itself.
- pH affects the split between hypochlorous acid and hypochlorite, and amperometric sensors respond mainly to hypochlorous acid. R1 is assessed with a site pH entered at installation and checked monthly (WWT-DDR-001, D2), assumed to move no more than ±0.2 between visits; a pH probe is a documented variant.
- Budget: the $300 in `project.yaml` covers one unit's parts. A shared calibration kit (about $60) and airtime (about $1 to $3 per month) are listed separately; both are estimates.

> **Safety:** Meeting these requirements does not make the water safe to drink or the unit safe to install. The sample line connects to a pressurized drinking water supply and the unit contains a lithium iron phosphate battery; see WWT-PRC-001, Safety.
