# 乐享归档与公共上传器

本文只描述归档层策略。Markdown 写入实现以独立
`upload-markdown-to-lexiang` Skill 为唯一事实源。

## 配置

归档目标优先级：

1. 用户本次指定的知识库或目录。
2. 工作区私有规则。
3. 本 Skill gitignored `config.json`。
4. 初始化向导。

目标配置不得写入公开 `SKILL.md` 或 Git 跟踪文件。

> ⚠️ **company 一致性硬规则（2026-07-17 加入）**：归档目标必须与上载器
> `upload-markdown-to-lexiang` 凭证所在的 company 完全一致。凡哥个人知识库(csig)
> 与上传器/OpenAPI 凭证(贾维斯 `e6c565`) 分属不同 company，强制路由到 csig 会 403。
> **做法**：直接复用上传器凭证所在 company（config.json 的 `target_space` 与之对齐），
> 建目录用同 company 的 OpenAPI、传页面用上传器 MCP，两边同 company 即不跨域。
> 不要因为某条记忆里写了"个人知识库=csig"就临时覆盖目标 space。

## 日期目录

> 目录（folder）创建/查询也必须走上传器凭证所在的 company：当前即 贾维斯(`e6c565`)，
> 因此用 **OpenAPI** 而非 csig 的 MCP `entry_*` 工具（后者跨 company 会 403）。
> OpenAPI 助手来自 `scripts/upload_video_via_openapi.py`（`load_config`/`get_access_token`）。

1. `space_id` 取 config.json 的 `target_space`（`b6013f64`），`root_entry_id` 用 space 根。
2. 列子目录：`GET /cgi-bin/v1/kb/entries?space_id=X&parent_id=<folder_id>&page=1&page_size=50`
   （过滤参数是 `parent_id`，**不是** `parent_entry_id`，后者会返回 space 根列表）。
3. 找到同名且 `entry_type=folder` 则复用；否则 `POST /cgi-bin/v1/kb/entries?space_id=X` 创建：
   `body={"data":{"attributes":{"name":"YYYY-MM-DD","entry_type":"folder"},"relationships":{"parent_entry":{"data":{"type":"entry","id":<父目录ID}}}}}`
   （folder 无需 `state` 字段）。
4. 标题子目录同样用 OpenAPI 建，再拿其 ID 作为 `--parent-id` 传给上传器。
5. 置顶用上传器 `--pin`（MCP，同 company）；不要用 `after=""`。

## 公共上传依赖

调用方不得假设固定安装路径。优先在当前 Skill 的同一个 skills 根目录寻找：

```text
upload-markdown-to-lexiang/
├── SKILL.md
└── scripts/lexiang_upload.py
```

缺失时由当前平台的 Skill 管理器安装。安装后要求版本满足 `>=1.1.0,<2.0.0`：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" --version
# cli_api == "1"
```

首次使用的个人凭证从 <https://lexiangla.com/ai/claw> 获取：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" auth login
```

不要读取 Agent MCP 配置、连接器 token 或旧 `LEXIANG_TOKEN`。

## Markdown 上传

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  "<最终文档>.md" \
  --parent-id "<日期目录ID>" \
  --name "<标题>" \
  --pin \
  --json
```

上传器统一处理纯文本、图文和大 Markdown 文档，因此不再按字符数或图片数量选择不同脚本。
它同时直接渲染 `trans-doc-to-md` Prepared Markdown Package 中的富元素标注；
正常上传不再由本 Skill 使用 MCP 二次渲染。

## 图片规则

- 抓取阶段必须把远程图片下载为 Markdown 同目录下的相对路径。
- `trans-doc-to-md` 加工阶段保留标准 `![](...)` 语法和位置。
- 上传前公共 CLI 检查每个本地文件。
- 上传后公共 CLI 对账 `local_images == remote_images`。
- 公网图片不属于本地上传范围；重要图片应先下载，避免 CDN 过期或防盗链。

## 局部修改

上传后只修少量 block 时可以使用乐享 block 工具精确修改，不必全量覆盖。
但修改必须同步回本地 Markdown，确保本地文档仍是内容事实源。

## 非 Markdown 文件

- 微信公众号链接：`file_create_hyperlink`。
- 视频和音频：`upload_video_via_openapi.py`。
- 独立 PDF/Office/附件：使用文件上传流程。
- 这些路径不调用公共 Markdown 上传器。
