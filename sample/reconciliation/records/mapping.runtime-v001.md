# 出力対応 runtime-v001

42ID。Wの論理パスとD/runtime-v001内の非実行保存先を結ぶ。対象hashは[generation manifest](generation-manifest.runtime-v001.json)、値全文と出所/状態は[台帳](answers.runtime-v001.json)。

| 項目ID | 質問ID/skill_key | W出力位置 | D非実行パス | 根拠・状態 |
| --- | --- | --- | --- | --- |
| EMP-001 | Q-E01 / employee | `AGENTS.md#emp-001` | `employee-agents.draft.md` | U01-A、U02-COMMON / proposed |
| EMP-002 | Q-E02 / employee | `AGENTS.md#emp-002` | `employee-agents.draft.md` | U02-Q02、U02-COMMON / proposed |
| EMP-003 | Q-E03 / employee | `AGENTS.md#emp-003` | `employee-agents.draft.md` | U02-COMMON、U02-PERMIT、FIX-005/006/007；窓口から保守への接続はCodex整理案 / proposed |
| EMP-004 | Q-E04 / employee | `AGENTS.md#emp-004` | `employee-agents.draft.md` | U02-Q01/Q03、U02-COMMON/PERMIT、仕様2.2/10章；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| EMP-005 | Q-E05 / employee | `AGENTS.md#emp-005` | `employee-agents.draft.md` | U02-Q01、U02-COMMON/PERMIT / proposed |
| EMP-006 | Q-E06 / employee | `AGENTS.md#emp-006` | `employee-agents.draft.md` | U02-Q02、U02-COMMON / proposed |
| EMP-007 | Q-E07 / employee | `AGENTS.md#emp-007` | `employee-agents.draft.md` | U02-Q02/Q03、U02-COMMON、FIX-006 / proposed |
| EMP-008 | Q-E08 / employee | `AGENTS.md#emp-008` | `employee-agents.draft.md` | U02-Q03、U02-COMMON / proposed |
| EMP-009 | Q-E09 / employee | `AGENTS.md#emp-009` | `employee-agents.draft.md` | U02-Q03、U02-COMMON/PERMIT、FIX-005 / proposed |
| EMP-010 | Q-E10 / employee | `AGENTS.md#emp-010` | `employee-agents.draft.md` | U01-A/C、U02-PERMIT、Q-S01、GEN-007；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| EMP-011 | Q-E11 / employee | `AGENTS.md#emp-011` | `employee-agents.draft.md` | U02-Q03、U02-COMMON/PERMIT、FIX-007、EMP-003/004；保守接続はCodex整理案 / proposed |
| EMP-012 | Q-E12 / employee | `AGENTS.md#emp-012` | `employee-agents.draft.md` | U02-COMMON、GEN-005/007、FIX-008；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| EMP-013 | Q-E13 / employee | `AGENTS.md#emp-013` | `employee-agents.draft.md` | U02-COMMON、U02-Q02、仕様EMP-013の非権限的既定 / proposed |
| SKL-001 | Q-S01 / work-001 | `.claude/skills/work-001/SKILL.md:frontmatter.name` | `work-001.draft.md` | Q-S01、v001のskill_key / fixed-default |
| SKL-002 | Q-S02 / work-001 | `.claude/skills/work-001/SKILL.md:frontmatter.description` | `work-001.draft.md` | EMP-001/002、SKL-003/007、U02-Q02/COMMON；Codex要約案 / proposed |
| SKL-003 | Q-S03 / work-001 | `.claude/skills/work-001/SKILL.md#skl-003` | `work-001.draft.md` | U02-COMMON/PERMIT、EMP-002/003 / proposed |
| SKL-004 | Q-S04 / work-001 | `.claude/skills/work-001/SKILL.md#skl-004` | `work-001.draft.md` | U02-Q01/Q02/Q03、R01/R11 / proposed |
| SKL-005 | Q-S05 / work-001 | `.claude/skills/work-001/SKILL.md#skl-005` | `work-001.draft.md` | U02-Q01/Q03、U02-COMMON、EMP-004/012、GEN-001/005；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| SKL-006 | Q-S06 / work-001 | `.claude/skills/work-001/SKILL.md#skl-006` | `work-001.draft.md` | U02-Q02/Q03、R01〜R11全文 / proposed |
| SKL-007 | Q-S07 / work-001 | `.claude/skills/work-001/SKILL.md#skl-007` | `work-001.draft.md` | U02-Q02、U02-COMMON、R09〜R11、EMP-004/006；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| SKL-008 | Q-S08 / work-001 | `.claude/skills/work-001/SKILL.md#skl-008` | `work-001.draft.md` | U02-COMMON/Q03、R07/R10/R11 / proposed |
| SKL-009 | Q-S09 / work-001 | `.claude/skills/work-001/SKILL.md#skl-009` | `work-001.draft.md` | U02-Q02、U02-COMMON、EMP-003/006/007 / proposed |
| SKL-010 | Q-S10 / work-001 | `.claude/skills/work-001/SKILL.md#skl-010` | `work-001.draft.md` | U02-Q03、Skillテンプレートの停止引継ぎ、EMP-008 / proposed |
| SKL-011 | Q-S11 / work-001 | `.claude/skills/work-001/SKILL.md#skl-011` | `work-001.draft.md` | U02-Q01/Q02、OBS-03；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| SKL-012 | Q-S12 / work-001 | `.claude/skills/work-001/SKILL.md#skl-012` | `work-001.draft.md` | v001から任意未回答を保持 / unanswered |
| SKL-013 | Q-S13 / work-001 | `.claude/skills/work-001/SKILL.md#skl-013` | `work-001.draft.md` | U02-COMMON/PERMIT、EMP-009、SKL-006/007；現在のユーザー依頼U-RUNTIME-001（新W/D・正規形式・版のみ） / proposed |
| FIX-001 | Q-F01 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-001 / fixed-default |
| FIX-002 | Q-F02 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-002 / fixed-default |
| FIX-003 | Q-F03 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-003 / fixed-default |
| FIX-004 | Q-F04 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-004 / fixed-default |
| FIX-005 | Q-F05 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-005 / fixed-default |
| FIX-006 | Q-F06 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-006 / fixed-default |
| FIX-007 | Q-F07 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-007 / fixed-default |
| FIX-008 | Q-F08 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-008 / fixed-default |
| FIX-009 | Q-F09 / employee | `AGENTS.md#fixed-rules` | `employee-agents.draft.md` | ai-employee-format 0.1.4-draft 4章 FIX-009 / fixed-default |
| GEN-001 | Q-G01 / generation | `records/definition.md#gen-001` | `records/definition.draft.md` | 現行仕様 GEN-001／Q&A Q-G01／U-RUNTIME-001 / 観察と試験許可を別記 |
| GEN-002 | Q-G02 / generation | `records/definition.md#gen-002` | `records/definition.draft.md` | 現行仕様 GEN-002／Q&A Q-G02／U-RUNTIME-001 / 観察と試験許可を別記 |
| GEN-003 | Q-G03 / generation | `records/definition.md#gen-003` | `records/definition.draft.md` | 現行仕様 GEN-003／Q&A Q-G03／U-RUNTIME-001 / 観察と試験許可を別記 |
| GEN-004 | Q-G04 / generation | `records/definition.md#gen-004` | `records/definition.draft.md` | 現行仕様 GEN-004／Q&A Q-G04／U-RUNTIME-001 / 観察と試験許可を別記 |
| GEN-005 | Q-G05 / generation | `records/definition.md#gen-005` | `records/definition.draft.md` | 現行仕様 GEN-005／Q&A Q-G05／U-RUNTIME-001 / 観察と試験許可を別記 |
| GEN-006 | Q-G06 / generation | `records/definition.md#gen-006` | `records/definition.draft.md` | 現行仕様 GEN-006／Q&A Q-G06／U-RUNTIME-001 / 観察と試験許可を別記 |
| GEN-007 | Q-G07 / generation | `records/definition.md#gen-007` | `records/definition.draft.md` | 現行仕様 GEN-007／Q&A Q-G07／U-RUNTIME-001 / 観察と試験許可を別記 |

## 子要素と派生依存

| 子要素/派生値 | 導出元 | W出力 | D非実行パス | 変換規則・状態 |
| --- | --- | --- | --- | --- |
| P01.invoice_source | work-001/SKL-004、U02-Q01/Q03、R01 | `.claude/skills/work-001/SKILL.md#p01-invoice_source` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P02.bank_source | work-001/SKL-004、U02-Q01/Q03、R01/R07 | `.claude/skills/work-001/SKILL.md#p02-bank_source` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P03.customer_source | work-001/SKL-004、U02-Q01、R01/R06 | `.claude/skills/work-001/SKILL.md#p03-customer_source` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P04.rule_source | work-001/SKL-004、U02-Q01/Q02、SKL-011 | `.claude/skills/work-001/SKILL.md#p04-rule_source` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P05.as_of | work-001/SKL-004、U02-Q01/Q03、R01 | `.claude/skills/work-001/SKILL.md#p05-as_of` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P06.period | work-001/SKL-004、U02-Q01/Q02/COMMON、R01 | `.claude/skills/work-001/SKILL.md#p06-period` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P07.money | work-001/SKL-004、U02-Q01/Q03、R01/R06/R10 | `.claude/skills/work-001/SKILL.md#p07-money` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P08.input_dir | work-001/SKL-004、U02-Q01/Q03 | `.claude/skills/work-001/SKILL.md#p08-input_dir` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P09.dataset_id | work-001/SKL-004、U02-Q01/Q03 | `.claude/skills/work-001/SKILL.md#p09-dataset_id` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| P10.manifest | work-001/SKL-004、U02-Q01/Q03、OBS-03 | `.claude/skills/work-001/SKILL.md#p10-manifest` | work-001.draft.md | 子要素キーを固定アンカーへ変換。proposed/試験内定義充足、具体値は実行時 |
| AGENTSの記録リンク | EMP-004 | AGENTS.md → records/definition.md | employee-agents.draft.md | root基準の定義記録パスをそのまま使う |
| Skillの記録リンク | EMP-004 | Skill → ../../../records/definition.md | work-001.draft.md | 正本ディレクトリから同じ定義記録へ相対変換 |
| 正本パス/slug | SKL-001、EMP-010 | .claude/skills/work-001/SKILL.md | work-001.draft.md | Q-S01の既存キーwork-001を維持 |
| Codex接続 | SKL-001、GEN-007 | .agents/skills/work-001 → ../../.claude/skills/work-001 | records/connection-plan.runtime-v001.md | 同じworkspace内の正本へ相対symlink |
| Claude取り込み | GEN-007 | CLAUDE.md → @AGENTS.md | employee-claude.draft.md | 固定の取り込み規則 |
| 作業位置 | EMP-004、GEN-001、SKL-005 | 社員workspace root | work-001.draft.md | 絶対保存先や旧W記号を本文へ埋め込まない |
| 成果と記録の保存 | EMP-004、SKL-007/010 | outputs、records/runsの新しいrun_id子ディレクトリ | work-001.draft.md | 指定root＋衝突しない識別子。業務開始時に生成 |
| 依存資料 | EMP-004、SKL-011 | Skill → ../../../inputsの6既存ファイル | work-001.draft.md | 正本基準の相対参照。既存原本不変 |

導出元が変われば依存リンク・子要素・出力位置・対象版と許可範囲を再評価する。機械的なパス変換を新しい業務回答にせず、意味の整理案はproposedを保持する。
