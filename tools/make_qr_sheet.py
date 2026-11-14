"""Make the A4 sheet of the 11 QR codes (start, QUIZ 2-5, six ハズレ) as an HTML page ready to print to PDF.

usage: python3 tools/make_qr_sheet.py <base url ending in /> <output.html> [font folder with notojp400.ttf / notojp700.ttf]
Each QR holds <base url>#<code>. Needs: pip install "qrcode[pil]"
"""
import base64, io, os, sys
import qrcode

base, out = sys.argv[1], sys.argv[2]
fonts = sys.argv[3] if len(sys.argv) > 3 else ''
ITEMS = [("スタート", "QUIZ 1 はスタートのあとに出ます", "go-7kx2"),
         ("Q2", "QUIZ 2", "q2-m4p9"), ("Q3", "QUIZ 3", "q3-t8w3"),
         ("Q4", "QUIZ 4", "q4-c5n7"), ("Q5", "QUIZ 5", "q5-h2v6")]
ITEMS += [("ハズレ %d" % (i + 1), "ちがうところを探してね", c)
          for i, c in enumerate(["x1-r9d3", "x2-k4m8", "x3-w7q2", "x4-b6t5", "x5-n3z9", "x6-d8c4"])]
cells = []
for label, sub, code in ITEMS:
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=4)
    q.add_data(base + '#' + code); q.make(fit=True)
    buf = io.BytesIO(); q.make_image(fill_color="black", back_color="white").convert("RGB").save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    cells.append('<div class="cell"><p class="lb">%s</p><img src="data:image/png;base64,%s"><p class="sub">%s</p></div>' % (label, b64, sub))
face = ''
if fonts:
    face = ('@font-face{font-family:NJ;src:url(file://%s/notojp400.ttf);font-weight:400}'
            '@font-face{font-family:NJ;src:url(file://%s/notojp700.ttf);font-weight:700}' % (fonts, fonts))
html = '''<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
%s
@page{size:A4;margin:12mm}
*{box-sizing:border-box}
body{font-family:NJ,"Noto Sans JP","Hiragino Sans",sans-serif;color:#22242c;margin:0}
h1{font-size:14pt;margin:0 0 2px;color:#1F3A6E}
.lead{font-size:8pt;color:#5b6070;margin:0 0 4mm;line-height:1.45}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
.cell{border:1px dashed #9aa3b8;border-radius:3mm;padding:2mm;text-align:center;break-inside:avoid}
.lb{font-size:11pt;font-weight:700;margin:0;color:#1F3A6E}
.cell img{width:42mm;height:42mm;display:block;margin:1mm auto 0;image-rendering:pixelated}
.sub{font-size:7pt;color:#7a8090;margin:.5mm 0 0}
</style></head><body>
<h1>HOUSE QUIZ RALLY　QRコード（全11枚）</h1>
<p class="lead">読みこむURL：%s<br>スマホのカメラで「スタート」から順番に読みとってください（LINEなどのアプリでは続きから遊べません）。ハズレは6枚とも同じ画面が出ます。</p>
<div class="grid">%s</div>
</body></html>''' % (face, base, "".join(cells))
open(out, 'w', encoding='utf-8').write(html)
print('wrote', out)
