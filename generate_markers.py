from PIL import Image, ImageDraw, ImageFont
import random
import os

def find_font(bold=False):
    """Cross-platform font lookup — tries common locations on Windows, macOS,
    and Linux in turn, falling back to PIL's built-in font if none are found."""
    candidates = [
        # Windows
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None  # caller falls back to PIL's built-in bitmap font

def make_marker(filename, label, sublabel, accent_color, pattern_seed):
    W, H = 800, 800
    img = Image.new('RGB', (W, H), '#FFFFFF')
    d = ImageDraw.Draw(img)

    random.seed(pattern_seed)

    d.rectangle([0,0,W,H], fill='#FFFFFF')
    d.rectangle([0,0,W-1,H-1], outline='#000000', width=18)
    d.rectangle([22,22,W-23,H-23], outline='#000000', width=6)

    cs = 90
    cm = 36
    for cx, cy in [(cm, cm), (W-cm-cs, cm), (cm, H-cm-cs), (W-cm-cs, H-cm-cs)]:
        d.rectangle([cx, cy, cx+cs, cy+cs], fill='#000000')
        d.rectangle([cx+12, cy+12, cx+cs-12, cy+cs-12], fill='#FFFFFF')
        d.rectangle([cx+24, cy+24, cx+cs-24, cy+cs-24], fill='#000000')

    dot_colors = ['#000000', '#222222', '#111111', accent_color, '#333333']
    for _ in range(280):
        x = random.randint(160, W-160)
        y = random.randint(160, H-160)
        r = random.randint(3, 10)
        col = random.choice(dot_colors)
        d.ellipse([x-r, y-r, x+r, y+r], fill=col)

    for i in range(0, W, 28):
        d.line([(i, 150), (i+200, 350)], fill='#CCCCCC', width=1)
        d.line([(W-i, 150), (W-i-200, 350)], fill='#CCCCCC', width=1)

    cx, cy = W//2, H//2
    for r in [200, 175, 140, 110, 70, 40]:
        col = accent_color if r % 70 == 0 else ('#000000' if r in [200, 140, 70] else '#FFFFFF')
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline='#000000', width=3,
                   fill=col if r in [200,140,70,40] else None)

    for _ in range(60):
        x = random.randint(140, W-140)
        y = random.randint(140, H-140)
        s = random.randint(6, 18)
        if abs(x-cx) > 90 or abs(y-cy) > 90:
            d.rectangle([x, y, x+s, y+s], fill='#000000')

    d.rectangle([36, H-130, W-36, H-36], fill='#000000')
    bold_path = find_font(bold=True)
    reg_path = find_font(bold=False)
    if bold_path:
        fnt_big = ImageFont.truetype(bold_path, 38)
    else:
        fnt_big = ImageFont.load_default(size=38)
    if reg_path:
        fnt_sm = ImageFont.truetype(reg_path, 22)
    else:
        fnt_sm = ImageFont.load_default(size=22)

    bbox = d.textbbox((0,0), label, font=fnt_big)
    tw = bbox[2]-bbox[0]
    d.text(((W-tw)//2, H-118), label, fill='#FFFFFF', font=fnt_big)

    bbox2 = d.textbbox((0,0), sublabel, font=fnt_sm)
    tw2 = bbox2[2]-bbox2[0]
    d.text(((W-tw2)//2, H-58), sublabel, fill=accent_color, font=fnt_sm)

    d.rectangle([36, 36, W-36, 110], fill='#000000')
    top_text = "ICMR NAVIGATION MARKER"
    bbox3 = d.textbbox((0,0), top_text, font=fnt_sm)
    tw3 = bbox3[2]-bbox3[0]
    d.text(((W-tw3)//2, 52), top_text, fill='#FFFFFF', font=fnt_sm)

    img.save(filename, 'PNG', dpi=(300,300))
    print(f"Created {filename}")


# ═══════════════════════════════════════════════════════════════
# IMPORTANT: generate + upload to the MindAR compiler in this EXACT
# order (00 -> 14). The order becomes targetIndex 0-14, which is
# hardcoded in index.html's NODES object. Do not reorder without
# also updating targetIndex values in the code.
#
# Colour key used below (matches the app's own colour language):
#   green  = plain walk / straight segments
#   blue   = branch / decision points
#   purple = lift or stairs entry points (transit)
#   orange = arrival points
# ═══════════════════════════════════════════════════════════════

make_marker('00-ENT.png',         'MARKER 0 - ENTRANCE',        'ENTRANCE -> RECEPTION',      '#00AA44', 1)
make_marker('01-RECEPTION.png',   'MARKER 1 - RECEPTION',       'BRANCH: STAIRS OR CORRIDOR', '#0055CC', 2)
make_marker('02-CORR_END.png',    'MARKER 2 - CORRIDOR END',    'BRANCH: LOCATION 3 OR LIFT', '#0055CC', 3)
make_marker('03-LOC3.png',        'MARKER 3 - ARRIVAL',         'LOCATION 3',                 '#CC4400', 4)
make_marker('04-LIFT_G.png',      'MARKER 4 - LIFT (GROUND)',   'GROUND FLOOR LIFT LOBBY',    '#8800CC', 5)
make_marker('05-LIFT_EXIT_1.png', 'MARKER 5 - LIFT EXIT F1',    '1ST FLOOR LIFT EXIT',        '#8800CC', 6)
make_marker('06-STAIRS_FOOT.png', 'MARKER 6 - STAIRS (FOOT)',   'FOOT OF STAIRCASE',          '#8800CC', 7)
make_marker('07-STAIRS_TOP.png',  'MARKER 7 - STAIRS (TOP)',    'TOP OF STAIRCASE',           '#8800CC', 8)
make_marker('08-F1_BRANCH.png',   'MARKER 8 - 1ST FL BRANCH',   'BRANCH: LOCATION 1 OR 2',    '#0055CC', 9)
make_marker('09-LOC1.png',        'MARKER 9 - ARRIVAL',         'LOCATION 1',                 '#CC4400', 10)
make_marker('10-LOC2.png',        'MARKER 10 - ARRIVAL',        'LOCATION 2',                 '#CC4400', 11)
make_marker('11-LIFT_EXIT_2.png', 'MARKER 11 - LIFT EXIT F2',   '2ND FLOOR LIFT EXIT',        '#8800CC', 12)
make_marker('12-LOC45.png',       'MARKER 12 - ARRIVAL',        'LOCATION 4 / LOCATION 5',    '#CC4400', 13)
make_marker('13-F2_CORR.png',     'MARKER 13 - 2ND FL CORRIDOR','TOWARD LOCATION 6',          '#00AA44', 14)
make_marker('14-LOC6.png',        'MARKER 14 - ARRIVAL',        'LOCATION 6',                 '#CC4400', 15)

print("\nAll 15 markers created. Upload to the MindAR compiler in numeric filename order (00 -> 14).")