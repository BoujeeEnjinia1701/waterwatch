"""WaterWatch general arrangement sheet WWT-DWG-001, Rev P4 (TRL 3; P2 adds the plugged pH port, WWT-DDR-002;
P4 shows the constructable design, WWT-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/WWT-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is WWT-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-10-02"
D0 = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly(with_riser=True)
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="WaterWatch", title="General arrangement", dwg_no="WWT-DWG-001", rev="P4",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Galvanized steel pole; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", D0, "AC"),
                         ("P2", "Plugged pH probe port in cell lid (DDR-002)", D0, "AC"),
                         ("P3", "Layout and labels tidied", D0, "AC"),
                         ("P4", "Constructable design: back plates, U-bolts, entries underneath (DDR-003)", "2026-10-02", "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    px = P["pole_x"]
    ew, ed, eh = P["enc"]
    co = D["cell_out"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L.append(f'<line x1="{x - 6:.2f}" y1="{zg:.2f}" x2="{x + w + 4:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    xr_end = c["right"][0] + c["right"][2] + 4
    L[-1] = f'<line x1="{x - 6:.2f}" y1="{zg:.2f}" x2="{xr_end:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>'
    L.append(_t(xr_end, zg - 1, "GROUND", 2.0, 600, MUTED, "end"))
    xl = X(bb.min.X) - 12                       # dimension columns to the left of the riser
    for i, (zz, label) in enumerate(((P["tee_z"], f"{P['tee_z']:.0f} tee"),
                                     (D["cell_bot"], f"{D['cell_bot']:.0f} cell underside"),
                                     (P["enc_z"], f"{P['enc_z']:.0f} enclosure center"),
                                     (D["overall_h"], f"{D['overall_h']:,.0f} overall above ground"))):
        xd = xl - 6 * i
        L += [ext(X(px) if zz != P["tee_z"] else X(0), Z(zz), xd - 1, Z(zz))]
        L += dim_v(xd, Z(zz), zg, label)
    xs = X(px + ew / 2 + P["shield_gap"] + P["shield_t"]) + 4
    L += [ext(X(px + ew / 2), Z(D["enc_top"]), xs + 1, Z(D["enc_top"])), ext(X(px + ew / 2), Z(D["enc_bot"]), xs + 1, Z(D["enc_bot"]))]
    L += dim_v(xs, Z(D["enc_top"]), Z(D["enc_bot"]), f"{eh:.0f}", side=3.2)
    L += dim_v(X(px - P["footing_d"] / 2) - 4, zg, Z(-P["embed"]), f"{P['embed']:.0f} embed")
    zt = D["overall_h"] + 90
    L += [ext(X(0), Z(P["riser_h"]) - 2, X(0), Z(zt) - 1), ext(X(px), Z(D["overall_h"]) - 2, X(px), Z(zt) - 1)]
    L += dim_h(X(0), X(px), Z(zt), "")
    L.append(_t(X(0) - 1.5, Z(zt) - 1.0, f"{px:.0f} riser to pole", 2.3, 400, INK, "end", mono=True))
    zf = -P["embed"] / 2
    fx1, fx2 = X(px - P["footing_d"] / 2), X(px + P["footing_d"] / 2)
    L += dim_h(fx1, fx2, Z(zf), "")
    L.append(_t(fx2 + 2.0, Z(zf) + 0.8, f"{P['footing_d']:.0f}", 2.3, 400, INK, "start", mono=True))
    L += leader(X(0), Z(60), X(0) - 9, Z(-260), "EXISTING RISER (NOT IN BOM)", "end")
    L += leader(X(P["drain_end"][0]), Z(P["drain_end"][2]), X(P["drain_end"][0]) + 13, Z(P["drain_end"][2] + 85), "DRAIN TO BASIN")
    L += leader(X(px + co[0] / 2 + 22), Z(D["outlet_z"] + P["vent_h"]), X(px + co[0] / 2 + 22) + 6, Z(D["outlet_z"] + P["vent_h"] + 150), "AIR-BREAK VENT")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L += leader(Xt(px), Yt(D["pole_y"]), Xt(bb.max.X) + 4, Yt(D["pole_y"]) - 3, f"POLE AXIS {D['pole_y']:.0f} BEHIND ENCLOSURE CENTER")

    # right view (from +X): Y to the right... looking along -X, +Y appears to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L += dim_h(Yr(-ed / 2), Yr(ed / 2), Zr(D["enc_top"] + 250), "")
    L.append(_t(Yr(-ed / 2) - 1.5, Zr(D["enc_top"] + 250) + 0.8, f"{ed:.0f}", 2.3, 400, INK, "end", mono=True))
    L += [ext(Yr(-ed / 2), Zr(D["enc_top"]), Yr(-ed / 2), Zr(D["enc_top"] + 260)), ext(Yr(ed / 2), Zr(D["enc_top"]), Yr(ed / 2), Zr(D["enc_top"] + 260))]
    L.append(_t(Yr(0) + 9, Zr(D["panel_z"]) + 1.5, f"PANEL TILT {P['panel_tilt']:.0f} DEG", 2.0, 400, INK, "start"))

    s._layers += L
    s.add_svg(views["iso"], 276, 40, 140, 92, label="Isometric view", sublabel="Not to scale")
    cix, ciy, ciz = P["cell_in"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Pole {P['pole_od']} x {P['pole_wall']} galvanized, {P['pole_h']:.0f} above ground, {P['embed']:.0f} in a {P['footing_d']:.0f} footing",
        f"Panel 5 W, {P['panel'][0]:.0f} x {P['panel'][1]:.0f}, tilt {P['panel_tilt']:.0f} deg; top {D['overall_h']:,.0f} above ground",
        f"Enclosure IP66 {ew:.0f} x {ed:.0f} x {eh:.0f}, center {P['enc_z']:.0f}; sun shield, {P['shield_gap']:.0f} gap",
        f"Back plates 3 mm aluminium on M8 U-bolts and V-saddles (DDR-003)",
        f"Flow cell body {co[0]:.0f} x {co[1]:.0f} x {co[2]:.0f} + {P['cell_top_t']:.0f} lid; cavity {cix:.0f} x {ciy:.0f} x {ciz:.0f}",
        f"Cell water {D['cell_net_l']:.2f} L; inlet at the bottom, outlet {D['outlet_z'] - D['cell_bot']:.0f} above the underside",
        f"Spare pH probe port (M20 gland) in cell lid, plugged (DDR-002)",
        f"Tee on the 25 mm riser at {P['tee_z']:.0f}; valve under the cell; 1/4 in tube {D['tube_l_mm']:.0f}",
        "Flush 0.5 L/min (pressure compensating) for 90 s hourly (WWT-CAL-001)",
        "Drain 12 mm bore with open air break; discharges to the basin",
        "Third-angle; front view from -Y, facing the equator; riser on the Z axis",
    ], x=276, y=154, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "WWT-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
