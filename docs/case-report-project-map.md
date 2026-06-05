# Case Report Project Map

このテンプレートを医学症例報告で使う場合の見取り図です。

## 最初に見る場所

```text
README.md                         全体説明
journal_guidelines/README.md       投稿規定URLと主要規定
templates/case_report_input_template.md
                                  症例情報入力テンプレート
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
6. `manuscripts/{case_id}/submission/` に投稿用ファイルを作成する。
7. `submission/09_citation_check_table.md` で本文主張と引用文献の対応を確認する。
8. `submission/08_submission_checklist.md` で投稿規定、個人情報、COI、患者同意、図表を確認する。

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

## Codexに依頼するときの短い書き方

```text
リポジトリ: <repo>
case_id: case_report_001
投稿先: <雑誌名>
投稿規定: journal_guidelines/README.mdを確認
症例情報: manuscripts/case_report_001/00_case_input.mdを使用
文献: manuscripts/case_report_001/generated/citation_evidence_cards.mdから確認できる文献のみ使用
出力: manuscripts/case_report_001/submission/に投稿用一式を作成
```
