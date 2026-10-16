# 入力構造と参照

版：runtime-v001。現在の入力実体からファイル名/ヘッダーを観察した記録であり、業務回答の本人確認ではない。業務判断の根拠はsales模擬回答と判断規則に置く。入力の版/hashは [入力観察](../../../../records/runtime-v001/input-structure.json) と [配置前hash](../../../../records/runtime-v001/input-before.json) を参照し、業務開始時に再取得する。

CSVはUTF-8のヘッダー付きファイル。販売日・返品日・価格有効日はISO暦日、ID/名称/channel/reasonは文字列として原値を保持する。販売数量・単価・割引は非負整数、金額は整数円。返品数量・返金額は元売上との数量/金額照合に用い、原記録を保持する。構造や重要な値の扱いが定義できなければ停止・確認し、架空の補完をしない。

| 入力（この参照資料からの相対リンク） | 必要列 |
| --- | --- |
| [inputs/master/price_history.csv](../../../../inputs/master/price_history.csv) | `sku,effective_from,unit_price_jpy` |
| [inputs/master/product_aliases.csv](../../../../inputs/master/product_aliases.csv) | `product_label,sku` |
| [inputs/master/products.csv](../../../../inputs/master/products.csv) | `sku,canonical_name,category` |
| [inputs/master/store_aliases.csv](../../../../inputs/master/store_aliases.csv) | `store_label,store_id` |
| [inputs/master/stores.csv](../../../../inputs/master/stores.csv) | `store_id,canonical_name` |
| [inputs/returns/returns.csv](../../../../inputs/returns/returns.csv) | `return_id,original_transaction_id,return_date,quantity,refund_jpy,reason` |
| [inputs/sales/2026-07-S01.csv](../../../../inputs/sales/2026-07-S01.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-07-S02.csv](../../../../inputs/sales/2026-07-S02.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-07-S03.csv](../../../../inputs/sales/2026-07-S03.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-07-S04.csv](../../../../inputs/sales/2026-07-S04.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-08-S01.csv](../../../../inputs/sales/2026-08-S01.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-08-S02.csv](../../../../inputs/sales/2026-08-S02.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-08-S03.csv](../../../../inputs/sales/2026-08-S03.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-08-S04.csv](../../../../inputs/sales/2026-08-S04.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-09-S01.csv](../../../../inputs/sales/2026-09-S01.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-09-S02.csv](../../../../inputs/sales/2026-09-S02.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-09-S03.csv](../../../../inputs/sales/2026-09-S03.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |
| [inputs/sales/2026-09-S04.csv](../../../../inputs/sales/2026-09-S04.csv) | `transaction_id,date,store_label,product_label,quantity,unit_price_jpy,discount_jpy,channel` |

商品マスタはsku/canonical_name/category、店舗マスタはstore_id/canonical_name。別名表はproduct_label→sku、store_label→store_idの明示対応。価格履歴はsku/effective_from/unit_price_jpyで販売時の比較基準を定める。カテゴリは商品マスタに従う。

補助資料：[入力README](../../../../inputs/README.md)、[入力manifest](../../../../inputs/manifest.json)、[店舗メモ](../../../../inputs/notes/2026-09-store-notes.md)。manifestの件数やfixture_revisionは入力作成者の記載であり、業務の正解値ではない。店舗メモは事情の併記と根拠参照用で、照合規則や権限の代わりにしない。現在の期間やファイル数を毎回のパラメータの既定値にしない。
