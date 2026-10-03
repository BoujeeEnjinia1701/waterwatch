"""WaterWatch parametric model (build123d), TRL 3, constructable design (WWT-DDR-003).

DDR-002 (2026-09-25): the cell lid carries a spare port, closed by a blanking plug, so that a
site that needs the pH probe variant can take one without a new cell.
DDR-003 (2026-09-30, design for construction): every part can now be made by its stated process
and is fixed to the parts next to it. The enclosure and the flow cell each hang on a 3 mm aluminium
back plate held to the pole by two M8 U-bolts with V-saddles; the enclosure hangs on the maker's
lugs; the parts inside sit on a printed internal plate on the box's moulded bosses; every cable
enters through the bottom face; the sun shield slides off forward after four thumb screws; the
flow cell is screwed to its plate through a thicker back wall; the optics are three small holders
(LED, 90 degree and 180 degree detectors) on three walls, with the baffle moved to the back wall so
the beam is clear; the valve is screwed to the cell plate under the cell; the panel sits on a
bought pole-top tilt mount.

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks (contacts, clearances, overlaps)
Exports:
    waterwatch-assembly.step / .stl   the whole sentinel, pole set in its footing
    flow-cell.step / .stl             flow cell, optics, sensors, lid, cell plate and valve
    enclosure.step / .stl             enclosure, parts inside, back plate and sun shield

Axes: the existing tapstand riser is the Z axis (x = y = 0), Z is up with the ground at z = 0,
and the WaterWatch pole stands on +X beside it. The enclosure and the panel face -Y; the pole is
behind them (+Y). Not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py
(WWT-CAL-001), the drawing WWT-DWG-001 (cad/src/sheets.py) and the build plan pictures
(cad/src/build_plan_media.py).
"""
import math
import sys
from pathlib import Path

SQ2 = math.sqrt(2.0)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface: existing tapstand riser (25 mm galvanized pipe, 33.7 mm OD)
    "riser_od": 33.7, "riser_h": 950.0, "tee_z": 500.0,
    # 1 pole: 40 NB galvanized tube, 48.3 x 3.2 mm, set in a concrete footing
    "pole_x": 470.0, "pole_od": 48.3, "pole_wall": 3.2,
    "pole_h": 2100.0,                 # above ground
    "embed": 600.0, "footing_d": 300.0,
    # 1 U-bolts (M8, for 48 mm pipe) and V-saddles; 18 back plates (3 mm aluminium sheet)
    "plate_t": 3.0,
    "saddle": (76.0, 30.0, 30.0),     # wide (x), deep (y), tall (z)
    "saddle_apex": 6.0,               # point of the 90 degree V from the saddle's back face
    "ub_d": 8.0, "ub_x": 29.0,        # U-bolt rod and leg spacing from the pole axis
    "nut": (14.0, 8.0),               # nut and washer across corners, thickness
    "enc_plate": (270.0, 420.0), "enc_ub_dz": 185.0,
    "cell_plate": (140.0, 385.0), "cell_plate_z": (600.0, 985.0), "cell_ub_z": (625.0, 960.0),
    # 2 solar panel, 5 W, on a bought pole-top tilt mount
    "panel": (250.0, 190.0, 18.0), "panel_tilt": 30.0, "panel_rise": 60.0,
    "sleeve": (30.0, 85.0),           # pole-top mount sleeve outer radius, length
    # 3, 4 enclosure (outer), lid depth, wall, center height
    "enc": (200.0, 120.0, 260.0), "lid_t": 12.0, "enc_wall": 3.0, "enc_z": 1300.0,
    # bottom-face entries: two rows, measured from the back face; x from the enclosure centre
    "pen_rows": (28.0, 70.0, 49.0),
    "pens": {"valve": (-62, 0), "chlorine": (-22, 0), "ph_spare": (22, 0), "temp": (62, 0),
             "panel": (-62, 1), "optics": (-22, 1), "vent": (22, 1), "antenna": (62, 1),
             "status": (0, 2)},
    # 19 lugs (maker's kit) and printed internal plate on the box's moulded bosses
    "lug": (20.0, 3.0, 20.0), "lug_x": 85.0,
    "mplate": (186.0, 205.0, 3.0), "mplate_gap": 6.0, "mplate_z": -90.0,
    # 5 to 7 parts inside the enclosure
    "battery": (80.0, 40.0, 130.0), "board": (90.0, 12.0, 120.0), "modem": (70.0, 12.0, 55.0),
    "standoff": 6.0,
    "antenna": (18.0, 140.0),
    # 17 ventilated sun shield: white aluminium hood over top, sides and front, open at the bottom
    "shield_gap": 25.0, "shield_t": 2.0, "shield_flange": 15.0, "shield_below": 20.0,
    # 21 status light (decided 2026-10-02, WWT-DEC-001): one 5 mm LED behind a lens that sits in a slot, open at the bottom,
    # in the shield front panel; the unit drops out of the slot so the shield still slides off
    "stat_below": 10.0,               # LED axis below the underside of the enclosure
    "stat_slot": 12.2, "stat_barrel": 12.0, "stat_flange": 16.0, "stat_lens_t": 1.5, "stat_collar": 18.0, "stat_collar_t": 2.0,
    "stat_len": 12.0,                 # barrel length behind the panel's inner face
    "stat_led_d": 5.0, "stat_led_l": 9.0, "stat_cable_d": 3.5, "stat_cable_drop": 24.0,
    # 9 flow-through cell: inner cavity (x, y, z), wall, back wall, center height, lid, baffle
    "cell_in": (80.0, 38.0, 66.0), "cell_wall": 8.0, "cell_back": 14.0, "cell_z": 850.0, "cell_top_t": 10.0,
    "gasket_t": 1.5,
    "baffle": (6.0, 26.0, 40.0), "baffle_x": 2.0,
    "inlet_id": 4.0, "outlet_id": 10.0, "inlet_x": -32.0, "outlet_y": 10.0,
    # 10 turbidity optics: beam along X, 13 mm in front of the cavity centre, at cavity mid-height
    "beam_y": -13.0, "win_d": 6.0, "holder": (20.0, 20.0, 16.0), "det90_x": -8.0,
    # 11, 12 sensors, positions in the lid relative to the cavity centre (x, y)
    "cl_d": 16.0, "cl_len": 120.0, "cl_immersed": 40.0, "cl_xy": (-24.0, 8.0),
    "t_d": 6.0, "t_len": 100.0, "t_immersed": 45.0, "t_xy": (34.0, -4.0),
    # 9 spare pH port (WWT-DDR-002), M20 gland closed by a blanking plug
    "ph_port_d": 12.0, "ph_x": 14.0, "ph_y": 10.0, "plug": (27.0, 8.0),
    "studs": ((-44.0, -23.0), (44.0, -23.0), (-44.0, 26.0), (44.0, 26.0)),
    # 13, 14 sample line: tube 6.35 mm (1/4 in) OD, 4.3 mm bore; valve body under the cell
    "tube_od": 6.35, "tube_id": 4.3,
    "valve_x": 470.0, "valve": (55.0, 45.0, 60.0), "valve_drop": 120.0, "tube_x": 45.0,
    # 15 drain: 12 mm bore hose, air-break vent at the outlet, discharge in the basin
    "hose_od": 16.0, "vent_h": 60.0, "drain_end": (240.0, -230.0, 170.0),
    "cable_d": 6.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note, drawing and build plan quote, computed from PARAMS."""
    ew, ed, eh = p["enc"]
    cix, ciy, ciz = p["cell_in"]
    w, wb = p["cell_wall"], p["cell_back"]
    pole_r = p["pole_od"] / 2
    plate_front = ed / 2                                       # enclosure back = plate front face
    plate_back = plate_front + p["plate_t"]
    apex = plate_back + p["saddle_apex"]
    pole_y = apex + pole_r * SQ2                               # pole rests on both faces of the 90 degree V
    cell_out = (cix + 2 * w, ciy + w + wb, ciz + w)            # body; open top closed by the lid
    cell_y = plate_front - (ciy / 2 + wb)                      # cavity centre: cell back on the plate
    cz = p["cell_z"]
    cell_bot = cz - cell_out[2] / 2
    body_top = cz + cell_out[2] / 2
    lid_bot = body_top + p["gasket_t"]
    cell_top = lid_bot + p["cell_top_t"]
    bx, by, bz = p["baffle"]
    cavity_l = cix * ciy * ciz / 1e6                           # L
    baffle_l = bx * by * bz / 1e6
    immersed_l = (math.pi / 4 * (p["cl_d"] ** 2 * p["cl_immersed"] + p["t_d"] ** 2 * p["t_immersed"])) / 1e6
    ro = p["riser_od"] / 2
    px = p["pole_x"]
    vz = cell_bot - p["valve_drop"]
    vw = p["valve"][0]
    # 1/4 in tube: regulator outlet to valve inlet, valve outlet to the cell inlet
    vy = plate_front - p["valve"][1] / 2
    tube_run = (((px + p["tube_x"]) - (ro + 155)) + vy + (vz - p["tee_z"]) + (p["tube_x"] - vw / 2)
                + (abs(p["inlet_x"]) - vw / 2) + (cell_bot - 20 - vz))
    return {
        "pole_y": pole_y, "pole_top": p["pole_h"], "plate_front": plate_front, "plate_back": plate_back,
        "saddle_apex_y": apex,
        "panel_z": p["pole_h"] + p["panel_rise"],
        "cell_out": cell_out, "cell_y": cell_y, "cell_bot": cell_bot, "cell_top": cell_top,
        "body_top": body_top, "lid_bot": lid_bot,
        "cav_z": cz + w / 2, "valve_z": vz,
        "cell_net_l": cavity_l - baffle_l - immersed_l,        # water volume of the cell
        "tube_l_mm": tube_run,
        "tube_vol_l": math.pi / 4 * p["tube_id"] ** 2 * tube_run / 1e6,
        "enc_bot": p["enc_z"] - eh / 2, "enc_top": p["enc_z"] + eh / 2,
        "outlet_z": cz + ciz / 2 + w / 2 - 12,                 # outlet near the top keeps the cell full
        "overall_h": p["pole_h"] + p["panel_rise"] + p["panel"][1] / 2 * math.sin(math.radians(p["panel_tilt"])) + p["panel"][2] / 2,
        "enc_area_m2": 2 * (ew * ed + ew * eh + ed * eh) / 1e6,
        "enc_ub_z": (p["enc_z"] - p["enc_ub_dz"], p["enc_z"] + p["enc_ub_dz"]),
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def span(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def tube(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def path(points, r, joints=True):
    """Rod along a polyline, with a ball at each bend so the corners are closed."""
    b = _b3d()
    s = fuse(tube(a, c, r) for a, c in zip(points, points[1:]))
    if joints:
        for q in points[1:-1]:
            s = s + b.Pos(*q) * b.Sphere(r)
    return s


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def ycyl(x, y0, y1, z, r):
    return tube((x, y0, z), (x, y1, z), r)


def xcyl(x0, x1, y, z, r):
    return tube((x0, y, z), (x1, y, z), r)


# ----------------------------------------------------------------------------- pole fixings
def saddle(p, D, x, z):
    """V-saddle between the back plate and the pole: back face on the plate, 90 degree V for the pole."""
    b = _b3d()
    sw, sd, sh = p["saddle"]
    y0 = D["plate_back"]
    blk = span(x - sw / 2, x + sw / 2, y0, y0 + sd, z - sh / 2, z + sh / 2)
    a = 40.0
    v = b.Pos(x, D["saddle_apex_y"] + a / SQ2, z) * b.Rot(0, 0, 45) * b.Box(a, a, sh + 2)
    blk = blk - v
    for s in (-1, 1):
        blk = blk - ycyl(x + s * p["ub_x"], y0 - 1, y0 + sd + 1, z, p["ub_d"] / 2 + 0.25)
    return blk


def ubolt(p, D, x, z):
    """M8 U-bolt round the back of the pole, legs through the saddle and plate, nuts on the plate front."""
    b = _b3d()
    pr = p["pole_od"] / 2
    rr = p["ub_d"] / 2
    R = p["ub_x"]                                   # centreline radius of the bend
    c = D["pole_y"] - (R - rr - pr)                 # bend inner surface touches the back of the pole
    tor = b.Pos(x, c, z) * b.Torus(R, rr)
    tor = tor & span(x - R - rr - 1, x + R + rr + 1, c, c + R + rr + 1, z - rr - 1, z + rr + 1)
    nd, nt = p["nut"]
    yf = D["plate_front"]
    legs = fuse(ycyl(x + s * R, yf - nt - 5, c, z, rr) for s in (-1, 1))
    nuts = fuse(ycyl(x + s * R, yf - nt, yf, z, nd / 2) for s in (-1, 1))
    return tor + legs + nuts


def plate_with_holes(p, D, x, z0, z1, width, ub_z, extra_holes=()):
    yf, yb = D["plate_front"], D["plate_back"]
    pl = span(x - width / 2, x + width / 2, yf, yb, z0, z1)
    for z in ub_z:
        for s in (-1, 1):
            pl = pl - ycyl(x + s * p["ub_x"], yf - 1, yb + 1, z, p["ub_d"] / 2 + 0.5)
    for hx, hz, hr in extra_holes:
        pl = pl - ycyl(hx, yf - 1, yb + 1, hz, hr)
    return pl


# ----------------------------------------------------------------------------- components
def build_components(p=PARAMS, below_ground=True):
    """Return {key: solid} for every separately made, bought or fitted part. Used by the checks,
    the build plan pictures and (grouped by BOM line) build_parts()."""
    b = _b3d()
    D = derived(p)
    px, py = p["pole_x"], D["pole_y"]
    pr = p["pole_od"] / 2
    C = {}

    # 1 pole and footing (footing is site supplied)
    z0 = -p["embed"] if below_ground else 0.0
    C["pole"] = zcyl(px, py, (z0 + p["pole_h"]) / 2, pr, p["pole_h"] - z0) - zcyl(px, py, (z0 + p["pole_h"]) / 2, pr - p["pole_wall"], p["pole_h"] - z0 + 2)
    if below_ground:
        C["footing"] = zcyl(px, py, -p["embed"] / 2, p["footing_d"] / 2, p["embed"]) - zcyl(px, py, -p["embed"] / 2, pr, p["embed"] + 2)

    ew, ed, eh = p["enc"]
    ez = p["enc_z"]
    yf, yb = D["plate_front"], D["plate_back"]

    # 18 enclosure back plate, 1 saddles and U-bolts
    pw, ph = p["enc_plate"]
    lx, lz = p["lug_x"], eh / 2 + 2 + p["lug"][2] / 2 + 1     # lug screw: on the lug tab, above and below the box
    sx = ew / 2 + p["shield_gap"] - p["shield_flange"] / 2          # shield screw x, mid-flange
    sz = eh / 2 - 20
    holes = [(px + s * lx, ez + t * lz, 2.75) for s in (-1, 1) for t in (-1, 1)]
    holes += [(px + s * sx, ez + t * sz, 2.4) for s in (-1, 1) for t in (-1, 1)]      # tapped M5 (drill 4.2)
    C["enc_plate"] = plate_with_holes(p, D, px, ez - ph / 2, ez + ph / 2, pw, D["enc_ub_z"], holes)
    for i, z in enumerate(D["enc_ub_z"]):
        C[f"enc_saddle_{i}"] = saddle(p, D, px, z)
        C[f"enc_ubolt_{i}"] = ubolt(p, D, px, z)

    # 3 enclosure base: open to -Y, four moulded bosses, eight drilled entries in the bottom face
    t, lt = p["enc_wall"], p["lid_t"]
    base = box(0, lt / 2, 0, ew, ed - lt, eh) - box(0, lt / 2 - t, 0, ew - 2 * t, ed - lt, eh - 2 * t)
    base = b.Pos(px, 0, ez) * base
    mw, mh, mt = p["mplate"]
    mz = ez + p["mplate_z"] + mh / 2                                   # internal plate centre height
    my1 = ed / 2 - t - p["mplate_gap"]                                 # plate back face
    boss_pts = [(px + s * (mw / 2 - 10), mz + q * (mh / 2 - 10)) for s in (-1, 1) for q in (-1, 1)]
    for bx_, bz_ in boss_pts:
        base = base + (ycyl(bx_, my1, ed / 2 - t + 0.5, bz_, 5) - ycyl(bx_, my1 - 1, ed / 2 - t, bz_, 2.0))
    zb = ez - eh / 2
    pen_xy = {}
    for k, (x, row) in p["pens"].items():
        y = ed / 2 - p["pen_rows"][row]
        pen_xy[k] = (px + x, y)
        r = {"vent": 6.1, "antenna": 3.25}.get(k, 8.1)
        base = base - zcyl(px + x, y, zb + t / 2, r, t + 2)
    C["enc_base"] = base
    C["enc_lid"] = b.Pos(px, 0, ez) * (box(0, -ed / 2 + lt / 2, 0, ew, lt, eh) - box(0, -ed / 2 + lt / 2 + t, 0, ew - 2 * t, lt, eh - 2 * t))

    # entries: glands (thread through the wall, body below, nut inside), vent, antenna bulkhead and whip
    gl = []
    for k, (x, y) in pen_xy.items():
        if k == "antenna":
            continue
        if k == "vent":
            gl.append(zcyl(x, y, zb + t / 2, 6, t) + zcyl(x, y, zb - 6, 9, 12) + zcyl(x, y, zb + t + 2.5, 8, 5))
        else:
            g = zcyl(x, y, zb + t / 2, 8, t) + zcyl(x, y, zb - 9, 12, 18) + zcyl(x, y, zb + t + 3, 11, 6)
            gl.append(g)
    C["glands"] = fuse(gl)
    ax_, ay_ = pen_xy["antenna"]
    ad, al = p["antenna"]
    C["antenna"] = (zcyl(ax_, ay_, zb + t / 2, 3.2, t) + zcyl(ax_, ay_, zb + t + 2.5, 5, 5)
                    + zcyl(ax_, ay_, zb - 6, ad / 2, 12) + zcyl(ax_, ay_, zb - 12 - (al - 12) / 2, 5, al - 12))

    # 19 lugs: an L on each back corner, foot on the box top or bottom, tab flat on the back plate
    lw, lth, lh = p["lug"]
    lugs, lug_scr = [], []
    for s in (-1, 1):
        for q in (-1, 1):
            x = px + s * lx
            ze = ez + q * eh / 2
            foot = span(x - lw / 2, x + lw / 2, yf - 20, yf - lth, ze, ze + q * lth)
            tab = span(x - lw / 2, x + lw / 2, yf - lth, yf, ze + q * 2, ze + q * (2 + lh))
            lugs.append(foot + tab - ycyl(x, yf - lth - 1, yf + 1, ez + q * lz, 2.75))
            lug_scr.append(ycyl(x, yf - lth, yb + 3.5, ez + q * lz, 2.5) + ycyl(x, yb, yb + 3.5, ez + q * lz, 4.5)
                           + ycyl(x, yf - lth - 4, yf - lth, ez + q * lz, 4.5))
    C["lugs"] = fuse(lugs)
    C["lug_screws"] = fuse(lug_scr)

    # 19 internal plate on the bosses; 5 battery, 6 controller and 7 modem on it
    C["mplate"] = span(px - mw / 2, px + mw / 2, my1 - mt, my1, mz - mh / 2, mz + mh / 2) - fuse(
        ycyl(bx_, my1 - mt - 1, my1 + 1, bz_, 2.2) for bx_, bz_ in boss_pts)
    C["mplate_screws"] = fuse(ycyl(bx_, my1 - mt - 3, my1 + 6, bz_, 2.0) + ycyl(bx_, my1 - mt - 3, my1 - mt, bz_, 3.6)
                              for bx_, bz_ in boss_pts)
    mf = my1 - mt                                                      # plate front face
    bw, bd, bh = p["battery"]
    C["battery"] = span(px - 85, px - 85 + bw, mf - bd, mf, ez - 72, ez - 72 + bh)
    so = p["standoff"]

    def on_standoffs(x0, x1, z0_, z1_, depth):
        brd = span(x0, x1, mf - so - depth, mf - so, z0_, z1_)
        for xx in (x0 + 5, x1 - 5):
            for zz in (z0_ + 5, z1_ - 5):
                brd = brd + ycyl(xx, mf - so, mf, zz, 2.5)
        return brd
    cw, cd, ch = p["board"]
    C["board"] = on_standoffs(px, px + cw, ez - 45, ez - 45 + ch, cd)
    mw_, md_, mh_ = p["modem"]
    C["modem"] = on_standoffs(px - 75, px - 75 + mw_, ez + 60, ez + 60 + mh_, md_)

    # 17 sun shield: hood with flanges folded in at the back of each side, four M5 thumb screws
    g, st, fl = p["shield_gap"], p["shield_t"], p["shield_flange"]
    sxo = ew / 2 + g + st
    s_y0 = -ed / 2 - g - st
    sz0, sz1 = ez - eh / 2 - p["shield_below"], ez + eh / 2 + g + st
    hood = span(px - sxo, px + sxo, s_y0, yf, sz0, sz1) - span(px - sxo + st, px + sxo - st, s_y0 + st, yf + 1, sz0 - 1, sz1 - st)
    for s in (-1, 1):
        f = span(px + s * (sxo - st), px + s * (sxo - st - fl), yf - st, yf, sz0, sz1 - st)
        for q in (-1, 1):
            f = f - ycyl(px + s * sx, yf - st - 1, yf + 1, ez + q * sz, 2.75)
        hood = hood + f
    # 21 status light: slot open at the bottom in the front panel, for the lens unit (it drops out downward)
    zl = ez - eh / 2 - p["stat_below"]
    hood = hood - ycyl(px, s_y0 - 1, s_y0 + st + 1, zl, p["stat_slot"] / 2) - span(px - p["stat_slot"] / 2, px + p["stat_slot"] / 2, s_y0 - 1, s_y0 + st + 1, sz0 - 1, zl)
    C["shield"] = hood
    yo, yi = s_y0, s_y0 + st
    fd, bd_ = p["stat_flange"], p["stat_barrel"]
    C["status_lens"] = ycyl(px, yo - p["stat_lens_t"], yo, zl, fd / 2)
    holder = ycyl(px, yo, yi + p["stat_len"], zl, bd_ / 2) + ycyl(px, yi, yi + p["stat_collar_t"], zl, p["stat_collar"] / 2)
    holder = holder - ycyl(px, yo - 0.1, yo + p["stat_led_l"], zl, p["stat_led_d"] / 2 + 0.01)
    C["status_holder"] = holder
    C["status_led"] = ycyl(px, yo, yo + p["stat_led_l"], zl, p["stat_led_d"] / 2)
    stx, sty = pen_xy["status"]
    yr = yi + p["stat_len"]
    zc = zb - p["stat_cable_drop"]
    C["status_cable"] = path([(px, yr, zl), (px, yr + 4, zl), (px, yr + 4, zc), (stx, sty, zc), (stx, sty, zb - 18)], p["stat_cable_d"] / 2)
    C["shield_screws"] = fuse(ycyl(px + s * sx, yf - st - 6, yb + 2, ez + q * sz, 2.4) + ycyl(px + s * sx, yf - st - 6, yf - st, ez + q * sz, 6)
                              for s in (-1, 1) for q in (-1, 1))

    # 18 cell back plate, saddles and U-bolts
    cpw, _ = p["cell_plate"]
    cpz0, cpz1 = p["cell_plate_z"]
    cz = p["cell_z"]
    cy = D["cell_y"]
    vz = D["valve_z"]
    cell_holes = [(px + s * 30, cz, 2.75) for s in (-1, 1)] + [(px + s * 18, vz, 2.25) for s in (-1, 1)]
    C["cell_plate"] = plate_with_holes(p, D, px, cpz0, cpz1, cpw, p["cell_ub_z"], cell_holes)
    for i, z in enumerate(p["cell_ub_z"]):
        C[f"cell_saddle_{i}"] = saddle(p, D, px, z)
        C[f"cell_ubolt_{i}"] = ubolt(p, D, px, z)

    # 9 flow cell body: open top, thick back wall with two tapped M5 holes, baffle on the back wall,
    #   three optical windows, inlet in the floor, outlet near the top of the +X wall, lid studs
    cix, ciy, ciz = p["cell_in"]
    w, wb = p["cell_wall"], p["cell_back"]
    co = D["cell_out"]
    by0 = cy - ciy / 2 - w                                    # body front face
    by1 = cy + ciy / 2 + wb                                   # body back face (on the plate)
    cav_z = D["cav_z"]
    cav_lo, cav_hi = cz - co[2] / 2 + w, D["body_top"]
    body = span(px - co[0] / 2, px + co[0] / 2, by0, by1, D["cell_bot"], D["body_top"])
    body = body - span(px - cix / 2, px + cix / 2, cy - ciy / 2, cy + ciy / 2, cav_lo, cav_hi + 1)
    bx, bby, bz = p["baffle"]
    baffle = span(px + p["baffle_x"] - bx / 2, px + p["baffle_x"] + bx / 2, cy + ciy / 2 - bby, cy + ciy / 2, cav_lo, cav_lo + bz)
    body = body + baffle
    yb_ = cy + p["beam_y"]
    wr = p["win_d"] / 2
    body = (body - xcyl(px - co[0] / 2 - 1, px - cix / 2 + 0.01, yb_, cav_z, wr)
            - xcyl(px + cix / 2 - 0.01, px + co[0] / 2 + 1, yb_, cav_z, wr)
            - ycyl(px + p["det90_x"], by0 - 1, cy - ciy / 2 + 0.01, cav_z, wr))
    cb = 2.5
    body = (body - xcyl(px - co[0] / 2 - 1, px - co[0] / 2 + cb, yb_, cav_z, 6)
            - xcyl(px + co[0] / 2 - cb, px + co[0] / 2 + 1, yb_, cav_z, 6)
            - ycyl(px + p["det90_x"], by0 - 1, by0 + cb, cav_z, 6))
    in_x = px + p["inlet_x"]
    in_y = yf - p["valve"][1] / 2          # inlet straight above the valve outlet elbow
    body = body - zcyl(in_x, in_y, D["cell_bot"] + w / 2, 4.25, w + 2)
    out_z = D["outlet_z"]
    oy = cy + p["outlet_y"]
    body = body - xcyl(px + cix / 2 - 1, px + co[0] / 2 + 1, oy, out_z, 8.5)
    for s in (-1, 1):
        body = body - ycyl(px + s * 30, by1 - 12, by1 + 1, cz, 2.5)          # tapped M5, 12 deep
    for sx_, sy_ in p["studs"]:
        body = body - zcyl(px + sx_, cy + sy_, D["body_top"] - 6, 2.0, 12.01)
    C["cell_body"] = body
    C["cell_screws"] = fuse(ycyl(px + s * 30, by1 - 10, yb + 3.5, cz, 2.5) + ycyl(px + s * 30, yb, yb + 3.5, cz, 4.5) for s in (-1, 1))

    # 9 gasket and lid with three gland holes and four stud holes; plug in the spare port
    def lid_outline(z0_, z1_):
        return span(px - co[0] / 2, px + co[0] / 2, by0, by1, z0_, z1_)
    gasket = lid_outline(D["body_top"], D["lid_bot"]) - span(px - cix / 2, px + cix / 2, cy - ciy / 2, cy + ciy / 2, D["body_top"] - 1, D["lid_bot"] + 1)
    lid = lid_outline(D["lid_bot"], D["cell_top"])
    clx, cly = px + p["cl_xy"][0], cy + p["cl_xy"][1]
    tx, ty = px + p["t_xy"][0], cy + p["t_xy"][1]
    phx, phy = px + p["ph_x"], cy + p["ph_y"]
    lt_mid = (D["lid_bot"] + D["cell_top"]) / 2
    for (x, y, r) in ((clx, cly, 12.6), (tx, ty, 6.1), (phx, phy, 10.1)):
        lid = lid - zcyl(x, y, lt_mid, r, p["cell_top_t"] + 2)
    for sx_, sy_ in p["studs"]:
        gasket = gasket - zcyl(px + sx_, cy + sy_, (D["body_top"] + D["lid_bot"]) / 2, 2.2, 3)
        lid = lid - zcyl(px + sx_, cy + sy_, lt_mid, 2.2, p["cell_top_t"] + 2)
    C["gasket"] = gasket
    C["cell_lid"] = lid
    ct = D["cell_top"]
    C["lid_glands"] = ((zcyl(clx, cly, lt_mid, 12.5, p["cell_top_t"]) - zcyl(clx, cly, lt_mid, 8.0, p["cell_top_t"] + 1)) + (zcyl(clx, cly, ct + 7.5, 16.5, 15) - zcyl(clx, cly, ct + 7.5, 8.0, 16))
                       + (zcyl(tx, ty, lt_mid, 6.0, p["cell_top_t"]) - zcyl(tx, ty, lt_mid, 3.0, p["cell_top_t"] + 1)) + (zcyl(tx, ty, ct + 6, 8.5, 12) - zcyl(tx, ty, ct + 6, 3.0, 13)))
    pd, phh = p["plug"]
    C["plug"] = zcyl(phx, phy, lt_mid, 10.0, p["cell_top_t"]) + zcyl(phx, phy, ct + phh / 2, pd / 2, phh)
    C["studs"] = fuse(zcyl(px + sx_, cy + sy_, D["body_top"] - 10 + (ct + 8 - D["body_top"] + 10) / 2, 2.0, ct + 8 - D["body_top"] + 10)
                      + zcyl(px + sx_, cy + sy_, ct + 4, 6, 8) for sx_, sy_ in p["studs"])

    # 10 optics: LED holder on the -X wall, 180 degree reference on the +X wall, 90 degree on the front
    hw, hh, hd = p["holder"]

    def holder():
        """Holder in local coordinates: wall face on z = 0, body toward -z, 5 mm bore 12 deep on the axis,
        3 mm lead hole out of the top (+y), two 3.4 mm screw holes at opposite corners."""
        hb = span(-hw / 2, hw / 2, -hh / 2, hh / 2, -hd, 0)
        hb = hb - zcyl(0, 0, -6, 2.5, 12.02) - tube((0, 0, -8), (0, hh / 2 + 1, -8), 1.5)
        for sx_, sy_ in ((-1, -1), (1, 1)):
            hb = hb - zcyl(sx_ * (hw / 2 - 3.5), sy_ * (hh / 2 - 3.5), -hd / 2, 1.7, hd + 2)
        return hb

    def place(origin, z_dir, x_dir):
        return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).from_local_coords(holder())
    # local +z points into the wall; local +y is up
    C["led_holder"] = place((px - co[0] / 2, yb_, cav_z), (1, 0, 0), (0, 1, 0))
    C["ref_holder"] = place((px + co[0] / 2, yb_, cav_z), (-1, 0, 0), (0, -1, 0))
    dx = px + p["det90_x"]
    C["det90_holder"] = place((dx, by0, cav_z), (0, 1, 0), (-1, 0, 0))

    # 11 chlorine sensor (PVC holder with three electrode tips) and 12 temperature probe
    cl_bot = D["body_top"] - p["cl_immersed"]
    chl = zcyl(clx, cly, cl_bot + p["cl_len"] / 2, p["cl_d"] / 2, p["cl_len"])
    for k in range(3):
        a = math.radians(90 + 120 * k)
        chl = chl + zcyl(clx + 4.5 * math.cos(a), cly + 4.5 * math.sin(a), cl_bot - 1.5, 1.0, 3.0)
    C["chlorine"] = chl
    t_bot = D["body_top"] - p["t_immersed"]
    C["temp"] = zcyl(tx, ty, t_bot + p["t_len"] / 2, p["t_d"] / 2, p["t_len"])

    # 13 latching valve, back face on the cell plate, two M4 screws from behind
    vw, vd, vh = p["valve"]
    vy = yf - vd / 2
    C["valve"] = box(px, vy, vz, vw, vd, vh) + zcyl(px, vy, vz + vh / 2 + 17, 17, 34) - fuse(ycyl(px + s * 18, yf - 8, yf + 1, vz, 2.0) for s in (-1, 1))
    C["valve_screws"] = fuse(ycyl(px + s * 18, yf - 8, yb + 3, vz, 2.0) + ycyl(px + s * 18, yb, yb + 3, vz, 3.6) for s in (-1, 1))

    # 14 sample line: saddle tee and isolation valve on the riser, strainer, check valve and
    #    regulator screwed in a line; 1/4 in tube to the valve; valve to the cell inlet
    ro = p["riser_od"] / 2
    tz = p["tee_z"]
    tr = p["tube_od"] / 2
    tee = (zcyl(0, 0, tz, ro + 7, 60) - zcyl(0, 0, tz, ro, 62)) + xcyl(ro + 6, ro + 30, 0, tz, 10)
    iso = span(ro + 30, ro + 54, -11, 11, tz - 11, tz + 11) + tube((ro + 42, 0, tz + 11), (ro + 42, 0, tz + 40), 3)
    train = (iso + xcyl(ro + 54, ro + 60, 0, tz, 7) + xcyl(ro + 60, ro + 90, 0, tz, 12) + xcyl(ro + 90, ro + 93, 0, tz, 7)
             + xcyl(ro + 93, ro + 102, 0, tz, 9) + xcyl(ro + 102, ro + 105, 0, tz, 7) + xcyl(ro + 105, ro + 155, 0, tz, 11))
    C["tee"] = tee
    C["fittings"] = train
    xt = px + p["tube_x"]
    C["supply_tube"] = path([(ro + 155, 0, tz), (xt, 0, tz), (xt, vy, tz), (xt, vy, vz), (px + vw / 2, vy, vz)], tr)
    C["cell_tube"] = path([(px - vw / 2, vy, vz), (in_x, vy, vz), (in_x, vy, D["cell_bot"] - 20)], tr)
    C["inlet_fit"] = zcyl(in_x, in_y, D["cell_bot"] - 10, 5, 20) + zcyl(in_x, in_y, D["cell_bot"] + w / 2, 4.25, w)

    # 15 drain: outlet fitting through the +X wall, tee with the open air-break vent, hose to the basin
    ox = px + co[0] / 2 + 22
    C["outlet_fit"] = xcyl(px + cix / 2, px + co[0] / 2, oy, out_z, 8.5) + xcyl(px + co[0] / 2, ox - 8, oy, out_z, 6.5)
    vent = tube((ox, oy, out_z - 8), (ox, oy, out_z + p["vent_h"]), 8) - tube((ox, oy, out_z), (ox, oy, out_z + p["vent_h"] + 1), 6)
    dx_, dy_, dz_ = p["drain_end"]
    hose = path([(ox, oy, out_z - 8), (ox, oy, 350), (ox, dy_, dz_), (dx_, dy_, dz_)], p["hose_od"] / 2)
    C["drain"] = vent + hose

    # 2 panel on the bought pole-top tilt mount
    sr, sl = p["sleeve"]
    ptop = p["pole_h"]
    sleeve = zcyl(px, py, ptop - sl / 2 + 5, sr, sl) - zcyl(px, py, ptop - sl / 2, pr + 0.4, sl)
    pnw, pnh, pnt = p["panel"]
    pz = D["panel_z"]
    tilt = math.radians(p["panel_tilt"])
    n = (0.0, -math.sin(tilt), math.cos(tilt))
    pc = (px, py - 40, pz)
    C["panel"] = b.Pos(*pc) * b.Rot(p["panel_tilt"], 0, 0) * b.Box(pnw, pnh, pnt)
    rail_c = tuple(pc[i] - (pnt / 2 + 2) * n[i] for i in range(3))
    rail = b.Pos(*rail_c) * b.Rot(p["panel_tilt"], 0, 0) * b.Box(60, 150, 4)
    arm_end = tuple(rail_c[i] - 1.5 * n[i] for i in range(3))
    arm = tube((px, py, ptop + 4), arm_end, 10)
    C["panel_mount"] = sleeve + rail + arm

    # 16 cables: each from its part to its gland, clear of everything else; panel lead down the back of the pole
    cr = p["cable_d"] / 2
    gz = zb - 18                                                        # under the gland bodies
    c45 = (pr + 14) / SQ2
    jb = tuple(pc[i] - (pnt / 2) * n[i] + (-60.0 if i == 0 else 0.0) for i in range(3))     # junction box, beside the rail
    pl_x, pl_y = pen_xy["panel"]
    cables = {
        "panel_lead": [jb, tuple(jb[i] - 15 * n[i] for i in range(3)), (px - c45, py + c45, ptop - sl - 10), (px - c45, py + c45, 1060),
                       (pl_x, py + c45, 1060), (pl_x, pl_y, 1060), (pl_x, pl_y, gz)],
        "valve_cable": [(px, vy, vz + vh / 2 + 34), (px, vy, vz + vh / 2 + 40), (px, yf - 10, vz + vh / 2 + 44), (px - 80, yf - 10, vz + vh / 2 + 44),
                        (px - 80, yf - 10, 1080), (pen_xy["valve"][0], pen_xy["valve"][1], 1080), (*pen_xy["valve"], gz)],
        "chlorine_cable": [(clx, cly, cl_bot + p["cl_len"]), (clx, cly, cl_bot + p["cl_len"] + 20),
                           (pen_xy["chlorine"][0], pen_xy["chlorine"][1], cl_bot + p["cl_len"] + 40), (*pen_xy["chlorine"], gz)],
        "temp_cable": [(tx, ty, t_bot + p["t_len"]), (tx, ty, t_bot + p["t_len"] + 20),
                       (pen_xy["temp"][0], pen_xy["temp"][1], 1010), (*pen_xy["temp"], gz)],
        "optics_cable": [(px - co[0] / 2 - hd / 2, yb_, cav_z + hh / 2), (px - co[0] / 2 - hd / 2, yb_, 1100),
                         (pen_xy["optics"][0], pen_xy["optics"][1], 1100), (*pen_xy["optics"], gz)],
    }
    for k, pts in cables.items():
        C[k] = path(pts, cr)
    # the panel lead leaves the junction box on the back of the panel
    return C


# BOM line for each component (bom/bom.csv)
BOM_OF = {
    "pole": 1, "enc_saddle_0": 1, "enc_saddle_1": 1, "enc_ubolt_0": 1, "enc_ubolt_1": 1,
    "cell_saddle_0": 1, "cell_saddle_1": 1, "cell_ubolt_0": 1, "cell_ubolt_1": 1,
    "panel": 2, "panel_mount": 2, "enc_base": 3, "enc_lid": 4, "battery": 5, "board": 6, "modem": 7,
    "antenna": 8, "cell_body": 9, "gasket": 9, "cell_lid": 9, "lid_glands": 9, "plug": 9, "studs": 9,
    "led_holder": 10, "ref_holder": 10, "det90_holder": 10, "chlorine": 11, "temp": 12, "valve": 13,
    "tee": 14, "fittings": 14, "supply_tube": 14, "cell_tube": 14, "inlet_fit": 14,
    "drain": 15, "outlet_fit": 15,
    "status_lens": 21, "status_holder": 21, "status_led": 21, "status_cable": 21,
    "glands": 16, "panel_lead": 16, "valve_cable": 16, "chlorine_cable": 16, "temp_cable": 16, "optics_cable": 16,
    "shield": 17, "enc_plate": 18, "cell_plate": 18, "lugs": 19, "mplate": 19,
    "lug_screws": 20, "mplate_screws": 20, "shield_screws": 20, "cell_screws": 20, "valve_screws": 20,
}

GROUPS = {   # build_parts() key: components (old keys kept so the media scripts keep working)
    "pole": ["pole", "enc_saddle_0", "enc_saddle_1", "enc_ubolt_0", "enc_ubolt_1", "cell_saddle_0", "cell_saddle_1",
             "cell_ubolt_0", "cell_ubolt_1"],
    "panel": ["panel", "panel_mount"], "enc_base": ["enc_base"], "enc_lid": ["enc_lid"], "battery": ["battery"],
    "board": ["board"], "modem": ["modem"], "antenna": ["antenna"],
    "cell": ["cell_body", "gasket", "cell_lid", "lid_glands", "plug", "studs"],
    "turb": ["led_holder", "ref_holder", "det90_holder"], "chlorine": ["chlorine"], "temp": ["temp"], "valve": ["valve"],
    "sample": ["tee", "fittings", "supply_tube", "cell_tube", "inlet_fit"], "drain": ["drain", "outlet_fit"],
    "cables": ["glands", "panel_lead", "valve_cable", "chlorine_cable", "temp_cable", "optics_cable"],
    "shield": ["shield"], "status": ["status_lens", "status_holder", "status_led", "status_cable"], "plates": ["enc_plate", "cell_plate"], "fixings": ["lugs", "mplate"],
    "screws": ["lug_screws", "mplate_screws", "shield_screws", "cell_screws", "valve_screws"],
}


def build_parts(p=PARAMS, below_ground=True):
    """Return {key: solid} grouped by BOM line (and the footing, which is site supplied)."""
    C = build_components(p, below_ground)
    parts = {k: fuse(C[c] for c in v) for k, v in GROUPS.items()}
    if "footing" in C:
        parts["footing"] = C["footing"]
    return parts


BOM_ORDER = [("pole", 1), ("panel", 2), ("enc_base", 3), ("enc_lid", 4), ("battery", 5), ("board", 6),
             ("modem", 7), ("antenna", 8), ("cell", 9), ("turb", 10), ("chlorine", 11), ("temp", 12),
             ("valve", 13), ("sample", 14), ("drain", 15), ("cables", 16), ("shield", 17), ("plates", 18),
             ("fixings", 19), ("screws", 20), ("status", 21)]


def riser_context(p=PARAMS):
    """Existing tapstand riser stub (grey on the drawing); not in the BOM."""
    return zcyl(0, 0, p["riser_h"] / 2, p["riser_od"] / 2, p["riser_h"])


def assembly(p=PARAMS, with_riser=False):
    b = _b3d()
    parts = build_parts(p)
    kids = list(parts.values()) + ([riser_context(p)] if with_riser else [])
    return b.Compound(children=kids)


# ----------------------------------------------------------------------------- constructability checks
# Every pair that must touch (a fixing or a seat), and every pair that must stay apart by a clearance.
TOUCH = [
    ("pole", "footing"), ("panel_mount", "pole"), ("panel", "panel_mount"),
    ("enc_saddle_0", "pole"), ("enc_saddle_1", "pole"), ("enc_saddle_0", "enc_plate"), ("enc_saddle_1", "enc_plate"),
    ("enc_ubolt_0", "pole"), ("enc_ubolt_1", "pole"), ("enc_ubolt_0", "enc_plate"), ("enc_ubolt_1", "enc_plate"),
    ("cell_saddle_0", "pole"), ("cell_saddle_1", "pole"), ("cell_saddle_0", "cell_plate"), ("cell_saddle_1", "cell_plate"),
    ("cell_ubolt_0", "pole"), ("cell_ubolt_1", "pole"), ("cell_ubolt_0", "cell_plate"), ("cell_ubolt_1", "cell_plate"),
    ("enc_base", "enc_plate"), ("lugs", "enc_base"), ("lugs", "enc_plate"), ("lug_screws", "lugs"), ("lug_screws", "enc_plate"),
    ("enc_lid", "enc_base"), ("mplate", "enc_base"), ("mplate_screws", "mplate"),
    ("battery", "mplate"), ("board", "mplate"), ("modem", "mplate"),
    ("glands", "enc_base"), ("antenna", "enc_base"),
    ("shield", "enc_plate"), ("shield_screws", "shield"), ("shield_screws", "enc_plate"),
    ("cell_body", "cell_plate"), ("cell_screws", "cell_plate"), ("gasket", "cell_body"), ("cell_lid", "gasket"),
    ("lid_glands", "cell_lid"), ("plug", "cell_lid"), ("studs", "cell_lid"),
    ("led_holder", "cell_body"), ("ref_holder", "cell_body"), ("det90_holder", "cell_body"),
    ("chlorine", "lid_glands"), ("temp", "lid_glands"),
    ("valve", "cell_plate"), ("valve_screws", "valve"), ("valve_screws", "cell_plate"),
    ("tee", "fittings"), ("fittings", "supply_tube"), ("supply_tube", "valve"), ("cell_tube", "valve"),
    ("cell_tube", "inlet_fit"), ("inlet_fit", "cell_body"), ("outlet_fit", "cell_body"), ("drain", "outlet_fit"),
    ("panel_lead", "glands"), ("valve_cable", "glands"), ("chlorine_cable", "glands"), ("temp_cable", "glands"),
    ("optics_cable", "glands"), ("valve_cable", "valve"), ("chlorine_cable", "chlorine"), ("temp_cable", "temp"),
    ("optics_cable", "led_holder"), ("panel_lead", "panel"),
    ("status_lens", "shield"), ("status_holder", "shield"), ("status_lens", "status_holder"), ("status_led", "status_lens"),
    ("status_led", "status_holder"), ("status_cable", "status_holder"), ("status_cable", "glands"),
]
CLEAR = [   # (a, b, minimum gap in mm, why)
    ("enc_ubolt_0", "shield", 2, "the shield slides off past the lower U-bolt nuts"),
    ("enc_ubolt_1", "shield", 2, "the shield top clears the upper U-bolt nuts"),
    ("lugs", "shield", 2, "the shield slides off past the lugs"),
    ("shield", "enc_base", 10, "25 mm ventilated gap on top, sides and front; flanges 12 mm from the box at the back"),
    ("shield", "enc_lid", 20, "ventilated gap in front of the lid"),
    ("status_holder", "enc_lid", 10, "the lens unit stays clear of the clear lid"),
    ("status_cable", "antenna", 20, "status lead clear of the antenna whip"),
    ("chlorine", "cell_body", 2, "chlorine sensor clear of the walls"),
    ("temp", "cell_body", 2, "temperature probe clear of the walls"),
    ("chlorine", "temp", 10, "probes apart"),
    ("battery", "board", 2, ""), ("battery", "modem", 2, ""), ("board", "modem", 2, ""),
    ("battery", "glands", 15, "room for cables to bend up inside the box"),
    ("mplate", "glands", 15, "room for cables to bend up inside the box"),
    ("cell_tube", "valve", 0, ""), ("antenna", "drain", 50, "whip clear of the air-break vent"),
    ("supply_tube", "cell_ubolt_0", 3, ""), ("drain", "cell_ubolt_0", 3, ""),
]


def beam(p=PARAMS):
    """The light path: LED window to reference window, and the 90 degree detector's line of sight."""
    D = derived(p)
    px = p["pole_x"]
    cix, ciy, _ = p["cell_in"]
    yb_ = D["cell_y"] + p["beam_y"]
    r = p["win_d"] / 2
    along = xcyl(px - cix / 2, px + cix / 2, yb_, D["cav_z"], r)
    sight = ycyl(px + p["det90_x"], D["cell_y"] - ciy / 2, D["cell_y"] + ciy / 2, D["cav_z"], r)
    return along, sight


def run_checks(p=PARAMS, verbose=True):
    import itertools
    C = build_components(p)
    res = []

    def inter(a, b):
        try:
            return (C[a] & C[b]).volume
        except Exception:
            return 0.0

    for a, b in TOUCH:
        d = C[a].distance_to(C[b])
        v = inter(a, b)
        res.append((d < 0.05 and v < 1.0, f"touch  {a} / {b}: gap {d:.2f} mm, overlap {v:.1f} mm3"))
    for a, b, g, why in CLEAR:
        d = C[a].distance_to(C[b])
        res.append((d >= g and inter(a, b) < 1.0, f"clear  {a} / {b}: {d:.1f} mm (needs {g}) {why}"))
    # nothing overlaps anything else
    keys = list(C)
    bbs = {k: C[k].bounding_box() for k in keys}
    for a, b in itertools.combinations(keys, 2):
        A, B = bbs[a], bbs[b]
        if A.max.X < B.min.X or B.max.X < A.min.X or A.max.Y < B.min.Y or B.max.Y < A.min.Y or A.max.Z < B.min.Z or B.max.Z < A.min.Z:
            continue
        v = inter(a, b)
        if v >= 1.0:
            res.append((False, f"overlap {a} / {b}: {v:.1f} mm3"))
    res.append((True, f"overlap scan of {len(keys)} components done"))
    # the optics see only water
    along, sight = beam(p)
    for k in ("chlorine", "temp", "cell_body", "plug", "inlet_fit"):
        for nm, s in (("beam", along), ("sight line", sight)):
            if k == "cell_body":
                x_ = s & C[k]
                v = x_.volume if x_ is not None else 0.0
                res.append((v < 1.0, f"optics {nm} / {k}: {v:.1f} mm3 in the way (baffle and walls)"))
            else:
                d = s.distance_to(C[k])
                res.append((d >= 2.0, f"optics {nm} / {k}: {d:.1f} mm clear"))
    # the beam is under water when the cell stands full to the outlet's lower edge
    D = derived(p)
    lvl = D["outlet_z"] - p["outlet_id"] / 2
    res.append((D["cav_z"] + p["win_d"] / 2 + 5 <= lvl, f"water: standing level {lvl:.0f}, top of the windows {D['cav_z'] + p['win_d'] / 2:.0f}"))
    ok = all(r[0] for r in res)
    if verbose:
        for good, msg in res:
            print(("PASS " if good else "FAIL ") + msg)
        print(f"{sum(r[0] for r in res)} of {len(res)} checks pass")
    return ok, res


if __name__ == "__main__":
    if "--check" in sys.argv:
        ok, _ = run_checks()
        sys.exit(0 if ok else 1)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {
        "waterwatch-assembly": list(P.values()),
        "flow-cell": [P[k] for k in ("cell", "turb", "chlorine", "temp", "valve")] + [build_components()["cell_plate"]],
        "enclosure": [P[k] for k in ("enc_base", "enc_lid", "battery", "board", "modem", "antenna", "shield", "fixings")]
        + [build_components()["enc_plate"]],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"cell water volume {D['cell_net_l']:.3f} L; sample tube {D['tube_l_mm']:.0f} mm, {D['tube_vol_l'] * 1000:.1f} mL; "
          f"overall height {D['overall_h']:.0f} mm above ground; pole axis {D['pole_y']:.1f} mm behind the enclosure centre")
