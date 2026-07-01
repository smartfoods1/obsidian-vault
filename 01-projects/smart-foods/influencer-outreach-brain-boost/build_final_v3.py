#!/usr/bin/env python3
"""Build final v3 deliverable: JSON + CSV + HTML dashboard."""
import json, csv, re, html
from datetime import datetime

with open('/tmp/brain_boost_creators/sf_scored_v3.json') as f:
    scored = json.load(f)

viable = [p for p in scored if p.get('tier') in ('A','B','C')]
viable.sort(key=lambda x: (x.get('tier'), -float(x.get('brand_fit',0) or 0)))

COMP = {
    'A': '$80-150K ARS + canje (3 productos)',
    'B': '$30-60K ARS + canje (2 productos)',
    'C': 'Solo canje (1-2 productos)',
}

EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')

def extract_email(p):
    bio = p.get('biography') or ''
    m = EMAIL_RE.search(bio)
    return m.group() if m else ''

def initials(name, user):
    n = (name or user or '').strip()
    parts = n.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return (user[:2] if user else '??').upper()

def fmt_fol(n):
    if n is None: return '0'
    if n >= 1_000_000: return f'{n/1_000_000:.1f}M'
    if n >= 1_000: return f'{n/1_000:.1f}K'
    return str(n)

final = []
for p in viable:
    er = 0
    posts = p.get('recent_posts') or []
    if posts and p.get('followers'):
        likes_avg = sum(post.get('likes',0) for post in posts) / len(posts)
        er = round(likes_avg / p['followers'] * 100, 2)
    final.append({
        'tier': p['tier'],
        'source': 'sf_followers_v3',
        'username': p['username'],
        'ig_url': f"https://instagram.com/{p['username']}",
        'full_name': p.get('full_name',''),
        'followers': p.get('followers') or 0,
        'engagement_rate': er,
        'creator_type': p.get('creator_type',''),
        'brand_fit': float(p.get('brand_fit',0) or 0),
        'is_content_creator': p.get('is_content_creator'),
        'creator_evidence': p.get('creator_evidence',''),
        'argentina': p.get('argentina'),
        'ar_evidence': p.get('ar_evidence',''),
        'fit_reason': p.get('fit_reason',''),
        'red_flags': '; '.join(p.get('red_flags') or []),
        'compensation_suggested': COMP[p['tier']],
        'outreach_hook': p.get('outreach_hook',''),
        'tier_reason': p.get('tier_reason',''),
        'email': extract_email(p),
        'external_url': p.get('external_url',''),
        'biography': (p.get('biography') or '')[:300],
        'category': p.get('category',''),
        'is_business': p.get('is_business'),
        'is_verified': p.get('is_verified'),
    })

# Save JSON
out_dir = '/Users/specialandres/obsidian-vault/01-projects/smart-foods/influencer-outreach-brain-boost'
import os
os.makedirs(out_dir, exist_ok=True)

with open(f'{out_dir}/creators_v3.json','w') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

# CSV
csv_cols = ['tier','username','ig_url','full_name','followers','engagement_rate','creator_type','brand_fit',
            'argentina','ar_evidence','fit_reason','red_flags','compensation_suggested','outreach_hook',
            'tier_reason','email','external_url','biography']
with open(f'{out_dir}/creators_v3.csv','w') as f:
    w = csv.DictWriter(f, fieldnames=csv_cols, extrasaction='ignore')
    w.writeheader()
    for r in final: w.writerow(r)

# HTML dashboard
cards_js = json.dumps([{
    'tier': L['tier'],
    'source': L['source'],
    'username': L['username'],
    'ig_url': L['ig_url'],
    'full_name': L['full_name'],
    'followers': L['followers'],
    'followers_fmt': fmt_fol(L['followers']),
    'er': L['engagement_rate'],
    'fit': L['brand_fit'],
    'niche': L['creator_type'],
    'fit_reason': L['fit_reason'],
    'ar': L['argentina'],
    'ar_evidence': L['ar_evidence'],
    'comp': L['compensation_suggested'],
    'hook': L['outreach_hook'],
    'email': L['email'],
    'web': L['external_url'],
    'bio': L['biography'],
    'tier_reason': L['tier_reason'],
    'creator_evidence': L['creator_evidence'],
    'is_verified': L['is_verified'],
    'initials': initials(L['full_name'], L['username']),
} for L in final], ensure_ascii=False)

total = len(final)
by_tier = {'A':[], 'B':[], 'C':[]}
for L in final:
    by_tier[L['tier']].append(L)
ar_yes = sum(1 for L in final if L['argentina'] == 'confirmado')
ar_unc = sum(1 for L in final if L['argentina'] == 'unclear')

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Brain Boost — Creator Outreach AR v3</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ --beige:#F1EADF; --beige-dark:#D9D0B6; --black:#282823; --sage:#A0B8A0; --forest:#4B6834; --lime:#E0E938; --gray:#6b6b66; --line:rgba(40,40,35,0.08); }}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--beige);color:var(--black);line-height:1.5;padding:24px}}
.wrap{{max-width:1280px;margin:0 auto}}
header{{margin-bottom:32px}}
h1{{font-family:Georgia,'Times New Roman',serif;font-size:36px;font-weight:600;letter-spacing:-0.02em;margin-bottom:8px}}
.subtitle{{font-size:15px;color:var(--gray);margin-bottom:20px}}
.banner{{background:linear-gradient(135deg,#fff3a8,#E0E938);padding:14px 18px;border-radius:12px;font-size:13px;margin-bottom:20px;border:1px solid var(--forest)}}
.banner b{{color:var(--forest)}}
.stats{{display:flex;gap:24px;flex-wrap:wrap;margin-bottom:20px}}
.stat{{background:white;border-radius:12px;padding:14px 18px;border:1px solid var(--line)}}
.stat .n{{font-size:24px;font-weight:700;color:var(--forest)}}
.stat .l{{font-size:12px;color:var(--gray);text-transform:uppercase;letter-spacing:0.05em}}
.controls{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;align-items:center}}
.filter-pill{{background:white;border:1px solid var(--line);border-radius:999px;padding:8px 16px;font-size:13px;font-weight:500;cursor:pointer;transition:all 0.15s;user-select:none}}
.filter-pill:hover{{background:var(--beige-dark)}}
.filter-pill.active{{background:var(--forest);color:white;border-color:var(--forest)}}
.search{{flex:1;min-width:220px;padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:white;font-size:14px;font-family:inherit}}
.sort-sel{{padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:white;font-size:13px;font-family:inherit;cursor:pointer}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:18px}}
.card{{background:white;border-radius:16px;padding:22px;border:1px solid var(--line);transition:transform 0.15s,box-shadow 0.15s;display:flex;flex-direction:column;gap:14px}}
.card:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(40,40,35,0.06)}}
.card.contacted{{opacity:0.55;background:#f6f4ee}}
.card-header{{display:flex;align-items:flex-start;gap:14px}}
.avatar{{width:48px;height:48px;border-radius:50%;background:var(--sage);color:white;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;flex-shrink:0}}
.card-id{{flex:1;min-width:0}}
.username{{font-weight:700;font-size:16px;color:var(--forest);text-decoration:none}}
.username:hover{{text-decoration:underline}}
.fullname{{font-size:13px;color:var(--gray);margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.tier-badge{{padding:4px 10px;border-radius:6px;font-size:11px;font-weight:700;letter-spacing:0.05em}}
.tier-A{{background:var(--lime);color:var(--black)}}
.tier-B{{background:#fff3a8;color:var(--black)}}
.tier-C{{background:var(--beige-dark);color:var(--black)}}
.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;background:var(--beige);padding:12px;border-radius:10px}}
.metric{{text-align:center}}
.metric .v{{font-size:16px;font-weight:700;color:var(--black)}}
.metric .k{{font-size:10px;text-transform:uppercase;color:var(--gray);letter-spacing:0.05em}}
.tags{{display:flex;gap:6px;flex-wrap:wrap}}
.tag{{padding:3px 8px;border-radius:6px;font-size:11px;background:var(--beige);color:var(--gray)}}
.tag.ar-confirmado{{background:var(--sage);color:white}}
.tag.ar-unclear{{background:#ffd980;color:var(--black)}}
.tag.creator{{background:var(--forest);color:white}}
.reason{{font-size:13px;color:var(--gray);font-style:italic;border-left:2px solid var(--sage);padding-left:10px}}
.evidence{{font-size:11px;color:var(--gray);background:var(--beige);padding:6px 10px;border-radius:6px}}
.evidence b{{color:var(--forest)}}
.hook-block{{background:linear-gradient(135deg,#fafaf3,#f0eee0);padding:14px;border-radius:10px;border:1px dashed var(--sage)}}
.hook-label{{font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:var(--forest);font-weight:700;margin-bottom:6px}}
.hook-text{{font-size:13px;line-height:1.5}}
.actions{{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}}
.btn{{padding:8px 14px;border-radius:8px;border:1px solid var(--line);background:white;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;text-decoration:none;color:var(--black);display:inline-flex;align-items:center;gap:6px;transition:all 0.15s}}
.btn:hover{{background:var(--beige)}}
.btn.primary{{background:var(--forest);color:white;border-color:var(--forest)}}
.btn.primary:hover{{background:var(--black)}}
.btn.active{{background:var(--lime);border-color:var(--lime)}}
.compensation{{font-size:12px;color:var(--forest);font-weight:600}}
.contact-row{{font-size:12px;color:var(--gray);display:flex;gap:10px;flex-wrap:wrap}}
.contact-row a{{color:var(--forest);text-decoration:none}}
.contact-row a:hover{{text-decoration:underline}}
.empty{{grid-column:1/-1;text-align:center;padding:48px;color:var(--gray);background:white;border-radius:12px}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--black);color:var(--lime);padding:12px 20px;border-radius:8px;font-size:13px;font-weight:600;opacity:0;transition:opacity 0.2s;pointer-events:none;z-index:100}}
.toast.show{{opacity:1}}
footer{{margin-top:48px;text-align:center;color:var(--gray);font-size:12px}}
@media (max-width:600px){{body{{padding:14px}}h1{{font-size:26px}}.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Brain Boost — Creator Outreach AR <span style="font-size:14px;color:var(--forest);font-weight:600">v3</span></h1>
  <div class="subtitle">{total} creators argentinos validados con 3 gates (is_creator → argentina → fit) · {datetime.now().strftime('%Y-%m-%d')}</div>
  <div class="banner">
    <b>Pipeline v3:</b> 5020 followers de @smartfoods.ar → 1693 públicos → 439 enriquecidos → 202 micro (1K-50K) → <b>{total} pasaron 3 gates Gemini estrictos</b> (83% descarte por NO ser content creator)
  </div>
  <div class="stats">
    <div class="stat"><div class="n">{total}</div><div class="l">Total</div></div>
    <div class="stat"><div class="n">{len(by_tier['A'])}</div><div class="l">Tier A</div></div>
    <div class="stat"><div class="n">{len(by_tier['B'])}</div><div class="l">Tier B</div></div>
    <div class="stat"><div class="n">{len(by_tier['C'])}</div><div class="l">Tier C</div></div>
    <div class="stat"><div class="n">{ar_yes}</div><div class="l">AR confirmado</div></div>
    <div class="stat"><div class="n">{ar_unc}</div><div class="l">AR verificar</div></div>
    <div class="stat"><div class="n" id="stat-contacted">0</div><div class="l">Contactados</div></div>
  </div>
  <div class="controls">
    <div class="filter-pill active" data-filter="all">Todos</div>
    <div class="filter-pill" data-filter="A">Tier A</div>
    <div class="filter-pill" data-filter="B">Tier B</div>
    <div class="filter-pill" data-filter="C">Tier C</div>
    <div class="filter-pill" data-filter="ar-confirmado">AR ✓</div>
    <div class="filter-pill" data-filter="ar-unclear">AR verificar</div>
    <div class="filter-pill" data-filter="founder">Founders</div>
    <div class="filter-pill" data-filter="pending">Pendientes</div>
    <input type="text" class="search" placeholder="Buscar nombre, nicho, bio…" id="search">
    <select class="sort-sel" id="sort">
      <option value="fit">Sort: Fit ↓</option>
      <option value="er">Sort: ER ↓</option>
      <option value="followers">Sort: Followers ↓</option>
      <option value="followers-asc">Sort: Followers ↑</option>
    </select>
  </div>
</header>
<div class="grid" id="grid"></div>
<footer>Smart Foods · Brain Boost outreach v3 · pipeline 5020→27 con triple gate Gemini · estado en localStorage</footer>
</div>
<div class="toast" id="toast"></div>
<script>
const LEADS = {cards_js};
const STORAGE = 'bb_creators_v3_state';
let state = JSON.parse(localStorage.getItem(STORAGE) || '{{}}');
let activeFilter = 'all';
let searchQ = '';
let sortKey = 'fit';

function save() {{ localStorage.setItem(STORAGE, JSON.stringify(state)); updateStats(); }}
function updateStats() {{
  document.getElementById('stat-contacted').textContent = LEADS.filter(L => state[L.username]?.contacted).length;
}}
function toast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1800);
}}
function render() {{
  const grid = document.getElementById('grid');
  let items = LEADS.filter(L => {{
    if (['A','B','C'].includes(activeFilter)) {{ if (L.tier !== activeFilter) return false; }}
    else if (activeFilter === 'ar-confirmado') {{ if (L.ar !== 'confirmado') return false; }}
    else if (activeFilter === 'ar-unclear') {{ if (L.ar !== 'unclear') return false; }}
    else if (activeFilter === 'founder') {{ if (!L.niche.includes('founder')) return false; }}
    else if (activeFilter === 'pending') {{ if (state[L.username]?.contacted) return false; }}
    if (searchQ) {{
      const hay = (L.username + ' ' + L.full_name + ' ' + L.niche + ' ' + L.bio + ' ' + L.fit_reason).toLowerCase();
      if (!hay.includes(searchQ.toLowerCase())) return false;
    }}
    return true;
  }});
  items.sort((a,b) => {{
    if (sortKey === 'fit') return b.fit - a.fit;
    if (sortKey === 'er') return b.er - a.er;
    if (sortKey === 'followers') return b.followers - a.followers;
    if (sortKey === 'followers-asc') return a.followers - b.followers;
    return 0;
  }});
  if (items.length === 0) {{ grid.innerHTML = '<div class="empty">No hay creators con estos filtros</div>'; return; }}
  grid.innerHTML = items.map(L => {{
    const st = state[L.username] || {{}};
    const contactedClass = st.contacted ? 'contacted' : '';
    const contactedBtn = st.contacted ? '✓ Contactado' : '○ Marcar contactado';
    const contactedActive = st.contacted ? 'active' : '';
    const escHook = L.hook.replace(/"/g,'&quot;').replace(/'/g,'&apos;');
    const verifiedBadge = L.is_verified ? '<span style="margin-left:6px;color:#1da1f2">✓</span>' : '';
    return `
      <div class="card ${{contactedClass}}" data-user="${{L.username}}">
        <div class="card-header">
          <div class="avatar">${{L.initials}}</div>
          <div class="card-id">
            <a class="username" href="${{L.ig_url}}" target="_blank">@${{L.username}}</a>${{verifiedBadge}}
            <div class="fullname">${{L.full_name || '—'}}</div>
          </div>
          <div class="tier-badge tier-${{L.tier}}">Tier ${{L.tier}}</div>
        </div>
        <div class="metrics">
          <div class="metric"><div class="v">${{L.followers_fmt}}</div><div class="k">followers</div></div>
          <div class="metric"><div class="v">${{L.er}}%</div><div class="k">engagement</div></div>
          <div class="metric"><div class="v">${{L.fit}}/10</div><div class="k">brand fit</div></div>
        </div>
        <div class="tags">
          <span class="tag ar-${{L.ar}}">AR ${{L.ar === 'confirmado' ? '✓' : '?'}}</span>
          <span class="tag creator">${{L.niche}}</span>
        </div>
        <div class="reason">${{L.fit_reason}}</div>
        <div class="evidence"><b>AR:</b> ${{L.ar_evidence || '—'}} · <b>Creator:</b> ${{L.creator_evidence || '—'}}</div>
        <div class="compensation">💰 ${{L.comp}}</div>
        <div class="hook-block">
          <div class="hook-label">Ángulo DM personalizado</div>
          <div class="hook-text">${{L.hook}}</div>
        </div>
        <div class="contact-row">
          ${{L.email ? `<a href="mailto:${{L.email}}">✉ ${{L.email}}</a>` : ''}}
          ${{L.web ? `<a href="${{L.web}}" target="_blank">🔗 web</a>` : ''}}
        </div>
        <div class="actions">
          <a class="btn primary" href="${{L.ig_url}}" target="_blank">Abrir IG</a>
          <button class="btn" onclick="copyHook(this, '${{escHook}}')">📋 Copiar hook</button>
          <button class="btn ${{contactedActive}}" onclick="toggleContacted('${{L.username}}', this)">${{contactedBtn}}</button>
        </div>
      </div>
    `;
  }}).join('');
}}
function copyHook(btn, text) {{
  navigator.clipboard.writeText(text).then(() => {{
    toast('Hook copiado');
    btn.textContent = '✓ Copiado';
    setTimeout(() => btn.textContent = '📋 Copiar hook', 1500);
  }});
}}
function toggleContacted(user, btn) {{
  state[user] = state[user] || {{}};
  state[user].contacted = !state[user].contacted;
  save();
  toast(state[user].contacted ? `Marcado @${{user}}` : `Desmarcado @${{user}}`);
  render();
}}
document.querySelectorAll('.filter-pill').forEach(p => {{
  p.addEventListener('click', () => {{
    document.querySelectorAll('.filter-pill').forEach(x => x.classList.remove('active'));
    p.classList.add('active');
    activeFilter = p.dataset.filter;
    render();
  }});
}});
document.getElementById('search').addEventListener('input', e => {{ searchQ = e.target.value; render(); }});
document.getElementById('sort').addEventListener('change', e => {{ sortKey = e.target.value; render(); }});
updateStats();
render();
</script>
</body>
</html>"""

with open(f'{out_dir}/dashboard_v3.html','w') as f:
    f.write(HTML)

print(f'Wrote {len(final)} creators to:')
print(f'  {out_dir}/dashboard_v3.html')
print(f'  {out_dir}/creators_v3.csv')
print(f'  {out_dir}/creators_v3.json')
print(f'Tiers: A={len(by_tier["A"])}, B={len(by_tier["B"])}, C={len(by_tier["C"])}')
print(f'AR: confirmado={ar_yes}, unclear={ar_unc}')
