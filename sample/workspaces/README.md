# 実行用のAI社員workspaceサンプル

**修正後の設定で生成した成果物を見る： [最新の売上・会議・請求入金レポート](../results/README.md)。**

現行KITの `ai-employee-generate` から、それぞれ独立した会話で新規生成した架空社員です。過去の説明用サンプルとは別に、実行に必要な配置を保って配布しています。このディレクトリには、実際に読み込める `AGENTS.md`、`CLAUDE.md`、`.claude/skills/<name>/SKILL.md`、`.agents/skills/<name>` の相対リンク、入力原本、必要資料、生成記録を同梱しています。模擬回答は人の確認済み回答ではありません。

| サンプル | 仕事 | 正式な設定 | 業務Skill | 実行時に渡す値 |
| --- | --- | --- | --- | --- |
| [sales](sales/) | 店舗売上・返品の照合と可視化 | [AGENTS](sales/AGENTS.md)・[Skill](sales/.claude/skills/work-001/SKILL.md) | work-001 | input_dir=inputs, start_date=2026-07-01, end_date=2026-09-30 |
| [minutes](minutes/) | 会議の決定・タスク・変更履歴の整理 | [AGENTS](minutes/AGENTS.md)・[Skill](minutes/.claude/skills/work-002/SKILL.md) | work-002 | input_dir=inputs, project_id=KOMOREBI-EVENT-2026, as_of=2026-10-15 |
| [reconciliation](reconciliation/) | 請求・銀行入金の照合と確認事項の整理 | [AGENTS](reconciliation/AGENTS.md)・[Skill](reconciliation/.claude/skills/work-001/SKILL.md) | work-001 | input_dir=inputs, dataset_id=AR-DEMO-2026, as_of=2026-10-15 |

## 新しい場所へ準備する

キットrootで、検査用Python環境（`scripts/requirements-validation.txt` のPyYAMLが必要）を使います。

```sh
python3 scripts/prepare_sample_workspace.py sales /path/outside-kit/sales-employee
```

`minutes`、`reconciliation` も同様です。保存先はまだ存在しないK外のディレクトリを指定します。スクリプトは内容hash、正式な配置、相対リンクを確認してコピーし、`workspace-copy-receipt.json` を作ります。業務を自動実行しません。隠しフォルダを除いて手動コピーするとSkillが認識されません。

コピー先をCodexの作業ディレクトリにし、**新しい会話**を開始してください。Kの下で業務を始めるとキット自身の指示が混ざる可能性があります。生成記録内の元のパス・承認・検査は当時の履歴です。現在の場所と当回の業務依頼は別に確認します。

まず、ツールでファイルを手動表示せず「現在適用されている担当・制約と利用可能な業務Skill」を尋ねます。Skillの一覧も確認し、次の別会話で実際の仕事を頼みます。例えばsalesでは以下を使えます。

```text
$work-001
このworkspaceの架空資料で売上照合・可視化を試験してください。
input_dir=inputs、start_date=2026-07-01、end_date=2026-09-30。
指定されたoutputs/とrecords/runs/へ新規保存し、必要ならscripts/に新規処理コードを置いてください。
入力原本・定義・既存成果を保持し、実行結果と確認待ち事項を報告してください。
```

他の2例も表のSkillと値を明示して、その仕事を依頼します。入力から結果を作り、既存の期待値や過去の成果を正解としてコピーしません。

## 検証の読み方

形式が合格すること、Codex本体がSkillを発見すること、会話開始時にAGENTSを読むこと、Skillを選択・読み込むこと、業務結果が正しいこと、人が検収することは別です。生成時の記録では後続試験を未検証としており、後からその記録を成功へ書き換えません。後続の試験証拠は別の検証記録として追加します。

本サンプルは架空資料による試験用です。実業務用の方針や承認を代替せず、人の検収は完了していません。Claudeとの共用ファイル構造は同梱していますが、この新しいサンプルでのClaude業務実行は別途検証が必要です。

今回の認識・業務試験・独立照合の結果と保存済みHTMLは [検証記録](../workspace-validation/README.md) を参照してください。
