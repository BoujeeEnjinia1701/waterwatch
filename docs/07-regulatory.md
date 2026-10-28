---
doc_id: WWT-REG-001
title: WaterWatch regulatory and standards register
project: WaterWatch
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: first register for the TRL 3 design (option A), with notes for options B and C"
---

# WaterWatch regulatory and standards register

Which standards and regulations would apply to WaterWatch as a product, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. WaterWatch is a monitoring aid that reports measurements; it never certifies water as safe (PR-013), and no certification is pursued while the portfolio is capped at TRL 3. The first region is not yet chosen (East Africa, through the first candidate partner, WWT-DEC-001), so national rows use Kenya as the worked example and are "to assess" for the region chosen. Rows W1 to W3 reuse the water-security research shared across the portfolio (LMF-REG-001, LumaFlow), each checked on the date in its source. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | WHO *Guidelines for Drinking-water Quality*, 4th edition with the first and second addenda | International (guidance adopted into national standards) | Chlorine residual and turbidity guidance; the basis of the field values in WWT-PRB-001 | Sets the meaning of the alert thresholds (0.2 mg/L free chlorine, 5 NTU; WWT-DDR-001 D6) and the rule that monitoring does not replace laboratory testing | Project lead | Applies (guidance) |
| R2 | ISO 7027-1:2016, water quality, determination of turbidity, quantitative methods | International | Nephelometric turbidity at 860 nm with detection at 90 degrees | The turbidity optics follow its wavelength and geometry (WWT-STM-001 S10); a claim of conformance would need its calibration and test procedure | Design lead | To assess (method followed, conformance not claimed) |
| R3 | ISO 7393-2, water quality, determination of free and total chlorine, colorimetric method with DPD | International | The DPD method used in the field reference (caretaker comparator) and in option B | Calibration reference for PR-001; the working principle of option B | Design lead | Applies (reference method) |
| R4 | EN 1717, protection against pollution of potable water in installations and devices to prevent pollution by backflow (current edition EN 1717:2025+A1:2026) | European Union and countries that adopt it | Fluid categories and backflow devices, including air gaps | The model for PR-014: an isolation valve and check valve on the supply, and an open air gap at the cell outlet so drain water can never reach the cell or the supply; the local water code at the site governs | Design lead with the operator | To assess at the first site (design follows the air-gap principle) |
| W1 | NSF/ANSI 61, drinking water system components, health effects | United States and Canada (referenced elsewhere) | Contaminants leached from materials in contact with drinking water | Wetted parts upstream of the check valve (saddle tee, isolation valve, strainer); downstream parts drain to waste | Design lead with a certification body | To assess (choose certified grades at part selection) |
| W2 | EU Drinking Water Directive (EU) 2020/2184, Article 11 (materials in contact with water) | European Union | Hygiene of materials and products in contact with drinking water | Wetted materials if sold in the EU | Design lead | To assess |
| R5 | National drinking water standard: for East African Community members the potable water specification EAS 12 (adopted nationally, for example as US EAS 12:2014 in Uganda; a 2022 revision was in draft) | East African Community | Limits for treated drinking water, including residual chlorine and turbidity | Context for site thresholds; WaterWatch measures, the operator complies | Scheme operator | To assess for the first region |
| R6 | IEC 60529, degrees of protection provided by enclosures (IP code) | International | Dust and water ingress ratings | The enclosure is a bought IP66 box; glands IP68; PR-009 asks for IP65 or better | Design lead | Met by design (bought ratings), to verify at TRL 4 after drilling |
| R7 | Kenya Information and Communications Act and the Importation, Type Approval and Distribution of Communications Equipment Regulations 2010 (Communications Authority of Kenya) | Kenya (worked example) | Type approval of radio and telecommunications equipment before import, sale or use | The cellular modem (BOM line 7) and the LoRaWAN variant; choose a modem module already type-approved in the country | Electronics lead | To assess; certification needed before any field unit |
| R8 | EU Radio Equipment Directive 2014/53/EU; US FCC Part 15 | European Union; United States | Radio and EMC conformity | Only if units are sold there | Electronics lead | Does not apply now; to assess at product stage |
| R9 | UN Manual of Tests and Criteria, section 38.3, and the dangerous goods rules for lithium cells (UN 3480, or UN 3481 when packed with or in equipment) | International (transport by air, sea and road) | Tests a lithium cell or battery type must pass before it is shipped | The one 32700 LiFePO4 cell (19.2 Wh): buy cells with a UN 38.3 test summary from the maker | Procurement | Applies (buy certified cells) |
| R10 | IEC 62133-2, safety of secondary lithium cells and batteries for portable applications | International | Cell and pack safety | The cell and its protection board; a recognised test is usual for a product | Electronics lead | To assess (product stage) |
| W3 | EU RoHS Directive 2011/65/EU and WEEE Directive 2012/19/EU; national e-waste rules | European Union; national | Hazardous substances and take-back of electrical equipment | Boards, modem, battery; end-of-life return through the operator | Electronics lead | To assess (product stage) |
| R11 | Data protection law in the region (for Kenya, the Data Protection Act 2019) | National | Personal data processing | Readings are not personal data, but SMS recipients' phone numbers are; the operator owns the data (WWT-DEC-001) | Scheme operator | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later.

Option B (reagent colorimetric analyser) adds the safety data sheets for its DPD and buffer reagents, their transport and storage, and the discharge of reacted sample, which the operator would need to clear locally (to assess). Option C (probes in the riser) puts glass pH and ORP electrodes and their reference electrolyte inside the drinking water path, so W1 and W2 would apply to the probes themselves (to assess).

## Sources

- World Health Organization, *Guidelines for Drinking-Water Quality: Fourth Edition Incorporating the First and Second Addenda* (Geneva: WHO, 2022), https://www.who.int/publications/i/item/9789240045064, accessed 2026-10-25.
- ISO 7027-1:2016 listing, International Organization for Standardization, https://www.iso.org/standard/62801.html, accessed 2026-10-25.
- EN 1717:2025+A1:2026 listing, Genorma, https://genorma.com/en/standards/en-1717-2025-a1-2026, and BSI Knowledge, https://knowledge.bsigroup.com/products/protection-against-pollution-of-water-intended-for-human-consumption-in-potable-water-installations-and-general-requirements-for-devices-to-prevent-pollution-by-backflow, accessed 2026-10-25.
- US EAS 12:2014, *Potable Water: Specification*, Uganda (Trade Barriers listing), https://tradebarriers.org/ntm/regulations/view/890, and the draft DEAS 12:2022, Tanzania Bureau of Standards, https://www.tbs.go.tz/uploads/publications/en-1664261414-DEAS%2012%20-%202022%20Potable%20water.pdf, accessed 2026-10-25.
- Communications Authority of Kenya, *Importation, Type Approval and Distribution of Communications Equipment Regulations, 2010*, https://www.ca.go.ke/sites/default/files/2023-06/Importation-Type-Approval-And-Distribution-Of-Communications-Equipment-Regulations-2010-1.pdf, and the type approval application form (revised 2023), https://ca.go.ke/sites/default/files/2024-04/Type-Approval-Application-Form-Revised-2023.pdf, accessed 2026-10-25.
- UN 38.3 overview: Transport Canada, "Research Summary: Evaluation and Analysis of Substandard Lithium-Ion Batteries by UN 38.3 Testing," https://tc.canada.ca/en/dangerous-goods/publications/lithium-battery-transport-research/research-summary-evaluation-analysis-substandard-lithium-ion-batteries-383-testing, accessed 2026-10-25.
- Rows W1 to W3: as cited in LMF-REG-001 (LumaFlow, water-security focus area), checked 2026-10-25.
- Rows R3, R6, R8, R10 and R11 are listed from the standards' and laws' own titles; their applicability is "to assess" and needs a test laboratory or regulatory consultant.
