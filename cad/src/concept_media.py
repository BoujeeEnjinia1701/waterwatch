"""WaterWatch concept media (TRL 3), generated from the detailed kit 1.9 model (option A).

Run from the repo root:  python cad/src/concept_media.py [all|web]
Takes every part of components(CHOSEN) in cad/src/model.py (option A, WWT-OPT-001), groups the parts by BOM
line (fasteners with the line they belong to, unnumbered fixings with line 20) so the exploded view's numbers
match bom/bom.csv, clips the pole at ground level, adds the existing public tapstand (grey, no BOM number) as
site context and renders the media set with .kit/concept.py. `web` writes only media/model.glb and
media/viewer.html. Figures on the sheet and in the flow diagram come from docs/04-calcs/sizing.py
(WWT-CAL-001). Not for fabrication.

Coordinates in mm. Z up, ground at Z = 0. The tapstand riser is the Z axis; WaterWatch stands on its own pole
beside it and draws a small hourly sample from a tee on the riser.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Compound, Cylinder, Pos  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P, tube  # noqa: E402


CUT_Y = 20.0   # 7 mm in front of the flow cell cavity centre (WWT-DDR-003 moved the cell back on its plate)


def cut_at_cell_plane(parts, keep="+Y"):
    """Like concept.cutaway_parts, but cut on Y = CUT_Y, through the flow cell cavity and the
    enclosure, so the cell cavity and both sensors show (the kit cuts at the mean Y of the parts,
    about 15 mm behind it here). The kit is unchanged."""
    big = 20000.0
    cutter = Pos(0, big / 2 + CUT_Y, 0) * Box(big, big, big)
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

GREY = "#B6BCC4"
# (name, colour, explode) per BOM line, as in the TRL 3 media
LINES = {1: ("Mounting pole, U-bolts and saddles", "#8A9299", (0, 0, 0)), 2: ("Solar panel, 5 W, with bracket", "#1E3A8A", (0, 0, 300)),
         3: ("Enclosure base, IP66", "#D1D5DB", (320, 0, 0)), 4: ("Enclosure lid and gasket", "#E5E7EB", (150, -520, 120)),
         5: ("LiFePO4 battery, one 6 Ah cell", "#C2410C", (680, 0, -160)), 6: ("Controller board", "#0F766E", (680, 0, 110)),
         7: ("Cellular modem", "#7C3AED", (900, 0, 120)), 8: ("Antenna", "#111827", (320, 0, 420)),
         9: ("Flow-through cell", "#475569", (760, 0, -420)), 10: ("Turbidity optics, 860 nm", "#D4A017", (760, -160, -420)),
         11: ("Free chlorine sensor", "#2563EB", (760, 0, -200)), 12: ("Temperature probe", "#16A34A", (900, 0, -240)),
         13: ("Latching solenoid valve", "#115E59", (0, -250, 150)), 14: ("Sample line, tee and regulator", "#0EA5E9", (0, 0, 0)),
         15: ("Drain hose and air break", "#6B7280", (760, 0, -420)), 16: ("Cables, glands and fuse", "#A16207", (0, 250, 0)),
         17: ("Sun shield, ventilated", "#F8FAFC", (-420, -300, 250)), 18: ("Mounting plates", "#A8A29E", (0, 220, 0)),
         19: ("Lugs and internal plate", "#94A3B8", (680, 0, 0)), 20: ("Fixings", "#374151", (0, 0, 0)),
         21: ("Status light, lens and lead", "#16A34A", (-420, -420, 60))}
ABOVE = Pos(0, 0, 5000) * Box(20000, 20000, 10000)


def _host(f, hosts):
    """BOM line of the smallest made or bought part whose box, grown by 12 mm, holds the fastener's centre."""
    c = f.bounding_box().center()
    best = None
    for n, bb, vol in hosts:
        if bb.min.X - 12 <= c.X <= bb.max.X + 12 and bb.min.Y - 12 <= c.Y <= bb.max.Y + 12 and bb.min.Z - 12 <= c.Z <= bb.max.Z + 12:
            if best is None or vol < best[1]:
                best = (n, vol)
    return best[0] if best else 20


def grouped():
    """Parts by BOM line; fasteners of line 20 (or none) go with the part they hold, so they explode with it."""
    groups, loose = {}, []
    comps = [p for p in M.components(M.CHOSEN) if p["kind"] != "context"]
    hosts = []
    for p in comps:
        if p["kind"] in ("made", "bought") and p["bom"] not in (None, 1, 14, 16):
            bb = p["shape"].bounding_box()
            hosts.append((p["bom"], bb, bb.size.X * bb.size.Y * bb.size.Z))
    for p in comps:
        sh = p["shape"] & ABOVE if p["shape"].bounding_box().min.Z < 0 else p["shape"]
        n = p["bom"]
        if p["kind"] == "fastener" and n in (None, 20):
            n = _host(sh, hosts)
        groups.setdefault(n or 20, []).append(sh)
    return {n: Compound(children=v) for n, v in sorted(groups.items())}


# The kit's cutaway cutter is centered on the origin, so shift the whole scene to put the
# enclosure and flow cell near the origin. Ground ends up at Z = -1100; nothing else changes.
SHIFT = Pos(-P["pole_x"], 0, -1100)


KEY_FIGURES = ["Free chlorine 0 to 2 mg/L, turbidity 0 to 100 NTU, temperature",
               "Hourly 90 s flush at 0.5 L/min; 18 L/day to drain (WWT-CAL-001)",
               "About 0.54 Wh/day; about 28 days on one 6 Ah cell (WWT-CAL-001)",
               "5 W panel, 3.2 V 6 Ah LiFePO4, sun shield; cellular with SMS",
               "$325 in parts (indicative); value-engineering target $300"]


def parts():
    out = [Part("Existing tapstand (not in BOM)", SHIFT * tapstand, GREY, None)]
    for n, sh in grouped().items():
        name, col, ex = LINES[n]
        out.append(Part(name, SHIFT * sh, col, n, ex))
    return out



def everything():
    return render_all(
    parts(), project="WaterWatch", title="Tapstand water quality sentinel concept", dwg_no="WWT-DWG-010",
    date="2026-10-02",
    key_figures=KEY_FIGURES,
    cut_exclude=("Existing tapstand (not in BOM)", "Mounting pole, U-bolts and saddles", "Mounting plates", "Solar panel, 5 W, with bracket",
                 "Drain hose and air break", "Sample line, tee and regulator", "Latching solenoid valve", "Antenna",
                 "Cables, glands and fuse", "Sun shield, ventilated", "Status light, lens and lead"),
    flow={"title": "sample and data flow (values from WWT-CAL-001)", "unit": "",
          "stages": [("Water at the tap", "tee on the riser"), ("Regulator and valve", "0.5 L/min, 90 s hourly"),
                     ("Flow-through cell", "0.19 L, 4 volumes a flush"), ("Controller", "log, 90 days on card"),
                     ("Cellular modem", "report every 4 h"), ("Caretaker, operator", "SMS within 13 min")],
          "losses": [(2, "Flushed sample to drain via air break, L per reading", 0.75)]},
)


def blueprint():
    """Concept blueprint sheet WWT-DWG-010 alone, as .kit/concept.py render_all draws it, from the grouped TRL 3
    geometry of build_parts() (the same design without its fasteners): the hidden-line projection of every
    D3 part does not fit in memory on a small machine (STANDARDS section 24 keeps the blueprint as it is)."""
    from drawing import Sheet, project_views
    md = ROOT / "media"
    legacy = M.build_parts(below_ground=False)
    shapes = [SHIFT * tapstand] + [SHIFT * sh for sh in legacy.values()]
    shown = concept.with_scale_figure([Part(f"p{i}", sh, GREY, None) for i, sh in enumerate(shapes)])
    views = project_views(Compound(children=shapes), md / "_views")
    views["iso"] = project_views(Compound(children=[q.shape for q in shown]), md / "_views_fig")["iso"]
    s = Sheet(project="WaterWatch", title="Tapstand water quality sentinel concept", dwg_no="WWT-DWG-010", rev="P1", author="Amish Chadha",
              date="2026-10-25", theme="blueprint", material="Massing model for concept communication",
              revisions=[("P1", "Concept sheet", "2026-10-25", "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    s.add_notes("Key figures", KEY_FIGURES, x=276, y=168, width=140)
    s.save(md / "concept-blueprint")
    return md / "concept-blueprint.png"


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what == "blueprint":
        print(blueprint())
    elif what == "web":
        print(concept.export_web_model([q for q in parts() if q.bom is not None] + parts()[:1], "media",
                                       title="WaterWatch: Tapstand water quality sentinel concept"))
    else:
        print(everything())
