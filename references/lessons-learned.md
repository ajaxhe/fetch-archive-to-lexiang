# 自省日志（Lessons Learned）

> 本文件是 fetch-archive-to-lexiang skill 的「组织记忆」。
> 每次用户指出错误、发现遗漏、或 Agent 自查发现问题后，**必须**将教训沉淀到此文件。
> Agent 在每次执行任务前**必须**读取此文件，避免重蹈覆辙。

---

## 📋 教训索引（按严重性排序）

### 🔴 P0 — 反复犯过的严重错误（必须彻底杜绝）

#### L001: 图片遗漏（2026-06-04, 2026-06-15 多次发生）
- **问题**：使用 `WebFetch` 抓取文章后直接翻译上传，完全忽略了原文中的配图
- **根因**：Agent 走了「省事路径」——WebFetch 返回纯文本，Agent 没有意识到原文有图片就直接进入翻译和上传流程
- **正确做法**：
  1. 抓取前先用 WebFetch 快速扫描原文，**明确记录图片数量**
  2. 如果有图片 → **必须**用 `fetch_article.py` 抓取（下载图片到 images/）
  3. 如果 `fetch_article.py` 因沙箱限制无法运行 → 手动用 curl 下载每张图片
  4. 上传时必须用 `md_to_page.py` 或 MCP 三步图片上传流程
  5. **禁止**在有图片的文章中使用 `entry_import_content` 纯文本导入
- **自检项**：上传完成后，用 `block_list_block_children` 检查是否存在 `block_type: "image"` 且有 `file_id` 的 block

#### L002: WebFetch 被当作万能抓取工具
- **问题**：Agent 倾向于用 WebFetch 获取文章内容并直接使用，跳过 `fetch_article.py`
- **根因**：WebFetch 调用简单、响应快，Agent 选择了阻力最小的路径
- **正确做法**：WebFetch **只能用于初步侦察**（判断文章语言、有无图片、大致结构），**不能作为正式抓取工具**。正式抓取必须用 `fetch_article.py`
- **例外**：纯文本无图片且不需要登录的文章，才可以用 WebFetch 的内容直接导入

### 🟡 P1 — 偶尔犯的错误（需要注意）

#### L003: 翻译时丢失图片占位符
- **问题**：翻译英文文章为中英对照时，原文中的 `![](images/xxx)` 图片引用被翻译过程吃掉了
- **正确做法**：翻译时必须保留所有 `![](...)` 引用不动，或翻译完成后用锚点匹配重新插入

#### L004: 知识库配置不匹配
- **问题**：config.json 中的"贾维斯"知识库在当前 MCP 账号下不可用，导致 API 报错
- **正确做法**：优先使用用户记忆中的目标知识库（ajaxhe的个人知识库），config.json 作为 fallback

### 🟡 P1 — 偶尔犯的错误（需要注意）

#### L007: 沙箱环境下 fetch_article.py 降级方案实操（2026-06-18 验证）
- **问题**：WorkBuddy/Cursor 沙箱阻止访问 `~/.fetch_article`，fetch_article.py CDP 模式无法创建 profile 目录；且 managed python venv 无 playwright/chromium
- **降级路径**（L001 认可的方案，本次完整跑通）：
  1. `curl -sL -A "<UA>" "<URL>" -o raw.html` 抓取完整 HTML（Substack 免费文章可达）
  2. grep 统计 `<img` 和 substack-post-media 图片 URL，确认图片数量
  3. `curl` 逐张下载正文图片到 `images/`（用 s3 原图 URL，排除头像/图标）
  4. python(bs4+html2text) 解析 `<div class="body markup">` 提取正文，按 s3 图片 ID 映射 `<img src>` 到本地路径
  5. 生成中英对照 markdown（图片引用 `![](images/xxx)`）
  6. 纯文字版（图片引用替换为 `[图片: xxx]` 占位）用 `entry_import_content` 一次性导入
  7. `block_list_block_children` 定位占位 block 的 index
  8. **从后往前**逐张：`block_apply_block_attachment_upload` → `curl PUT` 上传 → `block_create_block_descendant(index="占位index+1")` → `block_delete_block(占位block_id)`
- **关键技巧**：
  - 删除占位用 `block_id`（不依赖 index），插入图片用 `index`（基于推算）。两者区域不重叠时可并行
  - 从后往前处理，避免前面插入/删除影响后面的 index
  - `bs4` 用内置 `html.parser`，不需要 `lxml`；`html2text` 转 markdown 保留图片位置

### 🟢 P2 — 已修复的小问题（备忘）

#### L005: `after=""` 不是置顶
- **问题**：API 文档说 `after=""` 会排到最前面，实际是排到最后面
- **修复**：必须用 `before=<第一个条目ID>` 来置顶

#### L006: block_create_block_descendant 的 index 参数必须是字符串
- **问题**：传整数 `index: 81` 会参数校验失败
- **修复**：传字符串 `index: "81"`

---

## 🔄 规则演化记录

| 日期 | 触发事件 | 新增/修改的规则 | 影响范围 |
|------|----------|----------------|----------|
| 2026-06-03 | 首次图片上传失败 | 新增核心规则#5「图片不可丢失」 | SKILL.md |
| 2026-06-04 | baoyu.io 文章沙箱限制 | 新增 curl+HTML 解析组合方案 | tips-experience.md |
| 2026-06-04 | after="" 排序问题 | 修正置顶逻辑为 before 参数 | SKILL.md |
| 2026-06-09 | 新增原文链接保留要求 | 新增核心规则#2「原文链接必须保留」 | SKILL.md |
| 2026-06-15 | Every.to 文章图片遗漏 | 新增预检步骤、自检清单、自省机制 | SKILL.md, lessons-learned.md |

---

## 📝 如何更新此文件

Agent 在以下时机**必须**更新此文件：

1. **用户指出错误后**：立即将错误、根因、正确做法记录为新的 Lesson
2. **自查发现问题后**：同上
3. **成功应用新技巧后**：如果是值得复用的新做法，记录到规则演化表
4. **模型/API 行为变化后**：如果发现之前的做法不再适用，更新对应 Lesson

格式要求：
- 每条 Lesson 必须包含：问题描述、根因分析、正确做法
- 按严重性分级：🔴 P0（反复犯的）、🟡 P1（偶尔犯的）、🟢 P2（已修复的）
- P0 教训对应的自检项必须同步更新到 SKILL.md 的自检清单中
