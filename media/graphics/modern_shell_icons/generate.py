#!/usr/bin/env python3
"""Generate the original ReactOS Fluent shell icon set."""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
S = 4
CANVAS = 256
PX = CANVAS * S
ICO_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]


def q(values):
    return tuple(int(v * S) for v in values)


def canvas():
    return Image.new("RGBA", (PX, PX), (0, 0, 0, 0))


def draw_layer(im):
    layer = canvas()
    return layer, ImageDraw.Draw(layer)


def shadow(im, box, radius=22, offset=(0, 7), alpha=42):
    layer = canvas()
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    ox, oy = offset
    d.rounded_rectangle(q((x0 + ox, y0 + oy, x1 + ox, y1 + oy)),
                        radius=radius * S, fill=(25, 43, 68, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(7 * S))
    im.alpha_composite(layer)


def gradient(im, box, top, bottom, radius=0, outline=None, width=0):
    x0, y0, x1, y1 = box
    mask = Image.new("L", (PX, PX), 0)
    md = ImageDraw.Draw(mask)
    if radius:
        md.rounded_rectangle(q(box), radius=radius * S, fill=255)
    else:
        md.rectangle(q(box), fill=255)
    grad = canvas()
    gd = ImageDraw.Draw(grad)
    sy0, sy1 = int(y0 * S), int(y1 * S)
    for y in range(sy0, sy1 + 1):
        t = (y - sy0) / max(1, sy1 - sy0)
        color = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
        gd.line((int(x0 * S), y, int(x1 * S), y), fill=color)
    im.alpha_composite(Image.composite(grad, canvas(), mask))
    if outline:
        ImageDraw.Draw(im).rounded_rectangle(q(box), radius=radius * S,
                                             outline=outline, width=width * S)


def folder_base(opened=False):
    im = canvas()
    shadow(im, (24, 68, 232, 213), radius=23)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q((27, 55, 118, 105)), radius=17 * S,
                        fill=(255, 190, 42, 255))
    gradient(im, (24, 73, 232, 213), (255, 205, 61, 255),
             (245, 151, 18, 255), radius=22,
             outline=(218, 126, 8, 255), width=2)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q((36, 86, 216, 197)), radius=14 * S,
                        fill=(255, 226, 127, 210))
    if opened:
        # Raised front lip gives the open-folder silhouette.
        poly = q((21, 119, 225, 106, 205, 215, 42, 215))
        d.polygon(poly, fill=(255, 181, 30, 255))
        d.line(q((21, 119, 225, 106)), fill=(255, 226, 115, 255), width=4 * S)
    return im


def icon_document(text=False):
    im = canvas()
    shadow(im, (48, 25, 200, 228), radius=20)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q((47, 23, 201, 229)), radius=20 * S,
                        fill=(249, 252, 255, 255), outline=(186, 202, 220, 255), width=3 * S)
    d.polygon(q((151, 23, 201, 73, 151, 73)), fill=(213, 231, 247, 255))
    d.line(q((151, 23, 151, 73, 201, 73)), fill=(170, 195, 219, 255), width=3 * S)
    blue = (38, 126, 231, 255)
    d.rounded_rectangle(q((72, 101, 176, 113)), radius=6 * S, fill=blue)
    for y, end in ((137, 169), (164, 181), (191, 145)):
        d.rounded_rectangle(q((72, y, end, y + 8)), radius=4 * S,
                            fill=(112, 168, 224, 255) if text else (141, 184, 226, 255))
    return im


def icon_folder():
    return folder_base(False)


def icon_folder_open():
    return folder_base(True)


def icon_drive(optical=False):
    im = canvas()
    shadow(im, (26, 71, 230, 204), radius=25)
    gradient(im, (25, 68, 231, 201), (244, 249, 253, 255),
             (169, 190, 208, 255), radius=25,
             outline=(105, 133, 157, 255), width=3)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q((42, 156, 214, 187)), radius=11 * S,
                        fill=(79, 102, 124, 255))
    d.ellipse(q((181, 165, 195, 179)), fill=(45, 214, 133, 255))
    d.ellipse(q((202, 165, 216, 179)), fill=(45, 136, 232, 255))
    if optical:
        d.ellipse(q((73, 84, 178, 171)), fill=(207, 238, 250, 255),
                  outline=(108, 173, 207, 255), width=3 * S)
        d.ellipse(q((111, 115, 140, 144)), fill=(121, 155, 181, 255))
    else:
        d.rounded_rectangle(q((49, 91, 190, 139)), radius=11 * S,
                            fill=(213, 225, 235, 255))
    return im


def screen(im, box=(30, 34, 226, 184)):
    x0, y0, x1, y1 = box
    shadow(im, box, radius=22)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q(box), radius=22 * S, fill=(44, 59, 78, 255))
    gradient(im, (x0 + 9, y0 + 9, x1 - 9, y1 - 14),
             (54, 178, 246, 255), (23, 92, 203, 255), radius=12)
    d = ImageDraw.Draw(im)
    d.rectangle(q((111, y1, 145, 211)), fill=(95, 112, 130, 255))
    d.rounded_rectangle(q((78, 207, 178, 222)), radius=7 * S,
                        fill=(70, 88, 106, 255))


def icon_desktop():
    im = canvas()
    screen(im)
    d = ImageDraw.Draw(im)
    d.line(q((58, 151, 102, 108, 137, 137, 191, 79)),
           fill=(172, 232, 255, 210), width=8 * S, joint="curve")
    d.ellipse(q((177, 66, 199, 88)), fill=(255, 220, 83, 255))
    return im


def icon_computer():
    im = icon_desktop()
    d = ImageDraw.Draw(im)
    d.rectangle(q((65, 69, 119, 116)), fill=(223, 247, 255, 220))
    d.rectangle(q((126, 69, 180, 116)), fill=(175, 225, 253, 220))
    d.rectangle(q((65, 123, 119, 165)), fill=(175, 225, 253, 220))
    d.rectangle(q((126, 123, 180, 165)), fill=(223, 247, 255, 220))
    return im


def icon_network():
    im = canvas()
    shadow(im, (38, 35, 218, 220), radius=25)
    d = ImageDraw.Draw(im)
    d.ellipse(q((42, 32, 204, 194)), fill=(34, 166, 222, 255),
              outline=(24, 105, 180, 255), width=4 * S)
    grid = (221, 247, 255, 235)
    d.ellipse(q((84, 32, 162, 194)), outline=grid, width=5 * S)
    d.line(q((47, 85, 199, 85)), fill=grid, width=5 * S)
    d.line(q((47, 140, 199, 140)), fill=grid, width=5 * S)
    d.line(q((123, 37, 123, 189)), fill=grid, width=5 * S)
    # A single, clean connected-computer badge stays legible at 16 px.
    d.rounded_rectangle(q((132, 142, 224, 211)), radius=15 * S,
                        fill=(248, 252, 255, 255), outline=(57, 86, 121, 255), width=4 * S)
    d.rounded_rectangle(q((142, 152, 214, 190)), radius=8 * S,
                        fill=(79, 103, 220, 255))
    d.line(q((178, 191, 178, 202)), fill=(57, 86, 121, 255), width=5 * S)
    d.line(q((158, 202, 198, 202)), fill=(57, 86, 121, 255), width=5 * S)
    return im


def icon_settings(folder=False):
    im = folder_base(False) if folder else canvas()
    if not folder:
        shadow(im, (35, 35, 221, 221), radius=45)
    center = (153, 151) if folder else (128, 128)
    cx, cy = center
    outer = 64 if folder else 79
    inner = outer * .79
    points = []
    # Alternating radii make actual radial gear teeth instead of upright blocks.
    for i in range(32):
        a = math.radians(-90 + i * 11.25)
        tooth_phase = i % 4
        r = outer if tooth_phase in (0, 1) else inner
        points.append((int((cx + math.cos(a) * r) * S),
                       int((cy + math.sin(a) * r) * S)))
    gear = canvas()
    gd = ImageDraw.Draw(gear)
    gd.polygon(points, fill=(103, 83, 214, 255))
    gd.ellipse(q((cx - outer * .69, cy - outer * .69,
                  cx + outer * .69, cy + outer * .69)), fill=(111, 91, 221, 255))
    im.alpha_composite(gear)
    d = ImageDraw.Draw(im)
    d.ellipse(q((cx - 30, cy - 30, cx + 30, cy + 30)),
              fill=(236, 239, 255, 255), outline=(83, 67, 184, 255), width=3 * S)
    d.ellipse(q((cx - 14, cy - 14, cx + 14, cy + 14)), fill=(94, 77, 205, 255))
    return im


def icon_recycle(full=False):
    im = canvas()
    shadow(im, (48, 50, 208, 226), radius=22)
    d = ImageDraw.Draw(im)
    if full:
        for box, color in (((73, 51, 108, 86), (255, 189, 46, 255)),
                           ((115, 40, 154, 84), (72, 190, 139, 255)),
                           ((153, 54, 188, 89), (81, 142, 229, 255))):
            d.rounded_rectangle(q(box), radius=5 * S, fill=color)
    d.rounded_rectangle(q((52, 71, 204, 94)), radius=10 * S,
                        fill=(111, 143, 169, 255))
    d.rounded_rectangle(q((89, 45, 167, 67)), radius=9 * S,
                        fill=(111, 143, 169, 255))
    d.polygon(q((62, 94, 194, 94, 181, 222, 75, 222)),
              fill=(222, 239, 247, 245), outline=(92, 134, 164, 255))
    for x in (94, 128, 162):
        d.line(q((x, 113, x - 5, 198)), fill=(128, 166, 188, 255), width=5 * S)
    # Balanced three-arrow loop, drawn with explicit arrowheads for crisp downsizing.
    green = (37, 177, 115, 255)
    d.line(q((101, 166, 124, 129)), fill=green, width=9 * S)
    d.polygon(q((126, 117, 111, 139, 133, 137)), fill=green)
    d.line(q((132, 133, 157, 171)), fill=green, width=9 * S)
    d.polygon(q((164, 181, 155, 154, 143, 173)), fill=green)
    d.line(q((148, 185, 103, 185)), fill=green, width=9 * S)
    d.polygon(q((91, 185, 112, 171, 112, 199)), fill=green)
    return im


def icon_start():
    im = canvas()
    shadow(im, (37, 37, 219, 219), radius=40)
    gradient(im, (35, 35, 221, 221), (75, 190, 249, 255),
             (21, 99, 218, 255), radius=40)
    d = ImageDraw.Draw(im)
    gap = 8
    for x0, y0, x1, y1 in ((69, 68, 124-gap//2, 124-gap//2),
                           (132+gap//2, 68, 187, 124-gap//2),
                           (69, 132+gap//2, 124-gap//2, 188),
                           (132+gap//2, 132+gap//2, 187, 188)):
        d.rounded_rectangle(q((x0, y0, x1, y1)), radius=7 * S,
                            fill=(239, 250, 255, 250))
    return im


def icon_terminal():
    im = canvas()
    shadow(im, (27, 39, 229, 216), radius=30)
    gradient(im, (25, 36, 231, 214), (53, 66, 86, 255),
             (18, 25, 36, 255), radius=30,
             outline=(94, 118, 148, 255), width=3)
    d = ImageDraw.Draw(im)
    d.line(q((69, 91, 111, 127, 69, 163)), fill=(99, 217, 255, 255),
           width=12 * S, joint="curve")
    d.rounded_rectangle(q((123, 157, 188, 169)), radius=5 * S,
                        fill=(236, 245, 251, 255))
    return im


def icon_search():
    im = canvas()
    shadow(im, (32, 29, 220, 222), radius=42)
    d = ImageDraw.Draw(im)
    d.ellipse(q((43, 35, 177, 169)), fill=(211, 243, 255, 255),
              outline=(31, 132, 222, 255), width=15 * S)
    d.ellipse(q((71, 63, 149, 141)), fill=(116, 206, 247, 180))
    d.line(q((155, 154, 214, 213)), fill=(66, 78, 98, 255), width=24 * S)
    d.line(q((160, 159, 211, 210)), fill=(99, 114, 138, 255), width=12 * S)
    return im


def icon_power():
    im = canvas()
    shadow(im, (35, 35, 221, 221), radius=50)
    gradient(im, (34, 34, 222, 222), (255, 112, 102, 255),
             (215, 49, 75, 255), radius=50)
    d = ImageDraw.Draw(im)
    d.arc(q((69, 65, 187, 191)), start=-43, end=223,
          fill=(255, 248, 246, 255), width=17 * S)
    d.line(q((128, 57, 128, 126)), fill=(255, 248, 246, 255), width=17 * S)
    return im


def icon_browser():
    im = canvas()
    shadow(im, (35, 35, 221, 221), radius=50)
    d = ImageDraw.Draw(im)
    d.ellipse(q((38, 35, 218, 215)), fill=(41, 174, 226, 255),
              outline=(25, 111, 190, 255), width=4 * S)
    grid = (221, 249, 255, 230)
    d.ellipse(q((87, 35, 169, 215)), outline=grid, width=5 * S)
    d.line(q((44, 93, 212, 93)), fill=grid, width=5 * S)
    d.line(q((44, 151, 212, 151)), fill=grid, width=5 * S)
    d.line(q((128, 41, 128, 209)), fill=grid, width=5 * S)
    # Navigation pointer gives the globe an unambiguous browser identity.
    d.polygon(q((145, 116, 207, 134, 178, 151, 163, 195)),
              fill=(250, 252, 255, 255), outline=(49, 81, 121, 255))
    d.polygon(q((159, 131, 190, 139, 175, 148, 168, 170)), fill=(79, 95, 218, 255))
    return im


def icon_apps():
    im = canvas()
    shadow(im, (34, 64, 222, 224), radius=30)
    gradient(im, (32, 63, 224, 224), (131, 111, 237, 255),
             (62, 79, 200, 255), radius=30)
    d = ImageDraw.Draw(im)
    d.arc(q((76, 29, 180, 127)), start=190, end=350,
          fill=(71, 84, 133, 255), width=14 * S)
    colors=((255, 209, 71, 255),(96, 219, 173, 255),(104, 201, 248, 255),(255, 139, 123, 255))
    for box, color in zip(((70,103,121,151),(135,103,186,151),(70,166,121,210),(135,166,186,210)), colors):
        d.rounded_rectangle(q(box), radius=10 * S, fill=color)
    return im


def icon_explorer():
    im = folder_base(False)
    d = ImageDraw.Draw(im)
    d.ellipse(q((128, 113, 218, 203)), fill=(245, 252, 255, 255),
              outline=(38, 126, 219, 255), width=5 * S)
    d.polygon(q((173, 129, 190, 169, 151, 188, 166, 159)), fill=(46, 174, 226, 255))
    d.ellipse(q((169, 155, 181, 167)), fill=(255, 255, 255, 255))
    return im


def icon_documents():
    im = folder_base(False)
    doc = icon_document().resize((118 * S, 150 * S), Image.Resampling.LANCZOS)
    im.alpha_composite(doc, (118 * S, 82 * S))
    return im


def icon_new_folder():
    im = folder_base(False)
    d = ImageDraw.Draw(im)
    d.ellipse(q((143, 132, 225, 214)), fill=(39, 137, 231, 255),
              outline=(238, 249, 255, 255), width=5 * S)
    d.rounded_rectangle(q((179, 148, 190, 198)), radius=5 * S, fill=(255, 255, 255, 255))
    d.rounded_rectangle(q((159, 168, 210, 179)), radius=5 * S, fill=(255, 255, 255, 255))
    return im


def icon_generic_app():
    im = canvas()
    shadow(im, (32, 42, 224, 216), radius=26)
    gradient(im, (30, 40, 226, 214), (239, 248, 255, 255),
             (169, 211, 241, 255), radius=26,
             outline=(51, 122, 194, 255), width=3)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(q((30, 40, 226, 77)), radius=24 * S, fill=(39, 126, 222, 255))
    for x in (51, 70, 89):
        d.ellipse(q((x, 53, x + 9, 62)), fill=(224, 246, 255, 255))
    d.rounded_rectangle(q((58, 101, 114, 157)), radius=12 * S, fill=(91, 199, 239, 255))
    d.rounded_rectangle(q((130, 101, 198, 119)), radius=8 * S, fill=(101, 90, 221, 255))
    d.rounded_rectangle(q((130, 134, 183, 151)), radius=8 * S, fill=(69, 179, 134, 255))
    d.rounded_rectangle(q((58, 171, 198, 187)), radius=8 * S, fill=(114, 147, 181, 255))
    return im


ART = {
    "document": icon_document,
    "text": lambda: icon_document(True),
    "app": icon_generic_app,
    "folder": icon_folder,
    "folder_open": icon_folder_open,
    "new_folder": icon_new_folder,
    "drive": icon_drive,
    "optical": lambda: icon_drive(True),
    "network": icon_network,
    "computer": icon_computer,
    "settings": icon_settings,
    "settings_folder": lambda: icon_settings(True),
    "recycle_empty": lambda: icon_recycle(False),
    "recycle_full": lambda: icon_recycle(True),
    "desktop": icon_desktop,
    "start": icon_start,
    "terminal": icon_terminal,
    "search": icon_search,
    "power": icon_power,
    "browser": icon_browser,
    "apps": icon_apps,
    "explorer": icon_explorer,
    "documents": icon_documents,
}


SHELL32 = {
    "document": [1], "app": [3], "folder": [4], "folder_open": [5],
    "drive": [9], "optical": [12], "network": [14, 15, 18, 172, 257, 259],
    "computer": [16, 43], "settings": [22, 36, 137, 274, 321, 330],
    "settings_folder": [148, 210], "search": [23, 323, 337],
    "power": [28, 221, 329], "recycle_empty": [32, 191, 254],
    "recycle_full": [33, 192, 240], "desktop": [35], "start": [40],
    "explorer": [46], "text": [152], "documents": [235],
    "terminal": [278], "new_folder": [319], "browser": [512],
    "apps": [20, 37, 271],
}


EXPLORER = {
    100: "explorer", 101: "folder", 103: "desktop", 107: "start",
    108: "recycle_empty", 205: "computer", 252: "folder",
    253: "browser", 257: "start",
}


def save_ico(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.resize((256, 256), Image.Resampling.LANCZOS).save(
        path, format="ICO", sizes=ICO_SIZES, bitmap_format="bmp")


def main():
    rendered = {name: func() for name, func in ART.items()}
    shell_dir = ROOT / "dll/win32/shell32/res/icons"
    for name, ids in SHELL32.items():
        for resource_id in ids:
            save_ico(rendered[name], shell_dir / f"{resource_id}.ico")

    explorer_dir = ROOT / "base/shell/explorer/res/ico"
    for resource_id, name in EXPLORER.items():
        save_ico(rendered[name], explorer_dir / f"{resource_id}.ico")

    save_ico(rendered["terminal"], ROOT / "base/shell/cmd/res/terminal.ico")
    save_ico(rendered["apps"], ROOT / "base/applications/rapps/res/main.ico")
    save_ico(rendered["apps"], ROOT / "base/applications/rapps_com/main.ico")

    labels = ["computer", "documents", "network", "browser", "recycle_empty",
              "recycle_full", "folder", "folder_open", "new_folder", "drive",
              "settings", "apps", "explorer", "terminal", "search", "power"]
    preview = Image.new("RGBA", (8 * 132, 2 * 132), (244, 247, 251, 255))
    pd = ImageDraw.Draw(preview)
    for i, name in enumerate(labels):
        x, y = (i % 8) * 132, (i // 8) * 132
        icon = rendered[name].resize((88, 88), Image.Resampling.LANCZOS)
        preview.alpha_composite(icon, (x + 22, y + 5))
        pd.text((x + 8, y + 102), name.replace("_", " "), fill=(32, 45, 62, 255))
    preview.convert("RGB").save(HERE / "preview.png", optimize=True)
    print(f"Generated {sum(map(len, SHELL32.values())) + len(EXPLORER) + 3} icon resources")


if __name__ == "__main__":
    main()
