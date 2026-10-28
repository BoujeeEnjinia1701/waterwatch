"""WaterWatch repo-specific CAD helpers for the kit 1.9 model (cad/src/model.py).

Small hardware that .kit/cad_parts.py does not carry (M3 and M4 screws, nuts and standoffs, cable glands,
thumb screws and knurled nuts, inline plumbing fittings, printed circuit boards with their main parts) and a
few assemblies shared by the three concept options (a 5 W panel on its pole-top mount, a U-bolt pole clamp,
a wall-mount enclosure with lugs, glands and its electronics). Everything is a build123d solid in mm.
Repo-specific; nothing here belongs in .kit/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Sphere, Torus, extrude, fillet,  # noqa: E402
                       chamfer, Axis)
import cad_parts as cp  # noqa: E402
from cad_parts import break_edges  # noqa: E402

SQ3 = math.sqrt(3.0)

# local +Z of a part built along +Z, turned to point along a world axis
AXIS_ROT = {"+z": (0, 0, 0), "-z": (180, 0, 0), "+y": (-90, 0, 0), "-y": (90, 0, 0), "+x": (0, 90, 0), "-x": (0, -90, 0)}


def put(shape, origin, axis="+z", spin=0.0):
    """Turn a part built along +Z so its +Z points along `axis` ('+x', '-y', ...), spin it about that axis
    by `spin` degrees first, then move its origin to `origin`."""
    return Pos(*origin) * Rot(*AXIS_ROT[axis]) * Rot(0, 0, spin) * shape


def box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def span(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def rbox(x0, x1, y0, y1, z0, z1, r=0.5):
    """A box with its edges broken by r (a moulded or machined block, not a massing box)."""
    return break_edges(span(x0, x1, y0, y1, z0, z1), r)


def cyl_between(a, c, r):
    from build123d import Solid, Vector
    a, c = Vector(*a), Vector(*c)
    d = c - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    """A round cable or hose along a polyline, with a ball at each bend."""
    s = None
    for a, c in zip(points, points[1:]):
        t = cyl_between(a, c, r)
        s = t if s is None else s + t
    for q in points[1:-1]:
        s = s + Pos(*q) * Sphere(r)
    return s


def hexp(s, h):
    """Hex prism, s across flats, from z 0 to h, with the 30 degree chamfer of a nut or head."""
    prism = extrude(RegularPolygon(s / SQ3, 6), h)
    try:
        cap = Pos(0, 0, h / 2) * Cylinder(s / SQ3, h)
        cap = chamfer(cap.edges(), min(s / SQ3 - s / 2 * 0.95, h / 3))
        return prism & cap
    except Exception:
        return prism


# --------------------------------------------------------------------------------------------- fasteners
SMALL = {3: (5.5, 2.4, 7.0, 0.5), 4: (7.0, 3.2, 9.0, 0.8)}   # d: nut s, nut m, washer d2, washer h (ISO 4032, 7089)


def pan_screw(d, L):
    """ISO 7045 class pan head screw: head on top (z 0 to 0.6 d, diameter 2 d), shank from z 0 down to -L."""
    head = Pos(0, 0, 0.3 * d) * Cylinder(d, 0.6 * d)
    try:
        head = fillet(head.edges().sort_by(Axis.Z)[-1:], 0.25 * d)
    except Exception:
        pass
    head = head - Pos(0, 0, 0.6 * d) * Box(0.2 * d * 4, 0.25 * d, 0.5 * d)     # slot
    shank = Pos(0, 0, -L / 2) * Cylinder(d / 2, L)
    try:
        shank = chamfer(shank.edges().sort_by(Axis.Z)[0], 0.1 * d)
    except Exception:
        pass
    return head + shank


def nut(d):
    if d in cp.ISO:
        return cp.hex_nut(d)
    s, m, _, _ = SMALL[d]
    return hexp(s, m) - Pos(0, 0, m / 2) * Cylinder(d / 2, m)


def washer(d):
    if d in cp.ISO:
        return cp.washer(d)
    _, _, d2, h = SMALL[d]
    return extrude(_ring(d2 / 2, d * 0.54), h)


def _ring(ro, ri):
    from build123d import Sketch, Circle
    return Sketch() + Circle(ro) - Circle(ri)


def nut_h(d):
    return cp.ISO[d][2] if d in cp.ISO else SMALL[d][1]


def washer_h(d):
    return cp.ISO[d][4] if d in cp.ISO else SMALL[d][3]


def thumb_screw(d, L, head_d=None, head_h=None):
    """Knurled thumb screw: knurled head (z 0 to head_h), shank from 0 down to -L."""
    head_d = head_d or 2.4 * d
    head_h = head_h or 1.2 * d
    head = extrude(RegularPolygon(head_d / 2, 24), head_h)
    head = break_edges(head, 0.4)
    shank = Pos(0, 0, -L / 2) * Cylinder(d / 2, L)
    return head + shank


def knurled_nut(d, od, h):
    """Knurled thumb nut from z 0 to h, bore d."""
    body = break_edges(extrude(RegularPolygon(od / 2, 24), h), 0.4)
    return body - Pos(0, 0, h / 2) * Cylinder(d / 2, h + 1)


def stud(d, L):
    """Threaded stud along +Z from 0 to L, chamfered ends."""
    return cp.round_bar(d, L, chamfer_ends=0.3 * d / 2)


def set_screw(d, L):
    """Socket set screw along +Z from 0 to L, hex socket at the top."""
    s = cp.round_bar(d, L, chamfer_ends=0.1 * d)
    return s - Pos(0, 0, L - 0.25 * d) * extrude(RegularPolygon(0.25 * d, 6), 0.5 * d)


def hex_standoff(s, L, bore):
    """Hex standoff along +Z from 0 to L with a through bore (an M3 spacer)."""
    return extrude(RegularPolygon(s / SQ3, 6), L) - Pos(0, 0, L / 2) * Cylinder(bore / 2, L + 1)


def bolt_set(d, length, origin, axis, grip, washers=True):
    """A hex bolt through a joint `grip` thick, with a washer each side and a nut. The bolt head sits on the face
    at `origin`; the shank runs along `axis` (for example '+y') through the joint. Returns [(name, solid), ...]."""
    s, k = (cp.ISO[d][0], cp.ISO[d][1]) if d in cp.ISO else (SMALL[d][0], 0.7 * d)
    wh = washer_h(d) if washers else 0.0
    # build along -Z from the face at z = 0 (head above), then turn so -Z maps to `axis`
    flip = {"+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y", "+z": "-z", "-z": "+z"}[axis]
    head = hexp(s, k) if d not in cp.ISO else None
    bolt = cp.hex_bolt(d, length) if d in cp.ISO else (hexp(s, k) + Pos(0, 0, -length / 2) * Cylinder(d / 2, length))
    out = [(f"M{d}x{length:g} hex bolt", put(Pos(0, 0, wh) * bolt, origin, flip))]
    if washers:
        out.append((f"M{d} washer", put(washer(d), origin, flip)))
        out.append((f"M{d} washer", put(Pos(0, 0, -grip - wh) * washer(d), origin, flip)))
    out.append((f"M{d} hex nut", put(Pos(0, 0, -grip - wh - nut_h(d)) * nut(d), origin, flip)))
    return out


def screw_into(d, L, origin, axis, kind="pan", washer_under=False):
    """A screw whose head sits on the face at `origin` and whose shank runs along `axis` for L mm."""
    flip = {"+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y", "+z": "-z", "-z": "+z"}[axis]
    out = []
    off = 0.0
    if washer_under:
        out.append((f"M{d} washer", put(washer(d), origin, flip)))
        off = washer_h(d)
    sh = pan_screw(d, L) if kind == "pan" else (cp.hex_bolt(d, L) if d in cp.ISO else pan_screw(d, L))
    name = f"M{d}x{L:g} {'pan head screw' if kind == 'pan' else 'hex screw'}"
    out.insert(0, (name, put(Pos(0, 0, off) * sh, origin, flip)))
    return out


# --------------------------------------------------------------------------------------------- glands and fittings
def gland(thread_d, wall_t, body_s, cap_d, cap_h, bore_d, nut_s=None, nut_h_=5.0):
    """Cable gland in local coordinates: the wall's outer face is z = 0 and the wall runs to z = wall_t (the
    inside); the hex body and domed cap sit outside (z < 0), the thread runs through the wall, and the locknut
    sits on the inside face. Returns (body, locknut)."""
    hexb = Pos(0, 0, -body_s * 0.35) * hexp(body_s, body_s * 0.35)
    cap = Pos(0, 0, -body_s * 0.35 - cap_h / 2) * Cylinder(cap_d / 2, cap_h)
    try:
        cap = fillet(cap.edges().sort_by(Axis.Z)[:1], min(cap_d / 4, cap_h / 2.5))
    except Exception:
        pass
    thread = Pos(0, 0, (wall_t + nut_h_) / 2) * Cylinder(thread_d / 2, wall_t + nut_h_)
    body = (hexb + cap + thread) - Pos(0, 0, 0) * Cylinder(bore_d / 2, 400)
    ns = nut_s or body_s
    locknut = Pos(0, 0, wall_t) * (hexp(ns, nut_h_) - Pos(0, 0, nut_h_ / 2) * Cylinder(thread_d / 2, nut_h_ + 1))
    return body, locknut


def fitting(x0, x1, r, y=0.0, z=0.0, collar=2.0):
    """Inline plumbing fitting along X from x0 to x1: a round body with a hex collar at each end."""
    body = cyl_between((x0 + collar, y, z), (x1 - collar, y, z), r)
    s = 2 * r * 0.92
    for xa in (x0, x1 - collar):
        body = body + Pos(xa, y, z) * Rot(0, 90, 0) * extrude(RegularPolygon(s / SQ3, 6), collar)
    return body


# --------------------------------------------------------------------------------------------- electronics
def chip(x0, x1, y0, y1, z0, z1):
    """A component package or module on a board, edges broken."""
    return rbox(x0, x1, y0, y1, z0, z1, r=min(0.4, abs(y1 - y0) / 3))


def board_xz(x0, x1, z0, z1, y_back, t=1.6, holes=(), hole_d=3.2):
    """A printed circuit board in the XZ plane, back face at y_back, front face at y_back - t, with holes
    [(x, z), ...]."""
    b = span(x0, x1, y_back - t, y_back, z0, z1)
    for hx, hz in holes:
        b = b - cyl_between((hx, y_back - t - 1, hz), (hx, y_back + 1, hz), hole_d / 2)
    return break_edges(b, 0.3)


# --------------------------------------------------------------------------------------------- solar panel
def panel_local(pnw, pnh, pnt, jb_x=-60.0):
    """Framed 5 W module in local coordinates (module plane XY, sun side +Z, centre at the origin, frame from
    z -pnt/2 to +pnt/2): aluminium L frame with a top lip and a bottom flange, glass laminate, junction box on
    the back. Returns dict name -> solid."""
    h = pnt / 2
    w2, h2 = pnw / 2, pnh / 2
    wall = 2.0
    frame = span(-w2, w2, -h2, h2, -h, h) - span(-w2 + wall, w2 - wall, -h2 + wall, h2 - wall, -h - 1, h + 1)
    lip = span(-w2 + wall, w2 - wall, -h2 + wall, h2 - wall, h - 2, h) - span(-w2 + 6, w2 - 6, -h2 + 6, h2 - 6, h - 3, h + 1)
    flange = span(-w2 + wall, w2 - wall, -h2 + wall, h2 - wall, -h, -h + 2) - span(-w2 + 14, w2 - 14, -h2 + 14, h2 - 14, -h - 1, -h + 3)
    frame = frame + lip + flange
    lam = span(-w2 + wall, w2 - wall, -h2 + wall, h2 - wall, h - 6, h - 2)
    jb = rbox(jb_x - 20, jb_x + 20, -15, 15, -h, h - 6, 1.0)
    return {"frame": frame, "laminate": lam, "jbox": jb}


# --------------------------------------------------------------------------------------------- reagent bottle (option B)
def bottle(d, h, neck_d, neck_h, cap_d, cap_h):
    """HDPE bottle along +Z from 0: body with rounded shoulders, neck, ribbed cap. Returns (bottle, cap)."""
    body = Pos(0, 0, h / 2) * Cylinder(d / 2, h)
    try:
        body = fillet(body.edges(), min(d / 6, 8))
    except Exception:
        pass
    neck = Pos(0, 0, h + neck_h / 2) * Cylinder(neck_d / 2, neck_h)
    capb = Pos(0, 0, h + neck_h) * break_edges(extrude(RegularPolygon(cap_d / 2, 30), cap_h), 0.6)
    return body + neck, capb
