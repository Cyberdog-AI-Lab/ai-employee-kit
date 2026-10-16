# REQ-RUNTIME-001 — 現在の試験生成・配置依頼

記録者：Codex生成担当。以下は現在のユーザーメッセージの原文。送信時刻は取得していない。記録時刻はsource-manifest.jsonのgenerated_atを参照。
この依頼をruntime-v001の新規生成・指定Dへの保存・指定Wへの試験配置の根拠とする。旧REQ-001/002/003は過去の記録であり、現行の許可に置き換えて流用しない。新規定義の具体的なファイルとhashはdefinition-manifest.jsonで対応づける。通常の本人による意味回答確認・定義の検収・業務成果の検収を受けた記録ではない。

> $ai-employee-generate
>
> 現在のユーザー依頼に基づく生成回帰試験です。対象は架空のminutes社員だけです。Kit K=KIT_ROOT、承認された草稿 D=GENERATION_DRAFTS/minutes、承認された新規試験workspace W=GENERATED_WORKSPACES/minutes。K/D/Wは分離されています。
>
> ユーザーは「サンプルの中身がAGENTS.mdやSKILL.mdといったCodexが理解できる設定ファイルの形式でできてない。ちゃんとそこはKITにも反映して」「修正後、別の新規会話／正しい作業ディレクトリで実際に設定が認識されること、必要なスキルが選択できること、サンプル入力から業務を実行できることを検証」と依頼しています。これはこの架空サンプルの現行KITからの新規生成・Dへの保存・Wへの正式構造の試験配置を許可する範囲です。元データや過去成果物の置換、外部送信、実業務利用の許可ではありません。通常confirmed/人の承認・検収へ昇格しません。
>
> 引継ぎの模擬回答と質問の記録は TRIAL_RECORDS/generation-inputs/minutes にあります。旧仕様・旧W/D・旧承認は過去資料です。意味内容と出所を保持して現在の仕様0.1.4-draftとQ&A0.1.2-draftに対応づけ、新しい生成版runtime-v001としてDへ台帳と記録を作り、Wへ配置してください。過去の生成物を改名するだけではなく、実際のgenerate Skill・正本・テンプレートを読んで生成してください。全42ID対応と必要なパラメータ定義を保持します。今回の技術的な新W/D・正規形式への変更はユーザー依頼に含まれています。業務意味は勝手に変更しないでください。
>
> Wには既に架空inputsだけがあります。入力の具体的ファイル名・形式と必要な業務条件の確認のため読めます。inputsは変更しません。書込みはD・Wだけ。Kit Kと旧D/Wは読取りのみ。Kのsample/substantial各例のoutput・processing-reference・validation・expected・provenanceや、他の社員workspace、取りまとめの期待値・検査資料は読まないでください。正解を見て定義を作らないでください。
>
> 生成するAGENTS.mdとSKILL.mdは説明用コードフェンスで包まず、Wの .claude/skills/<slug>/SKILL.md を正本、.agents/skills/<slug> を同じW内への相対リンクとします。CLAUDE.mdも用意してください。依存する参照資料・定義記録はW内に実在させ、リンク先を解決してください。可搬性のため本文のパスはW基準/Skill基準の相対参照を使い、絶対保存先や古いW記号を業務手順に埋め込まないでください。根拠記録には今回の実パス・旧版との関係を正確に残せます。
>
> 配置後は /opt/homebrew/bin/python3 KIT_ROOT/scripts/verify_employee_workspace.py GENERATED_WORKSPACES/minutes --kit-root KIT_ROOT を実行し、JSONをDまたはWの記録へ保存してください。入力hash保持・GEN-007・42ID・未展開記号なしも確認し、今回の定義manifest/hashを作ります。配置対象の新規定義の形式修正と現在の許可範囲の試験配置はこの依頼で認められています。同じ許可を聞き直さず、業務意味の本当の未決/矛盾だけを具体的に報告してください。
>
> ここでは業務・HTML生成・スクリプト実装・会計更新を始めません。設定の自動認識や業務成功も未検証です。最後に新規生成したファイル、仕様版、Skill名、構造検査、残件を報告してください。別エージェント起動・ブラウザ操作・ユーザーの他作業への操作は不要です。

ユーザーから続けて提示されたSkill本文は、Kの実体 `.claude/skills/ai-employee-generate/SKILL.md` を読み、その実ファイルhashを生成元manifestに記録した。Skill本文は業務回答ではない。
