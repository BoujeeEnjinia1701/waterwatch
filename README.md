# WaterWatch

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $300 USD · **Difficulty:** 3 of 5

Solar sentinel sensor that logs turbidity, free chlorine and temperature at a tap or tank and alerts over GSM or LoRa.

## Problem

Rural water points go untested between rare lab visits.

## Concept

Solar sentinel sensor that logs turbidity, free chlorine and temperature at a tap or tank and alerts over GSM or LoRa.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- IR turbidity sensor
- Amperometric chlorine probe
- Flow-through cell
- ESP32
- Cellular or LoRa modem
- PV panel

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> A sensor alert does not replace accredited lab testing.

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
