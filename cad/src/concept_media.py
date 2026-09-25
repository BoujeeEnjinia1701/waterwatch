"""WaterWatch concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Z up, ground at Z = 0. The existing public tapstand (grey, no BOM
number) stands at the origin; WaterWatch mounts on its own pole beside it and draws a
small hourly sample from a tee on the tapstand riser.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all


def tube(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    s = None
    for p, q in zip(points, points[1:]):
        t = tube(p, q, r)
        s = t if s is None else s + t
    return s


# ---------------- existing tapstand (context, grey) ----------------
PLINTH = 150.0
tapstand = (Pos(0, 0, PLINTH / 2) * Box(700, 700, PLINTH)                       # concrete apron
            - Pos(0, 0, PLINTH - 20) * Box(560, 560, 41))                        # shallow basin
tapstand = tapstand + Pos(0, 0, PLINTH - 20 + 10) * Box(560, 560, 20)            # basin floor
riser = tube((0, 0, 0), (0, 0, 950), 17)                                          # 25 mm GI riser
tap = (tube((0, 0, 950), (0, -130, 950), 14) + tube((0, -130, 950), (0, -130, 890), 11)
       + Pos(0, 0, 990) * Cylinder(10, 60))
tapstand = tapstand + riser + tap

# ---------------- WaterWatch ----------------
POLE_X, POLE_Y = 470.0, 70.0
# 1 Mounting pole, 48 mm galvanized tube, with U-bolt clamps
pole = Pos(POLE_X, POLE_Y, 1050) * Cylinder(24, 2100)
clamps = None
for z in (905, 1210, 1390, 2060):
    c = Pos(POLE_X, POLE_Y, z) * (Cylinder(32, 22) - Cylinder(24, 24))
    clamps = c if clamps is None else clamps + c
pole = pole + clamps

# 2 Solar panel, 5 W (about 250 x 190 mm), tilted 30 degrees, facing -Y
panel = Pos(POLE_X, POLE_Y - 20, 2160) * Rot(30, 0, 0) * Box(250, 190, 18)
panel_bracket = tube((POLE_X, POLE_Y, 2080), (POLE_X, POLE_Y - 20, 2150), 12)
panel = panel + panel_bracket

# Electronics enclosure, 200 (X) x 120 (Y) x 260 (Z) mm, on the -Y face of the pole
EX, EY, EZ = POLE_X, 0.0, 1300.0
W, D, H, T = 200.0, 120.0, 260.0, 3.0
LID_T = 12.0
# 3 Enclosure base (open to -Y), with cable glands on the underside
base = Pos(EX, EY + LID_T / 2, EZ) * (Box(W, D - LID_T, H) - Pos(0, -T, 0) * Box(W - 2 * T, D - LID_T, H - 2 * T))
for gx in (-50, 0, 50):
    base = base + Pos(EX + gx, EY + 10, EZ - H / 2 - 8) * Cylinder(9, 16)
# 4 Enclosure lid with gasket
lid = Pos(EX, EY - D / 2 + LID_T / 2, EZ) * (Box(W, LID_T, H) - Pos(0, 3, 0) * Box(W - 2 * T, LID_T, H - 2 * T))
BACK = EY + D / 2 - T                      # inner face of the back wall
# 5 LiFePO4 battery, 2 x 32700 cells in parallel with protection board
battery = Pos(EX - 45, BACK - 22, EZ - 55) * Box(80, 40, 130)
# 6 Controller board (ESP32, solar charger, potentiostat front end, microSD)
board = Pos(EX + 45, BACK - 8, EZ + 20) * Box(90, 12, 120)
# 7 Cellular modem (LTE-M or NB-IoT with 2G fallback)
modem = Pos(EX - 45, BACK - 8, EZ + 75) * Box(70, 12, 55)
# 8 External antenna on the enclosure top
antenna = Pos(EX + 60, EY + 10, EZ + H / 2 + 70) * Cylinder(9, 140)

# Flow-through cell below the enclosure, 120 (X) x 60 (Y) x 90 (Z), opaque; about 0.37 L inside
FX, FY, FZ = POLE_X, 0.0, 850.0
FW, FD, FH, FT = 120.0, 60.0, 90.0, 8.0
# 9 Flow-through cell body (open cavity so the sensors show in the cutaway)
cell = Pos(FX, FY, FZ) * (Box(FW, FD, FH) - Pos(0, 0, FT / 2) * Box(FW - 2 * FT, FD - 2 * FT, FH - FT))
cell = cell + Pos(FX, FY, FZ + FH / 2 + 5) * (Box(FW, FD, 10) - Pos(-28, 12, 0) * Cylinder(8, 12)
                                             - Pos(26, 12, 0) * Cylinder(5, 12))      # top plate
cell = cell + Pos(FX, FY + 4, FZ - 5) * Box(6, FD - 2 * FT - 8, FH - 30)            # baffle
# 10 Turbidity head: 860 nm IR LED and 90 degree detector in a dark side block
turb = Pos(FX - FW / 2 - 16, FY, FZ - 12) * Box(32, 50, 50)
# 11 Free chlorine sensor (membrane-free three-electrode cell), from the top
chlorine = Pos(FX - 28, FY + 12, FZ + 40) * Cylinder(8, 140)
# 12 Temperature probe (DS18B20 in a stainless sheath), from the top
temp = Pos(FX + 26, FY + 12, FZ + 45) * Cylinder(4, 100)

# 13 Latching solenoid valve, 12 V, on the sample line
VX, VZ = 230.0, 500.0
valve = Pos(VX, 0, VZ) * Box(55, 45, 60) + Pos(VX, 0, VZ + 45) * Cylinder(17, 35)
# 14 Sample line: tee on the riser, strainer, restrictor and 6 mm tube to the cell inlet
tee = Pos(0, 0, VZ) * Cylinder(24, 60) + tube((17, 0, VZ), (60, 0, VZ), 12)
sample = tee + path([(60, 0, VZ), (VX - 28, 0, VZ)], 5) + Pos(120, 0, VZ) * Rot(0, 90, 0) * Cylinder(12, 50) \
    + path([(VX + 28, 0, VZ), (FX - FW / 2 + 20, 0, VZ), (FX - FW / 2 + 20, 0, FZ - FH / 2 - 1)], 5)
# 15 Drain hose from the cell outlet to the tapstand basin
drain = path([(FX + 40, -15, FZ - FH / 2), (FX + 40, -15, 350), (FX + 40, -230, 170), (240, -230, 170)], 8)
# 16 Cables, glands and fuse: cell and panel leads into the enclosure
cables = (path([(FX - 20, FY + 25, FZ + FH / 2 + 10), (FX - 20, FY + 25, EZ - H / 2 - 16)], 4)
          + path([(FX + 60, 55, 2090), (FX + 60, 55, EZ + H / 2 + 5)], 4))

GREY = "#B6BCC4"
# The kit's cutaway cutter is centred on the origin, so shift the whole scene to put the
# enclosure and flow cell near the origin. Ground ends up at Z = -1100; nothing else changes.
SHIFT = Pos(-POLE_X, 0, -1100)
parts = [
    Part("Existing tapstand (not in BOM)", SHIFT * tapstand, GREY, None),
    Part("Mounting pole and clamps", SHIFT * pole, "#8A9299", 1, (0, 0, 0)),
    Part("Solar panel, 5 W, with bracket", SHIFT * panel, "#1E3A8A", 2, (0, 0, 300)),
    Part("Enclosure base, IP66", SHIFT * base, "#D1D5DB", 3, (320, 0, 0)),
    Part("Enclosure lid and gasket", SHIFT * lid, "#E5E7EB", 4, (0, -380, 0)),
    Part("LiFePO4 battery, 6 Ah", SHIFT * battery, "#C2410C", 5, (680, 0, -160)),
    Part("Controller board", SHIFT * board, "#0F766E", 6, (680, 0, 110)),
    Part("Cellular modem", SHIFT * modem, "#7C3AED", 7, (900, 0, 120)),
    Part("Antenna", SHIFT * antenna, "#111827", 8, (320, 0, 160)),
    Part("Flow-through cell", SHIFT * cell, "#475569", 9, (320, 0, -160)),
    Part("Turbidity head, 860 nm", SHIFT * turb, "#D4A017", 10, (150, 0, -200)),
    Part("Free chlorine sensor", SHIFT * chlorine, "#2563EB", 11, (320, 0, 60)),
    Part("Temperature probe", SHIFT * temp, "#16A34A", 12, (450, 0, 20)),
    Part("Latching solenoid valve", SHIFT * valve, "#115E59", 13, (0, -250, 150)),
    Part("Sample line, tee and strainer", SHIFT * sample, "#0EA5E9", 14, (0, 0, 0)),
    Part("Drain hose", SHIFT * drain, "#6B7280", 15, (320, 0, -160)),
    Part("Cables, glands and fuse", SHIFT * cables, "#A16207", 16, (0, 250, 0)),
]

render_all(
    parts, project="WaterWatch", title="Tapstand water quality sentinel concept", dwg_no="WWT-DWG-010",
    date="2026-09-25",
    key_figures=["Free chlorine 0 to 2 mg/L, turbidity 0 to 100 NTU, temperature",
                 "Hourly 90 s flush and reading; about 18 L/day to drain (estimate)",
                 "About 0.5 Wh/day; about 30 days on battery (estimate)",
                 "5 W panel, 3.2 V 6 Ah LiFePO4; cellular with SMS alerts",
                 "About $270 in parts (indicative)"],
    cut_exclude=("Existing tapstand (not in BOM)", "Mounting pole and clamps", "Solar panel, 5 W, with bracket",
                 "Drain hose", "Sample line, tee and strainer", "Latching solenoid valve", "Antenna",
                 "Cables, glands and fuse"),
    flow={"title": "sample and data flow (estimated values)", "unit": "",
          "stages": [("Water at the tap", "tee on the riser"), ("Solenoid valve", "90 s flush, hourly"),
                     ("Flow-through cell", "about 0.75 L per flush"), ("Controller", "log, 90 days on card"),
                     ("Cellular modem", "report every 4 h"), ("Caretaker, operator", "SMS alert, 15 min")],
          "losses": [(2, "Flushed sample to drain, L per reading (estimate)", 0.75)]},
)
