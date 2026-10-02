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

(Record of the TRL 2 run. Items 1 to 8 and 10 were decided by Amish, 2026-09-25: go with recommendation (WWT-DDR-001, D1 to D10); item 9, the first partner, stays proposed, awaiting Amish (WWT-DDR-001, O1).)

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
3. **New, R1 target.** Options: (a) keep ±0.1 mg/L and accept that R1 is not met; (b) relax to ±0.2 mg/L or ±25 %, whichever is greater, which the design meets with site pH up to pH 7.5 at zero drift (WWT-CAL-001, E6); (c) keep the target and make the pH probe standard, which exceeds the budget. Recommendation: (b), because the DPD field reference alone takes ±0.07 of the ±0.1 mg/L budget. Decided by Amish, 2026-09-25: go with recommendation (WWT-DDR-002, D11).
4. **New, pH probe trigger.** Recommendation: fit the pH probe variant at sites whose pH is above 7.5 or moves more than 0.2 between visits. Decided by Amish, 2026-09-25: go with recommendation (WWT-DDR-002, D12).

Suggestions at the time (now decided by Amish, 2026-09-25: go with recommendation, WWT-DDR-002, D13 and D14): a confirming reading 15 min after a first threshold crossing would cut the worst case from event to SMS from 122 min to 77 min (WWT-CAL-001, H2); casting the footing on a survey visit would bring installation to about 65 min.

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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now decided by Amish, 2026-09-25: go with recommendation. Items without one stay proposed, awaiting Amish. Recorded in `docs/decisions/0002-recommendations-accepted.md` (WWT-DDR-002 v0.1).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D11 | Relax R1 to ±0.2 mg/L or ±25 %, whichever is greater | ±0.1 mg/L below 1.0 mg/L, ±15 % above; 2 of 8 cases met at zero drift; 0.038 mg/L left for drift | 8 of 8 cases met at 25 °C and zero drift (with D12); at least 0.130 mg/L left for drift; R10 drift allowance about 0.13 mg/L per month (was 0.04) |
| D12 | pH probe variant where site pH is above 7.5 or moves more than 0.2 between visits | No port for a probe | Spare 12 mm port with blanking plug in the cell lid; BOM item 9 $12 to $13; parts $282 to $283; variant site $343 to $383, priced outside the base-unit budget (R12 restated) |
| D13 | Confirming reading 15 min after a first threshold crossing (firmware rule) | 122 min worst case from event to SMS | 77 min; 9.7 mWh and 0.75 L per event |
| D14 | Cast the pole footing on the survey visit | 140 min critical path on installation day | 65 min; R11 restated as 2 h on installation day |

Budget: `budget_usd` unchanged at $300; no budget change was recommended. Pitch and problem in `project.yaml` unchanged; `trl: 3` and `trl_target: 3`.

Files changed: `cad/src/model.py` (plugged pH port; STEP and STL re-exported), `cad/src/sheets.py` and WWT-DWG-001 (Rev P1 to P2), `bom/bom.csv` and `bom/bom-notes.md`, `docs/04-calcs/sizing.py` and WWT-CAL-001 (v0.1 to v0.2: new sections E4 to E8, H2, H3, J2, K2 and Table 4), WWT-REQ-001 (v0.3 to v0.4: R1, R5, R11 and R12 restated), WWT-PRC-001 (v0.3 to v0.4), WWT-DDR-001 (v0.1 to v0.2), `cad/src/concept_media.py` and all of `media/` regenerated, `README.md` (new write-up sections before "Problem"), `project.yaml` (DDR-002 added to the evidence list), all PDFs in `docs/pdf/` rebuilt.

### Requirement status (WWT-CAL-001 v0.2)

0 not met, 4 at risk, 6 met on paper, 3 met by design (before: 2 not met, 3 at risk, 5 met on paper, 3 met by design).

| ID | Status | Key number |
| --- | --- | --- |
| R1 Free chlorine | **At risk** (was not met) | 8 of 8 cases at 25 °C before drift; 1.5 mg/L at pH 7.5 and 40 °C with site pH misses by 0.006 mg/L; drift unknown |
| R10 Maintenance | **At risk** (was not met) | Visit 30 min, at the limit; needs drift below about 0.13 mg/L per month, unverified |
| R2 Turbidity | At risk | Window fouling unknown |
| R9 Outdoors | At risk | 50.8 °C inside on a 45 °C day with the shield; shield factor assumed |
| R11 Installation | Met on paper (was at risk) | 65 min on installation day |
| R5, R6, R7, R8, R12 | Met on paper | 13.0 min to SMS (77 min from the event); 0.86 MB/month; 28.6 days; 18.0 L/day; $283 of $300 |
| R3, R4, R13 | Met by design | |

### Still awaiting Amish

- O1, first co-design partner and region (no choice made; partners are picked per area later).
- O2, alert language and recipients; O3, data ownership. No recommendation was made for either.

### Cross-repo actions

None. No decision in this repo needs a change in another repo.

### Other changes in this session

- Every generated file was re-rendered so that the footer shows designmolecule.com: `docs/pdf/`, WWT-DWG-001 and `media/`. The hero, blueprint and exploded images were checked after rendering.
- `README.md` gained "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea". The inspiration point is the Walkerton, Ontario outbreak of May 2000 and Part One of the Walkerton Inquiry (2002). The inquiry report itself could not be opened from this environment (access blocked); its figures are cited as summarized, with the report's archive link.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Nothing was built, bought, tested or programmed. D13 is recorded as a firmware rule only. The drift test that would settle R1 and R10 is TRL 4 work and has not started.

## Session 2026-09-26: sources strengthened

Amish asked to fix the weaker sources in the README (2026-09-26). Every new link below was fetched and checked against the claim it supports. No controlled document changed; `docs/01-problem.md` did not cite the replaced sources.

| Where | Old source | New source |
| --- | --- | --- |
| Country row, India (was "South Asia (Bangladesh, India)") | None | [UNICEF India, clean drinking water](https://www.unicef.org/india/what-we-do/clean-drinking-water): rural tap connections 17 % to over 49 % (2019 to 2022); under 49 % of rural people use safely managed water. Bangladesh and the uncited monsoon and intermittent-chlorination claims were dropped |
| Country row, Honduras (was "Andean and Central American rural schemes") | None | Lindmark et al., ACS ES&T Water 2023 ([PubMed 38094914](https://pubmed.ncbi.nlm.nih.gov/38094914/)): passive tank chlorinators run by community water boards; 77 % of samples at or above 0.2 mg/L; board errors 39 % of lapses; circuit-rider visits correlated with better chlorination |
| Country row, Canada (Walkerton) | Walkerton Inquiry Part One on archives.gov.on.ca (could not be opened from this session) | [CBC News, highlights of the Walkerton Inquiry report](https://www.cbc.ca/news/canada/highlights-of-the-walkerton-inquiry-report-1.867604): residuals not measured daily, seven deaths, 2,300 ill |
| What sparked the idea (Walkerton) | Walkerton Inquiry Part One (archives.gov.on.ca, unopened) plus Wikipedia summary | CBC News (above) and the [National Academies workshop summary, Lessons from Waterborne Disease Outbreaks](https://www.ncbi.nlm.nih.gov/sites/books/NBK28459/). The residual range "0.12 to 0.4 mg/L" and "weekly instead of daily" tests could not be verified in a credible source and were removed; the text now states what CBC and the National Academies report: 0.5 mg/L required after 15 min, too little chlorine used, residuals not measured on most days, false entries, seven deaths, 2,300 ill, and the inquiry's finding that continuous residual and turbidity monitors would have prevented the outbreak |

The inspiration event is unchanged; its line in `INSPIRATIONS.md` was updated to match the verified findings. Kept but not re-opened this session: Nagel et al., ES&T 2015 (publisher returned 403) and the Oxfam WASH chlorination page (fetch refused). No budget change.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (79 parts: 49 shell, 14 internal, 15 accessory, 1 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view without the tapstand and plumbing). It reuses PARAMS and derived() from `cad/src/model.py`; every part size, the X and Y positions and every interface are as model.py. It adds:

- Sun shield: rounded front and top edges, pressed side louvers, a teal accent band, a printed name plate, a grommet for the antenna and a lit green status light.
- Enclosure: filleted IP66 base with cable glands and a vent plug, a clear polycarbonate lid, a gasket line and four tamper-resistant lid screws.
- Inside: the LiFePO4 pack with a label, fuse holder and a hook-and-loop strap; the controller board (ESP32-S3 module and shield can, charger, potentiostat and boost ICs, microSD and RTC, terminal blocks); the cellular modem board with its module can and SIM holder; the whip antenna.
- Solar panel: aluminum frame, backsheet, cell grid with busbars, junction box, tilt rail, hinge and pole-top bracket.
- Flow cell: filleted black body and top plate, four knurled thumb nuts for the tool-free lid, the teal blanking plug in the spare pH port, a label; the turbidity head with flange, screws, label and gland; the chlorine sensor with gland nut and strain relief; the temperature probe with its fitting.
- Plumbing: saddle tee, isolation ball valve with lever, strainer, check valve and regulator, 1/4 in tube, the latching solenoid valve with push-fit ports, the inlet fitting, the outlet elbow with its open air-break vent, and the drain hose and clamp.
- Pole section with band clamps, mounting plates and a top cap; sensor and panel cables.
- Context (not in the BOM): a short section of the tapstand riser with its tap.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files.

### Differences from model.py (Proposed, awaiting Amish)

1. **Render layout of heights.** Installed, the parts spread over 2.2 m of pole, which makes each part small in a product render. The appearance model keeps the enclosure at its model.py height and draws the panel and pole top 520 mm lower, the flow cell 130 mm higher and the saddle tee and valve 350 mm higher (tee at 850 mm instead of 500 mm). The pole, riser and drain hose are shown as short sections, and the sample tube is rerouted to suit. All sizes and X and Y positions are unchanged. Proposed, awaiting Amish. Recommendation: keep this as a render-only layout (the hero note says heights are drawn closer together than installed); the installed heights stay as in model.py and WWT-DWG-001.
2. **Status light.** model.py and the BOM have no status light. The appearance model shows a lit green lens in the shield front, which would be fed by a light pipe from an LED on the controller board (BOM line 6). Proposed, awaiting Amish. Recommendation: adopt a single low-duty status LED behind a lens in the shield, with an open-bottom slot so the shield still lifts off; its power draw is negligible against the 0.54 Wh per day budget but should be added to WWT-CAL-001 if adopted. Option: omit the light and show nothing lit.
3. **Clear enclosure lid.** BOM lines 3 and 4 specify an IP66 polycarbonate enclosure without saying whether the lid is clear. The appearance model uses a clear lid so the exploded view shows the board, battery and modem; under the sun shield a clear lid gains no sun load. Proposed, awaiting Amish. Recommendation: accept a clear-lid enclosure (common and similar in price) and add "clear lid" to BOM line 3 at the next BOM revision; the BOM was not edited now.
4. **Panel cable gland on the enclosure top.** model.py brings the panel cable to the enclosure top but shows glands only underneath. The appearance model adds a fourth, small gland on the top, under the shield. Proposed, awaiting Amish. Recommendation: accept; it is within BOM line 16 (glands). Option: route the panel cable down the pole to a fourth gland underneath, which keeps all entries on the bottom face.
5. **Appearance detail only.** The louvers, labels, thumb nuts, strap and fixings are appearance detail within the existing BOM lines; no new BOM lines are implied. The flow cell stays opaque black, as the turbidity measurement requires.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: kit 1.7.0, constructable design and prototype build plan

Amish approved the build plan format on 2026-09-30 and asked for it in every repo, with outstanding decisions kept in a separate register, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." On 2026-10-01 he set budgets as value-engineering targets. This session applied both to WaterWatch. Nothing was built, bought or tested; `trl` stays 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Constructability review with build123d: `cad/src/model.py` rewritten to separate components and now runs 97 checks (`python cad/src/model.py --check`: 68 required contacts, 17 clearances, an overlap scan of all 53 parts, the light path in the cell and the standing water level). All pass. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (WWT-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (WWT-BLD-001 v0.1) from the kit template, with `cad/src/build_plan_media.py`: overview, 9 making sketches (`cad/drawings/WWT-DWG-101` to `109`), 3 drilling layouts, a wiring diagram, 12 joint close-ups and 18 assembly step pictures in `docs/05-build-plan/`.
- `docs/06-design-decisions.md` (WWT-DEC-001 v0.1): 10 open decisions, 8 items to confirm when parts are bought, a value engineering section and the decisions made.
- WWT-DWG-001 Rev P3 to P4; WWT-CAL-001 v0.2 to v0.3; WWT-REQ-001 v0.4 to v0.5; WWT-PRC-001 v0.4 to v0.5; `bom/bom.csv` (20 lines) and `bom/bom-notes.md`; `README.md` (links line, "Building the prototype", value-engineering wording); `project.yaml` (`design_state: constructable`, three evidence files added; `budget_usd` unchanged at 300). Three BOM rows that had unquoted commas in their notes were re-quoted.
- Concept media regenerated from the new model (`media/hero.png`, `cutaway.png`, `exploded.png`, `flow.png`, `concept-blueprint.*`, `model.glb`). PDFs rebuilt.

### Design changes made for construction (WWT-DDR-003)

1. P1. The solid concept plates and loose clamp rings became two 3 mm aluminium back plates, each on two M8 U-bolts with V-saddles; the pole axis moves from 94 to 103 mm behind the enclosure centre.
2. P2. The enclosure hangs on the maker's four lugs, one M5 screw each.
3. P3. A printed internal plate on the box's moulded bosses carries the battery, controller and modem.
4. P4. Every entry is in the bottom face: six glands (one a plugged spare for the pH probe), the vent and the antenna, which now points down; the panel lead runs down the back of the pole.
5. P5. The sun shield has flanges and four thumb screws and slides off forward.
6. P6. The turbidity optics are three holders on three walls (LED, 90° and 180° detectors); the baffle, unchanged in size, moved to the back wall so the beam is clear.
7. P7. The lid glands were laid out so none overlaps and every probe clears the beam and the baffle.
8. P8. The cell lid has a gasket, four studs and thumb nuts.
9. P9. The cell's back wall is 14 mm (body 60 deep instead of 54) and takes two M5 screws from behind the plate; the cavity and its volume are unchanged.
10. P10. The valve is screwed to the cell plate under the cell; the tube run falls from 738 to 696 mm.
11. P11. The panel sits on a bought pole-top tilt mount.
12. P12. The riser fittings are one screwed brass line with the check valve shown.
13. P13. Every cable has a defined route, clear of every part it is not fixed to.

### Key results

- Estimated cost of the constructable design: USD 319 against the USD 300 value-engineering target (USD 19 over); the construction parts added USD 36. A pH probe variant site: USD 379 to 419.
- Requirement status (WWT-CAL-001 v0.3): none not met; 4 at risk (R1, R2, R9, R10); 5 met on paper; 3 met by design; R12 over the value-engineering target by USD 19. No other status changed. The tube change moves two chlorine error figures by 0.001 mg/L.

### Open decisions (in WWT-DEC-001)

Review of WWT-DDR-003; shield thumb screws at public sites; antenna position; water volume basis in the calculation; and, carried over, the render layout, status light and clear lid (2026-09-26) and O1 to O3. All proposed, awaiting Amish.

### Picture notes

- The concept exploded view (`media/exploded.png`) is still dense around the small flow cell parts (callouts 9 to 12), although they were pulled further apart; the build plan overview shows them clearly.
- Some joint close-ups have leader lines that end close together where a part is mostly hidden behind another (joints 2, 4 and 5); the captions in the plan say which face meets which.

### Stale until regenerated on Amish's Mac

The design changed visibly, so `media/render-*.png`, `media/card.png` and `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: the antenna through the shield top, the single turbidity block, the solid mounting plates and clamp rings, and the panel bracket. They were not regenerated here.

### Safety

No change to the safety case. The plan adds safety stops for the battery, the connection to the drinking water supply (supply shut off, check valve direction, air break), the concrete footing and work at height. The shield now comes off by hand (open decision 2).

### Recommended next step

Amish reviews WWT-DDR-003 and the open decisions in WWT-DEC-001, and has the photoreal renders regenerated on the Mac. TRL 4 (building to the plan and testing) remains on hold.
