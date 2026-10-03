"""WaterWatch prototype build plan pictures (WWT-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/WWT-DWG-101 to 109        making sketches for the made and drilled components
    docs/05-build-plan/*-holes.png         drilling layouts (enclosure bottom, back plates, cell lid)
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring (matplotlib)
A single picture can be drawn on its own, for example `joints 3` or `steps 12`, to keep memory low.
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, span, zcyl, riser_context, beam  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
REPO = "github.com/BoujeeEnjinia1701/waterwatch"
D = derived(P)
C = build_components(P)
PX, PY = P["pole_x"], D["pole_y"]
EZ, CZ = P["enc_z"], P["cell_z"]
CY = D["cell_y"]

COL = {"plate": "#A8A29E", "saddle": "#57534E", "ubolt": "#B45309", "body": "#D1D5DB", "lid": "#E5E7EB",
       "glands": "#1F2937", "antenna": "#111827", "lugs": "#64748B", "mplate": "#94A3B8", "battery": "#C2410C",
       "board": "#0F766E", "modem": "#7C3AED", "shield": "#F5F5F4", "cell": "#334155", "optics": "#D4A017",
       "chlorine": "#2563EB", "temp": "#16A34A", "valve": "#115E59", "tube": "#0EA5E9", "fit": "#B45309",
       "drain": "#6B7280", "panel": "#1E3A8A", "mount": "#78716C", "cable": "#A16207", "bolt": "#111827",
       "pole": "#9CA3AF", "gasket": "#0F172A", "plug": "#0D9488"}


def fuse(keys):
    out = None
    for k in keys:
        out = C[k] if out is None else out + C[k]
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def pole_section(z0, z1):
    return part("Pole (set on the survey visit)", C["pole"] & span(PX - 40, PX + 40, PY - 40, PY + 40, z0, z1), COL["pole"])


def named():
    """The components in build order, as the plan names them."""
    return {
        "enc_plate": part("Enclosure back plate", C["enc_plate"], COL["plate"]),
        "enc_base": part("Enclosure body, drilled", C["enc_base"], COL["body"]),
        "entries": part("Glands, vent and antenna", fuse(["glands", "antenna"]), COL["glands"]),
        "lugs": part("Lugs (4) and M5 screws", fuse(["lugs", "lug_screws"]), COL["lugs"]),
        "mplate": part("Internal plate", fuse(["mplate", "mplate_screws"]), COL["mplate"]),
        "modules": part("Battery, controller, modem", fuse(["battery", "board", "modem"]), COL["board"]),
        "enc_lid": part("Enclosure lid", C["enc_lid"], COL["lid"]),
        "shield": part("Sun shield and thumb screws", fuse(["shield", "shield_screws"]), COL["shield"]),
        "status": part("Status light unit", fuse(["status_lens", "status_holder", "status_led"]), "#16A34A"),
        "cell_plate": part("Cell back plate", C["cell_plate"], COL["plate"]),
        "cell_body": part("Flow cell body", fuse(["cell_body", "cell_screws"]), COL["cell"]),
        "optics": part("Optics holders (3)", fuse(["led_holder", "ref_holder", "det90_holder"]), COL["optics"]),
        "valve": part("Latching valve", fuse(["valve", "valve_screws"]), COL["valve"]),
        "fits": part("Inlet, outlet and cell tube", fuse(["inlet_fit", "outlet_fit", "cell_tube"]), COL["fit"]),
        "cell_lid": part("Gasket, lid, glands, plug", fuse(["gasket", "cell_lid", "lid_glands", "plug", "studs"]), "#475569"),
        "sensors": part("Chlorine sensor, temperature probe", fuse(["chlorine", "temp"]), COL["chlorine"]),
        "saddles": part("V-saddles and U-bolts (4 sets)", fuse([f"{a}_{b}_{i}" for a in ("enc", "cell") for b in ("saddle", "ubolt") for i in (0, 1)]), COL["saddle"]),
        "mount": part("Pole-top tilt mount", C["panel_mount"], COL["mount"]),
        "panel": part("Solar panel", C["panel"], COL["panel"]),
        "tee": part("Saddle tee and fittings", fuse(["tee", "fittings"]), COL["fit"]),
        "supply": part("Supply tube", C["supply_tube"], COL["tube"]),
        "drain": part("Air-break tee and drain hose", C["drain"], COL["drain"]),
        "cables": part("Cables", fuse(["panel_lead", "valve_cable", "chlorine_cable", "temp_cable", "optics_cable", "status_cable"]), COL["cable"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = named()
    M["drain"] = part("Air-break tee and drain hose", C["drain"] & span(PX, PX + 200, -50, 100, 640, 1000), COL["drain"])
    M["supply"] = part("Supply tube", C["supply_tube"] & span(PX - 200, PX + 200, -50, 100, 450, 800), COL["tube"])
    M["cables"] = part("Cables", fuse(["panel_lead", "valve_cable", "chlorine_cable", "temp_cable", "optics_cable", "status_cable"]) & span(PX - 200, PX + 200, -100, 200, 1040, 1160), COL["cable"])
    E, Cg = (-260, 0, 0), (360, 0, 280)
    add = lambda a, d: tuple(x + y for x, y in zip(a, d))  # noqa: E731
    off = {"enc_plate": add(E, (0, 260, 0)), "enc_base": E, "entries": add(E, (0, 0, -130)), "lugs": add(E, (0, 130, 0)),
           "mplate": add(E, (0, -150, 0)), "modules": add(E, (0, -270, 0)), "enc_lid": add(E, (0, -400, 0)),
           "shield": add(E, (0, -120, 380)), "status": add(E, (0, -330, 330)),
           "cell_plate": add(Cg, (0, 260, 0)), "cell_body": Cg, "optics": add(Cg, (0, -130, 0)), "valve": add(Cg, (0, -120, -90)),
           "fits": add(Cg, (90, -40, -40)), "cell_lid": add(Cg, (0, 0, 110)), "sensors": add(Cg, (0, 0, 230)),
           "saddles": (40, 560, -330), "mount": (760, 260, -830), "panel": (760, 260, -700),
           "tee": (620, 0, 140), "supply": (480, -40, 60), "drain": add(Cg, (170, 0, -40)), "cables": add(E, (0, 0, -230))}
    parts = [mv(M[k], off[k]) for k in M]
    return bv.overview(parts, OUT / "overview.png", "WaterWatch prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Enclosure group left, flow cell group right, panel above. Pole, tapstand and long tube and hose runs not shown",
                       elev=16, azim=-50, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    import build123d as b
    M = named()
    base = dict(project="WaterWatch", date=DATE)
    out = []
    pz = lambda z0, z1: pole_section(z0, z1)  # noqa: E731
    want = sys.argv[2:] if len(sys.argv) > 2 and sys.argv[1] == "sheets" else None

    def go(n):
        return want is None or str(n) in want

    if go(101):
        out.append(bv.component_sheet(
            part("Enclosure back plate", C["enc_plate"], COL["plate"]),
            [M["enc_base"], M["lugs"], part("Saddles", fuse(["enc_saddle_0", "enc_saddle_1", "enc_ubolt_0", "enc_ubolt_1"]), COL["saddle"]), pz(1000, 1600)],
            dwg_no="WWT-DWG-101", title="WaterWatch enclosure back plate: making sketch",
            material="Aluminium sheet 3 mm, 5052 class, 270 x 420 mm",
            view_shape=b.Pos(-PX, 0, -EZ) * C["enc_plate"], inset_view=(20, -60),
            notes=["Blank 270 x 420 mm, 3 mm aluminium. Front view: the face the box sits on.",
                   "Heights from the bottom edge; sideways from the centre line.",
                   "U-bolt holes 9 mm at 29 each side, 25 and 395 up (two U-bolts).",
                   "Lug screw holes 5.5 mm at 85 each side, 67 and 353 up.",
                   "Shield screws: drill 4.2 mm and tap M5 at 117.5 each side,",
                   "  100 and 320 up (or fit M5 rivet nuts in 7 mm holes).",
                   "The box sits centred, from 80 to 340 up; mark its outline.",
                   "Deburr every hole and edge; round the corners to about 3 mm.",
                   "Fit: the box's back flat on the front face, held by four lugs;",
                   "  two V-saddles flat on the back face, one at each U-bolt.",
                   "Check: lay the lugs and saddles on it and look through each hole."], **base))
    if go(102):
        flip = b.Rot(180, 0, 0) * b.Pos(-PX, 0, -EZ) * C["enc_base"]
        out.append(bv.component_sheet(
            part("Enclosure body", C["enc_base"], COL["body"]), [M["enc_plate"], M["entries"], M["lugs"]],
            dwg_no="WWT-DWG-102", title="WaterWatch enclosure body: drilling sketch",
            material="Bought IP66 polycarbonate box 200 x 120 x 260 mm, four moulded bosses",
            view_shape=flip, inset_view=(-30, -60),
            notes=["Drawn upside down: stand the box on its top, back face toward you;",
                   "  the top view then shows the bottom face as you see it on the bench.",
                   "Measure from the back face, and sideways from the centre line",
                   "  (left and right as seen from the front). See the drilling layout.",
                   "Back row, 28 from the back face: valve gland 62 left, chlorine gland",
                   "  22 left, spare (plugged) 22 right, temperature gland 62 right: 16.2 mm.",
                   "Front row, 70 from the back face: panel gland 62 left, optics gland",
                   "  22 left (16.2 mm); vent 22 right (12.2 mm); antenna 62 right (6.5 mm).",
                   "Middle row, 49 from the back face: status light lead gland on the",
                   "  centre line (16.2 mm).",
                   "Tape the face, pilot drill 3 mm slowly with wood behind, open out with",
                   "  a step drill, light pressure. No solvents: polycarbonate crazes.",
                   "Check each hole size on the part's datasheet before the last step.",
                   "Fit the maker's four lugs to the back corners, feet on top and bottom."], **base))
    if go(103):
        out.append(bv.component_sheet(
            part("Internal plate", C["mplate"], COL["mplate"]), [M["enc_base"]],
            dwg_no="WWT-DWG-103", title="WaterWatch internal plate: making sketch",
            material="ASA, 3D printed flat, 100 % infill, 186 x 205 x 3 mm",
            view_shape=b.Pos(-PX, 0, -EZ) * C["mplate"], inset_view=(20, -60),
            notes=["Print flat, 186 wide x 205 tall x 3 mm, ASA, enclosed printer.",
                   "Four 4.5 mm holes 10 in from each side and from top and bottom",
                   "  (166 x 185 apart) to match the box's four moulded bosses.",
                   "  Measure your box's bosses first and move the holes to suit.",
                   "Lay out on the front face, measured from the left and bottom edges:",
                   "  battery 8 to 88 across, 18 to 148 up (strap round it);",
                   "  modem 18 to 88 across, 150 to 205 up;",
                   "  controller 93 to 183 across, 45 to 165 up.",
                   "Mark each board's holes through the board; drill 3.2 mm for M3",
                   "  screws on 6 mm nylon standoffs.",
                   "Fit: four M4 screws into the bosses; the plate sits 6 off the back",
                   "  wall and 37 above the floor, clear of the gland nuts.",
                   "Check: flat within 0.5 mm; drops in and lifts out without force."], **base))
    if go(104):
        out.append(bv.component_sheet(
            part("Sun shield", C["shield"], "#E7E5E4"), [M["enc_plate"], M["enc_base"], M["enc_lid"], M["lugs"]],
            dwg_no="WWT-DWG-104", title="WaterWatch sun shield: making sketch (to a sheet metal shop)",
            material="White powder-coated aluminium sheet 2 mm",
            view_shape=b.Pos(-PX, 0, -EZ) * C["shield"], inset_view=(22, -55),
            notes=["Folded hood 254 wide, 147 deep, 307 tall outside, open at the",
                   "  bottom and the back; 2 mm sheet, bent on a press brake.",
                   "Front 254 x 307; two sides 147 deep; top 254 x 147, joined to the",
                   "  sides by folded tabs with two 4 mm rivets each.",
                   "Back edge of each side: a 15 mm flange folded 90 degrees inward.",
                   "Flange holes 5.5 mm, 7.5 in from the side sheet, 40 and 260 up",
                   "  from the lower edge.",
                   "Powder coat white after folding; deburr every edge first.",
                   "Fit: flanges flat on the back plate, 10 clear of the box; four M5",
                   "  thumb screws. 25 mm air gap at the front, sides and top.",
                   "Front panel: a 12.2 mm slot open at the bottom edge, its round end",
                   "  10 mm up from the lower edge, for the status light unit.",
                   "To open the lid: pull the status light unit down out of its slot,",
                   "  undo the four thumb screws, slide the shield forward.",
                   "Check: on a trial fit the gap is 25 mm (plus or minus 3) all round."], **base))
    if go(105):
        out.append(bv.component_sheet(
            part("Cell back plate", C["cell_plate"], COL["plate"]),
            [M["cell_body"], M["valve"], part("Saddles", fuse(["cell_saddle_0", "cell_saddle_1", "cell_ubolt_0", "cell_ubolt_1"]), COL["saddle"]), pz(550, 1050)],
            dwg_no="WWT-DWG-105", title="WaterWatch cell back plate: making sketch",
            material="Aluminium sheet 3 mm, 5052 class, 140 x 385 mm",
            view_shape=b.Pos(-PX, 0, -sum(P["cell_plate_z"]) / 2) * C["cell_plate"], inset_view=(20, -60),
            notes=["Blank 140 x 385 mm, 3 mm aluminium. Front view: the cell side.",
                   "Heights from the bottom edge; sideways from the centre line.",
                   "U-bolt holes 9 mm at 29 each side, 25 and 360 up.",
                   "Cell screw holes 5.5 mm at 30 each side, 250 up.",
                   "Valve screw holes 4.5 mm at 18 each side, 93 up.",
                   "The cell body sits from 213 to 287 up, centred; the valve body",
                   "  from 63 to 123 up, centred, ports level.",
                   "Deburr every hole and edge; round the corners to about 3 mm.",
                   "Fit: cell and valve flat on the front, screws from behind;",
                   "  two V-saddles flat on the back, one at each U-bolt.",
                   "Check: the cell and valve holes line up with their parts."], **base))
    if go(106):
        out.append(bv.component_sheet(
            part("Flow cell body", C["cell_body"], COL["cell"]), [M["cell_plate"], M["optics"], M["cell_lid"], M["valve"]],
            dwg_no="WWT-DWG-106", title="WaterWatch flow cell body: making sketch",
            material="Black PVC block (or ASA printed 100 % infill), 96 x 60 x 74 mm",
            view_shape=b.Pos(-PX, -CY, -CZ) * C["cell_body"], inset_view=(28, -50),
            notes=["Block 96 wide x 60 deep x 74 tall. Pocket 80 x 38, 66 deep, from the",
                   "  top: walls 8 at the front, left and right, 14 at the back, floor 8.",
                   "Baffle 6 x 26 x 40 tall on the back wall, 2 right of centre: leave",
                   "  it when milling, or solvent-weld a PVC strip.",
                   "Windows 6 mm through, 41 up, each with a 12 mm counterbore 2.5 deep",
                   "  outside: left and right walls 14 from the front face; front wall",
                   "  8 left of centre. Bed a 2 mm acrylic disc in each with silicone.",
                   "Inlet: floor, 32 left of centre, 37.5 from the front; tap 1/8 BSPT.",
                   "Outlet: right wall, 62 up, 37 from the front; tap 3/8 BSP.",
                   "Back face: two M5 holes 12 deep at 30 each side, 37 up.",
                   "Top: four M4 holes 12 deep at 44 each side, 4 and 53 from the front.",
                   "Check: fill with water to the outlet; no leak in 30 min."], **base))
    if go(107):
        h = C["det90_holder"]
        out.append(bv.component_sheet(
            part("Optics holder", h, COL["optics"]), [M["cell_body"], part("Other holders", fuse(["led_holder", "ref_holder"]), COL["optics"])],
            dwg_no="WWT-DWG-107", title="WaterWatch optics holder (make 3): making sketch",
            material="Black ASA, 3D printed, 100 % infill, 20 x 20 x 16 mm",
            view_shape=b.Pos(-h.bounding_box().center().X, -h.bounding_box().center().Y, -h.bounding_box().center().Z) * h,
            inset_view=(22, -62),
            notes=["Make three the same, 20 x 20 x 16 mm, in black ASA.",
                   "A 5 mm bore on the axis from the wall face, 12 deep, for the LED",
                   "  (left wall) or a light-to-frequency detector (front and right).",
                   "A 3 mm hole from the bore out of the top for the leads.",
                   "Two 3.4 mm holes at opposite corners, 3.5 in from the edges, for",
                   "  M3 screws into tapped holes beside each window.",
                   "Seat the LED or detector against the window disc, pot it in black",
                   "  epoxy so no daylight leaks in, and lead the wires out of the top.",
                   "Fit: face flat on the cell wall, centred on its window.",
                   "Check: in the dark, the detector reads the same with the room",
                   "  light on and off."], **base))
    if go(108):
        ch = C["chlorine"]
        cb = ch.bounding_box()
        out.append(bv.component_sheet(
            part("Chlorine sensor", ch, COL["chlorine"]), [M["cell_body"], M["cell_lid"]],
            dwg_no="WWT-DWG-108", title="WaterWatch free chlorine sensor: making sketch",
            material="PVC conduit 16 mm OD; graphite rod, Ag/AgCl wire, stainless wire; epoxy",
            view_shape=b.Pos(-cb.center().X, -cb.center().Y, -cb.min.Z) * ch, inset_view=(20, -60),
            notes=["Body: 120 mm of 16 mm PVC conduit. Electrodes on a 9 mm circle,",
                   "  120 degrees apart, standing 3 mm proud of the tip:",
                   "  working: 2 mm graphite rod (pencil lead class), polished flat;",
                   "  reference: chlorided silver (Ag/AgCl) wire; counter: stainless wire.",
                   "Solder each lead to a core of a shielded 3-core cable.",
                   "Hold the electrodes in a printed jig and pot the bottom 20 mm of the",
                   "  tube in epoxy; seal the top round the cable with heat shrink.",
                   "Wet the tip, sand the graphite face with 1200 grit before use.",
                   "Fit: through the M25 gland in the cell lid; tip 40 mm below the",
                   "  top of the body, clear of the walls and the beam.",
                   "Check: electrodes isolated from each other (over 10 megohm dry)."], **base))
    if go(109):
        lid = C["cell_lid"]
        lb = lid.bounding_box()
        out.append(bv.component_sheet(
            part("Cell lid", lid, COL["lid"]), [M["cell_body"], M["sensors"]],
            dwg_no="WWT-DWG-109", title="WaterWatch flow cell lid and gasket: making sketch",
            material="Black PVC sheet 10 mm; EPDM sheet 1.5 mm for the gasket",
            view_shape=b.Pos(-lb.center().X, -lb.center().Y, -lb.center().Z) * lid, inset_view=(35, -55),
            notes=["Lid 96 x 60 x 10 mm. Measure from the front edge and the centre line.",
                   "Chlorine gland: tap M25 x 1.5, 24 left of centre, 35 from the front.",
                   "Spare pH port: tap M20 x 1.5, 14 right of centre, 37 from the front;",
                   "  fit the blanking plug (or a gland for the pH probe variant).",
                   "Temperature gland: tap M12 x 1.5, 34 right, 23 from the front.",
                   "Stud holes 4.5 mm at 44 each side, 4 and 53 from the front.",
                   "Gasket: same outline, 80 x 38 window centred 27 from the front,",
                   "  four 4.5 mm stud holes; cut from 1.5 mm EPDM.",
                   "Fit: four M4 studs in the body, gasket, lid, four knurled thumb",
                   "  nuts, finger tight. The lid lifts off with the sensors in it.",
                   "Check: glands do not touch each other or the thumb nuts."], **base))
    return out


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    r = sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))
    return r


def joints():
    want = sys.argv[2:] if len(sys.argv) > 2 and sys.argv[1] == "joints" else None
    out = []

    def go(n):
        return want is None or str(n) in want

    def J(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    zu = D["enc_ub_z"][1]
    if go(1):
        bx = (PX - 75, PX + 75, 30, 145, zu - 8, zu + 12)
        J(1, [part("Pole", win(C["pole"], *bx), COL["pole"]),
              part("Enclosure back plate", win(C["enc_plate"], *bx), COL["plate"]),
              part("V-saddle", win(C["enc_saddle_1"], *bx), COL["saddle"]),
              part("M8 U-bolt, nuts on the plate front", win(C["enc_ubolt_1"], *bx), COL["ubolt"])],
          "U-bolt, V-saddle, pole and back plate", "Cut level with the upper U-bolt, seen from above. The pole sits on both faces of the V",
          elev=75, azim=-90, size=(8, 6))
    if go(2):
        bx = (PX + 70, PX + 135, 25, 70, EZ + 110, EZ + 175)
        J(2, [part("Enclosure back plate", win(C["enc_plate"], *bx), COL["plate"]),
              part("Enclosure body", win(C["enc_base"], *bx), COL["body"]),
              part("Lug (maker's kit)", win(C["lugs"], *bx), COL["lugs"]),
              part("M5 screw and nyloc nut", win(C["lug_screws"], *bx), COL["bolt"])],
          "enclosure lug on the back plate (top right corner)", "The lug's foot sits on the box top, its tab flat on the plate; one M5 screw",
          elev=25, azim=-55, size=(8, 6))
    if go(3):
        zb = D["enc_bot"]
        bx = (PX - 105, PX + 105, -65, 65, zb - 45, zb + 8)
        J(3, [part("Enclosure bottom", win(C["enc_base"], *bx), COL["body"]),
              part("Glands (six) and vent", win(C["glands"], *bx), COL["glands"]),
              part("Antenna bulkhead and whip", win(C["antenna"], *bx), COL["antenna"])],
          "the bottom face, seen from below", "Back row 28 mm and front row 70 mm from the back face; flanges at least 16 mm apart",
          elev=-55, azim=-70, size=(8, 6))
    if go(4):
        mz = EZ + P["mplate_z"] + P["mplate"][1] / 2
        zb = mz - P["mplate"][1] / 2 + 10
        bx = (PX + 78, PX + 88, 15, 62, zb - 50, zb + 50)
        J(4, [part("Enclosure body (cut open)", win(C["enc_base"], *bx), COL["body"]),
              part("Internal plate", win(C["mplate"], *bx), COL["mplate"]),
              part("M4 screw into the moulded boss", win(C["mplate_screws"], *bx), COL["bolt"]),
              part("Controller on 6 mm standoffs", win(C["board"], *bx), COL["board"])],
          "internal plate on a moulded boss (lower right)", "A thin slice through the boss, seen from the right. Plate 6 mm off the back wall, 37 mm above the floor",
          elev=6, azim=10, size=(8, 6))
    if go(5):
        sx = P["enc"][0] / 2 + P["shield_gap"] - P["shield_flange"] / 2
        zs = EZ + P["enc"][2] / 2 - 20
        bx = (PX + 88, PX + 135, 25, 70, zs - 2, zs + 8)
        J(5, [part("Enclosure back plate", win(C["enc_plate"], *bx), COL["plate"]),
              part("Enclosure body", win(C["enc_base"], *bx), COL["body"]),
              part("Sun shield side and flange", win(C["shield"], *bx), "#D6D3D1"),
              part("M5 thumb screw", win(C["shield_screws"], *bx), COL["bolt"])],
          "sun shield flange on the back plate (right side, upper screw)", f"Cut level with the screw, seen from above. The flange lies flat on the plate; screw {sx:.1f} mm from the centre line",
          elev=78, azim=-90, size=(8, 6))
    if go(6):
        bx = (PX - 60, PX + 60, -5, 125, CZ - 3, CZ + 3)
        J(6, [part("Pole", win(C["pole"], PX - 60, PX + 60, -5, 140, CZ - 3, CZ + 3), COL["pole"]),
              part("Cell back plate", win(C["cell_plate"], *bx), COL["plate"]),
              part("Flow cell body, 14 mm back wall", win(C["cell_body"], *bx), "#94A3B8"),
              part("M5 screws from behind, 10 mm into the wall", win(C["cell_screws"], *bx), COL["bolt"])],
          "flow cell on its back plate", "Cut through the two screws, seen from above. The screws stop 4 mm short of the water",
          elev=80, azim=-90, size=(8, 6))
    if go(7):
        x0 = PX + P["cl_xy"][0]
        bx = (PX - 50, PX + 50, CY + P["cl_xy"][1] - 0.01, CY + 40, D["body_top"] - 45, D["cell_top"] + 25)
        J(7, [part("Flow cell body (cut open)", win(C["cell_body"], *bx), "#94A3B8"),
              part("Gasket", win(C["gasket"], *bx), COL["gasket"]),
              part("Lid", win(C["cell_lid"], *bx), "#475569"),
              part("Glands", win(C["lid_glands"], *bx), COL["glands"]),
              part("Blanking plug (spare pH port)", win(C["plug"], *bx), COL["plug"]),
              part("Chlorine sensor", win(C["chlorine"], *bx), COL["chlorine"]),
              part("Stud and thumb nut", win(C["studs"], *bx), COL["bolt"])],
          "cell lid, gasket, glands and studs", "Cut through the chlorine sensor, seen from the front. The lid lifts off with the sensors",
          elev=8, azim=-90, size=(8, 6))
        del x0
    if go(8):
        zc = D["cav_z"]
        bx = (PX - 70, PX + 70, -30, 70, zc - 2, zc + 2)
        J(8, [part("Flow cell body and baffle", win(C["cell_body"], *bx), COL["cell"]),
              part("LED holder (left wall)", win(C["led_holder"], *bx), COL["optics"]),
              part("180 degree detector (right wall)", win(C["ref_holder"], *bx), "#EAB308"),
              part("90 degree detector (front wall)", win(C["det90_holder"], *bx), "#CA8A04"),
              part("Chlorine sensor", win(C["chlorine"], *bx), COL["chlorine"]),
              part("Temperature probe", win(C["temp"], *bx), COL["temp"]),
              part("Cell back plate", win(C["cell_plate"], *bx), COL["plate"]),
              part("Light path and sight line", win(beam(P)[0] + beam(P)[1], *bx), "#DC2626")],
          "the light path in the flow cell", "Cut at the windows, seen from above. The beam runs 13 mm in front of the centre; nothing stands in it",
          elev=82, azim=-90, size=(10, 6))
    if go(9):
        vz = D["valve_z"]
        bx = (PX - 60, PX + 60, 0, 70, vz - 40, D["cell_bot"] + 12)
        J(9, [part("Cell back plate", win(C["cell_plate"], PX + 30, PX + 60, 55, 70, D["valve_z"] - 40, D["cell_bot"] + 12), COL["plate"]),
              part("Latching valve", win(C["valve"], *bx), COL["valve"]),
              part("Valve to cell tube, push-fit elbow", win(C["cell_tube"], *bx), COL["tube"]),
              part("Inlet fitting, 1/8 BSPT", win(C["inlet_fit"], *bx), COL["fit"]),
              part("Supply tube from the regulator", win(C["supply_tube"], *bx), COL["tube"]),
              part("Flow cell floor", win(C["cell_body"], *bx), COL["cell"])],
          "valve under the cell", "Seen from the front right. Two M4 screws from behind; water in from the right, out upward into the cell floor",
          elev=10, azim=-60, size=(8, 6))
    if go(10):
        oz = D["outlet_z"]
        bx = (PX + 30, PX + 95, 0, 70, oz - 60, oz + 70)
        J(10, [part("Flow cell body", win(C["cell_body"], *bx), COL["cell"]),
               part("Outlet hose tail, 3/8 BSP", win(C["outlet_fit"], *bx), COL["fit"]),
               part("Tee with open air-break vent, and hose", win(C["drain"], *bx), COL["drain"]),
               part("180 degree detector", win(C["ref_holder"], *bx), COL["optics"])],
          "outlet and air break", "Seen from the front right. The vent stays open, so the hose can never siphon the cell or touch the water in it",
          elev=12, azim=-35, size=(8, 6))
    if go(11):
        pt = P["pole_h"]
        bx = (PX - 140, PX + 140, PY - 160, PY + 50, pt - 260, pt + 140)
        J(11, [part("Pole", win(C["pole"], PX - 40, PX + 40, PY - 40, PY + 40, pt - 260, pt - P["sleeve"][1] + 4), COL["pole"]),
               part("Pole-top tilt mount (bought)", win(C["panel_mount"], *bx), COL["mount"]),
               part("Solar panel", win(C["panel"], *bx), COL["panel"]),
               part("Panel lead", win(C["panel_lead"], *bx), COL["cable"])],
          "panel on the pole-top mount", "Seen from the front left, below the panel. The sleeve slides over the pole top; two set screws hold it",
          elev=-8, azim=-130, size=(8, 6))
    if go(12):
        tz = P["tee_z"]
        ro = P["riser_od"] / 2
        bx = (-40, 200, -30, 30, tz - 40, tz + 60)
        J(12, [part("Existing riser (not in the bill)", win(riser_context(P), *bx), COL["pole"]),
               part("Saddle tee", win(C["tee"], *bx), COL["fit"]),
               part("Isolation valve", win(C["fittings"], ro + 29, ro + 56, -30, 30, tz - 40, tz + 60), "#B45309"),
               part("Strainer", win(C["fittings"], ro + 56, ro + 91, -30, 30, tz - 40, tz + 60), "#CA8A04"),
               part("Check valve (arrow away from the riser)", win(C["fittings"], ro + 91, ro + 104, -30, 30, tz - 40, tz + 60), "#DC2626"),
               part("Regulator, 0.5 L/min", win(C["fittings"], ro + 104, ro + 156, -30, 30, tz - 40, tz + 60), "#7C2D12"),
               part("Supply tube, 1/4 in", win(C["supply_tube"], *bx), COL["tube"])],
           "saddle tee and fittings on the riser", "Seen from the front. Flow from left to right; the check valve's arrow points away from the riser",
           elev=15, azim=-80, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    want = sys.argv[2:] if len(sys.argv) > 2 and sys.argv[1] == "steps" else None
    M = named()
    out = []

    def go(n):
        return want is None or str(n) in want

    def st(n, done, new, title, sub, **kw):
        if go(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    body = part("Enclosure body", C["enc_base"], COL["body"])
    st(1, [body], [mv(part("Glands (six) and vent", C["glands"], COL["glands"]), (0, 0, -90)),
                   mv(part("Antenna bulkhead and whip", C["antenna"], COL["antenna"]), (0, 0, -160))],
       "glands, vent and antenna into the box", "Each from below, seal outside, nut inside; the blanking plug in the spare gland. Seen from below",
       elev=-28, azim=-60, label_done=False)
    st(2, [body, M["entries"]], [mv(M["lugs"], (0, 70, 0))], "lugs onto the box corners",
       "Seen from behind. The maker's four lugs, feet on the top and bottom, tabs flush with the back face",
       elev=20, azim=45, label_done=False)
    st(3, [part("Internal plate", C["mplate"], COL["mplate"])],
       [mv(part("Battery (fuse out), strap", C["battery"], COL["battery"]), (0, -80, 0)),
        mv(part("Controller board", C["board"], COL["board"]), (0, -80, 0)),
        mv(part("Cellular modem", C["modem"], COL["modem"]), (0, -80, 0))],
       "build the internal plate", "Boards on M3 screws and 6 mm standoffs, battery under its strap; then wire them as the wiring picture shows",
       elev=12, azim=-35, label_done=True)
    boxd = [body, M["entries"], M["lugs"]]
    st(4, boxd, [mv(part("Internal plate with battery, controller, modem", fuse(["mplate", "mplate_screws", "battery", "board", "modem"]), "#0F766E"), (0, -200, 0))],
       "internal plate into the box", "Four M4 screws into the moulded bosses; connect the antenna pigtail; fresh desiccant",
       elev=15, azim=-50, label_done=False)
    inside = part("Internal plate and parts", fuse(["mplate", "battery", "board", "modem"]), COL["mplate"])
    st(5, [M["enc_plate"]], [mv(part("Box with lugs and parts inside", fuse(["enc_base", "glands", "antenna", "lugs", "lug_screws", "mplate", "battery", "board", "modem"]), COL["body"]), (0, -150, 0))],
       "box onto the enclosure back plate", "Box back flat on the plate, centred, 80 mm above its bottom edge; four M5 screws from behind, nyloc nuts in front",
       elev=18, azim=-50, label_done=True)
    cbody = part("Flow cell body", C["cell_body"], COL["cell"])
    st(6, [cbody], [mv(part("LED holder", C["led_holder"], COL["optics"]), (-60, 0, 0)),
                    mv(part("90 degree detector holder", C["det90_holder"], "#CA8A04"), (0, -60, 0)),
                    mv(part("180 degree detector holder", C["ref_holder"], "#EAB308"), (60, 0, 0))],
       "optics holders onto the cell", "Windows bedded first; each holder on two M3 screws, leads up. The LED goes on the left wall, hidden here",
       elev=22, azim=-50, label_done=False)
    st(7, [M["cell_plate"]], [mv(part("Flow cell with its optics", fuse(["cell_body", "led_holder", "det90_holder", "ref_holder"]), COL["cell"]), (0, -120, 0))],
       "cell onto the cell back plate", "Back face flat on the plate, 213 mm above its bottom edge; two M5 screws from behind, snug (plastic)",
       elev=15, azim=-50, label_done=True)
    celld = [M["cell_plate"], part("Flow cell and optics", fuse(["cell_body", "led_holder", "det90_holder", "ref_holder"]), COL["cell"])]
    st(8, celld, [mv(part("Latching valve", C["valve"], COL["valve"]), (0, -110, 0))],
       "valve onto the cell plate", "Coil up, inlet on the right; two M4 screws from behind",
       elev=15, azim=-50, label_done=False)
    st(9, celld + [M["valve"]], [mv(part("Inlet fitting", C["inlet_fit"], COL["fit"]), (0, 0, -40)),
                                 mv(part("Valve to cell tube and elbow", C["cell_tube"], COL["tube"]), (-40, 0, 0)),
                                 mv(part("Outlet hose tail", C["outlet_fit"], COL["fit"]), (50, 0, 0))],
       "fittings and the valve-to-cell tube", "Thread tape on the inlet and outlet threads, hand tight plus a quarter turn; push the tube fully home",
       elev=10, azim=-50, label_done=False)
    st(10, celld + [M["valve"], M["fits"]], [mv(part("Gasket", C["gasket"], COL["gasket"]), (0, 0, 40)),
                                             mv(part("Lid with glands, plug, thumb nuts", fuse(["cell_lid", "lid_glands", "plug", "studs"]), "#475569"), (0, 0, 90)),
                                             mv(part("Chlorine sensor and temperature probe", fuse(["chlorine", "temp"]), COL["chlorine"]), (0, 0, 200))],
       "gasket, lid and sensors", "Studs in, gasket, lid, thumb nuts finger tight; sensors to depth (chlorine tip 40 mm in), glands tight",
       elev=20, azim=-50, label_done=False)
    # site steps
    footing = part("Concrete footing (cast on the survey visit)", C["footing"], "#D6D3D1")
    st(11, [part("Existing tapstand riser", riser_context(P), COL["pole"])], [mv(part("Pole", C["pole"], COL["pole"]), (0, 0, 500)), mv(footing, (0, 0, 0))],
       "pole and footing (survey visit)", "Dig 300 mm round, 600 mm deep, 470 mm from the riser; set the pole plumb in fast-set concrete",
       elev=12, azim=-55, label_done=True)
    st(12, [part("Existing riser", riser_context(P) & span(-40, 40, -40, 40, 300, 700), COL["pole"])],
       [mv(part("Saddle tee", C["tee"], COL["fit"]), (0, -80, 0)), mv(part("Valve, strainer, check valve, regulator", C["fittings"], "#A16207"), (90, 0, 0))],
       "saddle tee and fittings on the riser", "Supply shut off first. Tee 500 mm above the ground; fittings on thread tape, check valve arrow away from the riser",
       elev=15, azim=-70, label_done=True)
    cellset = part("Cell plate with cell, valve, lid and sensors", fuse(["cell_plate", "cell_body", "led_holder", "det90_holder", "ref_holder", "valve", "inlet_fit", "cell_tube", "outlet_fit", "gasket", "cell_lid", "lid_glands", "plug", "studs", "chlorine", "temp"]), COL["cell"])
    sad_c = part("V-saddles and U-bolts", fuse(["cell_saddle_0", "cell_saddle_1", "cell_ubolt_0", "cell_ubolt_1"]), COL["saddle"])
    st(13, [pole_section(450, 1150)], [mv(cellset, (0, -160, 0)), mv(sad_c, (0, 140, 0))],
       "cell plate onto the pole", "Cell top 900 mm above the ground. Saddles between plate and pole, U-bolts round the pole, M8 nyloc nuts in front",
       elev=15, azim=55, label_done=True)
    encset = part("Enclosure plate with the box", fuse(["enc_plate", "enc_base", "glands", "antenna", "lugs", "lug_screws", "mplate", "battery", "board", "modem", "enc_lid"]), COL["body"])
    sad_e = part("V-saddles and U-bolts", fuse(["enc_saddle_0", "enc_saddle_1", "enc_ubolt_0", "enc_ubolt_1"]), COL["saddle"])
    st(14, [pole_section(550, 1650), cellset], [mv(encset, (0, -200, 0)), mv(sad_e, (0, 160, 0))],
       "enclosure plate onto the pole", "Box centre 1,300 mm above the ground, square with the cell plate below. Same U-bolts and saddles",
       elev=15, azim=55, label_done=True)
    st(15, [pole_section(1850, P["pole_h"])], [mv(part("Pole-top tilt mount", C["panel_mount"], COL["mount"]), (0, 0, 120)),
                                                 mv(part("Solar panel", C["panel"], COL["panel"]), (0, 0, 260))],
       "panel mount and panel on the pole top", "Sleeve over the pole top, two set screws; panel on the mount's bolts, facing the equator at 30 degrees",
       elev=12, azim=-55, label_done=False)
    st(16, [pole_section(100, 1150), cellset, part("Existing riser and fittings", riser_context(P) + C["tee"] + C["fittings"], COL["pole"])],
       [mv(part("Supply tube, 1/4 in", C["supply_tube"], COL["tube"]), (0, -100, 0)), mv(part("Air-break tee and drain hose", C["drain"], COL["drain"]), (80, 0, 0))],
       "supply tube and drain hose", "Push-fit tube from the regulator to the valve inlet; tee on the hose tail, vent up; hose to the basin",
       elev=15, azim=-50, label_done=False)
    st(17, [pole_section(700, 1600), cellset, encset], [mv(part("Panel lead, valve, sensor and optics cables", fuse(["panel_lead", "valve_cable", "chlorine_cable", "temp_cable", "optics_cable", "status_cable"]) & span(PX - 200, PX + 200, -100, 200, 700, 1600), COL["cable"]), (0, -60, 0))],
       "cables into their glands; close the lid", "Drip loop below each gland; tighten the gland caps; lid gasket clean, lid screws in a cross pattern",
       elev=12, azim=-40, label_done=False)
    st(18, [pole_section(1000, 1600), encset], [mv(M["shield"], (0, -220, 0))],
       "sun shield", "Slide it over the box from the front until its flanges lie on the plate; four M5 thumb screws, finger tight",
       elev=18, azim=-45, label_done=False)
    st(19, [pole_section(1000, 1600), encset, part("Sun shield", C["shield"], COL["shield"])],
       [mv(M["status"], (0, -90, -70))],
       "status light unit", "Unit up into the shield slot, lens out; lead hangs to its own gland. Pull it down to remove the shield",
       elev=14, azim=-40, label_done=False)
    return out


# ----------------------------------------------------------------- drilling layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    OUT.mkdir(parents=True, exist_ok=True)
    res = []

    def foot(fig):
        fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
        fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")

    # enclosure bottom face, seen from below with the back face at the top of the page
    ew, ed = P["enc"][0], P["enc"][1] - P["lid_t"]
    fig = plt.figure(figsize=(11, 7), dpi=150)
    ax = fig.add_axes([0.04, 0.08, 0.92, 0.76]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-ew / 2, 0), ew, ed, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-ew / 2, ed), ew, P["lid_t"], fc="white", ec=MUT, lw=0.8, ls="--"))
    ax.text(-ew / 4, ed + P["lid_t"] / 2, "lid (do not drill)", ha="center", va="center", fontsize=7.5, color=MUT)
    ax.text(-ew / 2, -3, "back face (goes against the back plate), toward you", ha="left", va="top", fontsize=8, color=MUT)
    ax.plot([0, 0], [-2, ed + 2], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    names = {"valve": "Valve cable", "chlorine": "Chlorine", "ph_spare": "Spare, plugged", "temp": "Temperature",
             "panel": "Panel lead", "optics": "Optics", "vent": "Vent", "antenna": "Antenna", "status": "Status light lead"}
    for k, (x, row) in P["pens"].items():
        y = P["pen_rows"][row]
        hole = {"vent": 12.2, "antenna": 6.5}.get(k, 16.2)
        fl = {"vent": 18, "antenna": 18}.get(k, 24)
        ax.add_patch(plt.Circle((x, y), fl / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.add_patch(plt.Circle((x, y), hole / 2, fc="white", ec=INK, lw=1.1))
        ax.plot([x - fl / 2 - 2, x + fl / 2 + 2], [y, y], color=MUT, lw=0.4); ax.plot([x, x], [y - fl / 2 - 2, y + fl / 2 + 2], color=MUT, lw=0.4)
        side = "left" if x < 0 else "right"
        if x == 0:     # on the centre line, between the rows: label above the rows, with a leader down the centre line
            ax.plot([0, 0], [y + fl / 2 + 2, 88], color=AC, lw=0.7)
            ax.text(0, 89, f"{names[k]} gland: {hole:g} hole, on the centre line", ha="center", va="bottom", fontsize=7, color=INK,
                    bbox=dict(boxstyle="round,pad=0.15", fc="#F3F4F6", ec="none"))
            continue
        xt = x + ((-5 if x < 0 else 5) if (row == 1 and abs(x) == 22) else 0)    # clear of the middle-row gland
        ax.text(xt, y - fl / 2 - 1.5, f"{names[k]}\n{hole:g} hole, {abs(x):g} {side}", ha="center", va="top", fontsize=7, color=INK,
                linespacing=1.2, bbox=dict(boxstyle="round,pad=0.15", fc="#F3F4F6", ec="none"))
    for r in P["pen_rows"]:
        ax.plot([ew / 2, ew / 2 + 12], [r, r], color=AC, lw=0.5, ls=":")
        ax.text(ew / 2 + 13, r, f"{r:g} from the back face", va="center", fontsize=8, color=AC)
    ax.set_xlim(-ew / 2 - 8, ew / 2 + 62); ax.set_ylim(-12, ed + P["lid_t"] + 3)
    fig.text(0.03, 0.97, "Enclosure bottom face: drilling layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Box standing upside down on its top, back face toward you (bottom of the page). Sideways from the centre line, left and right as seen from the front.\n"
             "Solid circle: the hole to drill (mm). Dashed circle: the outside flange of the part that goes in it.", fontsize=8.2, color=MUT, va="top")
    foot(fig)
    fig.savefig(OUT / "base-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "base-holes.png")

    # both back plates, front faces
    fig = plt.figure(figsize=(11, 9), dpi=150)
    fig.text(0.03, 0.975, "Back plates: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.945, "Seen from the front (the face the box or cell sits on). Heights up from the bottom edge, sideways from the centre line, mm.",
             fontsize=8.5, color=MUT, va="top")
    foot(fig)

    def plate(ax, w, h, holes, outlines, title):
        ax.set_aspect("equal"); ax.set_axis_off()
        ax.add_patch(Rectangle((-w / 2, 0), w, h, fc="#F5F5F4", ec=INK, lw=1.2))
        ax.plot([0, 0], [-8, h + 8], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
        for (x0, z0, ww, hh, nm) in outlines:
            ax.add_patch(Rectangle((x0, z0), ww, hh, fc="none", ec=AC, lw=0.8, ls="--"))
            ax.text(x0 + 3, z0 + hh - 3, nm, ha="left", va="top", fontsize=7.5, color=AC)
        zs = set()
        for (x, z, d, nm) in holes:
            for s in (-1, 1):
                ax.add_patch(plt.Circle((s * x, z), d / 2, fc="white", ec=INK, lw=1))
            ax.plot([x + d / 2 + 1, w / 2 + 4], [z, z], color=MUT, lw=0.4, ls=":")
            ax.text(w / 2 + 5, z, nm, fontsize=7, va="center", color=INK)
            zs.add(z)
        for i, z in enumerate(sorted(zs)):
            ax.plot([-w / 2 - 14, -w / 2], [z, z], color=AC, lw=0.4, ls=":")
            ax.text(-w / 2 - 15, z, f"{z:g}", ha="right", va="center", fontsize=7.5, color=AC)
        ax.text(0, -16, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.set_xlim(-w / 2 - 40, w / 2 + 110); ax.set_ylim(-34, h + 10)

    ax1 = fig.add_axes([0.02, 0.06, 0.56, 0.86])
    plate(ax1, 270, 420, [(29, 25, 9, "U-bolt 9, at 29"), (29, 395, 9, "U-bolt 9, at 29"), (85, 67, 5.5, "lug 5.5, at 85"),
                          (85, 353, 5.5, "lug 5.5, at 85"), (117.5, 100, 4.2, "M5 tapped, at 117.5"), (117.5, 320, 4.2, "M5 tapped, at 117.5")],
          [(-100, 80, 200, 260, "box 200 x 260")], "Enclosure back plate, 270 x 420 x 3")
    ax2 = fig.add_axes([0.6, 0.06, 0.38, 0.86])
    plate(ax2, 140, 385, [(29, 25, 9, "U-bolt 9"), (29, 360, 9, "U-bolt 9"), (30, 250, 5.5, "cell 5.5, at 30"), (18, 93, 4.5, "valve 4.5, at 18")],
          [(-48, 213, 96, 74, "cell"), (-27.5, 63, 55, 60, "valve")], "Cell back plate, 140 x 385 x 3")
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "plate-holes.png")

    # cell lid and top of the body
    fig = plt.figure(figsize=(10, 6.2), dpi=150)
    ax = fig.add_axes([0.04, 0.08, 0.7, 0.78]); ax.set_aspect("equal"); ax.set_axis_off()
    W, Dp = 96, 60
    ax.add_patch(Rectangle((-W / 2, 0), W, Dp, fc="#E5E7EB", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-40, 8), 80, 38, fc="none", ec=MUT, lw=0.7, ls="--"))
    ax.text(-6, 9.5, "pocket below (gasket window)", fontsize=6.5, color=MUT, va="bottom", ha="right")
    ax.plot([0, 0], [-1, Dp + 4], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    f0 = 27   # cavity centre from the front edge
    items = [(P["cl_xy"][0], f0 + P["cl_xy"][1], 25, 33, "Chlorine M25"), (P["ph_x"], f0 + P["ph_y"], 20, 27, "Spare pH M20"),
             (P["t_xy"][0], f0 + P["t_xy"][1], 12, 17, "Temp M12")]
    for x, y, d, fl, nm in items:
        ax.add_patch(plt.Circle((x, y), fl / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.add_patch(plt.Circle((x, y), d / 2, fc="white", ec=INK, lw=1.1))
        ax.text(x, y, f"{nm}\n{abs(x):g} {'left' if x < 0 else 'right'}, {y:g}", ha="center", va="center", fontsize=6.3, color=INK, linespacing=1.15)
    for sx, sy in P["studs"]:
        ax.add_patch(plt.Circle((sx, f0 + sy), 2.25, fc="white", ec=INK, lw=1))
    ax.text(W / 2 + 2, 4, "stud holes 4.5 at 44 each side,\n4 and 53 from the front", fontsize=7, va="center", color=AC)
    ax.text(-W / 4, -2, "front edge (measure from here)", ha="center", va="top", fontsize=7.5, color=MUT)
    ax.set_xlim(-W / 2 - 4, W / 2 + 40); ax.set_ylim(-9, Dp + 3)
    fig.text(0.03, 0.97, "Flow cell lid: hole layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Seen from above, front edge at the bottom. Sideways from the centre line, then distance from the front edge, mm.\n"
             "Solid circle: tapped hole. Dashed circle: the gland or plug's outside size. The same studs hold the gasket.", fontsize=8.2, color=MUT, va="top")
    foot(fig)
    fig.savefig(OUT / "lid-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "lid-holes.png")
    return res


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 74); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 72, "WaterWatch prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 68.6, "Bought carrier board and modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((25, 14), 61, 49, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(25.5, 61.8, "Inside the enclosure, on the internal plate", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.2, sub, ha="center", va="top", fontsize=7.1, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.1, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#374151"
    blk(3, 47, 15, 11, "Solar panel", "5 W, 6 V class\non the pole top", "#1E3A8A")
    blk(27, 20, 18, 14, "LiFePO4 battery", "3.2 V, 6 Ah, protection\nboard, NTC, 3 A fuse\nin its lead", "#C2410C")
    blk(30, 40, 30, 19, "Controller carrier board", "ESP32-S3, solar charger with\n0 to 45 °C cut-off, potentiostat,\n12 V boost and valve driver,\nmicroSD, real-time clock", "#0F766E")
    blk(64, 44, 18, 15, "Cellular modem", "LTE-M, NB-IoT, 2G\nSIM holder", "#7C3AED")
    blk(98, 52, 19, 9, "Antenna", "whip under the box", RF)
    wire([(10.5, 47), (10.5, 44), (30, 44)], RED); lab(11.5, 45.6, "panel lead, gland, 0.5 mm²", RED)
    wire([(36, 34), (36, 40)], RED); lab(35.4, 37, "0.75 mm²", RED, "right")
    wire([(42, 34), (42, 40)], GRY, 1.2); lab(42.6, 37, "NTC", GRY)
    wire([(60, 53), (64, 53)], BLU); lab(62, 55, "UART", BLU, "center")
    wire([(60, 49), (64, 49)], RED); lab(62, 47.2, "power", RED, "center")
    wire([(82, 55), (98, 56.5)], RF, 1.2); lab(90, 58, "RF pigtail", RF, "center")
    sens = [("Chlorine sensor", "WE, RE, CE + screen", "#2563EB", "screened 3-core", BLU),
            ("Temperature probe", "DS18B20, 3 wires", "#16A34A", "3-core", BLU),
            ("Optics", "LED + 2 detectors, 6 wires", "#D4A017", "6-core", BLU),
            ("Latching valve", "12 V coil, 2 wires", "#115E59", "2-core, 0.5 mm²", RED)]
    for k, (t, sub, colr, cab, wc) in enumerate(sens):
        y0 = 31 - 8.5 * k
        blk(98, y0, 19, 7, t, sub, colr)
        ym = y0 + 3.5
        xk = 58 - 4 * k
        wire([(xk, 40), (xk, ym), (98, ym)], wc)
        lab(96, ym + 1.6, cab, MUT, "right")
    blk(98, 42, 19, 7, "Status light", "5 mm LED, 5 mA, in the shield", "#16A34A")
    wire([(60, 46), (63, 46), (63, 41), (94, 41), (94, 45.5), (98, 45.5)], RED); lab(92, 39.6, "status lead, own gland, 2-core", MUT, "right")
    ax.text(2, 40, "Each cable enters through its own\ngland in the bottom face (see the\ndrilling layout). Leave a drip loop\nbelow every gland.",
            fontsize=7.2, color=MUT, va="top", linespacing=1.4)
    ax.text(2, 11.5, "Safety: battery fuse out until the\nstop points in section 6 are passed.\nCharging only between 0 and 45 °C.",
            fontsize=7.4, color="#B45309", fontweight="bold", va="top", linespacing=1.4)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    if len(sys.argv) > 1 and sys.argv[1] in fns:
        print(sys.argv[1], "->", fns[sys.argv[1]]())
    else:
        for w in fns:
            print(w, "->", fns[w]())
