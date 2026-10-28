"""WaterWatch STEM check calculations (WWT-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which docs/01b-stem-check.md tabulates. Rows S1 to S28 are the claims of
option A, the design as built on paper (WWT-PRC-001); B1 to B6 and C1 to C6 are the claims of options B and C
(WWT-OPT-001). The first-order numbers for option A come from the calculation note WWT-CAL-001
(docs/04-calcs/sizing.py), which this script imports, so a design change reruns the check. These are screens of
each claim against known science; the sizing itself is in the calculation note.
"""
import contextlib
import io
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401

sys.path.insert(0, "docs/04-calcs")  # noqa
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  WWT-CAL-001; reads cad/src/model.py and bom/bom.csv

c = Check()

# ------------------------------------------------------------------------------------------ option A: physics
c.balance("S1", "A 5 W panel covers the 0.54 Wh daily need on a dull rainy-season day", "Physics", "Electromagnetism and circuits",
          inputs={"panel yield, rainy-season day (2.5 peak sun hours, 0.6 derating)": CAL.y_wet},
          outputs={"daily need with 1.5 margin": CAL.e_day}, unit="Wh/day",
          law="Energy balance: P_panel x peak sun hours x derating >= E_day; at 1 peak sun hour the yield is 3.0 Wh, still above the need",
          closed_by="WWT-CAL-001 A3, B2")
c.claim("S2", "The battery runs the unit for 7 days or more without sun", "Physics", "Electromagnetism and circuits",
        f"Autonomy = usable energy / daily need, with an {CAL.CONV:.2f} efficient 3.3 V converter (independent review): {CAL.e_use:.2f} Wh / {CAL.e_day / CAL.CONV:.3f} Wh; "
        f"{CAL.aut:.1f} days without the converter loss", round(CAL.e_use / (CAL.e_day / CAL.CONV), 1), 7.0, "days", rule="above",
        closed_by="WWT-CAL-001 A6, B1")
hot_e = CAL.hot[(45.0, "dusty, with shield")][2]
c.claim("S4", "The panel refills an empty battery in 3 clear days or fewer, also on 45 degC days", "Physics", "Electromagnetism and circuits",
        f"Days = usable energy / (energy the charger may take - daily need); {CAL.e_use / (CAL.y_clear - CAL.e_day):.2f} days on a mild clear day; on a 45 degC day "
        f"only {hot_e:.1f} Wh may be charged under the shield (C4), so it depends on S5 (independent review)",
        round(CAL.e_use / (hot_e - CAL.e_day), 2), 3.0, "days", margin=0.05, closed_by="")
peak = CAL.hot[(45.0, "dusty, with shield")]
c.cited("S5", "Under the ventilated sun shield the enclosure stays near 51 degC on a 45 degC day and the battery can charge for about 5 h",
        "Physics", "Heat transfer",
        "Lumped thermal model: absorbed sun (absorptance 0.70, 900 W/m2 direct) against 10 W/m2K over the exposed area, time constant "
        f"{CAL.tau / 60:.0f} min; the shield passes a quarter of the solar gain (assumed)",
        f"Peak {peak[0]:.1f} degC, {peak[1]:.1f} sun hours below the 45 degC charge limit; the shield factor 0.25 is an assumption, "
        "to measure at TRL 4", PLAUSIBLE, closed_by="")
c.claim("S6", "One 90 s flush leaves less than 5 % of the previous hour's water in the cell when the chlorine is read", "Physics", "Fluid mechanics",
        f"Well-mixed cell: stale fraction = exp(-(Q t - V_tube) / V_cell), Q 0.5 L/min, t {CAL.t_cl:.0f} s, V_cell {CAL.v_cell:.3f} L",
        round(CAL.stale(CAL.Q, CAL.t_cl) * 100, 1), 5.0, "%", closed_by="WWT-CAL-001 D3 (above 0.7 bar; see S29)")
c.claim("S29", "At a 0.5 bar site a 110 s flush leaves less than 5 % stale water", "Physics", "Fluid mechanics",
        f"As S6 at {CAL.q_lo:.2f} L/min below the regulator's compensating pressure (90 s gives {CAL.stale(CAL.q_lo, CAL.t_cl) * 100:.1f} %, independent review); "
        f"{CAL.q_lo * CAL.T_FLUSH_LOW / 60 * CAL.READINGS:.1f} L/day", round(CAL.stale(CAL.q_lo, CAL.T_FLUSH_LOW - CAL.T_READ_CL) * 100, 1), 5.0, "%",
        closed_by="WWT-DEC-001 F5; WWT-CAL-001 D8")
c.claim("S7", "Hourly flushing uses 20 L/day or less at the regulator's upper tolerance", "Physics", "Fluid mechanics",
        "Volume = 0.55 L/min x 90 s x 24 readings (pressure-compensating regulator, +10 %); ten confirming readings a month add about 0.25 L/day; PR-008 counts the hourly schedule only (WWT-DEC-001 O4, decided by Amish 2026-10-25)", round(CAL.q_hi * CAL.T_FLUSH / 60 * CAL.READINGS, 1), 20.0, "L/day",
        closed_by="WWT-CAL-001 D5")
c.cited("S8", "The open air-break vent at the cell outlet stops the drain hose siphoning the cell and stops drain water reaching the cell",
        "Physics", "Fluid mechanics",
        "A siphon needs a sealed, liquid-filled path; a vent open to the atmosphere above the outlet holds atmospheric pressure there "
        "(hydrostatics). An air gap is the highest category of backflow protection in EN 1717 practice",
        "The vent rises 60 mm above the outlet and stays open; the inlet side is S30", WITHIN,
        closed_by="WWT-PRC-001, How it works 1; WWT-DWG-001")
c.cited("S30", "Cell water cannot flow back into the supply through the inlet when the main goes to negative pressure", "Engineering and technology", "Standards practice",
        "On an intermittent supply the main can fall below atmospheric pressure and draw water back; one plain check valve is not a verifiable barrier "
        "(independent review). The cell is closed and full, so a back-siphon would pull cell water through the inlet",
        "Two check valves in series (supply train and cell inlet) and the normally closed latching valve, shut 58 min in each hour (WWT-DEC-001 F8); "
        "a verifiable backflow device or an inlet air gap to assess with the operator under the local code (WWT-REG-001 R4)", WITHIN,
        closed_by="WWT-DEC-001 F8")
vb = CAL.stokes(100e-6, 1000, 1.52e-3)
c.claim("S9", "Bubbles of 100 um and larger clear the 66 mm cavity during the 30 s wait at 5 degC", "Physics", "Fluid mechanics",
        f"Stokes rise velocity, Re {1000 * vb * 100e-6 / 1.52e-3:.2f} (below 1, so Stokes holds), water at 5 degC; the wait clears bubbles of about 78 um and up, "
        "not bubbles stuck to the windows", round(CAL.H_CELL / vb, 1), 30.0, "s",
        closed_by="WWT-CAL-001 F1, F3")
c.cited("S10", "An 860 nm LED with a 90 degree scatter detector and a 180 degree transmitted-light detector measures turbidity from 0 to 100 units", "Physics", "Optics and radiation",
        "ISO 7027-1:2016 gives 860 nm diffuse radiation at 90 degrees for low turbidity (reported in FNU, about 0 to 40) and attenuation of the "
        "transmitted beam for higher turbidity (FAU); the cell has both detectors, so the upper range uses the 180 degree reading (independent review: "
        "say FNU, not NTU); Kelley et al. (2014) built an open-source turbidimeter on the same principle",
        "Principle and wavelength match the standard; accuracy of this cell (R2) to verify with stabilised standards at TRL 4", WITHIN,
        closed_by="Kelley et al. 2014; ISO 7027-1")
c.claim("S16", "The 48.3 x 3.2 mm pole carries a 35 m/s gust on the panel, sun shield and pole with a factor of at least 1.5 on yield", "Physics",
        "Strength of materials", f"sigma = M / Z at the footing, M {CAL.M:.0f} N m, Z {CAL.Z / 1000:.2f} cm3; S235 yield 235 MPa / 1.5",
        round(CAL.sig, 0), round(235 / 1.5, 0), "MPa", closed_by="WWT-CAL-001 I2")
c.claim("S17", "The 300 mm x 600 mm footing resists the gust load with a factor of at least 1.5, also in saturated sand", "Physics", "Mechanics and statics",
        f"Broms, short rigid free-head pile: H_u = 0.5 gamma D L^3 Kp / (e + L), Kp 3; dry medium sand (18 kN/m3) {CAL.Hu:.0f} N, saturated sand "
        "(9 kN/m3, independent review) shown; clay and made ground to assess at the survey visit",
        round(CAL.Hu_wet, 0), round(1.5 * CAL.F_tot, 0), "N", rule="above", closed_by="WWT-CAL-001 I3, I4")
c.claim("S35", "After 20 % capacity fade from hot-weather ageing the battery still runs 7 days without sun", "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 loses capacity faster when held above 45 degC (independent review); autonomy with 80 % of the capacity and the converter loss",
        round(0.8 * CAL.e_use / (CAL.e_day / CAL.CONV), 1), 7.0, "days", rule="above", closed_by="WWT-CAL-001 A6, B1")
c.cited("S18", "Charging is blocked below 0 degC and above 45 degC, which protects the LiFePO4 cell", "Physics", "Thermodynamics",
        "Lithium plating on charge below 0 degC and faster ageing when charged hot are known for LiFePO4; cell datasheets give a 0 to 45 degC charge window",
        "Charger with temperature cut-offs (BOM line 6) and NTC on the cell; to confirm in the charger datasheet (WWT-DEC-001, to confirm 8)", WITHIN,
        closed_by="WWT-DDR-001 D9")

# ------------------------------------------------------------------------------------------ option A: chemistry
# The battery claim failed at the first check: "1S2P 32700 cells, 3.2 V, 6 Ah". One 32700 LiFePO4 cell holds about 6 Ah,
# so two in parallel hold 12 Ah; the stated capacity, the cell count and the thermal mass (0.29 kg, two cells) disagreed.
# Fix (WWT-DEC-001 F1): one 32700 cell, 6 Ah, 0.135 kg; capacity, autonomy and price unchanged.
CELL_AH = 6.0
n_parallel_old, n_parallel = 2, 1
mismatch_old = abs(n_parallel_old * CELL_AH - CAL.CELLS[1]) / CAL.CELLS[1]
mismatch = abs(n_parallel * CELL_AH - CAL.CELLS[1]) / CAL.CELLS[1]
c.claim("S3", "The battery's cell count matches its stated capacity, 6 Ah at 3.2 V (19.2 Wh)", "Chemistry", "Electrochemistry and batteries",
        "Pack capacity = cells in parallel x cell capacity; one 32700 LiFePO4 cell is 6.0 Ah (reseller listing; maker datasheet to obtain, WWT-DEC-001 to confirm 9); mismatch between stated and built capacity",
        round(mismatch * 100, 1), 5.0, "%", closed_by="WWT-DEC-001 F1 (was 1S2P, 100 % mismatch)")
c.claim("S11", "At pH 8 and 25 degC about a quarter of free chlorine is hypochlorous acid", "Chemistry", "Physical (kinetics, equilibria, thermochemistry)",
        "HOCl fraction = 1 / (1 + 10^(pH - pKa)), pKa from Morris (1966): 3000 / T - 10.0686 + 0.0253 T",
        round(abs(CAL.f_hocl(8.0, 25) - 0.26), 3), 0.02, "absolute error vs 0.26", closed_by="WWT-CAL-001 E1, E2")
c.cited("S12", "A membrane-free graphite three-electrode sensor reads free chlorine from 0 to 2 mg/L with drift below 0.15 mg/L per month", "Chemistry",
        "Electrochemistry and batteries",
        "Amperometric reduction of HOCl at a carbon working electrode (Pan et al. 2015; pencil graphite electrodes, PLOS ONE 2021); long-term field "
        "drift of low-cost sensors is reported in Water Science and Technology (2025), not checked in full",
        "Response within known science; the drift that R1 and R10 allow (about 0.15 mg/L per month with the shared photometer, WWT-CAL-001 E12; 0.13 before the decisions of 2026-10-25) is unverified", PLAUSIBLE, closed_by="")
c.claim("S13", "The chlorine error budget meets the PR-001 target at 0.5 mg/L and pH 7.5 before drift", "Chemistry", "Analytical",
        "Root sum of squares of the DPD reference 0.07 mg/L, pH change between visits on the HOCl fraction and temperature residual, with the stale-water "
        "bias added linearly (independent review); the HOCl fraction is corrected for the measured temperature through pKa(T)",
        round(CAL.budget_span(0.5, 7.5, 0.2, 0.5, CAL.REF, 0.0), 3), 0.2, "mg/L", closed_by="WWT-CAL-001 E4, E9")
w9 = CAL.w_corr
c.cited("S31", "The chlorine error budget meets the PR-001 target at 1.5 mg/L at every pH", "Chemistry", "Analytical",
        "Corrected budget as S13 (independent review): at 1.5 mg/L the pH terms dominate; a one-point calibration at 0.5 mg/L carries the reference error as a relative error at 1.5 mg/L. PR-001 restated by Amish on 2026-10-25 as +/-30 % above 1.0 mg/L (WWT-DEC-001 O5), with the shared DPD photometer (+/-0.03 mg/L +/-3 %) as the monthly reference (O2)",
        f"{CAL.n_corr} of 8 cases met calibrated at the reading level; worst FC {w9[0]} mg/L pH {w9[1]}: +/-{w9[2]:.3f} against +/-{CAL.r1_target(w9[0]):.3f} mg/L; "
        f"with the photometer and calibrated at 0.5 mg/L where worse, {CAL.n12} of 8 (WWT-CAL-001 E12; worst +/-{CAL.w12[2]:.3f} against +/-{CAL.r1_target(CAL.w12[0]):.3f} mg/L)",
        WITHIN if CAL.n12 == 8 else FIX, closed_by="WWT-DEC-001 O2 and O5 (decided by Amish 2026-10-25); WWT-CAL-001 E11, E12")
c.cited("S32", "The membrane-free sensor's current does not depend on the flow past it", "Chemistry", "Electrochemistry and batteries",
        "Amperometric currents depend on mass transport, so on flow; the pressure-compensating regulator holds the flow above 0.7 bar, but at 0.5 bar it is 30 % lower (independent review)",
        "Flow dependence of this sensor unknown; read at the end of the flush at a held flow; to measure at TRL 4", PLAUSIBLE, closed_by="")
c.cited("S36", "The three-electrode sensor works in low-conductivity water", "Chemistry", "Electrochemistry and batteries",
        "Below about 50 uS/cm the solution resistance between the electrodes grows and the potentiostat loses control (independent review)",
        "Conductivity of candidate sources to survey; a conductivity floor to set at TRL 4", PLAUSIBLE, closed_by="")
c.cited("S14", "A silver/silver chloride pseudo-reference stays stable in low-chloride drinking water", "Chemistry", "Electrochemistry and batteries",
        "The Ag/AgCl potential follows the chloride activity (Nernst); without a filled reference chamber it moves with the water's chloride",
        "Potentiostat holds the working electrode against it; drift of the reference adds to S12; to measure at TRL 4", PLAUSIBLE, closed_by="")
c.cited("S27", "Flushed water (18 L/day at up to 2 mg/L free chlorine) to the tapstand basin is environmentally negligible", "Chemistry",
        "Environmental and atmospheric chemistry",
        "Mass balance: 36 mg of chlorine a day (40 mg at the regulator tolerance), the same water the tap already delivers to the basin; option A adds no reagent, "
        "unlike option B, whose drain must go to a soakaway (B5)",
        "Same water as the tap; no reagent added", WITHIN, closed_by="WWT-CAL-001 D2")
c.cited("S28", "PVC, ASA, EPDM, polycarbonate and stainless parts withstand 0.2 to 2 mg/L free chlorine and outdoor sun", "Chemistry",
        "Materials and polymer chemistry",
        "These materials are used in chlorinated water and outdoors at these levels; ASA and polycarbonate are UV-stabilised grades; EPDM is preferred "
        "over nitrile in chlorinated water", "Wetted parts drain to waste behind a check valve, so taste and leaching do not reach users; grades to confirm",
        WITHIN, closed_by="WWT-PRC-001, Main components")

# ------------------------------------------------------------------------------------------ option A: biology
c.cited("S22", "A monthly wipe keeps the cell windows and the chlorine electrode clean enough", "Biology", "Microbiology",
        "Biofilm and particle fouling of optical windows and electrodes in drinking water grows over weeks; residual chlorine slows it",
        "Rate at a turbid site unknown; to observe at TRL 4 and in field trials", PLAUSIBLE, closed_by="")
c.cited("S23", "Alert thresholds of 0.2 mg/L free chlorine and 5 NTU match field guidance for the point of delivery", "Biology", "Epidemiology",
        "WHO guidance as summarised for field use: at least 0.2 mg/L free chlorine at the point of delivery; chlorination loses effect as turbidity rises, "
        "markedly above about 10 NTU, so the 5 NTU alert is the earlier warning; the device reports measurements only (PR-013)",
        "Defaults decided by Amish (WWT-DDR-001 D6); at 0.2 mg/L the budget is about +/-0.08 mg/L, so a reading of 0.2 means about 0.12 to 0.28 (WWT-CAL-001 E3)", WITHIN,
        closed_by="WWT-PRB-001; WWT-DDR-001 D6")
c.cited("S24", "Calibration chemicals are handled safely by a caretaker", "Biology", "Toxicology",
        "DPD is harmful if swallowed and can sensitise skin, so tablets are handled with gloves and tested water goes to the drain, not back to a container; "
        "formazin is made from toxic precursors (hydrazine sulfate, hexamethylenetetramine), so only prepared, stabilised standards are used",
        "Rule in WWT-PRC-001 Safety and the build plan; disposal with the operator", WITHIN, closed_by="WWT-PRC-001, Safety")
c.cited("S25", "The enclosure (1.17 to 1.43 m) and the cell (0.81 to 0.90 m) sit within standing working reach; the panel is cleaned from the ground", "Biology", "Ergonomics",
        "Comfortable standing work and reach heights for adults lie about 0.8 to 1.5 m (anthropometric tables, Pheasant and Haslegrave, Bodyspace); "
        "the panel at 2.16 m is out of reach for small adults (independent review), so it is wiped with a long-handled brush",
        "Heights from the model; the 30 min monthly visit is a task analysis (WWT-CAL-001 J3)", WITHIN, closed_by="cad/src/model.py; WWT-CAL-001 J3")
c.cited("S33", "The water-filled cell survives a 0 degC night", "Physics", "Heat transfer",
        "At 0 degC air a small exposed volume can fall below freezing by night-sky radiation, and ice expands about 9 % (independent review)",
        "Freezing margin not shown; at sites near 0 degC drain the cell for the cold season or insulate it; to assess with the partner", PLAUSIBLE, closed_by="")
c.cited("S34", "The temperature probe reads the water to +/-0.5 degC", "Physics", "Heat transfer",
        "The DS18B20 is +/-0.5 degC; it is read after a flush of four cell volumes of supply water, but the black cell heats in the sun between flushes (independent review)",
        "Sun-heating bias of the reading to measure at TRL 4", PLAUSIBLE, closed_by="")
c.claim("S37", "Closing the valve at 4 bar does not overstress the sample line", "Physics", "Fluid mechanics",
        f"Joukowsky surge dp = rho a v, tube velocity {CAL.v_tube_ms:.2f} m/s, wave speed about 350 m/s in small PE tube (estimate): {CAL.dp_hammer:.1f} bar on top of 4 bar, "
        "against about 10 bar for 1/4 in PE tube (typical rating, BOM line 14)", round(4 + CAL.dp_hammer, 1), 10.0, "bar", closed_by="WWT-CAL-001 D9")

# ------------------------------------------------------------------------------------------ option A: mathematics and engineering
c.claim("S26", "The hot-day enclosure simulation uses a stable, converged time step", "Mathematics", "Numerical method",
        "Explicit Euler is stable and within about 4 % of the exact first-order response for dt / tau below 0.1 (dt 60 s)",
        round(60.0 / CAL.tau, 3), 0.1, "dt / tau", closed_by="WWT-CAL-001 C3, C4")
c.order_of_magnitude("S19", "One LTE-M upload, network attach included, costs about 20 mWh", "Engineering and technology", "Power and link budgets",
                     claimed=CAL.E_UPLOAD * 1000, estimate=0.15 * 3.8 * 140 / 3.6,
                     unit="mWh", law="SIM7000-class modem: about 150 mA at 3.8 V for the same 140 s per attach and post that S21 assumes (independent review)", closed_by="WWT-CAL-001 A2")
c.claim("S20", "Uploads stay under 1 MB a month", "Engineering and technology", "Power and link budgets",
        "Six sessions a day of 780 B payload; with TLS session resumption about 1.2 kB overhead; a full handshake every session (about 6 kB) would give "
        "1.22 MB (independent review), so the firmware keeps sessions", round(CAL.UPLOADS * 30 * (CAL.payload + 1200) / 1e6, 2), 1.0, "MB/month",
        closed_by="WWT-DEC-001 F7; WWT-CAL-001 G1, G3")
c.claim("S21", "An SMS leaves within 15 min of a confirmed crossing, with three tries", "Engineering and technology", "Control",
        "Attach 120 s and send 20 s per try, 3 min between tries; the firmware bounds each try at 140 s; from the event itself, with retries, up to 92 min (H4)",
        round(CAL.worst / 60, 1), 15.0, "min", closed_by="WWT-CAL-001 H1, H4")
c.cited("S15", "The latching valve opens at every supply pressure from 0.5 to 4 bar", "Engineering and technology", "Standards practice",
        "A direct-acting solenoid valve needs no minimum pressure difference (a pilot-operated valve needs about 0.2 to 0.5 bar), but a small direct-acting valve "
        "has a maximum opening differential (independent review)", "BOM line 13 specifies direct acting and rated to open against at least 4 bar; to confirm in the datasheet",
        WITHIN, closed_by="WWT-CAL-001 D7; WWT-DEC-001 F6")

# ------------------------------------------------------------------------------------------ option B: reagent colorimetric analyser
c.cited("B1", "DPD colorimetry reads free chlorine from 0 to 2 mg/L in a 12 mm cuvette", "Chemistry", "Analytical",
        "DPD reacts with free chlorine to a magenta colour read near 515 nm (ISO 7393-2; EPA 330.5 adaptations in commercial photometers)",
        "Standard method; used by field photometers and online analysers", WITHIN, closed_by="WWT-OPT-001")
c.cited("B2", "DPD and buffer reagents keep their strength for a month at up to 50 degC in the cabinet", "Chemistry", "Physical (kinetics, equilibria, thermochemistry)",
        "Liquid DPD indicator oxidises and darkens with heat and air; suppliers give shelf lives at room temperature",
        "Shelf life at 50 degC unknown; to assess with a supplier", PLAUSIBLE, closed_by="")
c.balance("B3", "80 mL of each reagent lasts 90 days at 0.03 mL per test and 24 tests a day", "Mathematics", "Units and dimensional analysis",
          inputs={"bottle": 80.0}, outputs={"90 days of tests": 0.03 * 24 * 90}, unit="mL", law="Mass balance of reagent", closed_by="WWT-OPT-001")
c.order_of_magnitude("B4", "The analyser needs about 0.8 Wh/day, within the 5 W panel", "Engineering and technology", "Power and link budgets",
                     claimed=0.8, estimate=(CAL.e_base + 24 * (2 * 0.5 * 5 + 0.3 * 30) / 3600) * CAL.MARGIN, unit="Wh/day",
                     law="Option A's budget plus two 0.5 W pumps for 5 s and a 0.3 W stirrer for 30 s per test")
c.cited("B5", "Reacted sample with DPD and phosphate buffer can go to a soakaway", "Biology", "Toxicology",
        "About 1.5 mL of reagent a day in 18 L of water; DPD (N,N-diethyl-p-phenylenediamine) is harmful if swallowed, so the drain must not reach "
        "the basin users fill from", "Drain to a soakaway, not the basin; to assess with the operator", PLAUSIBLE, closed_by="")
c.cited("B6", "The same 860 nm LED and 90 degree detector read turbidity in the cuvette before the reagent goes in", "Physics", "Optics and radiation",
        "Nephelometry as S10", "Same principle as option A", WITHIN, closed_by="WWT-OPT-001")

# ------------------------------------------------------------------------------------------ option C: in-riser probe manifold
c.cited("C1", "ORP and pH electrodes estimate free chlorine within the R1 target", "Chemistry", "Electrochemistry and batteries",
        "ORP follows the log of the HOCl activity and the pH, and other redox couples move it; it is used as a control signal, and tracks chlorine "
        "only loosely in the 0.2 to 2 mg/L range", "Principle known; meeting +/-0.2 mg/L unlikely without frequent calibration", PLAUSIBLE, closed_by="")
p_bar = 4.0e5
F_probe = p_bar * math.pi / 4 * 0.012 ** 2
c.claim("C2", "A 12 mm probe in a compression gland holds against 4 bar", "Physics", "Mechanics and statics",
        "Push-out force = p x pi d^2 / 4 at 4 bar; small PVC compression glands hold well over 100 N (to confirm in the gland datasheet)",
        round(F_probe, 1), 100.0, "N", closed_by="WWT-OPT-001")
c.cited("C3", "Probes in the riser read the water people draw, without flushing", "Physics", "Fluid mechanics",
        "While the tap runs, the riser carries the supply water; between draws the water stands in the pipe and the reading is of stale water",
        "Readings valid only during draws (a paddle flow switch wakes the unit); no reading at night when nobody draws", WITHIN, closed_by="WWT-OPT-001")
c.cited("C4", "Insertion turbidity in the running pipe is not upset by bubbles and daylight", "Physics", "Optics and radiation",
        "Entrained air from a tap opening scatters light like particles; the opaque manifold keeps daylight out",
        "Bubble bias in flowing water unknown; to assess", PLAUSIBLE, closed_by="")
c.order_of_magnitude("C5", "With no valve and no flush the manifold needs about 0.4 Wh/day", "Engineering and technology", "Power and link budgets",
                     claimed=0.4, estimate=(CAL.e_up + CAL.e_sleep + CAL.e_status + 24 * 0.264 * 20 / 3600) * CAL.MARGIN, unit="Wh/day",
                     law="Uploads, sleep and status light as option A, plus 24 wake-ups of 20 s at 0.264 W")
c.cited("C6", "Cutting the riser and fitting two unions keeps the tapstand watertight and serviceable", "Engineering and technology", "Standards practice",
        "Threaded unions on 25 mm galvanised pipe are standard plumbing; it changes the tapstand, which the problem statement rules out",
        "Within known science; conflicts with the PRB constraint of one tee only", WITHIN, closed_by="WWT-OPT-001")

if __name__ == "__main__":
    print(f"Record of the fix: battery as first specified (1S2P 32700, 6 Ah) mismatched its cells by {mismatch_old * 100:.0f} % "
          f"(two 6 Ah cells hold 12 Ah); fixed to one cell (WWT-DEC-001 F1), mismatch {mismatch * 100:.0f} %")
    c.write()
