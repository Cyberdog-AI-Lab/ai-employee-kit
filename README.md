# AI社員作成キット

**[KITで作った3人のAI社員と、実際に作成したレポート](sample/README.md)**

仕事を聞き取り、AIに任せる範囲・手順・確認方法をファイルに残すキットです。新人へ業務を引き継ぐように、目的、資料、迷ったときの対応、終わり方を一緒に整理します。売上集計専用ではなく、議事録整理や商品紹介など、異なる仕事を対象にできます。

**実験段階の公開版です。** 架空資料を使った試験記録を収録しています。専門的な支援なしで誰でも安全に使えること、実務全般での精度、全環境・両ツールでの動作を保証するものではありません。

## できること

- `ai-employee-interview`：少数ずつ質問し、既回答、提案、未決、矛盾を根拠付きの回答台帳にまとめる。
- `ai-employee-generate`：回答から非実行草稿を作り、配置条件と許可を確認して別の仕事用フォルダに社員定義を置く。
- 生成される `AGENTS.md`：担当範囲、原本の保持、人の確認、操作の境界を記す。
- 生成される業務Skill：具体的な手順、必要な入力、検査、停止・再開を記す。

キットの指示と完成する社員の指示は別物です。生成の依頼だけでは、社員の業務実行や外部送信まで許可したことにはなりません。

## はじめ方

```sh
git clone https://github.com/Cyberdog-AI-Lab/ai-employee-kit.git
cd ai-employee-kit
```

CodexまたはClaude Codeでこのフォルダを開き、まず次のように依頼します。使用するAIサービスの契約と、資料をAIに渡してよい範囲は利用者側で確認してください。

> AI社員に任せる仕事を一緒に整理してください。仕事は○○です。原本は変更せず、不明点は少数ずつ聞いてください。草稿はキットの外の○○フォルダへ保存してください。

明示的に呼ぶ場合、Codexでは `$ai-employee-interview`、Claude Codeでは `/ai-employee-interview` を使います。台帳から草稿を作るときは、それぞれ `$ai-employee-generate`、`/ai-employee-generate` です。

作業場所は次のように分けます。名称は例です。

```text
work/
├── ai-employee-kit/    キット K
├── employee-drafts/   台帳・非実行草稿 D
└── my-ai-employee/     完成する仕事用フォルダ W
```

1. 目的・入力資料・希望する成果物を伝える。未決でも台帳と非実行草稿を残せます。
2. 台帳の意味、未決、提案、操作の境界を確認する。草稿と配置可能な候補を区別します。
3. 対象の候補・保存先・操作を確認して配置を依頼する。K・D・Wは互いの配下に置きません。
4. Wを開いた新しい会話で、必要な実行条件を指定して仕事を依頼する。
5. 成果物、根拠、自己検査、不明点を人が確認する。改善は旧版と差分を残して再検証する。

## KITで作成したAI社員を試す

[sample/](sample/README.md) の [sales/](sample/sales/README.md)、[minutes/](sample/minutes/README.md)、[reconciliation/](sample/reconciliation/README.md) が、それぞれ1人分の完成した社員フォルダです。各フォルダに正式なAGENTS.md、Codexが発見する業務スキル、ヒアリング記録、架空入力、最新のHTML/JSON成果物、短い定義記録を揃えています。過去の草稿や実行・検証ログはGit履歴から参照できます。

社員フォルダ全体をKIT外へコピーし、そのフォルダを開いた新しいCodex会話で使います。各READMEからレポートを見られ、試験用の依頼例も確認できます。コピーは `scripts/prepare_sample_workspace.py`、配布物の整合確認は `scripts/verify_samples.py` を使用します。

全例はAIが模擬回答した架空資料の試験です。生成・認識・業務実行・独立照合・人の検収を分けた記録と、未検証事項は[検証記録](docs/validation.md)に示しています。以前の説明用サンプルはGit履歴で参照できます。

## セミナー用ダッシュボード

`python3 dashboard/serve.py` を実行し、**http://127.0.0.1:8765** を開くと、3社員の仕事内容・ヒアリング・AGENTS・Skill・入力・最新成果を切り替えて確認できます。ネット接続や追加パッケージは不要です。起動・投影・更新方法は [ダッシュボードの使い方](dashboard/README.md) を参照してください。

## 正本と構成

| 文書 | 役割 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | キット自身の共通指示 |
| [最終フォーマット仕様](formats/employee-format-spec.md) | 生成社員の42項目と固定規則 |
| [ヒアリングQ&A](docs/interview-qa.md) | 質問対応・空の回答台帳・引継ぎ契約 |
| [ヒアリングSkill](.claude/skills/ai-employee-interview/SKILL.md) | 少数ずつ聞き取る手順 |
| [生成Skill](.claude/skills/ai-employee-generate/SKILL.md) | 草稿・候補の生成と許可された配置 |
| [検証記録](docs/validation.md) | 実際に確認した範囲と未検証事項 |
| [両ツールの構成](docs/compatibility.md) | 正本、取り込み、相対リンク、コピー方式 |

Claude Code向けは `.claude/skills/`、Codex向けは `.agents/skills/` です。Skillの正本は前者に1つ置き、後者から相対リンクで参照します。`CLAUDE.md` は `@AGENTS.md` を取り込みます。リンクを使えない環境でのコピーと同期は[構成ガイド](docs/compatibility.md)を参照してください。

## 利用上の限界

指示ファイルはOSのアクセス制御ではありません。実際の権限・承認設定・AIサービスへ渡るデータを確認してください。原本保持、外部送信禁止などを記述しても、それだけで技術的に強制できるわけではありません。MCPなどの外部接続は必須ではなく、仕事に必要な場合に範囲を確認して追加します。

AIの自己検査と人の検収は別です。未確定値や矛盾を残した成果物を、そのまま実務上の確定情報として使わないでください。

## ライセンス

Apache License 2.0 — [LICENSE](LICENSE) を参照。帰属表示は [NOTICE](NOTICE) を参照。
Copyright 2026 Cyberdog AI Lab（株式会社サイバードッグ）。

本プロジェクトは "AS IS"（現状有姿）で提供され、いかなる種類の保証もありません。
