# sales 回答台帳 runtime-v001

案件：employee-showcase-sales。仕様0.1.4-draft / Q&A0.1.2-draft。固定記録日時：2026-10-16T04:36:08.158150+00:00。

仕事：showcase-sales-001 / work-001。意味回答はproposed、形式slugだけfixed-default、SKL-012は任意unanswered。通常confirmed=0。架空試験条件と実際のCURRENT-REQ-001許可を分離する。通常配置条件を満たした扱いにしない。詳細値・旧行の意味/状態/出所・パラメータは [機械可読台帳](answers.json)、[引用原文](source-evidence.md)、[改版記録](change-record.md)。

## 42ID対応

| スコープ | 質問 | ID | 通常状態/観察 | 出力位置 | 根拠・未決 |
| --- | --- | --- | --- | --- | --- |
| employee | Q-E01 | EMP-001 | proposed | `AGENTS.md#emp-001` | records/runtime-v001/source-evidence.md#sim-common; records/runtime-v001/source-evidence.md#sim-case; records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E02 | EMP-002 | proposed | `AGENTS.md#emp-002` | records/runtime-v001/source-evidence.md#sim-case; records/runtime-v001/source-evidence.md#sales-1; records/runtime-v001/source-evidence.md#sales-6; records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E03 | EMP-003 | proposed | `AGENTS.md#emp-003` | records/runtime-v001/source-evidence.md#sim-common; records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E04 | EMP-004 | proposed | `AGENTS.md#emp-004` | records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E05 | EMP-005 | proposed | `AGENTS.md#emp-005` | records/runtime-v001/source-evidence.md#sim-common; records/runtime-v001/source-evidence.md#detail-003 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E06 | EMP-006 | proposed | `AGENTS.md#emp-006` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sales-7 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E07 | EMP-007 | proposed | `AGENTS.md#emp-007` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sales-8 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E08 | EMP-008 | proposed | `AGENTS.md#emp-008` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sales-1; records/runtime-v001/source-evidence.md#sales-2; records/runtime-v001/source-evidence.md#sales-4 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E09 | EMP-009 | proposed | `AGENTS.md#emp-009` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sim-common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E10 | EMP-010 | proposed | `AGENTS.md#emp-010` | records/runtime-v001/source-evidence.md#sim-case; records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E11 | EMP-011 | proposed | `AGENTS.md#emp-011` | records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E12 | EMP-012 | proposed | `AGENTS.md#emp-012` | records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| employee | Q-E13 | EMP-013 | proposed | `AGENTS.md#emp-013` | records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S01 | SKL-001 | fixed-default | `.claude/skills/work-001/SKILL.md:frontmatter.name` | Q&A 0.1.2-draft Q-S01; source-manifest.json; prior skill_key showcase-sales-001 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S02 | SKL-002 | proposed | `.claude/skills/work-001/SKILL.md:frontmatter.description` | records/runtime-v001/source-evidence.md#sim-case; records/runtime-v001/source-evidence.md#sales-6; records/runtime-v001/source-evidence.md#sales-7 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S03 | SKL-003 | proposed | `.claude/skills/work-001/SKILL.md#skl-003` | records/runtime-v001/source-evidence.md#sim-case; records/runtime-v001/source-evidence.md#sales-1; records/runtime-v001/source-evidence.md#sales-6 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S04 | SKL-004 | proposed | `.claude/skills/work-001/SKILL.md#skl-004` | records/runtime-v001/source-evidence.md#sales-1; records/runtime-v001/source-evidence.md#sales-2; records/runtime-v001/source-evidence.md#sales-4; records/runtime-v001/source-evidence.md#sales-5; records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S05 | SKL-005 | proposed | `.claude/skills/work-001/SKILL.md#skl-005` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sales-1 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S06 | SKL-006 | proposed | `.claude/skills/work-001/SKILL.md#skl-006` | records/runtime-v001/source-evidence.md#sales-1; records/runtime-v001/source-evidence.md#sales-2; records/runtime-v001/source-evidence.md#sales-3; records/runtime-v001/source-evidence.md#sales-4; records/runtime-v001/source-evidence.md#sales-5; records/runtime-v001/source-evidence.md#sales-6; records/runtime-v001/source-evidence.md#sales-7; records/runtime-v001/source-evidence.md#sales-8; records/runtime-v001/source-evidence.md#detail-003; records/runtime-v001/source-evidence.md#legacy-interpretation / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S07 | SKL-007 | proposed | `.claude/skills/work-001/SKILL.md#skl-007` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sales-7; records/runtime-v001/source-evidence.md#detail-003 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S08 | SKL-008 | proposed | `.claude/skills/work-001/SKILL.md#skl-008` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sales-8; records/runtime-v001/source-evidence.md#sales-4; records/runtime-v001/source-evidence.md#detail-003 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S09 | SKL-009 | proposed | `.claude/skills/work-001/SKILL.md#skl-009` | records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S10 | SKL-010 | proposed | `.claude/skills/work-001/SKILL.md#skl-010` | records/runtime-v001/source-evidence.md#common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S11 | SKL-011 | proposed | `.claude/skills/work-001/SKILL.md#skl-011` | records/runtime-v001/source-evidence.md#sales-1; records/runtime-v001/source-evidence.md#sales-3; records/runtime-v001/source-evidence.md#sales-4; records/runtime-v001/source-evidence.md#detail-003 / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| showcase-sales-001 | Q-S12 | SKL-012 | unanswered | `.claude/skills/work-001/SKILL.md#skl-012` |  / 任意未回答 |
| showcase-sales-001 | Q-S13 | SKL-013 | proposed | `.claude/skills/work-001/SKILL.md#skl-013` | records/runtime-v001/source-evidence.md#common; records/runtime-v001/source-evidence.md#sim-common / 通常の本人確認なし。今回の実行値/実権限/認識/業務成功とは別。 |
| fixed | Q-F01 | FIX-001 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-001; source-manifest.json / なし |
| fixed | Q-F02 | FIX-002 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-002; source-manifest.json / なし |
| fixed | Q-F03 | FIX-003 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-003; source-manifest.json / なし |
| fixed | Q-F04 | FIX-004 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-004; source-manifest.json / なし |
| fixed | Q-F05 | FIX-005 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-005; source-manifest.json / なし |
| fixed | Q-F06 | FIX-006 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-006; source-manifest.json / なし |
| fixed | Q-F07 | FIX-007 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-007; source-manifest.json / なし |
| fixed | Q-F08 | FIX-008 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-008; source-manifest.json / なし |
| fixed | Q-F09 | FIX-009 | applied from canonical specification | `AGENTS.md#fixed-rules` | ai-employee-format 0.1.4-draft §4 FIX-009; source-manifest.json / なし |
| generation | Q-G01 | GEN-001 | 点検済み（候補作成時） | `records/definition.md#gen-001` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / なし |
| generation | Q-G02 | GEN-002 | 点検済み（候補作成時） | `records/definition.md#gen-002` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / なし |
| generation | Q-G03 | GEN-003 | 点検済み（候補作成時） | `records/definition.md#gen-003` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / なし |
| generation | Q-G04 | GEN-004 | 点検済み（候補作成時） | `records/definition.md#gen-004` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / business/runtime/human acceptance unverified |
| generation | Q-G05 | GEN-005 | 点検済み（候補作成時） | `records/definition.md#gen-005` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / business/runtime/human acceptance unverified |
| generation | Q-G06 | GEN-006 | 点検済み（候補作成時） | `records/definition.md#gen-006` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / なし |
| generation | Q-G07 | GEN-007 | 接続計画作成済み。配置後結果は定義記録へ | `records/definition.md#gen-007` | CURRENT-REQ-001; ai-employee-format 0.1.4-draft; preflight.json; source-manifest.json / business/runtime/human acceptance unverified |

## パラメータ子要素

| 親/子キー | 型 | 必須性 | 検証 | 定義状態/出所 | 不足時 |
| --- | --- | --- | --- | --- | --- |
| showcase-sales-001/SKL-004/input_dir | パス文字列 | 毎回必須 | 依頼から受領し、この社員workspaceの inputs/ と実パスが一致すること。配下のファイルとsymlinkも同範囲内で読取り可能であること。 | proposed / SIM-DETAIL-002 sales-5/common、本人確認なし | 開始前停止。質問前にrecords/runs新規停止記録、書けなければ会話。outputsを作らず別runで再開。 |
| showcase-sales-001/SKL-004/start_date | ISO日付 YYYY-MM-DD | 毎回必須 | 依頼から受領。実在する暦日で、start_date <= end_date。開始日を含む。 | proposed / SIM-DETAIL-002 sales-5/common、本人確認なし | 開始前停止。質問前にrecords/runs新規停止記録、書けなければ会話。outputsを作らず別runで再開。 |
| showcase-sales-001/SKL-004/end_date | ISO日付 YYYY-MM-DD | 毎回必須 | 依頼から受領。実在する暦日で、start_date <= end_date。終了日を含む。 | proposed / SIM-DETAIL-002 sales-5/common、本人確認なし | 開始前停止。質問前にrecords/runs新規停止記録、書けなければ会話。outputsを作らず別runで再開。 |

各子要素の出力はSKILL.md#skl-004の同名パラメータ。今回の値は未受領。親SKL-004もproposedを維持する。

## 未決と再開

必須業務意味の新しい未回答/衝突は検出していない。任意SKL-012は省略。通常の本人確認、実行時3値、業務環境/実権限、AGENTS自動読込み・Skill発見/選択、業務試験、人の検収は未完了。今回は試験配置まで。
