"""WaterWatch concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the sentinel parts from cad/src/model.py (PARAMS), adds the existing public tapstand
(grey, no BOM number) as site context, and renders the media set with .kit/concept.py.
Parts are colored and numbered to match bom/bom.csv. Figures on the sheet and in the flow
diagram come from docs/04-calcs/sizing.py (WWT-CAL-001). Not for fabrication.

Coordinates in mm. Z up, ground at Z = 0. The tapstand riser is the Z axis; WaterWatch
stands on its own pole beside it and draws a small hourly sample from a tee on the riser.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Cylinder, Pos  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import PARAMS as P, build_parts, tube  # noqa: E402


def cut_at_cell_plane(parts, keep="+Y"):
    """Like concept.cutaway_parts, but cut on Y = 0, the center plane of the flow cell and the
    enclosure, so the cell cavity and both sensors show (the kit cuts at the mean Y of the parts,
    about 15 mm behind it here). The kit is unchanged."""
    from build123d import Box, Pos
    big = 20000.0
    cutter = Pos(0, big / 2, 0) * Box(big, big, big)
    out = []
    for p in parts:
        s = p.shape & cutter
        if s.volume > 1e-6:
            out.append(Part(p.name, s, p.color, p.bom, p.explode, p.alpha))
    return out


concept.cutaway_parts = cut_at_cell_plane

# ---------------- existing tapstand (context, grey) ----------------
PLINTH = 150.0
tapstand = (Pos(0, 0, PLINTH / 2) * Box(700, 700, PLINTH)                       # concrete apron
            - Pos(0, 0, PLINTH - 20) * Box(560, 560, 41))                        # shallow basin
tapstand = tapstand + Pos(0, 0, PLINTH - 20 + 10) * Box(560, 560, 20)            # basin floor
riser = tube((0, 0, 0), (0, 0, P["riser_h"]), P["riser_od"] / 2)                 # 25 mm GI riser
tap = (tube((0, 0, P["riser_h"]), (0, -130, P["riser_h"]), 14) + tube((0, -130, P["riser_h"]), (0, -130, P["riser_h"] - 60), 11)
       + Pos(0, 0, P["riser_h"] + 40) * Cylinder(10, 60))
tapstand = tapstand + riser + tap

m = build_parts(below_ground=False)

GREY = "#B6BCC4"
# The kit's cutaway cutter is centered on the origin, so shift the whole scene to put the
# enclosure and flow cell near the origin. Ground ends up at Z = -1100; nothing else changes.
SHIFT = Pos(-P["pole_x"], 0, -1100)
parts = [
    Part("Existing tapstand (not in BOM)", SHIFT * tapstand, GREY, None),
    Part("Mounting pole, clamps and plates", SHIFT * m["pole"], "#8A9299", 1, (0, 0, 0)),
    Part("Solar panel, 5 W, with bracket", SHIFT * m["panel"], "#1E3A8A", 2, (0, 0, 300)),
    Part("Enclosure base, IP66", SHIFT * m["enc_base"], "#D1D5DB", 3, (320, 0, 0)),
    Part("Enclosure lid and gasket", SHIFT * m["enc_lid"], "#E5E7EB", 4, (150, -520, 120)),
    Part("LiFePO4 battery, 6 Ah", SHIFT * m["battery"], "#C2410C", 5, (680, 0, -160)),
    Part("Controller board", SHIFT * m["board"], "#0F766E", 6, (680, 0, 110)),
    Part("Cellular modem", SHIFT * m["modem"], "#7C3AED", 7, (900, 0, 120)),
    Part("Antenna", SHIFT * m["antenna"], "#111827", 8, (320, 0, 420)),
    Part("Flow-through cell", SHIFT * m["cell"], "#475569", 9, (480, 0, -250)),
    Part("Turbidity head, 860 nm", SHIFT * m["turb"], "#D4A017", 10, (330, 0, -330)),
    Part("Free chlorine sensor", SHIFT * m["chlorine"], "#2563EB", 11, (480, 0, -20)),
    Part("Temperature probe", SHIFT * m["temp"], "#16A34A", 12, (600, 0, -60)),
    Part("Latching solenoid valve", SHIFT * m["valve"], "#115E59", 13, (0, -250, 150)),
    Part("Sample line, tee and regulator", SHIFT * m["sample"], "#0EA5E9", 14, (0, 0, 0)),
    Part("Drain hose and air break", SHIFT * m["drain"], "#6B7280", 15, (480, 0, -250)),
    Part("Cables, glands and fuse", SHIFT * m["cables"], "#A16207", 16, (0, 250, 0)),
    Part("Sun shield, ventilated", SHIFT * m["shield"], "#F8FAFC", 17, (-420, -300, 250)),
]

render_all(
    parts, project="WaterWatch", title="Tapstand water quality sentinel concept", dwg_no="WWT-DWG-010",
    date="2026-09-25",
    key_figures=["Free chlorine 0 to 2 mg/L, turbidity 0 to 100 NTU, temperature",
                 "Hourly 90 s flush at 0.5 L/min; 18 L/day to drain (WWT-CAL-001)",
                 "About 0.54 Wh/day; about 29 days on battery (WWT-CAL-001)",
                 "5 W panel, 3.2 V 6 Ah LiFePO4, sun shield; cellular with SMS",
                 "$282 in parts (indicative), budget $300"],
    cut_exclude=("Existing tapstand (not in BOM)", "Mounting pole, clamps and plates", "Solar panel, 5 W, with bracket",
                 "Drain hose and air break", "Sample line, tee and regulator", "Latching solenoid valve", "Antenna",
                 "Cables, glands and fuse", "Sun shield, ventilated"),
    flow={"title": "sample and data flow (values from WWT-CAL-001)", "unit": "",
          "stages": [("Water at the tap", "tee on the riser"), ("Regulator and valve", "0.5 L/min, 90 s hourly"),
                     ("Flow-through cell", "0.19 L, 4 volumes a flush"), ("Controller", "log, 90 days on card"),
                     ("Cellular modem", "report every 4 h"), ("Caretaker, operator", "SMS within 13 min")],
          "losses": [(2, "Flushed sample to drain via air break, L per reading", 0.75)]},
)
