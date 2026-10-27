# 請求・入金照合担当 — 現行定義

業務条件はruntime-v001（生成仕様0.1.4-draft／Q&A0.1.2-draft）を継承します。配布構成はsample-layout-v003。履歴整理と参照先変更であり、社員の再生成や新しい業務実行を行った記録ではありません。

<a id="gen-001"></a>
## GEN-001 作業場所

この社員フォルダ全体をKIT外へコピーし、そのコピーを新しい会話の作業場所にします。inputsは原本、outputsは成果物、records/runsは今後の実行・停止記録です。必要な新規処理コードはscriptsへ保存します。後二者は必要時に作成します。過去の保存先や許可をコピー先に引き継ぎません。

<a id="gen-002"></a>
## GEN-002 定義の識別

[sample.json](../sample.json) の `current_definition_sha256` が現在のAGENTS・CLAUDE・Skill・参照資料・ヒアリング・この定義記録を識別します。開始時に実ファイルのhashを取得し、同じ台帳の入力hashと併せて照合します。不一致は黙って許容せず、変更内容と対象版を確認します。新しい実行記録には台帳自体のhashも残します。

同梱成果は整理前の定義から実行した最新runのままです。`latest_run.executed_definition_sha256` はその時のhashで、現在の定義hashとは別です。元の生成manifest・実行・検証記録は [保存済みGit版](https://github.com/Cyberdog-AI-Lab/ai-employee-kit/tree/8ed9ba51a3bf66ab8f8a009e6fbc3551b23394c1/sample/reconciliation/records) から回復できます。

<a id="gen-003"></a>
## GEN-003 回答と対応

[interview.md](../interview.md) に現行の質問・模擬回答・未決をまとめています。EMP-001〜013はAGENTS、SKL-001〜013はSkill、FIX-001〜009はAGENTSの固定規則、GEN-001〜007は本書に対応します。意味回答はproposed、SKL-001はfixed-default、SKL-012は任意unanswered、通常confirmedは0です。42IDの元台帳はヒアリングから参照できます。パラメータ子要素もproposedで、型・不足時の扱いはSkillのSKL-004にあります。

<a id="gen-004"></a>
## GEN-004 許可と検収

架空資料の試験として作成した社員です。入力が架空であるとの申告元は取りまとめAIで、入力READMEにも範囲を記載しています。定義の配置、個別の業務実行、人の成果検収を分けます。新しい仕事は依頼・パラメータ・入力利用範囲を確認してから始めます。過去の試験許可・AIレビューを人の承認へ変更しません。

<a id="gen-005"></a>
## GEN-005 実環境

コピー先の実権限・ツール・承認設定は、この配布記録では未確認です。開始担当が実パス、読取り、新規保存先、衝突、必要な操作権限を確認し、対象・日時・方法・結果・未確認を新しいrun記録へ残します。ファイルの静的整合や以前の成功から現在の権限を推定しません。

<a id="gen-006"></a>
## GEN-006 改訂

現行ツリーには最新定義と最新成果だけを同梱しています。過去の草稿・回答台帳・実行ログ・画面検証は上記Git版に保存済みです。今後の改訂でも変更前をGitまたは別の保全先へ保持し、対象ID・差分・理由・影響を確認します。既存出力を置換しません。

<a id="gen-007"></a>
## GEN-007 両ツールへの接続

AGENTS.mdが正本、CLAUDE.mdは `@AGENTS.md` を取り込みます。業務Skillの正本は [.claude/skills/work-001/SKILL.md](../.claude/skills/work-001/SKILL.md)、Codex用は `.agents/skills/work-001` から同じ社員内の正本への相対symlinkです。静的構造、実際のSkill発見、業務実行、人の検収は別に確認します。
