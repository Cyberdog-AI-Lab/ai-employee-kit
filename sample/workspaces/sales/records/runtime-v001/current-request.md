# CURRENT-REQ-001 — 今回の生成回帰試験依頼

出所：現在の会話の実ユーザー依頼。受信日時の精密値は未取得。記録日時：2026-10-16T04:36:08.158150+00:00。下記は対象/許可/制限の要約であり、新しい模擬業務回答ではない。

- 対象：架空sales社員のみ。新しい生成版runtime-v001。現行のgenerate Skill・仕様0.1.4-draft・Q&A0.1.2-draft・テンプレートから新規生成する。
- K：KIT_ROOT
- 承認されたD：GENERATION_DRAFTS/sales
- 承認された新規試験W：GENERATED_WORKSPACES/sales
- 引継ぎ：TRIAL_RECORDS/generation-inputs/sales
- Dへの新規台帳/草稿/記録保存、Wへの正式構造の新規定義の試験配置、配置対象の形式修正、構造検査、入力hash保持と定義manifest/hash記録を許可。同じ許可は聞き直さない。
- 業務意味と出所、全42IDと必要パラメータを保持。通常confirmed・本人の承認/検収へ昇格しない。旧仕様・旧D/W・旧承認は過去資料。
- 書込みはD/Wだけ。K・旧D/W・現在inputsは変更しない。inputsはファイル名/形式/必要条件の確認に読める。
- Kのsample/substantial各例のoutput・processing-reference・validation・expected・provenance、他社員workspace、取りまとめの期待値・検査資料を読まない。
- 業務、HTML生成、処理スクリプト実装、会計更新、外部送信、実業務利用、別エージェント起動、ブラウザ操作を行わない。
- W/AGENTS.md、CLAUDE.mdと.claude正本/.agents相対リンクを作り、本文は外側フェンスなし。業務本文は相対参照で、依存資料/記録を同じW内に実在させる。
- 指定のPythonとKIT検査スクリプトで配置後検査し、JSONを保存。今回の許可対象内容はdefinition-manifest.jsonに具体化する。これは依頼範囲への適用記録であり、ユーザーがhashを個別に検収した記録ではない。

元依頼の理由（引用）：
> サンプルの中身がAGENTS.mdやSKILL.mdといったCodexが理解できる設定ファイルの形式でできてない。ちゃんとそこはKITにも反映して

今回の作業でK自体を変更する許可へ広げず、現行Kを読み新規定義を作る。設定自動認識/Skill選択/業務成功は未検証として引き継ぐ。
