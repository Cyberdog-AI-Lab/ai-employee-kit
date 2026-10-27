# 検証範囲

## 最新サンプルの構成

[sampleの3社員](../sample/README.md) は、最新の設定・Skill・依存資料・ヒアリング・入力・成果物を各社員の直下にまとめています。`records/definition.md` は実行に必要な確認方法、`sample.json` は現在の定義hashと最新成果の実行時hash、`bundle-manifest.json` はコピー検査用です。

配布形式は `sample-layout-v003`。業務条件runtime-v001を継承し、保存先と参照資料を整理しました。入力37ファイルと最新成果7ファイルは整理前と同じbytesです。社員の再生成・業務の再実行・人の検収をしたとは扱いません。過去の草稿・実行・検証ログは [保存済みGit版](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/8ed9ba51a3bf66ab8f8a009e6fbc3551b23394c1) に残しています。

## この整理での確認

配置126件・コピー24件・配布回帰21件が合格し、配布整合134項目も合格しました。配布回帰はPython最適化モードでも21件合格。独立コピー3件で静的構造が通り、新規Codex app-serverのSkill探索で各社員の業務Skillを発見しました（探索エラー0、KIT生成Skillの混在なし）。現行Markdownの内部参照183件・アンカー14件と、Git保存版への参照13件を照合しています。

入力・成果物44ファイルの同一性、保存済み検証JSONのhash・件数、実行当時の定義hashを整理前のGit版と比較しました。今回のチェックでAI業務や画面確認をやり直したとは扱いません。

## 再現できる静的検査

Python 3.10以降と [PyYAML依存](../scripts/requirements-validation.txt) を使います。業務は開始しません。

```sh
python3 -I -B scripts/verify_samples.py
python3 -I -B scripts/test_employee_workspace.py
python3 -I -B scripts/test_prepare_sample_workspace.py
python3 -I -B scripts/test_samples.py
python3 -I -B scripts/prepare_sample_workspace.py minutes /path/outside-kit/minutes-employee
```

配置検査は126件、コピー回帰は24件です。配布検査は全ファイル・相対リンクとhash、現行Markdownのファイル参照、現在の定義・全Skill参照資料・入力・最新出力の対応を検査します。配布回帰は欠落・改変・範囲外参照・旧階層・誤った検収状態・実行当時の定義との不一致を検出します。Git履歴のURLは固定コミットと対象runの形を検査し、ネット取得はしません。

コピー先に必要な参照資料が揃うことと、AIによる再実行の結果は別です。実行する場合は各社員READMEのパラメータを明示した新しい依頼を使い、実環境・Skill発見・結果を確認します。AIの再実行で文章やHTMLのbytesが一致するとは限りません。

## 同梱成果の実行時点の検証

以下は整理前の実行実績です。現在の保存形式で再実行した件数ではありません。元の定義・run-manifest・独立照合・画面確認は [当時のsample](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/8ed9ba51a3bf66ab8f8a009e6fbc3551b23394c1/sample)、共通試験とClaude Codeのレビューは [当時の検証資料](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/8ed9ba51a3bf66ab8f8a009e6fbc3551b23394c1/docs/validation) にあります。各sample.jsonから社員別の固定記録へ直接辿れます。

| 社員 | 対象 | 当時の独立照合 |
| --- | --- | --- |
| sales | 21入力、売上5,770行・返品72行 | 35,984件合格 |
| minutes | 10入力、8会議・140発言 | 927件合格 |
| reconciliation | 6入力、請求100件・入金90件 | 4,540件合格 |

3件はKIT外の独立コピーで別々のCodex会話から実行しました。入力・根拠・全件処理・数値・形式間の対応を、社員の処理コードを使わず照合しました。CodexがユーザーのMacのOrcaブラウザで初期表示とグラフを確認しました。いずれもAIによる確認で、人の検収ではありません。

## 未検証の範囲

全て模擬回答と架空入力の試験です。本人confirmed、実業務の採用、実業務データの精度、全環境・全画面操作・印刷・モバイルの動作は確認していません。Claude Codeによる社員業務と、Codex DesktopのSkill選択UIも未検証です。指示ファイルはOSのアクセス制御を保証しません。
