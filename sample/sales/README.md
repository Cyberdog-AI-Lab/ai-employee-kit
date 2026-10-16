# 店舗売上の見渡し担当

4店舗・3か月の売上・返品を照合し、集計と確認事項を根拠付きで整理する社員です。

**このフォルダ自体が、KITで作成したAI社員です。** 設定・スキル・入力・成果物・ヒアリング記録がここで完結します。

**実際に作成したレポート：[HTML](outputs/20261016T081312Z-f54bb40cbcc1/report.html)・[JSON](outputs/20261016T081312Z-f54bb40cbcc1/report.json)**

| 内容 | このフォルダ内の正本 |
| --- | --- |
| 担当・共通ルール | [AGENTS.md](AGENTS.md) |
| Codexが発見する業務スキル | [work-001](.claude/skills/work-001/SKILL.md) |
| Claude Code向けの取り込み | [CLAUDE.md](CLAUDE.md) |
| ヒアリングと回答台帳 | [interview.md](interview.md) |
| 架空の入力原本 | [inputs/](inputs/) |
| 生成・定義の記録 | [records/definition.md](records/definition.md) |
| 成果物と設定・入力の対応 | [run-manifest.json](records/runs/20261016T081312Z-f54bb40cbcc1/run-manifest.json) |
| この成果物の独立照合 | [independent.json](records/verification/20261016T081312Z-f54bb40cbcc1/independent.json) |

入力は21ファイル。売上5,770行、返品72行とマスタ・注記。 定義版は `runtime-v001`（生成時の仕様0.1.4-draft／Q&A0.1.2-draft）。サンプルの配置形式は `sample-layout-v002` です。移動・同梱と社員定義の改訂を区別しています。

## コピーして使う

このフォルダ全体を、KITの外の新しいフォルダへコピーします。隠しフォルダと相対リンクも含めてください。KIT側の `scripts/prepare_sample_workspace.py sales <新しい保存先>` で、配置と全ファイルのハッシュを点検してコピーできます。コピー先をCodexの作業場所にした**新しい会話**で、次の仕事を依頼します。

```text
$work-001
このworkspaceの架空資料で、担当する仕事を試験してください。
input_dir=inputs、start_date=2026-07-01、end_date=2026-09-30。
inputsと定義は保持し、新しいoutputs/<run-id>/とrecords/runs/<run-id>/へ保存してください。
既存の成果物は読まず、入力から計算・整理し、根拠と確認待ち事項を報告してください。
```

`outputs/` はすでに実行した成果物、`records/runs/` は対応する実行記録です。新しい依頼では別のrunを作り、既存成果を置換しません。生成だけで成果物を作成済みにしたり、過去の許可を新しい仕事の許可にしたりしません。

`.agents/skills/work-001` は同じフォルダ内の `.claude/skills/work-001` への相対リンクです。`SKILL.md` の正本は1つで、両ツールから参照できます。KIT配下で仕事を始めるとKIT自身の指示も継承されるため、独立したコピー先から使います。

## 記録の読み方

この社員はAIが架空の担当者を演じた模擬回答から生成した試験例です。本人の回答確認・定義承認・人の検収は完了していません。入力原本とAGENTS/Skillは生成・試験時の内容を保持しています。公開した履歴と出力の一部では、個人のローカルパスだけを記号へ置き換えています。生成時のmanifestは当時の原本の記録、`bundle-manifest.json` は現在の配布ファイルの記録です。

静的配置の検査、Codexの認識、業務実行、独立照合、人の検収は別々の段階です。既存レポートの認識・実行証拠は上記run-manifestで追えます。Claude Codeでの業務遂行、実業務データでの精度、人による検収まで実証したものではありません。

今回の独立コピーでの [Codex認識・Skill選択の証拠](records/verification/20261016T081312Z-f54bb40cbcc1/recognition.json) を同梱しています。業務は入力から新規実行し、旧成果物を参照していません。配布用記録では個人のローカルパスだけを記号化し、原実行時と配布時のhashを分けています。

[Macブラウザでの表示確認](records/verification/20261016T081312Z-f54bb40cbcc1/browser.json)・[画面](records/verification/20261016T081312Z-f54bb40cbcc1/top.png) はCodexが操作・確認した証拠で、人の検収ではありません。
