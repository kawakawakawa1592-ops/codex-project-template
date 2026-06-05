# Start Here: Case Report Project

医学症例報告を作成する場合は、まずこのファイルを見てください。

## 1. 投稿規定を入れる

```text
journal_guidelines/README.md
```

ここに投稿先雑誌のURL、確認日、主要規定を記録します。
URLだけでなく、要旨、本文文字数、図表数、文献形式、COI、患者同意などを要約してください。

## 2. 症例情報を作る

```text
templates/case_report_input_template.md
```

このテンプレートをコピーして、症例ごとに以下へ保存します。

```text
manuscripts/{case_id}/00_case_input.md
```

例:

```text
manuscripts/case_report_001/00_case_input.md
```

## 3. Zotero Reference Searchを実行する

GitHub Actionsから `Zotero Reference Search` を実行します。

推奨入力:

```text
case_id: case_report_001
reference_source: collection
zotero_collection_names: Zoteroのフォルダー名
search_keywords: 補助的な検索語
max_results: 50
debug: true
```

Zotero内で関連論文をフォルダーにまとめている場合、`reference_source: collection` を使ってください。

## 4. Zotero出力を見る

症例ごとの出力はここです。

```text
manuscripts/{case_id}/generated/
```

見る順番:

```text
zotero_api_diagnostics.md       Zotero抽出が成功したか
zotero_collection_inventory.md  Zoteroフォルダー名とkey一覧
citation_evidence_cards.md      引用候補と根拠
03_selected_references.md       採用候補文献
08_notes_for_revision.md        注意点
```

`references/` は共有メモ用です。症例ごとの文献確認では、必ず `manuscripts/{case_id}/generated/` を優先してください。

## 5. 投稿用原稿を作る

投稿用ファイルはここに作ります。

```text
manuscripts/{case_id}/submission/
```

標準ファイル:

```text
00_author_guideline_check.md
01_title_page.md
02_abstract.md
03_main_manuscript.md
04_references.md
05_figure_table_legends.md
06_ethics_coi_patient_consent.md
07_cover_letter_draft.md
08_submission_checklist.md
09_citation_check_table.md
10_revision_notes.md
```

## Codexへの依頼例

```text
リポジトリ: <repo>
case_id: case_report_001
投稿規定: journal_guidelines/README.mdを確認
症例情報: manuscripts/case_report_001/00_case_input.mdを使用
文献: manuscripts/case_report_001/generated/citation_evidence_cards.mdで確認できる文献のみ使用
出力: manuscripts/case_report_001/submission/に投稿用一式を作成
不足情報は推測せず要確認として残す
```

## 大事なルール

- 症例情報にない事実を追加しない。
- Zoteroで内容確認できない文献を引用しない。
- 投稿規定は `journal_guidelines/` 内の情報を優先する。
- 患者同意、倫理、COI、著者情報、図表匿名化は必ずチェックリストに残す。
- 図表数と本文文字数は投稿規定に合わせて最終調整する。
