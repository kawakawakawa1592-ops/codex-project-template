# Manuscripts

症例ごとの作業フォルダーです。

## 推奨構成

```text
manuscripts/
  case_report_001/
    00_case_input.md
    generated/
      zotero_collection_inventory.md
      zotero_api_diagnostics.md
      zotero_search_results.md
      citation_evidence_cards.md
      pdf_fulltext_review.md
      03_selected_references.md
      08_notes_for_revision.md
    submission/
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

## 見る順番

1. `00_case_input.md`: ユーザー入力から整理した症例情報
2. `generated/zotero_api_diagnostics.md`: Zotero抽出が成功したか
3. `generated/citation_evidence_cards.md`: 引用候補と根拠
4. `submission/03_main_manuscript.md`: 論文本体
5. `submission/08_submission_checklist.md`: 投稿前チェック
6. `submission/09_citation_check_table.md`: 本文主張と引用文献の対応

## ルール

- 症例ごとの成果物は原則として `manuscripts/{case_id}/` に集約する。
- `generated/` は自動生成物。直接編集せず、再実行で更新する。
- `submission/` は投稿用ドラフト。Codexが編集してよい。
- 不足情報は削除せず、`要確認` として残す。
