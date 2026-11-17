# 消费解析产物（契约 v0.1）

本仓库是 `doc.schema.json` 的**消费方**。权威定义在
[`diligram-ocr-vlm/schema/doc.schema.json`](https://github.com/Ching-Chiang/diligram-ocr-vlm/blob/main/schema/doc.schema.json)，
本文件只记录我们怎么用它。

## 1. 版本引用

- 当前消费契约版本：**`0.1`**。
- 不复制 schema 文件到这里，避免两份定义漂移。
- 收到 `schema_version` 不等于 `0.1` 的产物时：**拒绝索引并报警**，不做猜测性兼容。
- 待办：把校验接进摄取流程（`jsonschema` + 生产方 schema 的固定 commit 引用）。

## 2. 可以依赖的不变量

以下是契约承诺、我们允许依赖的部分：

1. `pages` 按 `page_no` 升序，从 1 开始。
2. 每个 `block` 必有 `block_id`、`type`、`order`；`block_id` 在文档内唯一。
3. `bbox` 为 4 元组、归一化到 0–1；**可能缺失**，缺失时该块不可高亮。
4. `source.sha256` 为 64 位小写十六进制，用于固定文档版本。

## 3. 必须容忍的部分

| 情况 | 处理方式 |
|---|---|
| `bbox` 缺失 | 索引照常建立，证据引用退化为「页码 + 原文片段」 |
| `confidence` 缺失或为 `null` | 不参与排序加权；不得当作 0 |
| `block.table.cells` 不满格 | 按实际存在的单元格建索引，不补空串 |
| `fields` 缺失 | 走通用文本检索路径，不假设有结构化字段 |
| 同一 `sha256` 多次解析 | 以 `pipeline.created_at` 最新者为准，旧结果归档不删 |

## 4. 索引粒度

以 `block` 为最小索引单元，保留 `doc_id` / `page_no` / `block_id` 三元组作为引用键。
表格按 `cells` 展开为行级文本再索引，同时保留整表入口，避免只命中半张表。

**待验证：**块级索引在长文档上是否够用，还是需要章节级聚合。这是 v0.2 的实验项，不预设结论。

## 5. 升级流程

1. 生产方提升 `schema_version` → 本仓库发 issue 记录影响面（索引、引用、评测集）。
2. 新版本先并行摄取一份影子索引，跑同一评测集对比。
3. 达标后再切主索引；不达标就退回旧版本并说明原因。
