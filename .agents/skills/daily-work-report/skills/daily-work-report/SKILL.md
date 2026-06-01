---
name: Daily Work Report
description: >
  This skill should be used when the user asks to "生成工作日报", "整理今天的工作",
  "输出工作日志", "写工作日记", "复盘今天的工作", "daily standup", "daily report",
  "工作日报", "日报", "工作日志", or wants to compile a structured summary of work
  done in a specified day. Automatically collects context from memory files, project
  directories, and file change history to produce a comprehensive work diary.
version: 0.1.0
---

# Daily Work Report

## Overview

Generate a structured daily work diary by automatically collecting context from multiple sources: Claude Code memory files, project directory changes, and file modification timestamps. The output is a comprehensive Markdown report covering what was done, strategic insights, quality assessments, and future directions.

## When to Use

Trigger this skill whenever the user requests a daily work summary, diary, or report. The skill handles date ranges (single day, multi-day, or date range) and can target specific project directories or scan all projects.

## Workflow

### Step 1: Determine Scope

Clarify the report scope before collecting data:

1. **Target date**: Default to today. Parse user input for specific dates (e.g., "昨天", "5月6日", "2026-05-06").
2. **Working directory**: Default to current directory. User may specify a different root.
3. **Report type**: Full report (default) or brief summary.

### Step 2: Collect Context Sources

Gather information from four parallel channels. Execute these in parallel where possible.

#### Channel A: Memory Files

Scan Claude Code project memory directories:

```
~/.claude/projects/*/memory/MEMORY.md          → Index of all memories
~/.claude/projects/*/memory/*.md                → Individual memory files
```

Filter to files modified on or referencing the target date. Extract:
- Project context and background
- Strategic decisions made
- Key insights and pivots
- Feedback and lessons learned

#### Channel B: Sub-project Memory

Scan sub-projects within the working directory:

```
<workdir>/*/.claude/projects/*/memory/*.md      → Sub-project memories
```

Also check for CLAUDE.md files in sub-projects:
```
<workdir>/*/CLAUDE.md                           → Project-level instructions
```

#### Channel C: File Changes

Detect what was actually produced on the target date:

```bash
find <workdir> -type f -newermt "<target_date>" ! -newermt "<target_date+1>" \
  -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/.claude/*"
```

Categorize changes by type:
- **Documents** (.md, .docx, .pdf): New proposals, analyses, reports
- **Code** (.py, .js, .ts, .go): Implementation work
- **Data** (.json, .csv, .xlsx): Data processing outputs
- **Config** (.yaml, .json, .toml): Configuration changes

#### Channel D: Existing Work Diaries

Check for previously written diaries to avoid duplication and build continuity:

```
<workdir>/工作日记/工作日记_YYYYMMDD.md
```

If a diary exists for the target date, read it and treat as a base to extend rather than overwrite.

### Step 3: Analyze and Structure

Organize collected information into a structured report. Follow the template in `references/report-template.md` for section ordering and formatting.

#### Section Priority

1. **Work Activities** — Chronological listing of what was done (factual)
2. **Quality Assessment** — Evaluate outputs produced (if any code/reports were generated)
3. **Strategic Insights** — Decisions, pivots, and reflections
4. **Competitive Intelligence** — Any competitor or market research conducted
5. **Output Summary** — Files produced, documents written
6. **Retrospective** — What went well, what to improve, next steps

#### Quality Assessment Criteria

When evaluating produced outputs (reports, code, data), assess on these dimensions:

| Dimension | Criteria |
|-----------|----------|
| Completeness | Does it cover the intended scope? What's missing? |
| Accuracy | Do data points match source material? |
| Depth | Surface description vs. actionable insight |
| Actionability | Can the reader take immediate action from this? |
| Gaps | What would make this significantly more valuable? |

### Step 4: Generate Report

Write the final report to:

```
<workdir>/工作日记/工作日记_YYYYMMDD.md
```

Create the 工作日记 directory if it does not exist.

#### Writing Guidelines

- Use **objective, factual tone** — describe what happened, not what should have happened
- Include **specific numbers** — file counts, data volumes, time estimates
- Preserve **the user's own strategic language** — if the user expressed an insight in their own words, quote or paraphrase faithfully
- Avoid **inflation** — don't pad the report; if only 2 things were done, write 2 things
- Mark **incomplete or speculative items** clearly

### Step 5: Update Obsidian Knowledge Graph

After generating the diary, enhance the `工作日记/` directory with Obsidian wiki-links and concept notes to build a navigable knowledge graph.

#### 5.1 Add YAML Frontmatter to Diary

Prepend YAML frontmatter to the generated diary file:

```yaml
---
date: YYYY-MM-DD
tags: [工作日记, tag1, tag2, ...]
type: daily-report
---
```

Tags should reflect the diary's key themes. Common tags: `竞品分析`, `产品开发`, `战略思考`, `技术方案`, `定价研究`, etc.

#### 5.2 Add Wiki-Links to Diary Content

Convert the **first or most significant mention** of each key entity into an Obsidian `[[]]` wiki-link. Do not link every occurrence — only the primary reference in each section.

**Entity categories to link:**

| Category | Examples | How to identify |
|----------|----------|-----------------|
| Products/Projects | `[[观潮 BidWatcher]]` | Product names mentioned as work items |
| Competitors | `[[千里马]]`, `[[RCC瑞达恒]]` | Named competitors in analysis |
| Strategic Concepts | `[[报童模型]]`, `[[三层商业模型]]` | Frameworks, mental models, key insights |
| Technical Capabilities | `[[M0-M9 模块化提取]]` | Named technical features or architectures |
| Milestones | `[[最小验证]]` | Named project phases or validation stages |
| Core Insights | `[[多维交叉预测]]` | Major insights marked as "重大收获" or "核心洞察" |

**Linking rules:**
- Use `[[Entity Name]]` for exact links
- Use `[[Entity Name\|display text]]` when the link text differs from the note title (e.g., `[[观潮 BidWatcher\|观潮]]`)
- Use `[[Entity Name\|context]]` for alias references (e.g., `[[报童模型\|报童]]`)
- Only link the first meaningful mention per section, not every occurrence

#### 5.3 Create or Update Concept Notes

For each entity linked in the diary, check if a corresponding note exists in `工作日记/`. If not, create it. If yes, update it.

**Concept note template:**

```markdown
---
tags: [concept-type]
aliases: [alternative names]
---

# Entity Name

One-line definition.

## Key Points
- Point 1
- Point 2

## Related Concepts
- [[Related Concept A]]
- [[Related Concept B]]

## 提及日记
- [[工作日记_YYYYMMDD]] — brief context of mention
```

**Tag categories for concept notes:**

| Tag | Usage |
|-----|-------|
| `产品` | Products and projects |
| `竞品` | Competitor entities |
| `战略概念` | Business models, frameworks, strategic insights |
| `技术能力` | Technical features, architectures |
| `里程碑` | Project phases, validation stages |
| `核心洞察` | Major breakthrough insights |

**Update rules for existing concept notes:**
- Append new diary reference to the `## 提及日记` section
- Do NOT overwrite existing content — only add new information
- If the concept itself has evolved (e.g., product repositioned), add a new line to the relevant section rather than replacing the old one

#### 5.4 Concept Note Discovery

To find existing concept notes that should be linked from the new diary:

1. Read all `*.md` files in `工作日记/` that are NOT diary files (i.e., not matching `工作日记_YYYYMMDD.md`)
2. Each such file represents a concept node in the graph
3. If the new diary mentions a concept that has an existing note, link to it
4. If the new diary introduces a concept that appears in 2+ diaries or is flagged as significant, create a new note

### Step 6: Update Memory

If the report reveals new strategic insights, project decisions, or user preferences not yet captured in memory, offer to save them to the appropriate memory file.

## Additional Resources

### Reference Files

- **`references/report-template.md`** — Full report structure template with section examples

### Scripts

- **`scripts/collect-context.py`** — Cross-platform utility script (Python 3.6+, no dependencies) to collect file changes and memory data for a given date. Preferred on all platforms.
- **`scripts/collect-context.sh`** — Bash utility script for Linux/Git Bash environments. Requires GNU find (`-newermt`). Not compatible with macOS BSD find.

#### Script Usage

```bash
# Python (recommended, cross-platform)
python scripts/collect-context.py 2026-05-08 /path/to/workspace

# Bash (Linux / Git Bash only)
bash scripts/collect-context.sh 2026-05-08 /path/to/workspace
```

### Examples

Refer to `references/report-template.md` for complete section examples with sample content.
