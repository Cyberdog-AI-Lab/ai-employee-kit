# 検証記録

## 2026-10-16：各sampleを1人分の社員へ統合

`sample/sales/`・`sample/minutes/`・`sample/reconciliation/` 自体に、正式な設定、スキル、入力、ヒアリング記録、実際の成果物、生成・実行・検証記録を揃えました。[社員一覧](../sample/README.md)から各社員を開けます。別階層のworkspaces/results、説明用の旧 `.sample.md`、小規模な旧商品例は現行ツリーから整理しました。

社員定義は `runtime-v001`（生成仕様0.1.4-draft／Q&A0.1.2-draft）のままです。KITの仕様0.1.5-draft／Q&A0.1.3-draftはサンプル収録形式の契約を追加した版です。配置形式 `sample-layout-v002` への整理を、社員を再生成した実績として扱いません。

### この修正での検証

- 配置検査126件、コピー検査24件、配布物の回帰15件が合格。
- コピー検査は、隠し設定・相対リンク・入力の保持、既存保存先への拒否、旧階層へのフォールバック拒否を含みます。
- 配布回帰は、社員全体の独立コピー、設定・ヒアリング欠落、別フォルダへの参照、入力・出力・定義の改変、偽の検収状態、旧階層を検出します。
- コピーと配布回帰は通常実行・Python最適化モードの両方で合格。チェックは `assert` の有効性に依存しません。
- 独立コピー3件でCodex CLI 0.159.2の初期コンテキストを確認。手動ファイル表示やツール操作なしで、各担当・制約・業務Skillを識別しました。
- 新規Codex app-serverの `skills/list` で3社員のスキルを発見。探索エラー0件で、KITの生成Skillは混在しませんでした。
- 統合配置の独立コピー3件から新規業務を実行し、全て終了コード0で完了。固定した独立期待値と原本による照合も全て合格し、その新しいレポートを各社員に同梱しました。

初期試験ではOrcaアカウント設定の旧 `features.rmcp_client` キーを無視する警告がありました。3試験とも終了コード0で完了し、社員の読込み・スキル探索に失敗していません。アカウント設定自体は変更していません。

### 再現できる静的検査

Python 3.10以降と [PyYAML依存](../scripts/requirements-validation.txt) を使います。下記は保存済みファイルと構成の検査で、AI業務は再実行しません。

```sh
python3 -I -B scripts/verify_samples.py
python3 -I -B scripts/test_employee_workspace.py
python3 -I -B scripts/test_prepare_sample_workspace.py
python3 -I -B scripts/test_samples.py
```

配布検査は全ファイル・相対リンクとbundle hash、現行Markdownのファイル参照先、設定・Skill配下の補助資料・入力・出力・独立照合記録の対応を確認します。業務数値の再計算、外部リンク取得、Markdown全構文・全アンカー、Codex UI、人の検収は対象外です。生成時の本文アーカイブは `.txt` で当時の内容を保持し、現在の設定やナビゲーションと区別します。

## 同梱する今回の成果物の検証実績

同梱レポートは正式なAGENTS/Skillから別々のCodex会話で生成・実行した結果です。各社員の `sample.json` と `records/runs/<run-id>/run-manifest.json` が、使用した定義・入力・出力のhashを結びます。生成記録にある当時の未検証状態は書き換えていません。

| 社員 | 対象入力 | 独立照合 |
| --- | --- | --- |
| [sales](../sample/sales/README.md) | 21ファイル、売上5,770行、返品72行 | 35,984チェック合格 |
| [minutes](../sample/minutes/README.md) | 10ファイル、8会議・140発言 | 927チェック合格 |
| [reconciliation](../sample/reconciliation/README.md) | 6ファイル、請求100件・入金90件 | 4,540チェック合格 |

固定した架空入力を、社員の処理コードを使わない独立検査で照合しました。原本・設定の保持、全件の処理状況、引用、数値、未確定・矛盾、HTML/JSONの対応を含みます。CodexがユーザーのMacのOrcaブラウザを操作し、各レポートの初期表示と描画されたグラフを確認しました。スクリーンショットもCodexが読み取り、人の検収とはしていません。GUI表示と数値の独立照合は別の証拠です。

独立照合は各社員の `records/verification/<run-id>/independent.json`、画面は同じ場所の `top.png` にあります。前回公開時の共通試験は [前回の試験概要](validation/previous-native-publication/trial-summary.json) と [公開内容の検査](validation/previous-native-publication/publication-verification.json) に履歴として残しています。古いパスは当時の配置を示し、現在の導線は各社員READMEです。

## 履歴と未検証範囲

統合前の公開内容は [移行前のコミット](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/78d1c233cf23c09bd9c87b727e59e6b58d53c53f) から回復できます。初期の小規模試験、失敗と修正、旧説明用サンプルもGit履歴に残っています。未コミット資料は公開ツリーの外へ内容hashを照合した退避コピーを保持しました。

全て架空資料の試験です。模擬回答は本人confirmedではなく、AIレビュー・独立検査も人の検収ではありません。Codex DesktopのSkill選択UI、Claude Codeによる社員業務、実業務データでの精度、全画面操作・印刷・モバイル、人の成果検収は未実施です。

## レビューと修正

Codexが構造修正と試験を担当し、Claude Codeが通常のKITソースを読み取り専用でレビューしました。指摘を受けて、Skillの参照資料も実行時の定義hashへ含め、独立照合JSONもrun-manifestのhashで固定しました。売上のヒアリング原記録4点を社員内へ同梱し、READMEのSkillリンクはGitHub上でも辿れる正本のパスへ統一しました。旧試験用の未追跡スクリプト2本は内容を検証した外部退避へ移しました。

今回の独立照合の初回には、SVGを直接記述したHTMLだけを受け入れる検査が、JavaScriptで描画するSVGとCSSの棒グラフを不合格にしました。数値・原本・根拠の照合は通っており、社員の成果物は変更せず検査対象の表現形式を修正しました。保存した最終検査とMacの実表示で確認しています。失敗した検査記録は外部の試験履歴に保持しました。

[修正後の共通検査](validation/consolidated/checks.json) と [レビュー指摘への対応](validation/consolidated/review-adjudication.json) を参照してください。認識と業務の証拠は各社員の現行runの記録を正本とします。
