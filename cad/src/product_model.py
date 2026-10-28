"""WaterWatch product model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is (option A, WWT-OPT-001): the pole and
its four U-bolt clamps, both back plates, the IP66 enclosure with its clear lid, lugs, glands, vent and antenna,
the battery tray, controller and modem on their standoffs, the sun shield and status light, the flow cell with
its lid, studs, thumb nuts, optics holders, chlorine sensor and temperature probe, the latching valve, the saddle
tee, fittings and tubes, the air-break drain, the cables and the 5 W panel on its tilt mount, with every bolt,
nut, washer and screw. Nothing is redrawn and no height is moved (the render-only layout of 2026-09-26 is
retired: the product renders now show the installed heights). Only the site is added, as context parts: the
existing tapstand riser and tap, its concrete apron and basin, the pole's concrete footing and a 1.75 m
mannequin standing on the ground beside the unit. Ground level is model z = 0 and every site part reaches below
it. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the whole product), "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "WaterWatch: solar water quality sentinel for a village tap"

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=48,-75", "--lens=45"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 12, "az": -40, "args": _SITE,
     "note": "Site render from the front right, a little above (about 12 deg elevation): WaterWatch on its own pole "
             "beside a village tapstand on its concrete apron, sun shield over the enclosure, flow cell and valve on "
             "the lower plate, sample line from the saddle tee, drain to the basin, 5 W panel on top; 1.75 m person "
             "standing on the ground at the right for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 18, "az": -35, "args": ["--ground-z=0"],
     "note": "Studio render from the front right and a little above (about 18 deg elevation): the whole unit with "
             "every fastener, the buried 0.6 m of the pole below the floor line"},
]


def site():
    """Site context at a village tapstand. Ground level is model z = 0 (photoreal --ground-z=0); every site part
    reaches below it so no gap shows at the ground line."""
    P = M.PARAMS
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    apron = Pos(0, 0, 25) * Box(700, 700, 250) - Pos(0, 0, 150) * Box(560, 560, 41)
    ctx("Tapstand concrete apron and basin", break_edges(apron, 6), "concrete")
    ctx("Tapstand riser", Pos(0, 0, (P["riser_h"] - 100) / 2) * Cylinder(P["riser_od"] / 2, P["riser_h"] + 100), "galvanised")
    tap = (Pos(0, -65, P["riser_h"]) * Rot(90, 0, 0) * Cylinder(14, 130) + Pos(0, -130, P["riser_h"] - 30) * Cylinder(11, 60)
           + Pos(0, 0, P["riser_h"] + 40) * Cylinder(10, 60))
    ctx("Tapstand tap", tap, "brass")
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context" and "footing" in p["name"].lower():
            ctx("Pole footing, concrete", p["shape"], "concrete")
    try:
        import context_parts
        man = Pos(M.PARAMS["pole_x"] + 700, -350, 0) * Rot(0, 0, -30) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["group"] = "shell"
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "context" for p in ps), "context")
