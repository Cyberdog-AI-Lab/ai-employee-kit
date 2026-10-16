# KITで作成したAI社員

**各フォルダが1人分の完成したAI社員です。** フォルダを開くと、AGENTS.md、Codexが発見するスキル、架空入力、実際の成果物、ヒアリングと生成・実行記録を一緒に確認できます。

| AI社員 | 仕事 | 設定 | ヒアリング・成果物・使い方 |
| --- | --- | --- | --- |
| 店舗売上の見渡し担当 | 4店舗・3か月の売上と返品の照合 | [AGENTS](sales/AGENTS.md)・[Skill](sales/.claude/skills/work-001/SKILL.md) | [sales/](sales/README.md) |
| 会議引継ぎ担当 | 決定・変更・宿題と未解決事項の整理 | [AGENTS](minutes/AGENTS.md)・[Skill](minutes/.claude/skills/work-002/SKILL.md) | [minutes/](minutes/README.md) |
| 請求・入金照合担当 | 入金候補、未回収、確認事項の整理 | [AGENTS](reconciliation/AGENTS.md)・[Skill](reconciliation/.claude/skills/work-001/SKILL.md) | [reconciliation/](reconciliation/README.md) |

```text
sample/
├── sales/
├── minutes/
└── reconciliation/
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── .agents/skills/work-001/SKILL.md  ← 同じ社員内の正本を参照
    ├── .claude/skills/work-001/SKILL.md  ← スキルの正本
    ├── interview.md                    ← ヒアリング・回答台帳の索引
    ├── inputs/                         ← 架空の入力原本
    ├── outputs/<run-id>/               ← 実際に作成したレポート
    ├── records/                        ← 生成・実行・検証記録
    ├── sample.json                     ← 現行版と成果物の対応
    └── bundle-manifest.json            ← 配布内容のハッシュ
```

同じ構成を3社員に使います。`sample/<社員>/` 全体をKIT外へコピーし、そこを開いた新しいCodex会話で使います。各READMEに実行条件があります。隠しディレクトリを含むコピーと静的検査はKITの次のコマンドで行えます（Python 3.10+と `scripts/requirements-validation.txt` のPyYAMLが必要）。

```sh
python3 scripts/prepare_sample_workspace.py minutes /path/outside-kit/minutes-employee
```

保存先は新しいフォルダを指定してください。コピーだけでは仕事を実行しません。過去のヒアリング・許可は履歴であり、新しい依頼を代替しません。全例が模擬回答と架空入力による試験用で、人の検収は未実施です。

以前の説明用 `.sample.md`、小規模な商品紹介例、別階層の配布物・結果は現行ツリーから除き、[移行前のGit履歴](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/78d1c233cf23c09bd9c87b727e59e6b58d53c53f/sample)に残しています。現行の検証範囲は [検証記録](../docs/validation.md) を参照してください。
