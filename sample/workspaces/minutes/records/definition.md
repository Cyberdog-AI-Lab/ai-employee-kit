# minutes 定義記録 — runtime-v001

状態：試験配置済み・静的構造検査合格。通常の本人承認・本番利用・業務成功を意味しない。
生成日時（固定）：2026-10-16T04:36:33.497182+00:00。仕事は会議引継ぎ担当、skill_key=showcase-minutes-002、slug=work-002。
模擬回答の通常confirmedは0。通常の配置条件を満たした定義・実業務用・人の検収済みとは扱わない。

<a id="gen-001"></a>
## GEN-001 保存先・継承

現在の実パス、D/W既存内容、Kとの相互分離、祖先/アカウント指示、D発見先外の確認は [preflight](runtime-v001/preflight.json)。作業cwdはKのままで社員業務を起動していない。新Wをcwdとする新規会話での実際の自動認識は別試験。

<a id="gen-002"></a>
## GEN-002 生成元と固定版

仕様0.1.4-draft、Q&A0.1.2-draft、AGENTS/Skillテンプレート0.1.4-draft、生成Skill ai-employee-generateを実ファイルから使用。[生成元manifest](runtime-v001/source-manifest.json) と同梱sourcesにSHA-256・原文を保持。HEADは履歴参照で、未コミット変更のある現行内容の同一性を表さない。
本文と判断に影響する入力契約、接続の識別は [定義manifest](runtime-v001/definition-manifest.json)。定義digest：`69181c7387289d1fc3693ab0f0d26baec073721d8d7c543c371dba9f6324011e`。動的な回答/承認/配置/環境/検査記録をこのdigestへ循環して含めない。

<a id="gen-003"></a>
## GEN-003 全項目・子要素・派生値

[回答台帳](runtime-v001/answers.md)・[全42IDの値/根拠/状態](runtime-v001/answers.json)・[出力対応](runtime-v001/output-map.json)・[3パラメータ子要素](runtime-v001/parameter-definitions.json)。共通EMP13/FIX9/GEN7とwork-002のSKL13を対応。SKL-012は任意unansweredで本文省略、記録に対応。意味回答と形式導出と環境観察を分ける。

<a id="gen-004"></a>
## GEN-004 試験許可と人の役割

依頼/成果検収/定義変更確認/保守は架空の企画責任者というproposedの役割設定。[REQ-RUNTIME-001](runtime-v001/current-request.record.md) は現在のユーザーによるruntime-v001の新規生成、指定D保存、新W試験配置、形式修正と構造検査の許可。具体的な対象は上記定義manifestと出力対応。本人の意味回答confirmed・定義検収・成果検収にしない。業務開始、原本変更、既存成果置換、実業務利用、外部送信を許可しない。送信時刻は未取得、記録時刻と区別する。

<a id="gen-005"></a>
## GEN-005 実環境

生成担当：Codex、記録時刻はpreflightを参照。方法：現在の会話環境、実パス/ファイル属性/指示ファイル観察。現在はworkspace-write、network restricted、approval never。旧台帳のdanger-full-access/network有効は過去環境で適用しない。
業務環境・実権限・接続先・ツール読込み：未点検。生成時のD/W新規書込みが成功しても、社員業務の実行権限やアクセス制御の証明にはしない。業務開始担当が新しい会話で対象/日時/操作/確認方法/結果をrun記録へ残し、必要操作の確認前に開始しない。

<a id="gen-006"></a>
## GEN-006 旧版・現行・新案

[移行・比較記録](runtime-v001/migration.record.md)。旧台帳/質問をhash付きで保全。旧trial-v001の本文未取得で三者本文比較は不能。現在の新Wはinputsのみで置換対象なし。現行KITからの新規生成で、旧W/Dや手修正を上書きしない。今回の本文基準版はrecords/definition-history/runtime-v001に非実行名で保存する。

<a id="gen-007"></a>
## GEN-007 両対応の接続

AGENTS.md正本、CLAUDE.mdの `@AGENTS.md`、`.claude/skills/work-002/SKILL.md` 正本、`.agents/skills/work-002` → `../../.claude/skills/work-002` の相対symlinkを使う。保守担当は企画責任者役。コピー方式ではない。同じW内の正本への解決、内容一致、YAML、依存リンクを配置後に検査する。構造点検はCodex/Claudeでの発見・読込みの実証とは別。

<a id="deployment"></a>
## 配置記録

2026-10-16T04:45:57.568246+00:00、生成担当Codexが指定のverify_employee_workspace.pyを /opt/homebrew/bin/python3 で実行。終了コード0、all_passed=true、errors=[]。
[検査JSON](runtime-v001/workspace-verification.json)、[追加検査](runtime-v001/postdeployment-checks.json)、[配置結果](runtime-v001/deployment-receipt.json)、[入力before](runtime-v001/input-hashes.before.json)・[after](runtime-v001/input-hashes.after.json)を参照する。
入力10ファイルの一覧/hash一致、GEN-007、42ID、3パラメータ、FIX9、本文未展開記号なし、依存参照解決、定義manifest一致を静的に確認した。全入力の業務上の正しさを検証したものではない。
配置前の検査では台帳要約の相対リンク1件を修正した。元記録を保全し、[再検査](runtime-v001/predeployment-static-v002.json)で合格。業務本文・定義hashの変更なし。
設定の自動認識、Skill選択、業務実行、HTML/業務コード作成、独立レビュー、人の検収は未検証/未実施。別の新規会話・正しいcwdで続ける。業務意味の追加未決は検出していない。任意SKL-012と旧本文の比較不能は台帳に保持。
