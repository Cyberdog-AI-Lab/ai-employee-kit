# 店舗売上の見渡し担当 — 定義記録

生成版：runtime-v001。仕様：ai-employee-format 0.1.4-draft。Q&A：0.1.2-draft。両テンプレートの参照仕様：0.1.4-draft。生成日時（固定）：2026-10-16T04:36:08.158150+00:00。

案件employee-showcase-sales、仕事showcase-sales-001、slug/name work-001。意味回答の通常confirmedは0。必須意味回答はproposed、slugだけfixed-default、追加例SKL-012は任意unanswered。架空資料に限る試験例外として扱い、通常配置条件充足・本番利用・人の定義承認・検収へ昇格しない。

状態の正本はこの記録と配置/検査receipt。AGENTS/Skillの固定生成日時や本文は状態更新で書き換えない。配置の依頼は業務開始を含まない。別の明示的な試験業務依頼があれば、今回の入力/値/利用範囲/実権限とこの試験定義の適用を確認して開始する。

<a id="gen-001"></a>
## GEN-001 保存先と範囲

K：`KIT_ROOT`。承認D：`GENERATION_DRAFTS/sales`（本版：`GENERATION_DRAFTS/sales/runtime-v001`）。新規試験W：`GENERATED_WORKSPACES/sales`。

[preflight](runtime-v001/preflight.json) に実パス相互分離、祖先/アカウント指示、既知の発見設定、cwdと配置前内容を記録。Dは空、Wはinputsだけだった。Dの草稿は非実行名で、自動発見場所/稼働名を作らない。Kは読取りのみ。業務は起動しない。

<a id="gen-002"></a>
## GEN-002 生成元と内容識別

[source-manifest](runtime-v001/source-manifest.json) に現行のgenerate Skill、AGENTS、仕様/Q&A/両テンプレート/指定検査スクリプトと引継ぎ4ファイルのSHA-256を記録した。Git HEADは履歴上の参照だけで、未コミットの実キットを同一内容とみなさない。

[definition-manifest](runtime-v001/definition-manifest.json) は意味本文、判断参照、入力schema、回答出所抜粋と相対リンク文字列を識別する。manifest自体のSHA-256：`0221ee52b9377a677b2ec721b75ed4c2804998439018ee715ce3b125273e1f91`（[checksum](runtime-v001/definition-manifest.sha256)）。動的な承認/配置/検査記録を識別対象に循環的に含めない。

<a id="gen-003"></a>
## GEN-003 回答・出力対応

[台帳](runtime-v001/answers.md)、[詳細JSON](runtime-v001/answers.json)、[出力対応](runtime-v001/output-map.json) にEMP13/FIX9/GEN7/SKL13の42ID、3パラメータ子要素、10派生対応を記録した。本文に未展開の差込み記号を残さない。意味の出所は [質問/模擬回答](runtime-v001/source-evidence.md)。入力名/ヘッダーは [入力構造](runtime-v001/input-structure.json) のsource-only観察で、業務方針の本人確認ではない。fixture_revision v3の観察と過去v2の連絡を区別する。

EMP-004のrecords/definition.mdからAGENTSリンクとSkillの../../../records/definition.mdを導出した。同じW内で解決する。導出元変更時は子要素・参照・承認範囲を再評価する。

<a id="gen-004"></a>
## GEN-004 役割、実依頼と未承認

架空設定の4役割（依頼/成果検収/定義変更承認/保守・同期）は店長。AIが役割を演じた回答を本人確認としない。現在の実ユーザー [CURRENT-REQ-001](runtime-v001/current-request.md) はsales runtime-v001の新規生成、D保存、正規形式への修正、指定Wへの試験配置、静的検査とhash記録を許可している。上記manifestの対象がこの範囲に合うことを生成担当Codexが照合した。ユーザーが各hashを個別に検収した記録ではない。

旧REQ-001/002/003、旧保存先や旧承認は歴史資料。今回へ流用しない。設計レビュー、試験配置許可、業務実行依頼、成果検収は別欄に扱う。今回の業務実行・人の検収は未実施。実業務、原本変更、既存成果置換、外部送信/公開は範囲外。

<a id="gen-005"></a>
## GEN-005 実環境の観察

確認役：Codex生成担当。確認日時：2026-10-16T04:36:08.158150+00:00。対象：この生成会話。方法：session環境、指定先実パス/既存内容、祖先・アカウント指示、設定中の指示/Skill関連キー、Python/PyYAMLをローカルで点検。workspace-write、approval=never、network restrictedとして提供された環境。D/Wは指定された書込み対象。詳細はpreflightを参照する。

この観察とD/Wへの保存は業務環境の権限試験ではない。AGENTSの自動読込み、Skill発見/選択、業務用ツール/実権限/接続の確認は未実施。入力がOS設定で読取専用化されたとも主張しない。次の業務依頼時に当該Wの新しい会話で必要範囲を確認し、当回run記録に方法/対象/日時/未確認を残す。

<a id="gen-006"></a>
## GEN-006 新規生成と旧版保持

[変更記録](runtime-v001/change-record.md) を参照。旧台帳のtrial-v001と今回runtime-v001は別版。旧生成物実体は未読で三者比較は未実施/比較不能。現在Wには既存定義がなく、旧W/Dや手修正を置き換えない。指定の旧台帳・質問記録はDへbyte一致で保全した。旧仕様や承認を新しい事実へ書き換えない。

<a id="gen-007"></a>
## GEN-007 接続構造と配置点検

[接続計画](runtime-v001/connection-plan.json) と出力対応を使う。AGENTS.md正本、CLAUDE.mdの@AGENTS.md取り込み、.claude/skills/work-001/SKILL.md正本、.agents/skills/work-001から../../.claude/skills/work-001への相対symlink。保守担当はEMP-003の架空店長役、コピー方式は非該当。改訂ごとに参照の実体と同じ正本への到達を再検査する。

配置前の状態：試験候補。配置後の実体・構造・hashは後続のreceiptへ記録する。静的検査を自動認識/Skill選択/業務成功とみなさない。

## 未決・次の検証

生成/試験配置を止める新たな必須業務意味の未回答/矛盾は検出していない。SKL-012は任意未回答。実行時のinput_dir/start_date/end_dateは未受領であり、今回推定していない。必要値不足の停止はSKL-010へ接続済み。

AGENTS自動読込み、Skill発見/選択、入力からの業務遂行、HTMLの表示/操作、独立レビュー、人の検収は未実施。新しい会話・正しいWのcwdで別の依頼として検証する。業務出力/処理スクリプトはこの生成作業で作らない。

## 配置・検査の完了記録

記録日時：2026-10-16T04:46:11.529347+00:00。今回の到達点は **runtime-v001の新規試験配置・静的検査済み**。正常な設定自動認識や業務実行が確認された状態ではない。

[配置receipt](runtime-v001/deployment-receipt.json) は配置時点の19ファイル＋相対symlinkとhash、[指定構造検査JSON](runtime-v001/structure-check.json) は `/opt/homebrew/bin/python3` で指定KIT検査を実行した結果（exit 0、all_passed=true、errors空）、[追加点検](runtime-v001/extended-check.json) は42ID/3パラメータ/GEN-007/固定規則/未展開記号/参照解決/hashの検査結果。receiptの構造検査pendingは配置時点の履歴で、後続検査結果はこの節を参照する。

[配置前入力hash](runtime-v001/input-before.json) と [配置後入力hash](runtime-v001/input-after.json) は21ファイル一致。使用したK正本/テンプレート/検査スクリプトと引継ぎ4ファイルも保存前hashと一致。Dの原文保全も一致。業務出力・処理スクリプト・業務run記録を作成していない。

[完了receipt](runtime-v001/deployment-complete.json)、[配置済み全ファイル一覧/hash](runtime-v001/artifact-inventory.json)、[定義記録の状態更新](runtime-v001/definition-state-update.json) を参照。入力と動的記録を含む一覧は固定本文manifestと区別し、一覧自身は自己hashの対象に含めない。

残件：新しいCodex会話でこのWをcwdとしてAGENTS自動読込みとwork-001の発見/選択を確認する。別の業務依頼で必須3値/実権限を確認して架空入力の業務試験を行う。独立レビュー・人の検収は別途。ここではいずれも未実施。通常confirmed=0、human_acceptance=falseを維持する。
