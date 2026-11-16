# スタート用 A3ポスター

| ファイル | 中身 |
|---|---|
| `HOUSE_QUIZ_RALLY_A3_blank.pdf` | QRコードのところを白くあけたもの（本番用。QRは100mm角の白い四角の中に、82〜84mm角で入れる） |
| `HOUSE_QUIZ_RALLY_A3_with_qr.pdf` | スタートのQRコード（`https://pr-h.net/lp/22nd-anniversary/quiz/#go-7kx2`）を入れたもの。印刷して読めるか試す用 |
| `HOUSE_QUIZ_RALLY_A3_preview.jpg` | 画面で見る用の画像 |

## 作り直し
- 元は `source/poster.html`（文字・位置・色はここ）。ゲームの画像は `test/assets/` を使っています。
- `cd source && node render.js ..` で、2つのPDFとプレビューを作り直せます（Playwright と Chromium が必要。`CHROMIUM_PATH` で Chromium の場所を指定）。
- 書体は Yusei Magic・DotGothic16・Press Start 2P（どれも SIL Open Font License）。`source/fonts/` に入っています。
