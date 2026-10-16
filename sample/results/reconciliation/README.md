# reconciliation — 正式な設定から再生成した最新成果物

[HTMLレポート](report.html) ／ [JSON](report.json)。請求100件のうち照合済み74・要確認19・未入金7。未回収1,244,110円。

修正後の正式な定義 `runtime-v001` を別workspaceで読み込み、新しいCodex会話でSkill `work-001` を選択して入力から生成しました。run: `recon-20261016T135525-c1aaefa7`。過去の小規模サンプルの成果物を流用していません。独立照合は合格、人の検収は未実施です。

- [使用したworkspaceと入力](../../workspaces/reconciliation/)、[AGENTS.md](../../workspaces/reconciliation/AGENTS.md)、[SKILL.md](../../workspaces/reconciliation/.claude/skills/work-001/SKILL.md)
- [実行記録](execution.json)、[入力・定義・出力の対応とハッシュ](run-manifest.json)
- [独立照合](../../workspace-validation/business/reconciliation/independent.json)、[検証の範囲](../../workspace-validation/README.md)

公開時にローカルパスだけを記号へ置き換えています。AGENTS本文・Skill本文・入力原本は実行時と同一です。過去の記録中のハッシュは原本を識別し、公開複製のハッシュはrun-manifest.jsonに別記しています。既に検証済みの同一成果物を、公開のためだけにAIで再実行してはいません。

自分で再実行する場合は [準備手順](../../workspaces/README.md) を使います。保存済み成果物は入力の正解として社員へ渡さず、別の新しいrunへ保存します。
