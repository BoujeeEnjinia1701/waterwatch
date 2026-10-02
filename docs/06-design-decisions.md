---
doc_id: WWT-DEC-001
title: WaterWatch design decisions register
project: WaterWatch
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# WaterWatch design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, WWT-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review the design-for-construction changes P1 to P13 (back plates on U-bolts, entries underneath, shield fixing, three optics holders, baffle on the back wall, lid layout, valve on the cell plate, pole-top mount and others) | Accept; or ask for changes | Accept | Every component and step of the build plan | WWT-DDR-003, Table 1 |
| 2 | Shield fixing at public sites | (a) knurled thumb screws; (b) tamper-resistant M5 screws | (a) for the prototype; (b) for field units after the first site visit | Sun shield, step 18 | WWT-DDR-003, A1 |
| 3 | Antenna position | (a) whip pointing down from the bottom face; (b) short cable to an antenna on the pole top | (a), and measure signal strength at TRL 4 | Enclosure bottom face, antenna | WWT-DDR-003, A2 |
| 4 | Water volume used in the calculation | (a) keep the full-cavity 0.185 L, conservative for flushing; (b) revise to the standing volume of about 0.14 L now | (a), measure at TRL 4 | None in the build; WWT-CAL-001 section D | WWT-DDR-003, A3 |
| 5 | Product render layout of heights | (a) keep the render-only layout with heights drawn closer together; (b) render at installed heights | (a), with the note on the hero render | Renders only, not the build | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 6 | Status light | (a) one low-duty LED behind a lens in the shield front, with an open-bottom slot so the shield still comes off; (b) no light | (a) | Controller wiring and the shield, if adopted | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 7 | Clear enclosure lid | (a) accept a clear-lid box and say so in BOM line 3; (b) grey lid | (a) | Enclosure purchase | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 8 | First co-design partner and region | Partner type and region of the first site | None yet; partners are picked per area later | Site survey and installation | WWT-DDR-001, O1 |
| 9 | Alert language and recipients | Wording beyond the R13 rule, recipients per site | None yet; from co-design | Firmware settings, not the hardware | WWT-DDR-001, O2 |
| 10 | Data ownership | Who owns the data and who may see it | None yet; from co-design | Upload endpoint, not the hardware | WWT-DDR-001, O3 |

The 2026-09-26 proposal to add a panel gland on the enclosure top (`docs/REVIEW.md`, item 4) is overtaken by WWT-DDR-003, P4, which puts every entry in the bottom face, the option that review offered.

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

Value-engineering target: USD 300 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 319 per base unit (USD 19 over the target), from `bom/bom.csv` (WWT-CAL-001, K1). A pH probe variant site costs about USD 379 to 419. Main cost drivers and savings worth trying:

- The largest lines are the pole with its U-bolts and saddles (USD 35), the controller carrier board (USD 32), the cellular modem (USD 30), the chlorine sensor (USD 25), the enclosure (USD 22), the battery (USD 20) and the sample line fittings (USD 20).
- Making the design constructable added USD 36: the two back plates (USD 10), the lugs and internal plate (USD 8), fixings (USD 6), three more glands and a blanking plug (USD 4), the cell's gasket, studs and lid glands (USD 4), push-fit elbows (USD 2), the shield fixing (USD 1) and the drain hose tail (USD 1).
- Savings worth trying: the LoRaWAN modem variant (about USD 12 instead of USD 30) where a gateway is in range, which alone brings the unit to about USD 301; a box with moulded mounting flanges instead of a separate lug kit (about USD 3); cutting both back plates from one offcut and buying fixings in bulk for several units (about USD 3 to 5); a locally sourced pole or an existing post at sites that have one (up to about USD 25).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: membrane-free graphite chlorine sensor with monthly DPD check, site pH with a pH probe variant, cellular with LoRaWAN as a variant, separate pole, hourly 90 s flush, 0.2 mg/L and 5 NTU alerts, drain to the basin, tapstands first, LiFePO4 with 0 to 45 °C charging, no SwapCell | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | WWT-DDR-001 |
| 2026-09-25 | D11 to D14: R1 relaxed to ±0.2 mg/L or ±25 %; pH probe at sites above pH 7.5 or moving more than 0.2; confirming reading 15 min after a first crossing; footing cast on the survey visit | Amish: "i accept all your recommendations, go with them across all repos." | WWT-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan and in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | WWT-DDR-003 (changes made under this instruction, open for review: open decision 1) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | `.kit/STANDARDS.md` section 18; this register |
