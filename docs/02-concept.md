---
doc_id: WWT-PRC-001
title: WaterWatch design precis
project: WaterWatch
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, open questions, media)
---

# WaterWatch design precis

WaterWatch is a solar sentinel that stands on its own pole beside a village tapstand. Once an hour a latching valve on a tee in the tapstand riser opens for 90 s and flushes water through a small, dark flow-through cell. An infrared nephelometer measures turbidity, a membrane-free three-electrode sensor measures free chlorine and a sealed probe measures temperature. An ESP32 controller logs the readings, a cellular modem uploads them every 4 h, and an SMS goes to the caretaker and operator when chlorine drops below 0.2 mg/L or turbidity passes 5 NTU. First-order numbers suggest about 0.5 Wh per day, about 30 days on a 3.2 V, 6 Ah LiFePO4 battery without sun, about 18 L per day of flushed water and about $270 in parts. The weak point is the chlorine sensor: no low-cost sensor has yet shown months of unattended accuracy, so requirement R1 is not met on present evidence.

![Hero render](../media/hero.png)

*Figure 1. WaterWatch beside an existing tapstand (grey), with a 1.75 m person for scale. Solar panel on top, electronics enclosure at eye height, flow-through cell below it, latching valve and sample line from a tee on the tapstand riser, drain hose to the tapstand basin. Massing model.*

## How it works

1. **Sample.** A saddle tee with an isolation valve on the tapstand riser feeds a strainer, a flow restrictor (about 0.5 L/min) and a normally closed latching solenoid valve. Every hour the controller opens the valve for 90 s, flushing about two cell volumes through the flow-through cell, then closes it. A check valve stops water from the cell flowing back into the supply.
2. **Measure.** During the last 30 s of flow the controller reads the chlorine sensor, because amperometric sensors need steady flow across the electrode. After the valve closes it waits 10 s for bubbles to clear, then reads turbidity for 5 s and temperature. The cell is opaque so daylight does not reach the turbidity detector.
3. **Log.** Each reading is stored with a timestamp on a microSD card (90 days or more) and in a short ring buffer in flash.
4. **Report.** Every 4 h the modem wakes, attaches to LTE-M, NB-IoT or 2G, and posts a compact batch to an open endpoint the operator chooses. If two consecutive readings cross a threshold, it sends an SMS at once, without waiting for the next upload.
5. **Power.** A 5 W panel charges a 3.2 V, 6 Ah LiFePO4 battery through a small solar charger with temperature cut-offs. Everything else sleeps between readings.

![Sample and data flow](../media/flow.png)

*Figure 2. Sample and data flow. Values are estimates for the default hourly schedule.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Mounting pole and clamps | 48 mm galvanized tube, 2.1 m above ground, set in concrete beside the tapstand, U-bolt clamps | Keeps the tapstand itself unchanged |
| 2 | Solar panel | 5 W monocrystalline, about 250 x 190 mm, tilted 30° toward the equator | Oversized for the load so cloudy weeks are covered |
| 3 | Enclosure base | IP66 polycarbonate, about 200 x 120 x 260 mm, UV-stabilized, pressure-equalizing vent, cable glands underneath | Light grey to reduce solar heating |
| 4 | Enclosure lid and gasket | Supplied with item 3; tamper-resistant screws | |
| 5 | Battery | LiFePO4, 1S2P 32700 cells, 3.2 V, 6 Ah (19.2 Wh), protection board and NTC | Chemistry chosen for heat tolerance and thermal stability |
| 6 | Controller board | ESP32-S3 module, LiFePO4 solar charger, LMP91000-class potentiostat front end, valve driver with boost to 12 V, microSD, real-time clock | Carrier board; a custom PCB is TRL 4 work |
| 7 | Cellular modem | LTE-M and NB-IoT with 2G fallback (SIM7000G class), SIM | LoRaWAN module as a variant, proposed, awaiting Amish |
| 8 | Antenna | External LTE and GSM whip on a bulkhead | |
| 9 | Flow-through cell | Opaque black PVC or printed ASA block, about 120 x 60 x 90 mm, 0.37 L inside, with a baffle to slow flow past the sensors | Opens without tools for cleaning |
| 10 | Turbidity head | 860 nm infrared LED with light-to-frequency detectors at 90° (scatter) and 180° (reference), after [Kelley et al. (2014)](https://www.mdpi.com/1424-8220/14/4/7142) | ISO 7027 style wavelength |
| 11 | Free chlorine sensor | Membrane-free three-electrode sensor: graphite working electrode, Ag/AgCl reference, stainless counter, in a PVC holder, after [Pan et al. (2015)](https://pubs.acs.org/doi/10.1021/acs.analchem.5b03164) | Choice proposed, awaiting Amish; see design choices |
| 12 | Temperature probe | DS18B20 in a stainless sheath | Also used for chlorine sensor temperature compensation |
| 13 | Latching solenoid valve | 12 V, 6 mm (1/4 in) port, normally closed, food-safe wetted parts | Latching, so it draws power only while switching |
| 14 | Sample line | Saddle tee with isolation ball valve, strainer, check valve, 0.5 L/min restrictor, 6 mm PE tube | The only change to the tapstand |
| 15 | Drain hose | 12 mm hose from the cell outlet to the tapstand basin or soakaway | Site choice, see open questions |
| 16 | Cables, glands and fuse | Sensor and panel leads, IP68 glands, battery fuse | |

![Cutaway](../media/cutaway.png)

*Figure 3. Section looking at the front. Top: enclosure with the modem (7, purple) and battery (5, orange) on the left and the controller board (6, teal) on the right. Bottom: flow-through cell (9) with the chlorine sensor (11, blue) and temperature probe (12, green) entering from the top, and the turbidity head (10, yellow) on the left side.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions: hourly readings; 110 s awake per reading at an average of 80 mA from 3.3 V; a 50 µA sleep floor including the potentiostat bias, charger and protection board; six uploads a day at about 20 mWh each including network attach; a 50 % margin for alerts, retries and cold weather; 4.5 peak sun hours with 0.6 derating for heat, dust, angle and a small charger at low power.

Table 2. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Measurement energy | about 0.19 Wh/day | 0.26 W x 110 s x 24 | |
| Upload energy | about 0.12 Wh/day | 6 x 20 mWh | |
| Sleep and valve energy | about 0.01 Wh/day | 50 µA at 3.3 V for 24 h; 24 x 2 latching pulses of 50 ms at 12 V, 0.5 A, through an 80 % boost | |
| Daily energy with margin | about 0.5 Wh/day | 0.32 Wh x 1.5 | |
| Usable battery energy | about 15 Wh | 19.2 Wh x 0.8 | |
| Autonomy without sun | about 30 days | 15 / 0.5 | R7 met (7 days) |
| Solar yield, 5 W panel | about 13 Wh per clear day | 5 W x 4.5 h x 0.6 | R7 met: about 1.2 clear days to refill |
| Flow-through cell volume | about 0.37 L | Massing model interior | |
| Water per reading | about 0.75 L | 0.5 L/min for 90 s, about two cell volumes | |
| Water per day | about 18 L | 24 readings | R8 met (20 L), thin margin; about 0.4 % of a tapstand serving 250 people at 20 L each |
| Data per month | under 1 MB | About 1 kB per upload, 6 per day | R6 met; airtime about $1 to $3 per month |
| Alert delay | about 1 h worst case | Two consecutive hourly readings, then SMS within minutes | R5: the 15 min target counts from the confirming reading |
| Parts cost | about $270 | Indicative prices, see `bom/bom.csv` | R12 met, about $30 margin |
| Shared calibration kit | about $60 | DPD free chlorine and pH comparator, turbidity standards | Not in the unit cost |

The chlorine reading is the least certain number. Free chlorine is the sum of hypochlorous acid (HOCl) and hypochlorite (OCl⁻); their split depends on pH, with a pKa of about 7.5 at 25 °C, so at pH 8 only about a quarter of free chlorine is HOCl, while at pH 7 about three quarters is. Amperometric sensors respond mainly to HOCl, so the same free chlorine gives very different signals across the pH range in R1. The concept therefore relies on a site pH entered at installation and checked monthly with the DPD and pH comparator. That is adequate where source pH is stable and not where it varies, which is one reason R1 is marked not met.

## Key design choices

All are proposed, awaiting Amish.

- **Chlorine sensor.** Options: (a) a membrane-free graphite three-electrode sensor with a potentiostat front end, after [Pan et al. (2015)](https://pubs.acs.org/doi/10.1021/acs.analchem.5b03164) and the [pencil graphite work in PLOS ONE (2021)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0248142), about $25 in parts, open and cheap but unproven for months of unattended use; (b) an industrial membrane amperometric probe, well proven but about $1,900 for the probe alone ([Sensorex FCL](https://sensorex.com/product/fcl-amperometric-free-chlorine-sensor/)), far over budget; (c) an ORP probe as a proxy, about $175 as a kit ([Atlas Scientific](https://atlas-scientific.com/kits/ezo-complete-orp-kit/)), which tracks chlorine only loosely because ORP also depends on pH and other oxidants. Recommendation: (a), with the long-term performance literature ([Water Science and Technology, 2025](https://iwaponline.com/wst/article/92/2/326/108695/Long-term-performance-of-low-cost-free-chlorine)) reviewed at TRL 3, and a monthly DPD comparison built into the maintenance routine.
- **pH.** Options: (a) site pH entered at installation and checked monthly (no cost); (b) add a pH probe and interface (about $60 to $100, estimate), which would push the parts cost to about $330 to $370, over the $300 budget. Recommendation: (a) for the first build, with (b) as a documented variant for sites whose pH varies.
- **Sampling by timed flush, not continuous flow.** Continuous flow at 0.5 L/min would use about 720 L per day. An hourly 90 s flush uses about 18 L. Recommendation: timed flush with a latching valve.
- **Pole beside the tapstand, not on it.** A separate pole keeps the panel above head height, keeps the electronics out of reach of splashing and buckets, and needs no drilling into the tapstand. The cost is one more concrete footing. Recommendation: separate pole.
- **Connectivity.** Options: (a) cellular LTE-M and NB-IoT with 2G fallback and SMS alerts, working almost anywhere with coverage; (b) LoRaWAN, cheaper in airtime and power but only where a gateway exists, and with no direct SMS. Recommendation: (a) for the first build, with the modem as a swappable module so (b) is a variant, which keeps the "GSM or LoRa" pitch.
- **LiFePO4 battery.** Lithium-ion 18650 cells hold more energy per cell but degrade faster and are less stable in a hot enclosure. Recommendation: LiFePO4, with charging blocked below 0 °C and above 45 °C.
- **Drain.** Options: to the tapstand basin, to a soakaway, or into a container for non-drinking use. Recommendation: to the tapstand basin by default, decided per site with users.
- **SwapCell.** WaterWatch needs under 1 Wh per day, so the portfolio's 48 V SwapCell pack does not fit this design and is not proposed.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers. The tapstand (grey) is existing infrastructure and not in the BOM.*

## Safety

> **Safety:** WaterWatch is a monitoring aid, not a certification of water safety. A normal reading does not mean the water is free of pathogens or chemical contaminants; accredited laboratory testing, including microbiological testing, remains necessary. Alerts must be worded as measurements, never as "safe" or "unsafe".

> **Safety:** The design contains a lithium iron phosphate battery (19.2 Wh). Use cells with a protection board, a fuse at the battery, and charging cut-offs below 0 °C and above 45 °C. Keep the enclosure vented, light-colored and shaded where possible.

> **Safety:** The sample line connects to a pressurized drinking water supply. Fit an isolation valve and a check valve so nothing can flow back into the supply, use food-safe wetted materials, and never let the flushed sample return to the drinking water. Flushed water contains chlorine; drain it where it cannot pool against the tapstand or be mistaken for a separate water point.

> **Safety:** Calibration and cleaning use chemicals: DPD reagent tablets, and formazin turbidity standards, which are hazardous if made from their precursors. Use prepared, stabilized standards, gloves and the supplier's safety data sheets; do not make formazin in the field.

- The pole is a fall and impact hazard if it is not set properly; set it in concrete and keep sharp edges on the panel frame and clamps covered.
- Radio and battery equipment must meet local type-approval rules before any field installation.

## Open questions

- [ ] Which low-cost chlorine sensor has the best published long-term drift data, and what recalibration interval does it imply? (R1, R10)
- [ ] How hot does the enclosure get in full sun, and is shading needed for the battery? (R9)
- [ ] How fast do the cell and chlorine electrode foul at a turbid site, and does a monthly clean suffice? (R2, R10)
- [ ] Which alert thresholds, language and recipients do caretakers and operators want?
- [ ] Where should flushed sample water go at each site?
- [ ] Cellular or LoRaWAN for the first partner region? Proposed: cellular, awaiting Amish.
- [ ] First partner and region? Options: a rural utility or maintenance service provider already using handpump sensors, a WASH NGO running chlorinated piped schemes, or a university WASH research group. Proposed, awaiting Amish.
