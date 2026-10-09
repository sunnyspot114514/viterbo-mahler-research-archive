# Viterbo Mahler Research Archive

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[🇺🇸 English](README.md) | [🇨🇳 中文说明](README.zh-CN.md)

> AI 辅助研究档案：特定受限类别的 Viterbo / Mahler 证明候选、计算证书、历史报告和重放源码。

由 [@sunnyspot114514](https://github.com/sunnyspot114514) 整理，供审阅日期 **2026-10-07**。

本档案**不**宣称证明一般 Viterbo 或 Mahler 猜想，不主张相对于 OpenAI 的优先权，也不构成独立数学认证。

## 从这里开始

| 路径 | 内容 |
|------|------|
| [STATUS.md](STATUS.md) | 假设、证据层级、未决缺口与历史范围 |
| [latest/v61/report_zh.md](latest/v61/report_zh.md) | 最新原始研究报告（2026-09-27） |
| [latest/v61/README.md](latest/v61/README.md) | 原始 v61 源码与重放说明 |
| [originals/mahler/](originals/mahler/) | 未改动的 Mahler 快照，含原始 v61 ZIP |
| [originals/historical/](originals/historical/) | 未改动的 Viterbo 归档、恢复材料与早期独立文件 |
| [external-review/README.md](external-review/README.md) | 2026-10-07 对 OpenAI 工作的单独审读 |
| [publication_manifest.json](publication_manifest.json)、[FILES.tsv](FILES.tsv)、[SHA256SUMS](SHA256SUMS) | 文件清单与完整性校验 |

## 本包含什么

本包保留 **60 个原文件**（9,803,805 字节）：59 个原始研究文件，外加 1 个独立的外部审读归档。17 个重复 ZIP 载荷和 5 个重复散文件由已保留的归档代表，不再复制。最新 v61 载荷另外展开为 15 个未改动的可浏览文件。更早缺失的生成器和底层证书没有因此补齐。

整理时核对了文件大小、SHA-256 和 v61 归档载荷。**本次打包没有运行数学验证器。** 其中的 PASS 字符串和重放输出只是归档记录。部分历史重放说明依赖当时的环境；这不是一次已核验的一键重放发布。

## 许可证

[MIT 许可证](LICENSE) 仅覆盖自编软件源码。第三方材料、论文、证书和数据见 [LICENSE-SCOPE.md](LICENSE-SCOPE.md)。由 [@sunnyspot114514](https://github.com/sunnyspot114514) 维护。
