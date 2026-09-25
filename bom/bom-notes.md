# BOM notes

- Row numbers match the callouts in `media/exploded.png`, Table 1 of WWT-PRC-001 and the parts in `cad/src/model.py`.
- All prices are indicative USD for one prototype, taken from typical retail and distributor listings in 2026. They are estimates, not quotes; every line has a supplier type. Total: $282.00 against the $300 budget in `project.yaml`, a margin of $18 (6 %), checked by `docs/04-calcs/sizing.py` (WWT-CAL-001, K1).
- TRL 3 changes from WWT-CAL-001: item 9 is a smaller cell (0.19 L of water); item 13 is specified as direct acting; item 14 carries a pressure-compensating flow regulator in place of the fixed restrictor (+$3); item 15 adds an outlet elbow with an open air break (+$1); item 17, a ventilated sun shield, is new (+$8).
- Not in the unit cost: the existing tapstand; concrete for the pole footing; a shared calibration kit (DPD free chlorine and pH comparator, stabilized turbidity standards, about $60, estimate); cellular airtime (about $1 to $3 per month, estimate).
- Item 11 is the least certain line. An industrial amperometric probe costs about $1,900 and does not fit the budget; see the design choices in WWT-PRC-001. A pH probe variant (about $60 to $100, estimate) would also exceed the budget.
