---
doc_id: WWT-DEC-001
title: WaterWatch design decisions register
project: WaterWatch
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
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
---

# WaterWatch design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, WWT-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

## Value engineering

Value-engineering target: USD 300 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 322 per base unit (USD 22 over the target), from `bom/bom.csv` (WWT-CAL-001, K1). A pH probe variant site costs about USD 382 to 422. Main cost drivers and savings worth trying:

- The largest lines are the pole with its U-bolts and saddles (USD 35), the controller carrier board (USD 32), the cellular modem (USD 30), the chlorine sensor (USD 25), the enclosure (USD 22), the battery (USD 20) and the sample line fittings (USD 20).
- Making the design constructable added USD 36: the two back plates (USD 10), the lugs and internal plate (USD 8), fixings (USD 6), three more glands and a blanking plug (USD 4), the cell's gasket, studs and lid glands (USD 4), push-fit elbows (USD 2), the shield fixing (USD 1) and the drain hose tail (USD 1). The status light of 2026-10-02 added USD 3 (lens unit and lead USD 2, a seventh gland USD 1).
- Savings worth trying: the LoRaWAN modem variant (about USD 12 instead of USD 30) where a gateway is in range, which alone brings the unit to about USD 301; a box with moulded mounting flanges instead of a separate lug kit (about USD 3); cutting both back plates from one offcut and buying fixings in bulk for several units (about USD 3 to 5); a locally sourced pole or an existing post at sites that have one (up to about USD 25).

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
