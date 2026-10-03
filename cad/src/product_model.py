"""WaterWatch product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a white powder-coated sun shield with rounded
corners, side louvers, a name plate and a lit green status lens; the IP66 enclosure with a
clear polycarbonate lid, gasket line, tamper-resistant lid screws, cable glands and vent plug;
inside it the LiFePO4 pack under a hook-and-loop strap, the controller board and the cellular
modem; the whip antenna pointing down from the bottom face; the 5 W panel with an aluminum frame,
cell grid, junction box and pole-top tilt bracket; the opaque black flow-through cell with a
top plate held by knurled thumb nuts, the turbidity head, the chlorine sensor, the temperature
probe and the teal blanking plug in the spare pH port; the latching solenoid valve, the sample
line from a saddle tee (isolation valve, strainer, regulator, 1/4 in tube) and the drain elbow
with its open air-break vent and hose. Context is a short section of the tapstand riser with
its tap. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR
FABRICATION.

Every part size, the X and Y positions and every interface come from PARAMS and derived() in
model.py. Axes as model.py: riser on the Z axis, Z up, the pole on +X, enclosure and panel face
-Y. For a compact product render the heights are drawn closer together than installed (render
layout, see the constants below): the enclosure is at its model.py height; the panel and pole
top are drawn 520 mm lower, the flow cell 130 mm higher and the saddle tee 350 mm higher, and
the pole, riser and drain hose are shown as short sections. See docs/REVIEW.md, session
2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cone, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, build_components

TITLE = "WaterWatch: solar water quality sentinel for a village tap"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); tapstand riser at left "
             "feeding the flow cell and its sensors, enclosure under the white sun shield with the green status "
             "light lit, solar panel on top. Heights drawn closer together than installed"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 25, "az": -32,
     "note": "Exploded view from the front right and above (about 25 deg elevation): flow cell, turbidity head, "
             "chlorine and temperature sensors, enclosure, controller board, battery, cellular modem and "
             "antenna, sun shield and solar panel"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 18, "az": -32,
     "note": "Detail from the front right, slightly above (about 18 deg elevation), without the tapstand and "
             "plumbing: sun shield with the green status light lit, flow cell with its turbidity head, chlorine "
             "sensor and temperature probe, solar panel"},
]

# Render layout (heights only; X, Y and all sizes as model.py)
DZ_PANEL = -520.0      # panel, bracket and pole top drawn this much lower than installed
DZ_CELL = 130.0        # flow cell, sensors and drain elbow drawn this much higher
TEE_Z = 850.0          # saddle tee, sample line and valve height (model.py tee_z is 500)
SECTION_Z0 = 760.0     # bottom of the pole and riser sections
RISER_TOP = 1150.0     # top of the riser section, where the tap is

# Colours (restrained product palette; kit accent)
C_SHIELD = "#F1F2F3"
C_ENC = "#E2E5E8"
C_CLEAR = "#DCEBF5"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_METAL = "#B8BEC6"
C_GALV = "#A7AEB5"
C_CELL = "#23272C"
C_PVC = "#D5D9DD"
C_PCB = "#166534"
C_CHIP = "#111827"
C_TERM = "#2E7D5B"
C_BATT = "#34506B"
C_SOLAR = "#1B2A44"
C_BACKSHEET = "#E9EBED"
C_FRAME = "#C4C9CF"
C_BUS = "#AEB5BD"
C_TUBE = "#ECECE8"
C_HOSE = "#59626D"
C_VALVE = "#E7E8EA"
C_BRASS = "#C2A04A"
C_LEVER = "#B4432A"
C_LED_G = "#22C55E"
C_LABEL = "#F4F4F2"
C_RISER = "#9EA5AC"
C_STRAP = "#2A2E33"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _rod(a, c, r):
    a, c = Vector(*a), Vector(*c)
    d = c - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _sel(s, pred):
    return [e for e in s.edges() if pred(e.center())]


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _front(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _back(s):
    return s.faces().sort_by(Axis.Y)[-1].edges()


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, length):
    return Pos(x - length / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=length)


def _gland_down(x, y, z, af=18.0):
    """Cable gland under a face at height z (hex nut, then dome cap below)."""
    g = _hex_z(x, y, z - 2.5, af, 5.0) + _zcyl(x, y, z - 9.0, af * 0.42, 8.0)
    return _fillet_try(g, _bottom(g), [2.0, 1.0])


def _gland_up(x, y, z, af=16.0):
    g = _hex_z(x, y, z + 2.5, af, 5.0) + _zcyl(x, y, z + 8.0, af * 0.42, 6.0)
    return _fillet_try(g, _top(g), [1.6, 0.8])


def _knurled(x, y, z, r, h, n=20):
    """Knurled thumb nut, axis Z, centred at z."""
    k = _zcyl(x, y, z, r, h)
    k = _fillet_try(k, _top(k), [1.0, 0.5])
    for i in range(n):
        k -= Pos(x, y, z) * Rot(0, 0, 360.0 * i / n) * Pos(r, 0, -0.8) * Box(0.9, 0.9, h)
    return k


def _panel_loc(px, py, pz, tilt):
    return Pos(px, py - 40, pz) * Rot(tilt, 0, 0)


def _panel_pt(px, py, pz, tilt, lx, ly, lz):
    """World point of panel-local (lx, ly, lz); local Z is the panel normal."""
    a = math.radians(tilt)
    return (px + lx, py - 40 + ly * math.cos(a) - lz * math.sin(a), pz + ly * math.sin(a) + lz * math.cos(a))


CX = (380.0, 0.0, -150.0)    # exploded view: the flow cell group moves out to the right and down


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    px, py = P["pole_x"], D["pole_y"]
    pr = P["pole_od"] / 2
    ew, ed, eh = P["enc"]
    ez = P["enc_z"]
    et, lt = P["enc_wall"], P["lid_t"]
    e_bot, e_top = D["enc_bot"], D["enc_top"]
    pole_top = P["pole_h"] + DZ_PANEL
    pz = D["panel_z"] + DZ_PANEL
    tilt = P["panel_tilt"]
    cz = P["cell_z"] + DZ_CELL
    co = D["cell_out"]
    cix, ciy, ciz = P["cell_in"]
    cw_ = P["cell_wall"]
    cell_bot = D["cell_bot"] + DZ_CELL
    top_z = cz + co[2] / 2 + P["cell_top_t"] / 2
    cell_top = cz + co[2] / 2 + P["cell_top_t"]

    # ------------------------------------------------------------ 1 pole, plates and clamps
    pole = _zcyl(px, py, (SECTION_Z0 + pole_top) / 2, pr, pole_top - SECTION_Z0)
    pole -= _zcyl(px, py, (SECTION_Z0 + pole_top) / 2 - 5, pr - P["pole_wall"], pole_top - SECTION_Z0)
    add("Mounting pole (section)", pole, C_GALV, "metal", 1, "shell", (0, 0, 0))

    ep = _box(px, ed / 2 + P["plate_t"] / 2, ez, P["enc_plate"][0], P["plate_t"], P["enc_plate"][1])
    ep = _fillet_try(ep, _edges_par(ep, Axis.Y), [6.0, 4.0])
    cp_d = py - pr - co[1] / 2
    cp = _box(px, co[1] / 2 + cp_d / 2, cz, 50, cp_d, 60)
    cp = _fillet_try(cp, _edges_par(cp, Axis.Y), [4.0, 2.0])
    add("Mounting plates", ep + cp, C_GALV, "metal", 1, "shell", (0, 0, 0))

    clamps = None
    for z in (cz, e_bot + 30, e_top - 30):
        c = _zcyl(px, py, z, pr + 3.0, 22) - _zcyl(px, py, z, pr, 24)
        for sx in (-1, 1):
            c += _box(px + sx * (pr + 8), py, z, 12, 8, 22)
            c += _xcyl(px + sx * (pr + 16), py, z, 3.2, 6) + _hex_x(px + sx * (pr + 21), py, z, 10.0, 5.0)
        clamps = c if clamps is None else clamps + c
    add("Pole clamps", clamps, C_METAL, "metal", 1, "shell", (0, 0, 0))
    cap = _zcyl(px, py, pole_top + 3, pr + 1.5, 6)
    cap = _fillet_try(cap, _top(cap), [3.0, 2.0])
    add("Pole top cap", cap, C_BLACK, "plastic", 1, "shell", (0, 0, 0))

    # ------------------------------------------------------------ 2 solar panel and tilt bracket
    pw, ph, pt = P["panel"]
    L = _panel_loc(px, py, pz, tilt)
    EP = (0, -40, 330)
    frame = Box(pw, ph, pt)
    frame = _fillet_try(frame, _edges_par(frame, Axis.Z), [3.0, 2.0])
    frame -= Box(pw - 10, ph - 10, pt + 2)
    frame += Pos(0, 0, pt / 2 - 1.5) * (Box(pw - 2, ph - 2, 3) - Box(pw - 14, ph - 14, 4))
    add("Panel frame (anodized aluminum)", L * frame, C_FRAME, "metal", 2, "shell", EP)
    sheet = Pos(0, 0, pt / 2 - 5) * Box(pw - 10, ph - 10, 2)
    add("Panel backsheet", L * sheet, C_BACKSHEET, "plastic", 2, "shell", EP)
    nx, ny, gap = 6, 4, 2.2
    cwid, chei = (pw - 22 - (nx - 1) * gap) / nx, (ph - 22 - (ny - 1) * gap) / ny
    cells, bus = None, None
    for i in range(nx):
        for j in range(ny):
            cx_ = -(pw - 22) / 2 + cwid / 2 + i * (cwid + gap)
            cy_ = -(ph - 22) / 2 + chei / 2 + j * (chei + gap)
            c = Pos(cx_, cy_, pt / 2 - 3.7) * Box(cwid, chei, 0.6)
            cells = c if cells is None else cells + c
            for bx in (-cwid / 4, cwid / 4):
                b = Pos(cx_ + bx, cy_, pt / 2 - 3.3) * Box(0.9, chei - 1, 0.2)
                bus = b if bus is None else bus + b
    add("Solar cells", L * cells, C_SOLAR, "screen", 2, "shell", EP)
    add("Cell busbars", L * bus, C_BUS, "metal", 2, "shell", EP)
    jb = Pos(60, 45, -pt / 2 - 8) * Box(56, 36, 16)
    jb = _fillet_try(jb, jb.edges(), [2.0, 1.0])
    add("Panel junction box", L * jb, C_DARK, "plastic", 2, "shell", EP)
    rail = Pos(0, 0, -pt / 2 - 5) * Box(pw - 40, 24, 10)
    hinge = Pos(0, 0, -pt / 2 - 18) * Box(44, 28, 18)
    hinge = _fillet_try(hinge, _edges_par(hinge, Axis.X), [3.0, 2.0])
    hbolt = Pos(0, 0, -pt / 2 - 18) * Rot(0, 90, 0) * Cylinder(4, 54)
    add("Tilt bracket rail and hinge", L * (rail + hinge + hbolt), C_METAL, "metal", 2, "shell", EP)
    h_end = _panel_pt(px, py, pz, tilt, 0, 0, -pt / 2 - 22)
    sleeve = _zcyl(px, py, pole_top - 30, pr + 3, 60)
    sleeve = _fillet_try(sleeve, _top(sleeve), [2.0, 1.0])
    arm = _pipe([(px, py, pole_top + 4), (px, py, h_end[2] - 14), h_end], 11.0)
    add("Pole-top bracket", sleeve + arm, C_METAL, "metal", 2, "shell", (0, 0, 0))

    # ------------------------------------------------------------ 17 sun shield
    g, st = P["shield_gap"], P["shield_t"]
    sw = ew + 2 * (g + st)
    y0, y1 = -ed / 2 - g - st, ed / 2
    zb, zt = e_bot - 20, e_bot + eh + g + st
    ES = (0, -560, 110)
    so = _box(px, (y0 + y1) / 2, (zb + zt) / 2, sw, y1 - y0, zt - zb)
    so = _fillet_try(so, _sel(so, lambda c: abs(c.Z - (zb + zt) / 2) < 1 and c.Y < 0), [10.0, 8.0])
    so = _fillet_try(so, _sel(so, lambda c: c.Z > zt - 0.5 and c.Y < y1 - 1), [7.0, 5.0])
    si = _box(px, (y0 + st + y1 + 6) / 2, (zb - 6 + zt - st) / 2, sw - 2 * st, y1 + 6 - y0 - st, zt - st - zb + 6)
    si = _fillet_try(si, _sel(si, lambda c: abs(c.X - px) > 10 and c.Y < 0 and abs(c.Z - (zb - 6 + zt - st) / 2) < 1),
                     [8.0, 6.0])
    si = _fillet_try(si, _sel(si, lambda c: c.Z > zt - st - 0.5 and c.Y < y1 + 5), [5.0, 3.0])
    shield = so - si
    pen = {k: (px + x, ed / 2 - P["pen_rows"][row]) for k, (x, row) in P["pens"].items()}     # bottom-face entries, as model.py
    ant_x, ant_y = pen["antenna"]
    # status light slot in the front panel, open at the bottom (as model.py: stat_below, stat_slot)
    slz = e_bot - P["stat_below"]
    shield -= _ycyl(px, y0 + st / 2, slz, P["stat_slot"] / 2, st + 2) + _box(px, y0 + st / 2, (zb + slz) / 2 - 0.5, P["stat_slot"], st + 2, slz - zb + 1)
    # pressed side louvers (texture)
    for sx in (-1, 1):
        for k in range(6):
            zz = zb + 70 + 32 * k
            lv = Pos(px + sx * (sw / 2 + 0.7), -25, zz) * Box(1.4, 86, 5)
            lv = _fillet_try(lv, _edges_par(lv, Axis.Y), [0.6, 0.3])
            shield += lv
    add("Sun shield (white powder-coated aluminum)", shield, C_SHIELD, "painted", 17, "shell", ES)
    fy = y0
    band = _box(px, fy - 0.2, zt - 22, sw - 40, 0.4, 5)
    add("Shield accent band", band, C_ACCENT, "painted", 17, "shell", ES)
    plate = _box(px - 20, fy - 0.2, ez + 25, 120, 0.4, 46)
    plate = _fillet_try(plate, _edges_par(plate, Axis.Y), [3.0, 1.5])
    add("Name plate", plate, C_LABEL, "paper", 17, "shell", ES)
    ink = (_box(px - 48, fy - 0.5, ez + 37, 56, 0.3, 9) + _box(px - 20, fy - 0.5, ez + 23, 104, 0.3, 2.5)
           + _box(px - 34, fy - 0.5, ez + 16, 76, 0.3, 2.5) + _box(px - 38, fy - 0.5, ez + 9, 68, 0.3, 2.5)
           + _box(px + 26, fy - 0.5, ez + 37, 16, 0.3, 9))
    add("Name plate print", ink, C_DARK, "paper", 17, "shell", ES)
    lx, lz = px, slz       # the lens unit sits in the slot at the bottom of the shield front (model.py)
    fr = P["stat_flange"] / 2
    bez = _ycyl(lx, fy - 0.75, lz, fr, 1.5) - _ycyl(lx, fy - 1.0, lz, 5.6, 2.0)
    bez = _fillet_try(bez, _front(bez), [0.6, 0.3])
    add("Status light bezel", bez, C_DARK, "plastic", 21, "shell", ES)
    dome = _ycyl(lx, fy - 0.6, lz, 5.5, 1.2) + Pos(lx, fy - 1.2, lz) * Sphere(4.6)
    dome &= _box(lx, fy - 1.5, lz, 14, 3.0, 14)
    add("Status light, green (lit)", dome, C_LED_G, "emissive", 21, "shell", ES)
    yr = fy + P["shield_t"] + P["stat_len"]
    zc = e_bot - P["stat_cable_drop"]
    slead = _pipe([(px, yr, lz), (px, yr + 4, lz), (px, yr + 4, zc), (pen["status"][0], pen["status"][1], zc), (pen["status"][0], pen["status"][1], e_bot - 13)], P["stat_cable_d"] / 2)
    add("Status light lead", slead, C_BLACK, "rubber", 21, "shell", ES)

    # ------------------------------------------------------------ 3, 4 enclosure base and lid
    by0, by1 = -ed / 2 + lt, ed / 2
    bo = _box(px, (by0 + by1) / 2, ez, ew, by1 - by0, eh)
    bo = _fillet_try(bo, _edges_par(bo, Axis.Y), [8.0, 6.0])
    bo = _fillet_try(bo, _back(bo), [2.0, 1.0])
    bi = _box(px, (by0 + by1) / 2 - et, ez, ew - 2 * et, by1 - by0, eh - 2 * et)
    bi = _fillet_try(bi, _edges_par(bi, Axis.Y), [5.0, 3.0])
    base = bo - bi
    for k, (gx_, gy_) in pen.items():
        base -= _zcyl(gx_, gy_, e_bot + et / 2, {"vent": 6.1, "antenna": 3.25}.get(k, 8.1), et + 2)
    add("Enclosure base (IP66 polycarbonate)", base, C_ENC, "plastic", 3, "shell", (0, 0, 0))
    gl = None
    for k, (gx_, gy_) in pen.items():
        if k in ("antenna", "vent"):
            continue
        gg = _gland_down(gx_, gy_, e_bot)
        gl = gg if gl is None else gl + gg
    add("Cable glands", gl, C_DARK, "plastic", 16, "shell", (0, 0, 0))
    vent = _zcyl(pen["vent"][0], pen["vent"][1], e_bot - 3, 7.0, 6.0)
    vent = _fillet_try(vent, _bottom(vent), [2.0, 1.0])
    add("Pressure-equalizing vent plug", vent, C_BLACK, "plastic", 3, "shell", (0, 0, 0))

    ly0, ly1 = -ed / 2, -ed / 2 + lt
    EL = (0, -350, 0)
    lo = _box(px, (ly0 + ly1) / 2, ez, ew, lt, eh)
    lo = _fillet_try(lo, _edges_par(lo, Axis.Y), [8.0, 6.0])
    lo = _fillet_try(lo, _front(lo), [3.0, 2.0])
    li = _box(px, (ly0 + ly1) / 2 + et, ez, ew - 2 * et, lt, eh - 2 * et)
    li = _fillet_try(li, _edges_par(li, Axis.Y), [5.0, 3.0])
    lid = lo - li
    add("Enclosure lid (clear polycarbonate)", lid, C_CLEAR, "clear", 4, "shell", EL)
    gk = _box(px, ly1 + 0.3, ez, ew + 0.6, 1.2, eh + 0.6)
    gk = _fillet_try(gk, _edges_par(gk, Axis.Y), [8.2, 6.0])
    gki = _box(px, ly1 + 0.3, ez, ew - 5, 2.0, eh - 5)
    gki = _fillet_try(gki, _edges_par(gki, Axis.Y), [6.0, 4.0])
    add("Lid gasket", gk - gki, C_BLACK, "rubber", 4, "shell", (0, -310, 0))
    scr = None
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = px + sx * (ew / 2 - 10), ez + sz * (eh / 2 - 10)
            s = _ycyl(x, ly0 - 0.6, z, 3.6, 1.2)
            s = _fillet_try(s, _front(s), [0.5, 0.3])
            s -= Pos(x, ly0 - 1.2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(1.3, 6), amount=1.0, both=True)
            scr = s if scr is None else scr + s
    add("Tamper-resistant lid screws", scr, C_METAL, "metal", 4, "shell", (0, -380, 0))

    # ------------------------------------------------------------ 5 battery, 6 board, 7 modem, 8 antenna
    back = ed / 2 - et
    bw, bd, bh = P["battery"]
    bx_, by_, bz_ = px - 45, back - bd / 2 - 2, ez - 55
    EB = (-30, -190, -20)
    batt = _box(bx_, by_, bz_, bw, bd, bh)
    batt = _fillet_try(batt, _edges_par(batt, Axis.Z), [12.0, 8.0])
    batt = _fillet_try(batt, _top(batt) + _bottom(batt), [2.0, 1.0])
    add("LiFePO4 battery pack (1S2P 32700)", batt, C_BATT, "plastic", 5, "internal", EB)
    blab = _box(bx_, by_ - bd / 2 - 0.2, bz_ + 10, 50, 0.4, 44)
    add("Battery label", blab, C_LABEL, "paper", 5, "internal", EB)
    strap = _box(bx_, by_ + 1, bz_ - 20, bw + 2.4, bd + 2.4, 20) - _box(bx_, by_, bz_ - 20, bw - 1, bd, 22)
    strap = strap - _box(bx_, by_, bz_ - 20, bw - 16, bd + 10, 22) + _box(bx_, by_ - bd / 2 - 1.2, bz_ - 20, bw - 14, 2.4, 20)
    add("Hook-and-loop battery strap", strap, C_STRAP, "fabric", 5, "internal", EB)
    fuse = _box(bx_ + 22, by_ - bd / 2 - 5, bz_ + 58, 16, 10, 12)
    fuse = _fillet_try(fuse, fuse.edges(), [1.5, 1.0])
    add("Battery fuse holder", fuse, C_BLACK, "plastic", 16, "internal", EB)

    cw, cd, ch = P["board"]
    cx0, cz0 = px + 45, ez + 20
    yb = back - 2 - 1.6 / 2                        # PCB against the standoffs at the back
    EBd = (30, -190, 0)
    pcb = _box(cx0, yb, cz0, cw, 1.6, ch)
    pcb = _fillet_try(pcb, _edges_par(pcb, Axis.Y), [3.0, 2.0])
    add("Controller board PCB", pcb, C_PCB, "plastic", 6, "internal", EBd)
    fy_b = yb - 0.8
    esp = _box(cx0 - 12, fy_b - 1.5, cz0 + 32, 18, 3, 25.5)
    add("ESP32-S3 module", esp, C_CHIP, "plastic", 6, "internal", EBd)
    can = _box(cx0 - 12, fy_b - 3.4, cz0 + 30, 15, 0.8, 17)
    add("ESP32-S3 shield can", can, C_METAL, "metal", 6, "internal", EBd)
    chips = (_box(cx0 + 22, fy_b - 0.8, cz0 + 30, 10, 1.6, 10) + _box(cx0 + 22, fy_b - 0.8, cz0 + 8, 7, 1.6, 7)
             + _box(cx0 - 20, fy_b - 0.9, cz0 - 2, 12, 1.8, 12) + _box(cx0 + 5, fy_b - 0.7, cz0 - 2, 8, 1.4, 5))
    ind = _zcyl(cx0 + 24, fy_b - 5, cz0 - 18, 5.0, 8) + _ycyl(cx0 + 5, fy_b - 4, cz0 + 12, 3.0, 8)
    add("Charger, potentiostat and boost ICs", chips + ind, C_CHIP, "plastic", 6, "internal", EBd)
    sd = _box(cx0 - 22, fy_b - 1.0, cz0 - 26, 14, 2.0, 15)
    rtc = _ycyl(cx0 + 16, fy_b - 1.5, cz0 - 32, 6.5, 3.0)
    add("microSD socket and RTC cell", sd + rtc, C_METAL, "metal", 6, "internal", EBd)
    term = _box(cx0, fy_b - 5, cz0 - ch / 2 + 9, 70, 10, 12)
    for k in range(7):
        term -= _box(cx0 - 30 + 10 * k, fy_b - 10, cz0 - ch / 2 + 12, 4, 2.0, 4)
    add("Terminal blocks", term, C_TERM, "plastic", 6, "internal", EBd)

    mw, md, mh = P["modem"]
    mx0, mz0 = px - 45, ez + 75
    EM = (-30, -190, 40)
    mpcb = _box(mx0, yb, mz0, mw, 1.6, mh)
    mpcb = _fillet_try(mpcb, _edges_par(mpcb, Axis.Y), [2.5, 1.5])
    add("Cellular modem board", mpcb, "#1E3A5F", "plastic", 7, "internal", EM)
    mod = _box(mx0 - 8, fy_b - 1.3, mz0 + 4, 30, 2.6, 24)
    add("SIM7000G module can", mod, C_METAL, "metal", 7, "internal", EM)
    sim = _box(mx0 + 20, fy_b - 1.0, mz0 - 8, 16, 2.0, 18)
    add("SIM holder", sim, "#9AA1A8", "metal", 7, "internal", EM)
    mlab = _box(mx0 - 8, fy_b - 2.8, mz0 + 4, 20, 0.3, 12)
    add("Modem label", mlab, C_LABEL, "paper", 7, "internal", EM)

    ad, al = P["antenna"]
    EA = (0, 0, 200)
    abase = _hex_z(ant_x, ant_y, e_bot - 3, 16.0, 6.0) + _zcyl(ant_x, ant_y, e_bot - 16, ad / 2, 20)
    abase = _fillet_try(abase, _bottom(abase), [2.0, 1.0])
    add("Antenna bulkhead and base", abase, C_DARK, "plastic", 8, "shell", EA)
    whip = Pos(ant_x, ant_y, e_bot - 26 - (al - 26) / 2) * Cone(4.5, ad / 2 - 2, al - 26, align=None)
    whip = _fillet_try(whip, _bottom(whip), [2.0, 1.0])
    add("LTE whip antenna", whip, C_BLACK, "rubber", 8, "shell", EA)

    # ------------------------------------------------------------ 9 to 12 flow cell and sensors
    EC = CX
    body = _box(px, 0, cz, co[0], co[1], co[2])
    body = _fillet_try(body, _edges_par(body, Axis.Z), [6.0, 4.0])
    body = _fillet_try(body, _bottom(body), [2.0, 1.0])
    body -= _box(px, 0, cz + cw_ / 2, cix, ciy, ciz + 0.01)
    add("Flow cell body (black ASA)", body, C_CELL, "plastic", 9, "shell", EC)
    ET = _add(CX, (0, 0, 70))
    cl_x, t_x, port_y = px - 22, px + 24, 4.0
    tpl = _box(px, 0, top_z, co[0], co[1], P["cell_top_t"])
    tpl = _fillet_try(tpl, _edges_par(tpl, Axis.Z), [6.0, 4.0])
    tpl = _fillet_try(tpl, _top(tpl), [1.5, 1.0])
    tpl -= (_zcyl(cl_x, port_y, top_z, P["cl_d"] / 2 + 0.5, 12) + _zcyl(t_x, port_y, top_z, P["t_d"] / 2 + 0.5, 12)
            + _zcyl(px + P["ph_x"], port_y, top_z, P["ph_port_d"] / 2, 12))
    add("Flow cell top plate", tpl, C_CELL, "plastic", 9, "shell", ET)
    nuts = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            n = _knurled(px + sx * 38, sy * 19, cell_top + 4, 5.5, 8)
            nuts = n if nuts is None else nuts + n
    add("Knurled thumb nuts (tool-free lid)", nuts, C_METAL, "metal", 9, "shell", _add(CX, (0, 0, 110)))
    plug_d, plug_h = P["plug"]
    plug = _zcyl(px + P["ph_x"], port_y, cell_top + plug_h / 2, plug_d / 2, plug_h)
    plug = _fillet_try(plug, _top(plug), [2.0, 1.0])
    plug -= _box(px + P["ph_x"], port_y, cell_top + plug_h, 12, 2.0, 3)
    plug += _zcyl(px + P["ph_x"], port_y, top_z, P["ph_port_d"] / 2, P["cell_top_t"])
    add("pH port blanking plug", plug, C_ACCENT, "rubber", 9, "shell", _add(CX, (0, 0, 140)))
    clab = _box(px + 20, -co[1] / 2 - 0.2, cz + 6, 40, 0.4, 16)
    add("Flow cell label", clab, C_LABEL, "paper", 9, "shell", EC)
    arrow = _box(px + 8, -co[1] / 2 - 0.45, cz + 6, 6, 0.3, 2) + _box(px + 22, -co[1] / 2 - 0.45, cz + 9, 20, 0.3, 2) \
        + _box(px + 22, -co[1] / 2 - 0.45, cz + 3, 20, 0.3, 2)
    add("Flow cell label print", arrow, C_DARK, "paper", 9, "shell", EC)

    # turbidity optics: the three small holders of model.py (LED left wall, 90 degree detector front wall,
    # 180 degree reference right wall), shifted with the cell by the render layout
    ETb = _add(CX, (-70, 0, 0))
    _mc = build_components(P, below_ground=False)
    for nm, key in (("LED holder (860 nm)", "led_holder"), ("180 degree reference holder", "ref_holder"), ("90 degree detector holder", "det90_holder")):
        hsh = Pos(0, 0, DZ_CELL) * _mc[key]
        hsh = _fillet_try(hsh, hsh.edges(), [1.5, 1.0, 0.6])
        add(f"Turbidity optics: {nm}", hsh, C_DARK, "plastic", 10, "shell", ETb)
    _lb = (Pos(0, 0, DZ_CELL) * _mc["led_holder"]).bounding_box()
    txc = (_lb.min.X + _lb.max.X) / 2
    tgz = _lb.max.Z + 8

    ES2 = _add(CX, (0, 0, 210))
    cl_bot = P["cell_z"] + co[2] / 2 - P["cl_immersed"] + DZ_CELL
    cl_topz = cl_bot + P["cl_len"]
    clh = _zcyl(cl_x, port_y, cl_bot + P["cl_len"] / 2, P["cl_d"] / 2, P["cl_len"])
    clh = _fillet_try(clh, _top(clh), [2.0, 1.0])
    add("Free chlorine sensor (PVC holder)", clh, C_PVC, "plastic", 11, "shell", ES2)
    clb = _zcyl(cl_x, port_y, cl_topz - 22, P["cl_d"] / 2 + 0.3, 5)
    add("Chlorine sensor band", clb, C_ACCENT, "painted", 11, "shell", ES2)
    clr = _zcyl(cl_x, port_y, cl_topz + 6, 5.0, 12)
    clr = _fillet_try(clr, _top(clr), [2.0, 1.0])
    add("Chlorine sensor strain relief", clr, C_BLACK, "rubber", 11, "shell", ES2)
    clg = _hex_z(cl_x, port_y, cell_top + 4, 22.0, 8.0) - _zcyl(cl_x, port_y, cell_top + 4, P["cl_d"] / 2, 10)
    add("Chlorine sensor gland nut", clg, C_DARK, "plastic", 11, "shell", _add(CX, (0, 0, 150)))

    t_bot = P["cell_z"] + co[2] / 2 - P["t_immersed"] + DZ_CELL
    t_topz = t_bot + P["t_len"]
    tp = _zcyl(t_x, port_y, t_bot + P["t_len"] / 2, P["t_d"] / 2, P["t_len"])
    tp = _fillet_try(tp, _top(tp), [1.0, 0.5])
    add("Temperature probe (stainless sheath)", tp, C_METAL, "metal", 12, "shell", ES2)
    tpf = _hex_z(t_x, port_y, cell_top + 4, 12.0, 8.0) - _zcyl(t_x, port_y, cell_top + 4, P["t_d"] / 2, 10)
    add("Temperature probe fitting", tpf, C_BRASS, "metal", 12, "shell", _add(CX, (0, 0, 150)))
    tpr = _zcyl(t_x, port_y, t_topz + 5, 3.8, 10)
    add("Temperature probe boot", tpr, C_BLACK, "rubber", 12, "shell", ES2)

    # ------------------------------------------------------------ 16 cables
    cab = _pipe([(cl_x, port_y, cl_topz + 12), (cl_x, port_y, cl_topz + 24), (pen["chlorine"][0], pen["chlorine"][1], e_bot - 30),
                 (pen["chlorine"][0], pen["chlorine"][1], e_bot - 13)], 2.8)
    cab += _pipe([(t_x, port_y, t_topz + 10), (t_x, port_y, t_topz + 30), (pen["temp"][0], pen["temp"][1], e_bot - 30),
                  (pen["temp"][0], pen["temp"][1], e_bot - 13)], 2.2)
    add("Chlorine and temperature cables", cab, C_BLACK, "rubber", 16, "shell", ES2)
    tcab = _pipe([(txc, 0, tgz), (txc, 0, tgz + 30), (pen["optics"][0] + 15, pen["optics"][1] + 20, e_bot - 45), (pen["optics"][0], pen["optics"][1], e_bot - 30),
                  (pen["optics"][0], pen["optics"][1], e_bot - 13)], 2.8)
    add("Turbidity head cable", tcab, C_BLACK, "rubber", 16, "shell", ETb)
    jb_w = _panel_pt(px, py, pz, tilt, 60, 45, -pt / 2 - 16)
    cx_c = px + 35
    pcab = _pipe([jb_w, (cx_c, jb_w[1], jb_w[2] - 20), (cx_c, 110, pole_top - 40), (cx_c, 110, e_bot - 60),
                  (pen["panel"][0], pen["panel"][1], e_bot - 60), (pen["panel"][0], pen["panel"][1], e_bot - 13)], 2.8)
    add("Panel cable", pcab, C_BLACK, "rubber", 16, "shell", EP)

    # ------------------------------------------------------------ 13 valve, 14 sample line, 15 drain
    vx = P["valve_x"]
    vw, vd, vh = P["valve"]
    EV = (0, 0, -110)
    vb = _box(vx, 0, TEE_Z, vw, vd, vh)
    vb = _fillet_try(vb, vb.edges(), [4.0, 3.0, 2.0])
    add("Latching solenoid valve body", vb, C_VALVE, "plastic", 13, "accessory", EV)
    coil = _zcyl(vx, 0, TEE_Z + vh / 2 + 17, 17, 34)
    coil = _fillet_try(coil, _top(coil), [3.0, 2.0])
    add("Valve coil (12 V latching)", coil, C_BLACK, "plastic", 13, "accessory", EV)
    vlab = Pos(vx, 0, TEE_Z + vh / 2 + 15) * (Cylinder(17.3, 16) - Cylinder(16, 18))
    vlab &= _box(vx, -12, TEE_Z + vh / 2 + 15, 26, 24, 20)
    add("Valve coil label", vlab, C_LABEL, "paper", 13, "accessory", EV)
    pf = None
    for sx in (-1, 1):
        f = _xcyl(vx + sx * (vw / 2 + 6), 0, TEE_Z, 9.0, 12) + _xcyl(vx + sx * (vw / 2 + 13), 0, TEE_Z, 7.0, 3)
        pf = f if pf is None else pf + f
    add("Valve push-fit ports", pf, C_DARK, "plastic", 13, "accessory", EV)
    pcol = _xcyl(vx - vw / 2 - 14.5, 0, TEE_Z, 6.5, 1.5) + _xcyl(vx + vw / 2 + 14.5, 0, TEE_Z, 6.5, 1.5)
    add("Push-fit collets", pcol, C_ACCENT, "plastic", 13, "accessory", EV)

    ro = P["riser_od"] / 2
    tr = P["tube_od"] / 2
    in_x = px - cix / 2 + 12
    saddle = _zcyl(0, 0, TEE_Z, ro + 6, 50) - _zcyl(0, 0, TEE_Z, ro, 52)
    saddle = _fillet_try(saddle, _top(saddle) + _bottom(saddle), [1.5, 1.0])
    for sz in (-1, 1):
        saddle += _box(-ro - 9, 0, TEE_Z + sz * 18, 8, 34, 10)
        saddle += _ycyl(-ro - 9, 0, TEE_Z + sz * 18, 3.0, 44)
        saddle += _ycyl(-ro - 9, 21, TEE_Z + sz * 18, 5.5, 5)
    saddle += _xcyl(ro + 14, 0, TEE_Z, 10, 28)
    add("Saddle tee on riser", saddle, C_DARK, "plastic", 14, "accessory", (0, 0, 0))
    iso = _box(ro + 42, 0, TEE_Z, 26, 24, 24)
    iso = _fillet_try(iso, iso.edges(), [3.0, 2.0])
    iso += _hex_x(ro + 26, 0, TEE_Z, 20.0, 6.0) + _hex_x(ro + 58, 0, TEE_Z, 20.0, 6.0)
    add("Isolation ball valve", iso, C_BRASS, "metal", 14, "accessory", (0, 0, 0))
    lever = _zcyl(ro + 42, 0, TEE_Z + 15, 4, 8) + _box(ro + 54, 0, TEE_Z + 20, 40, 8, 4)
    lever = _fillet_try(lever, _edges_par(lever, Axis.Z), [1.5, 1.0])
    add("Isolation valve lever", lever, C_LEVER, "plastic", 14, "accessory", (0, 0, 0))
    strn = _xcyl(ro + 78, 0, TEE_Z, 12, 26) + _rod((ro + 78, 0, TEE_Z), (ro + 78, -18, TEE_Z - 22), 9)
    strn += _hex_x(ro + 64, 0, TEE_Z, 20.0, 5.0) + _hex_x(ro + 92, 0, TEE_Z, 20.0, 5.0)
    add("Strainer", strn, C_BRASS, "metal", 14, "accessory", (0, 0, 0))
    reg = _xcyl(ro + 128, 0, TEE_Z, 11, 50)
    reg = _fillet_try(reg, reg.edges(), [2.5, 1.5])
    add("Check valve and flow regulator", reg, C_VALVE, "plastic", 14, "accessory", (0, 0, 0))
    rband = _xcyl(ro + 116, 0, TEE_Z, 11.3, 6)
    add("Regulator band", rband, C_ACCENT, "painted", 14, "accessory", (0, 0, 0))
    line = (_pipe([(ro + 94, 0, TEE_Z), (ro + 103, 0, TEE_Z)], tr)
            + _pipe([(ro + 153, 0, TEE_Z), (vx - vw / 2 - 15, 0, TEE_Z)], tr)
            + _pipe([(vx + vw / 2 + 15, 0, TEE_Z), (in_x - 30, 0, TEE_Z), (in_x, 0, TEE_Z + 20),
                     (in_x, 0, cell_bot - 18)], tr))
    add("1/4 in food-grade PE tube", line, C_TUBE, "plastic", 14, "accessory", (0, 0, 0))
    inl = _zcyl(in_x, 0, cell_bot - 8, 6.5, 16) + _hex_z(in_x, 0, cell_bot - 3, 14.0, 6.0)
    add("Cell inlet fitting", inl, C_DARK, "plastic", 9, "shell", EC)

    out_z = D["outlet_z"] + DZ_CELL
    ox = px + co[0] / 2 + 22
    ED = CX
    elb = _xcyl(px + co[0] / 2 + 11, 0, out_z, 8, 22) + Pos(ox, 0, out_z) * Sphere(9.5)
    elb += _zcyl(ox, 0, out_z + 20, 8, 40) - _zcyl(ox, 0, out_z + 30, 5.5, 30)
    elb += _zcyl(ox, 0, out_z - 16, 8, 32)
    add("Outlet elbow with air-break vent", elb, C_DARK, "plastic", 15, "accessory", ED)
    hose = _pipe([(ox, 0, out_z - 30), (ox, 0, SECTION_Z0 + 60), (ox + 20, -60, SECTION_Z0 + 10),
                  (ox + 40, -130, SECTION_Z0 - 10)], P["hose_od"] / 2)
    add("Drain hose (12 mm bore)", hose, C_HOSE, "rubber", 15, "accessory", ED)
    hcl = _zcyl(ox, 0, out_z - 36, P["hose_od"] / 2 + 1.5, 6) - _zcyl(ox, 0, out_z - 36, P["hose_od"] / 2, 8)
    hcl += _box(ox + P["hose_od"] / 2 + 3, 0, out_z - 36, 5, 5, 6)
    add("Hose clamp", hcl, C_METAL, "metal", 15, "accessory", ED)

    # ------------------------------------------------------------ context: tapstand riser section with its tap
    riser = _zcyl(0, 0, (SECTION_Z0 + RISER_TOP) / 2, ro, RISER_TOP - SECTION_Z0)
    riser += _zcyl(0, 0, RISER_TOP - 10, ro + 4, 24)                          # socket
    tap = _pipe([(0, 0, RISER_TOP), (0, 0, RISER_TOP + 20), (0, -90, RISER_TOP + 20), (0, -90, RISER_TOP - 25)], 11)
    tap += _zcyl(0, -45, RISER_TOP + 37, 6, 14)
    tap += _box(0, -45, RISER_TOP + 46, 40, 8, 5)
    add("Tapstand riser and tap (existing)", riser + tap, C_RISER, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
