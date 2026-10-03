---
doc_id: WWT-DDR-001
title: WaterWatch TRL 2 review decisions
project: WaterWatch
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 to O3 recorded as decided by Amish on 2026-10-02
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Firmware settings notes added: alert message templates and recipient list (decision O2 of 2026-10-02)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D10; items O1 to O3 decided by Amish on 2026-10-02 (WWT-DEC-001)

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", and the design precis WWT-PRC-001 v0.2 listed key design choices, each with options and a recommendation. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open. The same instruction approved portfolio-wide decisions on the SwapCell interface (v0.3), on pricing shared SwapCell packs once, and on community designs picking co-design partners per area later. Only the last applies to WaterWatch.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in WWT-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Chlorine sensor | Option (a): a membrane-free graphite three-electrode sensor with a potentiostat front end, about $25, with a monthly DPD comparison built into the maintenance routine. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | pH | Option (a): site pH entered at installation and checked monthly, no added cost. A pH probe (option b) is kept as a documented variant for sites whose pH varies. `budget_usd` stays at $300. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Connectivity | Cellular LTE-M and NB-IoT with 2G fallback and SMS alerts for the first build, with the modem as a swappable module so a LoRaWAN module is a variant. This keeps the "GSM or LoRa" pitch. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Mounting | A separate pole beside the tapstand, not on it. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Sampling | An hourly 90 s timed flush through a latching valve, not continuous flow. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Default alert thresholds | Free chlorine below 0.2 mg/L and turbidity above 5 NTU, confirmed by two consecutive readings, adjustable per site. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Drain destination | The tapstand basin by default; a soakaway or a container for non-drinking use where users prefer, decided per site. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | First site type | Tapstands first; tank outlets and kiosks later. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | Battery | LiFePO4, with charging blocked below 0 °C and above 45 °C, rather than lithium-ion 18650 cells. Decided by Amish, 2026-09-25: go with recommendation. |
| D10 | SwapCell | Not used. WaterWatch needs about 0.5 Wh per day and a 48 V SwapCell pack does not fit. The SwapCell interface v0.3 items therefore do not apply. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items left open on 2026-09-25, decided by Amish on 2026-10-02 (WWT-DEC-001).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and region. The TRL 2 note suggested approaching a maintenance service provider, but Amish directed that community designs pick co-design partners per area later, so no partner, partner type or region was chosen on 2026-09-25. | Decided by Amish, 2026-10-02: a scheme operator that runs chlorinated, solar-powered piped schemes with public tapstands; the first candidate to approach is Water Mission, which runs such schemes in East Africa, with the first region taken from its country programs |
| O2 | Alert language, recipients and wording beyond the R13 rule; to come from caretakers and operators in co-design. No recommendation was made on 2026-09-25. | Decided by Amish, 2026-10-02: alerts go by SMS in the site's main local language, with an English copy to the operator, stating only what was measured, when and the threshold crossed; they go to the caretaker and the operator's maintenance contact, with a weekly summary to the district water officer |
| O3 | Who owns the data and who may see it (co-design checklist). No recommendation was made on 2026-09-25. | Decided by Amish, 2026-10-02: the scheme operator owns the data; the water committee and the district water and health offices can see it; anonymized site data are published only with the operator's written agreement |

## Firmware settings notes: alert messages and recipients

These notes carry decision O2 of 2026-10-02 into the firmware settings. They are notes for a later sketch, not firmware. The wording and languages are defaults to confirm with caretakers and the operator in co-design, and the first region is not yet chosen.

**Recipients, in the settings of each site.**

- The caretaker's phone: every alert, in the site's main local language.
- The operator's maintenance contact: every alert, with the English copy of the same message.
- The district water officer: a weekly summary only, in English or the local language as the district prefers. No single alert goes to the officer.
- Each number can be changed from the phone during the monthly visit. A site can hold up to five numbers.

**Rules for every message.** It states only what was measured, when, and the threshold crossed. It never says the water is safe or unsafe, never names a cause, and carries no instruction beyond asking the caretaker to check the tap and call the operator. It fits one SMS of 160 characters.

**Templates (English copy; the local language version is translated with the caretakers and checked by a speaker of that language before use).**

1. Chlorine low: "WaterWatch [site] [date] [time]: free chlorine [value] mg/L, below the [threshold] mg/L alert level, confirmed by two readings. Please check the tap and call [operator contact]."
2. Turbidity high: "WaterWatch [site] [date] [time]: turbidity [value] NTU, above the [threshold] NTU alert level, confirmed by two readings. Please check the tap and call [operator contact]."
3. Back to normal: "WaterWatch [site] [date] [time]: free chlorine [value] mg/L and turbidity [value] NTU, both within the alert levels."
4. No data: "WaterWatch [site] [date] [time]: no reading received since [date] [time]. Please check the box and the panel."
5. Weekly summary to the district officer: "WaterWatch [site] week to [date]: [n] readings; free chlorine lowest [value] mg/L, highest [value] mg/L; turbidity highest [value] NTU; [n] alerts. Measurements only; not a water safety result."

**Other settings.** An alert repeats at most once every 6 hours while the cause continues, and a first threshold crossing is confirmed by a second reading 15 minutes later (WWT-DDR-002, D13). The thresholds stay at free chlorine below 0.2 mg/L and turbidity above 5 NTU until the operator changes them.

## Consequences

- `project.yaml`: unchanged apart from the TRL fields. No budget, pitch or problem change was recommended, so `budget_usd` stays at $300 and the pitch still reads "alerts over GSM or LoRa".
- WWT-PRB-001, WWT-PRC-001 and WWT-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed". No requirement target changes as a result of these decisions; the 5 NTU and 0.2 mg/L defaults in R5 are now decided rather than proposed.
- The TRL 3 calculations (WWT-CAL-001) led to four design changes within these decisions: a smaller flow cell, a pressure-compensating flow regulator, a 30 s settling wait and a ventilated sun shield. They add $12 to the parts cost, now $282.
- WWT-CAL-001 v0.1 showed that R1 is not met with D2's site pH at pH 7.5 and above. The relaxed R1 target and the trigger for the pH probe variant that were then proposed are now decided by Amish, 2026-09-25: go with recommendation (WWT-DDR-002). D2 stands for sites at or below pH 7.5 whose pH stays within 0.2 between visits.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
