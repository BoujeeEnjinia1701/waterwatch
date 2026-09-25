"""WaterWatch parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    waterwatch-assembly.step / .stl   the whole sentinel, pole set in its footing
    flow-cell.step / .stl             flow-through cell with sensor ports, baffle and fittings
    enclosure.step / .stl             enclosure base, lid, parts inside and the sun shield

Axes: the existing tapstand riser is the Z axis (x = y = 0), Z is up with the ground at
z = 0, and the WaterWatch pole stands on +X beside it. The enclosure and the panel face -Y.
Main dimensions and interfaces only: pole and footing, panel, enclosure envelope, flow
cell volume and port positions, sample line from the tee on the riser, drain with its air
break. Not fabrication detail; not for fabrication. The same PARAMS feed
docs/04-calcs/sizing.py (WWT-CAL-001) and the drawing WWT-DWG-001 (cad/src/sheets.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface: existing tapstand riser (25 mm galvanized pipe, 33.7 mm OD)
    "riser_od": 33.7, "riser_h": 950.0, "tee_z": 500.0,
    # 1 pole: 40 NB galvanized tube, 48.3 x 3.2 mm, set in a concrete footing
    "pole_x": 470.0, "pole_od": 48.3, "pole_wall": 3.2,
    "pole_h": 2100.0,                 # above ground
    "embed": 600.0, "footing_d": 300.0,
    "plate_t": 10.0,                  # mounting plates between parts and pole
    # 2 solar panel, 5 W
    "panel": (250.0, 190.0, 18.0), "panel_tilt": 30.0, "panel_rise": 60.0,
    # 3, 4 enclosure (outer), lid depth, wall, center height
    "enc": (200.0, 120.0, 260.0), "lid_t": 12.0, "enc_wall": 3.0, "enc_z": 1300.0,
    # 5 to 7 parts inside the enclosure
    "battery": (80.0, 40.0, 130.0), "board": (90.0, 12.0, 120.0), "modem": (70.0, 12.0, 55.0),
    "antenna": (18.0, 140.0),
    # 17 ventilated sun shield: white aluminum hood over top, sides and front, open at the back and bottom
    "shield_gap": 25.0, "shield_t": 2.0,
    # 9 flow-through cell: inner cavity (x, y, z), wall, center height of the body, baffle
    "cell_in": (80.0, 38.0, 66.0), "cell_wall": 8.0, "cell_z": 850.0, "cell_top_t": 10.0,
    "baffle": (6.0, 26.0, 40.0),
    "inlet_id": 4.0, "outlet_id": 10.0,
    # 10 to 12 sensors
    "turb": (32.0, 46.0, 46.0),
    "cl_d": 16.0, "cl_len": 120.0, "cl_immersed": 40.0,
    "t_d": 6.0, "t_len": 100.0, "t_immersed": 45.0,
    # 13, 14 sample line: tube 6.35 mm (1/4 in) OD, 4.3 mm bore; valve body
    "tube_od": 6.35, "tube_id": 4.3,
    "valve_x": 230.0, "valve": (55.0, 45.0, 60.0),
    # 15 drain: 12 mm bore hose, air-break vent at the outlet high point, discharge in the basin
    "hose_od": 16.0, "vent_h": 60.0, "drain_end": (240.0, -230.0, 170.0),
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    ew, ed, eh = p["enc"]
    cix, ciy, ciz = p["cell_in"]
    w = p["cell_wall"]
    cell_out = (cix + 2 * w, ciy + 2 * w, ciz + w)            # body; open top closed by the top plate
    pole_r = p["pole_od"] / 2
    pole_y = ed / 2 + p["plate_t"] + pole_r                    # pole just behind the enclosure plate
    cell_bot = p["cell_z"] - cell_out[2] / 2
    cell_top = p["cell_z"] + cell_out[2] / 2 + p["cell_top_t"]
    bx, by, bz = p["baffle"]
    cavity_l = cix * ciy * ciz / 1e6                           # L
    baffle_l = bx * by * bz / 1e6
    immersed_l = (math.pi / 4 * (p["cl_d"] ** 2 * p["cl_immersed"] + p["t_d"] ** 2 * p["t_immersed"])) / 1e6
    tube_run = (p["valve_x"] - p["riser_od"] / 2) + (p["pole_x"] - cix / 2 + 12 - p["valve_x"]) + (cell_bot - p["tee_z"])
    return {
        "pole_y": pole_y, "pole_top": p["pole_h"],
        "panel_z": p["pole_h"] + p["panel_rise"],
        "cell_out": cell_out, "cell_bot": cell_bot, "cell_top": cell_top,
        "cell_net_l": cavity_l - baffle_l - immersed_l,        # water volume of the cell
        "tube_l_mm": tube_run,
        "tube_vol_l": math.pi / 4 * p["tube_id"] ** 2 * tube_run / 1e6,
        "enc_bot": p["enc_z"] - eh / 2, "enc_top": p["enc_z"] + eh / 2,
        "outlet_z": p["cell_z"] + ciz / 2 + w / 2 - 12,          # outlet near the top keeps the cell full
        "overall_h": p["pole_h"] + p["panel_rise"] + p["panel"][1] / 2 * math.sin(math.radians(p["panel_tilt"])) + p["panel"][2] / 2,
        "enc_area_m2": 2 * (ew * ed + ew * eh + ed * eh) / 1e6,
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def tube(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    return fuse(tube(a, c, r) for a, c in zip(points, points[1:]))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def build_parts(p=PARAMS, below_ground=True):
    """Return {key: solid} for BOM items 1 to 17 (and the footing, which is site-supplied)."""
    b = _b3d()
    D = derived(p)
    px, py = p["pole_x"], D["pole_y"]
    pr = p["pole_od"] / 2
    parts = {}

    # 1 Pole, clamps and mounting plates
    z0 = -p["embed"] if below_ground else 0.0
    pole = zcyl(px, py, (z0 + p["pole_h"]) / 2, pr, p["pole_h"] - z0) - zcyl(px, py, (z0 + p["pole_h"]) / 2, pr - p["pole_wall"], p["pole_h"] - z0 + 2)
    ew, ed, eh = p["enc"]
    enc_plate = box(px, ed / 2 + p["plate_t"] / 2, p["enc_z"], 110, p["plate_t"], eh + 40)
    co = D["cell_out"]
    cell_plate = box(px, co[1] / 2 + (py - pr - co[1] / 2) / 2, p["cell_z"], 50, py - pr - co[1] / 2, 60)
    clamps = fuse(zcyl(px, py, z, pr + 7, 22) - zcyl(px, py, z, pr, 24)
                  for z in (p["cell_z"], p["enc_z"] - eh / 2 + 30, p["enc_z"] + eh / 2 - 30, p["pole_h"] - 40))
    parts["pole"] = pole + enc_plate + cell_plate + clamps
    if below_ground:
        parts["footing"] = zcyl(px, py, -p["embed"] / 2, p["footing_d"] / 2, p["embed"]) - zcyl(px, py, -p["embed"] / 2, pr, p["embed"] + 2)

    # 2 Solar panel on a tilt bracket at the pole top, facing -Y
    pw, ph, pt = p["panel"]
    pz = D["panel_z"]
    panel = b.Pos(px, py - 40, pz) * b.Rot(p["panel_tilt"], 0, 0) * b.Box(pw, ph, pt)
    bracket = tube((px, py, p["pole_h"] - 30), (px, py - 40, pz - 8), 12)
    parts["panel"] = panel + bracket

    # 3 Enclosure base (open to -Y) with cable glands underneath; 4 lid
    t, lt = p["enc_wall"], p["lid_t"]
    ez = p["enc_z"]
    base = box(0, lt / 2, 0, ew, ed - lt, eh) - box(0, lt / 2 - t, 0, ew - 2 * t, ed - lt, eh - 2 * t)
    base = b.Pos(px, 0, ez) * base
    for gx in (-50, 0, 50):
        base = base + zcyl(px + gx, 10, ez - eh / 2 - 8, 9, 16)
    parts["enc_base"] = base
    lid = box(0, -ed / 2 + lt / 2, 0, ew, lt, eh) - box(0, -ed / 2 + lt / 2 + t, 0, ew - 2 * t, lt, eh - 2 * t)
    parts["enc_lid"] = b.Pos(px, 0, ez) * lid
    back = ed / 2 - t
    bw, bd, bh = p["battery"]
    parts["battery"] = box(px - 45, back - bd / 2 - 2, ez - 55, bw, bd, bh)
    cw, cd, ch = p["board"]
    parts["board"] = box(px + 45, back - cd / 2 - 2, ez + 20, cw, cd, ch)
    mw, md, mh = p["modem"]
    parts["modem"] = box(px - 45, back - md / 2 - 2, ez + 75, mw, md, mh)
    ad, al = p["antenna"]
    parts["antenna"] = zcyl(px + 60, 10, ez + eh / 2 + al / 2, ad / 2, al)
    # 17 Sun shield (lifts off for the monthly visit)
    g, st = p["shield_gap"], p["shield_t"]
    sw, sh = ew + 2 * (g + st), eh + g + st
    sd = ed + g + st
    s_y0, s_y1 = -ed / 2 - g - st, ed / 2                      # front skin to the mounting plate
    hood = box(px, (s_y0 + s_y1) / 2, ez - eh / 2 + sh / 2 - 20, sw, s_y1 - s_y0, sh + 20)
    hood = hood - box(px, (s_y0 + s_y1) / 2 + st / 2 + 0.5, ez - eh / 2 + sh / 2 - 20 - st / 2 - 0.5,
                      sw - 2 * st, s_y1 - s_y0 - st + 1, sh + 20 - st + 1)
    parts["shield"] = hood

    # 9 Flow-through cell: open-top body, top plate with sensor ports, baffle, inlet and outlet
    cix, ciy, ciz = p["cell_in"]
    w, cz = p["cell_wall"], p["cell_z"]
    body = box(px, 0, cz, co[0], co[1], co[2]) - box(px, 0, cz + w / 2, cix, ciy, ciz + 0.01)
    top_z = cz + co[2] / 2 + p["cell_top_t"] / 2
    cl_x, t_x, port_y = px - 22, px + 24, 4.0
    top = (box(px, 0, top_z, co[0], co[1], p["cell_top_t"])
           - zcyl(cl_x, port_y, top_z, p["cl_d"] / 2 + 0.5, p["cell_top_t"] + 2)
           - zcyl(t_x, port_y, top_z, p["t_d"] / 2 + 0.5, p["cell_top_t"] + 2))
    bx, by, bz = p["baffle"]
    baffle = box(px, -ciy / 2 + by / 2, cz - ciz / 2 + w / 2 + bz / 2, bx, by, bz)
    in_x = px - cix / 2 + 12
    inlet = zcyl(in_x, 0, D["cell_bot"] - 10, 5, 20)
    out_z = D["outlet_z"]
    outlet = tube((px + co[0] / 2 - 1, 0, out_z), (px + co[0] / 2 + 22, 0, out_z), 8)
    parts["cell"] = body + top + baffle + inlet + outlet

    # 10 Turbidity head on the -X side wall at mid-height of the cavity
    tx, ty, tz = p["turb"]
    parts["turb"] = box(px - co[0] / 2 - tx / 2, 0, cz + w / 2 - 4, tx, ty, tz)
    # 11 Chlorine sensor and 12 temperature probe through the top plate
    cl_bot = cz + co[2] / 2 - p["cl_immersed"]
    parts["chlorine"] = zcyl(cl_x, port_y, cl_bot + p["cl_len"] / 2, p["cl_d"] / 2, p["cl_len"])
    t_bot = cz + co[2] / 2 - p["t_immersed"]
    parts["temp"] = zcyl(t_x, port_y, t_bot + p["t_len"] / 2, p["t_d"] / 2, p["t_len"])

    # 13 Latching solenoid valve (direct acting) on the sample line
    vx, tz_ = p["valve_x"], p["tee_z"]
    vw, vd, vh = p["valve"]
    parts["valve"] = box(vx, 0, tz_, vw, vd, vh) + zcyl(vx, 0, tz_ + vh / 2 + 17, 17, 34)

    # 14 Sample line: saddle tee and isolation valve, strainer, check valve and
    #    pressure-compensating flow regulator, 1/4 in tube to the cell inlet
    ro = p["riser_od"] / 2
    tr = p["tube_od"] / 2
    tee = zcyl(0, 0, tz_, ro + 7, 60) + tube((ro, 0, tz_), (ro + 30, 0, tz_), 10)
    iso = box(ro + 42, 0, tz_, 24, 22, 22) + tube((ro + 42, 0, tz_ + 11), (ro + 42, 0, tz_ + 40), 3)
    strainer = tube((ro + 60, 0, tz_), (ro + 90, 0, tz_), 12)
    reg = tube((ro + 105, 0, tz_), (ro + 155, 0, tz_), 11)
    line = (path([(ro + 30, 0, tz_), (ro + 60, 0, tz_)], tr) + path([(ro + 90, 0, tz_), (ro + 105, 0, tz_)], tr)
            + path([(ro + 155, 0, tz_), (vx - vw / 2, 0, tz_)], tr)
            + path([(vx + vw / 2, 0, tz_), (in_x, 0, tz_), (in_x, 0, D["cell_bot"] - 19)], tr))
    parts["sample"] = tee + iso + strainer + reg + line

    # 15 Drain: outlet elbow with an open air-break vent at the high point, hose down to the basin
    ox = px + co[0] / 2 + 22
    vent = tube((ox, 0, out_z - 8), (ox, 0, out_z + p["vent_h"]), 8)
    dx, dy, dz = p["drain_end"]
    hose = path([(ox, 0, out_z), (ox, 0, 350), (ox, dy, dz), (dx, dy, dz)], p["hose_od"] / 2)
    parts["drain"] = vent + hose

    # 16 Cables: cell sensors to the enclosure underside; panel to the enclosure top
    parts["cables"] = (path([(cl_x, port_y, cl_bot + p["cl_len"]), (cl_x, 30, cl_bot + p["cl_len"] + 20),
                             (cl_x, 30, D["enc_bot"] - 16)], 4)
                       + path([(px + 60, 45, p["pole_h"] - 20), (px + 60, 45, D["enc_top"] + 5)], 4))
    return parts


BOM_ORDER = [("pole", 1), ("panel", 2), ("enc_base", 3), ("enc_lid", 4), ("battery", 5), ("board", 6),
             ("modem", 7), ("antenna", 8), ("cell", 9), ("turb", 10), ("chlorine", 11), ("temp", 12),
             ("valve", 13), ("sample", 14), ("drain", 15), ("cables", 16), ("shield", 17)]


def riser_context(p=PARAMS):
    """Existing tapstand riser stub (grey on the drawing); not in the BOM."""
    return zcyl(0, 0, p["riser_h"] / 2, p["riser_od"] / 2, p["riser_h"])


def assembly(p=PARAMS, with_riser=False):
    b = _b3d()
    parts = build_parts(p)
    kids = list(parts.values()) + ([riser_context(p)] if with_riser else [])
    return b.Compound(children=kids)


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {
        "waterwatch-assembly": list(P.values()),
        "flow-cell": [P[k] for k in ("cell", "turb", "chlorine", "temp")],
        "enclosure": [P[k] for k in ("enc_base", "enc_lid", "battery", "board", "modem", "antenna", "shield")],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"cell water volume {D['cell_net_l']:.3f} L; sample tube {D['tube_l_mm']:.0f} mm, {D['tube_vol_l'] * 1000:.1f} mL; "
          f"overall height {D['overall_h']:.0f} mm above ground")
