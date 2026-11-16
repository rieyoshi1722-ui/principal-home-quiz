# スタート用 A3ポスター

| ファイル | 中身 |
|---|---|
| `HOUSE_QUIZ_RALLY_A3_blank.pdf` | QRコードのところを白くあけたもの（本番用。QRは100mm角の白い四角の中に、82〜84mm角で入れる） |
| `HOUSE_QUIZ_RALLY_A3_with_qr.pdf` | スタートのQRコード（`https://pr-h.net/lp/22nd-anniversary/quiz/#go-7kx2`）を入れたもの。印刷して読めるか試す用 |
| `HOUSE_QUIZ_RALLY_A3_preview.jpg` | 画面で見る用の画像 |
| `HOUSE_QUIZ_RALLY_A3_with_qr_textimage.pdf` / `..._blank_textimage.pdf` | **文字をすべて画像にした**PDF（書体が入っていないので、Illustrator でも文字化けしません。文字は直せません） |
| `HOUSE_QUIZ_RALLY_A3_text_only.png` | 文字だけの、背景が透明な画像（A3・300dpi） |
| `LETS_GO_text.png` / `LETS_GO_text.svg` | 「LET'S GO!」の文字だけ（透明PNG・1200dpi、幅65.0mm×高さ7.14mm。SVGは図形なので書体不要）。ポスター上の位置は、左 114.84mm・上 276.99mm |

## 作り直し
- 元は `source/poster.html`（文字・位置・色はここ）。ゲームの画像は `test/assets/` を使っています。
- `cd source && node render_textimage.js ..` で、「文字を画像にしたPDF」2つと、文字だけの透明PNGを作り直せます。
- `cd source && node render.js ..` で、2つのPDF（文字が文字のまま）とプレビューを作り直せます（Playwright と Chromium が必要。`CHROMIUM_PATH` で Chromium の場所を指定）。
- 書体は Yusei Magic・DotGothic16・Press Start 2P（どれも SIL Open Font License）。`source/fonts/` に入っています。
- 「LET'S GO!」の文字は、Illustrator で書体がなくても開けるように、**図形（アウトライン）**にしてあります（Press Start 2P は PDF に入っていません）。ほかの文字は、Yusei Magic と DotGothic16 のままです。
