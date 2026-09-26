---
doc_id: WWT-CAL-001
title: WaterWatch sizing calculations
project: WaterWatch
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# WaterWatch sizing calculations

On paper, WaterWatch meets nine of its thirteen requirements (six by calculation, three by design) and has four at risk; none is missed outright. Version 0.2 applies Amish's decisions of 2026-09-25 (WWT-DDR-002): R1 is relaxed to ±0.2 mg/L or ±25 %, whichever is greater; the pH probe variant is fitted at sites whose pH is above 7.5 or moves more than 0.2 between visits; a confirming reading follows 15 min after a first threshold crossing; and the pole footing is cast on the survey visit. With these, the chlorine error budget meets the relaxed R1 target in all eight cases at 25 °C before sensor drift, leaving at least 0.13 mg/L for drift, and installation day drops to 65 min. R1 and R10 remain at risk because the low-cost sensor's drift over a month is still unknown, and at 40 °C one case (1.5 mg/L at pH 7.5 with site pH) misses by 0.006 mg/L. The other two at risk are turbidity (R2, fouling) and outdoor survival (R9, battery temperature). Version 0.1 had R1 and R10 not met and R11 at risk. The calculations changed four parts of the TRL 2 concept: the flow cell is half its former volume so that the flush clears it, a pressure-compensating regulator replaces the fixed restrictor, the settling wait before the turbidity reading rises from 10 s to 30 s, and a ventilated sun shield is added so that the battery can charge on hot days. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that water is safe to drink, and they are not a substitute for laboratory checks of the sensors, backflow tests on the sample line or electrical safety checks on the battery. See WWT-PRC-001, Safety.

## Scope and method

The note checks every requirement in WWT-REQ-001 v0.4 against the design in WWT-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, so the cell volume, tube run, enclosure size, pole and footing used here are the ones in the STEP files and in drawing WWT-DWG-001. The script also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a public tapstand on a chlorinated rural scheme, with a supply pressure of 0.5 to 4 bar (7 to 58 psi), ambient 0 to 45 °C, hourly readings and uploads every 4 h over LTE-M or NB-IoT.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Electronics | 80 mA average at 3.3 V while awake; 50 µA sleep floor including potentiostat bias, charger and protection board; 20 mWh per upload including network attach; latching valve 2 pulses of 50 ms at 12 V, 0.5 A through an 80 % boost | Typical ESP32-S3 and SIM7000-class figures; to confirm from datasheets and measurement |
| Reading cycle | 90 s flush with chlorine averaged over the last 10 s; 30 s settling; 5 s turbidity; 5 s for temperature and logging: 130 s awake | Section F sets the 30 s |
| Margin | 1.5 on daily energy for alerts, retries and cold weather | As at TRL 2 |
| Battery | LiFePO4 1S2P, 3.2 V, 6 Ah; 80 % usable; 85 % of capacity at 0 °C | Typical cell data |
| Solar | 5 W panel; 4.5 peak sun hours on a clear day, 2.5 on an overcast day; 0.6 derating for heat, dust, angle and a small charger | Screening values |
| Enclosure heat | Combined convection and radiation 10 W/m²K; direct sun 900 W/m², diffuse 100 W/m²; absorptance 0.45 (light grey) or 0.70 (dusty); back face against the mounting plate; sun square to the front face | Handbook ranges; worst azimuth |
| Sun shield | Ventilated white hood with a 25 mm gap lets a quarter of the solar gain reach the enclosure | Assumed; to be measured |
| Flow | 0.5 L/min pressure-compensating regulator, +10 % tolerance, compensating above about 0.7 bar; well-mixed cell (worst case for flushing) | Typical drip-irrigation flow regulators |
| Chlorine | HOCl pKa from Morris (1966); sensor responds to HOCl; calibrated at the site against a DPD comparator read to ±0.07 mg/L; residual temperature error 2.5 %/K times ±0.5 K; site pH may move ±0.2 between visits; a pH probe variant reads to ±0.1 and is fitted where site pH is above 7.5 or moves more than 0.2 (WWT-DDR-002) | pH drift and sensor coefficients are assumptions, to confirm with partner data and tests |
| Wind | 35 m/s gust; drag coefficients 1.2 (panel, pole) and 1.3 (enclosure); medium sand, 18 kN/m³, Kp = 3 | Screening values, not a code check |

## A. Daily energy (R7, R4)

- **Per reading.** 130 s awake at 0.264 W is 9.53 mWh, or 0.229 Wh per day at 24 readings [A1].
- **Uploads, sleep and valve.** Six uploads take 0.120 Wh, the sleep floor 4.0 mWh and the valve pulses 5.0 mWh per day [A2].
- **Daily need.** The sum is 0.358 Wh; with the 1.5 margin it is 0.537 Wh per day, a 22.4 mW average [A3]. The TRL 2 figure of about 0.5 Wh stands; the longer settling wait adds about 35 mWh per day [F3].
- **Sensitivity.** A site with only 2G coverage, where each upload costs four times as much, needs 1.077 Wh per day [A4]. The 15 min schedule allowed by R4 needs 1.589 Wh per day [A5].

## B. Battery autonomy and solar recharge (R7)

- **Autonomy.** The 19.2 Wh pack gives 15.36 Wh usable, which lasts 28.6 days without sun, or 24.3 days at 0 °C. On a 2G-only site it lasts 14.3 days and on the 15 min schedule 9.7 days [B1]. R7 (7 days) is met in every case.
- **Recharge.** The 5 W panel yields 13.5 Wh on a clear day and 7.5 Wh on an overcast day [B2]. From empty it refills in 1.18 clear days or 2.21 overcast days [B3]. R7 (3 clear days) is met.
- **Panel size.** The smallest panel that would refill the pack in three overcast days is 3.8 W, so the 5 W panel carries a modest margin for the rainy season. At full sun it charges at about 1.25 A (0.21 C), well within the cells' rating [B4].
- **Hot weather.** Charging depends on the battery staying below its 45 °C charge limit (section C). Without the sun shield, a clear 45 °C day allows no useful charge at all.

## C. Enclosure temperature (R9)

- **Loss coefficient.** The 200 x 120 x 260 mm enclosure has 0.2144 m² of surface, 0.1624 m² exposed, and loses 1.62 W/K to the air [C1].
- **Steady rise.** With the sun 60° high and square to the front face, a clean light grey enclosure absorbs 22.6 W and runs 13.9 K above ambient; a dusty one absorbs 35.2 W and runs 21.6 K above. The panel's shadow on the top reduces these to 8.7 K and 13.6 K [C2].
- **Time constant.** About 1,460 J/K of enclosure, cells and boards gives a 15 min time constant, so the inside follows the sun within the hour [C3].

*Table 2. Hottest point inside the enclosure and charging on a clear day [C4].*

| Day | Case | Peak inside | Sun hours with charging allowed | Energy available |
| --- | --- | --- | --- | --- |
| 30 to 45 °C | Clean, no shield | 60.7 °C | 0.4 h | 0.0 Wh |
| 30 to 45 °C | Dusty, no shield | 69.8 °C | 0.2 h | 0.0 Wh |
| 30 to 45 °C | Clean, with shield | 48.6 °C | 6.3 h | 7.3 Wh |
| 30 to 45 °C | Dusty, with shield | 50.8 °C | 5.4 h | 5.8 Wh |
| 22 to 35 °C | Clean, no shield | 50.8 °C | 8.0 h | 10.1 Wh |
| 22 to 35 °C | Dusty, no shield | 59.9 °C | 0.4 h | 0.0 Wh |
| 22 to 35 °C | Dusty, with shield | 40.9 °C | 12.0 h | 13.5 Wh |

- **The TRL 2 enclosure would not charge in hot weather.** The battery's charge cut-off at 45 °C (R9) blocks charging for nearly all of a clear hot day, and even on a 35 °C day once the box is dusty. A run of such days would drain the pack within its 29 days.
- **Sun shield.** A ventilated white aluminum hood over the top, sides and front (BOM item 17, $8) keeps the inside to about 51 °C on a 45 °C day and leaves 5.8 Wh for charging, 10.8 times the daily need. It lifts off for the monthly visit.
- **R9 is at risk.** The shield factor is assumed, the battery still sits above 45 °C for part of a hot day (which ages LiFePO4 cells faster), and the electronics' ratings are met with margin (ESP32-S3 and SIM7000-class modules are rated to 85 °C). Enclosure sealing (IP66), UV-stable materials and the opaque cell are met by the choice of parts.

## D. Sample flow, flushing and water use (R8, R1)

- **Cell volume.** The TRL 2 cell held 0.37 L. The TRL 3 cell holds 0.185 L of water once the baffle and the immersed sensors are subtracted. The 1/4 in sample tube from the tee to the cell runs 738 mm and holds 10.7 mL [D1].
- **Water use.** Each 90 s flush at 0.5 L/min uses 0.75 L, 18.0 L per day [D2]. At the start of the 10 s chlorine window, 2.9 % of the previous hour's water is still in the cell, and 1.8 % at its end; the TRL 2 cell would have held 17.0 %, enough to bias every chlorine reading low by that much when the old water had lost its residual [D3]. This is why the cell was made smaller rather than the flush longer.
- **Pressure.** A fixed orifice sized for 0.5 L/min at 1 bar passes 0.35 L/min at 0.5 bar and 1.00 L/min at 4 bar, which would use 36.0 L per day [D4] and break R8. A pressure-compensating regulator holds 0.5 L/min; at its +10 % tolerance the unit uses 19.8 L per day [D5]. **R8 is met on paper** with a 1 % margin at the upper tolerance. Below the regulator's compensating range, at 0.5 bar, the flow falls to about 0.35 L/min and the stale fraction rises to 8.5 % [D5]; a low-pressure site needs a longer flush, set per site.
- **Context.** The daily flush is 0.36 % of the draw of a tapstand serving 250 people at 20 L each. On the 15 min schedule the unit would use 72 L per day [D6]; R8 applies to hourly sampling.
- **Valve.** At 0.5 bar the valve must be direct acting, with no minimum pressure difference; pilot-operated valves need about 0.2 to 0.5 bar [D7]. BOM item 13 now says so.

## E. Free chlorine error budget (R1)

The HOCl pKa is 7.75 at 5 °C, 7.54 at 25 °C and 7.43 at 40 °C [E1]. At 25 °C the share of free chlorine present as HOCl is 0.92 at pH 6.5, 0.77 at pH 7.0, 0.52 at pH 7.5, 0.26 at pH 8.0 and 0.10 at pH 8.5; across the pH and temperature range of R1 it spans 0.15 to 0.90 [E2]. The TRL 2 precis quoted about a quarter at pH 8 and three quarters at pH 7; both stand.

Calibration against a DPD comparator at the site absorbs the pH at the time of calibration into the sensor's slope. What remains is the change in pH between visits, the comparator's own reading error (±0.07 mg/L), a 1.25 % residual temperature error and the 2.9 % stale-water bias [E3].

Under WWT-DDR-002, R1's target is ±0.2 mg/L or ±25 %, whichever is greater (it was ±0.1 mg/L below 1.0 mg/L and ±15 % above), and a site uses the pH probe variant when its pH is above 7.5 or moves more than 0.2 between visits. Table 3 gives both methods and marks the one the rule applies.

*Table 3. Error in free chlorine at 25 °C and zero sensor drift, against the relaxed R1 target [E4].*

| Free chlorine | pH | Site pH (±0.2 between visits) | pH probe variant (±0.1) | Method under the rule | Target (v0.3 target) | Room for drift |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5 mg/L | 7.0 | ±0.092 mg/L | ±0.077 mg/L | Site pH | ±0.200 (±0.100) mg/L | 0.177 mg/L |
| 0.5 mg/L | 7.5 | ±0.131 mg/L | ±0.091 mg/L | Site pH | ±0.200 (±0.100) mg/L | 0.151 mg/L |
| 0.5 mg/L | 8.0 | ±0.202 mg/L | ±0.115 mg/L | pH probe | ±0.200 (±0.100) mg/L | 0.163 mg/L |
| 0.5 mg/L | 8.5 | ±0.260 mg/L | ±0.135 mg/L | pH probe | ±0.200 (±0.100) mg/L | 0.148 mg/L |
| 1.5 mg/L | 7.0 | ±0.194 mg/L | ±0.118 mg/L | Site pH | ±0.375 (±0.225) mg/L | 0.321 mg/L |
| 1.5 mg/L | 7.5 | ±0.339 mg/L | ±0.186 mg/L | Site pH | ±0.375 (±0.225) mg/L | 0.160 mg/L |
| 1.5 mg/L | 8.0 | ±0.574 mg/L | ±0.284 mg/L | pH probe | ±0.375 (±0.225) mg/L | 0.245 mg/L |
| 1.5 mg/L | 8.5 | ±0.753 mg/L | ±0.352 mg/L | pH probe | ±0.375 (±0.225) mg/L | 0.130 mg/L |

- **Before DDR-002.** Against the v0.3 target with site pH everywhere, only 2 of the 8 cases were met, both at pH 7.0 [E5]. The DPD comparator alone took ±0.07 of the ±0.10 mg/L budget, so the target was as tight as the field reference.
- **With DDR-002.** The relaxed target is met in all 8 cases at zero drift when the pH probe rule applies [E6]. Site pH alone would just miss at pH 8.0 (±0.202 against ±0.200 mg/L at 0.5 mg/L), which is why the trigger sits at pH 7.5.
- **Warm water.** At 40 °C the HOCl pKa falls to 7.43 and the pH term grows. With the rule, 9 of 10 cases from pH 6.5 to 8.5 are met; the exception is 1.5 mg/L at pH 7.5 with site pH, at ±0.381 against ±0.375 mg/L [E7]. A site with warm water near pH 7.5 is a candidate for the probe.
- **Room for drift.** At 25 °C the smallest margin left for sensor drift under the rule is 0.130 mg/L, against 0.038 mg/L (and only at pH 7.0) under the v0.3 target [E8]. No verified long-term drift data are available (see `docs/REVIEW.md`), so **R1 is at risk**, not met.

## F. Turbidity reading: bubbles and settling (R2)

- **Bubbles.** Air released when the flow stops scatters light like particles. At 5 °C a 100 µm bubble rises at 3.6 mm/s and takes 18 s to clear the 66 mm cavity; a 50 µm bubble takes 74 s. At 25 °C the same bubbles take 11 s and 43 s [F1]. The TRL 2 wait of 10 s was too short in cold water.
- **Settling.** Silt of 10 µm settles at 0.10 mm/s: 3.5 mm during the 35 s of waiting and reading, and the clear layer at the top takes 5.4 min to reach the beam at mid-height [F2]. Settling does not bias the reading.
- **Change.** The wait is now 30 s, which clears 100 µm bubbles at 5 °C, for 35 mWh per day [F3]. Smaller bubbles remain possible when the supply is supersaturated with air.
- **R2 is at risk.** Range and resolution follow the published open-source design (Kelley et al., 2014), but fouling of the optical windows between monthly cleans cannot be estimated on paper.

## G. Data and storage (R6)

- **Airtime.** Each upload carries about 780 B of readings and status plus about 4,000 B of TLS, HTTP and network overhead, 0.86 MB per month; with TLS session resumption it falls to about 0.36 MB [G1]. R6's airtime assumption of under 1 MB per month holds.
- **Storage.** 90 days of readings take 138 kB as CSV on the microSD card; a 7-day ring buffer in flash takes 5.4 kB [G2]. R6 is met on paper.

## H. Alert latency (R5)

- **From confirmation to SMS.** A modem wake, network attach and SMS take about 140 s at the first try; with three tries at 3 min spacing the worst case is 13.0 min [H1]. R5 (15 min) is met on paper where there is coverage. The TRL 2 plan did not fix the retry spacing; at 5 min spacing the worst case would be 17 min, so 3 min is now specified.
- **From the event.** Under WWT-DDR-002 the firmware takes a confirming reading 15 min after a first threshold crossing instead of waiting for the next hourly reading. The worst case from the start of an event to the SMS falls from 122 min to 77 min [H2]. Each confirming reading costs 9.7 mWh and 0.75 L; even ten a month add only 3.2 mWh per day, 0.6 % of the daily need [H3], so sections A, B and D stand.

## I. Pole and footing in wind (structure, R11)

- **Loads.** A 35 m/s gust (735 Pa) puts 42 N on the panel at 2.16 m, 50 N on the enclosure at 1.30 m and 89 N on the pole at 1.05 m: 181 N in all and a base moment of 249 N·m [I1]. The shield adds a little to the enclosure area; it is inside the margins below.
- **Pole.** The 48.3 x 3.2 mm tube has a section modulus of 4.80 cm³ and sees 52 MPa, a factor of 4.5 on the 235 MPa yield [I2].
- **Footing.** A 300 mm footing 600 mm deep in medium sand resists 886 N sideways, a factor of 4.9 [I3]. Soft or wet ground needs a site check.

## J. Installation and the monthly visit (R11, R10)

- **Installation.** The tasks take 160 person-minutes. Done in one visit, the critical path is digging, setting the pole, waiting 30 min for fast-set concrete, then mounting, cabling and commissioning: 140 min against the 120 min of R11 [J1]. Under WWT-DDR-002 the footing is dug and cast, with the pole set in it, on the survey visit (75 min including the set). The critical path on installation day is then 65 min, with the 50 min of plumbing done in parallel [J2]. **R11 is met on paper** as restated in WWT-REQ-001 v0.4; the design parts of R11 (one tee, an isolation valve, a check valve, food-safe wetted parts and hand tools only) are met by design, and the open air break at the outlet keeps the drain from ever connecting back to the cell.
- **Monthly visit.** Cleaning the cell and electrode, a DPD test, a pH check, calibration from a phone and a look at the strainer, drain and panel take 30 min, exactly the R10 limit [J3]. **R10 is at risk:** a monthly visit is enough if the chlorine sensor drifts less than about 0.13 mg/L in a month under the relaxed R1 target (section E, [E8]; it was about 0.04 mg/L under the v0.3 target), and no verified data yet show the drift. At a pH probe variant site the pH comparator step becomes a check of the probe in a buffer, of similar length.

## K. Cost (R12)

The BOM has 17 lines totaling $283.00 against the $300 `budget_usd`, a margin of $17.00 (6 %) [K1]. The TRL 3 changes added $3 for the pressure-compensating regulator, $1 for the air-break fitting and $8 for the sun shield; WWT-DDR-002 added $1 for a spare pH port and blanking plug in the cell lid. R12 is met on paper for the base unit. A pH probe variant site costs about $343 to $383 per unit (probe and interface about $60 to $100, estimate) [K2]; as restated in WWT-REQ-001 v0.4, the probe is priced per variant site, outside the base-unit budget, like the shared calibration kit.

## L. Results against every requirement

*Table 4. Requirement status from this note [L].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Measure free chlorine | 8 of 8 cases met at 25 °C and zero drift with the pH probe rule; room for drift 0.13 mg/L; 1.5 mg/L at pH 7.5 and 40 °C misses by 0.006 mg/L | ±0.2 mg/L or ±25 %, whichever is greater, pH 6.5 to 8.5 | **At risk** (drift unknown) |
| R10 | Maintainable by a caretaker | Visit 30 min; needs drift below about 0.13 mg/L per month, unverified | Monthly or less, 30 min or less | **At risk** |
| R2 | Measure turbidity | 30 s wait clears 100 µm bubbles at 5 °C; fouling unknown | 0 to 100 NTU, ±0.5 NTU or ±10 % | **At risk** |
| R9 | Survive outdoors | 50.8 °C peak inside on a 45 °C day with the shield (69.8 °C without) | IP65; 0 to 45 °C ambient; charging blocked above 45 °C | **At risk** (shield factor assumed) |
| R11 | Install simply and safely | 65 min on installation day with the footing cast on the survey visit (140 min in one visit) | 2 h on installation day, hand tools, backflow prevented | Met on paper |
| R5 | Alert the people who act | 13.0 min worst case from confirmation to SMS; 77 min from the event with the 15 min confirming reading | 15 min | Met on paper (where there is coverage) |
| R6 | Report and keep data | 0.86 MB per month; 90 days in 138 kB | 4 h uploads, 90 days on board | Met on paper |
| R7 | Run on sunlight alone | 28.6 days autonomy; 1.18 clear days to refill | 7 days; 3 clear days | Met on paper |
| R8 | Use little treated water | 18.0 L/day nominal, 19.8 L at regulator tolerance | 20 L/day | Met on paper (thin margin) |
| R12 | Stay within the budget | $283 per base unit; $343 to $383 at a pH probe variant site | $300 per base unit | Met on paper |
| R3 | Measure water temperature | DS18B20, ±0.5 °C from -10 to 85 °C | 0 to 50 °C, ±0.5 °C | Met by design |
| R4 | Sample on a schedule | Hourly default; 15 min schedule within energy (1.589 Wh/day, 9.7 days) | 15 min to 24 h | Met by design |
| R13 | Report measurements, not verdicts | Alert wording rule | Never says "safe" | Met by design |

Counts: 0 not met, 4 at risk, 6 met on paper, 3 met by design (v0.1: 2 not met, 3 at risk, 5 met on paper, 3 met by design). No requirement is left unverifiable at TRL 3, although R1, R2, R9 and R10 each rest on an assumption that only a test can settle.

## Checks against the TRL 2 figures

| TRL 2 claim (WWT-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| About 0.5 Wh/day | 0.537 Wh/day (130 s awake) | Precis updated |
| About 30 days without sun | 28.6 days (24.3 days at 0 °C) | Precis updated |
| About 13 Wh per clear day; about 1.2 days to refill | 13.5 Wh; 1.18 days | Stands |
| Cell 0.37 L; 0.75 L flush is about two cell volumes | 0.185 L; 0.75 L is about four cell volumes | Cell halved, precis updated |
| About 18 L/day, R8 met | 18.0 L nominal, but 36 L at 4 bar with a fixed restrictor | Regulator added, precis updated |
| 10 s wait for bubbles | Too short at 5 °C; 30 s | Precis updated |
| Enclosure temperature not estimated | 61 to 70 °C peak without a shield on a 45 °C day | Shield added, precis updated |
| Under 1 MB per month | 0.86 MB | Stands |
| SMS within minutes | 13.0 min worst case with 3 min retries | Precis updated |
| HOCl about a quarter at pH 8, three quarters at pH 7 | 0.26 and 0.77 | Stands |
| About $270 | $283 (v0.1: $282) | Precis and BOM notes updated |
