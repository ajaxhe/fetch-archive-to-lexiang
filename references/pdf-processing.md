### PDF 文件/链接处理（2026-05-12 实战验证 ✅）

**触发条件**：用户提供的是 PDF 直链（如 `arxiv.org/pdf/xxx`、COS/CDN 直链）、乐享知识库中已存储的 PDF 条目链接，或本地 PDF 文件路径。

**核心原则**：
- PDF 的文字和图片必须分两条路处理，不能合并为一步
- 非中文 PDF（如英文论文）**默认翻译为中英对照格式**后再转存，不可跳过
- 最终产出为乐享**在线文档（page 类型）**，支持后续编辑

#### Step A：获取 PDF 文件

**情况1：乐享知识库中已有 PDF 条目**（如 `lexiangla.com/pages/xxx`）

> 🥇 **首选：用乐享 AI 解析能力直接读取完整原文**（见下方「乐享内 PDF 翻译归档专用流程」）。
> 一条命令即可拿到结构化 markdown 原文 + 图片清单 + 原文 PDF：
>
> ```bash
> python3 scripts/lexiang_pdf_parse.py <entry_id> --download-pdf --out-dir <项目子目录>
> ```

如只需原始 PDF 文件（用于 pymupdf 提取图表）：

```python
# 1. 从 URL 提取 entry_id；entry.target_id 即 file_id
entry = mcp.entry_describe_entry(entry_id="<entry_id>")
file_id = entry.target_id
# 2. 获取下载链接（有效期 3600s）→ 3. 下载
download_url = mcp.file_download_file(file_id=file_id, expire_seconds=3600).url
# curl -L -o paper.pdf "<download_url>"
```

> ✅ **`entry_describe_ai_parse_content` 是读取乐享内 PDF 原文的正确方式**（实测可返回 149K+ 字符，无 80K 限制）。
> 它返回的 `data.content` 是带 `#` 标题层级的 markdown，并把每张图渲染为 `[IMAGE]…[/IMAGE]` 块（含图片标题、AI 生成的中文描述、`/assets/xxx` 链接）。
> ⚠️ `/assets/xxx` 链接需浏览器 JWT 会话，**MCP token 无法下载**——图片仍须从原始 PDF 用 pymupdf 提取。

**情况2：arXiv 等直链 PDF**

```bash
curl -L -o paper.pdf "https://arxiv.org/pdf/2605.05538"
```

---

### 🌟 乐享内英文 PDF → 中英对照 → 转存回同目录（专用流程）

> 适用：用户给出乐享 PDF 条目链接（`lexiangla.com/pages/xxx`），要求翻译为中英对照并转存。
> **最关键的一步是拿到完整、丰富的原文解析内容**——解析不全后续全废。

```
任务进度清单：
- [ ] 1. 解析读取：lexiang_pdf_parse.py 拿到 parsed_raw.md + images.json + meta.json + paper.pdf
- [ ] 2. 图片甄别：从 images.json 区分「真数据图表」与「装饰元素」
- [ ] 3. 图表裁剪：pymupdf 卡片检测裁剪真图表
- [ ] 4. 清洗装配：清掉页眉页脚噪音 + 降级冗余标题（作者/重复子标签/纯数字）为加粗正文，按标题把图片插回对应位置
- [ ] 5. 翻译：默认用当前模型逐块翻译（标题单行双语 `EN / 中文`）；仅用户要求+有 key 时才用 translate_gemini.py
- [ ] 6. 转存：md_to_page.py 上传到 meta.parent_id（原 PDF 所在目录，不新建日期目录）
```

**Step 1 — 一条命令拿全原文解析**

```bash
python3 scripts/lexiang_pdf_parse.py <entry_id> --download-pdf --out-dir <项目子目录>
```

产出 `parsed_raw.md`（完整 markdown 原文）、`images.json`（每个 `[IMAGE]` 的 page/标题/描述/上下文）、`meta.json`（含 `parent_id` = 转存目标目录）、`paper.pdf`。

**Step 2 — 甄别图片（🚨 解析器会过度识别装饰元素）**

乐享解析把**所有**视觉元素都标成 `[IMAGE]`，其中混有：封面图案、作者头像、箭头/图标、纯数字高亮框（如孤立的 “73%” 色块）。这些的数据**已在正文文字里**，无需单独成图。只保留**真数据图表**（条形对比、分布图、信息图等）。判断依据：`images.json` 的 `title`/`desc` 是否描述了**多组可比数据**，以及对应 PDF 页面渲染后是否为独立图表卡片。

**Step 3 — 用「卡片检测」裁剪真图表**（比逐张光栅/矢量提取更稳，因报告图表常由几十个碎片拼成）

```python
import fitz
doc = fitz.open('paper.pdf')
def crop_card(page, mat=fitz.Matrix(2.4, 2.4), pad=7):
    W, H = page.rect.width, page.rect.height
    best = None
    for d in page.get_drawings():
        r = d['rect']
        if r.width <= 0 or r.height <= 0:
            continue
        af = (r.width * r.height) / (W * H)
        # 卡片背景：占页 10%~78%、宽度过半的最大填充矩形（排除整页背景 af≈1.0）
        if 0.10 < af < 0.78 and r.width > 0.5 * W and r.height > 0.10 * H:
            if best is None or r.width * r.height > best.width * best.height:
                best = r
    if best:
        clip = fitz.Rect(best.x0 - pad, best.y0 - pad, best.x1 + pad, best.y1 + pad)
        return page.get_pixmap(matrix=mat, clip=clip)
    return None
```

> ⚠️ 卡片检测对**纯文字卡片**（如附录的「How AI gets absorbed」段落、文字表格）也会命中——务必渲染成图后**目视核对**（拼成 contact sheet 一次看多张），只留真图表。封面/作者合影用固定区域裁剪。

**Step 4 — 清洗 + 控制标题 + 按标题插图**

- 删除运行页眉/页脚噪音（`Presented by…` / `Powered by glean` / `Work AI Institute` / `p. NN` / 重复副标题）和 `<!-- page-number -->` 注释。
- **🚨 标题层级要克制（否则乐享目录极度膨胀）**：乐享按 `#` 标题生成目录。解析出的 markdown 往往把**作者名、人物叙事名、重复子标签（如各地区/职能/行业下的 The posture / How AI gets absorbed / What workers are doing / The tradeoff）、纯数字百分比**都标成了标题——这些**一律降级为加粗正文 `**...**`**。只保留真正的章节/小节标题，每个大章节在目录里**一行**即可。
- **🚨 标题层级要重排（解析常把二/三级误标为一级）**：解析器给的 `#` 级别**不可信**——它经常把章节内的图表标题、小节都标成 `#`（一级），导致目录里几十个一级标题、层级全乱。务必**按文档真实逻辑重排**：①只让**正文真正的大章节**（对应目录页那几条 + 标题页/作者/目录）保持一级 `#`；②大章节内的图表/小节统一为二级 `##`；③附录里「地区/职能/行业」这类并列项是三级 `###`（其上的 Appendix A/B/C 为二级）。判定英文标题名时注意两类坑：中文译文以 `AI`/`UX` 等短词开头会污染「首个中文字符前取英文」的切法；而 `Government / public sector`、`Nonprofit / NGO` 这类名称**内部就含 ` / `**，不能当双语分隔符切断。
- **🚨 目录页（Table of Contents）单独重建**：原文的目录常被解析成**表格**，再叠加双语翻译，导致每个章节拆成 3–4 行（Page/页码、英文标题、中文标题各占一格），极度冗余。**不要保留表格**，重建为「一章一行」的清单：`- **Section N / 第 N 部分**：English Title / 中文标题 · p.NN`。
- **精确插图技巧**：这类报告每张图表都有一句标题，且**与正文某个 `#` 标题一字不差**。把图表标题作为关键字匹配正文标题行，在其后插入 `![双语图注](images/xxx.png)`——位置自然正确，无需手算 block index。
- **🚨 表格翻译：中英同格 + 合并单元格用 HTML**：解析出的 markdown 表格有两个通病——①翻译时把中文**整行/整表另起**（一个英文行下面再来一个中文行，甚至整张表复制成中文表），目录/正文都很乱；②原文的合并单元格（rowspan/colspan）、统计卡片布局被拍平成普通网格，意思走样。**正确做法**：把每个表**重建为原生 HTML `<table>`**——文本单元格内 `English<br>中文` 同格双语（数据/百分比格不必翻译）；合并单元格用 `rowspan`/`colspan` 还原；统计卡片用 2×N 的 `<td>` 网格。乐享 `entry_import_content_to_entry` 的 **markdown 和 html 两种 content_type 都会把内嵌 `<table>` 透传渲染成表格块**（实测 `rowspan`/`colspan` 正确生效），所以直接把 HTML 表嵌在 markdown 正文里即可，无需切换 content_type。改完用 `block_convert_content_to_blocks`（纯转换、不落库）可先验证 `col_span`/`row_span` 是否正确。
- 保留所有 `![](...)`（核心规则 #6）。

**Step 5 — 翻译为中英对照**

🥇 **默认：用当前运行 skill 的大模型（Agent 自己）逐块翻译**（长文按 3000–5000 字符分块），无外部依赖、质量可控。翻译时遵守：

- **🚨 标题单行双语**：`## English Title / 中文标题`（同一行 ` / ` 分隔），**禁止**把中文标题另起一行——否则一个章节在目录里占两行，查看极不便。
- 正文每段英文后紧跟中文译文（空行分隔）；保留所有 `![](...)`。

🥈 **备选（仅用户明确要求且已提供 `GEMINI_API_KEY` 时）**：

```bash
python3 scripts/translate_gemini.py <清洗后.md> <中英对照.md>   # 保留 ![](...)；注意校验失败分块并补译
```

**Step 6 — 转存回原目录**

用 `meta.json` 里的 `parent_id`（原 PDF 所在目录）作为上传目标，**不新建日期目录**：

```bash
python3 scripts/md_to_page.py <中英对照.md> --parent-id <meta.parent_id> --name "<标题> 中英对照"
```

无 LEXIANG_TOKEN 时按 SKILL.md「MCP 直接调用方法」全自动降级。

---

#### Step B：提取文字（pymupdf）

```python
import fitz

doc = fitz.open('paper.pdf')
text = ''
for page in doc:
    text += page.get_text()
with open('paper.txt', 'w') as f:
    f.write(text)
print(f"Pages: {doc.page_count}, chars: {len(text)}")
```

`get_text()` 只提取纯文字——矢量图（流程图/柱状图）和表格结构会丢失，这是预期行为，图形通过 Step C 单独处理。

#### Step C：定位并精确裁剪图形

PDF 中的图形分两类，提取方式不同：

| 类型 | 判断方法 | 提取方法 |
|------|---------|---------|
| **光栅图**（嵌入的 PNG/JPEG） | `page.get_images()` 有结果 | `page.get_image_rects(xref)` 获取坐标 → `clip=Rect` 裁剪 |
| **矢量图**（流程图/柱状图，PDF 绘图命令） | `page.get_images()` 无结果，但 `page.get_drawings()` 有数据 | `page.get_drawings()` 获取边界 → `clip=Rect` 截图 |

**定位图形坐标**（先找出各 Figure 所在页面）：

```python
doc = fitz.open('paper.pdf')

for page_idx in range(doc.page_count):
    page = doc[page_idx]
    
    # 找 Figure caption 位置（确定图形所在页）
    blocks = page.get_text("blocks")
    for b in blocks:
        if 'Figure' in b[4]:
            print(f"Page {page_idx+1}: [{b[0]:.0f},{b[1]:.0f},{b[2]:.0f},{b[3]:.0f}] {b[4][:60]}")
    
    # 光栅图坐标
    for img in page.get_images(full=True):
        rects = page.get_image_rects(img[0])
        print(f"  Raster img: {rects}")
    
    # 矢量图分布（按左栏/右栏区分，双栏论文左栏 x<295，右栏 x>295）
    drawings = page.get_drawings()
    if drawings:
        xs0 = [d['rect'].x0 for d in drawings]
        xs1 = [d['rect'].x1 for d in drawings]
        ys0 = [d['rect'].y0 for d in drawings]
        ys1 = [d['rect'].y1 for d in drawings]
        print(f"  Vector drawings bbox: ({min(xs0):.0f},{min(ys0):.0f},{max(xs1):.0f},{max(ys1):.0f})")
```

**精确裁剪图形区域**（3x 高清，仅裁剪图形本身+caption，不含论文正文）：

```python
mat = fitz.Matrix(3.0, 3.0)  # 3x 放大，确保清晰

# 根据上面分析的坐标，裁剪每个 Figure
# 双栏论文参考坐标：左栏 x: 58-290，右栏 x: 295-535
# y 坐标从 caption 文字位置往上定图形起点
clip = fitz.Rect(x0, y0, x1, y1)  # 精确到图形边界，含 caption
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(f'Figure{n}.png')
```

**⚠️ 关键注意事项**：
- **绝对不能用 `page.get_pixmap()` 不传 clip**——会截整页（含论文正文），不是图形本身
- `get_image_rects()` 只对光栅图有效；矢量图只能通过 `get_drawings()` 的 bbox + caption 坐标推断边界
- 验证截图效果：`Read` 工具可预览 PNG，检查是否干净（只含图形+caption）
- 如果矢量图跨越双栏（`x0 < 295`），说明是通栏图，裁剪区域应包含完整宽度

#### Step D：语言检测与翻译

读取 `paper.txt` 前 500 字符，统计中文字符占比：
- 中文字符比例 ≥ 30% → 中文内容，**跳过翻译**
- 中文字符比例 < 30% → 非中文（如英文论文），**必须翻译为中英对照格式**

**中英对照翻译格式**（每段先英文原文，紧跟中文翻译，保留所有结构）：

```markdown
## Introduction / 引言

Standard RAG pipelines follow a static retrieve-then-generate paradigm...

标准 RAG 流水线遵循静态的"先检索再生成"范式...

### Tables（表格保留完整数据，加中文表头）

### Figures（图形位置用文字描述，图片在 Step E 中插入）
```

翻译方式（按优先级）：
1. **Agent（当前运行的模型）直接翻译**（默认方式，无外部依赖）：长文按 3000-5000 字符分块逐块翻译
2. `translate_gemini.py`（`GEMINI_API_KEY` 可用时）
3. `translate_article.py`（`OPENAI_API_KEY` 可用时）

#### Step E：导入乐享在线文档 + 插入图片

**1. 创建在线文档（import_content）**

```python
result = mcp.entry_import_content(
    name="论文标题 中英对照翻译",
    content=open('paper_translated.md').read(),  # 中英对照版
    content_type="markdown",
    parent_id="<日期目录ID>",
    space_id="<SPACE_ID>"
)
page_entry_id = result.entry.id
page_root_block_id = result.entry.target_id  # page 根 block，用于 move/insert
```

**2. 上传各 Figure 图片并插入正确位置**

每张图的完整流程（三步）：

```bash
# Step 1: 申请上传凭证
session_id, upload_url = mcp.block_apply_block_attachment_upload(
    entry_id=page_entry_id,
    name="FigureN.png",
    size=str(file_size),
    mime_type="image/png"
)

# Step 2: 上传图片（必须包含 Content-Length 和 Content-Type）
curl -X PUT "<upload_url>" \
  -H "Content-Type: image/png" \
  -H "Content-Length: <size>" \
  --data-binary @FigureN.png

# Step 3: 在文档正确位置插入 image block
# - 先用 block_list_block_children 获取 block 列表，找到对应章节段落的 index
# - caption 格式：英文原文 / 中文翻译（放在一行，用 / 分隔）
mcp.block_create_block_descendant(
    entry_id=page_entry_id,
    parent_block_id=page_root_block_id,
    index="<正确位置>",
    descendant=[{
        "block_type": "image",
        "image": {
            "session_id": session_id,
            "caption": "Figure N: English caption / 图N：中文翻译",
            "align": "center"
        }
    }]
)
```

> **⚠️ 重要**：
> - **caption 英中放在一行**：用 ` / ` 分隔，不要额外插入独立段落作为图注，否则显示时会有多余换行
> - **图片位置要精确**：先获取 block 列表找到对应章节 block 的 index，不能全部 append 到末尾
> - **`update_block` 不支持修改 image block 的 caption**：如果 caption 写错了，只能 delete + recreate。重建时可用已有的 `file_id`（通过 `block_describe_block` 查询），**不需要重新上传文件**
> - **每次插入图片后 index 会偏移**：如需在不同位置插入多张图，要按顺序从前往后插，并累计计算 index

**3. 图片位置确定方法**

先获取文档当前全部 block：
```python
blocks = mcp.block_list_block_children(entry_id=page_entry_id, with_descendants=False)
```

找到对应章节的最后一个 p/h block 的 index，图片插入该 index+1 处。

**已验证的工作流（arXiv PDF 2605.05538 实战，2026-05-12）**：
- Figure 1/2 为光栅图（嵌入 PNG），用 `get_image_rects()` 定位
- Figure 3/4 为矢量图（柱状图），用 `get_drawings()` bbox + caption 坐标确定裁剪区域
- Figure 5 为光栅图（截图），用 `get_image_rects()` 定位
- 所有图片 3x 渲染后 60-90KB，质量良好

### 微信公众号文章（mp.weixin.qq.com）专项优化
脚本对微信公众号文章有专门的检测和处理策略：

1. **自动检测**：识别 `mp.weixin.qq.com` 域名，自动启用微信模式
2. **无需登录**：微信公众号文章是公开可读的，跳过登录检测和 Cookie 注入流程
3. **专用内容选择器**：使用 `#js_content` / `.rich_media_content` 精准定位正文区域（而非通用选择器可能匹配到页面其他内容）
4. **标题提取**：`#activity-name` > `h1.rich_media_title` > 通用 h1 > meta 标签回退
5. **作者提取**：`#js_name`（公众号名称）> `.rich_media_meta_nickname` > 通用选择器回退
6. **日期提取**：`#publish_time` > 通用 time/date 选择器回退
7. **图片懒加载增强**：
   - 微信图片使用 `data-src` + IntersectionObserver 懒加载
   - 滚动速度放慢（300px 步长、200ms 间隔）以确保触发所有 IntersectionObserver
   - 强制将未触发的 `data-src` 复制到 `src`（兜底策略）
   - 图片下载时优先使用 `data-src` 的高清原图 URL
8. **图片格式识别**：微信图片 URL 格式特殊（`mmbiz.qpic.cn/...?wx_fmt=png`），从 `wx_fmt` 查询参数推断文件扩展名
9. **Referer 防盗链**：通过 Playwright 页面上下文的 `page.request.get()` 下载图片，自动携带正确的 Referer 头

**Substack 站点（如 www.lennysnewsletter.com）专项优化**：
脚本对 Substack 托管的站点（`*.substack.com`、`lennysnewsletter.com` 等）有专门的登录检测和**登录态缓存**机制：

1. **登录态缓存**：登录成功后自动保存 Playwright `storage_state` 到 `~/.substack/storage_state.json`，后续抓取直接复用，**无需重复登录和邮箱验证**
2. **优先级**：缓存 `storage_state` > Chrome cookies > 引导登录
3. **自动检测登录状态**：加载页面后检查右上角是否有用户头像（已登录）还是 "Sign in" 按钮（未登录）
4. **已登录** → 直接抓取全文，并刷新缓存延长有效期
5. **缓存过期** → 自动清理旧缓存，进入引导登录流程
6. **未登录** → 打开可见浏览器窗口引导登录，用户在终端输入 `y` 确认后二次验证，通过后自动缓存

**独立登录命令**（推荐首次使用时先执行）：
```bash
python scripts/fetch_article.py login
```
此命令单独完成 Substack 登录并缓存，不需要指定文章 URL。后续所有 Substack 文章抓取都会自动复用此登录态。

**非 Substack 站点的登录确认机制**：
- 无 Chrome cookies 时自动切换到非无头模式，打开可见浏览器窗口
- 终端提示用户完成登录操作后**按回车键**继续
- 收到确认信号后重新加载页面并检测付费墙状态

**付费墙检测**：脚本同时检测以下信号：
- DOM 元素：`[data-testid="paywall"]`、`.paywall`
- 文本关键词：`This post is for paid subscribers`、`Subscribe to read`、`Upgrade to paid` 等
- 注意：不同网站的付费墙 DOM 结构和关键词不同，如遇新网站抓取不完整，需检查页面实际的付费墙标识并更新检测逻辑

**判断内容是否完整的方法**：
- 先用 `web_fetch` 尝试获取，如果明显被截断（内容不完整、出现付费提示），则切换到 `fetch_article.py`
- 抓取完成后**必须**告知用户查看 `article.md` 确认内容完整性
- 关注文章末尾是否有作者署名/总结段落作为完整性标志
- 如果用户反馈内容不完整，检查：(1) 登录账号是否有付费权限 (2) 页面是否有懒加载内容未触发 (3) 内容选择器是否匹配到了免费预览区而非全文区

**产出物**：
- `<项目子目录>/<原文标题>.md` — 完整文章 Markdown（含图片引用）
- `<项目子目录>/<原文标题>_meta.json` — 结构化元信息（原文链接、作者、发布时间、抓取时间等）
- `<项目子目录>/images/` — 所有文章配图

`<原文标题>_meta.json` 格式：
```json
{
  "url": "原文链接",
  "title": "文章标题",
  "subtitle": "副标题",
  "author": "作者",
  "date": "发布时间",
  "content_length": 12345,
  "image_count": 5,
  "images": ["images/img_01_xxx.png", ...],
  "fetched_at": "2026-02-25T10:30:00"
}
```

#### X.com / Twitter 帖子抓取（必须用 CDP 模式）

**X.com 是登录墙网站的典型代表**，`web_fetch` 和普通 Cookie 注入模式都无法抓取，**必须使用 CDP 模式**：

```bash
# CDP 模式（必须）
python scripts/fetch_article.py fetch "https://x.com/<username>/status/<id>" --output-dir <项目子目录> --cdp
```

**CDP 模式工作原理**：
1. 通过 Chrome DevTools Protocol (port 9222) 连接用户真实 Chrome 浏览器
2. 复用浏览器中已登录的 X 账号会话
3. 绕过自动化浏览器检测（X 会检测并阻止 Playwright/Selenium）

**CDP 模式前置条件**：
```bash
# 启动 Chrome 并开启 CDP 端口
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# 验证
curl -s http://localhost:9222/json/version
```

**X.com 抓取的特殊处理**：
1. 帖子内容会转换为 Markdown 格式
2. 图片（帖子中的媒体）会下载到 `images/` 目录
3. 帖子中的链接会转换为 Markdown 链接格式
4. 转发数、点赞数等元信息会保留

**产出物**：
- `<项目子目录>/<原文标题>.md` — 帖子 Markdown
- `<项目子目录>/<原文标题>_meta.json` — 元信息
- `<项目子目录>/images/` — 帖子中的媒体图片

#### 微博帖子抓取（必须用 CDP 模式）

**微博是强制登录墙网站**，所有端口（PC 端 `weibo.com`、移动端 `m.weibo.cn`、API `m.weibo.cn/statuses/show`）均需要登录态，`web_fetch` 和普通 Playwright 都会被重定向到 `Sina Visitor System` 登录页。**必须使用 CDP 模式**。

**抓取命令**：

```bash
# CDP 模式（必须）— 连接本地已登录 Chrome
python scripts/fetch_article.py fetch "https://weibo.com/<uid>/<mid>" --output-dir <项目子目录> --cdp
```

**完整流程**：

1. **确保 Chrome 已开启 CDP 端口**（port 9222）且已登录微博
2. **运行 `fetch_article.py --cdp`**：脚本会连接真实 Chrome，复用微博登录态
3. **CDP 连接失败时的自动降级**：脚本会回退到 Cookie 注入模式（从 Chrome Cookie DB 提取 cookies），但微博 Cookie 注入通常也能工作
4. **抓取后整理内容**：微博原始 HTML 结构较乱，抓取结果中可能包含导航、按钮等噪音文本，需要手动清理或用 AI 整理为结构化 Markdown
5. **转存乐享**：使用 `entry_import_content` 创建页面（非 `file_create_hyperlink`，后者仅支持微信公众号链接）

**微博抓取的特殊注意事项**：

| 问题 | 说明 |
|------|------|
| `web_fetch` 失败 | 微博强制登录，WebFetch 会被重定向到 `passport.weibo.com/visitor/visitor` |
| Playwright 失败 | 微博检测 HeadlessChrome UA，即使用 `--browser=chrome` 也会被拦截 |
| CDP 前置条件 | Chrome 必须已开启 `--remote-debugging-port=9222` 且已登录微博 |
| 内容整理 | 微博页面标题通常是「微博正文 - 微博」，转存时应提取作者名和关键主题作为标题 |
| 图片处理 | 微博图片使用 `sinaimg.cn` CDN，`fetch_article.py` 可以下载，但部分图片可能需要 Referer |

**产出物**：
- `<项目子目录>/article.md` — 微博内容 Markdown（注意：微博标题通常是通用的，需手动重命名）
- `<项目子目录>/article_meta.json` — 元信息
- `<项目子目录>/images/` — 微博中的图片（如有）

**转存乐享时的标题建议**：
微博原始标题是「微博正文 - 微博」，转存时应改为有意义的标题，格式建议：`<作者>：<主题关键词>`，例如：
- `唐杰THU：最近的一些想法（AI 技术趋势）`
- `李飞飞：关于 Spatial AI 的思考`

#### 英文文章翻译为中英对照

对于英文文章（如 X 帖子、英文博客等），可以使用 OpenAI API 翻译为中英对照格式：

**翻译脚本** (`scripts/translate_article.py`)：

```bash
python scripts/translate_article.py <原文.md> <输出.md> --model gpt-4o-mini
```

**翻译格式**：
```markdown
## 英文标题

[英文原文段落]

[中文翻译]

## 第二节英文标题

[英文原文...]

[中文翻译...]
```

**翻译工作流**：
1. 先用 `fetch_article.py` 抓取原文
2. 用 `translate_article.py` 翻译为中英对照
3. 将翻译后的 Markdown 上传到乐享知识库

**依赖**：
- `OPENAI_API_KEY` 环境变量

#### 使用 `web_fetch` 获取的免费文章

对于通过 `web_fetch` 获取到完整内容的免费文章，**同样需要保存原文**：
1. **保存原文全文**：将 `web_fetch` 返回的内容直接保存为 Markdown，**不做总结、不做摘要、不做改写**，保持原文的完整结构和措辞
2. 文件名使用原文标题：`<项目子目录>/<原文标题>.md`
3. 手动构建 `<原文标题>_meta.json`，包含 URL、标题、作者、日期等元信息
4. 如果文章包含图片，尽量下载保存到 `<项目子目录>/images/`

> **关键区分**：`web_fetch` 工具可能会返回总结/摘要版本而非原文全文。如果返回的内容明显是总结（缺少原始段落、引用、细节），需要在 `web_fetch` 调用时明确要求"返回完整原始全文内容，不要总结或缩写"。保存到本地的**必须是原文全文**，而不是经过 AI 总结的摘要。

