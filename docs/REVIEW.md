# Review note: WaterWatch

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

Amish was not available during this run, so every choice below is recorded as proposed, awaiting Amish.

### What was done

- `docs/01-problem.md` (WWT-PRB-001 v0.2): the problem with cited figures (2.1 billion people without safely managed drinking water; chlorine and turbidity guidance), users and context, constraints, out of scope, prior work, co-design checklist, open questions.
- `docs/03-requirements.md` (WWT-REQ-001 v0.2): 13 measurable requirements (R1 to R13) with targets, planned verification and concept status.
- `docs/02-concept.md` (WWT-PRC-001 v0.2): how it works, components table numbered to the BOM and exploded view, first-order numbers with assumptions, design choices with options, safety, open questions.
- `cad/src/concept_media.py`: massing model of the pole, 5 W panel, enclosure and lid, battery, controller, modem, antenna, flow-through cell, turbidity head, chlorine sensor, temperature probe, latching valve, sample line, drain hose and cables, beside an existing tapstand (grey, not in the BOM). The scene is shifted so the enclosure sits near the origin, because the kit's cutaway cutter is centered on the origin.
- `media/`: hero with a 1.75 m person, blueprint sheet (PNG, PDF, SVG), cutaway, exploded view with BOM callouts, sample and data flow diagram (estimates marked), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 16 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image, links line, concept paragraph, key components and safety updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still match the concept.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Daily energy | about 0.5 Wh (0.32 Wh plus 50 % margin) | |
| Autonomy without sun | about 30 days on 3.2 V, 6 Ah LiFePO4 | R7 met (7 days) |
| Solar refill, 5 W panel | about 13 Wh per clear day; about 1.2 days from empty | R7 met |
| Water to drain | about 0.75 L per reading, about 18 L/day | R8 met (20 L), thin margin |
| Data | under 1 MB per month | R6 met |
| Parts cost | about $270 | R12 met, about $30 margin |
| Shared calibration kit and airtime | about $60 once; about $1 to $3 per month | Outside the unit budget |

Requirements not met on present evidence:

- **R1, free chlorine accuracy.** No low-cost membrane-free sensor has shown months of unattended accuracy at the ±0.1 mg/L level, and the reading depends on pH, which the base design does not measure.
- **R10, monthly maintenance.** The chlorine sensor's drift and recalibration interval are unknown.

At risk: R2 (turbidity accuracy under fouling and bubbles in continuous use) and R9 (enclosure and battery temperature in full sun).

### Proposed, awaiting Amish

1. **Chlorine sensor.** (a) Membrane-free graphite three-electrode sensor with a potentiostat front end, about $25; (b) industrial membrane amperometric probe, about $1,900, over budget; (c) ORP probe as a proxy, about $175 as a kit, loose correlation. Recommendation: (a), with a monthly DPD comparison.
2. **pH.** (a) Site pH entered at installation and checked monthly; (b) add a pH probe (about $60 to $100, estimate), raising parts to about $330 to $370, over the $300 budget. Recommendation: (a) now, (b) as a documented variant. If Amish prefers (b), the budget in `project.yaml` would need to rise to about $375; that change is proposed only, and `project.yaml` is unchanged at $300.
3. **Connectivity.** Cellular LTE-M and NB-IoT with 2G fallback and SMS alerts (recommended), with a LoRaWAN module as a swappable variant.
4. **Mounting.** Separate pole beside the tapstand (recommended) rather than on the tapstand itself.
5. **Sampling.** Hourly 90 s timed flush with a latching valve (recommended) rather than continuous flow (about 720 L/day).
6. **Default alert thresholds.** Free chlorine below 0.2 mg/L and turbidity above 5 NTU, two consecutive readings, adjustable per site.
7. **Drain destination.** Tapstand basin by default; soakaway or a container for non-drinking use per site.
8. **First site type.** Tapstands first; tank outlets and kiosks later.
9. **First partner.** A rural utility or maintenance service provider already using handpump sensors, a WASH NGO running chlorinated piped schemes, or a university WASH research group. Recommendation: a maintenance service provider, because alerts only help if someone is paid to act on them.
10. **SwapCell.** Not proposed; WaterWatch needs under 1 Wh per day, and a 48 V pack does not fit.

### Safety concerns

- The biggest risk is false reassurance: a normal reading must never be presented as "safe water". Alert wording is a requirement (R13).
- Backflow into a drinking water supply: an isolation valve, a check valve and food-safe wetted parts are in the concept; they need review against local plumbing rules.
- LiFePO4 battery in a sun-heated box: protection board, fuse and charging temperature cut-offs are in the concept; the enclosure temperature is not yet estimated.
- Calibration chemicals (DPD reagents, turbidity standards): prepared, stabilized standards only; no formazin preparation in the field.

### Gaps and notes

- Some sources could not be opened in full during this run (access limits on publisher sites). The long-term low-cost chlorine sensor study (Water Science and Technology, 2025) and the Rwanda handpump study are cited from their titles and abstracts, not the full text; check them at TRL 3.
- Several prices, including items 6, 9, 10 and 11, are rough estimates without a named supplier listing.
- The exploded view is dense around the flow-through cell; small callouts (10 to 12) partly cover their parts.

### Recommended next step

Review this note and the media. If Amish approves, run `/advance-trl3` to review the low-cost chlorine sensor literature for drift and pH effects, size the energy and thermal budgets by calculation, estimate the enclosure temperature, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish reviewed the TRL 2 review points on 2026-09-25 and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session ran `/advance-trl3` on that instruction and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (WWT-DDR-001 v0.1): ten items decided by Amish on 2026-09-25, going with the recommendations (D1 to D10), and three items left open (O1 to O3).
- `docs/04-calcs/01-sizing.md` (WWT-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: energy, solar, enclosure temperature, flushing and water use, a free chlorine error budget, turbidity bubbles and settling, data, alert latency, wind on the pole and footing, installation and maintenance task times, and cost, with a status for every requirement. The script imports the model's parameters and reads the BOM and `project.yaml`; every number in the note is printed by it.
- `cad/src/model.py`: parametric build123d model (pole and footing, panel, enclosure and contents, sun shield, flow cell with ports and baffle, sensors, valve, sample line from the riser tee, drain with air break). Exports `cad/step/` and `cad/stl/` for `waterwatch-assembly`, `flow-cell` and `enclosure`.
- `cad/src/sheets.py` and `cad/drawings/WWT-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:25, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". WWT-DWG-001 was free because the concept blueprint is WWT-DWG-010.
- `bom/bom.csv` (17 lines, all priced with a supplier type, $282.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. The cutaway now cuts on the cell's center plane (a project-side wrapper; the kit is unchanged) so the cavity and both sensors show.
- WWT-PRB-001, WWT-PRC-001 and WWT-REQ-001 revised to v0.3; `README.md` and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes found necessary by the calculations, all within the decided choices: the flow cell is halved to 0.19 L of water (the TRL 2 cell kept 17 % old water at the chlorine reading); a pressure-compensating 0.5 L/min regulator replaces the fixed restrictor (a restrictor would pass 36 L/day at 4 bar); the outlet sits near the top with an open air break so the cell stays full and cannot siphon; the valve is specified direct acting for 0.5 bar sites; the bubble wait before the turbidity reading rises from 10 s to 30 s; SMS retries are at 3 min spacing; and a ventilated sun shield (item 17, $8) is added.

### Requirement status (WWT-CAL-001, Table 4)

2 not met, 3 at risk, 5 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R1 Free chlorine | **Not met** | ±0.131 mg/L at 0.5 mg/L and pH 7.5 with site pH, before sensor drift (target ±0.1); met only at pH 7.0 |
| R10 Maintenance | **Not met** on present evidence | Visit 30 min, at the limit; monthly interval needs drift below about 0.04 mg/L per month, unknown |
| R2 Turbidity | At risk | Bubbles handled by the 30 s wait; window fouling unknown |
| R9 Outdoors | At risk | 50.8 °C inside on a 45 °C day with the shield, 69.8 °C without; shield factor assumed |
| R11 Installation | At risk | 140 min critical path with the footing cast on the day (target 120 min); 65 min if cast earlier |
| R5, R6, R7, R8, R12 | Met on paper | 13.0 min to SMS; 0.86 MB/month; 28.6 days autonomy, 1.18 days to refill; 18.0 L/day (19.8 L at tolerance); $282 of $300 |
| R3, R4, R13 | Met by design | DS18B20 ±0.5 °C; 15 min schedule within energy; wording rule |

Key numbers: 0.537 Wh/day; 13.5 Wh per clear day from the 5 W panel; pole 52 MPa (factor 4.5) and footing factor 4.9 in a 35 m/s gust.

### Decisions recorded (WWT-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 membrane-free graphite chlorine sensor with monthly DPD comparison; D2 site pH, pH probe as a variant, budget unchanged at $300; D3 cellular with LoRaWAN as a swappable variant; D4 separate pole; D5 hourly 90 s timed flush; D6 defaults of 0.2 mg/L and 5 NTU, two consecutive readings; D7 drain to the basin by default, per site; D8 tapstands first; D9 LiFePO4 with 0 to 45 °C charging; D10 no SwapCell. No budget, pitch or problem rewording was recommended, so none was applied. The SwapCell interface v0.3 items do not apply to this design.

### Still awaiting Amish

1. **O1, first co-design partner and region.** Left open by Amish's direction that community designs pick partners per area later.
2. **O2, alert language and recipients; O3, data ownership.** No recommendation was made; for co-design.
3. **New, R1 target.** Options: (a) keep ±0.1 mg/L and accept that R1 is not met; (b) relax to ±0.2 mg/L or ±25 %, whichever is greater, which the design meets with site pH up to pH 7.5 at zero drift (WWT-CAL-001, E6); (c) keep the target and make the pH probe standard, which exceeds the budget. Recommendation: (b), because the DPD field reference alone takes ±0.07 of the ±0.1 mg/L budget. Not applied.
4. **New, pH probe trigger.** Recommendation: fit the pH probe variant at sites whose pH is above 7.5 or moves more than 0.2 between visits. Not applied.

Suggestions only, not in the repo: a confirming reading 15 min after a first threshold crossing would cut the worst case from event to SMS from 122 min to 77 min (WWT-CAL-001, H2); casting the footing on a survey visit would bring installation to about 65 min.

### Safety concerns

- False reassurance remains the biggest risk: R1 is not met, so a low chlorine reading could be missed at high-pH sites. Alerts must stay worded as measurements (R13), and the monthly DPD test stays part of the routine.
- Battery heat: without the sun shield the enclosure reaches about 70 °C on a 45 °C day, above typical LiFePO4 discharge limits. The shield is essential, and its benefit is assumed, not measured.
- Backflow and cross-connection: the check valve, isolation valve and the new open air break at the outlet need review against local plumbing rules; fitting the saddle tee needs the supply shut off or a tool for tapping under pressure.
- Calibration chemicals: prepared, stabilized standards only; no formazin preparation in the field.

### Gaps and notes

- Citations: a web search on 2026-09-25 confirmed the titles and venues of "Long-term performance of low-cost free chlorine sensors to monitor on-site water reuse" (Water Science and Technology, 2025, doi 10.2166/wst.2025.090) and the Rwanda handpump study (Nagel et al., Environmental Science and Technology 49(24), 2015, doi 10.1021/acs.est.5b04077). Neither the full text nor the abstract could be opened (publisher 403, a CAPTCHA on PubMed, and the proxy blocked Europe PMC), so their findings, and in particular any drift data for R1 and R10, remain unchecked.
- Assumptions that only tests can settle: the sun shield factor, sensor drift, pH movement between visits, and window fouling.
- The exploded view is still dense around the flow cell: callouts 9 to 12 partly cover their small parts.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on the R1 target and the pH probe trigger above. For the record only, TRL 4 would need: a bench build of the flow cell, chlorine sensor and turbidity head; a lab test report (TST, `environment: lab`) of chlorine accuracy and drift against DPD over pH 6.5 to 8.5, turbidity against stabilized standards with bubbles and fouling, and enclosure temperature with and without the shield in sun; and build log entries. None of this has been started.
