"""WaterWatch sizing calculations, WWT-CAL-001 v0.2 (TRL 3; R1, R5, R11 and R12 updated for WWT-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[A3] that the note cites. Geometry comes from cad/src/model.py (PARAMS and derived), the
parts cost from bom/bom.csv and the budget from project.yaml. First-principles estimates
for a paper proof of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)


def tag(t, text):
    print(f"[{t}] {text}")


# ------------------------------------------------------------------ assumptions
V_SYS = 3.3            # V, logic rail
I_AWAKE = 0.080        # A average while awake (ESP32-S3 active, sensors, LED pulses)
T_FLUSH = 90.0         # s valve open
T_READ_CL = 10.0       # s chlorine averaging window at the end of the flush
T_SETTLE = 30.0        # s wait after the valve closes (was 10 s at TRL 2; see section F)
T_READ_T = 5.0         # s turbidity reading
T_LOG = 5.0            # s temperature, logging, housekeeping
I_SLEEP = 50e-6        # A sleep floor incl. potentiostat bias, charger and protection board
E_UPLOAD = 0.020       # Wh per upload incl. network attach (LTE-M or NB-IoT)
UPLOADS = 6            # per day (every 4 h)
VALVE = (12.0, 0.5, 0.050, 0.80)   # V, A, s per pulse, boost efficiency; 2 pulses per reading
MARGIN = 1.5           # alerts, retries, cold weather
READINGS = 24          # per day at the default hourly schedule
CELLS = (3.2, 6.0)     # V, Ah: 1S2P 32700 LiFePO4
DOD = 0.80             # usable fraction
COLD = 0.85            # capacity factor at 0 degC
PANEL_W = 5.0
PSH = 4.5              # peak sun hours, clear day
PSH_WET = 2.5          # peak sun hours, overcast rainy-season day
DERATE = 0.60          # heat, dust, angle, small-charger losses

print("WaterWatch sizing, WWT-CAL-001 v0.2")
print(f"Geometry from cad/src/model.py: cell cavity {P['cell_in']} mm, enclosure {P['enc']} mm, pole {P['pole_od']} x {P['pole_wall']} mm")

# ------------------------------------------------------------------ A. Energy (R7, R4)
print("\nA. Daily energy")
t_awake = T_FLUSH + T_SETTLE + T_READ_T + T_LOG
e_read = V_SYS * I_AWAKE * t_awake / 3600
e_meas = e_read * READINGS
e_up = E_UPLOAD * UPLOADS
e_sleep = I_SLEEP * V_SYS * 24
v, i, t, eta = VALVE
e_valve = 2 * v * i * t / eta / 3600 * READINGS
e_base = e_meas + e_up + e_sleep + e_valve
e_day = e_base * MARGIN
tag("A1", f"awake {t_awake:.0f} s per reading at {V_SYS * I_AWAKE:.3f} W: {e_read * 1000:.2f} mWh per reading, {e_meas:.3f} Wh/day")
tag("A2", f"uploads {UPLOADS} x {E_UPLOAD * 1000:.0f} mWh = {e_up:.3f} Wh/day; sleep {e_sleep * 1000:.1f} mWh/day; valve {e_valve * 1000:.1f} mWh/day")
tag("A3", f"sum {e_base:.3f} Wh/day; with {MARGIN:.1f} margin {e_day:.3f} Wh/day ({e_day / 24 * 1000:.1f} mW average)")
e_2g = (e_meas + 4 * e_up + e_sleep + e_valve) * MARGIN
tag("A4", f"2G-only site (uploads cost 4 x as much): {e_2g:.3f} Wh/day")
e_15 = ((e_read + 2 * v * i * t / eta / 3600) * 96 + e_up + e_sleep) * MARGIN
tag("A5", f"15 min schedule (R4 minimum interval): {e_15:.3f} Wh/day")

# ------------------------------------------------------------------ B. Battery and solar (R7)
print("\nB. Battery autonomy and solar recharge")
e_bat = CELLS[0] * CELLS[1]
e_use = e_bat * DOD
aut = e_use / e_day
aut_cold = e_use * COLD / e_day
tag("B1", f"battery {e_bat:.1f} Wh, usable {e_use:.2f} Wh; autonomy {aut:.1f} days ({aut_cold:.1f} days at 0 degC); 2G-only {e_use / e_2g:.1f} days; 15 min schedule {e_use / e_15:.1f} days")
y_clear = PANEL_W * PSH * DERATE
y_wet = PANEL_W * PSH_WET * DERATE
tag("B2", f"panel yield {y_clear:.1f} Wh per clear day, {y_wet:.1f} Wh per overcast day")
tag("B3", f"recharge from empty: {e_use / (y_clear - e_day):.2f} clear days, {e_use / (y_wet - e_day):.2f} overcast days")
p_min = (e_use / 3 + e_day) / (PSH_WET * DERATE)
tag("B4", f"smallest panel that refills in 3 overcast days: {p_min:.1f} W; charge current at full sun about {PANEL_W * 0.85 / 3.4:.2f} A ({PANEL_W * 0.85 / 3.4 / CELLS[1]:.2f} C)")

# ------------------------------------------------------------------ C. Enclosure temperature (R9)
print("\nC. Enclosure temperature in full sun")
ew, ed, eh = (x / 1000 for x in P["enc"])
A_tot = D["enc_area_m2"]
A_exp = A_tot - ew * eh                      # back face against the mounting plate
H_COMB = 10.0                                # W/m2K convection plus radiation, light wind
DNI, DIFF = 900.0, 100.0


def absorbed(el_deg, alpha, top_shaded=False):
    el = math.radians(el_deg)
    if el <= 0:
        return 0.0
    top = 0.0 if top_shaded else ew * ed * math.sin(el)
    front = ew * eh * math.cos(el)           # sun square to the front face (worst azimuth)
    diffuse = ew * ed + (ew * eh + 2 * ed * eh) / 2
    return alpha * (DNI * (top + front) + DIFF * diffuse)


tag("C1", f"enclosure area {A_tot:.4f} m2, exposed {A_exp:.4f} m2, loss coefficient {H_COMB * A_exp:.2f} W/K")
for alpha, label in ((0.45, "light grey, clean"), (0.70, "dusty or weathered")):
    q = absorbed(60, alpha)
    qs = absorbed(60, alpha, top_shaded=True)
    tag("C2", f"alpha {alpha} ({label}), sun at 60 deg: {q:.1f} W absorbed, rise {q / (H_COMB * A_exp):.1f} K ({qs / (H_COMB * A_exp):.1f} K with the top shaded by the panel)")
C_TH = 0.9 * 1200 + 0.29 * 1000 + 0.10 * 900  # J/K: enclosure, cells, boards and brackets
tau = C_TH / (H_COMB * A_exp)
tag("C3", f"thermal mass {C_TH:.0f} J/K, time constant {tau / 60:.0f} min (quasi-steady within the hour)")

SHIELD = 0.25   # fraction of solar gain reaching the enclosure under the ventilated shield (item 17), assumed


# clear day: ambient sinusoid between t_lo and t_hi (peak 15:00), sun 06:00 to 18:00, overhead at noon
def hot_day(alpha, shield=1.0, t_lo=30.0, t_hi=45.0):
    dt = 60.0
    T = 30.0
    tmax, hours_ok, e_ok, e_all = 0.0, 0.0, 0.0, 0.0
    yield_norm = sum(max(0.0, math.sin(math.pi * (k / 60 - 6) / 12)) for k in range(24 * 60)) / 60
    for day in range(2):
        for k in range(24 * 60):
            h = k / 60
            ta = (t_lo + t_hi) / 2 + (t_hi - t_lo) / 2 * math.sin(2 * math.pi * (h - 9) / 24)
            s = math.sin(math.pi * (h - 6) / 12) if 6 < h < 18 else 0.0
            el = 90 * s
            q = absorbed(el, alpha) * shield
            T += dt / tau * (ta + q / (H_COMB * A_exp) - T)
            if day == 1:
                tmax = max(tmax, T)
                pv = y_clear * max(0.0, s) / yield_norm / 60     # Wh this minute
                e_all += pv
                if 0.0 < T < 45.0:
                    hours_ok += (1 / 60) if s > 0 else 0
                    e_ok += pv
    return tmax, hours_ok, e_ok, e_all


hot = {}
for (t_lo, t_hi) in ((30.0, 45.0), (22.0, 35.0)):
    for alpha, shield, label in ((0.45, 1.0, "clean, no shield"), (0.70, 1.0, "dusty, no shield"),
                                 (0.45, SHIELD, "clean, with shield"), (0.70, SHIELD, "dusty, with shield")):
        tmax, hok, eok, eall = hot_day(alpha, shield, t_lo, t_hi)
        hot[(t_hi, label)] = (tmax, hok, eok)
        tag("C4", f"{t_lo:.0f} to {t_hi:.0f} degC day, {label}: peak inside {tmax:.1f} degC; charging allowed {hok:.1f} sun hours, "
                  f"{eok:.1f} of {eall:.1f} Wh ({eok / e_day:.1f} x the daily need)")

# ------------------------------------------------------------------ D. Sample flow and flushing (R8, R1)
print("\nD. Sample flow, flushing and water use")
Q = 0.5                                        # L/min nominal
v_cell = D["cell_net_l"]
v_tube = D["tube_vol_l"]
tag("D1", f"cell water volume {v_cell:.3f} L (model; TRL 2 cell was 0.37 L); sample tube {D['tube_l_mm']:.0f} mm, {v_tube * 1000:.1f} mL")
v_flush = Q * T_FLUSH / 60
tag("D2", f"flush {v_flush:.2f} L per reading, {v_flush * READINGS:.1f} L/day nominal")


def stale(q_lpm, t_s):
    """Fraction of old water left in a well-mixed cell after the tube is flushed."""
    v = q_lpm * t_s / 60 - v_tube
    return math.exp(-max(v, 0) / v_cell)


t_cl = T_FLUSH - T_READ_CL
tag("D3", f"stale fraction at the start of the chlorine window ({t_cl:.0f} s): {stale(Q, t_cl) * 100:.1f} %, at the end: {stale(Q, T_FLUSH) * 100:.1f} % "
          f"(TRL 2 cell of 0.37 L: {math.exp(-(Q * t_cl / 60 - v_tube) / 0.37) * 100:.1f} %)")
# supply pressure 0.5 to 4 bar: fixed orifice vs pressure-compensating regulator
for p_bar in (0.5, 1.0, 2.0, 4.0):
    q_or = 0.5 * math.sqrt(p_bar / 1.0)       # orifice sized for 0.5 L/min at 1 bar
    tag("D4", f"fixed orifice at {p_bar:.1f} bar: {q_or:.2f} L/min, {q_or * T_FLUSH / 60 * READINGS:.1f} L/day")
q_hi, q_lo = 0.55, 0.35                         # PC regulator +10 %; below its 0.7 bar threshold at 0.5 bar
tag("D5", f"PC regulator 0.50 L/min +10 %: {q_hi * T_FLUSH / 60 * READINGS:.1f} L/day (R8 limit 20 L); at 0.5 bar about {q_lo:.2f} L/min, stale fraction {stale(q_lo, t_cl) * 100:.1f} %")
tag("D6", f"15 min schedule: {v_flush * 96:.0f} L/day (R8 applies to hourly sampling); tapstand serving 250 people at 20 L: {v_flush * READINGS / 5000 * 100:.2f} % of daily draw")
dp_valve_min = 0.0
tag("D7", f"supply 0.5 bar minimum: valve must be direct acting (minimum differential {dp_valve_min:.1f} bar); pilot valves need about 0.2 to 0.5 bar")

# ------------------------------------------------------------------ E. Free chlorine error budget (R1)
print("\nE. Free chlorine error budget")


def pka(t_c):
    tk = t_c + 273.15
    return 3000.0 / tk - 10.0686 + 0.0253 * tk   # Morris (1966)


def f_hocl(ph, t_c):
    return 1.0 / (1.0 + 10 ** (ph - pka(t_c)))


tag("E1", f"pKa {pka(5):.2f} at 5 degC, {pka(25):.2f} at 25 degC, {pka(40):.2f} at 40 degC")
tag("E2", "HOCl fraction at 25 degC: " + ", ".join(f"pH {ph}: {f_hocl(ph, 25):.2f}" for ph in (6.5, 7.0, 7.5, 8.0, 8.5))
    + f"; over pH 6.5 to 8.5 and 5 to 40 degC: {f_hocl(8.5, 5):.2f} to {f_hocl(6.5, 40):.2f}")
REF = 0.07          # mg/L, DPD comparator reference at calibration (0.05 reading plus 0.05 color, RSS)
TCOEF = 0.025       # per K, assumed sensor temperature coefficient after compensation residual
T_ERR = 0.5         # K, DS18B20
tag("E3", f"reference {REF:.2f} mg/L; temperature residual {TCOEF * T_ERR * 100:.2f} %; stale water {stale(Q, t_cl) * 100:.1f} % (bias low)")


def ph_err(ph, dph, t_c=25):
    return max(abs(f_hocl(ph + s * dph, t_c) / f_hocl(ph, t_c) - 1) for s in (-1, 1))




def r1_target(fc, relaxed=True):
    """R1 target: v0.3 was +/-0.1 mg/L below 1.0 mg/L and +/-15 % above; DDR-002 relaxed it to
    +/-0.2 mg/L or +/-25 %, whichever is greater."""
    if relaxed:
        return max(0.2, 0.25 * fc)
    return 0.10 if fc < 1.0 else 0.15 * fc


def budget(fc, ph, dph, t_c=25):
    rel = math.sqrt(ph_err(ph, dph, t_c) ** 2 + (TCOEF * T_ERR) ** 2 + stale(Q, t_cl) ** 2)
    return math.sqrt(REF ** 2 + (fc * rel) ** 2)


PH_TRIGGER = 7.5     # DDR-002: pH probe variant where site pH is above 7.5 or moves more than 0.2 between visits


def method(ph):
    return (0.1, "pH probe") if ph > PH_TRIGGER else (0.2, "site pH")


rows = []
for fc in (0.5, 1.5):
    for ph in (7.0, 7.5, 8.0, 8.5):
        site, probe = budget(fc, ph, 0.2), budget(fc, ph, 0.1)
        dph, used = method(ph)
        tot = budget(fc, ph, dph)
        tgt, old = r1_target(fc), r1_target(fc, relaxed=False)
        room = math.sqrt(tgt ** 2 - tot ** 2) if tot < tgt else 0.0
        rows.append((fc, ph, used, tot, tgt, room, site, probe, old))
        tag("E4", f"FC {fc} mg/L, pH {ph}: site pH +/-{site:.3f}, pH probe +/-{probe:.3f} mg/L; rule uses {used} (+/-{tot:.3f}) "
                  f"vs relaxed target +/-{tgt:.3f} (v0.3 target +/-{old:.3f}); room for drift {room:.3f} mg/L"
                  + ("" if tot < tgt else "  NOT MET at zero drift"))
n_old = sum(1 for r in rows if r[6] < r[8])
tag("E5", f"v0.3 target with site pH everywhere: {n_old} of {len(rows)} cases met at zero drift (superseded by DDR-002)")
n_new = sum(1 for r in rows if r[3] < r[4])
tag("E6", f"relaxed target with the pH probe rule: {n_new} of {len(rows)} cases met at zero drift; "
          f"site pH alone at pH 8.0 would give +/-{budget(0.5, 8.0, 0.2):.3f} mg/L at 0.5 mg/L against +/-0.200")
hot_rows = []
for fc in (0.5, 1.5):
    for ph in (6.5, 7.0, 7.5, 8.0, 8.5):
        dph, used = method(ph)
        tot = budget(fc, ph, dph, t_c=40)
        hot_rows.append((fc, ph, tot, r1_target(fc)))
worst40 = max(hot_rows, key=lambda r: r[2] / r[3])
tag("E7", f"at 40 degC (pKa {pka(40):.2f}) with the rule, worst case FC {worst40[0]} mg/L pH {worst40[1]}: +/-{worst40[2]:.3f} vs +/-{worst40[3]:.3f} mg/L; "
          f"{sum(1 for r in hot_rows if r[2] < r[3])} of {len(hot_rows)} cases met")
drift_room = min(r[5] for r in rows)
tag("E8", f"smallest room for sensor drift under the rule at 25 degC: {drift_room:.3f} mg/L (was 0.038 mg/L at pH 7.0 only under the v0.3 target)")

# ------------------------------------------------------------------ F. Turbidity: bubbles and settling (R2)
print("\nF. Turbidity reading: bubble clearance and settling")
g = 9.81
H_CELL = P["cell_in"][2] / 1000


def stokes(d, drho, mu):
    return g * d ** 2 * abs(drho) / (18 * mu)


for t_c, mu in ((5, 1.52e-3), (25, 0.89e-3)):
    for d_um in (50, 100, 200):
        vb = stokes(d_um * 1e-6, 1000, mu)
        re = 1000 * vb * d_um * 1e-6 / mu
        tag("F1", f"{t_c} degC, bubble {d_um} um: rise {vb * 1000:.1f} mm/s (Re {re:.2f}), clears the {H_CELL * 1000:.0f} mm cavity in {H_CELL / vb:.0f} s")
vs = stokes(10e-6, 1650, 0.89e-3)
tag("F2", f"10 um silt settles {vs * 1000:.2f} mm/s: {vs * (T_SETTLE + T_READ_T) * 1000:.1f} mm during the {T_SETTLE + T_READ_T:.0f} s wait and read; "
          f"clear layer reaches mid-height after {H_CELL / 2 / vs / 60:.1f} min")
tag("F3", f"settle time raised from 10 s to {T_SETTLE:.0f} s so that 100 um bubbles clear at 5 degC; energy cost {V_SYS * I_AWAKE * 20 * 24 / 3600 * 1000:.0f} mWh/day")

# ------------------------------------------------------------------ G. Data and storage (R6)
print("\nG. Data and storage")
rec_csv = 64          # bytes per reading as a CSV line
payload = 4 * 120 + 300
overhead = 4000       # TLS, HTTP and network overhead per session (no session resumption)
mb = UPLOADS * 30 * (payload + overhead) / 1e6
tag("G1", f"upload {payload} B payload plus {overhead} B overhead; {mb:.2f} MB per month; with TLS session resumption about {UPLOADS * 30 * (payload + 1200) / 1e6:.2f} MB")
tag("G2", f"90 days on microSD: {90 * READINGS * rec_csv / 1e3:.0f} kB as CSV; 7 day ring buffer in flash: {7 * READINGS * 32 / 1e3:.1f} kB at 32 B per record")

# ------------------------------------------------------------------ H. Alert latency (R5)
print("\nH. Alert latency")
attach_s, sms_s, retry_s, tries = 120, 20, 180, 3
worst = attach_s + sms_s + (tries - 1) * (retry_s + attach_s + sms_s)
tag("H1", f"confirmation to SMS: {attach_s + sms_s} s first try; {worst / 60:.1f} min with {tries} tries at {retry_s / 60:.0f} min spacing (R5 limit 15 min)")
CONFIRM_S = 900    # DDR-002 firmware rule: confirming reading 15 min after a first threshold crossing
tag("H2", f"event onset to SMS worst case: {(2 * 3600 + attach_s + sms_s) / 60:.0f} min with the next hourly reading as confirmation (v0.1); "
          f"{(3600 + CONFIRM_S + attach_s + sms_s) / 60:.0f} min with the 15 min confirming reading (DDR-002)")
e_conf = e_read + 2 * v * i * t / eta / 3600
tag("H3", f"each confirming reading costs {e_conf * 1000:.1f} mWh and {v_flush:.2f} L; ten a month add {10 * e_conf / 30 * 1000:.1f} mWh/day ({10 * e_conf / 30 / e_day * 100:.1f} % of the daily need)")

# ------------------------------------------------------------------ I. Pole and footing in wind
print("\nI. Pole and footing in wind")
V = 35.0
q = 0.5 * 1.2 * V ** 2
pw, ph_, _ = P["panel"]
loads = [("panel", pw * ph_ / 1e6, 1.2, D["panel_z"] / 1000),
         ("enclosure", P["enc"][0] * P["enc"][2] / 1e6, 1.3, P["enc_z"] / 1000),
         ("pole", P["pole_od"] * P["pole_h"] / 1e6, 1.2, P["pole_h"] / 2000)]
F_tot = sum(q * a * cf for _, a, cf, _ in loads)
M = sum(q * a * cf * z for _, a, cf, z in loads)
do, di = P["pole_od"], P["pole_od"] - 2 * P["pole_wall"]
Z = math.pi / 32 * (do ** 4 - di ** 4) / do
sig = M * 1000 / Z
tag("I1", f"{V:.0f} m/s gust, q {q:.0f} Pa: " + "; ".join(f"{n} {q * a * cf:.0f} N at {z:.2f} m" for n, a, cf, z in loads)
    + f"; total {F_tot:.0f} N, base moment {M:.0f} N m")
tag("I2", f"pole {do} x {P['pole_wall']} mm, Z {Z / 1000:.2f} cm3: {sig:.0f} MPa, factor {235 / sig:.1f} on 235 MPa yield")
gam, Kp, Dd, L = 18000.0, 3.0, P["footing_d"] / 1000, P["embed"] / 1000
e = M / F_tot
Hu = 0.5 * gam * Dd * L ** 3 * Kp / (e + L)
tag("I3", f"footing {Dd * 1000:.0f} mm x {L * 1000:.0f} mm in medium sand (Broms, short rigid pile): lateral capacity {Hu:.0f} N, factor {Hu / F_tot:.1f}")

# ------------------------------------------------------------------ J. Install and maintenance tasks (R11, R10)
print("\nJ. Installation and monthly visit, task times")
install = [("dig 300 mm x 600 mm hole", 25, "A"), ("set pole plumb in fast-set concrete", 20, "A"),
           ("concrete sets before loading the pole", 30, "wait"),
           ("shut off supply, fit saddle tee and isolation valve", 20, "B"),
           ("fit strainer, check valve, regulator, valve, run tube", 20, "B"),
           ("mount enclosure, cell and panel", 25, "A"), ("cables and glands", 15, "A"),
           ("drain hose and air break", 10, "B"),
           ("commission: first flush, DPD calibration, site pH, test SMS", 25, "A")]
pm = sum(m for _, m, w in install if w != "wait")
crit = sum(m for n, m, w in install if w in ("A", "wait"))
survey = sum(m for n, m, w in install[:3])
crit_day = crit - survey
tag("J1", f"installation in one visit: {pm} person-minutes; critical path (dig, set, cure, mount, cable, commission) {crit} min against 120 min")
tag("J2", f"DDR-002: footing dug and cast on the survey visit ({survey} min incl. the 30 min set); installation day critical path {crit_day} min "
          f"(mount, cable, commission; plumbing {sum(m for n, m, w in install if w == 'B')} min in parallel) against 120 min")
visit = [("shut isolation valve, open and wipe the cell", 5), ("wipe the chlorine electrode", 5), ("flush and wait", 3),
         ("DPD free chlorine test", 4), ("pH comparator", 3), ("enter calibration from a phone", 4),
         ("check strainer and drain air break", 4), ("wipe panel, look over the site", 2)]
tag("J3", f"monthly visit: {sum(m for _, m in visit)} min against 30 min (" + ", ".join(f"{n} {m}" for n, m in visit) + ")")

# ------------------------------------------------------------------ K. Cost (R12)
print("\nK. Parts cost")
rows_b = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows_b)
budget_usd = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget_usd = float(line.split(":")[1].split("#")[0])
diff = total - budget_usd
tag("K1", f"{len(rows_b)} BOM lines, total ${total:,.2f}; value-engineering target (budget_usd) ${budget_usd:,.0f}: "
    f"${abs(diff):,.2f} {'over' if diff > 0 else 'under'} the target ({abs(diff) / budget_usd * 100:.0f} %)")
PH_VARIANT = (60.0, 100.0)   # USD, pH probe and interface, estimate (not a quote)
tag("K2", f"pH probe variant site (DDR-002): ${total + PH_VARIANT[0]:,.0f} to ${total + PH_VARIANT[1]:,.0f} per unit; the probe is priced per variant site, outside the base-unit budget")

# ------------------------------------------------------------------ L. Results
print("\nL. Requirement status (see Table 4 of the note)")
status = [
    ("R1", "At risk", f"relaxed target met at zero drift in {n_new} of {len(rows)} cases with the pH probe rule; room for drift {drift_room:.2f} mg/L, drift unknown"),
    ("R10", "At risk", f"visit 30 min, at the limit; monthly interval needs drift below about {drift_room:.2f} mg/L per month, unverified"),
    ("R2", "At risk", "bubbles handled by the 30 s wait; fouling in service unknown"),
    ("R9", "At risk", f"with the shield, peak {hot[(45.0, 'dusty, with shield')][0]:.0f} degC inside on a 45 degC day (no shield {hot[(45.0, 'dusty, no shield')][0]:.0f} degC); shield factor assumed"),
    ("R11", "Met on paper", f"installation day critical path {crit_day} min with the footing cast on the survey visit"),
    ("R5", "Met on paper", f"{worst / 60:.0f} min worst confirmation-to-SMS"),
    ("R6", "Met on paper", "under 1 MB per month; 90 days in 138 kB"),
    ("R7", "Met on paper", f"{aut:.0f} days autonomy; {e_use / (y_clear - e_day):.1f} clear days to refill"),
    ("R8", "Met on paper", "18.0 L nominal, 19.8 L at regulator tolerance"),
    ("R12", "Over target" if total > budget_usd else "Met on paper",
     f"${total:,.0f} per base unit against the ${budget_usd:,.0f} value-engineering target"),
    ("R3", "Met by design", "DS18B20 +/-0.5 degC"),
    ("R4", "Met by design", "firmware schedule; energy at 15 min checked"),
    ("R13", "Met by design", "alert wording rule"),
]
for rid, st, why in status:
    tag("L", f"{rid}: {st} ({why})")
counts = {}
for _, st, _ in status:
    counts[st] = counts.get(st, 0) + 1
tag("L", ", ".join(f"{v} {k.lower()}" for k, v in counts.items()))
