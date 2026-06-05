# Case Report Project Map

このテンプレートを医学症例報告で使う場合の見取り図です。

## 最初に見る場所

```text
README.md                         全体説明
START_HERE_CASE_REPORT.md          症例報告用の入口
journal_guidelines/README.md       投稿規定URLと主要規定
templates/case_report_input_template.md
                                  症例情報入力テンプレート
project_rules/case_report_discussion_policy.md
                                  考察作成・校正の指示簿
templates/discussion_revision_checklist.md
                                  考察校正チェックリスト
manuscripts/{case_id}/00_case_input.md
                                  症例ごとの入力情報整理
manuscripts/{case_id}/generated/   Zotero reference search出力
manuscripts/{case_id}/submission/  投稿用ドラフト一式
```

## 症例ごとの作業フロー

1. `templates/case_report_input_template.md` をもとに症例情報を整理する。
2. `journal_guidelines/README.md` に投稿規定URL、確認日、主要規定を保存する。
3. GitHub Actionsの `Zotero Reference Search` を実行する。
4. `manuscripts/{case_id}/generated/zotero_api_diagnostics.md` で抽出成功を確認する。
5. `manuscripts/{case_id}/generated/citation_evidence_cards.md` で引用可能文献を確認する。
6. `project_rules/case_report_discussion_policy.md` を確認して、考察の中心となる臨床判断の問いを決める。
7. `manuscripts/{case_id}/submission/` に投稿用ファイルを作成する。
8. `templates/discussion_revision_checklist.md` で考察を自己点検する。
9. `submission/09_citation_check_table.md` で本文主張と引用文献の対応を確認する。
10. `submission/08_submission_checklist.md` で投稿規定、個人情報、COI、患者同意、図表を確認する。

## Zotero出力を見る順番

```text
manuscripts/{case_id}/generated/zotero_api_diagnostics.md
manuscripts/{case_id}/generated/zotero_collection_inventory.md
manuscripts/{case_id}/generated/citation_evidence_cards.md
manuscripts/{case_id}/generated/03_selected_references.md
```

`references/` は共有文献メモ用です。症例ごとの判断では、必ず `manuscripts/{case_id}/generated/` を優先します。

## 投稿用ファイルの役割

- `00_author_guideline_check.md`: 投稿規定の確認結果
- `01_title_page.md`: 表題、英語表題、キーワード、著者情報
- `02_abstract.md`: 投稿規定に応じた要旨・抄録
- `03_main_manuscript.md`: 論文本体
- `04_references.md`: 参考文献
- `05_figure_table_legends.md`: 図表説明
- `06_ethics_coi_patient_consent.md`: 倫理、同意、COI
- `07_cover_letter_draft.md`: カバーレター案
- `08_submission_checklist.md`: 投稿前チェックリスト
- `09_citation_check_table.md`: 引用対応表
- `10_revision_notes.md`: 修正履歴と残課題

## 考察作成の基本姿勢

考察は文献紹介ではなく、本症例で生じた臨床判断の問いに答える文章として構成します。

必ず以下を確認します。

```text
project_rules/case_report_discussion_policy.md
templates/discussion_revision_checklist.md
```

考察で避けること:

- 文献A、文献B、文献Cを順に紹介するだけの構成
- 症例経過の再掲
- 処置名の羅列
- 「本症例は〜を示唆する」の多用
- 小児心理社会的負担を治療判断と切り離した一般論として書くこと

考察で重視すること:

- 本症例で最も難しかった臨床判断を1文で定義する
- 既報と本症例の共通点だけでなく相違点を書く
- 各治療を病態生理と治療意図で整理する
- 段落末に次段落への橋渡しを入れる
- 最後に本症例から得られる実践的示唆へ戻る

## Codexに依頼するときの短い書き方

```text
リポジトリ: <repo>
case_id: case_report_001
投稿先: <雑誌名>
投稿規定: journal_guidelines/README.mdを確認
症例情報: manuscripts/case_report_001/00_case_input.mdを使用
文献: manuscripts/case_report_001/generated/citation_evidence_cards.mdから確認できる文献のみ使用
考察: project_rules/case_report_discussion_policy.mdに従って臨床判断の問いを中心に構成
出力: manuscripts/case_report_001/submission/に投稿用一式を作成
```
