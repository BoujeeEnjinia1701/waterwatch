---
doc_id: WWT-URS-001
title: WaterWatch user requirements
project: WaterWatch
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "First user requirements, drawn from WWT-PRB-001 Tables 1 to 3 (kit 1.9.1 upgrade)"
---

# WaterWatch user requirements

What caretakers, scheme operators, district officers, researchers and the people who drink the water need, written from their side. They are drawn from the users and stakeholders in WWT-PRB-001 (Tables 1 to 3) and the decisions Amish has made (WWT-DDR-001, WWT-DDR-002, WWT-DEC-001). None is yet validated with a scheme operator; co-design with the first partner will revise them. The product requirements that meet these needs are in WWT-PRS-001 (`03-requirements.md`), and the links are in the traceability matrix WWT-RTM-001 (`03b-traceability.md`). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Chlorine at the tap | Know whether free chlorine is reaching the tap, often enough to act before people drink unprotected water for days | High | Caretaker; scheme operator; district health officer (PRB Tables 1 and 2) |
| UR-002 | Performance | Cloudy water | Know when the water turns cloudy, because chlorine stops working well in turbid water | High | Scheme operator; district water officer |
| UR-003 | Usability | Alerts to the people who act | Get a plain alert on a basic phone soon after a problem is confirmed, in the local language | High | Caretaker; scheme operator (WWT-DEC-001, alert rules) |
| UR-004 | Performance | Trends and records | See readings from many tapstands over time, kept even when the network fails, in an open format | Medium | Scheme operator; district officers |
| UR-005 | Environment and durability | No mains power | Run on sunlight alone, through cloudy weeks, with no mains supply at the site | High | Scheme operator (PRB, Users and context) |
| UR-006 | Environment and durability | Outdoor site | Keep working in direct sun, heat to 45 °C, dust and splashing for years | High | Scheme operator; caretaker |
| UR-007 | Safety | Supply kept clean | Never contaminate the drinking water supply, by backflow or by unsafe materials | High | People who drink the water; district health officer (PRB Table 3) |
| UR-008 | Logistics | Little water used | Use only a small share of the treated water the tapstand delivers | Medium | Water committee (PRB, Constraints) |
| UR-009 | Maintenance | Monthly caretaker check | Keep the unit accurate with one short monthly visit by a trained caretaker using a comparator kit and no special tools | High | Caretaker; scheme operator |
| UR-010 | Deployment and assembly | Simple installation | Install beside an existing tapstand with hand tools, changing nothing on the tapstand beyond one tee on the riser | High | Scheme operator; water committee (PRB, Constraints) |
| UR-011 | Cost | Affordable per point | Cost little enough per tapstand that a small operator can monitor many points | High | Scheme operator; funders (`project.yaml` value-engineering target) |
| UR-012 | Regulatory | Measurements, not verdicts | Report what was measured and when, and never claim that the water is safe | High | District health officer (PRB, Constraints) |
| UR-013 | Performance | Water temperature | Know the water temperature, for chlorine correction and context | Low | Researcher; scheme operator |
| UR-014 | Usability | Open and reproducible | Build, inspect and improve the design from published files | Medium | Researcher or open hardware community (PRB Table 2) |
| UR-015 | Safety | Safe to handle | Handle the unit, its battery and its calibration chemicals without harm | High | Caretaker; technician |
| UR-016 | Performance | Adjustable schedule | Change how often the unit reads, for an outbreak or a study | Low | Scheme operator; researcher |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.

> **Safety:** A unit that meets these needs still does not show that water is safe to drink. Accredited laboratory testing, including microbiological testing, remains necessary (WWT-PRC-001, Safety).
