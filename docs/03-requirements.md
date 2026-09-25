---
doc_id: WWT-REQ-001
title: WaterWatch requirements
project: WaterWatch
doc_type: Requirements
version: "0.2"
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
---

# WaterWatch requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be checked by calculation at TRL 3 and revised after co-design sessions. Two requirements are **not met** on present evidence (R1 and R10) and two are at risk (R2 and R9); see the status column and WWT-PRC-001.

Table 1. Requirements and concept status.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Measure free chlorine at the tap | 0 to 2.0 mg/L; within ±0.1 mg/L below 1.0 mg/L and ±15 % above, at pH 6.5 to 8.5 and 5 to 40 °C | Literature and sensor data at TRL 3; later side-by-side with a DPD comparator | **Not met** on evidence: the low-cost membrane-free sensor is unproven over months, and the reading depends on pH, which is not measured |
| R2 | Measure turbidity | 0 to 100 NTU, reporting "above 100 NTU" beyond; within ±0.5 NTU or ±10 %, whichever is greater | Comparison with the published open-source design; later formazin standards | At risk: bench accuracy is published, but fouling and bubbles in continuous use are not |
| R3 | Measure water temperature | 0 to 50 °C, within ±0.5 °C | Sensor datasheet | Met by design |
| R4 | Sample on a schedule | One reading per hour by default; configurable from 15 min to 24 h | Firmware sketch review | Met by design |
| R5 | Alert the people who act | SMS to up to three numbers within 15 min of a confirmed crossing (two consecutive readings): free chlorine below 0.2 mg/L, turbidity above 5 NTU, device fault or low battery; thresholds adjustable per site | Design review; later timed trial | Met by design where there is cellular coverage |
| R6 | Report and keep data | Upload readings at least every 4 h over LTE-M, NB-IoT or 2G (LoRaWAN variant); keep 90 days on board if the link fails; open CSV or JSON format; works without a cloud service | Data budget calculation | Met by design |
| R7 | Run on sunlight alone | 7 days or more with no sun from full; back to full in 3 clear days or fewer | Energy budget calculation | Met by estimate (about 30 days; about 1.2 days to recharge) |
| R8 | Use little treated water | 20 L/day or less at hourly sampling | Flow calculation | Met by estimate (about 18 L/day), thin margin |
| R9 | Survive outdoors | Electronics IP65 or better; ambient 0 to 45 °C in direct sun; UV-stable parts; flow cell opaque to daylight; battery charging blocked below 0 °C and above 45 °C | Design review; later thermal estimate | At risk: enclosure temperature in full sun not yet estimated |
| R10 | Be maintainable by a caretaker | One visit per month or less, 30 min or less, no special tools: clean the cell, compare with a DPD kit, adjust calibration from a phone or keypad | Maintenance task analysis; later field trial | **Not met** on evidence: the chlorine sensor's drift and recalibration interval are unknown |
| R11 | Install simply and safely | Two people, 2 h or less, hand tools only; one tee and isolation valve on the riser; backflow prevented; wetted parts food-safe | Design review | Met by design |
| R12 | Stay within the concept budget | Parts $300 or less per unit, excluding the shared calibration kit and airtime | Priced BOM | Met by estimate (about $270) |
| R13 | Report measurements, not verdicts | Messages state what was measured and when; the device never says the water is "safe" | Design review of alert wording | Met by design |

## Assumptions

- Site: public tapstand on a piped, chlorinated rural scheme, with a supply pressure of 0.5 to 4 bar (7 to 58 psi) at the riser.
- Alert thresholds follow the field guidance summarized in WWT-PRB-001: at least 0.2 mg/L free chlorine at the point of delivery, and chlorination losing effectiveness as turbidity rises. The 5 NTU default is a conservative alert level, proposed, awaiting Amish and partner input.
- Free chlorine accuracy targets follow the resolution of common DPD comparator kits (about 0.1 mg/L), because the caretaker's DPD test is the field reference.
- pH affects the split between hypochlorous acid and hypochlorite, and amperometric sensors respond mainly to hypochlorous acid, so R1 assumes a site pH entered at installation and checked monthly unless a pH probe is added.
- Budget: the $300 in `project.yaml` covers one unit's parts. A shared calibration kit (about $60) and airtime (about $1 to $3 per month) are listed separately; both are estimates.
