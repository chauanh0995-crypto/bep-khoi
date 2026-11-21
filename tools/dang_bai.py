"""Đăng bài blog đến hạn cho suoncaykhonglo.vn.

Hàng chờ: thư mục _lich-dang/ (chỉ nằm trên máy, không đẩy lên GitHub).
Mỗi bài là một tệp .html dạng:

    ---
    date: 2026-11-21
    slug: duong-dan-bai
    title: Tiêu đề hiện trên Google
    h1: Tiêu đề lớn, <em>từ nhấn</em>
    desc: Mô tả 140–160 ký tự
    excerpt: Một hai câu tóm tắt
    hero: hero-bai-....jpg        (ảnh ngang nét, đầu bài)
    cover: ten-anh.jpg            (ảnh trong bài và thẻ bài)
    cover_alt: Mô tả ảnh
    ---
    <p class="lede">...</p>
    ...

Bài có date <= hôm nay và chưa đăng sẽ được tạo trang, cập nhật blog, sitemap, llms.txt,
rồi commit + push (trừ khi chạy với --khong-push). Chạy: python -X utf8 tools/dang_bai.py
"""
import datetime, glob, json, os, re, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://suoncaykhonglo.vn/'
QUEUE = os.path.join(ROOT, '_lich-dang')
REG = os.path.join(ROOT, 'blog', 'bai-viet.json')
LOG = os.path.join(ROOT, 'tools', 'dang-bai.log')
INDEXNOW_KEY = '7f3c9a2e5b8d41f6a0c4e9b2d7f1a3c8'
PUSH = '--khong-push' not in sys.argv
TODAY = datetime.date.today().isoformat()
if '--ngay' in sys.argv:                       # chạy thử như thể hôm nay là ngày khác
    TODAY = sys.argv[sys.argv.index('--ngay') + 1]

def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(s)

def vn_date(d):
    return f'{d[8:]}/{d[5:7]}/{d[:4]}'

# ---------- mẫu trang: lấy từ thuc-don.html để luôn khớp thanh menu, chân trang ----------
tpl = rd('thuc-don.html')
T_HEAD = tpl[:tpl.index('<title>')]
T_TAIL = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '',
                tpl[tpl.index('<meta name="theme-color"'):tpl.index('</head>')], flags=re.S)
T_TOP = tpl[tpl.index('<body'):tpl.index('<main>') + len('<main>\n')]
T_FOOT = tpl[tpl.index('  <section class="cta-strip">'):]

def relink(html, pre):
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'(https?:|#|mailto:|tel:|data:|/)', url):
            return m.group(0)
        return f'{attr}="{pre}{url}"'
    html = re.sub(r'\b(href|src)="([^"]*)"', fix, html)
    return re.sub(r"url\('(?!https?:|/)([^']+)'\)", lambda m: f"url('{pre}{m.group(1)}')", html)

def nav(pre):
    top = T_TOP.replace(' aria-current="page"', '').replace('>Blog</a>', ' aria-current="page">Blog</a>', 1)
    return relink(top, pre)

def meta(title, desc, path, image, kind='website', extra=''):
    url = BASE + path
    return f'''<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="Bếp Khói – Sườn Cay Khổng Lồ Đà Lạt">
<meta property="og:locale" content="vi_VN">
<meta property="og:type" content="{kind}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}images/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="VN-35">
<meta name="geo.placename" content="Đà Lạt">
<meta name="geo.position" content="11.9511412;108.4653718">
<meta name="ICBM" content="11.9511412, 108.4653718">
{extra}'''

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>\n'

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
                                for i, (n, u) in enumerate(items)]}

def page_hero(crumb_html, h1, sub, image):
    return f'''  <section class="page-hero" style="--bg: url('{image}')">
    <div class="wrap">
      <nav class="crumbs" aria-label="Vị trí trang">{crumb_html}</nav>
      <h1>{h1}</h1>
      <p>{sub}</p>
    </div>
  </section>

'''

def card(p, pre):
    return f'''        <article class="post-card reveal">
          <a href="{pre}{p['slug']}/" class="pc-img"><img src="{pre}../images/{p['cover']}" alt="{p['cover_alt']}" loading="lazy"></a>
          <div class="pc-body">
            <p class="pc-date">{vn_date(p['date'])}</p>
            <h3><a href="{pre}{p['slug']}/">{p['title']}</a></h3>
            <p>{p['excerpt']}</p>
            <a class="pc-more" href="{pre}{p['slug']}/">Đọc tiếp <span aria-hidden="true">→</span></a>
          </div>
        </article>
'''

def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    if not m:
        raise ValueError(f'{os.path.basename(path)}: thiếu phần --- đầu tệp')
    meta_ = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta_[k.strip()] = v.strip()
    for k in ['date', 'slug', 'title', 'h1', 'desc', 'excerpt', 'hero', 'cover', 'cover_alt']:
        if not meta_.get(k):
            raise ValueError(f'{os.path.basename(path)}: thiếu {k}')
    for img in (meta_['hero'], meta_['cover']):
        if not os.path.exists(os.path.join(ROOT, 'images', img)):
            raise ValueError(f'{os.path.basename(path)}: không có ảnh images/{img}')
    meta_['body'] = m.group(2).strip()
    return meta_

def build_post(p, published):
    url = f"blog/{p['slug']}/"
    others = [o for o in sorted(published, key=lambda x: x['date'], reverse=True) if o['slug'] != p['slug']][:2]
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'], "description": p['desc'],
           "image": [BASE + "images/" + p['hero'], BASE + "images/" + p['cover']],
           "datePublished": p['date'], "dateModified": p['date'], "inLanguage": "vi",
           "mainEntityOfPage": BASE + url,
           "author": {"@type": "Organization", "name": "Bếp Khói", "url": BASE},
           "publisher": {"@type": "Organization", "name": "Bếp Khói",
                         "logo": {"@type": "ImageObject", "url": BASE + "images/logo-bep-khoi.png"}},
           "about": {"@id": BASE + "#restaurant"}}
    plain_h1 = re.sub('<[^>]+>', '', p['h1'])
    html = (T_HEAD + meta(p['title'] + ' | Bếp Khói', p['desc'], url, p['hero'], 'article',
                          f'<meta property="article:published_time" content="{p["date"]}">\n')
            + relink(T_TAIL, '../../')
            + ld(crumbs([('Trang chủ', ''), ('Blog', 'blog/'), (plain_h1, url)])) + ld(art)
            + '</head>\n' + nav('../../')
            + page_hero('<a href="../../index.html">Trang chủ</a><span>/</span><a href="../">Blog</a><span>/</span>Bài viết',
                        p['h1'], p['excerpt'], f"/images/{p['hero']}")
            + f'''  <section class="section paper">
    <div class="wrap article-wrap">
      <article class="article">
        <p class="article-meta">Bếp Khói · {vn_date(p['date'])}</p>
        <figure class="article-fig"><img src="../../images/{p['cover']}" alt="{p['cover_alt']}" loading="lazy"><figcaption>{p['cover_alt']}</figcaption></figure>
{p['body']}
        <div class="article-cta">
          <a class="btn btn-fire" href="../../dia-chi.html#dat-ban">Đặt bàn</a>
          <a class="btn btn-dark" href="../../thuc-don.html">Xem thực đơn</a>
        </div>
      </article>
      <aside class="related">
        <p class="label">Bài khác</p>
''' + ''.join(card(o, '../') for o in others) + '''      </aside>
    </div>
  </section>

''' + relink(T_FOOT, '../../'))
    wr(url + 'index.html', html)

def build_index(published):
    posts = sorted(published, key=lambda x: x['date'], reverse=True)
    html = (T_HEAD + meta('Blog Bếp Khói – Sườn cay khổng lồ, ăn gì ở Đà Lạt',
                          'Blog của Bếp Khói Đà Lạt: giá sườn cay khổng lồ 4 size, thử thách cấp cay, món BBQ, lẩu và kinh nghiệm ăn ở quán.',
                          'blog/', 'og-trang-chu.jpg')
            + relink(T_TAIL, '../')
            + ld(crumbs([('Trang chủ', ''), ('Blog', 'blog/')]))
            + ld({"@context": "https://schema.org", "@type": "Blog", "name": "Blog Bếp Khói", "url": BASE + "blog/",
                  "inLanguage": "vi", "publisher": {"@id": BASE + "#restaurant"},
                  "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": BASE + f"blog/{p['slug']}/",
                                "datePublished": p['date']} for p in posts]})
            + '</head>\n' + nav('../')
            + page_hero('<a href="../index.html">Trang chủ</a><span>/</span>Blog', 'Blog <em>Bếp Khói</em>',
                        'Giá món, thử thách cấp cay và kinh nghiệm ăn sườn cay khổng lồ ở Đà Lạt.', '/images/hero-khoanh-khac.jpg')
            + '  <section class="section paper">\n    <div class="wrap">\n      <div class="post-grid">\n'
            + ''.join(card(p, '') for p in posts)
            + '      </div>\n    </div>\n  </section>\n\n' + relink(T_FOOT, '../'))
    wr('blog/index.html', html)

STATIC = [('', '1.0'), ('thuc-don.html', '0.9'), ('khoanh-khac.html', '0.7'), ('khong-gian.html', '0.7'),
          ('dia-chi.html', '0.8'), ('blog/', '0.7')]

def build_sitemap(published):
    rows = [f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for u, pr in STATIC]
    rows += [f"  <url><loc>{BASE}blog/{p['slug']}/</loc><lastmod>{p['date']}</lastmod><priority>0.6</priority></url>\n"
             for p in sorted(published, key=lambda x: x['date'], reverse=True)]
    wr('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + ''.join(rows) + '</urlset>\n')

def build_llms(published):
    s = rd('llms.txt')
    head = s[:s.index(f'- [Blog]({BASE}blog/)')]
    lines = ''.join(f"- [{p['title']}]({BASE}blog/{p['slug']}/)\n"
                    for p in sorted(published, key=lambda x: x['date'], reverse=True))
    wr('llms.txt', head + f'- [Blog]({BASE}blog/)\n\n## Bài viết\n' + lines)

def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')

def indexnow(urls):
    body = json.dumps({"host": "suoncaykhonglo.vn", "key": INDEXNOW_KEY,
                       "keyLocation": f"{BASE}{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            log(f'IndexNow: {r.status}')
    except Exception as e:
        log(f'IndexNow loi (khong anh huong bai da dang): {e}')

def push_with_retry():
    for attempt in range(6):
        r = git('push', '-q')
        if r.returncode == 0:
            return True
        log(f'LOI push lan {attempt + 1}: {r.stderr.strip()}')
        time.sleep(30)
    return False

def push_backlog(published):
    """Đẩy các commit đã tạo trên máy nhưng chưa lên GitHub (vd. lần trước mất mạng)."""
    ahead = git('rev-list', '--count', '@{u}..HEAD')
    if ahead.returncode != 0 or ahead.stdout.strip() in ('', '0'):
        return
    log(f'Con {ahead.stdout.strip()} commit chua len GitHub, day lai')
    if PUSH and push_with_retry():
        log('Da day bu len GitHub')
        recent = [p for p in published if p['date'] >= (datetime.date.fromisoformat(TODAY) - datetime.timedelta(days=3)).isoformat()]
        indexnow([BASE + f"blog/{p['slug']}/" for p in recent] + [BASE + 'blog/', BASE + 'sitemap.xml'])

def main():
    published = json.load(open(REG, encoding='utf-8')) if os.path.exists(REG) else []
    push_backlog(published)
    done = {p['slug'] for p in published}
    new = []
    for path in sorted(glob.glob(os.path.join(QUEUE, '*.html'))):
        p = parse(path)
        if p['date'] <= TODAY and p['slug'] not in done:
            new.append(p)
    if not new:
        log(f'Khong co bai den han (hom nay {TODAY}, da dang {len(published)} bai)')
        return
    for p in new:
        published.append({k: p[k] for k in ['date', 'slug', 'title', 'excerpt', 'cover', 'cover_alt']})
    for p in new:
        build_post(p, published)
    build_index(published)
    build_sitemap(published)
    build_llms(published)
    wr('blog/bai-viet.json', json.dumps(published, ensure_ascii=False, indent=1) + '\n')
    names = ', '.join(p['slug'] for p in new)
    log(f'Da tao {len(new)} bai: {names}')
    if not PUSH:
        log('Che do chay thu: khong commit, khong push')
        return
    git('add', '-A')
    c = git('commit', '-q', '-m', f'Đăng bài blog {TODAY}: {names}')
    if c.returncode != 0:
        log('LOI commit: ' + (c.stderr or c.stdout).strip()); sys.exit(1)
    if not push_with_retry():
        log('Chua day duoc, lan chay sau se tu day bu')
        sys.exit(1)
    log('Da push len GitHub')
    indexnow([BASE + f"blog/{p['slug']}/" for p in new] + [BASE + 'blog/', BASE + 'sitemap.xml'])

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f'LOI: {e}')
        sys.exit(1)
