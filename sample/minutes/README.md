# 会議引継ぎ担当

架空のこもれび商店の企画責任者へ、体験販売会の現行決定、正式変更、判断待ち、担当別の宿題を根拠付きで引き継ぐ。

- 設定：[AGENTS](AGENTS.md)・[Skill](.claude/skills/work-002/SKILL.md)・[現行ヒアリング](interview.md)
- 入力：[架空原本](inputs/README.md)
- 最新成果：[HTML](outputs/20261016T081240Z-b20b49b029d5/report.html)・[JSON](outputs/20261016T081240Z-b20b49b029d5/report.json)・[MD](outputs/20261016T081240Z-b20b49b029d5/report.md)（人の検収前）
- 版とhash：[sample.json](sample.json)・[定義記録](records/definition.md)

## 使い方

隠しフォルダと相対リンクを含むこの社員フォルダ全体をKIT外へコピーし、コピー先を開いた新しいCodex会話で依頼します。KIT側で `python3 scripts/prepare_sample_workspace.py minutes /path/outside-kit/minutes-employee` を使えます。Python 3.10+とPyYAMLが必要です。

```text
$work-002
input_dir: inputs
project_id: KOMOREBI-EVENT-2026
as_of: 2026-10-15
架空入力から指定のレポートを作成してください。原本・既存成果は変更せず、新しいrunへ保存し、不明点と自己検査結果を示してください。
```

Claude Codeで明示選択する場合は `/work-002`。Claude Codeでのこの社員の業務実行は未検証です。必要なローカル処理コードは新しい実行の中で作成するため、固定の業務スクリプトへの依存はありません。実行・停止記録は必要時にrecords/runsへ新規保存します。

同梱成果は整理前の定義で実行した最新runです。今回の整理では再実行せず、入力と出力を同じbytesで保持しています。AIの再実行でHTMLや文章の完全一致を保証するものではありません。過去の草稿・実行ログ・検証記録は [Gitの保存済み版](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/8ed9ba51a3bf66ab8f8a009e6fbc3551b23394c1/sample/minutes/records) にあります。
