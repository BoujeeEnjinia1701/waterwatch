# WaterWatch

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $300 USD · **Difficulty:** 3 of 5

Solar sentinel sensor that logs turbidity, free chlorine and temperature at a tap or tank and alerts over GSM or LoRa.

![WaterWatch concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Rural water points go untested between rare lab visits, so a chlorinator that runs dry or a storm that clouds the source can go unnoticed for weeks. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A pole-mounted sentinel beside a village tapstand flushes a small sample through a dark flow-through cell once an hour, measures turbidity, free chlorine and temperature, logs the readings and sends them over cellular (LTE-M, NB-IoT or 2G; LoRaWAN as a variant). An SMS goes to the caretaker and operator when chlorine drops below 0.2 mg/L or turbidity passes 5 NTU. Estimates: about 0.5 Wh per day, about 30 days on battery without sun, about 18 L per day of flushed water and about $270 in parts. The low-cost chlorine sensor is unproven over months of unattended use, so the chlorine accuracy requirement is not yet met.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Infrared (860 nm) nephelometric turbidity head
- Membrane-free three-electrode free chlorine sensor with a potentiostat front end (proposed)
- Temperature probe
- Opaque flow-through cell fed by a latching solenoid valve from a tee on the tapstand riser
- ESP32 controller with microSD logging
- Cellular modem (LTE-M, NB-IoT, 2G fallback), LoRaWAN as a variant
- 5 W solar panel and 3.2 V, 6 Ah LiFePO4 battery

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

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

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
