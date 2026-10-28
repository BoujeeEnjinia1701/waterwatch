---
doc_id: WWT-DEC-001
title: WaterWatch design decisions register
project: WaterWatch
doc_type: Design decisions register
version: '0.5'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open items 1 to 10 on 2026-10-02 (WWT-DDR-003 accepted with A1 to A3, render and appearance items, Water Mission as first candidate partner, alert and data rules); moved to decisions made
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions carried out: status light in the model, BOM line 21 and a seventh gland (cost USD 322); alert message templates; tamper-resistant shield screws named for field units"
  - version: "0.4"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: O1 to O5 opened (concept, calibration reference, render layout, water-use counting, chlorine target above 1 mg/L; proposed, awaiting Amish); F1 and F5 to F8 made under the standing instruction of 2026-10-23 (STEM check and its independent review); F2 to F4 detail changes found while modelling to D3, made under the instruction of 2026-09-30; cost USD 325"
  - version: '0.5'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Amish decided O1 to O5 as recommended on 2026-10-25 ("i concur with your recommendations"); moved to decisions made'
---

# WaterWatch design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, WWT-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None open from the kit 1.9.1 upgrade: Amish decided O1 to O5 on 2026-10-25 as recommended ("i concur with your recommendations"); they are under Decisions made. The approach to the first candidate partner (Water Mission, decided 2026-10-02) is Amish's outreach and stays with him.

| # | Decision | Options | Recommendation | Record |
| --- | --- | --- | --- | --- |

## Decided under Amish's standing instructions (kit 1.9.1 upgrade)

Made in the session of 2026-10-25 without a new decision from Amish, under the instruction named; each can be reversed.

| # | Change | Why | Options weighed | Cost | Instruction |
| --- | --- | --- | --- | --- | --- |
| F1 | Battery: one 32700 LiFePO4 cell (1S1P), 3.2 V, 6 Ah, 0.135 kg, in place of "1S2P 32700 cells, 3.2 V, 6 Ah" | STEM check S3 failed: one 32700 cell holds about 6 Ah, so the stated pack did not match its cells, and the calculation used two cells' mass (WWT-STM-001) | Two 32700 cells, 12 Ah (more autonomy, about USD 4 more, a parallel joint); two 26650 cells, 6.4 Ah (two joints); one 32700 cell, 6 Ah (chosen: simplest, every energy figure kept) | None; BOM line 5 held at USD 20 | Standing instruction of 2026-10-23 (fix rule, STANDARDS section 20) |
| F2 | Lug screws: M5 x 16 hex screws with a washer under the head and under the nut, in place of M5 x 12 | Through a 3 mm lug tab and a 3 mm plate, two washers and a nyloc nut need about 14 mm; 12 mm leaves no thread showing | M5 x 12 without washers; M5 x 16 with washers (chosen) | None (line 20 unchanged) | Instruction of 2026-09-30, make the design physically buildable (WWT-DDR-003) |
| F3 | Battery tray held to the internal plate by two M3 x 8 screws and nuts, in place of a strap round the pack and the plate | A strap round the plate would need slots in the printed plate and clash with the plate's bosses; the tray screws hold the cell, its protection board and fuse as one unit | Strap with plate slots; tray screws (chosen) | None (line 20 unchanged) | Instruction of 2026-09-30 (WWT-DDR-003) |
| F4 | Pole-top mount rail modelled 190 mm long, the panel's height, so its four M5 bolts reach the panel frame's bottom flange | The 150 mm rail of the TRL 3 model stopped short of the frame, so the panel had no bolted joint | Clamps on the frame edge; a rail the panel's height (chosen); to confirm with the bought mount (to confirm 4) | None (bought mount, line 2) | Instruction of 2026-09-30 (WWT-DDR-003) |
| F5 | Flush of 110 s at sites whose supply is below 0.7 bar, set per site at commissioning (90 s elsewhere) | Independent review of S6: below the regulator's compensating pressure the flow falls to about 0.35 L/min and 90 s leaves 8.5 % stale water against 5 % | 110 s everywhere (wastes water at normal pressure); a regulator for lower pressure (not a catalogue part at 0.5 L/min); per-site 110 s (chosen) | None (firmware setting); 15.4 L/day and 35 mWh/day more at such sites | Standing instruction of 2026-10-23 (fix rule) |
| F6 | Latching valve specified as rated to open against at least 4 bar | Independent review of S15: a small direct-acting valve has a maximum opening differential | None, or a pilot valve (needs a minimum pressure, rejected at TRL 3) | None (BOM line 13 wording) | Standing instruction of 2026-10-23 (fix rule) |
| F7 | Firmware keeps TLS sessions between uploads (session resumption) | Independent review of S20: a full handshake every session gives 1.22 MB a month against PR-006's 1 MB | Fewer uploads (slower data); MQTT over a kept session; TLS resumption (chosen, simplest) | None | Standing instruction of 2026-10-23 (fix rule) |
| F8 | A second check valve, 1/4 in push-fit inline, at the cell inlet | Independent review of S8: on an intermittent main the inlet side relied on one plain check valve | An inlet air gap with a gravity-fed cell (a change of layout); a verifiable backflow preventer (larger, dearer; to assess under the local code); a second check valve (chosen) | USD 3 on BOM line 14 (indicative); parts USD 325 | Standing instruction of 2026-10-23 (fix rule) |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The enclosure model, its boss spacing (assumed 166 x 185 mm) and its four-lug kit | They set the internal plate holes and the lug holes in the back plate | WWT-DDR-003, P2 and P3 |
| 2 | The U-bolt and V-saddle kits fit 48.3 mm pipe, and the depth of the saddle's V | The V sets how far the pole sits behind the plates (40 mm assumed) | WWT-DDR-003, P1 |
| 3 | The valve has two M4 mounting holes in its back face, or a maker's bracket | Sets the valve holes in the cell plate | WWT-DDR-003, P10 |
| 4 | The pole-top mount fits 48.3 mm pipe and the panel frame's holes | The panel position and tilt depend on it | WWT-DDR-003, P11 |
| 5 | The M25 gland grips the 16 mm chlorine sensor body and the M12 gland the 6 mm temperature probe | Gland clamping ranges differ between makers | WWT-DDR-003, P7 |
| 6 | The push-fit elbows and the inlet fitting are 1/8 BSPT; the hose tail is 3/8 BSP for 12 mm hose | Sets the taps for the cell body | WWT-DDR-003, P9 and P10 |
| 7 | The light-to-frequency detectors and the 860 nm LED fit a 5 mm bore | Sets the holder bore | WWT-DDR-003, P6 |
| 8 | The charger's charging window is 0 to 45 °C in its datasheet | Some chargers of this class fix a different window | WWT-DDR-001, D9 |
| 9 | The 32700 cell's maker datasheet: 6 Ah, charge window, UN 38.3 test summary | The capacity was taken from a reseller listing | WWT-DEC-001 F1; WWT-STM-001 S3 |
| 10 | The latching valve opens against 4 bar; the 1/4 in PE tube is rated 10 bar or more | Opening differential and surge (6 bar on closing) | WWT-DEC-001 F6; WWT-STM-001 S15, S37 |

## Value engineering

Value-engineering target: USD 300 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 325 per base unit, USD 3 more since 2026-10-02 for the second check valve of F8 (USD 25 over the target), from `bom/bom.csv` (WWT-CAL-001, K1). A pH probe variant site costs about USD 385 to 425. Main cost drivers and savings worth trying:

- The largest lines are the pole with its U-bolts and saddles (USD 35), the controller carrier board (USD 32), the cellular modem (USD 30), the chlorine sensor (USD 25), the enclosure (USD 22), the battery (USD 20) and the sample line fittings (USD 23).
- Making the design constructable added USD 36: the two back plates (USD 10), the lugs and internal plate (USD 8), fixings (USD 6), three more glands and a blanking plug (USD 4), the cell's gasket, studs and lid glands (USD 4), push-fit elbows (USD 2), the shield fixing (USD 1) and the drain hose tail (USD 1). The status light of 2026-10-02 added USD 3 (lens unit and lead USD 2, a seventh gland USD 1).
- Savings worth trying: the LoRaWAN modem variant (about USD 12 instead of USD 30) where a gateway is in range, which alone brings the unit to about USD 304; a box with moulded mounting flanges instead of a separate lug kit (about USD 3); cutting both back plates from one offcut and buying fixings in bulk for several units (about USD 3 to 5); a locally sourced pole or an existing post at sites that have one (up to about USD 25).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: membrane-free graphite chlorine sensor with monthly DPD check, site pH with a pH probe variant, cellular with LoRaWAN as a variant, separate pole, hourly 90 s flush, 0.2 mg/L and 5 NTU alerts, drain to the basin, tapstands first, LiFePO4 with 0 to 45 °C charging, no SwapCell | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | WWT-DDR-001 |
| 2026-09-25 | D11 to D14: R1 relaxed to ±0.2 mg/L or ±25 %; pH probe at sites above pH 7.5 or moving more than 0.2; confirming reading 15 min after a first crossing; footing cast on the survey visit | Amish: "i accept all your recommendations, go with them across all repos." | WWT-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan and in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | WWT-DDR-003 (changes made under this instruction, open for review: open decision 1) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | `.kit/STANDARDS.md` section 18; this register |
| 2026-10-02 | Design for construction accepted: the changes P1 to P13 of WWT-DDR-003, as made | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-003, Table 1 |
| 2026-10-02 | Shield fixing: knurled thumb screws for the prototype; tamper-resistant M5 screws on field units after the first site visit | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-003, A1 |
| 2026-10-02 | Antenna: the whip points down from the bottom face, and signal strength is measured at TRL 4; a pole-top antenna is used only at a weak-signal site | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-003, A2 |
| 2026-10-02 | Water volume in the calculation: the full-cavity 0.185 L is kept, conservative for flushing; the standing volume is measured at TRL 4 | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-003, A3 |
| 2026-10-02 | Product render layout: the render-only layout with heights drawn closer together is kept, with the note on the hero render | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 2026-10-02 | Status light: one low-duty LED behind a lens in the shield front, with an open-bottom slot so the shield still slides off (carried out 2026-10-02: lens unit in a 12.2 mm slot, BOM line 21, USD 2 plus a gland USD 1) | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-02 | Enclosure lid: a clear-lid enclosure is accepted, and BOM line 3 says so | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-02 | First co-design partner and region: a scheme operator that runs chlorinated, solar-powered piped schemes with public tapstands; the first candidate to approach is Water Mission, which runs such schemes in East Africa, with the first region taken from its country programs | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-001, O1 |
| 2026-10-02 | Alert language and recipients: alerts go by SMS in the site's main local language, with an English copy to the operator, stating only what was measured, when and the threshold crossed; they go to the caretaker and the operator's maintenance contact, with a weekly summary to the district water officer | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-001, O2 |
| 2026-10-02 | Data ownership: the scheme operator owns the data; the water committee and the district water and health offices can see it; anonymized site data are published only with the operator's written agreement | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WWT-DDR-001, O3 |
| 2026-10-25 | O1 concept carried forward: option A, the timed-flush flow cell on its own pole (196 of 245), with option B as the fallback if the TRL 4 drift test fails | Amish: "i concur with your recommendations" | WWT-DDR-004 D1 v0.2; WWT-OPT-001 v0.2; `project.yaml` `concept_chosen: A` |
| 2026-10-25 | O2 calibration reference: a shared handheld DPD photometer per operator (±0.03 mg/L ±3 %, Hanna HI97711 class, USD 379.99 to 599.99, WWT-MKT-001), outside the unit cost, in place of the colour comparator for chlorine; WWT-CAL-001 E rerun with its accuracy (E12: 8 of 8 cases met, 0.15 mg/L left for drift) | Amish: "i concur with your recommendations" | WWT-DDR-004 D2; WWT-CAL-001 v0.7 E12; WWT-PRS-001 v0.8 PR-001, PR-010; WWT-BLD-001 v0.4 first checks |
| 2026-10-25 | O3 product render layout: the installed heights, as the kit 1.9.1 product model built from `components("A")` shows them, in place of the render-only layout of 2026-10-02 | Amish: "i concur with your recommendations" | `cad/src/product_model.py` (no change) |
| 2026-10-25 | O4 PR-008 water use counts the hourly schedule only (19.8 L/day at tolerance), not the rare alert-driven confirming readings; said so in PR-008 | Amish: "i concur with your recommendations" | WWT-PRS-001 v0.8 PR-008; WWT-STM-001 S7; WWT-CAL-001 R8 |
| 2026-10-25 | O5 PR-001 target restated as ±30 % above 1.0 mg/L (±0.2 mg/L or ±25 % up to 1.0 mg/L unchanged); PR-001 not met to met on paper | Amish: "i concur with your recommendations" | WWT-PRS-001 v0.8 PR-001; WWT-CAL-001 v0.7 E11, E12; WWT-STM-001 v0.2 S31 |
