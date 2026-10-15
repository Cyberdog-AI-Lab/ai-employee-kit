# 商品紹介原稿（架空資料・社内レビュー用）

状態：自己検査済み・検収待ち

- run_id：run-20261015T104236-52241244
- 資料ID：CATALOG-001
- 入力：inputs/products-fictional.json
- 入力SHA-256：3f541c3aaeb86e784067f3077304456a0cd08bfe485a5612e1d34efdb014a2c4
- 手順：work-0001 / 0.1.0-trial
- 手順SHA-256：f3824f00d42f3d4361eee16ba3b9415fbd50d7dd9f7c9968c88b1677b1ae5507
- 検収役：架空の店舗の企画担当
- 人の検収：未実施（human_acceptance: false）
- 本番利用不可。公開可否は判断していない。

## P001 — 架空ブレンド茶

| 項目 | 値 | 入力根拠（JSON Pointer） |
| --- | --- | --- |
| SKU | P001 | /products/0/sku |
| 名前 | 架空ブレンド茶 | /products/0/name |
| 価格 | 800円 | /products/0/price_jpy |
| 内容量・仕様 | ティーバッグ5包 | /products/0/content |
| 仕様・特徴 | 焙煎した穀物をブレンド | /products/0/features/0 |
| 仕様・特徴 | 個包装 | /products/0/features/1 |

### 紹介文

ティーバッグ5包で、焙煎した穀物をブレンドしています。個包装です。

### 各主張の根拠

| 主張 | 入力根拠（JSON Pointer） |
| --- | --- |
| ティーバッグ5包で、焙煎した穀物をブレンドしています。 | /products/0/content, /products/0/features/0 |
| 個包装です。 | /products/0/features/1 |

### 不明点・要確認

- 原材料の詳細（未確認。根拠：/products/0/unknowns/0）
- アレルゲン情報（未確認。根拠：/products/0/unknowns/1）

## P002 — 架空陶器マグ

| 項目 | 値 | 入力根拠（JSON Pointer） |
| --- | --- | --- |
| SKU | P002 | /products/1/sku |
| 名前 | 架空陶器マグ | /products/1/name |
| 価格 | 価格未定・要確認 | /products/1/price_jpy |
| 内容量・仕様 | 容量250ml | /products/1/content |
| 仕様・特徴 | 手作業による釉薬仕上げ | /products/1/features/0 |
| 仕様・特徴 | 1点ずつ色合いが異なる | /products/1/features/1 |

### 紹介文

容量250mlで、手作業による釉薬仕上げです。1点ずつ色合いが異なります。

### 各主張の根拠

| 主張 | 入力根拠（JSON Pointer） |
| --- | --- |
| 容量250mlで、手作業による釉薬仕上げです。 | /products/1/content, /products/1/features/0 |
| 1点ずつ色合いが異なります。 | /products/1/features/1 |

### 不明点・要確認

- 価格未定・要確認（price_jpy: null。根拠：/products/1/price_jpy）
- 価格（未確認。根拠：/products/1/unknowns/0）
- 電子レンジ対応（未確認。根拠：/products/1/unknowns/1）
- 食洗機対応（未確認。根拠：/products/1/unknowns/2）

## 自己検査

以下は保存済みの原稿データとMarkdownを入力に照合したAI自己検査。人の検収ではない。

| 検査 | 結果 | 確認内容 |
| --- | --- | --- |
| 入力形式・資料ID | pass | UTF-8 JSON、資料ID一致、fictional:true、必須項目・価格型・文字列配列を確認。 |
| 全商品網羅・SKU一意 | pass | 入力2商品、出力2商品。入力順・SKUを照合し除外なし。 |
| 原値・不明点保持 | pass | SKUのキー名と値、name/content/price&#95;jpy/features/unknownsを原入力と型も含めて照合。 |
| 未確定値の表示 | pass | null価格は未定として表示し、unknownsとともに保持。価格や対応可否の推測なし。 |
| 各主張の根拠対応 | pass | 4文すべてに実在する同一商品のcontent/features参照があり、表示項目も原フィールドへ対応。 |
| 入力外主張の不在（AI本文照合） | pass | AIが入力全商品のcontent/featuresと各文を照合。内容量・既知の特徴の言い換えのみで、入力外の効能、安全性、人気、在庫、配送日、評価表現がないことを確認。 |
| Markdown/JSONの意味一致 | pass | 保存済みMarkdownの見出し・表・紹介文・根拠・不明点を独立に抽出し、再読込JSONと原入力に照合。 |
| 入力SHA-256 | pass | 配置時copy&#95;sha256・開始時・検査時のW内入力SHA-256が一致。外部原本は参照していない。 |
| 既存記録・手順の保持 | pass | AGENTS・正本Skill・定義/配置記録・前回停止記録の前後SHA-256が一致。 |
| 人の検収との分離 | pass | 人の検収は未実施。AI自己検査を検収済みに扱っていない。 |

自己検査記録：../../records/run-20261015T104236-52241244/validation.json
最終保存後の再読込・入力終了SHA・出力SHA：../../records/run-20261015T104236-52241244/finish.json

## 引継ぎ

上記の価格未定・unknownsを保持して、架空の店舗の企画担当の検収を待つ。
掲載・外部送信・公開用の確定は行っていない。入力外の確認や人による検収は未実施。
