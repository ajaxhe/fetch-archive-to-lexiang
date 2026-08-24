import os, re, urllib.parse, urllib.request, html
from html.parser import HTMLParser

ROOT = "/Users/ajaxhe/.workbuddy/skills/fetch-archive-to-lexiang/articles/glean_model_routing_20260824"
HTML = os.path.join(ROOT, "source.html")
IMG_DIR = os.path.join(ROOT, "images")
os.makedirs(IMG_DIR, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

with open(HTML, encoding="utf-8") as f:
    raw = f.read()

# ---------- extract meta: title / author / date ----------
def meta_content(prop):
    # robust: scan all <meta> tags, match property/name regardless of attr order
    for m in re.finditer(r'<meta\b[^>]*>', raw, re.I):
        tag = m.group(0)
        pm = re.search(r'property=["\']([^"\']+)["\']', tag, re.I)
        nm = re.search(r'name=["\']([^"\']+)["\']', tag, re.I)
        key = (pm.group(1) if pm else None) or (nm.group(1) if nm else None)
        if key and key.lower() == prop.lower():
            cm = re.search(r'content=["\']([^"\']+)["\']', tag, re.I)
            if cm: return cm.group(1)
    return None

title = meta_content("og:title") or meta_content("twitter:title")
pub = meta_content("article:published_time")
author = meta_content("article:author")
# JSON-LD fallback
if not author:
    m = re.search(r'"author"\s*:\s*\{\s*"name"\s*:\s*"([^"]+)"', raw)
    if m: author = m.group(1)
    else:
        m = re.search(r'"author"\s*:\s*"([^"]+)"', raw)
        if m: author = m.group(1)
if not title:
    m = re.search(r'"headline"\s*:\s*"([^"]+)"', raw)
    if m: title = m.group(1)

if not title:
    title = "Frontier Model Cost and Open-Weights Popularity is Driving Demand for Model Routing"
if not author:
    author = "Richard MacManus"
if not pub:
    pub = "2026-08-19"

print("TITLE:", title)
print("AUTHOR:", author)
print("PUBLISHED:", pub)

# ---------- extract .available-content subtree ----------
class AvailExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.capturing = False
        self.start_depth = None
        self.start_tag = None
        self.out = []
        self.imgs = []  # (original_src, local_path)

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        depth = len(self.stack)
        cls = dict(attrs).get("class", "")
        if not self.capturing and "available-content" in cls:
            self.capturing = True
            self.start_depth = depth
            self.start_tag = tag
        if self.capturing:
            if tag == "img":
                d = dict(attrs)
                src = d.get("src", "")
                # derive real S3 url
                real = src
                i = src.find("substack-post-media.s3.amazonaws.com")
                if i >= 0:
                    real = "https://" + urllib.parse.unquote(src[i:])
                idx = len(self.imgs) + 1
                ext = "png"
                mm = re.search(r"\.([a-zA-Z0-9]+)(?:\?|$)", real)
                if mm: ext = mm.group(1).lower()
                local = f"images/img_{idx:02d}.{ext}"
                self.imgs.append((real, local))
                # rebuild tag with local src + keep alt
                alt = d.get("alt") or ""
                self.out.append(f'<img src="{local}" alt="{html.escape(str(alt))}">')
            else:
                # reconstruct minimal start tag
                inner = " ".join(f'{k}="{html.escape(str(v))}"' for k, v in attrs)
                self.out.append(f"<{tag} {inner}>" if inner else f"<{tag}>")

    def handle_endtag(self, tag):
        depth = len(self.stack)
        if self.capturing:
            self.out.append(f"</{tag}>")
            if tag == self.start_tag and depth == self.start_depth:
                self.capturing = False
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if self.capturing:
            self.out.append(data)

p = AvailExtractor()
p.feed(raw)
subtree = "".join(p.out)
print("IMAGES FOUND:", len(p.imgs))
for real, local in p.imgs:
    print("  ", local, "<-", real[:90])

# ---------- download images ----------
for real, local in p.imgs:
    dst = os.path.join(ROOT, local)
    try:
        req = urllib.request.Request(real, headers={"User-Agent": UA, "Referer": "https://www.latent.space/"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(dst, "wb") as f:
            f.write(data)
        print("downloaded", local, len(data), "bytes")
    except Exception as e:
        print("FAIL", local, e)

# ---------- convert subtree to markdown ----------
import html2text
h = html2text.HTML2Text()
h.body_width = 0
h.baseurl = ""
md = h.handle(subtree)

# strip known platform noise blocks
noise_markers = [
    "Subscribe to Latent Space", "Discover more from Latent Space",
    "Discussion about", "© 2026 Latent Space", "Share this post",
]
lines = md.splitlines()
clean = []
skip = False
for ln in lines:
    if any(m in ln for m in noise_markers):
        skip = True
        continue
    if skip:
        # resume on a blank line or a real heading
        if ln.strip() == "" or ln.startswith("#") or ln.startswith("!["):
            skip = False
        else:
            continue
    clean.append(ln)
md = "\n".join(clean).strip() + "\n"

# header block
header = f"> **{title}**\n>\n> 作者：{author or 'Richard MacManus'}  ·  发布：{pub or '2026-08-19'}  ·  来源：[Latent Space](https://www.latent.space/p/glean-model-routing)\n\n"

with open(os.path.join(ROOT, "source.md"), "w", encoding="utf-8") as f:
    f.write(header + md)

print("source.md written, chars=", len(header + md))
print("=== first 600 chars ===")
print((header + md)[:600])
