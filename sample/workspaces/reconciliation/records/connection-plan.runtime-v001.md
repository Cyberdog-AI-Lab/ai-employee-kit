# GEN-007接続計画 runtime-v001

| D/runtime-v001からの非実行パス | Wの正式配置先 | 方式 |
| --- | --- | --- |
| employee-agents.draft.md | AGENTS.md | 展開済み本文。外側コードフェンスなし |
| employee-claude.draft.md | CLAUDE.md | @AGENTS.mdの1行を取り込み |
| work-001.draft.md | .claude/skills/work-001/SKILL.md | 先頭YAML name/description付き正本 |
| この接続計画 | .agents/skills/work-001 | ../../.claude/skills/work-001への相対symlink |
| records/definition.draft.md | records/definition.md | 定義・観察・許可記録 |
| records内の残りの記録 | records内の同名相対パス | 台帳・出所・対応・検査・原bytesアーカイブ |

DにAGENTS.md/CLAUDE.md/SKILL.mdや.claude/skills・.agents/skillsを作らない。Wのリンク先は同じW内の正本。既存リンク・実ディレクトリ・リンク文字列ファイルを上書きしない。今回はsymlink方式でコピー同期は発生しない。保守担当はEMP-003の別途変更を依頼されたキット生成担当。正本変更ごとに参照解決と同一内容を確認する。コピー方式へ移行した場合はコピー先を編集せず同担当が同期・内容一致を確認する。

AGENTSからrecords/definition.md、Skill正本から../../../records/definition.mdへ同じ記録を参照する。入力6ファイルは既存原本を依存先として使用し、配置でコピー/置換しない。
