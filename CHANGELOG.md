# Changelog

All notable changes to this project are documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [1.0.0] - 2026-11-07

### Added
- 纯 Python 标准库实现的**可排序唯一 ID 生成引擎**，零第三方依赖、完全离线。
- **ULID**：26 字符 Crockford Base32，时间可排序，支持单调生成（monotonic）与解析/校验。
- **UUID v7**：RFC 9562 实现，48 位毫秒时间戳 + 随机，时间可排序、可解析。
- **UUID v4**：RFC 4122 随机版本，带版本/变体位校验。
- 命令行工具 `idforge`：`ulid` / `uuid7` / `uuid4` / `parse` 子命令，支持批量生成与类型识别、时间戳还原。
- 完整中文（简/繁）与英文三语文档。
