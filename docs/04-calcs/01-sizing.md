---
doc_id: WWT-CAL-001
title: WaterWatch sizing calculations
project: WaterWatch
doc_type: Calculation
version: '0.7'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (energy, solar, enclosure temperature, flushing and water use, chlorine error budget, turbidity settling, data, alert latency, wind, task times, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Design made constructable (WWT-DDR-003); tube run, chlorine error budget and cost re-run; budget treated as a value-engineering target
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Status light (WWT-DEC-001): energy line A2 and cost lines K1 and K2 re-run; autonomy 28.5 days, cost USD 322"
- version: "0.5"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: battery is one 32700 cell, 6 Ah (WWT-DEC-001 F1, STEM check S3); thermal mass and C3, C4 re-run; requirement numbers R1 to R13 now PR-001 to PR-013 (WWT-PRS-001)"
- version: "0.6"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Independent review of the STEM check (WWT-STM-001): converter loss (A6), low-pressure flush (D8, WWT-DEC-001 F5), valve-closing surge (D9), corrected chlorine budget (E9 to E11, R1 not met at 1.5 mg/L in 2 of 8 cases; O5 to Amish), full TLS handshake (G3, F7), event-to-SMS with retries (H4), wind on the sun shield (I1 to I3), saturated sand (I4); second check valve (F8): cost USD 325"
- version: '0.7'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish''s decisions of 2026-10-25: R1 target ±30 % above 1.0 mg/L (O5), budget rerun with the shared photometer [E12] (O2), R1 not met to met on paper, drift room 0.15 mg/L; R8 counts the hourly schedule only (O4)'
---

# WaterWatch sizing calculations

**Revision 0.7 (2026-10-25).** Amish's decisions of 2026-10-25 ("i concur with your recommendations"): R1 (PR-001) restated as ±30 % above 1.0 mg/L (WWT-DEC-001 O5); the shared DPD photometer is the monthly reference and the error budget is rerun with its accuracy [E12] (O2); R8 (PR-008) counts the hourly schedule only (O4). R1 moves from not met to met on paper; the room for drift that R10 rests on is now about 0.15 mg/L (was 0.13).

**Revision 0.6 (2026-10-25).** An independent reviewer (a separate session that saw only the STEM check, this note, the requirements and the script) recomputed the note and weakened several results; this revision answers it. (1) The 3.3 V rail needs a converter from the 2.5 to 3.65 V cell; at 85 % efficiency the daily need is 0.635 Wh, inside the 1.5 margin, and autonomy is 24.2 days [A6]. (2) Below the regulator's 0.7 bar compensating pressure a 90 s flush leaves 8.5 % stale water; sites below 0.7 bar now flush for 110 s, which leaves 4.5 % and uses 15.4 L/day (WWT-DEC-001 F5) [D8]. (3) Closing the valve at 4 bar raises a surge of about 2.0 bar in the 1/4 in tube, 6.0 bar in all, against about 10 bar for the tube [D9]. (4) With the stale-water bias added linearly rather than in quadrature, the chlorine budget meets R1 in 6 of 8 cases at 25 °C before drift; at 1.5 mg/L it misses at pH 7.5 by 0.004 mg/L and at pH 8.5 by 0.017 mg/L [E9], and a one-point calibration at 0.5 mg/L carries the reference error as 14 % at 1.5 mg/L, so 1 of 4 high-chlorine cases is met (2 of 4 with a photometer) [E10]. A target of ±30 % above 1.0 mg/L would meet all 8 [E11]; that changes a requirement and is proposed to Amish (WWT-DEC-001 O5). R1 is now **not met** at 1.5 mg/L. (5) A full TLS handshake every session would use 1.22 MB a month; the firmware keeps TLS sessions (F7), 0.36 MB [G3]. (6) With all three SMS tries the worst case from the event itself is 92 min, not 77 [H4]; R5's 15 min from confirmation stands. (7) The wind sees the sun shield, not the bare enclosure: 75 N on it, 206 N in all, 59 MPa in the pole (a factor of 4.0) and a footing factor of 4.3 in dry sand [I1 to I3], 2.2 in saturated sand [I4]. (8) A second check valve at the cell inlet (F8) adds USD 3: USD 325 per base unit, USD 25 over the target [K1].

**Revision 0.5 (2026-10-25).** The STEM check (WWT-STM-001 S3) found that the battery as specified, "1S2P 32700 cells, 3.2 V, 6 Ah", did not match its cells: one 32700 LiFePO4 cell holds about 6 Ah, so two in parallel would hold 12 Ah, while this note used 6 Ah for energy and two cells' mass (0.29 kg) for heat. Under Amish's standing instruction of 2026-10-23 the battery is now one 32700 cell, 6 Ah, 0.135 kg (WWT-DEC-001 F1). Every energy figure stands; the thermal mass falls from 1,460 to 1,305 J/K and the time constant from 15 to 13 min [C3]; the hottest points inside the enclosure are unchanged to 0.1 °C, and the charging hours without the shield on a 45 °C day fall from 0.4 and 0.2 h to 0.3 and 0.1 h [C4]. No requirement changes status. The requirements are now numbered PR-001 to PR-013 in WWT-PRS-001, which replaces WWT-REQ-001; this note keeps the old R numbers, listed in the "Was" column there.

**Revision 0.4 (2026-10-02).** Amish decided on 2026-10-02 that the status light is one low-duty LED behind a lens in the shield front (WWT-DEC-001). It adds 1.98 mWh a day to the energy sum (5 mA for 50 ms every 10 s from the 3.3 V rail, 0.55 % of the sum) [A2], which moves the daily need from 0.537 to 0.540 Wh, autonomy from 28.6 to 28.5 days and the refill from 1.18 to 1.19 clear days [A3, B1, B3]. A seventh gland and the status light unit add USD 3 to the parts: USD 322 against the USD 300 value-engineering target, USD 22 over [K1]. No requirement changes status. The paragraph below describes revision 0.3.

On paper, WaterWatch meets eight of its thirteen requirements (five by calculation, three by design) and has four at risk; none is missed outright, and the parts cost of the constructable design is USD 19 over the USD 300 value-engineering target (R12) at version 0.3. Version 0.3 re-runs the note for the constructable design of WWT-DDR-003: the sample tube is shorter (696 mm), which moves two chlorine error figures by 0.001 mg/L, and the added mounting plates, fixings, glands and lid fittings raise the parts cost from USD 283 to USD 319. Version 0.2 applies Amish's decisions of 2026-09-25 (WWT-DDR-002): R1 is relaxed to ±0.2 mg/L or ±25 %, whichever is greater; the pH probe variant is fitted at sites whose pH is above 7.5 or moves more than 0.2 between visits; a confirming reading follows 15 min after a first threshold crossing; and the pole footing is cast on the survey visit. With these, the chlorine error budget meets the relaxed R1 target in all eight cases at 25 °C before sensor drift, leaving at least 0.13 mg/L for drift, and installation day drops to 65 min. R1 and R10 remain at risk because the low-cost sensor's drift over a month is still unknown, and at 40 °C one case (1.5 mg/L at pH 7.5 with site pH) misses by 0.006 mg/L. The other two at risk are turbidity (R2, fouling) and outdoor survival (R9, battery temperature). Version 0.1 had R1 and R10 not met and R11 at risk. The calculations changed four parts of the TRL 2 concept: the flow cell is half its former volume so that the flush clears it, a pressure-compensating regulator replaces the fixed restrictor, the settling wait before the turbidity reading rises from 10 s to 30 s, and a ventilated sun shield is added so that the battery can charge on hot days. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that water is safe to drink, and they are not a substitute for laboratory checks of the sensors, backflow tests on the sample line or electrical safety checks on the battery. See WWT-PRC-001, Safety.

## Scope and method

The note checks every requirement in WWT-REQ-001 v0.5 against the design in WWT-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, so the cell volume, tube run, enclosure size, pole and footing used here are the ones in the STEP files and in drawing WWT-DWG-001. The script also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a public tapstand on a chlorinated rural scheme, with a supply pressure of 0.5 to 4 bar (7 to 58 psi), ambient 0 to 45 °C, hourly readings and uploads every 4 h over LTE-M or NB-IoT.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Electronics | 80 mA average at 3.3 V while awake; 50 µA sleep floor including potentiostat bias, charger and protection board; 20 mWh per upload including network attach; latching valve 2 pulses of 50 ms at 12 V, 0.5 A through an 80 % boost | Typical ESP32-S3 and SIM7000-class figures; to confirm from datasheets and measurement |
| Reading cycle | 90 s flush with chlorine averaged over the last 10 s; 30 s settling; 5 s turbidity; 5 s for temperature and logging: 130 s awake | Section F sets the 30 s |
| Margin | 1.5 on daily energy for alerts, retries and cold weather | As at TRL 2 |
| Battery | One 32700 LiFePO4 cell (1S1P), 3.2 V, 6 Ah, 0.135 kg; 80 % usable; 85 % of capacity at 0 °C | Cell datasheet (WWT-STM-001 S3); typical cell data |
| Solar | 5 W panel; 4.5 peak sun hours on a clear day, 2.5 on an overcast day; 0.6 derating for heat, dust, angle and a small charger | Screening values |
| Enclosure heat | Combined convection and radiation 10 W/m²K; direct sun 900 W/m², diffuse 100 W/m²; absorptance 0.45 (light grey) or 0.70 (dusty); back face against the mounting plate; sun square to the front face | Handbook ranges; worst azimuth |
| Sun shield | Ventilated white hood with a 25 mm gap lets a quarter of the solar gain reach the enclosure | Assumed; to be measured |
| Flow | 0.5 L/min pressure-compensating regulator, +10 % tolerance, compensating above about 0.7 bar; well-mixed cell (worst case for flushing) | Typical drip-irrigation flow regulators |
| Chlorine | HOCl pKa from Morris (1966); sensor responds to HOCl; calibrated at the site against a DPD comparator read to ±0.07 mg/L; residual temperature error 2.5 %/K times ±0.5 K; site pH may move ±0.2 between visits; a pH probe variant reads to ±0.1 and is fitted where site pH is above 7.5 or moves more than 0.2 (WWT-DDR-002) | pH drift and sensor coefficients are assumptions, to confirm with partner data and tests |
| Wind | 35 m/s gust; drag coefficients 1.2 (panel, pole) and 1.3 (enclosure); medium sand, 18 kN/m³, Kp = 3 | Screening values, not a code check |

## A. Daily energy (R7, R4)

- **Per reading.** 130 s awake at 0.264 W is 9.53 mWh, or 0.229 Wh per day at 24 readings [A1].
- **Uploads, sleep and valve.** Six uploads take 0.120 Wh, the sleep floor 4.0 mWh and the valve pulses 5.0 mWh per day [A2].
- **Daily need.** The sum is 0.360 Wh, including 2 mWh for the status light; with the 1.5 margin it is 0.540 Wh per day, a 22.5 mW average [A2, A3]. The TRL 2 figure of about 0.5 Wh stands; the longer settling wait adds about 35 mWh per day [F3].
- **Converter.** The 3.3 V rail comes from a 2.5 to 3.65 V cell through a converter; at 85 % efficiency the need is 0.635 Wh per day, which the 1.5 margin covers with 1.27 to spare on everything else [A6].
- **Sensitivity.** A site with only 2G coverage, where each upload costs four times as much, needs 1.080 Wh per day [A4]. The 15 min schedule allowed by R4 needs 1.592 Wh per day [A5].

## B. Battery autonomy and solar recharge (R7)

- **Autonomy.** The 19.2 Wh pack gives 15.36 Wh usable, which lasts 28.5 days without sun, or 24.2 days at 0 °C. On a 2G-only site it lasts 14.2 days and on the 15 min schedule 9.6 days [B1]. R7 (7 days) is met in every case.
- **Recharge.** The 5 W panel yields 13.5 Wh on a clear day and 7.5 Wh on an overcast day [B2]. From empty it refills in 1.19 clear days or 2.21 overcast days [B3]. R7 (3 clear days) is met.
- **Panel size.** The smallest panel that would refill the pack in three overcast days is 3.8 W, so the 5 W panel carries a modest margin for the rainy season. At full sun it charges at about 1.25 A (0.21 C), well within the cells' rating [B4].
- **Hot weather.** Charging depends on the battery staying below its 45 °C charge limit (section C). Without the sun shield, a clear 45 °C day allows no useful charge at all.

## C. Enclosure temperature (R9)

- **Loss coefficient.** The 200 x 120 x 260 mm enclosure has 0.2144 m² of surface, 0.1624 m² exposed, and loses 1.62 W/K to the air [C1].
- **Steady rise.** With the sun 60° high and square to the front face, a clean light grey enclosure absorbs 22.6 W and runs 13.9 K above ambient; a dusty one absorbs 35.2 W and runs 21.6 K above. The panel's shadow on the top reduces these to 8.7 K and 13.6 K [C2].
- **Time constant.** About 1,305 J/K of enclosure, cell and boards gives a 13 min time constant, so the inside follows the sun within the hour [C3].

*Table 2. Hottest point inside the enclosure and charging on a clear day [C4].*

| Day | Case | Peak inside | Sun hours with charging allowed | Energy available |
| --- | --- | --- | --- | --- |
| 30 to 45 °C | Clean, no shield | 60.7 °C | 0.3 h | 0.0 Wh |
| 30 to 45 °C | Dusty, no shield | 69.8 °C | 0.1 h | 0.0 Wh |
| 30 to 45 °C | Clean, with shield | 48.6 °C | 6.3 h | 7.3 Wh |
| 30 to 45 °C | Dusty, with shield | 50.8 °C | 5.4 h | 5.8 Wh |
| 22 to 35 °C | Clean, no shield | 50.8 °C | 8.0 h | 10.1 Wh |
| 22 to 35 °C | Dusty, no shield | 59.9 °C | 0.4 h | 0.0 Wh |
| 22 to 35 °C | Dusty, with shield | 40.9 °C | 12.0 h | 13.5 Wh |

- **The TRL 2 enclosure would not charge in hot weather.** The battery's charge cut-off at 45 °C (R9) blocks charging for nearly all of a clear hot day, and even on a 35 °C day once the box is dusty. A run of such days would drain the pack within its 29 days.
- **Sun shield.** A ventilated white aluminum hood over the top, sides and front (BOM item 17, $8) keeps the inside to about 51 °C on a 45 °C day and leaves 5.8 Wh for charging, 10.7 times the daily need. It lifts off for the monthly visit.
- **R9 is at risk.** The shield factor is assumed, the battery still sits above 45 °C for part of a hot day (which ages LiFePO4 cells faster), and the electronics' ratings are met with margin (ESP32-S3 and SIM7000-class modules are rated to 85 °C). Enclosure sealing (IP66), UV-stable materials and the opaque cell are met by the choice of parts.

## D. Sample flow, flushing and water use (R8, R1)

- **Cell volume.** The TRL 2 cell held 0.37 L. The TRL 3 cell holds 0.185 L of water once the baffle and the immersed sensors are subtracted. The 1/4 in sample tube, from the regulator to the valve and from the valve to the cell, runs 696 mm and holds 10.1 mL [D1] (738 mm and 10.7 mL before WWT-DDR-003 moved the valve onto the cell plate).
- **Water use.** Each 90 s flush at 0.5 L/min uses 0.75 L, 18.0 L per day [D2]. At the start of the 10 s chlorine window, 2.9 % of the previous hour's water is still in the cell, and 1.8 % at its end; the TRL 2 cell would have held 17.0 %, enough to bias every chlorine reading low by that much when the old water had lost its residual [D3]. This is why the cell was made smaller rather than the flush longer.
- **Pressure.** A fixed orifice sized for 0.5 L/min at 1 bar passes 0.35 L/min at 0.5 bar and 1.00 L/min at 4 bar, which would use 36.0 L per day [D4] and break R8. A pressure-compensating regulator holds 0.5 L/min; at its +10 % tolerance the unit uses 19.8 L per day [D5]. **R8 is met on paper** with a 1 % margin at the upper tolerance. Below the regulator's compensating range, at 0.5 bar, the flow falls to about 0.35 L/min and the stale fraction rises to 8.5 % [D5]; a low-pressure site needs a longer flush, set per site.
- **Context.** The daily flush is 0.36 % of the draw of a tapstand serving 250 people at 20 L each. On the 15 min schedule the unit would use 72 L per day [D6]; R8 applies to hourly sampling.
- **Valve.** At 0.5 bar the valve must be direct acting, with no minimum pressure difference; pilot-operated valves need about 0.2 to 0.5 bar [D7]. BOM item 13 now says so.
- **Low-pressure sites.** Below 0.7 bar the flush is set to 110 s at commissioning (WWT-DEC-001 F5): at 0.5 bar and about 0.35 L/min it leaves 4.5 % stale water and uses 15.4 L per day, for 35 mWh per day of extra awake time [D8].
- **Valve closing.** The flow in the 1/4 in tube is 0.57 m/s; closing the valve raises a Joukowsky surge of about 2.0 bar, 6.0 bar in all at a 4 bar supply, against about 10 bar for the tube (typical rating, to confirm) [D9]. The valve is specified to open against at least 4 bar (F6).

## E. Free chlorine error budget (R1)

The HOCl pKa is 7.75 at 5 °C, 7.54 at 25 °C and 7.43 at 40 °C [E1]. At 25 °C the share of free chlorine present as HOCl is 0.92 at pH 6.5, 0.77 at pH 7.0, 0.52 at pH 7.5, 0.26 at pH 8.0 and 0.10 at pH 8.5; across the pH and temperature range of R1 it spans 0.15 to 0.90 [E2]. The TRL 2 precis quoted about a quarter at pH 8 and three quarters at pH 7; both stand.

Calibration against a DPD comparator at the site absorbs the pH at the time of calibration into the sensor's slope. What remains is the change in pH between visits, the comparator's own reading error (±0.07 mg/L), a 1.25 % residual temperature error and the 2.9 % stale-water bias [E3].

Under WWT-DDR-002, R1's target is ±0.2 mg/L or ±25 %, whichever is greater (it was ±0.1 mg/L below 1.0 mg/L and ±15 % above), and a site uses the pH probe variant when its pH is above 7.5 or moves more than 0.2 between visits. Table 3 gives both methods and marks the one the rule applies.

*Table 3. Error in free chlorine at 25 °C and zero sensor drift, against the R1 target [E4] (±0.2 mg/L or ±25 % up to 1.0 mg/L, ±30 % above since Amish's decision of 2026-10-25, WWT-DEC-001 O5).*

| Free chlorine | pH | Site pH (±0.2 between visits) | pH probe variant (±0.1) | Method under the rule | Target (v0.3 target) | Room for drift |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5 mg/L | 7.0 | ±0.092 mg/L | ±0.077 mg/L | Site pH | ±0.200 (±0.100) mg/L | 0.177 mg/L |
| 0.5 mg/L | 7.5 | ±0.131 mg/L | ±0.090 mg/L | Site pH | ±0.200 (±0.100) mg/L | 0.151 mg/L |
| 0.5 mg/L | 8.0 | ±0.202 mg/L | ±0.115 mg/L | pH probe | ±0.200 (±0.100) mg/L | 0.163 mg/L |
| 0.5 mg/L | 8.5 | ±0.260 mg/L | ±0.135 mg/L | pH probe | ±0.200 (±0.100) mg/L | 0.148 mg/L |
| 1.5 mg/L | 7.0 | ±0.194 mg/L | ±0.118 mg/L | Site pH | ±0.450 (±0.225) mg/L | 0.406 mg/L |
| 1.5 mg/L | 7.5 | ±0.339 mg/L | ±0.186 mg/L | Site pH | ±0.450 (±0.225) mg/L | 0.296 mg/L |
| 1.5 mg/L | 8.0 | ±0.574 mg/L | ±0.284 mg/L | pH probe | ±0.450 (±0.225) mg/L | 0.349 mg/L |
| 1.5 mg/L | 8.5 | ±0.753 mg/L | ±0.352 mg/L | pH probe | ±0.450 (±0.225) mg/L | 0.281 mg/L |

- **Before DDR-002.** Against the v0.3 target with site pH everywhere, only 2 of the 8 cases were met, both at pH 7.0 [E5]. The DPD comparator alone took ±0.07 of the ±0.10 mg/L budget, so the target was as tight as the field reference.
- **With DDR-002.** The relaxed target is met in all 8 cases at zero drift when the pH probe rule applies [E6]. Site pH alone would just miss at pH 8.0 (±0.202 against ±0.200 mg/L at 0.5 mg/L), which is why the trigger sits at pH 7.5.
- **Warm water.** At 40 °C the HOCl pKa falls to 7.43 and the pH term grows. With the rule, 10 of 10 cases from pH 6.5 to 8.5 meet the restated target; the closest is 1.5 mg/L at pH 7.5 with site pH, at ±0.381 against ±0.450 mg/L (it missed the ±0.375 mg/L of the earlier target) [E7].
- **Room for drift.** At 25 °C the smallest margin left for sensor drift under the rule is 0.148 mg/L with the comparator (0.130 mg/L before the target was restated), against 0.038 mg/L (and only at pH 7.0) under the v0.3 target [E8]. No verified long-term drift data are available (see `docs/REVIEW.md`), so **R1 is at risk**, not met.

**Corrected budget (independent review, revision 0.6).** The reviewer pointed out that the stale-water bias always reads low, so it adds linearly, not in quadrature, and that a one-point slope calibration carries the reference's ±0.07 mg/L as a relative error at other readings. The firmware corrects the HOCl fraction for the measured temperature through pKa(T), so a temperature change between visits adds only the residual of [E3]. With the bias added linearly and the calibration at the reading's level, 6 of 8 cases meet R1 before drift; at 1.5 mg/L the pH 7.5 case misses by 0.004 mg/L and the pH 8.5 case (pH probe) by 0.017 mg/L [E9]. Calibrated at 0.5 mg/L and read at 1.5 mg/L, only 1 of 4 cases is met with the comparator and 2 of 4 with a handheld photometer [E10]. Against the target as it then stood, R1 was not met at 1.5 mg/L. Amish decided on 2026-10-25 ("i concur with your recommendations") to restate the target as ±30 % above 1.0 mg/L (WWT-DEC-001 O5), which the comparator budget meets in all 8 cases [E11], and to make a shared handheld DPD photometer per operator (±0.03 mg/L ±3 %, the Hanna HI97711 class, WWT-MKT-001) the monthly reference (O2). Rerun with the photometer, calibrated at the reading level or at 0.5 mg/L, whichever is worse, all 8 cases are met; the worst is 1.5 mg/L at pH 8.5, ±0.411 against ±0.450 mg/L, and at least 0.146 mg/L is left for drift [E12]. **R1 is met on paper.** It is met with room at 0.2 to 0.5 mg/L, where the alerts are set (about ±0.08 mg/L at 0.2 mg/L). The photometer is shared per operator and is outside the unit cost (WWT-PLN-001). The reviewer also noted that a membrane-free sensor's current depends on flow; the regulator holds the flow above 0.7 bar, and the flow dependence goes to the TRL 4 tests (WWT-STM-001 S32).

## F. Turbidity reading: bubbles and settling (R2)

- **Bubbles.** Air released when the flow stops scatters light like particles. At 5 °C a 100 µm bubble rises at 3.6 mm/s and takes 18 s to clear the 66 mm cavity; a 50 µm bubble takes 74 s. At 25 °C the same bubbles take 11 s and 43 s [F1]. The TRL 2 wait of 10 s was too short in cold water.
- **Settling.** Silt of 10 µm settles at 0.10 mm/s: 3.5 mm during the 35 s of waiting and reading, and the clear layer at the top takes 5.4 min to reach the beam at mid-height [F2]. Settling does not bias the reading.
- **Change.** The wait is now 30 s, which clears 100 µm bubbles at 5 °C, for 35 mWh per day [F3]. Smaller bubbles remain possible when the supply is supersaturated with air.
- **R2 is at risk.** Range and resolution follow the published open-source design (Kelley et al., 2014), but fouling of the optical windows between monthly cleans cannot be estimated on paper.

## G. Data and storage (R6)

- **Airtime.** Each upload carries about 780 B of readings and status plus about 4,000 B of TLS, HTTP and network overhead, 0.86 MB per month; with TLS session resumption it falls to about 0.36 MB [G1]. A full TLS handshake every session (about 6 kB) would use 1.22 MB, over R6's 1 MB, so the firmware keeps TLS sessions (WWT-DEC-001 F7) [G3]. R6's airtime assumption of under 1 MB per month then holds.
- **Storage.** 90 days of readings take 138 kB as CSV on the microSD card; a 7-day ring buffer in flash takes 5.4 kB [G2]. R6 is met on paper.

## H. Alert latency (R5)

- **From confirmation to SMS.** A modem wake, network attach and SMS take about 140 s at the first try; with three tries at 3 min spacing the worst case is 13.0 min [H1]. R5 (15 min) is met on paper where there is coverage. The TRL 2 plan did not fix the retry spacing; at 5 min spacing the worst case would be 17 min, so 3 min is now specified.
- **From the event.** Under WWT-DDR-002 the firmware takes a confirming reading 15 min after a first threshold crossing instead of waiting for the next hourly reading. The worst case from the start of an event to the SMS falls from 122 min to 77 min with a first-try SMS [H2], and is 92 min when all three tries are needed [H4]. The firmware bounds each try at 140 s. Each confirming reading costs 9.7 mWh and 0.75 L; even ten a month add only 3.2 mWh per day, 0.6 % of the daily need [H3], so sections A, B and D stand.

## I. Pole and footing in wind (structure, R11)

- **Loads.** A 35 m/s gust (735 Pa) puts 42 N on the panel at 2.16 m, 75 N on the sun shield over the enclosure (254 x 307 mm, revision 0.6) at 1.30 m and 89 N on the pole at 1.05 m: 206 N in all and a base moment of 281 N·m [I1].
- **Pole.** The 48.3 x 3.2 mm tube has a section modulus of 4.80 cm³ and sees 59 MPa, a factor of 4.0 on the 235 MPa yield [I2].
- **Footing.** A 300 mm footing 600 mm deep in medium sand resists 890 N sideways, a factor of 4.3 [I3]. In saturated sand (submerged unit weight 9 kN/m³) it resists 445 N, a factor of 2.2 [I4]. Clay and made ground need a check at the survey visit.

## J. Installation and the monthly visit (R11, R10)

- **Installation.** The tasks take 160 person-minutes. Done in one visit, the critical path is digging, setting the pole, waiting 30 min for fast-set concrete, then mounting, cabling and commissioning: 140 min against the 120 min of R11 [J1]. Under WWT-DDR-002 the footing is dug and cast, with the pole set in it, on the survey visit (75 min including the set). The critical path on installation day is then 65 min, with the 50 min of plumbing done in parallel [J2]. **R11 is met on paper** as restated in WWT-REQ-001 v0.4; the design parts of R11 (one tee, an isolation valve, a check valve, food-safe wetted parts and hand tools only) are met by design, and the open air break at the outlet keeps the drain from ever connecting back to the cell.
- **Monthly visit.** Cleaning the cell and electrode, a DPD test, a pH check, calibration from a phone and a look at the strainer, drain and panel take 30 min, exactly the R10 limit [J3]. **R10 is at risk:** a monthly visit is enough if the chlorine sensor drifts less than about 0.15 mg/L in a month under the restated R1 target with the photometer (section E, [E12]; 0.13 mg/L before the decisions of 2026-10-25; it was about 0.04 mg/L under the v0.3 target), and no verified data yet show the drift. At a pH probe variant site the pH comparator step becomes a check of the probe in a buffer, of similar length.

## K. Cost (R12)

Value-engineering target: USD 300 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 325.00 for the base unit, 21 BOM lines (USD 25.00 over the target, 8 %) [K1]. Revision 0.6 added $3 for a second check valve at the cell inlet (WWT-DEC-001 F8). The TRL 3 changes added $3 for the pressure-compensating regulator, $1 for the air-break fitting and $8 for the sun shield; WWT-DDR-002 added $1 for a spare pH port and blanking plug in the cell lid; WWT-DDR-003 added $36 for construction: the two drilled back plates ($10), the enclosure lugs and printed internal plate ($8), fixings ($6), three more glands and a blanking plug ($4), the cell's gasket, studs and lid glands ($4), push-fit elbows ($2), the shield fixing ($1) and the drain hose tail ($1); WWT-DEC-001 (2026-10-02) then added $3 for the status light: the lens unit and lead ($2) and a seventh gland ($1). R12 is reported as over the value-engineering target; the savings worth trying are listed in the design decisions register (WWT-DEC-001). A pH probe variant site costs about $385 to $425 per unit (probe and interface about $60 to $100, estimate) [K2]; as restated in WWT-REQ-001 v0.4, the probe is priced per variant site, outside the base-unit budget, like the shared calibration kit.

## L. Results against every requirement

*Table 4. Requirement status from this note [L].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Measure free chlorine | With the shared photometer as the monthly reference: 8 of 8 cases met at 25 °C and zero drift, worst ±0.411 against ±0.450 mg/L at 1.5 mg/L, pH 8.5; at least 0.15 mg/L left for drift [E11, E12] | ±0.2 mg/L or ±25 %, whichever is greater, up to 1.0 mg/L; ±30 % above (WWT-DEC-001 O5, 2026-10-25); pH 6.5 to 8.5 | Met on paper; drift unknown |
| R10 | Maintainable by a caretaker | Visit 30 min; needs drift below about 0.15 mg/L per month with the photometer (O2), unverified | Monthly or less, 30 min or less | **At risk** |
| R2 | Measure turbidity | 30 s wait clears 100 µm bubbles at 5 °C; fouling unknown | 0 to 100 NTU, ±0.5 NTU or ±10 % | **At risk** |
| R9 | Survive outdoors | 50.8 °C peak inside on a 45 °C day with the shield (69.8 °C without) | IP65; 0 to 45 °C ambient; charging blocked above 45 °C | **At risk** (shield factor assumed) |
| R11 | Install simply and safely | 65 min on installation day with the footing cast on the survey visit (140 min in one visit) | 2 h on installation day, hand tools, backflow prevented | Met on paper |
| R5 | Alert the people who act | 13.0 min worst case from confirmation to SMS; 77 min from the event with the 15 min confirming reading and a first-try SMS, 92 min with all three tries | 15 min | Met on paper (where there is coverage) |
| R6 | Report and keep data | 0.36 MB per month with TLS session resumption (1.22 MB without); 90 days in 138 kB | 4 h uploads, 90 days on board | Met on paper |
| R7 | Run on sunlight alone | 28.5 days autonomy; 1.19 clear days to refill | 7 days; 3 clear days | Met on paper |
| R8 | Use little treated water | 18.0 L/day nominal, 19.8 L at regulator tolerance; 15.4 L/day at a 0.5 bar site with the 110 s flush; confirming readings add about 0.25 L/day and are not counted (WWT-DEC-001 O4, decided by Amish 2026-10-25) | 20 L/day | Met on paper (thin margin) |
| R12 | Stay within the budget | $325 per base unit; $385 to $425 at a pH probe variant site | $300 value-engineering target per base unit | Over the target by $25 |
| R3 | Measure water temperature | DS18B20, ±0.5 °C from -10 to 85 °C | 0 to 50 °C, ±0.5 °C | Met by design |
| R4 | Sample on a schedule | Hourly default; 15 min schedule within energy (1.592 Wh/day, 9.6 days) | 15 min to 24 h | Met by design |
| R13 | Report measurements, not verdicts | Alert wording rule | Never says "safe" | Met by design |

Counts: 3 at risk, 6 met on paper, 1 over the value-engineering target, 3 met by design (v0.6: 1 not met, R1 at 1.5 mg/L, 3 at risk, 5 met on paper, 1 over, 3 by design; v0.5: 4 at risk, 5 met on paper, 1 over, 3 by design; v0.2: 4 at risk, 6 met on paper, 3 met by design; v0.1: 2 not met, 3 at risk, 5 met on paper, 3 met by design). No requirement is left unverifiable at TRL 3, although R1, R2, R9 and R10 each rest on an assumption that only a test can settle.

## Checks against the TRL 2 figures

| TRL 2 claim (WWT-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| About 0.5 Wh/day | 0.540 Wh/day (130 s awake; 0.537 before the status light) | Precis updated |
| About 30 days without sun | 28.5 days (24.2 days at 0 °C; 28.6 before the status light) | Precis updated |
| About 13 Wh per clear day; about 1.2 days to refill | 13.5 Wh; 1.19 days | Stands |
| Cell 0.37 L; 0.75 L flush is about two cell volumes | 0.185 L; 0.75 L is about four cell volumes | Cell halved, precis updated |
| About 18 L/day, R8 met | 18.0 L nominal, but 36 L at 4 bar with a fixed restrictor | Regulator added, precis updated |
| 10 s wait for bubbles | Too short at 5 °C; 30 s | Precis updated |
| Enclosure temperature not estimated | 61 to 70 °C peak without a shield on a 45 °C day | Shield added, precis updated |
| Under 1 MB per month | 0.86 MB | Stands |
| SMS within minutes | 13.0 min worst case with 3 min retries | Precis updated |
| HOCl about a quarter at pH 8, three quarters at pH 7 | 0.26 and 0.77 | Stands |
| About $270 | $325 for the constructable design (v0.5: $322; v0.3: $319; v0.2: $283; v0.1: $282) | Precis and BOM notes updated |
