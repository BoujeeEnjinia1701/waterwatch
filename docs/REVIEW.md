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

`media/render-*.png`, `media/card.png` and `media/social-preview.png` are to be made again on Amish's Mac from the render scenes exported on 2026-10-02 (see "Approved follow-ups carried out" below). The appearance model `cad/src/product_model.py` was brought in line with `model.py` on 2026-10-02 (optics holders, antenna and entries in the bottom face, back plate size, status light).

### Safety

No change to the safety case. The plan adds safety stops for the battery, the connection to the drinking water supply (supply shut off, check valve direction, air break), the concrete footing and work at height. The shield now comes off by hand (open decision 2).

### Recommended next step

Amish reviews WWT-DDR-003 and the open decisions in WWT-DEC-001, and has the photoreal renders regenerated on the Mac. TRL 4 (building to the plan and testing) remains on hold.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." This approves the recommendation written for each open decision in the design decisions register (WWT-DEC-001), as he did for the other 555 open decisions ("i approve your recommendations for all 555 open decisions."). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Ten decisions, all moved to Decisions made in WWT-DEC-001, dated 2026-10-02:

1. Design for construction accepted: the changes P1 to P13 of WWT-DDR-003, as made.
2. Shield fixing: knurled thumb screws for the prototype; tamper-resistant M5 screws on field units after the first site visit.
3. Antenna: the whip points down from the bottom face, and signal strength is measured at TRL 4; a pole-top antenna is used only at a weak-signal site.
4. Water volume in the calculation: the full-cavity 0.185 L is kept, conservative for flushing; the standing volume is measured at TRL 4.
5. Product render layout: the render-only layout with heights drawn closer together is kept, with the note on the hero render.
6. Status light: one low-duty LED behind a lens in the shield front, with an open-bottom slot so the shield still slides off.
7. Enclosure lid: a clear-lid enclosure is accepted, and BOM line 3 says so.
8. First co-design partner and region: a scheme operator that runs chlorinated, solar-powered piped schemes with public tapstands; the first candidate to approach is Water Mission, which runs such schemes in East Africa, with the first region taken from its country programs.
9. Alert language and recipients: alerts go by SMS in the site's main local language, with an English copy to the operator, stating only what was measured, when and the threshold crossed; they go to the caretaker and the operator's maintenance contact, with a weekly summary to the district water officer.
10. Data ownership: the scheme operator owns the data; the water committee and the district water and health offices can see it; anonymized site data are published only with the operator's written agreement.

### Documents changed

- `docs/06-design-decisions.md` (WWT-DEC-001 v0.2): open decisions moved to Decisions made.
- `docs/decisions/0003-design-for-construction.md` (WWT-DDR-003 v0.2): acceptance recorded in the status line; A1 to A3 decided (record stays Draft).
- `docs/decisions/0001-trl2-review-decisions.md` (WWT-DDR-001 v0.3) and `docs/decisions/0002-recommendations-accepted.md` (WWT-DDR-002 v0.2): O1 to O3 recorded as decided.
- `docs/01-problem.md` (WWT-PRB-001 v0.4): partner, alert and data questions answered.
- `docs/02-concept.md` (WWT-PRC-001 v0.6): open questions answered.
- `bom/bom.csv` (line 3 specification text only: clear lid; no quantity or price change).
- `README.md`: the build plan paragraph says WWT-DDR-003 is accepted and the decisions are all made.

### Follow-up actions to carry approved decisions into the design

1. Decision 6 (model): Model the status LED and its lens in the shield front, with the open-bottom slot so the shield still slides off, and check its clearance to the enclosure.
2. Decision 6 (BOM): Add the status LED, lens and lead to the BOM with a price basis.
3. Decision 6 (calculations): Add the LED's low-duty energy to the energy budget in WWT-CAL-001.
4. Decision 6 (pictures): Show the status LED and its wiring in the general arrangement, the build plan's shield and wiring pictures and the concept media.
5. Decision 2 (docs): Name tamper-resistant M5 shield screws as the field-unit fixing in the build plan's shield step and BOM line 20 note when field units are planned.
6. Decision 9 (docs): Write the alert message templates (SMS, local language with an English copy) and the recipient list into the firmware settings notes.
7. Decisions 8, 9 and 10 (docs): Approach Water Mission, choose the first region from its East African country programs, and confirm the alert and data defaults with the operator and caretakers.

### Points found in the review

- None.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out. `trl: 3` is unchanged; no build or test work was done.

### Follow-ups

1. Done. Decision 6, model: the status light is in `cad/src/model.py` (parts `status_lens`, `status_holder`, `status_led`, `status_cable`): a 16 mm lens and printed holder whose 12 mm barrel sits in a 12.2 mm slot, open at the bottom, in the shield front panel (round end 10 mm above the lower edge); the lead hangs to a seventh gland in the bottom face (middle row, centre line). The unit drops out of the slot downward, so the shield still slides off forward. Interpretation recorded: the decision text does not say where the lead goes or how the unit is held, so this is the reading chosen. New checks: 7 touches and 2 clearances (holder 10 mm or more from the clear lid; lead 20 mm or more from the antenna); 106 of 106 checks pass; STEP and STL regenerated.
2. Done. Decision 6, BOM: line 21 (USD 2.00; LED about 0.40, lens disc 0.40, printed holder 0.30, lead with crimps and resistor 0.90) and a seventh gland on line 16 (USD 19.00, +1.00).
3. Done. Decision 6, calculations: WWT-CAL-001 v0.4 and `sizing.py`: 5 mA for 50 ms every 10 s adds 1.98 mWh a day; daily need 0.540 Wh (was 0.537), autonomy 28.5 days (was 28.6).
4. Done. Decision 6, pictures: WWT-DWG-001 Rev P5 (status light leader and note); shield sketch WWT-DWG-104 and enclosure sketch WWT-DWG-102; bottom-face drilling layout; joint 3; steps 1, 17 and 18; new step 19; overview; wiring diagram; concept media (new line 21 in the exploded view).
5. Done. Decision 2, docs: tamper-resistant M5 screws named for field units in the build plan (shield section and steps 18) and in the BOM line 20 note (about USD 2 a unit, not in the total).
6. Done. Decision 9, docs: alert message templates (five, English copy; the local language text is translated with the caretakers) and the recipient list are in WWT-DDR-001 v0.4, section "Firmware settings notes". The repo has no firmware sketch (TRL cap), so the notes live in that record.
7. Not done: decisions 8, 9 and 10, approach Water Mission, choose the first region and confirm the defaults with the operator and caretakers; this is outreach by Amish.

### Other changes

- Value-engineering target: USD 300. Estimated cost of the constructable design: USD 322 (USD 22 over the target), 21 lines (was USD 319, 20 lines). `budget_usd` unchanged. The pH probe variant site is now about USD 382 to 422.
- Requirement status changes: none. R7 is still met on paper (28.5 days); R12 is still over the target, by USD 22.
- Appearance model (`cad/src/product_model.py`) was stale against the constructable model and did not run (it read a turbidity parameter that no longer exists). Now it takes the three optics holders from `model.py`, puts the antenna and all entries in the bottom face at the model's positions, sizes the enclosure back plate from `model.py`, and shows the status light in the slot with its lead (the green light moves from the upper right of the shield front to the bottom centre). Still render-only, kept by Amish's decision of 2026-10-02: heights drawn closer together, the cell back bar, the pole clamps in place of U-bolts and saddles, and the louvers on the shield. Render scenes exported to `/home/claude/renders/waterwatch` (hero, exploded, detail, with `waterwatch__jobs.json`); photoreal renders, `media/card.png` and `media/social-preview.png` are for Amish's Mac.

### Cross-repo actions

- None needed in other repos for the status light. Water Mission outreach and the first region are Amish's.

### Documents changed

WWT-CAL-001 v0.4, WWT-REQ-001 v0.6, WWT-PRC-001 v0.7, WWT-DDR-001 v0.4, WWT-DDR-003 v0.3, WWT-DEC-001 v0.3, WWT-BLD-001 v0.2, README, `bom/bom.csv`, `bom/bom-notes.md`, WWT-DWG-001 Rev P5.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

## Session 2026-10-24: kit 1.9.1 upgrade

Run on 2026-10-25 under Amish's instructions of 2026-10-24 ("I want detailed TRL3 CAD - and in fact want to ensure the CAD is detailed across all TRLs", "Detail every option", "Kit 1.9.1 rollout - proceed to rollout across the other repos") and his standing instruction of 2026-10-23 (the fix rule). `trl: 3` is unchanged; the repo is now at `stage: P3`. No build or test work was done, and nothing is decided that Amish has not decided.

### What was added (kit 1.8 pipeline)

- STEM check: `docs/01b-stem-check.md` (WWT-STM-001), `docs/04-calcs/stem_check.py` (imports `sizing.py`), `docs/04-calcs/stem_results.csv` and `docs/04-calcs/stm_table.py`, which writes the claims table from the CSV.
- Concept options: `docs/02a-concept-options.md` (WWT-OPT-001) and the concept selection record `docs/decisions/0004-concept-selection.md` (WWT-DDR-004, proposed, awaiting Amish).
- Requirements: users-and-needs and stakeholder tables in WWT-PRB-001 v0.5; `docs/03a-user-requirements.md` (WWT-URS-001, 16 URs); `docs/03-requirements.md` is now WWT-PRS-001 v0.7 (replaces WWT-REQ-001): R1 to R13 carried to PR-001 to PR-013 with the old numbers in "Was", PR-014 to PR-016 added for user needs that had none; `docs/03b-traceability.md` (WWT-RTM-001) generated by `python .kit/trace.py`.
- `docs/07-regulatory.md` (WWT-REG-001), `docs/08-feasibility.md` (WWT-FEA-001), `docs/09-risk.md` (WWT-RSK-001, with a preliminary hazard analysis and a first-pass design FMEA of 13 failure modes), `docs/10-market.md` (WWT-MKT-001), `docs/11-plan.md` (WWT-PLN-001, with the reference list).
- Updated: WWT-PRC-001 v0.8, WWT-CAL-001 v0.6 (and `sizing.py`), WWT-BLD-001 v0.3, WWT-DEC-001 v0.4, `bom/bom.csv` (lines 5, 13, 14, 20), README (links line, STEM check and Concept options sections), `project.yaml` (`stage: P3`, `stem_check: open`, `concept_options: [A, B, C]`, `concept_chosen: A (proposed)`, `trl_evidence`).

### What was added (kit 1.9 CAD)

- `cad/src/model.py` now has the kit 1.9 interface: `PARAMS` (unchanged), `OPTIONS`, `PRINCIPLES`, `CHOSEN = "A"`, `OPTION_VIEWS` (with `ground_z: 0`, since the poles go 0.6 m below ground), `ALLOWED_CONTACTS` (empty: no overlaps needed allowing) and `components(option)`. Option A is the existing design: the geometry of `build_components()` (which the sizing script, the build plan pictures and the making sketches still read) split into its parts, with every bolt, nut, washer, screw, stud and standoff drawn from `.kit/cad_parts.py` or the new repo helper `cad/src/wwt_parts.py` (M3 and M4 hardware, glands, thumb screws, knurled nuts, standoffs, fittings, boards, the framed panel). Options B and C are new detailed models built from shared builders in `model.py` (pole clamp, cabinet with lugs, glands, hood and internal plate, battery tray and carrier boards, panel on its tilt mount, sample train). No design dimension of option A changed; detail changes found while modelling are F2 to F4 below.
- `python .kit/cad_check.py --export` passes at D3 (`cad/fidelity.json`): option A 215 parts (95 made or bought, 120 fasteners), 19.2 kg; option B 173 parts (108 fasteners), 18.8 kg; option C 139 parts (88 fasteners), 6.4 kg; no bare primitives, no interference over 5 mm³ in any option. Per-part STEP for option A in `cad/step/A/`; assembly STEP per option in `cad/step/`. There are no welds in any option (bolted and screwed throughout).
- Regenerated from the model: `cad/step/waterwatch-assembly.step`, `flow-cell.step`, `enclosure.step` and the STL (0.2 mm chord, now from `components("A")`); WWT-DWG-001 Rev P6 (from the D3 model); making sketches WWT-DWG-101 to 109 (103 at Rev P2, the battery tray holes); build plan pictures; concept media (`cad/src/concept_media.py` now draws `components("A")` grouped by BOM line, fasteners travelling with the part they hold); `media/model.glb` re-exported alone with the web tessellation (10.9 MB). The concept blueprint WWT-DWG-010 is drawn by `python cad/src/concept_media.py blueprint` from the grouped TRL 3 geometry of `build_parts()` (the same design without fasteners): the hidden-line projection of all 215 D3 parts ran out of memory in `render_all` on this 2-CPU machine (exit 137), and STANDARDS section 24 keeps the blueprint as it is.
- `cad/src/product_model.py` rebuilt from `components(CHOSEN)` plus site context parts (tapstand apron and basin, riser and tap, the pole's footing, all reaching below ground; a 1.75 m mannequin standing on the ground). `RENDER_VIEWS`: `hero` (outdoor, soil, ground at z = 0, sun 48 deg elevation at azimuth -75 against a camera at -40, 45 mm lens) and `studio` (with `--ground-z=0`).
- `cad/src/options_preview.py` draws a shaded stand-in `media/options.png` from the three D3 models; the Cycles render (`python .kit/options.py`) replaces it on Amish's Mac. Product renders, options render and cards were not run here (coordinator renders).

### STEM verdicts and fixes

Option A: 37 claims, 27 within known science, 9 plausible (S4 hot-day recharge, S5 shield factor, S12 chlorine drift, S14 pseudo-reference, S22 fouling, S32 flow dependence, S33 freezing, S34 sun-heated temperature reading, S36 low conductivity), 1 fails with a fix proposed (S31). Options B and C: 6 claims each, 4 within and 2 plausible each. `stem_check: open`. Fixes made under the standing instruction of 2026-10-23, recorded in WWT-DEC-001 and reversible by Amish:

- F1 (S3): the battery was "1S2P 32700 cells, 6 Ah", but one 32700 cell holds 6 Ah; now one cell. Energy figures unchanged; thermal mass 1,305 J/K (was 1,460).
- F5 (S6, S29): 110 s flush at sites below 0.7 bar (4.5 % stale water instead of 8.5 %).
- F6 (S15): valve rated to open against at least 4 bar.
- F7 (S20): TLS session resumption (0.36 MB a month; a full handshake each time would be 1.22 MB).
- F8 (S8, S30): a second check valve at the cell inlet; BOM line 14 +USD 3.

Detail changes found while modelling to D3, under the instruction of 2026-09-30 (WWT-DDR-003): F2 lug screws M5 x 16 with washers (was M5 x 12), F3 battery tray screwed to the internal plate (was a strap), F4 pole-top mount rail modelled the panel's height so its bolts reach the frame.

### Independent review

A separate Claude session (`claude -p`, read-only tools, run from its own folder) saw only the STEM check, WWT-CAL-001, WWT-PRS-001 and `sizing.py` with its output, and tried to refute the headline results and every "Within known science" verdict. It upheld 7 rows, weakened 17, refuted none outright and listed 7 missing claims. Changes made from it: F5 to F8 above; corrected chlorine budget (stale bias added linearly, one-point calibration span) giving S31 and E9 to E11; converter loss (A6); hot-day recharge (S4 now plausible); wind on the sun shield (pole 59 MPa, factor 4.0; footing 4.3 dry, 2.2 saturated); event-to-SMS 92 min with all three tries (H4); ISO 7027 range in FNU; wording of S23, S24, S25, S27; new rows S29, S30, S32 to S37; lightning, static and condensation added to the risk register (P8), freezing and a stuck second check valve to the FMEA (F12, F13). The row-by-row record is in WWT-STM-001, "Independent review".

### Option scores

A, timed-flush flow cell on its own pole: 196 of 245. B, reagent colorimetric analyser cabinet: 167 (85 % of A). C, in-riser probe manifold: 155 (79 %). Not within 10 %, so a recommendation is made: A, with B's best idea (a shared DPD photometer as the monthly reference) grafted on; proposed, awaiting Amish.

### Requirements not met

- **PR-001 free chlorine: not met at 1.5 mg/L.** The corrected budget meets 6 of 8 cases at 25 °C before drift; at 1.5 mg/L it misses by 0.004 mg/L (pH 7.5) and 0.017 mg/L (pH 8.5), and by more when the sensor is calibrated at 0.5 mg/L (1 of 4 met; 2 of 4 with a photometer). Met at 0.2 to 0.5 mg/L, where the alerts are set.
- **PR-012 parts cost: over target.** USD 325 against the USD 300 value-engineering target (USD 25 over), after the second check valve. `budget_usd` unchanged.
- At risk: PR-002 turbidity (fouling), PR-009 outdoor survival (shield factor), PR-010 caretaker maintenance (drift). PR-008 water use is met on paper with a 1 % margin (19.8 L against 20 L).
- Traceability: `python .kit/trace.py` reports no gaps (16 URs, 16 PRs).

### Decisions awaiting Amish (WWT-DEC-001)

- O1: concept carried forward; A recommended (WWT-DDR-004 D1).
- O2: shared DPD photometer per operator as the monthly reference (option B's graft); recommended (D2).
- O3: product render layout. On 2026-10-02 Amish kept a render-only layout with heights drawn closer together; the kit 1.9.1 product model is built from `components("A")` and shows the installed heights. Installed heights recommended; until he decides, `product_model.py` follows the kit 1.9.1 brief.
- O4: whether PR-008 counts confirming-reading flushes; counting the hourly schedule only is recommended.
- O5: PR-001 above 1.0 mg/L; restating it as ±30 % is recommended (meets 8 of 8 cases).
- Earlier open items unchanged: approach Water Mission and choose the first region (outreach by Amish).

### Safety

The sample line now has two check valves in series and the normally closed valve between the cell and the supply; a verifiable backflow device or an inlet air gap is still to assess under the local code at the first site (WWT-REG-001 R4). The battery is one 19.2 Wh LiFePO4 cell, to be bought with a UN 38.3 test summary. Freezing of the water-filled cell near 0 °C is new and unassessed (S33). The monitoring-aid rule stands: no message may say the water is safe.

### Kit and environment notes

- No agent-spawning tool was available in this session, so the independent reviewer was run as a separate `claude -p` process with read-only tools; it saw only copies of the four files.
- The session scratchpad is shared with other fleet agents (another repo's reviewer prompt sat in `scratchpad/review/`); the WaterWatch review was moved to its own folder before it ran.
- `.kit/cad_parts.py` has no M3 or M4 sizes in its ISO table (`hex_bolt_set(4, ...)` raises a KeyError), so small screws, nuts, washers and standoffs are in `cad/src/wwt_parts.py`.
- `.kit/concept.py` `with_scale_figure` stands the figure on the lowest point of all parts, which is 0.6 m below ground for a pole in a footing; `options_preview.py` and `concept_media.py` clip parts at ground level first.
- `render.py --check` requires `media/options.png`, which `.kit/options.py` makes, but the brief forbids running it here; the shaded stand-in from `options_preview.py` fills the gap until the Cycles render.
- `.kit/concept.py` `render_all` projects every part for the blueprint in one hidden-line pass, which ran out of memory for a D3 model of 215 parts; worked around with a blueprint-only mode in `cad/src/concept_media.py`.
- `.kit/stem_check.py` `claim()` gives only within, plausible or fails, so a "Fails, fix proposed" row with a number (S31) has to go through `cited()`.

### Recommended next step

Amish decides O1 to O5. Then the coordinator renders `media/options.png`, the hero and studio views and the cards from the D3 models. The design is not ready for TRL 4 work until the chlorine drift question is planned as the first bench test (WWT-PLN-001); no TRL 4 work was started.

## Session 2026-10-25: decisions

Amish, 2026-10-25 10:19 CT, after a report listing each repo's proposed decisions and recommendations: "i concur with your recommendations". Every decision that carried a recommendation is recorded as decided with the option recommended; every decision without a pick stays open.

### Decided by Amish, 2026-10-25

- **O1 concept:** option A (196 of 245), B the fallback if the TRL 4 drift test fails. `project.yaml` `concept_chosen: A`; WWT-DDR-004 v0.2 decided (D1); WWT-OPT-001 v0.2; WWT-PLN-001 v0.2; README.
- **O2 calibration reference:** a shared handheld DPD photometer per operator (±0.03 mg/L ±3 %, USD 379.99 to 599.99, WWT-MKT-001), outside the unit cost. `docs/04-calcs/sizing.py` new row E12 reruns the chlorine budget with it: 8 of 8 cases met at zero drift, worst ±0.411 against ±0.450 mg/L (1.5 mg/L, pH 8.5), 0.146 mg/L left for drift. PR-010 and the build plan's first chlorine check now name the photometer (WWT-BLD-001 v0.4); PLN calibration kit line; PRC calibration kit row.
- **O3 product render layout:** installed heights, as `cad/src/product_model.py` already draws them. No change.
- **O4 PR-008:** counts the hourly schedule only (19.8 L/day at tolerance); the requirement text says so. STEM S7 wording.
- **O5 PR-001:** restated as ±30 % above 1.0 mg/L (`r1_target()` in `sizing.py`). With it, E9 8 of 8 (was 6), E10 4 of 4 with the comparator and with the photometer (were 1 and 2), E7 10 of 10 at 40 °C (was 9), E11 8 of 8. PR-001 **not met to met on paper**; STEM S31 from "fails, fix proposed" to **Within known science** (WWT-STM-001 v0.2: 28 within and 9 plausible for option A; 36 within and 13 plausible overall; `stem_check` stays open). Drift room behind PR-001 and PR-010 is now about 0.15 mg/L a month (was 0.13); S12 restated.
- Documents: WWT-PRS-001 v0.8, WWT-CAL-001 v0.7 (Table 3, section E, R1, R8, R10, counts: 3 at risk, 6 met on paper, 1 over target, 3 met by design), WWT-STM-001 v0.2, WWT-DEC-001 v0.5 (O1 to O5 moved to decisions made), WWT-DDR-004 v0.2, WWT-OPT-001 v0.2, WWT-PRC-001 v0.9, WWT-PLN-001 v0.2, WWT-BLD-001 v0.4, README, `project.yaml`. No part, dimension or BOM line changed; `budget_usd` unchanged (USD 325 against USD 300).

### Still open (no recommendation to concur with)

- The approach to the first candidate partner (Water Mission) and the first region: Amish's outreach, with no option recommended in this round.

### Checks

Run in this order on 2026-10-25 (no edit to `cad/src/` or `bom/bom.csv` this session):

- `python3 docs/04-calcs/sizing.py`: runs; L: 6 met on paper, 3 at risk, 1 over target, 3 met by design (R1 met on paper, E12 8 of 8).
- `python3 docs/04-calcs/stem_check.py`: open, 36 within, 13 plausible, 0 fail.
- `python3 .kit/trace.py`: RTM regenerated, 0 gaps.
- `python3 .kit/cad_check.py --export`: PASS at D3.
- `python3 .kit/render.py` and `python3 .kit/render.py --check`: pass, no FAIL.
- `python3 -m reuse lint`: compliant.
- Em and en dash scan outside `.kit/` and `LICENSES/`: none.
