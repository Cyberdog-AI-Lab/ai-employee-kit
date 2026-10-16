# 議事録担当の試験記録（説明用）

**ここは過去の試験を読むための説明用資料です。** このフォルダをCodexで開いても、社員用のAGENTS.mdとSKILL.mdは自動認識されません。`definition/*.sample.md` は記録を読むための複製です。

**実際に動かす場合は [正式な会議workspace](../workspaces/minutes/) と [準備・実行手順](../workspaces/README.md) を使ってください。** 新しい例は8会議・140発言を扱う会議担当で、このページの小規模な試験とは入力・Skill・実行結果が別です。[新しい試験の結果](../workspace-validation/README.md)も確認できます。

キットrootで次を実行し、作成したキット外のフォルダを開いた新しいCodex会話から依頼します。Python 3.10以上と `scripts/requirements-validation.txt` の依存が必要です。保存先は未作成のフォルダを指定してください。

```sh
python3 scripts/prepare_sample_workspace.py minutes /path/outside-kit/minutes-employee
```

修正後の設定から生成した [最新HTML](../results/minutes/report.html) と [入力・定義・実行の対応](../results/minutes/README.md) を直接確認できます。

以下は以前の試験記録です。原本・定義の参照複製・期待値・成果物を保持しています。

[インタビュー](interview.md)で不明値や矛盾の扱いを聞き取り、キット外へ試験配置した社員を、新しいCodex会話で実行しました。架空の役割と資料を使う試験であり、人の候補レビュー・成果検収は未実施です。

## 読む順序

1. [インタビュー](interview.md)
2. [社員定義](definition/employee-agents.sample.md)・[業務手順](definition/work-0001.skill.sample.md)
3. [期待値](expected.json)とinput/の架空資料
4. [成果物Markdown](output/report.md)・[JSON](output/report.json)
5. [独立検証](validation/result.json)・[開始前の停止記録](validation/stop-record.json)

## 実行結果

資料IDが未指定の依頼では、入力からIDを補完せず、停止理由と再開条件を保存しました。その時点ではoutputsはありませんでした。ID回答後は停止記録を参照した新しいrunで処理し、旧記録と入力を保持しました。

会議IDと日付、決定と提案を区別しました。A01は担当を企画担当Aとし、競合する期限をnullに保ち、2026-10-20と2026-10-22の両候補をM03/M06へ結びました。A02の担当はnull、期限は2026-10-18です。次回会議日もnullのままです。

期待値との独立照合、根拠との対応、入力の前後ハッシュ、停止・再開の記録を確認しました。AIの自己検査済みと人の検収待ちは別の状態です。

## 参照資料としての制約

[provenance.json](provenance.json)で試験原本と公開用複製を区別しています。定義は非実行名で、ローカルパスは匿名化しました。このフォルダをそのまま稼働させず、インタビューと入力例をもとに自分の作業場所へ再生成してください。
