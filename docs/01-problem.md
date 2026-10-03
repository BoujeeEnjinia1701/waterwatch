---
doc_id: WWT-PRB-001
title: WaterWatch problem statement
project: WaterWatch
doc_type: Problem statement
version: "0.4"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: For TRL 3, record Amish's decisions from WWT-DDR-001 (tapstands first, default thresholds); partner and region left open
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Partner, alert and data questions answered by Amish's decisions of 2026-10-02 (WWT-DEC-001)
---

# WaterWatch problem statement

Rural water points go untested between rare lab visits, so a chlorinator that runs dry or a storm that clouds the source can go unnoticed for weeks while people keep drinking the water.

## The problem

In 2024, 2.1 billion people still lacked safely managed drinking water, and about 40 % of rural people had no safely managed service ([WHO and UNICEF JMP, 2025](https://www.who.int/news/item/26-08-2025-1-in-4-people-globally-still-lack-access-to-safe-drinking-water---who--unicef); [JMP report 2025](https://data.unicef.org/resources/jmp-report-2025/)). Many rural schemes now chlorinate at the tank or with an in-line doser, but the check that the chlorine actually reaches the tap is a manual test with a comparator kit, done when a technician visits.

Two quantities tell an operator most of what they need to act on:

- **Free chlorine residual.** WHO guidance, as summarized for field use by Oxfam, is at least 0.5 mg/L after 30 min of contact at pH below 8, and at least 0.2 mg/L at the point of delivery ([Oxfam WASH, chlorination in emergencies](https://www.oxfamwash.org/chlorination-in-emergencies/)). No residual at the tap means the dose is missing or used up, and the water has no protection against recontamination.
- **Turbidity.** Particles shield microbes from chlorine. Chlorination loses effectiveness above about 10 NTU and is not recommended above 100 NTU without pre-treatment (same source); WHO's review of turbidity explains why lower is better ([WHO, Water quality and health: review of turbidity](https://iris.who.int/server/api/core/bitstreams/938bdda2-b77c-480b-806c-1aa06e3126d0/content)).

Remote monitoring has already changed rural water services for **functionality**. Cellular sensors on handpumps in Rwanda shortened repair times when paired with a maintenance service that acted on the data, and similar sensors have tracked functionality and use in Nigeria ([Nagel et al., ES&T 2015](https://pubs.acs.org/doi/10.1021/acs.est.5b04077); [Plateau State sensors, 2022](https://www.sciencedirect.com/science/article/pii/S2352728522000094); [Thomson, WIREs Water 2021](https://wires.onlinelibrary.wiley.com/doi/10.1002/wat2.1502)). The same is not yet true for **water quality**. Reagent-free in-line chlorine analyzers are built for utilities: an amperometric probe alone lists at about $1,900 ([Sensorex FCL](https://sensorex.com/product/fcl-amperometric-free-chlorine-sensor/)) and needs a flow cell, a transmitter and mains power. Low-cost parts exist but are not yet a system: a proven open-source turbidimeter ([Kelley et al., Sensors 2014](https://www.mdpi.com/1424-8220/14/4/7142)), research graphite chlorine sensors ([Pan et al., Anal. Chem. 2015](https://pubs.acs.org/doi/10.1021/acs.analchem.5b03164); [pencil graphite electrodes, PLOS ONE 2021](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0248142)) and early long-term trials of low-cost chlorine sensors in on-site water reuse ([Water Science and Technology, 2025](https://iwaponline.com/wst/article/92/2/326/108695/Long-term-performance-of-low-cost-free-chlorine)). There is no open, solar-powered reference design that a small operator can build, install on a tapstand and trust enough to act on.

## Users and context

Table 1. Users and context (proposed; to be confirmed through co-design).

| User | Need | Context |
| --- | --- | --- |
| Tapstand caretaker or water committee member | A plain alert when the water at the tap needs attention, and a simple monthly check routine | Village tapstand, kiosk or school tank; phone with SMS, often not a smartphone |
| Scheme operator or maintenance service provider | Chlorine and turbidity trends from many points, so dosing and repairs can be targeted | Small utility, NGO or private operator serving several villages |
| District water or health officer | Evidence that treated water reaches people, especially during cholera or flood season | Periodic review; outbreak response |
| Researcher or open hardware community | A reproducible, inspectable design to build on | University labs, makerspaces, WASH research groups |

Typical site: a public tapstand or a storage tank outlet on a piped rural scheme with chlorination at the source or tank. No mains power. Ambient temperature from about 0 to 45 °C, direct sun, dust and splashing. Cellular coverage is usually 2G or LTE-M/NB-IoT; some districts have a LoRaWAN gateway.

## Constraints

- Garage-buildable prototype, about $300 USD in parts per unit (`project.yaml`), using off-the-shelf modules and simple fabricated parts.
- Solar powered, with no mains connection and no change to the tapstand beyond one tee on the riser.
- Must not waste much treated water, and must not contaminate the supply (backflow and material safety).
- Must be maintainable by a trained caretaker with a comparator kit, without special tools.
- Must not claim that water is "safe". It reports measurements and alerts; accredited lab testing, including microbiological testing, stays necessary.

## Out of scope

- Microbiological detection (for example *E. coli*); the sensor watches indicators only.
- Chemical contaminants such as arsenic, fluoride or nitrate.
- Controlling the chlorine dose; WaterWatch observes and alerts, it does not dose.
- Household point-of-use treatment.

## Co-design checklist

- [ ] Identify a partner scheme operator or maintenance service and two or three pilot sites.
- [ ] Interview caretakers, operators and district officers on alert content, language, thresholds and who acts.
- [ ] Confirm local cellular coverage and SMS costs, or LoRaWAN availability.
- [ ] Agree where flushed sample water goes at each site.
- [ ] Agree who owns the data and who may see it.

## Open questions

- Which partner and region first? Decided by Amish, 2026-10-02 (WWT-DEC-001): a scheme operator that runs chlorinated, solar-powered piped schemes with public tapstands; the first candidate to approach is Water Mission, which runs such schemes in East Africa, with the first region taken from its country programs; not yet approached.
- Tapstand only, or also storage tank outlets and kiosks? Decided by Amish, 2026-09-25: tapstands first, tank outlets and kiosks later (WWT-DDR-001, D8).
- Which alert thresholds should be defaults? Decided by Amish, 2026-09-25: free chlorine below 0.2 mg/L and turbidity above 5 NTU, confirmed by two consecutive readings and adjustable per site (WWT-DDR-001, D6). Partners may still ask for other site values.
- Alert language, recipients and data ownership: decided by Amish, 2026-10-02 (WWT-DEC-001) as defaults to confirm in co-design: alerts go by SMS in the site's main local language, with an English copy to the operator, stating only what was measured, when and the threshold crossed; they go to the caretaker and the operator's maintenance contact, with a weekly summary to the district water officer; the scheme operator owns the data; the water committee and the district water and health offices can see it; anonymized site data are published only with the operator's written agreement.
