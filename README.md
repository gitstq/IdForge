# 🆔 IdForge

> 零依赖 · 可排序唯一 ID 生成引擎（ULID / UUID v7 / UUID v4，纯 Python 标准库）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Zero Dependency](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](requirements.txt)

**IdForge** 是一个**零第三方依赖、完全离线**的唯一标识符生成引擎，用纯 Python 标准库实现。它支持三种主流方案——**ULID**（时间可排序、人类友好）、**UUID v7**（RFC 9562，毫秒时间戳可排序）、**UUID v4**（RFC 4122，纯随机）——既可作为库导入，也可作为命令行工具直接使用，适合分布式系统、数据库主键、日志追踪与 Agent 工具链。

🌐 **语言 / Language：**
[🇨🇳 简体中文](#-简体中文-1) ｜ [🇹🇼 繁體中文](#-繁體中文-1) ｜ [🇺🇸 English](#-english-1)

---

<details open>
<summary><b>🇨🇳 简体中文</b></summary>

## 🎉 项目介绍

**IdForge** 定位于「开箱即用的唯一 ID 工厂」。它在分布式系统、数据库主键、事件溯源、日志链路追踪与 AI Agent 工具链等场景中，解决一个共同痛点：**如何在不引入任何依赖、不依赖数据库/中心服务的前提下，生成全局唯一且可按时间排序的 ID**。

- **核心价值**：单文件可嵌入；输出符合公开规范（ULID / RFC 9562 / RFC 4122），可被任意语言解析；时间可排序，天然适合作为数据库主键与索引。
- **解决痛点**：传统自增 ID 暴露规模、UUID v4 不可排序导致索引碎片化、第三方 Snowflake 库又重又依赖网络。IdForge 用纯标准库一次性解决。
- **自研差异化亮点**：
  - 同时支持 **ULID / UUIDv7 / UUIDv4** 三种语义，统一 API；
  - ULID 提供 **单调生成（monotonic）** 模式，避免同一毫秒内的时钟回拨/乱序；
  - 内置 `parse` 命令可**反解 ID 类型与创建时间戳**，便于排障；
  - 密码学安全随机源（`secrets`），无随机数质量隐患。
- **灵感来源**：ULID 规范、RFC 9562（UUID v7）、RFC 4122（UUID v4）。

## ✨ 核心特性

- 🪪 **ULID**：26 字符 Crockford Base32，字典序 == 时间序，大小写容错解析。
- 🕒 **UUID v7**：RFC 9562，48 位毫秒时间戳 + 随机，时间可排序。
- 🎲 **UUID v4**：RFC 4122 随机版本，带版本/变体位校验。
- ⛓️ **单调模式**：ULID 在同毫秒内严格递增，杜绝乱序。
- 🔎 **解析与校验**：`parse` 自动识别类型并还原时间戳；`validate` 校验合法性。
- 🔌 **可管道化**：CLI 支持批量生成与 JSON 友好的纯文本输出，便于 CI / Agent 集成。
- 📦 **零依赖**：仅需 Python 3.8+ 标准库，无 `pip install` 负担。

## 🚀 快速开始

**环境要求**：Python 3.8 及以上（仅需标准库）。

**方式一 · 源码直接运行（推荐零依赖体验）**
```bash
git clone https://github.com/gitstq/IdForge.git
cd IdForge
python3 -m idforge ulid
```

**方式二 · 作为库安装**
```bash
pip install idforge
idforge uuid7
```

**本地启动 / 一键运行**
```bash
python3 -m idforge uuid7                 # 生成一个 UUID v7
python3 -m idforge ulid --count 5        # 批量生成 5 个 ULID
python3 -m idforge ulid --monotonic      # 单调模式
python3 -m idforge parse 01M6RTKHBT02... # 识别类型并还原时间戳
```

## 📖 详细使用指南

### 作为库调用
```python
from idforge import ulid, uuid7, uuid4

u, (ms, _) = ulid()        # 返回 (字符串, (时间戳ms, 随机熵))
print(u, ms)
print(uuid7())              # RFC 9562 时间可排序 UUID
print(uuid4())              # RFC 4122 随机 UUID
```

### `ulid` —— 生成 ULID
```bash
idforge ulid                 # 单个
idforge ulid --count 10      # 批量
idforge ulid --monotonic     # 单调（同毫秒内严格递增）
```

### `uuid7` / `uuid4` —— 生成 UUID
```bash
idforge uuid7 --count 3
idforge uuid4
```

### `parse` —— 识别 ID 类型并还原时间戳
```bash
idforge parse 01M6RTKHBT02R52BXA2ES679CH
# type : ULID
# time : 1793982035172 ms  (2026-11-06 16:20:35 UTC)

idforge parse 018F6C2A-9B1A-7C3D-8F2E-0123456789AB
# type : UUIDv7
# time : 1715506682650 ms  (2024-05-12 09:38:02 UTC)
```

### 典型使用场景
- **数据库主键**：用 UUID v7 / ULID 替代自增 ID，避免暴露规模且保持索引局部性。
- **日志链路追踪**：用 ULID 作为 trace-id，按字典序即可按时间排序检索。
- **Agent 工具**：批量生成唯一标识供工具链消费，纯文本输出可直接管道化。

## 💡 设计思路与迭代规划

**设计理念**：唯一 ID 应当**规范兼容、可排序、零依赖**。相比需要中心服务（Snowflake）或重依赖的库，IdForge 用纯标准库覆盖最常用的三种方案。

**技术选型原因**：纯标准库（`secrets` / `time` / `argparse`）保证零安装成本、零供应链风险、可在任意受限/离线环境运行。

**后续迭代计划**：
1. 增加 UUID v8（自定义布局）实验性支持。
2. 增加 `idforge bench` 吞吐量基准与单调性压测。
3. 提供 `idforge sql` 输出可直接用于建表（如 PostgreSQL `uuid` / `char(26)`）。
4. 增加更严格的可配置单调性（带节点 ID 防冲突）。

**社区贡献方向**：更多语言翻译、规范向量补齐、性能优化。

## 📦 打包与部署指南

IdForge 属于**工具/库类**项目，无需上传跨平台二进制 Release。

- **作为 Python 库分发**：`pip install idforge`（见 `pyproject.toml`，暴露 `idforge` 命令行入口）。
- **作为源码嵌入**：直接复制 `idforge/` 包到你的项目，`import idforge` 即可，无任何依赖。
- **容器化**：基于 `python:3.8-slim` 即可，`COPY` 源码后 `python3 -m idforge`。
- **兼容环境**：Python 3.8 / 3.9 / 3.10 / 3.11 / 3.12，Windows / macOS / Linux 均验证可用。

## 🤝 贡献指南

欢迎通过 Issue 与 Pull Request 参与。提交请遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范（`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`）。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前请运行：

```bash
python3 -m unittest discover -s tests
```

## 📄 开源协议说明

本项目以 **MIT 协议** 开源。你可以自由使用、修改、分发，包括商业用途，但需保留版权声明。详见 [LICENSE](LICENSE)。

</details>

---

<details>
<summary><b>🇹🇼 繁體中文</b></summary>

## 🎉 專案介紹

**IdForge** 定位為「開箱即用的唯一 ID 工廠」。它在分散式系統、資料庫主鍵、事件溯源、日誌鏈路追蹤與 AI Agent 工具鏈等場景中，解決一個共同痛點：**如何在不引入任何依賴、不依賴資料庫/中心服務的前提下，產生全域唯一且可按時間排序的 ID**。

- **核心價值**：單檔即可嵌入；輸出符合公開規範（ULID / RFC 9562 / RFC 4122），可被任意語言解析；時間可排序，天然適合作為資料庫主鍵與索引。
- **解決痛點**：傳統自增 ID 暴露規模、UUID v4 不可排序導致索引碎片化、第三方 Snowflake 函式庫又重又依賴網路。IdForge 用純標準函式庫一次解決。
- **自研差異化亮點**：
  - 同時支援 **ULID / UUIDv7 / UUIDv4** 三種語意，統一 API；
  - ULID 提供 **單調產生（monotonic）** 模式，避免同毫秒內的時鐘回撥/亂序；
  - 內建 `parse` 指令可**反解 ID 類型與建立時間戳**，便於排障；
  - 密碼學安全隨機源（`secrets`），無隨機數品質隱患。
- **靈感來源**：ULID 規範、RFC 9562（UUID v7）、RFC 4122（UUID v4）。

## ✨ 核心特性

- 🪪 **ULID**：26 字元 Crockford Base32，字典序 == 時間序，大小寫容錯解析。
- 🕒 **UUID v7**：RFC 9562，48 位毫秒時間戳 + 隨機，時間可排序。
- 🎲 **UUID v4**：RFC 4122 隨機版本，帶版本/變體位校驗。
- ⛓️ **單調模式**：ULID 在同毫秒內嚴格遞增，杜絕亂序。
- 🔎 **解析與校驗**：`parse` 自動識別類型並還原時間戳；`validate` 校驗合法性。
- 🔌 **可管線化**：CLI 支援批次產生與 JSON 友好的純文字輸出，便於 CI / Agent 整合。
- 📦 **零依賴**：僅需 Python 3.8+ 標準函式庫，無 `pip install` 負擔。

## 🚀 快速開始

**環境要求**：Python 3.8 及以上（僅需標準函式庫）。

**方式一 · 原始碼直接執行**
```bash
git clone https://github.com/gitstq/IdForge.git
cd IdForge
python3 -m idforge ulid
```

**方式二 · 作為函式庫安裝**
```bash
pip install idforge
idforge uuid7
```

**本地啟動 / 一鍵執行**
```bash
python3 -m idforge uuid7
python3 -m idforge ulid --count 5
python3 -m idforge ulid --monotonic
python3 -m idforge parse 01M6RTKHBT02...
```

## 📖 詳細使用指南

### 作為函式庫呼叫
```python
from idforge import ulid, uuid7, uuid4
u, (ms, _) = ulid()
print(u, ms)
print(uuid7())
print(uuid4())
```

### `ulid` / `uuid7` / `uuid4` / `parse`
```bash
idforge ulid --count 10
idforge ulid --monotonic
idforge uuid7 --count 3
idforge parse 01M6RTKHBT02R52BXA2ES679CH
```

### 典型使用場景
- **資料庫主鍵**：用 UUID v7 / ULID 替代自增 ID，避免暴露規模且保持索引區域性。
- **日誌鏈路追蹤**：用 ULID 作為 trace-id，按字典序即可按時間排序檢索。
- **Agent 工具**：批次產生唯一標識供工具鏈消費。

## 💡 設計思路與迭代規劃

**設計理念**：唯一 ID 應當**規範相容、可排序、零依賴**。

**技術選型原因**：純標準函式庫確保零安裝成本、零供應鏈風險、可離線執行。

**後續迭代計畫**：
1. 增加 UUID v8（自訂佈局）實驗性支援。
2. 增加 `idforge bench` 吞吐量基準與單調性壓測。
3. 提供 `idforge sql` 輸出可直接用於建表。
4. 增加更嚴格的可設定單調性（帶節點 ID 防衝突）。

**社群貢獻方向**：更多語言翻譯、規範向量補齊、效能優化。

## 📦 打包與部署指南

IdForge 屬於**工具/函式庫類**專案，無需上傳跨平台二進位 Release。

- **作為 Python 函式庫分發**：`pip install idforge`。
- **作為原始碼嵌入**：直接複製 `idforge/` 套件，`import idforge` 即可，無任何依賴。
- **容器化**：基於 `python:3.8-slim` 即可。
- **相容環境**：Python 3.8 ~ 3.12，Windows / macOS / Linux 均驗證可用。

## 🤝 貢獻指南

歡迎透過 Issue 與 Pull Request 參與，請遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範。詳見 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前請執行：

```bash
python3 -m unittest discover -s tests
```

## 📄 開源協議說明

本專案以 **MIT 協議** 開源，可自由使用、修改、散佈（含商業用途），但須保留版權聲明。詳見 [LICENSE](LICENSE)。

</details>

---

<details>
<summary><b>🇺🇸 English</b></summary>

## 🎉 Introduction

**IdForge** is an "out-of-the-box unique ID factory". It solves a shared pain point across distributed systems, database primary keys, event sourcing, log trace correlation, and AI-Agent toolchains: **how to generate globally unique, time-sortable IDs without any dependency and without a database / central service**.

- **Core value**: a single embeddable package; outputs conform to public specs (ULID / RFC 9562 / RFC 4122) and are parseable from any language; time-sortable, ideal as DB keys and indexes.
- **Problem solved**: auto-increment IDs leak scale; UUID v4 is non-sortable (index fragmentation); third-party Snowflake libs are heavy and network-dependent. IdForge solves all three with pure stdlib.
- **Self-developed differentiators**:
  - Unified API for **ULID / UUIDv7 / UUIDv4**;
  - ULID **monotonic** mode prevents out-of-order IDs within the same millisecond;
  - Built-in `parse` **detects the type and recovers the creation timestamp** for debugging;
  - Cryptographically secure randomness (`secrets`), no RNG-quality concerns.
- **Inspiration**: ULID spec, RFC 9562 (UUID v7), RFC 4122 (UUID v4).

## ✨ Core Features

- 🪪 **ULID**: 26-char Crockford Base32, lexicographic == chronological, case-tolerant parsing.
- 🕒 **UUID v7**: RFC 9562, 48-bit ms timestamp + random, time-sortable.
- 🎲 **UUID v4**: RFC 4122 random version with version/variant validation.
- ⛓️ **Monotonic mode**: ULID strictly increases within the same millisecond.
- 🔎 **Parse & validate**: `parse` auto-detects type and recovers timestamp; `validate` checks legality.
- 🔌 **Pipe-friendly**: batch generation and plain-text output for CI / Agent integration.
- 📦 **Zero dependency**: only Python 3.8+ standard library, no `pip install` overhead.

## 🚀 Quick Start

**Requirements**: Python 3.8+ (standard library only).

**Option 1 · Run from source**
```bash
git clone https://github.com/gitstq/IdForge.git
cd IdForge
python3 -m idforge ulid
```

**Option 2 · Install as a library**
```bash
pip install idforge
idforge uuid7
```

**Run locally**
```bash
python3 -m idforge uuid7
python3 -m idforge ulid --count 5
python3 -m idforge ulid --monotonic
python3 -m idforge parse 01M6RTKHBT02...
```

## 📖 Detailed Usage

### As a library
```python
from idforge import ulid, uuid7, uuid4
u, (ms, _) = ulid()
print(u, ms)
print(uuid7())
print(uuid4())
```

### CLI
```bash
idforge ulid --count 10
idforge ulid --monotonic
idforge uuid7 --count 3
idforge parse 01M6RTKHBT02R52BXA2ES679CH
# type : ULID
# time : 1793982035172 ms  (2026-11-06 16:20:35 UTC)
```

### Typical scenarios
- **DB primary keys**: UUID v7 / ULID instead of auto-increment — no scale leakage, better index locality.
- **Log trace IDs**: ULID as trace-id; lexicographic order == time order.
- **Agent tooling**: batch-generate unique IDs for pipelines; plain-text output pipes cleanly.

## 💡 Design & Roadmap

**Design philosophy**: unique IDs should be **spec-compatible, sortable, and zero-dependency**.

**Why stdlib only**: zero install cost, zero supply-chain risk, runs in any restricted/offline environment.

**Roadmap**:
1. Experimental UUID v8 (custom layout) support.
2. `idforge bench` throughput baseline and monotonic stress test.
3. `idforge sql` output for table creation (PostgreSQL `uuid` / `char(26)`).
4. Configurable monotonicity with node IDs to prevent collisions.

**Community directions**: more translations, spec test vectors, performance tuning.

## 📦 Packaging & Deployment

IdForge is a **tool/library** project — no cross-platform binary Release required.

- **As a PyPI library**: `pip install idforge` (exposes the `idforge` console script).
- **Embed from source**: copy the `idforge/` package and `import idforge`; no dependencies.
- **Container**: base on `python:3.8-slim`, `COPY` source, then `python3 -m idforge`.
- **Compatibility**: Python 3.8–3.12 on Windows / macOS / Linux (verified).

## 🤝 Contributing

Issues and PRs are welcome. Please follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`). See [CONTRIBUTING.md](CONTRIBUTING.md). Before submitting:

```bash
python3 -m unittest discover -s tests
```

## 📄 License

Released under the **MIT License** — free to use, modify, and distribute, including commercially, provided the copyright notice is retained. See [LICENSE](LICENSE).

</details>
