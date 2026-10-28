---
doc_id: WWT-PLN-001
title: WaterWatch project plan
project: WaterWatch
doc_type: Project plan
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: workstreams, resources, stage gates, decision request and the reference list"
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'O1 to O5 decided by Amish (2026-10-25); calibration kit with the shared photometer'
---

# WaterWatch project plan

WaterWatch is at stage P3 (design outputs, TRL 3) with every P0 to P3 deliverable in place; the next gate, P4 verification, is on hold under the portfolio's stage cap of P3. Amish decided the concept carried forward (option A), the calibration reference graft, the product render layout, how water use counts event flushes and the chlorine accuracy target above 1 mg/L on 2026-10-25 (WWT-DEC-001 O1 to O5). Still open: the approach to the first candidate partner, which is Amish's outreach. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Project lead | WWT-PRB-001 with users and stakeholder tables | Done (P0 to P1) |
| STEM check | Design lead | WWT-STM-001 and `docs/04-calcs/stem_check.py` | Open: 9 plausible rows for option A need tests (TRL 4); S31 awaits Amish (O5) |
| Concept options | Design lead | WWT-OPT-001, WWT-DDR-004, D3 models of A, B and C | Done; option A chosen by Amish, 2026-10-25 |
| Requirements and traceability | Design lead | WWT-URS-001, WWT-PRS-001, WWT-RTM-001 | Done (P2) |
| Calculations | Design lead | WWT-CAL-001 v0.5 | Done (P2 to P3) |
| Design outputs | Design lead | `cad/src/model.py` at D3, STEP, drawings WWT-DWG-001 and 101 to 109, priced BOM, WWT-BLD-001, WWT-DEC-001 | Done (P3) |
| Regulatory, feasibility, risk, market | Project lead | WWT-REG-001, WWT-FEA-001, WWT-RSK-001 with design FMEA, WWT-MKT-001 | Done (P3 first pass) |
| Partner and pilot | Project lead | Approach the first candidate partner (Water Mission, WWT-DEC-001) | Not started; Amish's decision to approach |
| Verification (P4) | Design lead with a lab | Bench drift test of the chlorine sensor, turbidity standards, shield temperature log, backflow test | On hold (stage cap P3) |
| Validation (P5) | Partner | Field trial at two or three tapstands | On hold (stage cap P3) |

## Resources needed

Table 2. Resources for the next stages (estimates, for planning only; no spending is proposed while the cap is P3).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Prototype parts | One unit to the BOM | Workshop build, about 3 days | 325 (BOM, indicative) |
| Calibration kit | Handheld DPD photometer (O2, decided 2026-10-25), pH comparator, turbidity standards | Shared per operator | 380 to 600 for the photometer (WWT-MKT-001), plus about 60 for the comparator kit (estimate) |
| Lab bench time | Chlorine drift test against DPD over 4 weeks or more (closes S12, S14) | About 2 days set-up, 4 weeks logging | To assess with a partner lab |
| Partner time | Site survey (pressure, pH, coverage), caretaker routine | 2 to 3 site visits | To assess with the partner |
| Regulatory advice | Radio type approval route, wetted materials (WWT-REG-001 R7, W1) | Consultant, a few days | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Met |
| P1 Definition | URS, PRS, RSK, MKT | Met |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR | Met; the DDR's choice awaits Amish |
| P3 Design outputs | Model at D3 for every option, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability complete | Met (`cad/fidelity.json` passed) |
| P4 Verification | Bench tests close S4, S5, S12, S14, S22, S32 to S34, S36; PR-001, PR-002, PR-009, PR-010 verified | On hold (stage cap P3) |
| P5 Validation | Field trial with a partner; certification status in REG | On hold |
| P6 Commercialization | Launch plan with a named deployment partner | On hold |

## Next steps and decision requested

1. Done: Amish decided O1 to O5 on 2026-10-25 as recommended (WWT-DEC-001): option A, the shared photometer, installed heights in the product render, PR-008 counting the hourly schedule only, and PR-001 restated as ±30 % above 1.0 mg/L.
2. With his go, approach the first candidate partner with this TRL 3 pack (WWT-DEC-001, 2026-10-02).
3. When the portfolio cap allows TRL 4: build one unit and run the chlorine drift test first, because it decides between A and the fallback B (WWT-RSK-001 P1, F1).

## References

Every source cited in this repo's documents.

- Broms, B. B. "Lateral Resistance of Piles in Cohesionless Soils." *Journal of the Soil Mechanics and Foundations Division* 90, no. SM3 (1964): 123 to 156.
- CBC News. "Highlights of the Walkerton Inquiry Report." https://www.cbc.ca/news/canada/highlights-of-the-walkerton-inquiry-report-1.867604.
- Communications Authority of Kenya. *Importation, Type Approval and Distribution of Communications Equipment Regulations, 2010.* https://www.ca.go.ke/sites/default/files/2023-06/Importation-Type-Approval-And-Distribution-Of-Communications-Equipment-Regulations-2010-1.pdf. Accessed October 25, 2026.
- EN 1717:2025+A1:2026. *Protection against Pollution of Potable Water in Water Installations.* Listing at https://genorma.com/en/standards/en-1717-2025-a1-2026. Accessed October 25, 2026.
- Hanna Instruments. "Free and Total Chlorine Portable Photometer, HI97711." https://hannainst.com/free-and-total-chlorine-portable-photometer-hi97711.html. Accessed October 25, 2026.
- HX IFR32700 3.2 V 6000 mAh LiFePO4 cell. Product page, https://st.robu.in/?p=1430462. Accessed October 25, 2026.
- ISO 7027-1:2016. *Water Quality: Determination of Turbidity, Part 1: Quantitative Methods.* https://www.iso.org/standard/62801.html. Accessed October 25, 2026.
- ISO 7393-2. *Water Quality: Determination of Free Chlorine and Total Chlorine, Part 2: Colorimetric Method Using N,N-Diethyl-1,4-Phenylenediamine.*
- Kelley, C. D., A. Krolick, L. Brunner, A. Burklund, D. Kahn, W. P. Ball, and M. Weber-Shirk. "An Affordable Open-Source Turbidimeter." *Sensors* 14, no. 4 (2014): 7142 to 7155. https://www.mdpi.com/1424-8220/14/4/7142.
- Lindmark, M., et al. Passive chlorination by community water boards in Honduras. *ACS ES&T Water* (2023). https://pubmed.ncbi.nlm.nih.gov/38094914/.
- Morris, J. C. "The Acid Ionization Constant of HOCl from 5 to 35 °C." *Journal of Physical Chemistry* 70, no. 12 (1966): 3798 to 3805.
- Nagel, C., et al. Handpump sensors and repair times in Rwanda. *Environmental Science and Technology* (2015). https://pubs.acs.org/doi/10.1021/acs.est.5b04077.
- National Academies. *Lessons from Waterborne Disease Outbreaks* (workshop summary). https://www.ncbi.nlm.nih.gov/sites/books/NBK28459/.
- Oxfam WASH. "Chlorination in Emergencies." https://www.oxfamwash.org/chlorination-in-emergencies/.
- Pan, S., M. J. Deen, and R. Ghosh. "Low-Cost Graphite-Based Free Chlorine Sensor." *Analytical Chemistry* 87 (2015). https://pubs.acs.org/doi/10.1021/acs.analchem.5b03164.
- Pheasant, S., and C. M. Haslegrave. *Bodyspace: Anthropometry, Ergonomics and the Design of Work.* 3rd ed. Boca Raton: CRC Press, 2006.
- Plateau State water point sensors (2022). https://www.sciencedirect.com/science/article/pii/S2352728522000094.
- *PLOS ONE.* Pencil graphite electrodes for free chlorine (2021). https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0248142.
- Sensorex. "FCL Amperometric Free Chlorine Sensor." https://sensorex.com/product/fcl-amperometric-free-chlorine-sensor/.
- Atlas Scientific. "EZO Complete ORP Kit." https://atlas-scientific.com/kits/ezo-complete-orp-kit/.
- Thomson, P. Remote monitoring of rural water services. *WIREs Water* (2021). https://wires.onlinelibrary.wiley.com/doi/10.1002/wat2.1502.
- Transport Canada. "Research Summary: Evaluation and Analysis of Substandard Lithium-Ion Batteries by UN 38.3 Testing." https://tc.canada.ca/en/dangerous-goods/publications/lithium-battery-transport-research/research-summary-evaluation-analysis-substandard-lithium-ion-batteries-383-testing. Accessed October 25, 2026.
- UNICEF India. "Clean Drinking Water." https://www.unicef.org/india/what-we-do/clean-drinking-water.
- US EAS 12:2014. *Potable Water: Specification* (Uganda). https://tradebarriers.org/ntm/regulations/view/890. Accessed October 25, 2026.
- USABlueBook. "Hach CL17sc Chlorine Analyzer with Pressure Regulator Installation Kit, 8572400." https://usabluebook.com/hach-cl17sc-chlorine-analyzer-with-pressure-regula-53224. Accessed October 25, 2026.
- *Water Science and Technology* 92, no. 2 (2025): 326. Long-term performance of low-cost free chlorine sensors. https://iwaponline.com/wst/article/92/2/326/108695/Long-term-performance-of-low-cost-free-chlorine.
- WHO and UNICEF Joint Monitoring Programme. *Progress on Household Drinking Water, 2025.* https://data.unicef.org/resources/jmp-report-2025/; news release https://www.who.int/news/item/26-08-2025-1-in-4-people-globally-still-lack-access-to-safe-drinking-water---who--unicef.
- World Health Organization. "Drinking-Water" fact sheet (2023). https://www.who.int/news-room/fact-sheets/detail/drinking-water.
- World Health Organization. *Guidelines for Drinking-Water Quality: Fourth Edition Incorporating the First and Second Addenda.* Geneva: WHO, 2022. https://www.who.int/publications/i/item/9789240045064.
- World Health Organization. *Water Quality and Health: Review of Turbidity.* https://iris.who.int/server/api/core/bitstreams/938bdda2-b77c-480b-806c-1aa06e3126d0/content.
- Shared water-security register rows (NSF/ANSI 61; EU Drinking Water Directive (EU) 2020/2184; RoHS and WEEE): as cited in LMF-REG-001 (LumaFlow).
