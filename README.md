# WaterWatch

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $300 USD · **Difficulty:** 3 of 5

Solar sentinel sensor that logs turbidity, free chlorine and temperature at a tap or tank and alerts over GSM or LoRa.

![WaterWatch concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/WWT-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

The two readings that tell a rural operator most about treated water at the tap are free chlorine residual and turbidity, and both can be measured without reagents. WaterWatch therefore pairs a membrane-free graphite chlorine sensor and an open-source infrared turbidimeter with a timed hourly flush, a small solar supply and plain SMS alerts, rather than a mains-powered utility analyzer whose chlorine probe alone costs about $1,900. It watches indicators and raises an alert; it does not dose, and it never declares water safe.

Keeping the design open and garage-buildable matters because the people who would install and maintain it are small scheme operators, maintenance service providers and caretakers, not utility instrument technicians. Every part is off the shelf or made from simple stock, the calibration is a monthly DPD comparator check that caretakers already know, and the CERN-OHL-S license lets a regional workshop build, repair and adapt the unit without a vendor.

## Burning platform

In 2024, 2.1 billion people still lacked safely managed drinking water ([WHO and UNICEF JMP, 2025](https://www.who.int/news/item/26-08-2025-1-in-4-people-globally-still-lack-access-to-safe-drinking-water---who--unicef)). WHO estimates that at least 1.7 billion people use a drinking water source contaminated with faeces, and that contaminated drinking water causes about 505,000 diarrhoeal deaths each year ([WHO, drinking-water fact sheet, 2023](https://www.who.int/news-room/fact-sheets/detail/drinking-water)).

Chlorination is the cheapest defense a piped rural scheme has, but it only protects people when a residual of at least 0.2 mg/L reaches the tap ([Oxfam WASH, chlorination in emergencies](https://www.oxfamwash.org/chlorination-in-emergencies/)). Today that is checked by hand when a technician visits, so a chlorinator that runs dry or a storm that clouds the source can go unnoticed for weeks. Remote sensors have already cut repair times for broken handpumps when someone was paid to act on the data ([Nagel et al., ES&T 2015](https://pubs.acs.org/doi/10.1021/acs.est.5b04077)); nothing comparable, open and affordable yet watches the quality of the water itself.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Rural water utilities and scheme operators | Watch chlorine residual and turbidity at tapstands across many villages and target dosing and repairs |
| Maintenance service providers | Add water quality alerts to existing handpump and scheme functionality monitoring contracts |
| Humanitarian WASH response | Track free chlorine at tapstands in camps and after floods, where chlorination is routine and outbreaks spread fast |
| Schools and health facilities | Monitor the tank outlet or tap that serves pupils and patients between official tests |
| Water kiosks and small private operators | Give customers and regulators a running record of the water they sell |
| Universities and WASH research groups | Collect long, open data sets on residual decay and turbidity events at the point of use |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Rwanda | Cellular handpump sensors paired with a paid maintenance service shortened repair times ([Nagel et al., 2015](https://pubs.acs.org/doi/10.1021/acs.est.5b04077)); the same service model could act on water quality alerts |
| Nigeria (Plateau State) | Sensors have already tracked functionality and use of rural water points ([Plateau State sensors, 2022](https://www.sciencedirect.com/science/article/pii/S2352728522000094)); water quality alerts would extend the same approach |
| South Asia (Bangladesh, India) | Dense shared taps, piped schemes with intermittent chlorination and monsoon turbidity make hourly readings useful to operators |
| Andean and Central American rural schemes | Gravity-fed community systems chlorinate at the tank, far from where people collect water, and are run by volunteer committees |
| Canada (Ontario) | A high-income example: at Walkerton in May 2000 low chlorine residuals at a municipal well went unrecorded and more than 2,000 people fell ill ([Walkerton Inquiry, Part One, 2002](http://www.archives.gov.on.ca/en/e_records/walkerton/report1/index.html)); small and remote systems still rely on few operators |

## What sparked the idea

The idea traces back to the E. coli outbreak in Walkerton, Ontario, in May 2000. Part One of the Walkerton Inquiry, released by Associate Chief Justice Dennis O'Connor in January 2002, found that the operators of Well 5 kept chlorine residuals of about 0.12 to 0.4 mg/L against the 0.5 mg/L required after 15 min of contact, tested weekly instead of daily, and often recorded estimates rather than measurements; more than 2,000 people fell ill and at least six died ([Walkerton Inquiry, Part One](http://www.archives.gov.on.ca/en/e_records/walkerton/report1/index.html); [summary of the findings](https://en.wikipedia.org/wiki/Walkerton_E._coli_outbreak)). A town in a high-income country, with a regulated municipal supply, lost its chlorine barrier without anyone noticing in time. At a village tapstand checked only on rare visits, the gap is wider, and a logged, automatic residual reading that raises its own alert is the part WaterWatch aims to supply.

## Problem

Rural water points go untested between rare lab visits, so a chlorinator that runs dry or a storm that clouds the source can go unnoticed for weeks. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A pole-mounted sentinel beside a village tapstand flushes a small sample through a dark flow-through cell once an hour, measures turbidity, free chlorine and temperature, logs the readings and sends them over cellular (LTE-M, NB-IoT or 2G; LoRaWAN as a variant). An SMS goes to the caretaker and operator when chlorine drops below 0.2 mg/L or turbidity passes 5 NTU. The TRL 3 calculations give 0.54 Wh per day, 28.6 days on battery without sun, 18 L per day of flushed water and $283 in parts against a $300 budget. Following Amish's decisions of 2026-09-25 (WWT-DDR-002), the chlorine accuracy target is ±0.2 mg/L or ±25 %, and sites above pH 7.5 or with a moving pH take a pH probe in a spare port of the cell; the error budget then meets the target before drift, but the low-cost sensor's long-term drift is unknown, so chlorine accuracy and the monthly maintenance interval remain at risk.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Infrared (860 nm) nephelometric turbidity head
- Membrane-free three-electrode free chlorine sensor with a potentiostat front end
- Temperature probe
- Opaque 0.19 L flow-through cell fed through a pressure-compensating regulator and a latching solenoid valve from a tee on the tapstand riser, draining through an open air break
- ESP32 controller with microSD logging
- Cellular modem (LTE-M, NB-IoT, 2G fallback), LoRaWAN as a variant
- 5 W solar panel and 3.2 V, 6 Ah LiFePO4 battery in an enclosure under a ventilated sun shield

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is `cad/src/model.py`, with STEP files in `cad/step/`.

## Safety

> A sensor alert does not replace accredited lab testing, and a normal reading does not mean the water is safe to drink. Contains a LiFePO4 battery: use a protection board, a fuse and charging temperature cut-offs. The sample line connects to a pressurized drinking water supply: fit an isolation valve and a check valve so nothing flows back into the supply.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (WWT-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `WWT-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
