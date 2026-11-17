# diligram-rag

面向多源、多跳问题的检索与问答仓库：问题分解 → 逐步取证据（语义检索 + 关联/图查询）→ 证据整合 → 带出处的答案。

> 状态：**v0.1 骨架**。输出数据结构与评测约定已确定，检索与生成尚未实现。

## 定位

| 项 | 说明 |
|---|---|
| 输入 | `diligram-ocr-vlm` 产出的 `doc.schema.json` 文档 + 问题 |
| 输出 | 答案 + 证据链（文档、页码、`block_id`、原文片段）|
| 关键要求 | 每个结论都能回指到具体文本块；证据不足时要**明说不足**，而不是补全 |

## 与 diligram-ocr-vlm 的关系

```
原始文件 ──► diligram-ocr-vlm ──► doc.schema.json ──► diligram-rag ──► 证据链 + 答案
              (契约生产方)          (契约 v0.1)        (本仓库，消费方)
```

- 契约的**唯一权威**在 [`diligram-ocr-vlm/schema/doc.schema.json`](https://github.com/Ching-Chiang/diligram-ocr-vlm/blob/main/schema/doc.schema.json)。
- 本仓库**不复制** schema 文件，只按版本号引用；升级时机与容忍规则见 [`docs/interface.md`](docs/interface.md)。
- 本仓库只读契约产物，不解析原始 PDF / 图片。解析质量问题回 `diligram-ocr-vlm` 修。

## 目录

```
src/diligram_rag/         问答编排（当前为桩）
  pipeline.py             answer() 入口 + Answer / Evidence 数据结构
docs/interface.md         如何消费解析产物、版本升级策略
docs/eval.md              评测集、基线、指标与消融约定
configs/                  检索与生成配置示例
tests/                    数据结构与不变量测试
```

## 快速开始

```bash
pip install -e ".[dev]"
pytest
```

## 要解决的问题

单轮语义相似度检索在多源场景下容易**漏证据**：需要沿中间线索（实体、事件、持股关系）才能找到的信息，一次相似度查询命中不了。本仓库的方向是：

1. **问题分解** — 把复杂问题拆成有序的子问题与查询步骤
2. **混合检索** — 语义检索覆盖自由文本，关联/图查询覆盖实体与关系
3. **证据整合** — 逐步累积证据，识别矛盾与缺口
4. **按需补证** — 缺口不靠模型臆测，而是发起下一步检索

## 不做的事

- 不做文档解析与 OCR（→ `diligram-ocr-vlm`）
- 不做数据采集与爬取
- 不在缺少证据时输出「看起来合理」的答案

## 许可

尚未选择许可证。公开仓库在无许可证时默认保留所有权利，确定后再补 `LICENSE`。
