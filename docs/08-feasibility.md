---
doc_id: WWT-FEA-001
title: WaterWatch feasibility assessment
project: WaterWatch
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: first assessment of the TRL 3 design (option A)"
---

# WaterWatch feasibility assessment

Verdict (after the independent review of the STEM check): option A is feasible to build and run on paper with parts a small workshop can buy, but whether the low-cost chlorine sensor holds its calibration for a month is the one question that decides whether it is worth deploying, and only a test can answer it. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design: sensing | Turbidity follows a published open design and the ISO 7027 principle; temperature is a catalogue part; the chlorine sensor's response is known science, its drift is not | Medium | Drift of the membrane-free sensor and of its Ag/AgCl pseudo-reference (S12, S14), flow and conductivity effects (S32, S36); PR-001 not met at 1.5 mg/L by the corrected budget (S31, to Amish as O5) | WWT-STM-001 S10 to S14; WWT-CAL-001 E |
| Design: hydraulics | Timed flush clears the 0.185 L cell to 2.9 % stale water; the pressure-compensating regulator holds 19.8 L/day at its upper tolerance; air break and two check valves protect the supply | High | Below 0.7 bar the regulator stops compensating, so those sites flush for 110 s (WWT-DEC-001 F5); freezing near 0 °C to assess (S33) | WWT-STM-001 S6 to S9; WWT-CAL-001 D |
| Design: structure | Pole stress 59 MPa against 235 MPa yield in a 35 m/s gust on the sun shield; footing factor 4.3 in dry sand, 2.2 saturated | High | Screening wind values, not a code check | WWT-STM-001 S16, S17; WWT-CAL-001 I |
| Materials | Galvanised steel, aluminium sheet, PVC or ASA, EPDM, UV-stabilised polycarbonate, stainless fixings; all common and used in chlorinated water | High | Wetted grades to confirm (WWT-REG-001 W1) | WWT-STM-001 S28 |
| Manufacturing and assembly | Two plates cut and drilled, a cell machined or printed, three printed holders, a turned sensor holder; 19 assembly steps; installation day 65 min | High | Printed ASA porosity in a wet cell; machining the cell from PVC block is the safer route | WWT-BLD-001; WWT-CAL-001 J |
| Power and controls | 0.54 Wh/day against 7.5 Wh on an overcast day; 28.5 days on one 6 Ah cell; charging needs the sun shield on hot days | Medium | Shield factor assumed (S5); hot-day charging window of 5.4 h | WWT-STM-001 S1 to S5, S18; WWT-CAL-001 A to C |
| Communications | LTE-M, NB-IoT or 2G with SMS; 0.36 MB/month with TLS session resumption; 13 min worst confirmation to SMS, 92 min from the event | Medium | Coverage at each site to survey; type approval before field use (WWT-REG-001 R7) | WWT-STM-001 S19 to S21; WWT-CAL-001 G, H |
| Supply of parts | Every BOM line is a catalogue item or a simple made part; USD 325 per base unit, USD 25 over the value-engineering target | Medium | Prices are indicative; the LoRaWAN variant would bring the unit to about USD 304 | `bom/bom.csv`; WWT-CAL-001 K |

Ratings: High, Medium, Low.

The alternatives were assessed at the same level (WWT-OPT-001): option B (reagent colorimetry) is feasible but adds reagent supply, heat-limited reagent life and a chemical drain; option C (probes in the riser) is feasible to build but cuts the riser, puts glass electrodes in the drinking water path and estimates chlorine only loosely from ORP.

> **Safety:** The unit connects to a pressurised drinking water supply and contains a lithium iron phosphate cell. See WWT-PRC-001, Safety, and WWT-RSK-001.
