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
