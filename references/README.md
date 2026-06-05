# References

プロジェクト全体で共有する文献メモを置くフォルダーです。

## 重要

症例ごとのZotero抽出結果は、原則として以下を優先して確認します。

```text
manuscripts/{case_id}/generated/
```

この `references/` フォルダーは、複数症例で再利用する文献メモ、検索戦略、投稿済み文献リストなどの共有資料用です。

## 推奨ファイル

- `search_strategy.md`: 文献検索方針
- `common_references.md`: 複数症例で使う代表文献
- `excluded_references.md`: 引用しないと判断した文献と理由

## 運用ルール

- 症例本文に引用する文献は、症例別の `generated/citation_evidence_cards.md` と `submission/09_citation_check_table.md` で対応を確認する。
- Zotero keyやDOIなど確認用情報はドラフト段階では残してよいが、投稿用最終版では投稿規定に従って削除・整形する。
