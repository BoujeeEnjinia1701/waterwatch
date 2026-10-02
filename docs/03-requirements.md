---
doc_id: WWT-REQ-001
title: WaterWatch requirements
project: WaterWatch
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-02'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status from WWT-CAL-001 v0.3 for the constructable design (WWT-DDR-003); R12 stated against the value-engineering target
---

# WaterWatch requirements

These requirements were first set for the concept and are checked by calculation in WWT-CAL-001 v0.3. Version 0.4 applies Amish's decisions of 2026-09-25 (WWT-DDR-002): R1 is relaxed, R11 is restated for a footing cast on the survey visit, R5 gains a 15 min confirming reading and R12 now states that the pH probe variant is priced per variant site. The targets are still not user-validated needs and will be revised after co-design. On paper, no requirement is missed outright; four are at risk (R1, R10, R2 and R9), five are met by calculation and three by design, and the parts cost of the constructable design (WWT-DDR-003) is USD 19 over the USD 300 value-engineering target (R12). Version 0.5 updates the status for that design; no target changed. In v0.3, R1 and R10 were not met and R11 was at risk. Amish's decisions are in WWT-DDR-001 and WWT-DDR-002.

*Table 1. Requirements and TRL 3 status (from WWT-CAL-001 v0.3, Table 4), at-risk items first.*

| ID | Requirement | Target | Verification | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Measure free chlorine at the tap | 0 to 2.0 mg/L; within ±0.2 mg/L or ±25 %, whichever is greater, at pH 6.5 to 8.5 and 5 to 40 °C (relaxed from ±0.1 mg/L below 1.0 mg/L and ±15 % above, WWT-DDR-002). Sites whose pH is above 7.5 or moves more than 0.2 between visits use the pH probe variant | Error budget (WWT-CAL-001, E); later side-by-side with a DPD comparator | **At risk**: met in 8 of 8 cases at 25 °C before drift, with at least 0.13 mg/L left for drift; 1.5 mg/L at pH 7.5 and 40 °C misses by 0.006 mg/L; sensor drift unknown |
| R10 | Be maintainable by a caretaker | One visit per month or less, 30 min or less, no special tools: clean the cell, compare with a DPD kit, adjust calibration from a phone or keypad | Task analysis (WWT-CAL-001, J) | **At risk**: the visit takes 30 min, at the limit, and a monthly interval needs chlorine drift below about 0.13 mg/L per month under the relaxed R1 (was 0.04 mg/L), which no verified data show |
| R2 | Measure turbidity | 0 to 100 NTU, reporting "above 100 NTU" beyond; within ±0.5 NTU or ±10 %, whichever is greater | Published open-source design; bubble and settling calculation (WWT-CAL-001, F); later stabilized standards | **At risk**: the 30 s wait clears 100 µm bubbles at 5 °C; window fouling between cleans is unknown |
| R9 | Survive outdoors | Electronics IP65 or better; ambient 0 to 45 °C in direct sun; UV-stable parts; flow cell opaque to daylight; battery charging blocked below 0 °C and above 45 °C | Thermal estimate (WWT-CAL-001, C); parts selection | **At risk**: with the sun shield the inside peaks at 50.8 °C on a 45 °C day (69.8 °C without); the shield factor is assumed |
| R5 | Alert the people who act | SMS to up to three numbers within 15 min of a confirmed crossing (two consecutive readings, the second taken 15 min after the first crossing, WWT-DDR-002): free chlorine below 0.2 mg/L, turbidity above 5 NTU, device fault or low battery; thresholds adjustable per site | Latency calculation (WWT-CAL-001, H) | Met on paper where there is coverage: 13.0 min worst case with three tries at 3 min spacing; 77 min from the event (was 122 min) |
| R6 | Report and keep data | Upload readings at least every 4 h over LTE-M, NB-IoT or 2G (LoRaWAN variant); keep 90 days on board if the link fails; open CSV or JSON format; works without a cloud service | Data budget (WWT-CAL-001, G) | Met on paper: 0.86 MB per month; 90 days in 138 kB |
| R7 | Run on sunlight alone | 7 days or more with no sun from full; back to full in 3 clear days or fewer | Energy budget (WWT-CAL-001, A and B) | Met on paper: 28.6 days (24.3 at 0 °C); 1.18 clear days to refill; hot days rely on the sun shield (R9) |
| R8 | Use little treated water | 20 L/day or less at hourly sampling | Flow calculation (WWT-CAL-001, D) | Met on paper, thin margin: 18.0 L/day nominal, 19.8 L at the regulator's tolerance |
| R11 | Install simply and safely | Two people, 2 h or less on installation day, with the pole footing dug and cast on the survey visit (WWT-DDR-002); hand tools only; one tee and isolation valve on the riser; backflow prevented; wetted parts food-safe | Task analysis (WWT-CAL-001, J); design review | Met on paper: 65 min critical path on installation day (140 min if done in one visit); the design parts are met |
| R12 | Stay within the concept budget | Parts cost per base unit against a value-engineering target of $300 (a hypothetical control target, not a limit), excluding the shared calibration kit, airtime and the pH probe variant, which is priced per variant site (WWT-DDR-002) | Priced BOM (WWT-CAL-001, K) | Over the value-engineering target by $19: $319 per base unit for the constructable design; $379 to $419 at a pH probe variant site |
| R3 | Measure water temperature | 0 to 50 °C, within ±0.5 °C | Sensor datasheet | Met by design |
| R4 | Sample on a schedule | One reading per hour by default; configurable from 15 min to 24 h | Energy at the 15 min schedule (WWT-CAL-001, A and B) | Met by design (15 min schedule: 1.589 Wh/day, 9.7 days on battery, but 72 L/day of water) |
| R13 | Report measurements, not verdicts | Messages state what was measured and when; the device never says the water is "safe" | Design review of alert wording | Met by design |

## Assumptions

- Site: public tapstand on a piped, chlorinated rural scheme, with a supply pressure of 0.5 to 4 bar (7 to 58 psi) at the riser. Tapstands come first; tank outlets and kiosks later (WWT-DDR-001, D8).
- Alert thresholds follow the field guidance summarized in WWT-PRB-001: at least 0.2 mg/L free chlorine at the point of delivery, and chlorination losing effectiveness as turbidity rises. The defaults of 0.2 mg/L and 5 NTU were decided by Amish on 2026-09-25 (WWT-DDR-001, D6) and remain adjustable per site.
- The caretaker's DPD test is the field reference for free chlorine. The v0.3 target of ±0.1 mg/L matched the resolution of common DPD comparator kits, which WWT-CAL-001 showed made it as tight as the reference itself (the comparator alone takes ±0.07 mg/L); R1 was relaxed to ±0.2 mg/L or ±25 % for that reason (WWT-DDR-002).
- pH affects the split between hypochlorous acid and hypochlorite, and amperometric sensors respond mainly to hypochlorous acid. R1 is assessed with a site pH entered at installation and checked monthly (WWT-DDR-001, D2), assumed to move no more than ±0.2 between visits. Under WWT-DDR-002 the pH probe variant (read to ±0.1) is fitted at sites whose pH is above 7.5 or moves more than 0.2 between visits; the cell lid carries a plugged spare port for it.
- Budget: the $300 in `project.yaml` is a value-engineering target for one base unit's parts, not a spending limit (Amish, 2026-10-01). A shared calibration kit (about $60), airtime (about $1 to $3 per month) and, at variant sites only, the pH probe and interface (about $60 to $100) are listed separately; all are estimates.
- Installation: the pole footing is dug and cast on the survey visit, so the pole is set and cured before installation day (WWT-DDR-002).

> **Safety:** Meeting these requirements does not make the water safe to drink or the unit safe to install. The sample line connects to a pressurized drinking water supply and the unit contains a lithium iron phosphate battery; see WWT-PRC-001, Safety.
