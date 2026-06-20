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

#### L003: 翻译时丢失图片语法（🚨 升级为 P0，2026-06-20 严重后果验证）
- **问题**：翻译英文文章为中英对照时，原文中的 `![](images/xxx)` 图片引用被替换为 `[IMG_PLACEHOLDER_N]` 非标准占位符
- **根因**：Agent 翻译时认为占位符更"整洁"，没有意识到 `md_to_page.py` 依赖 `![](...)` 语法来拆分文本段和图片段
- **后果链路**：占位符 → `md_to_page.py` 无法识别图片 → 被迫走 MCP「先全文后补图」手动定位 → `block_create_block_descendant` 的 index 不等于 block_list 位置 → 图片反复错位 → 需要多轮 trial-and-error 修复
- **正确做法**：
  1. 翻译时**必须原样保留** `![alt](images/xxx)` 图片引用，不得替换为任何非标准格式
  2. alt 文本可翻译为双语（如 `![Zone of Genius / 天才区域框架](images/img_03_xxx.png)`）
  3. 图片引用放在对应段落的上方或下方，确保图文对应关系不丢失
  4. 只有这样 `md_to_page.py` 才能自动拆分文本段和图片段，实现一步到位
- **自检项**：翻译完成后，grep 检查 `!\[.*\]\(images/` 出现次数是否等于原文图片数；如果发现 `[IMG_PLACEHOLDER]` 格式 → 立即修正

#### L004: 知识库配置不匹配
- **问题**：config.json 中的"贾维斯"知识库在当前 MCP 账号下不可用，导致 API 报错
- **正确做法**：优先使用用户记忆中的目标知识库，config.json 作为 fallback

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

#### L008: WorkBuddy MCP 工具调用 params 字段丢失（2026-06-19 首次遇到）
- **问题**：在 WorkBuddy 会话中通过 DeferExecuteTool 调用 mcp__lexiang__* 工具时，**有参工具**（如 entry_list_children / entry_create_entry / entry_import_content）反复返回 `validation error: <field> is required`，但**无参工具**（whoami / space_list_recently_spaces / team_list_teams）正常工作
- **直接 curl 调用**也失败：MCP 端点 `https://mcp.lexiang-app.com/mcp` 报 401 invalid_token；本地存储的 token（WorkBuddy 连接器 token 文件路径）已过期 11 小时，WorkBuddy 内部有自动刷新机制但**不会暴露 refresh_token 给 Agent**
- **触发场景推测**：
  - 同一会话中前序工具调用较多 + 后续 MCP 工具调用有 params 时
  - 可能与 DeferExecuteTool 在多轮调用中的 JSON 序列化有关
- **临时绕行方案**：
  1. **首选**：在新会话中执行上传操作（短上下文）
  2. **次选**：将准备好的 markdown + images 落到工作区，由用户手动上传
  3. **未来方案**：写一个 fetch-archive skill 的配套脚本（`upload_to_lexiang.py`），通过 `requests` 直接调用 MCP 端点 + 处理 OAuth 刷新
- **自检项**：调用前先用 `whoami` 测试 MCP 是否通；如果 whoami 通但 entry_list_children 仍报"parent_id required"，基本可确认是 L008 问题

### 🟢 P2 — 已修复的小问题（备忘）

#### L005: `after=""` 不是置顶
- **问题**：API 文档说 `after=""` 会排到最前面，实际是排到最后面
- **修复**：必须用 `before=<第一个条目ID>` 来置顶

#### L006: block_create_block_descendant 的 index 参数必须是字符串
- **问题**：传整数 `index: 81` 会参数校验失败
- **修复**：传字符串 `index: "81"`

#### L009: block_create_block_descendant 的 index 不等于 block_list 位置（2026-06-20 两次实战验证）
- **问题**：手动用 `block_create_block_descendant` 在特定位置插入图片时，index 参数不等于 `block_list_block_children` 返回的直接子节点位置（0-based），导致图片反复插入到错误位置（嵌套进 quote/callout 容器块内，或出现在不相关的段落之间）
- **根因**：乐享 API 的 index 使用包含嵌套子节点的**扁平索引系统**——quote/callout/toggle 等容器块的 children 也被计入 flat index
- **经验值**：
  - 靠近页面顶部：offset 约 +1-2（少量嵌套）
  - 页面中后部（Section 2-3）：offset 约 +4-5（多个 quote/callout 各含 1-6 个 children）
  - 估算公式：直接子节点位置 + 前面所有嵌套子节点数量
- **根本解法**：优先使用 `md_to_page.py` 自动处理图片位置（交替文本段+图片段，所有元素用 index=-1 顺序追加），避免手动计算 index。只有 md_to_page.py 不可用时才走 MCP 手动定位路径
- **手动定位策略**（作为备选）：
  1. 从后往前插入，避免前面插入影响后续 index
  2. 先尝试估算 index，用 `block_fetch_page(render_mode="clean")` 验证位置
  3. 每次调整 ±2
  4. 已上传图片可通过 `file_id` 重新创建（无需重新上传到 COS）

#### L010: COS 上传 MIME 类型必须匹配文件实际格式（2026-06-20 验证）
- **问题**：部分 .png 扩展名文件实际是 JPEG 格式（`sips` 检测为 `format: jpeg`），上传时使用 `Content-Type: image/png` 被 COS 拒绝（HTTP 403 Forbidden）
- **根因**：`fetch_article.py` 从 Substack CDN 下载图片时，CDN URL 中的文件扩展名不一定反映实际格式；Substack 会将 JPEG 图片保存为 .png 扩展名
- **正确做法**：
  1. 上传前用 `sips -g format <图片路径>` 检测实际格式
  2. JPEG 格式文件（无论扩展名）用 `Content-Type: image/jpeg`
  3. PNG 格式文件用 `Content-Type: image/png`
  4. 或在 `md_to_page.py` 中自动检测（脚本已更新）

---

## 🔄 规则演化记录

| 日期 | 触发事件 | 新增/修改的规则 | 影响范围 |
|------|----------|----------------|----------|
| 2026-06-03 | 首次图片上传失败 | 新增核心规则#5「图片不可丢失」 | SKILL.md |
| 2026-06-04 | baoyu.io 文章沙箱限制 | 新增 curl+HTML 解析组合方案 | tips-experience.md |
| 2026-06-04 | after="" 排序问题 | 修正置顶逻辑为 before 参数 | SKILL.md |
| 2026-06-09 | 新增原文链接保留要求 | 新增核心规则#2「原文链接必须保留」 | SKILL.md |
| 2026-06-15 | Every.to 文章图片遗漏 | 新增预检步骤、自检清单、自省机制 | SKILL.md, lessons-learned.md |
| 2026-06-19 | WorkBuddy MCP 工具调用 params 丢失 | 新增 L008：建议短会话执行 MCP 上传；提供手动上传兜底 | lessons-learned.md |
| 2026-06-20 | 翻译时用 IMG_PLACEHOLDER 替代图片语法 → md_to_page.py 无法识别 → 手动定位 index 错位 | 新增核心规则#6「翻译必须保留图片语法」；L003 升级为 P0；新增 L009/L010 | SKILL.md, lessons-learned.md |

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
