# 出所・試験許可・履歴 runtime-v001

記録者：Codex生成担当。記録日時：2026-10-16T13:36:24+09:00。現在のユーザー発言の正確な時刻は未取得。この時刻を承認時刻としない。

<a id="u-runtime-001"></a>
## U-RUNTIME-001 / TEST-PERMIT-RUNTIME-001

[現在のユーザー依頼原文](definition-history/runtime-v001/source-archive/current-user-request.txt)が今回の操作許可の根拠。runtime-v001を現行KITから新規生成し、承認されたDへ保存、指定新Wへ正式構造で試験配置する。配置対象の形式修正も同じ依頼の範囲。対象本文・依存入力・相対リンクの識別子は[generation manifest](generation-manifest.runtime-v001.json)に結ぶ。ユーザーが個々のhashを事前レビューしたとは記録しない。

| root | 今回の実パス |
| --- | --- |
| K（読取のみ） | `KIT_ROOT` |
| 承認D | `GENERATION_DRAFTS/reconciliation` |
| 今回の束 | `GENERATION_DRAFTS/reconciliation/runtime-v001` |
| 新規試験W | `GENERATED_WORKSPACES/reconciliation` |
| 引継ぎ入力 | `TRIAL_RECORDS/generation-inputs/reconciliation` |

K/D/Wの実パス相互分離・祖先/アカウント指示・登録設定・既存内容は[環境観察](environment-observation.runtime-v001.json)。D保存とW新規配置の許可を業務・HTML生成・スクリプト実装・会計更新へ広げない。入力の置換、旧成果置換、外部送信、実業務利用、別エージェント起動、ブラウザ操作、他作業への操作は含まない。

## 模擬回答と旧版

- [質問履歴v001の原bytes](definition-history/runtime-v001/source-archive/interview-history.v001.md.txt)：U01-A〜E、H01-Q01〜03。元シナリオ作成者は特定できない。
- [模擬回答履歴v002の原bytes](definition-history/runtime-v001/source-archive/interview-history.v002.md.txt)：U02-Q01/Q02/Q03/COMMON/PERMIT。回答者は取りまとめCodexが演じる架空経理担当。旧記録時刻2026-10-16T00:28:46+09:00、発言時刻未取得。
- [旧台帳v001](definition-history/runtime-v001/source-archive/answers.v001.md.txt)と[旧台帳v002](definition-history/runtime-v001/source-archive/answers.v002.md.txt)もbytesを保持。原ファイルとSHA-256対応は[source identifiers](source-identifiers.runtime-v001.json)。旧台帳の値が省略表示されている箇所は、過去生成物を読まず、U02の全文・現在の仕様/テンプレート・実入力の採用ルールから新規に展開した。
- 旧記録の `K` / `D-reconciliation` / `W-reconciliation` は旧資料中の表記。旧実パスは引継ぎ資料から取得できないため創作しない。旧仕様0.1.3-draft、旧Q&A0.1.1-draft、旧trial-v001、TEST-PERMIT-01/02は歴史資料であり、今回の版・場所の許可や認識/業務成功の根拠に流用しない。
- 原bytes資料は `.txt` で保存した参照アーカイブであり、社員設定や現在の手順ではない。内部の旧リンク/未解決表記は過去資料として保持し、現在の定義の依存先にしない。現在の業務条件・リンクは新しい台帳/本文に完結させる。

## 意味内容の引継ぎ

全業務意味はproposedのまま。SKL-001は形式規則fixed-default、FIX9は現行仕様fixed-default、SKL-012は任意unanswered。通常confirmedは0件。GENの観察、実際のユーザーの試験操作許可、人による定義承認/検収を別記する。試験内定義条件は充足と判定するが、通常の仕様7章の必須確定条件を満たしたとはしない。

U01の月次はU02の毎日の目的へ更新された履歴を保持。U02の「期日後の入金」という略記は、旧履歴がすでに説明する採用ルールR01/R08のposted_on > as_ofに対応させ、due_onによる入金除外を追加しない。fixture_revision=v3とルール表題v1の違いを保持。EMP-003/011の試験窓口・保守への接続はCodex整理案のまま、人の承認権限をAIへ付与しない。

## 読取と生成の範囲

実際にai-employee-generate Skill、キットAGENTS、仕様、Q&A、両テンプレートを読み、テンプレートの内側本文へ新しいEMP/SKL値を展開した。FIXは現行仕様原文から収録。旧生成物の改名や転用ではない。入力は6ファイルのhash/manifest/CSVヘッダーとREADME/ルール全文の定義確認まで。請求・入金の照合業務は実施していない。

Kの禁止されたサンプル成果/検査資料、他の社員workspace、取りまとめ期待値を読まず、Kと旧D/Wに書き込んでいない。外部判定サービスはユーザーの外部送信許可範囲外のため使用せず、ローカル静的検査と原文照合を行う。
