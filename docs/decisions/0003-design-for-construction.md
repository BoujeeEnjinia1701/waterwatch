---
doc_id: WWT-DDR-003
title: WaterWatch design for construction
project: WaterWatch
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-02
- **Status:** Draft. Every change in Table 1 was made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish approved the build plan format for the portfolio and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of WWT-DDR-002 showed what WaterWatch does and passed its calculations, but many of its parts were shapes that could not be made, fixed or fitted as drawn. Checking the model with build123d (intersections, distances and volumes between every pair of parts) found the thirteen problems below.

The changes keep what WaterWatch does: the same pole, footing and heights, the same enclosure, battery, controller, modem, panel and tilt, the same flow cell cavity, water volume, baffle size, inlet at the bottom and outlet near the top with its air break, the same sensors, valve, regulator, check valve and drain, and the same sun shield gap. Nothing here changes the pitch, the measurement principle or the safety case. Every change is in `cad/src/model.py`, which now runs 97 constructability checks (`python cad/src/model.py --check`): 68 pairs that must touch do touch without overlapping, 17 pairs keep their stated clearance, no two of the 53 parts overlap, the light path in the cell is clear of every part, and the windows stay under water when the cell stands full. All 97 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The enclosure and cell "plates" were solid 10 mm and 43 mm blocks that met the round pole along a line, and the four clamps were rings round the pole joined to nothing. | Two 3 mm aluminium back plates (enclosure plate 270 x 420 mm, cell plate 140 x 385 mm), each held to the pole by two M8 U-bolts through 90° V-saddles, with nyloc nuts on the plate front. The pole axis moves from 94 to 103 mm behind the enclosure centre. | A U-bolt with a V-saddle is the standard bought way to hold a flat plate to a round pole; the pole bears on both faces of the V and the U-bolt pulls it in. The heights of every part are unchanged. |
| P2 | The enclosure had no fixing to its plate. | The enclosure maker's kit of four external lugs, one at each back corner, feet on the box top and bottom, each held by one M5 screw through the plate. | The box back stays sealed and flat on the plate. |
| P3 | The battery, controller and modem floated against the back wall. | A printed internal plate (186 x 205 x 3 mm) on the box's four moulded bosses, 6 mm off the back wall and 37 mm above the floor; boards on 6 mm standoffs; the battery under a strap. The modem moves 13 mm up and 5 mm right, the battery 48 mm up and the controller 5 mm down, to clear the bosses and the gland nuts. | Uses what a stock box already has; leaves room above the floor for cables to bend up from the glands. |
| P4 | The antenna stood on the enclosure top and passed through the sun shield; the panel lead came down through the shield to a top entry; only three glands served five cables. | Every entry is in the bottom face, in two rows 28 and 70 mm from the back face: six M16 glands (panel lead, valve, chlorine, temperature, optics, and a spare closed by a blanking plug for the pH probe variant), the vent and the antenna bulkhead, with the whip pointing down. The panel lead runs down the back of the pole and comes forward under the plate with a drip loop. | Nothing passes through the shield, so the shield can come off, and no entry faces the rain. Flanges are at least 16 mm apart, room for a spanner. |
| P5 | The sun shield had no fixing and could not lift off over the antenna. | A 15 mm flange folded in at the back of each side lies flat on the plate; four M5 thumb screws into tapped holes in the plate. The shield slides off forward. | No tools at the pole; the 25 mm gap on the top, sides and front and the open bottom are unchanged, so the thermal result stands. |
| P6 | The turbidity "head" was one block on the left wall, which cannot give both a 90° scatter path and a 180° reference path; and a beam across the cell at mid-height would have struck the baffle and the chlorine sensor. | Three holders, each 20 x 20 x 16 mm with a 6 mm window: the LED on the left wall, the 180° reference detector on the right wall, the 90° detector on the front wall. The beam runs 13 mm in front of the cavity centre, 41 mm above the underside of the cell. The baffle, unchanged in size, now stands on the back wall instead of the front. | This is the Kelley et al. (2014) geometry the concept cites. The dark back wall is the light trap. The beam is 16 mm under the standing water level. |
| P7 | The three lid ports were in one line: the chlorine and pH gland bodies would have overlapped (22 mm apart, 30 mm needed), and a pH probe in the centre port would have hit the baffle. | Lid layout: chlorine (M25 gland) 24 mm left of centre and 8 mm behind it, spare pH port (M20 gland and blanking plug) 14 mm right and 10 mm behind, temperature probe (M12 gland) 34 mm right and 4 mm in front. | Every gland body clears the others and the thumb nuts; every probe clears the walls, the baffle, the beam and the 90° detector's line of sight. |
| P8 | The cell lid had no fixing and no seal; it was "tool-free" in words only. | A 1.5 mm EPDM gasket and four M4 studs in the body's corners, with knurled thumb nuts. | The lid lifts off with the sensors in it for the monthly clean, without tools. |
| P9 | The cell was held on by nothing. | The back wall is 14 mm thick (body 96 x 60 x 74 mm instead of 96 x 54 x 74 mm); two M5 screws from behind the plate go 10 mm into it, 4 mm short of the water. The cavity and its 0.185 L are unchanged. | No hole through a wet wall; the plate and the screws are reached from behind with the cell full. |
| P10 | The valve hung on the 1/4 in tube, 230 mm from the riser, with no support. | The valve is screwed to the cell plate under the cell (two M4 screws from behind); its outlet goes up through a push-fit elbow into the cell floor. The tube run falls from 738 to 696 mm (10.7 to 10.1 mL). | A plastic tube cannot carry a valve. Keeping the valve beside the cell also keeps the stale water between valve and cell short. |
| P11 | The panel bracket was a rod passing into the pole top. | A bought pole-top tilt mount: a sleeve over the pole top with two set screws and a tilt rail under the panel. | A stock part for a 48 mm pole; the panel position and 30° tilt are unchanged. |
| P12 | The strainer, check valve and regulator were joined by lengths of 1/4 in tube, and the check valve was not drawn. | The isolation valve, strainer, check valve and regulator screw together in one brass line on short nipples off the saddle tee; the tube starts at the regulator outlet. | Threaded fittings make a rigid line; the check valve is now shown where it must go. |
| P13 | Cables ran through the air 60 mm from the pole and through the shield. | Every cable has a route: sensor and valve cables up the front of the cell plate to their glands, the optics cable from the LED holder, the panel lead down the back of the pole. Each clears every part it is not fixed to. | So the plan can say where each one goes. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Lines 1, 2, 3, 8, 9, 10, 13, 14, 15, 16 and 17 respecified; lines 18 (mounting plates), 19 (lugs and internal plate) and 20 (fixings) added. 20 lines, USD 319.00 (was USD 283.00). | Parts added for construction: plates USD 10, lugs and internal plate USD 8, fixings USD 6, three more glands and a blanking plug USD 4, cell gasket, studs and lid glands USD 4, push-fit elbows USD 2, shield fixing USD 1, drain hose tail USD 1. |
| Cost | Value-engineering target: USD 300. Estimated cost of the constructable design: USD 319 (USD 19 over the target). `budget_usd` unchanged. | Savings worth trying are in the design decisions register (WWT-DEC-001). |
| Calculations | WWT-CAL-001 v0.3: tube run 696 mm and 10.1 mL [D1]; two chlorine error figures move by 0.001 mg/L [E4]; cost [K1], [K2]. No requirement changes status except R12, now reported as over the value-engineering target. Energy, solar, temperature, water use, data, alert latency, wind and task times are unchanged. | Re-run of `docs/04-calcs/sizing.py`. |
| Documents | WWT-REQ-001 v0.5 and WWT-PRC-001 v0.5 updated; WWT-DWG-001 Rev P4; making sketches WWT-DWG-101 to 109; build plan WWT-BLD-001; design decisions register WWT-DEC-001. | Follow the model. |
| Media | `media/hero.png`, `cutaway.png`, `exploded.png`, `concept-blueprint.*`, `flow.png`, `model.glb` regenerated. The photoreal renders, `media/card.png` and `media/social-preview.png` (made on Amish's Mac) still show the concept: the antenna through the shield top and the single turbidity block. | Visible change. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The shield now comes off by hand, which lowers tamper resistance at a public tapstand. | (a) knurled thumb screws, as modelled; (b) tamper-resistant M5 screws, which add about 2 minutes to a visit that only rarely needs the box open. | (a) for the prototype; (b) for field units after the first site visit. |
| A2 | The antenna now points down from the bottom face, about 0.1 m above the cell lid and 0.13 m from the steel pole. | (a) keep it there and measure signal strength at TRL 4; (b) a short cable to an antenna on the pole top beside the panel. | (a): it keeps the shield free and costs nothing; (b) if a weak-signal site needs it. |
| A3 | Water stands in the cell only up to the outlet's lower edge, 17 mm below the lid, about 0.14 L, not the full 0.185 L the calculation uses. | (a) keep 0.185 L in WWT-CAL-001, which is conservative for flushing (a smaller standing volume is cleared faster), and measure at TRL 4; (b) revise the calculation now. | (a): no requirement changes, and the chlorine tip stays 23 mm under water. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan WWT-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: none not met, 4 at risk (R1, R2, R9, R10), 5 met on paper, 3 met by design, and R12 over the value-engineering target by USD 19 (WWT-CAL-001 v0.3).
- The appearance model `cad/src/product_model.py` and the photoreal renders still show the concept layout; they need updating on Amish's Mac, where Blender is.
- The enclosure, U-bolt kits, valve and pole-top mount are chosen at TRL 4; the items to confirm when they are bought are listed in WWT-DEC-001.
