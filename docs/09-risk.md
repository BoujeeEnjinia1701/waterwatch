---
doc_id: WWT-RSK-001
title: WaterWatch risk register and hazard analysis
project: WaterWatch
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: project risks, preliminary hazard analysis and first-pass design FMEA for option A"
---

# WaterWatch risk register and hazard analysis

The top risks are that the low-cost chlorine sensor drifts faster than a monthly calibration can absorb, so alerts go wrong in both directions, and that people read a quiet sensor as proof the water is safe. The largest hazards are contamination of the supply through the sample line, the lithium cell in a hot enclosure, and the pole. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found) to 5 (unlikely to be found).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Chlorine drift beyond the monthly allowance | Membrane-free graphite sensor and pseudo-reference drift (WWT-STM-001 S12, S14) | False alarms or missed loss of residual; operators stop trusting alerts | 4 | 5 | Design lead | Bench drift test is the first TRL 4 task; fallback is option B's DPD chemistry or a membrane probe at higher cost |
| P2 | No partner adopts it | Water Mission not yet approached; operators may prefer proven commercial analysers | No pilot sites, no field data | 3 | 4 | Project lead | Approach the first candidate with this TRL 3 pack; offer co-design of thresholds and alerts |
| P3 | Cost above the value-engineering target | USD 325 against USD 300; recurring airtime | Fewer points monitored per budget | 3 | 2 | Design lead | LoRaWAN variant where a gateway exists (about USD 304); bulk fixings and plates |
| P4 | Network coverage too weak at the site | Rural LTE-M or 2G gaps | Late or lost alerts | 3 | 3 | Scheme operator | Survey signal at each site; pole-top antenna or LoRaWAN variant (WWT-DDR-003 A2) |
| P5 | Vandalism or theft | Panel, battery and modem are of value | Loss of the unit | 3 | 3 | Scheme operator | Tamper-resistant shield screws on field units (WWT-DEC-001); community ownership |
| P6 | Type approval delays | Radio equipment rules in the chosen country (WWT-REG-001 R7) | No legal field installation | 3 | 3 | Electronics lead | Use a modem module already approved in the country |
| P7 | Sun shield less effective than assumed | Shield factor of 0.25 assumed (S5) | Battery too hot to charge on hot days | 3 | 3 | Design lead | Log enclosure temperature at TRL 4; larger gap or a second reflective layer |
| P8 | Lightning, static and condensation | Exposed pole and panel; daily temperature swings in a sealed box | Board or modem damage; corrosion | 2 | 3 | Electronics lead | Pole bonded to the footing; surge protection on the panel and antenna leads; pressure-equalising vent and a desiccant pack; to assess at TRL 4 (independent review, 2026-10-25) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Contamination of the drinking water supply | Backflow from the cell or drain into the riser; unsafe wetted materials | Illness of people who drink from the tap | 5 | 1 | Isolation valve and two check valves in series (supply train and cell inlet, WWT-DEC-001 F8) with the normally closed valve; open air break at the cell outlet so drain water cannot reach the cell (PR-014, WWT-STM-001 S8, S30); food-contact grades upstream of the check valve | Low |
| H2 | Reading taken as proof the water is safe | A normal reading does not cover pathogens or chemicals | Illness if lab testing stops | 4 | 3 | Alerts state measurements only (PR-013); documentation and training say laboratory testing stays necessary | Medium |
| H3 | Lithium cell overheats or is overcharged | Hot enclosure, charger fault, damaged cell | Burns, fire in the enclosure | 4 | 2 | LiFePO4 chemistry; protection board, fuse at the cell, 0 to 45 °C charge window (PR-016); ventilated sun shield; UN 38.3 cells | Low |
| H4 | Pole falls or is struck | Poor footing, high wind, impact | Injury to people at the tapstand | 4 | 1 | 300 x 600 mm footing cast on the survey visit, factor 4.3 in dry sand and 2.2 saturated in a 35 m/s gust (S17); pole stress factor 4.0 (S16) | Low |
| H5 | Sharp edges and pinch points | Cut plates, U-bolt ends, shield edges | Cuts to caretakers and children | 2 | 3 | Edges broken on every cut part (model, build plan); U-bolt ends inside the shield | Low |
| H6 | Chemical exposure during calibration | DPD tablets; turbidity standards | Skin or eye irritation; toxic precursors if formazin is made locally | 3 | 2 | Prepared, stabilised standards only; gloves; supplier safety data sheets (S24) | Low |
| H7 | Flushed water mistaken for a separate water point or pooling | Drain hose discharge | Slips; people collecting flush water | 2 | 2 | Drain to the tapstand basin or a soakaway agreed with the committee (WWT-DDR-001 D7) | Low |
| H8 | Working on a pressurised riser | Fitting the saddle tee | Water jet, injury | 2 | 2 | Shut off the supply or use a tapping tool; build plan safety stops | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Free chlorine sensor (BOM 11) | Read free chlorine to PR-001 | Slope drifts between visits | Wrong alerts (missed or false) | Electrode fouling, pseudo-reference drift, flow and conductivity effects (S32, S36) | 5 | 4 | 3 | 60 | Drift test at TRL 4; monthly DPD comparison flags a large error; consider a weekly self-check |
| F2 | Turbidity optics (BOM 10) | Read turbidity to PR-002 | Window fouled | Reading high, false turbidity alerts | Biofilm, silt on windows | 3 | 3 | 2 | 18 | Monthly wipe; 180 degree reference detector shows window loss |
| F3 | Latching valve (BOM 13) | Open and close the flush | Sticks open | Water wasted (up to 720 L/day), cell over-flushed | Debris, scale | 3 | 2 | 2 | 12 | Strainer upstream; daily water count from flush time; alert on unexpected flow |
| F4 | Latching valve (BOM 13) | Open and close the flush | Fails to open | No fresh sample; stale readings | Coil fault, low supply pressure | 4 | 2 | 3 | 24 | Detect by unchanged temperature and chlorine over several readings; fault alert |
| F5 | Pressure-compensating regulator (BOM 14) | Hold 0.5 L/min | Flow low below 0.7 bar | Stale fraction rises to 8.5 % (WWT-CAL-001 D5) | Low supply pressure | 3 | 3 | 3 | 27 | Site pressure survey; longer flush set per site |
| F6 | Check valves and air break (BOM 14, 15) | Protect the supply | One check valve leaks back | The second check valve still holds (F8); air may enter the sample line | Seat wear | 5 | 1 | 4 | 20 | Two check valves in series; air break kept open by design; inspect at the monthly visit |
| F7 | Battery and charger (BOM 5, 6) | Store energy | Charging blocked on hot days | Autonomy drains in heat waves | Enclosure above 45 °C | 3 | 3 | 2 | 18 | Sun shield; low-battery alert; log temperature at TRL 4 |
| F8 | Cellular modem and antenna (BOM 7, 8) | Upload and send SMS | No network | Alerts late or lost | Coverage, SIM, antenna damage | 4 | 3 | 2 | 24 | Three tries; 90 days on board; site survey; LoRaWAN variant |
| F9 | Enclosure and glands (BOM 3, 16) | Keep water out (IP66) | Water ingress at a gland | Corrosion, board failure | Gland not tightened, cable too small for the gland | 4 | 2 | 3 | 24 | Glands matched to cable diameters; check at commissioning; pressure-equalising vent |
| F10 | Flow cell lid and gasket (BOM 9) | Hold water in the cell | Leak at the lid | Air in the cell, false turbidity, wet electronics below | Thumb nuts loose, gasket aged | 3 | 2 | 2 | 12 | Thumb nuts checked at each visit; spare gasket in the caretaker kit |
| F11 | Pole and footing (BOM 1) | Hold the unit | Pole leans | Panel and enclosure misaligned; risk H4 | Footing undersized for soft or wet soil | 4 | 1 | 2 | 8 | Factor 2.2 in saturated sand (WWT-CAL-001 I4); clay and made ground checked at the survey visit; larger footing where needed |
| F12 | Flow cell (BOM 9) | Hold water | Water freezes in the cell | Cracked cell or lid, leak | Clear nights near 0 °C (WWT-STM-001 S33) | 3 | 2 | 3 | 18 | Drain the cell for the cold season at sites that reach 0 °C; insulate; to assess with the partner |
| F13 | Sample line (BOM 14) | Carry the sample | Second check valve sticks shut | No sample; stale readings | Debris past the strainer | 3 | 2 | 3 | 18 | Same detection as F4; strainer upstream; check at the monthly visit |

The highest RPN is the chlorine sensor's drift (F1, 60), the same open question as P1 and WWT-STM-001 S12.
