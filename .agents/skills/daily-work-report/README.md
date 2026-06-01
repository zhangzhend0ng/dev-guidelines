# 工作日报生成器（Daily Work Report）

一个 Claude Code Skill，自动从多数据源收集上下文信息，生成结构化的每日工作日记。

## 功能特性

- **多源上下文采集**：从 Claude Code 记忆文件、子项目记忆、文件变更历史、Git 提交记录中收集信息
- **结构化输出**：生成格式一致的 Markdown 工作日记
- **质量评估**：自动检测并评估产出物（报告、代码、数据）的质量
- **复盘支持**：内置战略反思和下一步规划模板
- **去重续写**：读取已有日记进行扩展而非覆盖
- **Obsidian 知识图谱**：自动添加 YAML frontmatter、`[[]]` 双链、创建/更新概念笔记，构建可导航的工作知识图谱
- **跨平台**：支持 Windows / macOS / Linux

## 目录结构

```
daily-work-report/
├── SKILL.md                       # Skill 定义与工作流说明
├── README.md                      # 本文件
├── references/
│   └── report-template.md         # 报告结构模板（含各章节说明与示例）
└── scripts/
    ├── collect-context.py         # 上下文采集脚本（跨平台，推荐）
    └── collect-context.sh         # 上下文采集脚本（Bash，GNU find 依赖）
```

## 使用方法

在 Claude Code 中通过以下方式触发：

- "整理今天的工作"
- "生成工作日报"
- "输出工作日志"
- "写工作日记"
- "复盘今天的工作"
- "daily report"

Skill 会自动执行以下步骤：

1. **确定范围**：目标日期（默认今天）、工作目录（默认当前目录）
2. **四通道采集**：记忆文件 → 子项目记忆 → 文件变更 → 已有日记
3. **分析结构化**：工作内容 → 产出评估 → 战略思考 → 总结
4. **生成报告**：输出到 `工作日记/工作日记_YYYYMMDD.md`
5. **更新 Obsidian 知识图谱**：添加 frontmatter + 双链 + 创建/更新概念笔记
6. **更新记忆**：如有新洞察，建议保存到记忆文件

## 脚本工具

### Python 版（推荐，跨平台）

```bash
python scripts/collect-context.py 2026-05-08 /path/to/workspace
```

输出内容包括：
- 指定日期修改的记忆文件
- 子项目 .claude 目录
- 指定日期变更的文件（按类型分类：DOC/CODE/DATA/CONFIG）
- 已有的工作日记
- 指定日期的 Git 提交记录

**依赖**：Python 3.6+（无第三方依赖）

### Bash 版（Linux / Git Bash）

```bash
bash scripts/collect-context.sh 2026-05-08 /path/to/workspace
```

**限制**：依赖 GNU find（`-newermt` 参数），macOS 原生 BSD find 不支持，建议使用 Python 版。

## 报告结构

默认报告包含以下章节（按需调整）：

| 章节 | 说明 | 必选 |
|------|------|------|
| 工作内容 | 按时间顺序记录当日工作项 | 是 |
| 产出物评估 | 对代码/报告/数据的质量评估 | 有产出时 |
| 战略思考 | 决策、方向判断、洞察记录 | 有讨论时 |
| 文档产出 | 当天创建或修改的文档清单 | 有产出时 |
| 工作量总结 | 按类别汇总 | 是 |
| 总结 | 1-3条核心收获 | 是 |
| 复盘思考 | 不足反思、自检标准、后续方向 | 可选 |

详细模板见 `references/report-template.md`。

## Obsidian 知识图谱集成

生成日记后，Skill 会自动执行以下 Obsidian 增强操作：

### 5.1 YAML Frontmatter

每篇日记自动添加日期、标签、类型等元数据，便于 Obsidian 搜索和筛选。

### 5.2 双向链接（Wiki-Links）

将日记中的关键实体转为 `[[]]` 链接，覆盖 6 类实体：

| 类别 | 示例 | Tag |
|------|------|-----|
| 产品/项目 | `[[MyProduct]]` | `产品` |
| 竞品 | `[[CompetitorA]]` | `竞品` |
| 战略概念 | `[[商业模式A]]` | `战略概念` |
| 技术能力 | `[[FeatureX]]` | `技术能力` |
| 里程碑 | `[[MVP验证]]` | `里程碑` |
| 核心洞察 | `[[关键认知]]` | `核心洞察` |

### 5.3 概念笔记

每个被链接的实体会自动创建或更新对应的 Markdown 笔记，包含定义、关联概念和提及日记列表。概念笔记存放在 `工作日记/` 目录下，与日记文件并列，Obsidian Graph View 中会形成星形网络结构。

### 效果示例

```
                  CompetitorA ────────┐
                      │               │
日记_Day1 ────── MyProduct ─────── 日记_Day3
                      │               │
日记_Day2 ────── 商业模型A         日记_Day4
                      │                │
               战略概念B           核心洞察C
```

## 跨平台兼容性

| 平台 | Python 脚本 | Bash 脚本 | Claude Code 集成 |
|------|------------|-----------|-----------------|
| Windows | 支持 | 需 Git Bash | 支持 |
| macOS | 支持 | 需 GNU find | 支持 |
| Linux | 支持 | 支持 | 支持 |

## 系统要求

- Claude Code（支持 Skill）
- Python 3.6+（推荐，用于采集脚本）
- Git（可选，用于提交历史收集）

## 许可证

MIT
