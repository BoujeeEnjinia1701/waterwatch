---
doc_id: WWT-MKT-001
title: WaterWatch market and viability
project: WaterWatch
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: segments, cited benchmarks, unit cost from the BOM and the open route"
---

# WaterWatch market and viability

WaterWatch is for small scheme operators who chlorinate rural piped water but can only check the residual when a technician visits; the instruments that watch chlorine continuously cost ten times its parts cost and need mains power. An open, solar design that a regional workshop can build and an operator can maintain fills that gap, if the sensor holds its calibration (WWT-RSK-001 P1). Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Rural piped schemes with public tapstands | Scheme operators and maintenance service providers, East Africa first (WWT-DEC-001) | Hach CL17sc colorimetric chlorine analyser with installation kit, without reagents: USD 3,454 (USABlueBook, checked 2026-10-25); it needs mains power and reagents | 325 (parts, option A, `bom/bom.csv`, indicative) | Continuous free chlorine and turbidity at the tap, off grid, with SMS alerts, for about a tenth of the analyser's price |
| NGO and emergency chlorination programmes | WASH programmes, cholera and flood response | Manual DPD testing by a technician; a handheld DPD photometer, Hanna HI97711: USD 379.99 to 599.99 (Hanna Instruments, checked 2026-10-25) | 325 | Readings every hour between visits, not once a visit; the photometer stays the calibration reference |
| Research and teaching | Universities, WASH research groups, makerspaces | Amperometric free chlorine probe alone, Sensorex FCL: about USD 1,900 (cited in WWT-PRB-001, 2026-09-25); ORP kit, Atlas Scientific: about USD 175 (cited in WWT-PRC-001, 2026-09-25); neither page could be re-opened on 2026-10-25, so both are to re-check | 325 | An inspectable, reproducible system to test low-cost sensors against lab methods |
| Option B (reagent colorimetric analyser) | As the first segment | As above | About 380 to 450 (estimate from the option A BOM less the flow cell and sensors, plus two pumps, a stirrer, a larger cabinet and reagents; to assess) | Reference-method chemistry, at the cost of reagents to resupply |
| Option C (probes in the riser) | As the first segment | As above | About 300 to 380 (estimate: no pole or flow cell, plus pH and ORP electrodes and a manifold; to assess) | No water used, but a cut riser and a loose chlorine estimate |

Running costs per unit, outside the parts cost: airtime of about USD 1 to 3 a month (estimate, WWT-PRS-001 assumptions), DPD reagent for the caretaker's comparator, and, for option A, a chlorine electrode refresh at a rate to be found at TRL 4.

## Open route

- **Who builds it.** A regional electronics or water workshop builds units from the published files: two cut aluminium plates, a machined or printed flow cell, printed holders, bought modules and plumbing. The scheme operator installs and maintains them with the caretakers.
- **How it spreads.** Through the operator's own schemes first, then through WASH networks, universities that test low-cost sensors, and open hardware communities. Build reports and design suggestions come back through the repository's issue templates.
- **What keeps it open.** Hardware under CERN-OHL-S-2.0, software under MIT (PR-015); every change is published; no cloud service is required to receive the data (PR-006), so an operator is never locked to a vendor.
- **What it does not do.** It is a monitoring aid. It does not replace accredited laboratory testing and never declares water safe (PR-013, WWT-REG-001 R1).

## Sources

- USABlueBook, "Hach CL17sc Chlorine Analyzer with Pressure Regulator Installation Kit (no reagents included), 8572400," https://usabluebook.com/hach-cl17sc-chlorine-analyzer-with-pressure-regula-53224, accessed 2026-10-25.
- Hanna Instruments, "Free and Total Chlorine Portable Photometer, HI97711," https://hannainst.com/free-and-total-chlorine-portable-photometer-hi97711.html, accessed 2026-10-25.
- Sensorex, "FCL Amperometric Free Chlorine Sensor," https://sensorex.com/product/fcl-amperometric-free-chlorine-sensor/, as cited in WWT-PRB-001 (2026-09-25); not re-opened on 2026-10-25, to re-check.
- Atlas Scientific, "EZO Complete ORP Kit," https://atlas-scientific.com/kits/ezo-complete-orp-kit/, as cited in WWT-PRC-001 (2026-09-25); not re-opened on 2026-10-25, to re-check.
- Unit cost: `bom/bom.csv` and WWT-CAL-001 K1 (indicative prices, not quotes).
