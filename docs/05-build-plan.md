---
doc_id: WWT-BLD-001
title: WaterWatch prototype build plan
project: WaterWatch
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: First build plan; design made constructable (WWT-DDR-003)
---

# WaterWatch prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order: the enclosure group on the left, the flow cell group on the right, the panel above. The pole, the existing tapstand and the long runs of tube, hose and cable are left out.*

The prototype is one WaterWatch on its own galvanized pole beside a village tapstand. Two flat aluminium back plates are held to the pole by U-bolts: the upper one carries a grey plastic box holding the battery, controller and cellular modem under a white sun shield; the lower one carries a small black flow cell with its sensors and, under it, the valve that lets a sample in once an hour. A saddle tee on the tapstand riser feeds the valve through a line of screwed brass fittings and a thin plastic tube; the cell drains through an open air break to the tapstand basin. A 5 W panel sits on the pole top. Figure 1 shows the 22 components in the order you make or fit them. Eight are made in a small workshop: the two back plates, the internal plate, the flow cell body and lid, the three optics holders and the chlorine sensor; the sun shield is folded by a sheet metal shop to a sketch; the bought box is drilled. Everything else is bought and fitted. The work is cutting and drilling aluminium sheet, drilling a plastic box, milling or printing a plastic block, tapping threads in plastic, two small prints, soldering and potting three electrodes, wiring bought boards with screw terminals, and simple plumbing with thread tape and push-fit tube. The parts cost about USD 319 from the bill of materials.

> **Safety:** The prototype holds a lithium iron phosphate battery of 19.2 Wh and its charger. Keep the battery fuse out until section 6 says otherwise, never charge below 0 °C or above 45 °C, and never leave a first build charging unattended. The sample line connects to a pressurized drinking water supply: shut the supply off before fitting the saddle tee, fit the check valve the right way round, and keep the open air break so nothing can flow back. Cut aluminium edges are sharp; deburr everything. Printing ASA and milling PVC give off fumes and dust; work with ventilation. Wet concrete burns skin; wear gloves.

## 2. What changed to make it buildable

The concept showed what WaterWatch does; many of its parts could not be made, fixed or fitted as drawn. Each change below keeps what it does, and all of them are recorded in decision record WWT-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Pole fixing | Solid 10 mm and 43 mm blocks touching the round pole along a line; clamp rings joined to nothing | Two 3 mm aluminium back plates, each on two M8 U-bolts through V-saddles (Figure 4) | The standard bought way to hold a flat plate to a round pole |
| Enclosure | No fixing to its plate; parts inside floating | The maker's four lugs (Figure 6); a printed internal plate on the box's moulded bosses (Figure 9) | The box back stays sealed; everything inside is screwed down |
| Entries | Antenna and panel lead through the sun shield top; three glands for five cables | Six glands (one a plugged spare), the vent and the antenna all in the bottom face, in two rows (Figure 7) | Nothing passes through the shield, and no entry faces the rain |
| Sun shield | No fixing; trapped by the antenna | Flanges folded in at the back, four thumb screws; slides off forward (Figure 13) | Comes off by hand at the pole; same 25 mm air gap |
| Turbidity optics | One block on one wall, which cannot see at both 90° and 180°; the beam would have hit the baffle | Three holders on three walls; baffle moved to the back wall, same size (Figure 21) | Gives the 90° scatter and 180° reference paths the concept cites |
| Flow cell lid | Three ports in a line, two of them overlapping; no seal or fixing | Glands laid out clear of each other, a gasket, four studs and thumb nuts (Figures 24 and 25) | Every gland fits and every probe clears the beam and the baffle |
| Flow cell body | Held on by nothing; 8 mm back wall | 14 mm back wall with two screws from behind the plate (Figure 17) | No hole through a wet wall |
| Valve | Hanging on the plastic tube 230 mm from the riser | Screwed to the cell plate under the cell (Figure 26) | A tube cannot carry a valve; shorter stale run (696 mm instead of 738 mm) |
| Panel | A rod pushed into the pole top | A bought pole-top tilt mount (Figure 28) | A stock part for a 48 mm pole |
| Fittings at the riser | Fittings joined by plastic tube; check valve not drawn | One screwed brass line with the check valve shown (Figure 29) | Rigid, and the check valve is where it must go |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in front of WaterWatch, looking at the enclosure lid. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Enclosure back plate

![Figure 2. Making sketch of the enclosure back plate](../cad/drawings/WWT-DWG-101.png)

*Figure 2. Enclosure back plate making sketch (WWT-DWG-101).*

![Figure 3. Hole positions on both back plates](05-build-plan/plate-holes.png)

*Figure 3. Every hole on both back plates, up from the bottom edge and sideways from the centre line.*

**What it is and what it is made from.** The flat plate the enclosure hangs on, held to the pole by two U-bolts. Aluminium sheet 3 mm thick, 5052 class, cut to 270 x 420 mm.

**How to make it.**

1. Cut the blank square to 270 x 420 mm. File the edges and round the corners to about 3 mm.
2. Scribe a centre line down the long side. Choose one face as the front (the box side) and mark it.
3. Mark every hole from Figure 3: heights up from the bottom edge, sideways from the centre line. Every hole is one of a pair, the same distance each side.
4. U-bolt holes: four 9 mm holes, 29 each side of centre, 25 and 395 up.
5. Lug holes: four 5.5 mm holes, 85 each side of centre, 67 and 353 up.
6. Shield screw holes: four holes 117.5 each side of centre, 100 and 320 up. Drill 4.2 mm and tap M5 (or drill 7 mm and fit M5 rivet nuts).
7. Mark the box outline on the front: 200 wide, centred, from 80 to 340 up.
8. Deburr every hole on both faces.

**How it fits the parts next to it.**

![Figure 4. Joint 1: U-bolt, V-saddle, pole and back plate](05-build-plan/joint-01.png)

*Figure 4. The V-saddle lies flat on the back of the plate; the pole sits on both faces of its V; the U-bolt passes round the back of the pole, through the saddle and the plate, with nyloc nuts on the front.*

The box's back sits flat on the front face between 80 and 340 up, held by four lugs (Figure 6). A V-saddle sits flat on the back face at each U-bolt; the pole centre ends up 40 behind the back face. The sun shield's flanges lie flat on the front face either side of the box (Figure 13).

**Check before moving on.** Lay the lugs and the saddles on the plate and look through each hole: the holes must line up without forcing a screw or a U-bolt leg.

### 3.2 Enclosure body, drilled, with its glands, vent, antenna and lugs

![Figure 5. Drilling sketch of the enclosure body](../cad/drawings/WWT-DWG-102.png)

*Figure 5. Enclosure drilling sketch (WWT-DWG-102), drawn upside down so the top view shows the bottom face.*

![Figure 5a. Bottom face drilling layout](05-build-plan/base-holes.png)

*Figure 5a. Drilling layout, with the box standing upside down on its top and its back face toward you.*

**What it is and what it is made from.** A bought grey polycarbonate box, 200 wide, 120 deep and 260 tall, rated IP66, with a gasketed lid on the front, four moulded bosses inside the back wall and the maker's kit of four external mounting lugs. Eight holes are drilled in its bottom face.

**How to make it.**

1. Stand the box upside down on its top on a soft cloth, back face toward you. Cover the bottom face with masking tape.
2. Mark the holes from Figure 5a. Back row, 28 from the back face: valve cable gland 62 left of centre, chlorine gland 22 left, the spare (plugged) 22 right, temperature gland 62 right. Front row, 70 from the back face: panel lead gland 62 left, optics gland 22 left, vent 22 right, antenna 62 right. Left and right are as seen from the front of the box.
3. Put a block of wood inside under the face. Pilot drill every hole 3 mm at low speed; do not centre punch hard, since polycarbonate cracks.
4. Open each hole with a step drill, light pressure, low speed: 16.2 for the six glands (one is the spare), 12.2 for the vent, 6.5 for the antenna. Before the last step, check the size against the part's datasheet.
5. Deburr inside and out, peel the tape, and clean with water and mild soap only; solvents craze polycarbonate.
6. Fit the four lugs to the box's back corners as the lug kit's maker describes, feet on the top and bottom faces, tabs flush with the back face.

![Figure 6. Joint 2: enclosure lug on the back plate](05-build-plan/joint-02.png)

*Figure 6. Each lug's foot sits on the box; its tab lies flat on the plate beside the box, held by one M5 screw from behind the plate with a nyloc nut in front.*

![Figure 7. Joint 3: the bottom face, seen from below](05-build-plan/joint-03.png)

*Figure 7. Six glands, the vent and the antenna bulkhead in two rows; the whip points down.*

**How it fits the parts next to it.** Each gland, the vent and the antenna bulkhead go in from below with the sealing washer outside and the nut inside (step 1). The outside flanges are at least 16 apart, room for a spanner. The box back sits flat on the back plate, held by the four lugs (step 5).

**Check before moving on.** Each part seats flat on its washer; no crack runs out from any hole under a bright lamp; with the lugs fitted, the box sits flat on the plate and all four lug holes line up.

### 3.3 Internal plate and the electronics on it

![Figure 8. Making sketch of the internal plate](../cad/drawings/WWT-DWG-103.png)

*Figure 8. Internal plate making sketch (WWT-DWG-103).*

**What it is and what it is made from.** A printed plate that carries the battery, the controller carrier board and the cellular modem, and lifts out of the box as one unit. ASA plastic, 186 x 205 x 3 mm, printed flat at 100 % infill in an enclosed printer.

**How to make it.**

1. Measure the four bosses inside your box. The model assumes they are 166 apart across and 185 apart up and down; move the plate's holes to match your box.
2. Print the plate with four 4.5 mm holes at the bosses, 10 in from each edge. Let it cool on the bed so it does not warp.
3. Lay out the parts on the front face, measured from the plate's left and bottom edges: the battery from 8 to 88 across and 18 to 148 up; the modem from 18 to 88 across and 150 to 205 up; the controller from 93 to 183 across and 45 to 165 up.
4. Mark each board's mounting holes through the board, drill 3.2 mm, and fit the boards on M3 screws with 6 mm nylon standoffs. Hold the battery with a strap round it and the plate, with its fuse out.
5. Wire the boards as Figure 10 shows.

![Figure 9. Joint 4: internal plate on a moulded boss](05-build-plan/joint-04.png)

*Figure 9. The plate sits on the four moulded bosses, 6 off the back wall and 37 above the floor, clear of the gland nuts, held by four M4 screws.*

**How it fits the parts next to it.** The plate's back face sits on the ends of the four bosses; four M4 screws go into the bosses. The 37 mm below the plate leaves room for each cable to bend up from its gland.

#### 3.3.1 Wiring

![Figure 10. Block-level wiring](05-build-plan/wiring.png)

*Figure 10. Block-level wiring. No circuit board is laid out at this stage; the bought carrier board stands in for a custom board, which is TRL 4 work.*

Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. Battery to the carrier board's battery terminals, through the 3 A fuse in the battery lead: 0.75 mm² (18 AWG).
2. The battery's temperature sensor to the charger's temperature input, twisted, with the sensor taped to the cells.
3. Panel lead, through its gland, to the carrier board's solar input: 0.5 mm² (20 AWG).
4. Carrier board to the modem: power and serial lines, as the modem maker's carrier describes; antenna pigtail from the modem to the bulkhead, away from the power wires.
5. Chlorine sensor: screened 3-core cable to the potentiostat's working, reference and counter terminals, screen to ground at the board end only.
6. Temperature probe: 3-core to the one-wire input.
7. Optics: 6-core to the LED driver and the two frequency inputs.
8. Valve: 2-core 0.5 mm² to the 12 V valve driver.

Check that the charger's temperature window really is 0 to 45 °C in its datasheet before buying: some chargers of this class fix a different window.

**Check before moving on.** Every wire continues end to end; with the battery fuse out, the battery terminals and every supply read open to ground; every wire is labelled; the plate is flat within 0.5 mm and drops in and lifts out without force.

### 3.4 Sun shield

![Figure 11. Making sketch of the sun shield](../cad/drawings/WWT-DWG-104.png)

*Figure 11. Sun shield making sketch (WWT-DWG-104), for a sheet metal shop.*

**What it is and what it is made from.** A white folded hood that shades the box on its front, sides and top with a 25 mm air gap, so the battery can charge on hot days. White powder-coated aluminium sheet 2 mm.

**How to make it.** Order it from a sheet metal shop with the sketch, or fold it on a press brake:

1. Cut a front 254 x 307 mm with a side 147 deep on each long edge and a top 147 deep on the top edge; add a 10 mm tab on each end of the top and a 15 mm flange on the back edge of each side.
2. Drill a 3 mm relief hole wherever two fold lines cross, so the sheet does not tear.
3. Fold the sides back 90°, then the top, then the tabs down over the sides; rivet each tab with two 4 mm rivets.
4. Fold each flange 90° inward. Drill two 5.5 mm holes in each flange, 7.5 in from the side sheet, 40 and 260 up from the lower edge.
5. Deburr every edge, then powder coat white.

![Figure 12. Step 18 picture: the shield going on](05-build-plan/step-18.png)

*Figure 12. The shield slides over the box from the front.*

![Figure 13. Joint 5: shield flange on the back plate](05-build-plan/joint-05.png)

*Figure 13. The flange lies flat on the back plate, 10 beside the box; an M5 thumb screw holds it.*

**How it fits the parts next to it.** The flanges lie flat on the front of the back plate either side of the box, and four M5 thumb screws go through them into the tapped holes in the plate. The shield stands 25 off the box's front, sides and top, its lower edge 20 below the box, open at the bottom. To open the box, undo the four thumb screws and slide the shield forward.

**Check before moving on.** On a trial fit over the box, the gap is 25, give or take 3, all round.

### 3.5 Cell back plate

![Figure 14. Making sketch of the cell back plate](../cad/drawings/WWT-DWG-105.png)

*Figure 14. Cell back plate making sketch (WWT-DWG-105); hole positions also in Figure 3.*

**What it is and what it is made from.** The flat plate the flow cell and the valve hang on, held to the pole by two U-bolts below the enclosure. Aluminium sheet 3 mm, 5052 class, cut to 140 x 385 mm.

**How to make it.**

1. Cut the blank square to 140 x 385 mm, file the edges and round the corners to about 3 mm. Scribe a centre line and mark the front face.
2. U-bolt holes: four 9 mm holes, 29 each side of centre, 25 and 360 up.
3. Cell screw holes: two 5.5 mm holes, 30 each side of centre, 250 up.
4. Valve screw holes: two 4.5 mm holes, 18 each side of centre, 93 up.
5. Mark the outlines: the cell from 213 to 287 up, 96 wide; the valve from 63 to 123 up, 55 wide; both centred.
6. Deburr every hole on both faces.

**How it fits the parts next to it.** The flow cell's back and the valve's back sit flat on the front face, held by screws from behind (Figures 17 and 26). Two V-saddles sit on the back face, one at each U-bolt, as on the enclosure plate (Figure 4).

**Check before moving on.** Hold the cell body and the valve against the plate: their tapped holes line up with the plate holes.

### 3.6 Flow cell body

![Figure 15. Making sketch of the flow cell body](../cad/drawings/WWT-DWG-106.png)

*Figure 15. Flow cell body making sketch (WWT-DWG-106).*

**What it is and what it is made from.** The dark block the sample flows through: a pocket of 0.19 L with an inlet in the floor, an outlet near the top of the right wall, a baffle on the back wall and three windows for the light. Black PVC block, 96 x 60 x 74 mm, milled; or black ASA printed at 100 % infill.

**How to make it.**

1. Square the block to 96 wide, 60 deep and 74 tall. Mark the front face.
2. Mill a pocket 80 wide and 38 deep (front to back), 66 down from the top, leaving walls of 8 at the front, left and right, 14 at the back, and a floor of 8. Leave a baffle standing on the back wall, 6 thick, 26 deep and 40 tall from the floor, its centre 2 right of the pocket centre; or solvent-weld a PVC strip of that size in place.
3. Windows: drill three 6 mm holes through the walls, centred 41 up from the underside. In the left and right walls they are 14 from the front face; in the front wall it is 8 left of centre. Counterbore each 12 mm, 2.5 deep, from outside, and bed a 2 mm clear acrylic disc in each with neutral-cure silicone.
4. Beside each window, drill and tap two M3 holes 6 deep at the holder's corners (Figure 19).
5. Inlet: in the floor, 32 left of centre and 37.5 from the front face; drill 8.8 and tap 1/8 BSPT.
6. Outlet: in the right wall, 62 up from the underside and 37 from the front face; drill 14.75 and tap 3/8 BSP.
7. Back face: two M5 holes 12 deep, 30 each side of centre, 37 up.
8. Top face: four M4 holes 12 deep, 44 each side of centre, 4 and 53 from the front face, for the lid studs.
9. Deburr; wash out every chip.

**How it fits the parts next to it.**

![Figure 16. Step 7 picture: the cell going onto its plate](05-build-plan/step-07.png)

*Figure 16. The cell goes onto the cell plate with its optics holders already fitted.*

![Figure 17. Joint 6: flow cell on its back plate](05-build-plan/joint-06.png)

*Figure 17. Two M5 screws from behind the plate go 10 into the 14 mm back wall and stop 4 short of the water.*

The back face sits flat on the cell plate, held by two M5 screws from behind. The holders sit on the three windows (Figure 21), the lid on the top face (Figure 24), the inlet fitting in the floor (Figure 26) and the outlet hose tail in the right wall (Figure 27).

**Check before moving on.** Plug the inlet and the outlet, fill the pocket with water and stand it on paper for 30 min: no wet mark. The windows show no daylight from inside when you look in from the top with the holders off and your hand over the pocket.

### 3.7 Optics holders (make 3)

![Figure 19. Making sketch of the optics holder](../cad/drawings/WWT-DWG-107.png)

*Figure 19. Optics holder making sketch (WWT-DWG-107).*

**What it is and what it is made from.** Three small black blocks that hold the infrared LED (left wall), the 90° detector (front wall) and the 180° reference detector (right wall) against their windows and keep daylight out. Black ASA, printed at 100 % infill, 20 x 20 x 16 mm.

**How to make it.**

1. Print three, each with a 5 mm bore 12 deep on the axis from the face that goes on the wall, a 3 mm lead hole from the bore out of the top, and two 3.4 mm holes at opposite corners, 3.5 in from the edges.
2. Push the 860 nm LED into one holder and a light-to-frequency detector into each of the other two, against the window face, leads out of the top.
3. Pot each in black epoxy so no light can reach it except through the window.

![Figure 20. Step 6 picture: the holders going on](05-build-plan/step-06.png)

*Figure 20. Each holder goes onto its window on two M3 screws.*

![Figure 21. Joint 8: the light path in the flow cell](05-build-plan/joint-08.png)

*Figure 21. Cut at the windows, seen from above. The beam runs from the LED on the left to the reference detector on the right, 13 in front of the pocket centre; the 90° detector looks across it from the front; the sensors and the baffle stand behind the beam.*

**How it fits the parts next to it.** Each holder's face sits flat on the cell wall, centred on its window, on two M3 screws. The three leads join one 6-core cable in a heat-shrink splice beside the LED holder.

**Check before moving on.** In a dark room, with the cell full of clean water, each detector reads the same with the room light switched on and off.

### 3.8 Free chlorine sensor

![Figure 22. Making sketch of the free chlorine sensor](../cad/drawings/WWT-DWG-108.png)

*Figure 22. Free chlorine sensor making sketch (WWT-DWG-108).*

**What it is and what it is made from.** A membrane-free three-electrode sensor: a graphite working electrode, a silver chloride reference and a stainless counter electrode, potted in the tip of a plastic tube. 16 mm PVC conduit, 2 mm graphite rod, chlorided silver wire, stainless wire, epoxy.

**How to make it.**

1. Cut 120 mm of 16 mm PVC conduit and deburr both ends.
2. Solder each electrode to a core of a screened 3-core cable and insulate the joints.
3. Hold the three electrodes in a printed jig on a 9 mm circle, 120° apart, standing 3 mm proud of the tube end.
4. Pot the bottom 20 mm of the tube in epoxy and let it cure fully. Seal the top round the cable with adhesive heat shrink.
5. Sand the graphite face flat with 1200 grit and rinse.

**How it fits the parts next to it.** The sensor goes through the M25 gland in the cell lid, its tip 40 below the top of the cell body, clear of the walls, the baffle and the beam (Figure 24).

**Check before moving on.** Dry, the electrodes read more than 10 megohms to each other.

### 3.9 Flow cell lid and gasket

![Figure 23. Making sketch of the lid and gasket](../cad/drawings/WWT-DWG-109.png)

*Figure 23. Flow cell lid and gasket making sketch (WWT-DWG-109).*

![Figure 23a. Lid hole layout](05-build-plan/lid-holes.png)

*Figure 23a. Lid hole layout, front edge at the bottom.*

**What it is and what it is made from.** The lid that carries the chlorine sensor, the temperature probe and the spare pH port, and lifts off with them for cleaning. Black PVC sheet 10 mm, cut to 96 x 60 mm; the gasket from 1.5 mm EPDM sheet.

**How to make it.**

1. Cut the lid to 96 x 60 and mark the front edge.
2. Chlorine gland: drill 23.5 and tap M25 x 1.5, 24 left of centre and 35 from the front edge.
3. Spare pH port: drill 18.5 and tap M20 x 1.5, 14 right of centre and 37 from the front edge.
4. Temperature gland: drill 10.5 and tap M12 x 1.5, 34 right of centre and 23 from the front edge.
5. Stud holes: four 4.5 mm holes, 44 each side of centre, 4 and 53 from the front edge.
6. Gasket: cut the same outline from EPDM, with an 80 x 38 window centred 27 from the front edge and the four stud holes.
7. Screw the M25 and M12 glands and the M20 blanking plug into the lid.

![Figure 24. Joint 7: lid, gasket, glands and studs](05-build-plan/joint-07.png)

*Figure 24. Cut through the chlorine sensor. The gasket sits between body and lid; the glands grip the sensors; the thumb nuts hold the lid down.*

![Figure 25. Step 10 picture: gasket, lid and sensors](05-build-plan/step-10.png)

*Figure 25. The gasket and the lid go down over the four studs; the sensors go in from above.*

**How it fits the parts next to it.** Four M4 studs stand in the body's top face; the gasket and the lid go over them and four knurled thumb nuts hold the lid down, finger tight. The temperature probe goes 45 into the cell through its gland. At a site that needs the pH probe, a gland replaces the blanking plug.

**Check before moving on.** No gland body touches another or a thumb nut; with the cell full to the outlet, nothing drips from under the lid.

### 3.10 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Pole, U-bolts and V-saddles (line 1).** 40 NB galvanized tube, 48.3 x 3.2 mm, 2.7 m long; four M8 U-bolts for 48 mm pipe, each with a 90° V-saddle, washers and nyloc nuts.
- **Solar panel and pole-top mount (line 2).** 5 W monocrystalline, 6 V class, about 250 x 190 mm, aluminium frame with fixing holes; a pole-top tilt mount for 48 mm pipe with set screws.
- **Enclosure and lid (lines 3 and 4).** Polycarbonate, IP66, UV stabilized, 200 x 120 x 260 mm, four moulded bosses inside the back wall, tamper-resistant lid screws, and the maker's four-lug mounting kit (line 19). Drill as section 3.2.
- **Battery (line 5).** LiFePO4, 1S2P 32700 cells, 3.2 V, 6 Ah, with protection board, temperature sensor and an in-line 3 A fuse.
- **Controller carrier (line 6) and modem (line 7).** ESP32-S3 module, LiFePO4 solar charger with a 0 to 45 °C charging window, LMP91000-class potentiostat, 12 V boost valve driver, microSD and real-time clock; LTE-M and NB-IoT modem with 2G fallback and SIM holder.
- **Antenna (line 8).** LTE and GSM whip about 140 mm on an SMA bulkhead for a 6.5 mm hole, with pigtail.
- **Temperature probe (line 12).** DS18B20 in a 6 mm stainless sheath, 1 m cable.
- **Valve (line 13).** 12 V latching, direct acting, normally closed, 1/4 in ports, food-safe wetted parts, with two M4 mounting holes in its back face or the maker's bracket.
- **Sample line (line 14).** 25 mm saddle tee with an isolation ball valve; strainer, check valve and pressure-compensating 0.5 L/min regulator, all screwed in line on brass nipples; 1 m of 1/4 in food-grade PE tube; two push-fit elbows (1/8 BSPT).
- **Drain (line 15).** 3/8 BSP hose tail for 12 mm hose, a tee for the air-break vent, 2 m of 12 mm bore hose and a clamp.
- **Glands and cables (line 16).** Six M16 IP68 nylon glands with nuts, one M16 blanking plug for the spare, one M12 pressure-equalizing vent; sensor and panel cables.
- **Fixings (line 20).** Stainless: 4 x M5 x 12 screws with nyloc nuts (lugs), 4 x M4 x 12 screws (internal plate), 4 x M5 knurled thumb screws (shield), 2 x M5 x 16 screws (cell), 2 x M4 x 10 screws (valve), M3 screws and 6 mm nylon standoffs, a battery strap, UV-stable cable ties.

### 3.11 How the bought parts join

![Figure 26. Joint 9: valve under the cell](05-build-plan/joint-09.png)

*Figure 26. The valve sits flat on the cell plate under the cell, held by two M4 screws from behind. Water comes in from the regulator on the right and leaves upward through a push-fit elbow and a straight tube into the inlet fitting in the cell floor.*

![Figure 27. Joint 10: outlet and air break](05-build-plan/joint-10.png)

*Figure 27. The hose tail screws into the right wall near the top. The tee above it carries an open vent pointing up and the hose pointing down, so the hose cannot siphon the cell and the drain never touches the water in it.*

![Figure 28. Joint 11: panel on the pole-top mount](05-build-plan/joint-11.png)

*Figure 28. The mount's sleeve slides over the pole top and is held by two set screws; the panel bolts to the tilt rail at 30°. The panel lead leaves the junction box beside the rail.*

![Figure 29. Joint 12: saddle tee and fittings on the riser](05-build-plan/joint-12.png)

*Figure 29. The saddle tee clamps round the riser; the isolation valve, strainer, check valve and regulator screw on in that order, flow from left to right.*

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in. Steps 1 to 10 are bench work; steps 11 to 18 are at the site.

### Step 1: glands, vent and antenna into the box

![Step 1](05-build-plan/step-01.png)

Each goes in from below with its sealing washer outside and its nut inside, tightened to the maker's torque. Put the blanking plug in the spare gland until a pH probe is fitted.

### Step 2: lugs onto the box

![Step 2](05-build-plan/step-02.png)

The maker's four lugs on the back corners, feet on the top and bottom faces, tabs flush with the back face.

### Step 3: build the internal plate

![Step 3](05-build-plan/step-03.png)

Boards on M3 screws and standoffs, battery under its strap with its fuse out; wire them as Figure 10. **Hold point:** the wiring checks of section 3.3 pass before going on.

### Step 4: internal plate into the box

![Step 4](05-build-plan/step-04.png)

Four M4 screws into the bosses. Connect the antenna pigtail. Add a fresh desiccant pack.

### Step 5: box onto the enclosure back plate

![Step 5](05-build-plan/step-05.png)

Box back flat on the plate, centred, 80 above the plate's bottom edge. Four M5 screws through the lug tabs from behind the plate, nyloc nuts in front, snug.

### Step 6: optics holders onto the cell

![Step 6](05-build-plan/step-06.png)

Windows bedded and cured first. Each holder on two M3 screws, leads out of the top; splice the three leads to the 6-core cable.

### Step 7: cell onto the cell back plate

![Step 7](05-build-plan/step-07.png)

Back face flat on the plate, 213 above its bottom edge, centred. Two M5 screws from behind, snug: the threads are in plastic.

### Step 8: valve onto the cell plate

![Step 8](05-build-plan/step-08.png)

Coil up, inlet port on the right, centred, 63 above the plate's bottom edge. Two M4 screws from behind.

### Step 9: fittings and the valve-to-cell tube

![Step 9](05-build-plan/step-09.png)

Thread tape on the inlet fitting and the outlet hose tail, hand tight plus a quarter turn. Push-fit elbow on the valve outlet; tube straight up into the inlet fitting, pushed fully home.

### Step 10: gasket, lid and sensors

![Step 10](05-build-plan/step-10.png)

Studs into the body, gasket, lid, four thumb nuts finger tight. Chlorine sensor down until its tip is 40 below the top of the body; temperature probe 45 in; tighten both glands by hand.

### Step 11: pole and footing (survey visit)

![Step 11](05-build-plan/step-11.png)

On the survey visit, before installation day: dig a 300 mm hole 600 deep, 470 mm from the riser centre and square to the tapstand; set the pole plumb in fast-set concrete with 2.1 m standing above the ground.

### Step 12: saddle tee and fittings on the riser

![Step 12](05-build-plan/step-12.png)

**Hold point:** the supply to the tapstand is shut off and the riser drained. Saddle tee 500 above the ground; isolation valve, strainer, check valve and regulator on thread tape, with the check valve's arrow pointing away from the riser. Leave the isolation valve shut.

### Step 13: cell plate onto the pole

![Step 13](05-build-plan/step-13.png)

Seen from behind. The top of the cell lid 900 above the ground, facing the same way as the tapstand tap. A V-saddle between plate and pole at each U-bolt; U-bolts round the pole; M8 nyloc nuts in front, tightened evenly.

### Step 14: enclosure plate onto the pole

![Step 14](05-build-plan/step-14.png)

Seen from behind. Box centre 1,300 above the ground, square with the cell plate below. Same saddles and U-bolts.

### Step 15: panel mount and panel on the pole top

![Step 15](05-build-plan/step-15.png)

Sleeve over the pole top, two set screws. Panel on the tilt rail with the mount's bolts through its frame, facing the equator at 30°.

### Step 16: supply tube and drain hose

![Step 16](05-build-plan/step-16.png)

Push-fit tube from the regulator outlet to the valve inlet, clipped to the pole. Tee on the outlet hose tail with the vent pointing up and open; hose down to the basin, clamped, falling all the way.

### Step 17: cables into their glands; close the lid

![Step 17](05-build-plan/step-17.png)

Panel lead down the back of the pole, tied every 300 mm, under the plate and up into its gland; sensor and valve cables up the front of the cell plate into theirs. A drip loop below each gland; tighten the gland caps. Lid gasket clean, lid screws in a cross pattern. **Hold point:** safety stops S3 to S6 in section 6.

### Step 18: sun shield

![Step 18](05-build-plan/step-18.png)

Slide it over the box from the front until its flanges lie on the plate; four M5 thumb screws, finger tight.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of WWT-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Cell holds water | R2, R9 | Fill the closed cell to the outlet on the bench; 30 min on paper | No wet mark |
| Light tight | R2, R9 | Detectors read in a dark room with the light on and off, cell full | Same reading both ways |
| Turbidity response | R2 | Clean water, then a prepared, stabilized 20 NTU standard | The 90° reading rises clearly; the 180° reading falls |
| Chlorine response | R1 | Tap water and the same water after standing open a day, each checked with a DPD kit | The current follows the DPD difference |
| Temperature | R3 | Probe beside a reference thermometer in a water bath | Within 0.5 °C |
| Charge voltage and cut-offs | R7, R9 | Bench supply at 6 V in place of the panel, 1 A limit, temperature sensor replaced by resistors for -1 °C and 46 °C | 3.6 V charge, give or take 0.05 V; no charge current in either cut-off case |
| Valve | R4, R7 | Pulse open and closed from the controller | Opens and closes on one pulse each; no current between pulses |
| Flow per flush | R8 | Time the outflow at the hose end over 90 s at the site pressure | 0.75 L, give or take 10 % |
| Backflow | R11 | Close the isolation valve, open a drain cock upstream | Nothing flows back past the check valve |
| Air break | R1, R2 | Close the valve after a flush | The cell stays full to the outlet; the vent stays open and dry |
| Report and alert | R5, R6 | Force an upload and a test alert | Upload received; SMS received at the test number |
| Entries sealed | R9 | Look at each washer under a lamp; gland caps tight on their cables | Every washer evenly squeezed |
| Shield gap and fixing | R9 | Measure the gap; push the shield by hand | 25 mm, give or take 3, all round; nothing moves |
| Mounting | R11 | Pole plumb with a spirit level; push on the panel and the box | Plumb within 1°; no movement at a U-bolt |
| Installation time | R11 | Time installation day with two people | 2 h or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the battery comes into the workshop.** Voltage about 2.8 to 3.4 V; no swelling, dents or leaks; a datasheet from its maker. Fuse out. A charging spot ready on a non-combustible surface with a fire extinguisher for electrical fires within reach.
- **S2. Before the battery fuse goes in.** The wiring checks of section 3.3 pass. Battery polarity at the carrier board checked with a meter, not by wire colour.
- **S3. Before any charging source is connected.** The charge voltage is measured at 3.6 V with the battery out; the panel input polarity is checked at the board.
- **S4. Before the battery is allowed to charge.** Both cut-off checks of section 5 pass with the substitute resistors; the temperature sensor is back on the cells.
- **S5. First charge.** Attended the whole time, lid open, on the charging spot; battery temperature checked every 15 minutes. Stop if it passes 45 °C or 3.65 V.
- **S6. Before the modem transmits.** The antenna is connected. Transmitting without one can damage the modem.
- **S7. Before cutting into the riser.** The supply is shut off at the scheme valve and the riser drained, or a tool for tapping under pressure is used with the operator's permission. Local plumbing rules for a connection to drinking water are checked.
- **S8. Before the isolation valve is opened.** The check valve points away from the riser; every threaded joint is taped and tight; the air break vent is open; the drain hose falls to the basin all the way.
- **S9. Before the pole carries anything.** The concrete has set for at least the maker's time (overnight for a first build); the pole is plumb.
- **S10. Work at height.** Fit the panel from a stable ladder footed by a second person, never on a pole that carries power lines.

## 7. Tools, skills and workspace

**Tools.** Hacksaw or jigsaw with a metal blade; files; bench drill or a drill in a stand; drills 2.5 to 15 mm; step drill to 20 mm; taps M3, M4, M5, M12 x 1.5, M20 x 1.5 and M25 x 1.5, 1/8 BSPT and 3/8 BSP, with their tap drills; small milling machine (or a 3D printer with an enclosure and a 120 x 120 mm bed that prints ASA, for the cell body); scriber, square, steel rule and calipers; soldering iron, ferrule crimper and wire strippers; multimeter with a megohm range; bench power supply with a current limit (0 to 15 V, 0 to 2 A); spanners or sockets for M8 nuts and the glands; pipe wrench and thread tape; spade and post-hole digger; spirit level; stepladder; stopwatch and a measuring jug.

**Skills.** No certified trade is needed for the unit itself. Basic metalwork (marking out, cutting, drilling, tapping), milling or 3D printing, through-hole soldering and crimping, safe use of a bench power supply and care with lithium cells. Connecting to a drinking water supply may need the scheme operator's permission and a plumber's sign-off under local rules. All circuits are extra-low voltage: 3.6 V at the battery, 12 V at the valve pulse, under about 10 V from the panel; no mains wiring is part of this build.

**Workspace.** A bench about 1.2 x 0.6 m; a metalwork corner kept apart from the electronics so chips stay off the boards; a ventilated place for the printer, the epoxy and the silicone; the charging spot of S1.

**Personal protective equipment.** Safety glasses for cutting, drilling, soldering and concrete; gloves for sheet edges, epoxy and wet concrete; hearing protection when cutting; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 97 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/WWT-DWG-101` to `WWT-DWG-109`.
- General arrangement: `cad/drawings/WWT-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (WWT-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; flush and tube [D1] to [D5], enclosure temperature [C4], installation [J2], cost [K1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (WWT-DDR-003), with WWT-DDR-001 and WWT-DDR-002; design decisions register `docs/06-design-decisions.md` (WWT-DEC-001).
- Requirements: `docs/03-requirements.md` (WWT-REQ-001 v0.5).
