# 贡献指南 / Contributing

感谢你关注 **IdForge**！本项目遵循以下协作规范。

## 🐛 问题反馈（Issue）
- 提交前请先检索是否已有相同或类似问题。
- 请清晰描述：复现步骤、期望行为、实际行为、Python 版本与操作系统。

## 🔧 提交规范（Pull Request）
本仓库采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 前缀 | 含义 |
| --- | --- |
| `feat:` | 新增功能 |
| `fix:` | 修复问题 |
| `docs:` | 文档更新 |
| `refactor:` | 代码重构 |
| `test:` | 新增/修改测试 |
| `chore:` | 构建/工程化调整 |

示例：
```
feat: 增加 UUIDv8 实验性支持
fix: 修复 ULID 单调模式跨毫秒溢出处理
```

## ✅ 开发自检
- 本仓库**零第三方依赖**，仅需 Python 3.8+。
- 提交前请运行测试：
  ```bash
  python3 -m unittest discover -s tests
  ```
- 代码风格遵循 PEP 8，保持注释清晰、无冗余。

## 📜 协议
提交即代表你同意以 **MIT 协议** 发布你的贡献。
