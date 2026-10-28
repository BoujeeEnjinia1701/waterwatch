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
    python .kit/cad_check.py --export  kit 1.9 fidelity check of every option (D3), STEP per part and per option
    python cad/src/model.py            part list with masses; STEP and STL of the chosen design (option A)
    python cad/src/model.py --check    run the TRL 3 constructability checks on build_components()
Exports (from components(CHOSEN), every part and fastener):
    waterwatch-assembly.step / .stl   the whole sentinel, pole set in its footing
    flow-cell.step / .stl             flow cell, optics, sensors, lid, cell plate, valve and their fixings
    enclosure.step / .stl             enclosure, parts inside, back plate, sun shield and their fixings

Kit 1.9 (STANDARDS section 24): OPTIONS, PRINCIPLES, CHOSEN, OPTION_VIEWS and components(option) below model
every concept option of WWT-OPT-001 to detail level D3 with .kit/cad_parts.py and cad/src/wwt_parts.py.
build_components() keeps the TRL 3 geometry of option A, which components("A") splits into its parts; the
sizing script, the build plan pictures and the making sketches read it.

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
    for hx, hz in ((px - 30, ez + 35), (px - 30, ez - 62)):      # battery tray screws (WWT-DEC-001 F3)
        C["mplate"] = C["mplate"] - ycyl(hx, my1 - mt - 1, my1 + 1, hz, 1.7)
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
    C["cell_tube"] = C["cell_tube"] + zcyl(in_x, vy, 755.0, 6.0, 30.0)      # inline check valve at the cell inlet (WWT-DEC-001 F8)
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


def assembly(p=PARAMS, with_riser=False, detailed=True):
    """The chosen design as one compound: every part of components(CHOSEN) (kit 1.9, D3), or the grouped TRL 3
    parts of build_parts() with detailed=False; optionally with the riser stub."""
    b = _b3d()
    if detailed:
        kids = [q["shape"] for q in components(CHOSEN) if q["kind"] != "context"]
    else:
        kids = list(build_parts(p).values())
    kids += [riser_context(p)] if with_riser else []
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


# ============================================================================================ kit 1.9 interface
# STANDARDS section 24. Every concept option (WWT-OPT-001) is modelled to D3 here and returned by
# components(option) as cad_parts.part() dicts. Option A is the existing design: the same geometry as
# build_components() above, split into its individual parts, with every bolt, nut, washer, screw, stud and
# standoff modelled from .kit/cad_parts.py and cad/src/wwt_parts.py. Options B and C are the alternatives
# scored in WWT-OPT-001 (proposed, awaiting Amish); they are modelled to the same level so the choice can be
# made on real geometry. BOM line numbers are given for option A only.

TITLE = "WaterWatch"
OPTIONS = {"A": "Timed-flush flow cell on its own pole",
           "B": "Reagent colorimetric analyser cabinet",
           "C": "In-riser probe manifold"}
PRINCIPLES = {
    "A": "An hourly 90 s flush through a small dark flow cell beside the tapstand; reagent-free: an 860 nm "
         "nephelometer and a membrane-free amperometric chlorine sensor read the water as it flows.",
    "B": "An hourly sample is drawn into a glass cuvette, dosed with DPD reagent by two micro pumps and read by an "
         "LED photometer at 515 nm (chlorine) and 860 nm (turbidity); the reacted sample goes to drain.",
    "C": "Probes sit in a manifold cut into the tapstand riser and read the water while people draw it: ORP and pH "
         "electrodes (potentiometric) estimate free chlorine, an insertion head reads turbidity; no flushing.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 20, "az": -50, "scale": "person", "keep_context": True, "ground_z": 0} for k in OPTIONS}
# Substring pairs whose solids are allowed to share a little volume (a modelled thread engagement).
ALLOWED_CONTACTS = []


def _kit():
    sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[2] / ".kit")]
    import cad_parts as cp
    import wwt_parts as W
    return cp, W


class _Parts(list):
    """Collects cad_parts.part() dicts."""

    def __init__(self, xf=None):
        super().__init__()
        self.xf = xf

    def add(self, name, shape, material, kind="made", bom=None, group="shell", explode=(0, 0, 0)):
        cp, _ = _kit()
        if self.xf is not None:
            shape = self.xf * shape
        self.append(cp.part(name, shape, material, kind=kind, bom=bom, group=group, explode=explode))

    def fasteners(self, items, bom=None, material="stainless", group="shell"):
        for nm, s in items:
            self.add(nm, s, material, "fastener", bom, group)


def ubolt_bare(p, D, x, z):
    """U-bolt round the back of the pole (rod and bend only); legs through the saddle and plate."""
    b = _b3d()
    pr = p["pole_od"] / 2
    rr = p["ub_d"] / 2
    R = p["ub_x"]
    c = D["pole_y"] - (R - rr - pr)
    tor = b.Pos(x, c, z) * b.Torus(R, rr)
    tor = tor & span(x - R - rr - 1, x + R + rr + 1, c, c + R + rr + 1, z - rr - 1, z + rr + 1)
    yf = D["plate_front"]
    legs = fuse(ycyl(x + s * R, yf - 13, c, z, rr) for s in (-1, 1))
    return tor + legs


def _pole_clamps(out, p, D, x, zs, label, bom=None, d=8):
    """V-saddles, U-bolts, washers and nuts for each height in zs (legacy saddle and U-bolt geometry)."""
    cp, W = _kit()
    b = _b3d()
    yf = D["plate_front"]
    for i, z in enumerate(zs):
        pos = "lower" if i == 0 else "upper"
        out.add(f"V-saddle, {label} {pos}", saddle(p, D, x, z), "galvanised", "bought", bom)
        out.add(f"M{d} U-bolt, {label} {pos}", ubolt_bare(p, D, x, z), "galvanised", "bought", bom)
        for s in (-1, 1):
            xx = x + s * p["ub_x"]
            out.add(f"M{d} washer (ISO 7089), {label}", W.put(W.washer(d), (xx, yf, z), "-y"), "stainless", "fastener", bom)
            out.add(f"M{d} nut (ISO 4032), {label}", W.put(b.Pos(0, 0, W.washer_h(d)) * W.nut(d), (xx, yf, z), "-y"),
                    "stainless", "fastener", bom)


def _panel(out, px, py, ptop, pr, rise, tilt, pnw, pnh, pnt, bom=None, sleeve=(30.0, 85.0), dy=-40.0):
    """5 W panel on a bought pole-top tilt mount: framed module, laminate, junction box, sleeve with two set
    screws, arm and rail, four M5 bolts. Returns (junction box cable point, panel normal)."""
    cp, W = _kit()
    b = _b3d()
    sr, sl = sleeve
    pz = ptop + rise
    n = (0.0, -math.sin(math.radians(tilt)), math.cos(math.radians(tilt)))
    pc = (px, py + dy, pz)
    T = b.Pos(*pc) * b.Rot(tilt, 0, 0)
    loc = W.panel_local(pnw, pnh, pnt)
    hb = pnt / 2
    holes = [(sx * 20.0, sy * (pnh / 2 - 8.0)) for sx in (-1, 1) for sy in (-1, 1)]
    frame = loc["frame"]
    for hx, hy in holes:
        frame = frame - b.Pos(hx, hy, -hb + 1) * b.Cylinder(2.75, 4)
    out.add("Solar panel frame, aluminium", T * frame, "aluminium", "bought", bom)
    out.add("Solar panel laminate, 5 W monocrystalline", T * cp.break_edges(loc["laminate"], 0.5), "glass", "bought", bom)
    out.add("Solar panel junction box", T * loc["jbox"], "hdpe_black", "bought", bom)
    rail = W.span(-30, 30, -pnh / 2, pnh / 2, -hb - 4, -hb)
    for hx, hy in holes:
        rail = rail - b.Pos(hx, hy, -hb - 2) * b.Cylinder(2.75, 6)
    rail = cp.break_edges(rail, 0.6)
    rail_c = tuple(pc[i] - (hb + 2) * n[i] for i in range(3))
    arm_end = tuple(rail_c[i] - 1.5 * n[i] for i in range(3))
    arm = W.cyl_between((px, py, ptop + 4), arm_end, 10)
    sleeve_s = zcyl(px, py, ptop - sl / 2 + 5, sr, sl) - zcyl(px, py, ptop - sl / 2, pr + 0.4, sl)
    zs = (ptop - sl + 25, ptop - 18)
    for zz in zs:
        sleeve_s = sleeve_s - xcyl(px + pr - 1, px + sr + 1, py, zz, 3.0)
    out.add("Pole-top tilt mount (sleeve, arm and rail)", sleeve_s + arm + T * rail, "galvanised", "bought", bom)
    for zz in zs:
        out.add("M6x10 socket set screw", W.put(W.set_screw(6, 10), (px + pr + 0.5, py, zz), "+x"), "stainless", "fastener", bom)
    for hx, hy in holes:
        for nm, s in W.bolt_set(5, 16, (hx, hy, -hb + 2), "-z", grip=6):
            out.add(nm + " (panel to rail)", T * s, "stainless", "fastener", bom)
    jb = tuple(pc[i] - hb * n[i] + (-60.0 if i == 0 else 0.0) for i in range(3))
    return jb, n


# ----------------------------------------------------------------------------------------------- option A
def _option_a(p=PARAMS):
    cp, W = _kit()
    b = _b3d()
    C = build_components(p)
    D = derived(p)
    out = _Parts()
    px, py = p["pole_x"], D["pole_y"]
    yf, yb = D["plate_front"], D["plate_back"]
    ew, ed, eh = p["enc"]
    ez = p["enc_z"]
    t, lt = p["enc_wall"], p["lid_t"]
    zb = ez - eh / 2
    pr = p["pole_od"] / 2

    # site context and the pole (BOM line 1)
    out.add("Existing tapstand riser (site)", zcyl(0, 0, (p["riser_h"] - 300) / 2, p["riser_od"] / 2, p["riser_h"] + 300),
            "galvanised", "context", None, "context")
    out.add("Concrete footing 300 mm (site)", C["footing"], "concrete", "context", None, "context")
    out.add("Mounting pole, 48.3 x 3.2 mm galvanised tube", C["pole"], "galvanised", "bought", 1, "pole")
    _pole_clamps(out, p, D, px, D["enc_ub_z"], "enclosure plate", 1)
    _pole_clamps(out, p, D, px, p["cell_ub_z"], "cell plate", 1)

    # 18 back plates
    out.add("Enclosure back plate, 270 x 420 x 3 mm aluminium", cp.break_edges(C["enc_plate"], 0.6), "aluminium", "made", 18)
    out.add("Cell back plate, 140 x 385 x 3 mm aluminium", cp.break_edges(C["cell_plate"], 0.6), "aluminium", "made", 18)

    # 3, 4 enclosure base with four corner posts for the lid screws; lid; four lid screws
    posts, lid = [], C["enc_lid"]
    base = C["enc_base"]
    corners = [(px + s * (ew / 2 - t - 5), ez + q * (eh / 2 - t - 5)) for s in (-1, 1) for q in (-1, 1)]
    for cx_, cz_ in corners:
        post = span(cx_ - 5, cx_ + 5, -ed / 2 + lt, -ed / 2 + lt + 20, cz_ - 5, cz_ + 5)
        base = base + post - ycyl(cx_, -ed / 2 + lt - 1, -ed / 2 + lt + 16, cz_, 2.0)
        lid = lid - ycyl(cx_, -ed / 2 - 1, -ed / 2 + lt + 1, cz_, 2.2)
    out.add("Enclosure base, IP66 polycarbonate", base, "polycarbonate", "bought", 3, "enclosure")
    out.add("Enclosure lid, clear polycarbonate", lid, "polycarbonate", "bought", 4, "enclosure")
    for cx_, cz_ in corners:
        out.fasteners(W.screw_into(4, 16, (cx_, -ed / 2, cz_), "+y"), 4)

    # 16 glands, vent and 8 antenna on the bottom face
    pen_xy = {k: (px + x, ed / 2 - p["pen_rows"][row]) for k, (x, row) in p["pens"].items()}
    for k, (x, y) in pen_xy.items():
        if k == "antenna":
            continue
        if k == "vent":
            body, ln = W.gland(12, t, 17, 15, 8, 2.0, nut_h_=4.0)
            out.add("M12 pressure-equalising vent", W.put(body, (x, y, zb), "+z"), "hdpe_black", "bought", 16)
            out.add("M12 vent locknut", W.put(ln, (x, y, zb), "+z"), "hdpe_black", "fastener", 16)
        else:
            body, ln = W.gland(16, t, 22, 19, 10, 7.0)
            what = {"ph_spare": "spare", "status": "status light lead"}.get(k, k + " cable")
            out.add(f"M16 IP68 cable gland ({what})", W.put(body, (x, y, zb), "+z"), "hdpe_black", "bought", 16)
            out.add("M16 gland locknut", W.put(ln, (x, y, zb), "+z"), "hdpe_black", "fastener", 16)
    ax_, ay_ = pen_xy["antenna"]
    ad, al = p["antenna"]
    ant = (zcyl(ax_, ay_, zb + t / 2 + 4, 3.2, t + 8) + zcyl(ax_, ay_, zb - 6, ad / 2, 12)
           + zcyl(ax_, ay_, zb - 12 - (al - 12) / 2, 5, al - 12))
    out.add("LTE and GSM whip antenna on SMA bulkhead", cp.break_edges(ant, 0.4), "matte_black", "bought", 8)
    out.add("SMA bulkhead nut", W.put(W.hexp(8, 4) - b.Pos(0, 0, 2) * b.Cylinder(3.2, 5), (ax_, ay_, zb + t), "+z"),
            "brass", "fastener", 8)

    # 19 lugs (maker's kit) with 20 M5 bolts through the back plate
    lw, lth, lh = p["lug"]
    lx, lz = p["lug_x"], eh / 2 + 2 + p["lug"][2] / 2 + 1
    for s in (-1, 1):
        for q in (-1, 1):
            x = px + s * lx
            ze = ez + q * eh / 2
            foot = span(x - lw / 2, x + lw / 2, yf - 20, yf - lth, ze, ze + q * lth)
            tab = span(x - lw / 2, x + lw / 2, yf - lth, yf, ze + q * 2, ze + q * (2 + lh))
            lug = foot + tab - ycyl(x, yf - lth - 1, yf + 1, ez + q * lz, 2.75)
            out.add("Enclosure mounting lug", cp.break_edges(lug, 0.4), "stainless", "bought", 19, "enclosure")
            out.fasteners([(n + " (lug)", sh) for n, sh in W.bolt_set(5, 16, (x, yf - lth, ez + q * lz), "+y", grip=lth + p["plate_t"])], 20)

    # 19 internal plate on the moulded bosses, four M4 screws; holes for the battery tray screws
    mw, mh, mt = p["mplate"]
    mz = ez + p["mplate_z"] + mh / 2
    my1 = ed / 2 - t - p["mplate_gap"]
    mf = my1 - mt
    boss_pts = [(px + s * (mw / 2 - 10), mz + q * (mh / 2 - 10)) for s in (-1, 1) for q in (-1, 1)]
    tray_scr = [(px - 30, ez + 35), (px - 30, ez - 62)]
    mpl = C["mplate"]
    for hx, hz in tray_scr:
        mpl = mpl - ycyl(hx, mf - 1, my1 + 1, hz, 1.7)
    out.add("Internal plate, printed ASA", cp.break_edges(mpl, 0.5), "hdpe_natural", "made", 19, "internal")
    for bx_, bz_ in boss_pts:
        out.fasteners(W.screw_into(4, 9, (bx_, mf, bz_), "+y"), 20)

    # 5 battery: one 32700 LiFePO4 cell, 6 Ah (WWT-DEC-001 D-STM1), protection board and fuse in a tray
    bw, bd, bh = p["battery"]
    x0b, z0b = px - 85, ez - 72
    tray = W.rbox(x0b, x0b + bw, mf - bd, mf, z0b, z0b + bh, 1.0) - span(x0b + 2, x0b + bw - 2, mf - bd - 1, mf - 2, z0b + 2, z0b + bh - 2)
    for hx, hz in tray_scr:
        tray = tray - ycyl(hx, mf - 3, mf + 1, hz, 1.7)
    out.add("Battery tray", tray, "hdpe_black", "bought", 5, "internal")
    out.add("LiFePO4 cell 32700, 3.2 V 6 Ah", W.put(cp.round_bar(32, 70, 1.0), (x0b + 19, mf - 19, ez - 60), "+z"), "mild_steel", "bought", 5, "internal")
    out.add("Battery protection board with NTC", W.board_xz(px - 45, px - 12, ez - 50, ez, mf - 2), "hdpe_recycled", "bought", 5, "internal")
    out.add("Battery fuse holder", W.chip(px - 40, px - 22, mf - 9.6, mf - 3.6, ez - 44, ez - 30), "hdpe_black", "bought", 5, "internal")
    out.add("Protection IC and MOSFETs", W.chip(px - 20, px - 15, mf - 4.6, mf - 3.6, ez - 20, ez - 8), "matte_black", "bought", 5, "internal")
    for hx, hz in tray_scr:
        out.fasteners(W.screw_into(3, 8, (hx, mf - 2, hz), "+y"), 20)
        out.add("M3 nut (ISO 4032)", W.put(W.nut(3), (hx, my1, hz), "+y"), "stainless", "fastener", 20)

    # 6 controller and 7 modem on M3 standoffs
    so = p["standoff"]

    def carrier(x0, x1, z0, z1, label, bom, comps):
        holes = [(xx, zz) for xx in (x0 + 5, x1 - 5) for zz in (z0 + 5, z1 - 5)]
        yb_ = mf - so
        out.add(label, W.board_xz(x0, x1, z0, z1, yb_, 1.6, holes), "hdpe_recycled", "bought", bom, "internal")
        for xx, zz in holes:
            out.add("M3 x 6 hex standoff, nylon", W.put(W.hex_standoff(5.5, so, 3.2), (xx, yb_, zz), "+y"), "hdpe_natural", "fastener", 20, "internal")
            out.fasteners(W.screw_into(3, 6, (xx, yb_ - 1.6, zz), "+y"), 20)
        for nm, (a0, a1, c0, c1, depth) in comps.items():
            out.add(nm, W.chip(x0 + a0, x0 + a1, yb_ - 1.6 - depth, yb_ - 1.6, z0 + c0, z0 + c1), "matte_black", "bought", bom, "internal")
    cw, cd, ch = p["board"]
    carrier(px, px + cw, ez - 45, ez - 45 + ch, "Controller carrier board", 6,
            {"ESP32-S3 module": (10, 28, 75, 100.5, 3.1), "Potentiostat front end (LMP91000 class)": (40, 50, 75, 85, 1.2),
             "LiFePO4 solar charger with inductor": (55, 75, 25, 45, 4.0), "12 V boost valve driver": (12, 30, 10, 30, 5.0),
             "microSD socket and real-time clock": (55, 80, 90, 105, 2.0), "Board connectors": (35, 78, 2, 10, 8.0)})
    mw_, md_, mh_ = p["modem"]
    carrier(px - 75, px - 75 + mw_, ez + 60, ez + 60 + mh_, "Cellular modem board (SIM7000G class)", 7,
            {"LTE-M and NB-IoT module": (12, 42, 12, 42, 2.5), "SIM holder": (46, 62, 14, 34, 2.0),
             "Antenna lead connector": (46, 54, 38, 44, 2.5)})

    # 17 sun shield and four M5 thumb screws; 21 status light
    out.add("Sun shield, white powder-coated aluminium", C["shield"], "aluminium", "bought", 17, "enclosure")
    st = p["shield_t"]
    sx = ew / 2 + p["shield_gap"] - p["shield_flange"] / 2
    sz = eh / 2 - 20
    for s in (-1, 1):
        for q in (-1, 1):
            out.add("M5 knurled thumb screw", W.put(W.thumb_screw(4.8, st + p["plate_t"] + 2, 12, 6), (px + s * sx, yf - st, ez + q * sz), "-y"),
                    "stainless", "fastener", 20)
    out.add("Status light lens, polycarbonate", cp.break_edges(C["status_lens"], 0.3), "polycarbonate", "made", 21)
    out.add("Status light holder, printed ASA", C["status_holder"], "hdpe_natural", "made", 21)
    out.add("Status light LED, 5 mm bi-colour", cp.break_edges(C["status_led"], 0.6), "polycarbonate", "bought", 21)
    out.add("Status light lead", C["status_cable"], "epdm", "bought", 21)

    # 9 flow cell: body with tapped holes for the optics holder screws, gasket, lid, glands, plug, studs, nuts
    cix, ciy, ciz = p["cell_in"]
    w, wb = p["cell_wall"], p["cell_back"]
    co = D["cell_out"]
    cz, cy = p["cell_z"], D["cell_y"]
    cav_z = D["cav_z"]
    yb_ = cy + p["beam_y"]
    by0 = cy - ciy / 2 - w
    hw, hh, hd = p["holder"]
    planes = {"led": ((px - co[0] / 2, yb_, cav_z), (1, 0, 0), (0, 1, 0)),
              "ref": ((px + co[0] / 2, yb_, cav_z), (-1, 0, 0), (0, -1, 0)),
              "det90": ((px + p["det90_x"], by0, cav_z), (0, 1, 0), (-1, 0, 0))}

    def on_wall(key, shape):
        o, zd, xd = planes[key]
        return b.Plane(origin=o, x_dir=xd, z_dir=zd).from_local_coords(shape)
    corners_h = [(sx_ * (hw / 2 - 3.5), sy_ * (hh / 2 - 3.5)) for sx_, sy_ in ((-1, -1), (1, 1))]
    body = C["cell_body"]
    for key in planes:
        for hx, hy in corners_h:
            body = body - on_wall(key, b.Pos(hx, hy, 3) * b.Cylinder(1.5, 6.02))
    out.add("Flow cell body, black PVC", body, "hdpe_black", "made", 9, "cell")
    for s in (-1, 1):
        out.fasteners(W.screw_into(5, 16, (px + s * 30, yb, cz), "-y", kind="hex", washer_under=True), 20)
    out.add("Flow cell gasket, 1.5 mm EPDM", C["gasket"], "epdm", "made", 9, "cell")
    out.add("Flow cell lid, black PVC", C["cell_lid"], "hdpe_black", "made", 9, "cell")
    ct = D["cell_top"]
    lt_mid = (D["lid_bot"] + ct) / 2
    ctt = p["cell_top_t"]
    clx, cly = px + p["cl_xy"][0], cy + p["cl_xy"][1]
    tx, ty = px + p["t_xy"][0], cy + p["t_xy"][1]
    gl_cl = zcyl(clx, cly, lt_mid, 12.5, ctt) + b.Pos(clx, cly, ct) * W.hexp(28, 7) + zcyl(clx, cly, ct + 11, 14, 8)
    gl_cl = gl_cl - zcyl(clx, cly, ct, 8.0, 60)
    out.add("M25 lid gland (chlorine sensor)", gl_cl, "hdpe_black", "bought", 9, "cell")
    gl_t = zcyl(tx, ty, lt_mid, 6.0, ctt) + b.Pos(tx, ty, ct) * W.hexp(14, 5) + zcyl(tx, ty, ct + 8.5, 7, 7)
    gl_t = gl_t - zcyl(tx, ty, ct, 3.0, 60)
    out.add("M12 lid gland (temperature probe)", gl_t, "hdpe_black", "bought", 9, "cell")
    out.add("M20 blanking plug (spare pH port)", cp.break_edges(C["plug"], 0.4), "hdpe_black", "bought", 9, "cell")
    for sx_, sy_ in p["studs"]:
        x, y = px + sx_, cy + sy_
        out.add("M4 stud, stainless", W.put(W.stud(4, ct + 8 - D["body_top"] + 10), (x, y, D["body_top"] - 10), "+z"), "stainless", "fastener", 9, "cell")
        out.add("M4 knurled thumb nut", W.put(W.knurled_nut(4, 12, 8), (x, y, ct), "+z"), "stainless", "fastener", 9, "cell")

    # 10 optics: three holders, each with two M3 screws, its window, and the LED or detector in its bore
    names = {"led": ("LED holder (left wall)", "860 nm infrared LED, 5 mm"),
             "ref": ("180 degree reference detector holder (right wall)", "Light-to-frequency detector, 180 degree reference"),
             "det90": ("90 degree scatter detector holder (front wall)", "Light-to-frequency detector, 90 degree scatter")}
    for key, (hn, en) in names.items():
        out.add(f"Optics {hn}", C[f"{key}_holder"], "matte_black", "made", 10, "cell")
        for hx, hy in corners_h:
            sc = b.Pos(hx, hy, -hd) * b.Rot(180, 0, 0) * W.pan_screw(3, hd + 5)
            out.add("M3x21 pan head screw (optics holder)", on_wall(key, sc), "stainless", "fastener", 20, "cell")
        em = cp.break_edges(b.Pos(0, 0, -5.5) * b.Cylinder(2.5, 9), 0.6)
        out.add(en, on_wall(key, em), "polycarbonate", "bought", 10, "cell")
        win = cp.break_edges(b.Pos(0, 0, 1.5) * b.Cylinder(5.8, 2.0), 0.3)
        out.add("Optical window, 2 mm acrylic", on_wall(key, win), "polycarbonate", "made", 10, "cell")

    # 11 chlorine sensor (PVC holder, three electrodes), 12 temperature probe
    cl_bot = D["body_top"] - p["cl_immersed"]
    out.add("Free chlorine sensor holder, PVC", W.put(cp.round_bar(p["cl_d"], p["cl_len"], 1.0), (clx, cly, cl_bot), "+z"), "hdpe_natural", "made", 11, "cell")
    for k, (en, mat) in enumerate((("Graphite working electrode", "matte_black"), ("Ag/AgCl reference electrode", "stainless"),
                                   ("Stainless counter electrode", "stainless"))):
        a = math.radians(90 + 120 * k)
        out.add(en, W.put(cp.round_bar(2.0, 3.0, 0.3), (clx + 4.5 * math.cos(a), cly + 4.5 * math.sin(a), cl_bot - 3), "+z"), mat, "bought", 11, "cell")
    t_bot = D["body_top"] - p["t_immersed"]
    out.add("Temperature probe, DS18B20 in a stainless sheath", W.put(cp.round_bar(p["t_d"], p["t_len"], 0.8), (tx, ty, t_bot), "+z"), "stainless", "bought", 12, "cell")

    # 13 latching valve and two M4 screws from behind the cell plate
    vz = D["valve_z"]
    out.add("Latching solenoid valve, 12 V, 1/4 in", cp.break_edges(C["valve"], 0.6), "hdpe_black", "bought", 13, "cell")
    for s in (-1, 1):
        out.fasteners(W.screw_into(4, 11, (px + s * 18, yb, vz), "-y"), 20)

    # 14 sample line: saddle tee clamp (two halves, two M6 bolts), isolation valve, nipples, strainer, check valve,
    #    regulator, tubes and push-fit elbows; 15 drain with air-break vent, hose and clamp
    ro = p["riser_od"] / 2
    tz = p["tee_z"]
    ring = zcyl(0, 0, tz, ro + 7, 60) - zcyl(0, 0, tz, ro, 62)
    halves = {"branch": span(0, 200, -100, 100, tz - 40, tz + 40), "back": span(-200, 0, -100, 100, tz - 40, tz + 40)}
    for hname, hs in halves.items():
        sgn = 1 if hname == "branch" else -1
        ears = fuse(span(0, sgn * 6, sy * (ro + 4), sy * (ro + 20), tz - 10, tz + 10) for sy in (-1, 1))
        half = (ring & hs) + ears
        for sy in (-1, 1):
            half = half - xcyl(-8, 8, sy * (ro + 13), tz, 3.3)
        if hname == "branch":
            half = half + xcyl(ro + 6, ro + 30, 0, tz, 10) - xcyl(ro - 1, ro + 31, 0, tz, 5.0)
        out.add(f"Saddle tee clamp, {hname} half (25 mm)", cp.break_edges(half, 0.4), "brass", "bought", 14, "sample")
    for sy in (-1, 1):
        out.fasteners([(n + " (saddle tee)", s_) for n, s_ in W.bolt_set(6, 25, (-6, sy * (ro + 13), tz), "+x", grip=12)], 14)
    iso = span(ro + 30, ro + 54, -11, 11, tz - 11, tz + 11)
    iso = cp.break_edges(iso, 1.0) + tube((ro + 42, 0, tz + 11), (ro + 42, 0, tz + 40), 3) + span(ro + 36, ro + 70, -4, 4, tz + 36, tz + 42)
    out.add("Isolation ball valve, 1/4 in", iso, "brass", "bought", 14, "sample")
    for x0_, x1_ in ((54, 60), (90, 93), (102, 105)):
        nip = b.Pos(ro + x0_, 0, tz) * b.Rot(0, 90, 0) * W.extrude(W.RegularPolygon(12 / W.SQ3, 6), x1_ - x0_)
        out.add("Brass hex nipple, 1/4 in", nip, "brass", "bought", 14, "sample")
    out.add("Strainer, 1/4 in", W.fitting(ro + 60, ro + 90, 12, 0, tz), "brass", "bought", 14, "sample")
    out.add("Check valve, 1/4 in", W.fitting(ro + 93, ro + 102, 9, 0, tz), "brass", "bought", 14, "sample")
    out.add("Pressure-compensating flow regulator, 0.5 L/min", W.fitting(ro + 105, ro + 155, 11, 0, tz), "hdpe_black", "bought", 14, "sample")
    out.add("Supply tube, 1/4 in food-grade PE", C["supply_tube"], "hdpe_natural", "bought", 14, "sample")
    # second check valve at the cell inlet, inline on the valve-to-cell tube (WWT-DEC-001 F8, after the STEM review)
    vw_ = p["valve"][0]
    vy_ = yf - p["valve"][1] / 2
    in_x_ = px + p["inlet_x"]
    cv0, cv1 = 740.0, 770.0
    trr = p["tube_od"] / 2
    out.add("Valve-to-check-valve tube, 1/4 in food-grade PE", W.path([(px - vw_ / 2, vy_, vz), (in_x_, vy_, vz), (in_x_, vy_, cv0)], trr),
            "hdpe_natural", "bought", 14, "sample")
    cvb = zcyl(in_x_, vy_, (cv0 + cv1) / 2, 6.0, cv1 - cv0 - 6)
    for z_ in (cv0, cv1 - 3):
        cvb = cvb + b.Pos(in_x_, vy_, z_) * W.extrude(W.RegularPolygon(11 / W.SQ3, 6), 3)
    out.add("Inline check valve, 1/4 in push-fit (cell inlet)", cvb, "hdpe_natural", "bought", 14, "sample")
    out.add("Check-valve-to-cell tube, 1/4 in food-grade PE", cp.break_edges(W.path([(in_x_, vy_, cv1), (in_x_, vy_, D["cell_bot"] - 20)], trr), 0.3),
            "hdpe_natural", "bought", 14, "sample")
    out.add("Cell inlet push-fit", C["inlet_fit"], "hdpe_black", "bought", 14, "sample")
    out.add("Cell outlet hose tail", C["outlet_fit"], "hdpe_black", "bought", 15, "sample")
    oy = cy + p["outlet_y"]
    out_z = D["outlet_z"]
    ox = px + co[0] / 2 + 22
    vent = W.cyl_between((ox, oy, out_z - 8), (ox, oy, out_z + p["vent_h"]), 8) - W.cyl_between((ox, oy, out_z), (ox, oy, out_z + p["vent_h"] + 1), 6)
    out.add("Air-break vent tee", vent, "hdpe_natural", "bought", 15, "sample")
    dx_, dy_, dz_ = p["drain_end"]
    out.add("Drain hose, 12 mm bore PVC", W.path([(ox, oy, out_z - 8), (ox, oy, 350), (ox, dy_, dz_), (dx_, dy_, dz_)], p["hose_od"] / 2),
            "hdpe_natural", "bought", 15, "sample")
    clamp = (zcyl(ox, oy, out_z - 22, 9.6, 8) - zcyl(ox, oy, out_z - 22, 8.0, 9)) + span(ox + 8.5, ox + 14, oy - 3, oy + 3, out_z - 26, out_z - 18)
    out.add("Hose clamp", clamp, "stainless", "fastener", 15, "sample")

    # 16 cables
    for k, nm in (("panel_lead", "Panel lead"), ("valve_cable", "Valve cable"), ("chlorine_cable", "Chlorine sensor cable"),
                  ("temp_cable", "Temperature probe cable"), ("optics_cable", "Optics cable")):
        out.add(nm, C[k], "epdm", "bought", 16, "cables")

    # 2 panel on the pole-top mount
    _panel(out, px, py, p["pole_h"], pr, p["panel_rise"], p["panel_tilt"], *p["panel"], bom=2, sleeve=p["sleeve"])
    return out


# ----------------------------------------------------------------------------------------------- shared cabinet
def _cabinet(out, w, d, h, lt=12.0, t=3.0, glands=(), layout="B", ant=None, hood=True, plate_t=3.0):
    """A wall-mount IP66 cabinet in local coordinates: back face at y = 0 on the back plate (the plate is in
    +Y), box from y = -d to 0, centre z = 0, lid at the front. Base with moulded bosses and lid-screw posts, clear
    lid, four lid screws, four lugs with M5 bolts through the plate, internal plate with four M4 screws, glands and
    vent in the bottom face, antenna, ventilated hood with four thumb screws. Returns the internal plate's front
    face y."""
    cp, W = _kit()
    b = _b3d()
    zb = -h / 2
    base = span(-w / 2, w / 2, -d + lt, 0, -h / 2, h / 2) - span(-w / 2 + t, w / 2 - t, -d + lt - 1, -t, -h / 2 + t, h / 2 - t)
    lid = span(-w / 2, w / 2, -d, -d + lt, -h / 2, h / 2) - span(-w / 2 + t, w / 2 - t, -d + t, -d + lt + 1, -h / 2 + t, h / 2 - t)
    corners = [(s * (w / 2 - t - 5), q * (h / 2 - t - 5)) for s in (-1, 1) for q in (-1, 1)]
    for cx_, cz_ in corners:
        base = base + span(cx_ - 5, cx_ + 5, -d + lt, -d + lt + 20, cz_ - 5, cz_ + 5) - ycyl(cx_, -d + lt - 1, -d + lt + 16, cz_, 2.0)
        lid = lid - ycyl(cx_, -d - 1, -d + lt + 1, cz_, 2.2)
    mw, mh, mt, gap = w - 2 * t - 8, h - 2 * t - 16, 3.0, 6.0
    my1 = -t - gap
    mf = my1 - mt
    bosses = [(s * (mw / 2 - 10), q * (mh / 2 - 10)) for s in (-1, 1) for q in (-1, 1)]
    for bx_, bz_ in bosses:
        base = base + (ycyl(bx_, my1, -t + 0.5, bz_, 5) - ycyl(bx_, my1 - 1, -t, bz_, 2.0))
    for gx, gy, kind in glands:
        r_hole = {"antenna": 3.25, "vent": 6.1}.get(kind, 8.1)
        base = base - zcyl(gx, gy, zb + t / 2, r_hole, t + 2)
    out.add("Cabinet base, IP66 polycarbonate", base, "polycarbonate", "bought", None, "enclosure")
    out.add("Cabinet lid, clear polycarbonate", lid, "polycarbonate", "bought", None, "enclosure")
    for cx_, cz_ in corners:
        out.fasteners(W.screw_into(4, 16, (cx_, -d, cz_), "+y"))
    for gx, gy, kind in glands:
        if kind == "antenna":
            ant_s = zcyl(gx, gy, zb + t / 2 + 4, 3.2, t + 8) + zcyl(gx, gy, zb - 6, 9, 12) + zcyl(gx, gy, zb - 12 - 64, 5, 128)
            out.add("LTE and GSM whip antenna on SMA bulkhead", cp.break_edges(ant_s, 0.4), "matte_black", "bought")
            out.add("SMA bulkhead nut", W.put(W.hexp(8, 4) - b.Pos(0, 0, 2) * b.Cylinder(3.2, 5), (gx, gy, zb + t), "+z"), "brass", "fastener")
        elif kind == "vent":
            body, ln = W.gland(12, t, 17, 15, 8, 2.0, nut_h_=4.0)
            out.add("M12 pressure-equalising vent", W.put(body, (gx, gy, zb), "+z"), "hdpe_black", "bought")
            out.add("M12 vent locknut", W.put(ln, (gx, gy, zb), "+z"), "hdpe_black", "fastener")
        else:
            body, ln = W.gland(16, t, 22, 19, 10, 7.0)
            out.add(f"M16 IP68 cable gland ({kind})", W.put(body, (gx, gy, zb), "+z"), "hdpe_black", "bought")
            out.add("M16 gland locknut", W.put(ln, (gx, gy, zb), "+z"), "hdpe_black", "fastener")
    # lugs and bolts
    lw, lth, lh = 20.0, 3.0, 20.0
    lx, lz = w / 2 - 15, h / 2 + 2 + lh / 2 + 1
    for s in (-1, 1):
        for q in (-1, 1):
            x, ze = s * lx, q * h / 2
            foot = span(x - lw / 2, x + lw / 2, -20, -lth, ze, ze + q * lth)
            tab = span(x - lw / 2, x + lw / 2, -lth, 0, ze + q * 2, ze + q * (2 + lh))
            out.add("Cabinet mounting lug", cp.break_edges(foot + tab - ycyl(x, -lth - 1, 1, q * lz, 2.75), 0.4), "stainless", "bought", None, "enclosure")
            out.fasteners([(n + " (lug)", sh) for n, sh in W.bolt_set(5, 16, (x, -lth, q * lz), "+y", grip=lth + plate_t)])
    mpl = span(-mw / 2, mw / 2, mf, my1, -mh / 2, mh / 2) - fuse(ycyl(bx_, mf - 1, my1 + 1, bz_, 2.2) for bx_, bz_ in bosses)
    if hood:
        g, st, fl = 25.0, 2.0, 15.0
        sxo = w / 2 + g + st
        s_y0 = -d - g - st
        sz0, sz1 = -h / 2 - 20, h / 2 + g + st
        hd_ = span(-sxo, sxo, s_y0, 0, sz0, sz1) - span(-sxo + st, sxo - st, s_y0 + st, 1, sz0 - 1, sz1 - st)
        sx = w / 2 + g - fl / 2
        sz = h / 2 - 20
        for s in (-1, 1):
            f = span(s * (sxo - st), s * (sxo - st - fl), -st, 0, sz0, sz1 - st)
            for q in (-1, 1):
                f = f - ycyl(s * sx, -st - 1, 1, q * sz, 2.75)
            hd_ = hd_ + f
        out.add("Sun shield, white powder-coated aluminium", hd_, "aluminium", "bought", None, "enclosure")
        for s in (-1, 1):
            for q in (-1, 1):
                out.add("M5 knurled thumb screw", W.put(W.thumb_screw(4.8, st + plate_t + 2, 12, 6), (s * sx, -st, q * sz), "-y"), "stainless", "fastener")
    return mpl, mf, my1, bosses, corners


def _electronics(out, mf, my1, bat_xz, ctl, mdm, bat_size=(80.0, 40.0, 130.0), extra_mpl_holes=()):
    """Battery tray with one 32700 cell and its protection board, controller and modem carriers on standoffs,
    on an internal plate whose front face is at y = mf (local cabinet coordinates)."""
    cp, W = _kit()
    bw, bd, bh = bat_size
    x0b, z0b = bat_xz
    tray = W.rbox(x0b, x0b + bw, mf - bd, mf, z0b, z0b + bh, 1.0) - span(x0b + 2, x0b + bw - 2, mf - bd - 1, mf - 2, z0b + 2, z0b + bh - 2)
    scr = [(x0b + bw - 25, z0b + bh - 12), (x0b + bw - 25, z0b + 10)]
    for hx, hz in scr:
        tray = tray - ycyl(hx, mf - 3, mf + 1, hz, 1.7)
    out.add("Battery tray", tray, "hdpe_black", "bought", None, "internal")
    out.add("LiFePO4 cell 32700, 3.2 V 6 Ah", W.put(cp.round_bar(32, 70, 1.0), (x0b + 19, mf - 19, z0b + 12), "+z"), "mild_steel", "bought", None, "internal")
    out.add("Battery protection board with NTC", W.board_xz(x0b + 40, x0b + bw - 6, z0b + 25, z0b + 75, mf - 2), "hdpe_recycled", "bought", None, "internal")
    out.add("Battery fuse holder", W.chip(x0b + 44, x0b + 62, mf - 9.6, mf - 3.6, z0b + 30, z0b + 44), "hdpe_black", "bought", None, "internal")
    for hx, hz in scr:
        out.fasteners(W.screw_into(3, 8, (hx, mf - 2, hz), "+y"))
        out.add("M3 nut (ISO 4032)", W.put(W.nut(3), (hx, my1, hz), "+y"), "stainless", "fastener")

    def carrier(x0, x1, z0, z1, label, comps):
        holes = [(xx, zz) for xx in (x0 + 5, x1 - 5) for zz in (z0 + 5, z1 - 5)]
        yb_ = mf - 6.0
        out.add(label, W.board_xz(x0, x1, z0, z1, yb_, 1.6, holes), "hdpe_recycled", "bought", None, "internal")
        for xx, zz in holes:
            out.add("M3 x 6 hex standoff, nylon", W.put(W.hex_standoff(5.5, 6.0, 3.2), (xx, yb_, zz), "+y"), "hdpe_natural", "fastener", None, "internal")
            out.fasteners(W.screw_into(3, 6, (xx, yb_ - 1.6, zz), "+y"))
        for nm, (a0, a1, c0, c1, depth) in comps.items():
            out.add(nm, W.chip(x0 + a0, x0 + a1, yb_ - 1.6 - depth, yb_ - 1.6, z0 + c0, z0 + c1), "matte_black", "bought", None, "internal")
    carrier(*ctl[0], ctl[1], ctl[2])
    carrier(*mdm[0], mdm[1], mdm[2])
    return [(hx, hz) for hx, hz in scr] + list(extra_mpl_holes)


# ----------------------------------------------------------------------------------------------- option B
def _option_b(p=PARAMS):
    """Reagent colorimetric (DPD) analyser cabinet on the same pole beside the tapstand."""
    cp, W = _kit()
    b = _b3d()
    px = p["pole_x"]
    w, d, h, cz0 = 240.0, 140.0, 320.0, 1250.0
    pb = dict(p, enc=(w, d, h))
    yf = d / 2
    D = dict(plate_front=yf, plate_back=yf + 3.0, saddle_apex_y=yf + 3.0 + p["saddle_apex"])
    D["pole_y"] = D["saddle_apex_y"] + p["pole_od"] / 2 * SQ2
    py = D["pole_y"]
    pr = p["pole_od"] / 2
    out = _Parts()
    out.add("Existing tapstand riser (site)", zcyl(0, 0, (p["riser_h"] - 300) / 2, p["riser_od"] / 2, p["riser_h"] + 300), "galvanised", "context", None, "context")
    out.add("Concrete footing 300 mm (site)", zcyl(px, py, -p["embed"] / 2, p["footing_d"] / 2, p["embed"]) - zcyl(px, py, -p["embed"] / 2, pr, p["embed"] + 2),
            "concrete", "context", None, "context")
    out.add("Mounting pole, 48.3 x 3.2 mm galvanised tube", zcyl(px, py, (p["pole_h"] - p["embed"]) / 2, pr, p["pole_h"] + p["embed"])
            - zcyl(px, py, (p["pole_h"] - p["embed"]) / 2, pr - p["pole_wall"], p["pole_h"] + p["embed"] + 2), "galvanised", "bought")
    ub_z = (cz0 - h / 2 - 35, cz0 + h / 2 + 35)
    _pole_clamps(out, pb, D, px, ub_z, "cabinet plate")
    # back plate with the U-bolt, lug and hood holes
    lx, lz = w / 2 - 15, h / 2 + 2 + 10 + 1
    sx, sz = w / 2 + 25 - 7.5, h / 2 - 20
    holes = [(px + s * lx, cz0 + q * lz, 2.75) for s in (-1, 1) for q in (-1, 1)] + [(px + s * sx, cz0 + q * sz, 2.4) for s in (-1, 1) for q in (-1, 1)]
    plate = plate_with_holes(pb, D, px, ub_z[0] - 20, ub_z[1] + 20, 330.0, ub_z, holes)
    out.add("Cabinet back plate, 330 x 430 x 3 mm aluminium", cp.break_edges(plate, 0.6), "aluminium", "made")
    # cabinet in local coordinates, placed with its back face on the plate front
    cab = _Parts(xf=b.Pos(px, yf, cz0))
    gl = [(-90, -40, "sample in"), (-50, -40, "reacted sample out"), (-10, -40, "panel cable"), (30, -90, "spare"), (70, -90, "vent"), (100, -100, "antenna")]
    mpl, mf, my1, bosses, corners = _cabinet(cab, w, d, h, glands=gl)
    # inside (local x, z on the internal plate, bosses at (+-103, +-139)): battery lower left, modem upper left,
    # controller upper right, cuvette block with stirrer and sample valve in the middle, pumps and bottles right
    holes_m = _electronics(cab, mf, my1, (-105, -130), ((12, 92, 30, 140), "Controller carrier board",
                           {"ESP32-S3 module": (10, 28, 75, 100.5, 3.1), "Photometer front end": (40, 52, 75, 85, 1.2),
                            "Pump and stirrer drivers": (55, 75, 25, 45, 4.0), "12 V boost valve driver": (12, 30, 10, 30, 5.0),
                            "Board connectors": (35, 72, 2, 10, 8.0)}),
                           ((-92, -22, 80, 135), "Cellular modem board (SIM7000G class)",
                            {"LTE-M and NB-IoT module": (12, 42, 12, 42, 2.5), "SIM holder": (46, 62, 14, 34, 2.0)}))
    bx0, bx1, bxc = -8.0, 32.0, 12.0
    blk = W.rbox(bx0, bx1, mf - 40, mf, -100, -40, 1.0) - zcyl(bxc, mf - 20, -70, 6.0, 62) - xcyl(bx0 - 1, bx1 + 1, mf - 20, -78, 2.5)
    blk_scr = [(bx0 + 5, -90), (bx1 - 5, -50)]
    for xx, zz in blk_scr:
        blk = blk - ycyl(xx, mf - 41, mf + 1, zz, 1.6)
    cab.add("Cuvette block, black acetal", blk, "matte_black", "made", None, "analyser")
    cab.add("Glass cuvette, 12 mm", zcyl(bxc, mf - 20, -72, 6.0, 52) - zcyl(bxc, mf - 20, -70, 5.0, 52), "glass", "bought", None, "analyser")
    for xw, sgn, nm, en in ((bx0, -1, "LED holder (515 and 860 nm LEDs)", "Photometer LED"), (bx1, 1, "Photometer detector holder", "Photodiode")):
        hold = W.rbox(min(xw, xw + sgn * 12), max(xw, xw + sgn * 12), mf - 30, mf - 10, -88, -68, 0.6) - xcyl(xw - 13, xw + 13, mf - 20, -78, 2.5)
        cab.add(nm, hold, "matte_black", "made", None, "analyser")
        cab.add(en, W.put(cp.break_edges(b.Pos(0, 0, 4.5) * b.Cylinder(2.5, 9), 0.5), (xw + sgn * 1.5, mf - 20, -78), "+x" if sgn > 0 else "-x"),
                "polycarbonate", "bought", None, "analyser")
    for xx, zz in blk_scr:
        cab.fasteners(W.screw_into(3, 44, (xx, mf - 40, zz), "+y"))
    motor = zcyl(bxc, mf - 20, -115, 13, 28) + span(bx0, bx1, mf - 6, mf, -129, -101)
    mot_scr = [(bxc - 14, -115), (bxc + 14, -115)]
    motor = motor - fuse(ycyl(xx, mf - 7, mf + 1, zz, 1.7) for xx, zz in mot_scr)
    cab.add("Magnetic stirrer motor with bracket", cp.break_edges(motor, 0.4), "matte_black", "bought", None, "analyser")
    for xx, zz in mot_scr:
        cab.fasteners(W.screw_into(3, 10, (xx, mf - 6, zz), "+y"))
    pump_scr = []
    for cx_, nm in ((60, "DPD reagent pump"), (96, "Buffer reagent pump")):
        bodyp = W.rbox(cx_ - 13, cx_ + 13, mf - 30, mf, -25, 20, 1.0) + span(cx_ - 18, cx_ + 18, mf - 3, mf, -10, 5)
        bodyp = bodyp - fuse(ycyl(cx_ + s * 15.5, mf - 4, mf + 1, -2.5, 1.7) for s in (-1, 1))
        head = cp.break_edges(ycyl(cx_, mf - 44, mf - 30, -2.5, 12), 0.8)
        cab.add(f"Peristaltic {nm}, 12 V", bodyp + head, "matte_black", "bought", None, "analyser")
        pump_scr += [(cx_ + s * 15.5, -2.5) for s in (-1, 1)]
    shelf = span(44, 117, mf - 46, mf, -150, -147) + span(44, 95, mf - 3, mf, -147, -118)
    shelf_scr = [(52, -130), (88, -130)]
    shelf = shelf - fuse(ycyl(xx, mf - 4, mf + 1, zz, 1.7) for xx, zz in shelf_scr)
    cab.add("Bottle bracket, bent 1.5 mm stainless", cp.break_edges(shelf, 0.4), "stainless", "made", None, "analyser")
    for cx_, nm in ((63, "DPD indicator"), (99, "Phosphate buffer")):
        bt, cap = W.bottle(36, 80, 16, 6, 22, 10)
        cab.add(f"Reagent bottle, 80 mL ({nm})", W.put(bt, (cx_, mf - 23, -147), "+z"), "hdpe_natural", "bought", None, "analyser")
        cab.add("Reagent bottle cap", W.put(cap, (cx_, mf - 23, -147), "+z"), "hdpe_black", "bought", None, "analyser")
    val = W.rbox(-5, 19, mf - 30, mf, -20, 20, 0.8) + span(-10, 24, mf - 3, mf, -6, 6) + cp.break_edges(ycyl(7, mf - 45, mf - 30, 0, 12), 0.6)
    val_scr = [(-7.5, 0), (21.5, 0)]
    val = val - fuse(ycyl(xx, mf - 4, mf + 1, zz, 1.7) for xx, zz in val_scr)
    cab.add("Latching sample valve, 12 V", val, "hdpe_black", "bought", None, "analyser")
    for xx, zz in pump_scr + shelf_scr + val_scr:
        cab.fasteners(W.screw_into(3, 8, (xx, mf - 3, zz), "+y"))
        cab.add("M3 nut (ISO 4032)", W.put(W.nut(3), (xx, my1, zz), "+y"), "stainless", "fastener")
    for hx, hz in holes_m + blk_scr + mot_scr + pump_scr + shelf_scr + val_scr:
        mpl = mpl - ycyl(hx, mf - 1, my1 + 1, hz, 1.7)
    cab.add("Internal plate, printed ASA", cp.break_edges(mpl, 0.5), "hdpe_natural", "made", None, "internal")
    for bx_, bz_ in bosses:
        cab.fasteners(W.screw_into(4, 9, (bx_, mf, bz_), "+y"))
    out.extend(cab)
    # outside: sample line from a saddle tee, tube up to the cabinet, drain with an air break, panel
    zb = cz0 - h / 2
    _sample_train(out, p, (px - 90, yf - 40, zb - 18))
    ox, oy = px - 50, yf - 40
    vent = W.cyl_between((ox, oy, zb - 18), (ox, oy, zb - 120), 8) - W.cyl_between((ox, oy, zb - 17), (ox, oy, zb - 121), 6)
    vent = vent + xcyl(ox + 6, ox + 30, oy, zb - 100, 7) + W.cyl_between((ox + 30, oy, zb - 107), (ox + 30, oy, zb - 50), 7)
    vent = vent - xcyl(ox, ox + 30, oy, zb - 100, 5) - W.cyl_between((ox + 30, oy, zb - 100), (ox + 30, oy, zb - 49), 5)
    out.add("Air-break vent tee", vent, "hdpe_natural", "bought", None, "sample")
    out.add("Drain hose to soakaway, 12 mm bore PVC", W.path([(ox, oy, zb - 120), (ox, oy, 350), (ox, -230, 170), (240, -230, 170)], 8), "hdpe_natural", "bought", None, "sample")
    jb, n = _panel(out, px, py, p["pole_h"], pr, p["panel_rise"], p["panel_tilt"], *p["panel"], sleeve=p["sleeve"])
    c45 = (pr + 14) / SQ2
    out.add("Panel lead", W.path([jb, tuple(jb[i] - 15 * n[i] for i in range(3)), (px - c45, py + c45, p["pole_h"] - 95),
                                  (px - c45, py + c45, zb - 26), (px - 175, py + c45, zb - 26), (px - 175, yf - 20, zb - 26),
                                  (px - 10, yf - 20, zb - 26), (px - 10, yf - 40, zb - 26), (px - 10, yf - 40, zb - 18)], 3), "epdm", "bought", None, "cables")
    return out


def _sample_train(out, p, end):
    """Saddle tee clamp (two halves, two M6 bolts), isolation valve, nipples, strainer, check valve, regulator,
    and a 1/4 in tube to `end` (x, y, z)."""
    cp, W = _kit()
    b = _b3d()
    ro = p["riser_od"] / 2
    tz = p["tee_z"]
    ring = zcyl(0, 0, tz, ro + 7, 60) - zcyl(0, 0, tz, ro, 62)
    for hname, hs, sgn in (("branch", span(0, 200, -100, 100, tz - 40, tz + 40), 1), ("back", span(-200, 0, -100, 100, tz - 40, tz + 40), -1)):
        ears = fuse(span(0, sgn * 6, sy * (ro + 4), sy * (ro + 20), tz - 10, tz + 10) for sy in (-1, 1))
        half = (ring & hs) + ears
        for sy in (-1, 1):
            half = half - xcyl(-8, 8, sy * (ro + 13), tz, 3.3)
        if hname == "branch":
            half = half + xcyl(ro + 6, ro + 30, 0, tz, 10) - xcyl(ro - 1, ro + 31, 0, tz, 5.0)
        out.add(f"Saddle tee clamp, {hname} half (25 mm)", cp.break_edges(half, 0.4), "brass", "bought", None, "sample")
    for sy in (-1, 1):
        out.fasteners([(n + " (saddle tee)", s_) for n, s_ in W.bolt_set(6, 25, (-6, sy * (ro + 13), tz), "+x", grip=12)])
    iso = cp.break_edges(span(ro + 30, ro + 54, -11, 11, tz - 11, tz + 11), 1.0) + tube((ro + 42, 0, tz + 11), (ro + 42, 0, tz + 40), 3) + span(ro + 36, ro + 70, -4, 4, tz + 36, tz + 42)
    out.add("Isolation ball valve, 1/4 in", iso, "brass", "bought", None, "sample")
    for x0_, x1_ in ((54, 60), (90, 93), (102, 105)):
        out.add("Brass hex nipple, 1/4 in", b.Pos(ro + x0_, 0, tz) * b.Rot(0, 90, 0) * W.extrude(W.RegularPolygon(12 / W.SQ3, 6), x1_ - x0_), "brass", "bought", None, "sample")
    out.add("Strainer, 1/4 in", W.fitting(ro + 60, ro + 90, 12, 0, tz), "brass", "bought", None, "sample")
    out.add("Check valve, 1/4 in", W.fitting(ro + 93, ro + 102, 9, 0, tz), "brass", "bought", None, "sample")
    out.add("Pressure-compensating flow regulator, 0.5 L/min", W.fitting(ro + 105, ro + 155, 11, 0, tz), "hdpe_black", "bought", None, "sample")
    ex, ey, ez_ = end
    out.add("Supply tube, 1/4 in food-grade PE", W.path([(ro + 155, 0, tz), (ex, 0, tz), (ex, ey, tz), (ex, ey, ez_)], p["tube_od"] / 2), "hdpe_natural", "bought", None, "sample")


# ----------------------------------------------------------------------------------------------- option C
def _option_c(p=PARAMS):
    """In-riser probe manifold: a sensor block replaces a short length of the riser between two unions; ORP, pH and
    temperature probes and an insertion turbidity head read the water while people draw it, woken by a paddle
    flow switch. Electronics in a small cabinet clamped behind the riser; panel on a short mast. Built with the
    cabinet in front of the riser (-Y) and turned 180 degrees about the riser at the end, so the cabinet sits
    behind the tapstand and the tap faces the users (-Y)."""
    cp, W = _kit()
    b = _b3d()
    out = _Parts()
    turn = b.Rot(0, 0, 180)
    ro = p["riser_od"] / 2
    # riser in two lengths (site), a short tap stub at the top
    out.add("Existing tapstand riser, lower length (site)", zcyl(0, 0, (450 - 300) / 2, ro, 750), "galvanised", "context", None, "context")
    out.add("Existing tapstand riser, upper length and tap (site)", zcyl(0, 0, 800, ro, 300) + tube((0, 0, 950), (0, 130, 950), 14),
            "galvanised", "context", None, "context")
    # unions and the sensor manifold (made)
    for z0 in (450.0, 630.0):
        u = b.Pos(0, 0, z0) * W.hexp(46, 20) - zcyl(0, 0, z0 + 10, ro + 0.2, 22)
        out.add("Brass union, 25 mm", u, "brass", "bought", None, "sample")
    man = W.rbox(-35, 35, -35, 35, 470, 630, 2.0) - zcyl(0, 0, 550, 13.5, 162)
    ports = {"ORP electrode": ((0, -35, 600), "-y", 6.5), "pH electrode": ((-35, 0, 600), "-x", 6.5),
             "Temperature probe": ((35, 0, 600), "+x", 3.5), "Turbidity insertion head": ((35, 0, 510), "+x", 9.0),
             "Paddle flow switch": ((0, 35, 545), "+y", 9.0)}
    inward = {"-y": "+y", "-x": "+x", "+x": "-x", "+y": "-y"}
    for nm, (o, ax, r) in ports.items():
        man = man - W.put(b.Pos(0, 0, 11) * b.Cylinder(r, 24), o, inward[ax])
    out.add("Sensor manifold, black PVC block", man, "hdpe_black", "made", None, "sample")
    for nm, (o, ax, r) in ports.items():
        thread = 2 * r
        if nm == "Paddle flow switch":
            fs = W.put(b.Pos(0, 0, 0) * W.hexp(24, 10) + b.Pos(0, 0, 27) * b.Cylinder(14, 34) + b.Pos(0, 0, -6) * b.Cylinder(r, 12), o, ax)
            out.add(nm + ", 1/2 in", cp.break_edges(fs, 0.4), "hdpe_black", "bought", None, "sample")
            continue
        body, ln = W.gland(thread, 0.01, thread + 8, thread + 4, 10, 2 * r - 1.0, nut_h_=0.01)
        out.add(f"Compression gland ({nm})", W.put(body, o, inward[ax]), "hdpe_black", "bought", None, "sample")
        L = {"ORP electrode": 130.0, "pH electrode": 130.0, "Temperature probe": 110.0, "Turbidity insertion head": 90.0}[nm]
        rr = r - 0.5
        start = tuple(o[i] + {"-y": (0, 22, 0), "-x": (22, 0, 0), "+x": (-22, 0, 0)}[ax][i] for i in range(3))
        mat = "polycarbonate" if "electrode" in nm else ("stainless" if "Temperature" in nm else "matte_black")
        out.add(nm, W.put(cp.round_bar(2 * rr, L, 1.0), start, ax), mat, "bought", None, "sample")
    # back plate behind the riser with two U-bolt clamps (built in front, turned at the end)
    pc = dict(p, pole_od=2 * ro, saddle=(56.0, 22.0, 24.0), saddle_apex=5.0, ub_x=22.0, ub_d=6.0, nut=(11.0, 5.0))
    yf = -(3.0 + 5.0 + ro * SQ2)
    D = dict(plate_front=yf, plate_back=yf + 3.0, saddle_apex_y=yf + 8.0, pole_y=0.0)
    w, d, h, cz0 = 160.0, 90.0, 190.0, 775.0
    ub_z = (665.0, 905.0)
    sub = _Parts()
    _pole_clamps(sub, pc, D, 0.0, ub_z, "riser clamp", d=6)
    lx, lz = w / 2 - 15, h / 2 + 2 + 10 + 1
    sx, sz = w / 2 + 25 - 7.5, h / 2 - 20
    holes = [(s * lx, cz0 + q * lz, 2.75) for s in (-1, 1) for q in (-1, 1)] + [(s * sx, cz0 + q * sz, 2.4) for s in (-1, 1) for q in (-1, 1)]
    holes += [(60.0, zz, 3.3) for zz in (930.0, 975.0)]
    plate = plate_with_holes(pc, D, 0.0, 645.0, 1000.0, 250.0, ub_z, holes)
    sub.add("Cabinet back plate, 250 x 355 x 3 mm aluminium", cp.break_edges(plate, 0.6), "aluminium", "made")
    # mast for the panel, bolted to the back of the plate
    mr = ro
    my = D["plate_back"] + mr
    mast = zcyl(60, my, (900 + 1150) / 2, mr, 250) - zcyl(60, my, (900 + 1150) / 2, mr - 2.6, 252)
    for zz in (930.0, 975.0):
        mast = mast - ycyl(60, my - mr - 1, my + mr + 1, zz, 3.3)
    sub.add("Panel mast, 33.7 x 2.6 mm galvanised tube", mast, "galvanised", "bought")
    for zz in (930.0, 975.0):
        sub.fasteners([(n + " (mast)", s_) for n, s_ in W.bolt_set(6, 55, (60, yf, zz), "+y", grip=3.0 + 2 * mr)])
    jb, n = _panel(sub, 60, my, 1150.0, mr, 60.0, p["panel_tilt"], *p["panel"], sleeve=(mr + 6, 85.0), dy=40.0)
    cab = _Parts(xf=b.Pos(0, yf, cz0))
    gl = [(-50, -60, "ORP cable"), (-20, -60, "pH cable"), (10, -60, "panel cable"), (40, -60, "turbidity and temperature cable"),
          (-45, -35, "vent"), (55, -35, "antenna")]
    mpl, mf, my1, bosses, corners = _cabinet(cab, w, d, h, glands=gl)
    holes_m = _electronics(cab, mf, my1, (-60, -66), ((12, 68, -62, 62), "Controller carrier board",
                           {"ESP32-S3 module": (10, 28, 70, 95.5, 3.1), "pH and ORP front end": (32, 46, 70, 80, 1.2),
                            "Solar charger": (30, 52, 20, 40, 4.0), "Board connectors": (12, 46, 3, 10, 6.0)}),
                           ((-54, 2, 36, 80), "Cellular modem board (SIM7000G class)",
                            {"LTE-M and NB-IoT module": (10, 40, 10, 34, 2.5)}), bat_size=(64.0, 40.0, 96.0))
    for hx, hz in holes_m:
        mpl = mpl - ycyl(hx, mf - 1, my1 + 1, hz, 1.7)
    cab.add("Internal plate, printed ASA", cp.break_edges(mpl, 0.5), "hdpe_natural", "made", None, "internal")
    for bx_, bz_ in bosses:
        cab.fasteners(W.screw_into(4, 9, (bx_, mf, bz_), "+y"))
    # probe cables up to the cabinet glands (built in front, then turned)
    zgb = cz0 - h / 2 - 18
    cab_y = lambda gy: yf + gy
    cables = [("ORP cable", [(0, -35 - 130 + 22, 600), (0, -175, 600), (0, -175, zgb - 8), (-50, cab_y(-60), zgb - 8), (-50, cab_y(-60), zgb)]),
              ("pH cable", [(-35 - 130 + 22, 0, 600), (-175, 0, 600), (-175, -150, 600), (-175, -150, zgb - 16), (-20, cab_y(-60), zgb - 16), (-20, cab_y(-60), zgb)]),
              ("Turbidity cable", [(35 + 90 - 22, 0, 510), (115, 0, 510), (115, -110, 510), (115, -110, zgb - 14), (40, cab_y(-60), zgb - 14), (40, cab_y(-60), zgb)])]
    for nm, pts in cables:
        sub.add(nm, W.path(pts, 3.0), "epdm", "bought", None, "cables")
    j2 = tuple(jb[i] - 15 * n[i] for i in range(3))
    sub.add("Panel lead", W.path([jb, j2, (j2[0], j2[1], 1010), (140, j2[1], 1010), (140, yf - 120, 1010), (140, yf - 120, zgb - 26),
                                  (10, cab_y(-60), zgb - 26), (10, cab_y(-60), zgb)], 3.0),
            "epdm", "bought", None, "cables")
    sub.extend(cab)
    for q in out + sub:
        q["shape"] = turn * q["shape"]
    out.extend(sub)
    return out


_CACHE = {}


def components(option=CHOSEN):
    """Every part of a concept option as cad_parts.part() dicts (kit 1.9, STANDARDS section 24)."""
    if option not in _CACHE:
        _CACHE[option] = {"A": _option_a, "B": _option_b, "C": _option_c}[option]()
    return list(_CACHE[option])



if __name__ == "__main__":
    if "--check" in sys.argv:
        ok, _ = run_checks()
        sys.exit(0 if ok else 1)
    import copy
    from build123d import Compound, export_step, export_stl
    _cp, _ = _kit()
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    A = [q for q in components(CHOSEN) if q["kind"] != "context"]
    for q in A:
        print(f"{q['kind']:8s} {str(q['bom'] or ''):>3s} {_cp.mass_kg(q):7.3f} kg  {q['name']}")
    print(f"{len(A)} parts, {sum(_cp.mass_kg(q) for q in A):.1f} kg")
    groups = {
        "waterwatch-assembly": A,
        "flow-cell": [q for q in A if q["group"] == "cell" or q["name"].startswith("Cell back plate")],
        "enclosure": [q for q in A if q["group"] in ("enclosure", "internal") or q["name"].startswith("Enclosure back plate")],
    }
    for name, qs in groups.items():
        c = Compound(children=[copy.copy(q["shape"]) for q in qs])
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.5)
        bb = c.bounding_box()
        print(f"{name}: {len(qs)} parts, {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"cell water volume {D['cell_net_l']:.3f} L; sample tube {D['tube_l_mm']:.0f} mm, {D['tube_vol_l'] * 1000:.1f} mL; "
          f"overall height {D['overall_h']:.0f} mm above ground; pole axis {D['pole_y']:.1f} mm behind the enclosure centre")
