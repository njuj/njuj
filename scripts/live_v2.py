"""KIRA live panels (v2 look): heartbeat.svg, infection.svg, bodycount.svg from real GitHub data.

Run daily by .github/workflows/live.yml after scripts/live.py. Locally: GH_TOKEN=... python scripts/live_v2.py assets/v2
Standard library only. Output SVGs: no script, no external reference, CSS animation only, reduced-motion aware.
"""
import datetime, json, math, os, sys, urllib.request
from pathlib import Path

USER = "njuj"
Q = """query($u:String!){user(login:$u){followers{totalCount}
  contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}
  repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){totalCount nodes{name stargazerCount}}}}"""


def fetch():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": Q, "variables": {"u": USER}}).encode(),
                                 {"Authorization": f"bearer {tok}", "Content-Type": "application/json", "User-Agent": "profile-live"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"graphql: {data['errors']}")
    return data["data"]["user"]


OBS, GRA, TIT, IVW, IV, MUT, RULE, RULE2 = "#050505", "#191919", "#9BAAB5", "#D8D2C4", "#F1EFE7", "#8E8C86", "#2A2A28", "#3A3A38"
CRIM = "#B3123A"
CRIM_T = "#E0566F"  # crimson for small text on obsidian (5.6:1)
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif"
MONO = "ui-monospace,'Cascadia Mono','SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

DARK = dict(bg=OBS, ink=IV, ink2=IVW, mut=MUT, rule=RULE2, fib=(IV, IVW, TIT), dust=IV, pupil="#000",
            metal=((0, "#7d858b"), (.28, "#f4f1ea"), (.5, "#a9b4bc"), (.64, "#fbfaf6"), (1, "#5f666b")), crim=CRIM, crim_t=CRIM_T)

RM = ("@media (prefers-reduced-motion:reduce){*{animation:none!important}.rm{opacity:1!important}.rmh{display:none!important}}")

FLOW = "@keyframes flow{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}"
FADE = "@keyframes fade{from{opacity:0}to{opacity:1}}"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def n(x):
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def metal(id_, pal, x2=0, y2=1):
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in pal["metal"])
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{st}</linearGradient>'


def doc(w, h, title, desc, body, style="", defs="", pal=DARK, frame=True, rx=20):
    fr = f'<rect width="{w}" height="{h}" rx="{rx}" fill="{pal["bg"]}"/>' if frame else ""
    bd = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{pal["rule"]}"/>' if frame else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<defs><style>text{{font-family:{MONO}}}.s{{font-family:{SERIF}}}{style}{RM}</style>{defs}</defs>'
            f'{fr}{body}{bd}</svg>\n')


def t(x, y, s, size=12, fill=IVW, anchor="start", ls=0, cls="", extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{n(x)}" y="{n(y)}" font-size="{size}" fill="{fill}"{a}{l}{c}{extra}>{s}</text>'


def blur(id_, s):
    return f'<filter id="{id_}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>'


def smooth(pts):
    """Catmull-Rom through pts as relative cubic Béziers on an integer grid (small files, no drift)."""
    if len(pts) < 2:
        return ""
    R_ = lambda p: (round(p[0]), round(p[1]))
    cur = R_(pts[0])
    d = [f"M{cur[0]} {cur[1]}c"]
    seg = []
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = R_((p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6))
        c2 = R_((p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6))
        e = R_(p2)
        seg.append(f"{c1[0]-cur[0]} {c1[1]-cur[1]} {c2[0]-cur[0]} {c2[1]-cur[1]} {e[0]-cur[0]} {e[1]-cur[1]}")
        cur = e
    return d[0] + " ".join(seg).replace(" -", "-")


def warp(px, py, mx, my, strength, reach, swirl):
    dx, dy = px - mx, py - my
    rr = math.hypot(dx, dy) + 1e-6
    f = math.exp(-rr / reach)
    nr = rr * (1 - strength * f)
    a = math.atan2(dy, dx) + swirl * f
    return mx + math.cos(a) * nr, my + math.sin(a) * nr


def grid(x0, y0, x1, y1, step, mx, my, strength, reach, swirl, pal, width=.6, op=.35, samples=14):
    lines = []
    def run(pts):
        return smooth([warp(x, y, mx, my, strength, reach, swirl) for x, y in pts])
    y = y0
    while y <= y1 + .1:
        lines.append(run([(x0 + (x1 - x0) * k / samples, y) for k in range(samples + 1)]))
        y += step
    x = x0
    while x <= x1 + .1:
        lines.append(run([(x, y0 + (y1 - y0) * k / samples) for k in range(samples + 1)]))
        x += step
    return f'<path d="{"".join(lines)}" fill="none" stroke="{pal["fib"][2]}" stroke-width="{width}" opacity="{op}"/>'



def streaks(counts):
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, tail = 0, counts[:-1] if counts and not counts[-1] else counts
    for c in reversed(tail):
        if not c:
            break
        cur += 1
    return cur, longest


assert streaks([1, 1, 0, 1, 1, 1]) == (3, 3) and streaks([1, 1, 1, 0]) == (3, 3) and streaks([0, 0]) == (0, 0)


def head(label, title, W, right=""):
    return (t(36, 40, label, 11, MUT, ls=3) + t(36, 76, title, 30, IV, cls="s") +
            (t(W - 36, 40, right, 11, IVW, "end", 2) if right else "") +
            f'<line x1="36" y1="92" x2="{W-36}" y2="92" stroke="{RULE2}"/>')


def heartbeat(days):
    W, H, N, base = 900, 250, 60, 180
    days = days[-N:]
    step = (W - 72) / N
    d, x = [f"M36 {base}"], 36.0
    for day in days:  # same beat geometry as live.py: one beat per day with commits, relative segments sum to 0
        c = day["contributionCount"]
        if c:
            h = 14 + min(c, 25) * 2.6
            d.append(f"H{x+step*.25:.1f} l{step*.08:.1f} -5 l{step*.08:.1f} 5 l{step*.08:.1f} 8 l{step*.1:.1f} -{h+8:.1f} l{step*.1:.1f} {h+16:.1f} l{step*.08:.1f} -16")
        x += step
        d.append(f"H{x:.1f}")
    path = " ".join(d)
    last = next((dd["date"] for dd in reversed(days) if dd["contributionCount"]), "never")
    today = days[-1]["contributionCount"]
    status = (f'<tspan fill="{IV}">ALIVE</tspan> · {today} commits today' if today else
              f'<tspan fill="{CRIM_T}">FLATLINE</tspan> · last signal {last}')
    ticks = "".join(f'<line x1="{n(36+i*step*5)}" y1="{base+22}" x2="{n(36+i*step*5)}" y2="{base+28}" stroke="{RULE2}"/>' for i in range(N // 5 + 1))
    body = (head("§ 02 · VITALS · LAST 60 DAYS · 1 BEAT = 1 DAY OF COMMITS", "Vitals", W, status) + ticks +
            f'<line x1="36" y1="{base}" x2="{W-36}" y2="{base}" stroke="{RULE2}" stroke-dasharray="1 5"/>'
            f'<g opacity=".55">{grid(0, 100, W, H - 30, 30, W - 60, base, .3, 140, .4, DARK, .5, .22)}</g>'
            f'<path d="{path}" fill="none" stroke="{IV}" stroke-width="5" opacity=".22" filter="url(#hb)"/>'
            + "".join(f'<path d="{path}" transform="translate(0 {dy})" fill="none" stroke="url(#hm)" stroke-width="{w}" opacity="{o}" stroke-linejoin="round"/>'
                      for dy, w, o in ((-2.2, .5, .35), (2.4, .5, .3), (-1, .7, .6), (1.1, .6, .5), (0, 1.3, 1))) +
            f'<path class="pl" d="{path}" pathLength="1000" fill="none" stroke="{IV}" stroke-width="2.2" stroke-linejoin="round" stroke-dasharray="70 930"/>'
            + t(36, H - 16, "each beat is a real day · the light travels the last sixty", 10.5, MUT))
    style = FLOW + ".pl{animation:flow 8s linear infinite}"
    return doc(W, H, "Vitals: heartbeat from the last 60 days of commits",
               f"An ECG line with one beat per day that had commits. Status: {'ALIVE' if today else 'FLATLINE, last signal ' + last}.",
               body, style, metal("hm", DARK, 1, 0) + blur("hb", 3))



def level(c, peak):
    return 0 if not c else 1 + min(3, int(4 * c / (peak + 1)))


def infection(weeks):
    S, G, T = 12, 3, 12
    W = 72 + len(weeks) * (S + G)
    H = 7 * (S + G) + 150
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1)
    calm = ["#141414", "#3a4248", "#5f6c74", "#8f9ea8", "#d9dfe3"]
    ox, oy = len(weeks) * .55, 3  # patient zero, as in live.py
    maxd = math.hypot(max(ox, len(weeks) - ox), 4)
    B = 24
    cells, waves = [], [[] for _ in range(B)]
    for i, w in enumerate(weeks):
        for d in w["contributionDays"]:
            j = datetime.date.fromisoformat(d["date"]).isoweekday() % 7
            lv = level(d["contributionCount"], peak)
            b = min(B - 1, int(B * math.hypot(i - ox, j - oy) / maxd))
            px0, py0 = 36 + ox * (S + G) + S / 2, 110 + oy * (S + G) + S / 2
            wx, wy = warp(36 + i * (S + G) + S / 2, 110 + j * (S + G) + S / 2, px0, py0, .22, 130, .3)
            cells.append(f'<rect class="l{lv}" x="{wx-S/2:.1f}" y="{wy-S/2:.1f}" width="{S}" height="{S}" rx="2">'
                         f'<title>{d["date"]}: {d["contributionCount"]}</title></rect>')
            waves[b].append(f"M{wx-S/2:.1f} {wy-S/2:.1f}h{S}v{S}h-{S}z")
    px, py = 36 + ox * (S + G) + S / 2, 110 + oy * (S + G) + S / 2
    R = maxd * (S + G)
    # infected at delay, purged by the expanding containment ring half a cycle later
    # cells stay static; one overlay path per distance band (24) animates opacity + fill
    style = ("".join(f".l{k}{{fill:{c}}}" for k, c in enumerate(calm)) +
             "@keyframes inf{0%{opacity:0;fill:" + CRIM + "}3%,46%{opacity:1;fill:" + CRIM + "}49%{opacity:1;fill:" + IV + "}54%,100%{opacity:0;fill:" + IV + "}}" +
             f".wv{{opacity:0;pointer-events:none;animation:inf {T}s linear infinite}}" +
             "".join(f".d{b}{{animation-delay:{b/B*T*.4:.2f}s}}" for b in range(B) if waves[b]) +
             f"@keyframes ring{{0%,49%{{transform:scale(0);opacity:0}}50%{{opacity:.9}}90%{{transform:scale(1);opacity:.6}}91%,100%{{transform:scale(1);opacity:0}}}}"
             f".rg{{animation:ring {T}s linear infinite;transform-origin:{n(px)}px {n(py)}px}}")
    overlay = "".join(f'<path class="wv d{b} rmh" d="{"".join(w)}"/>' for b, w in enumerate(waves) if w)
    body = (head("§ 07 · CONTAINMENT GRID · ONE YEAR OF COMMITS", "Containment", W,
                 f'<tspan fill="{CRIM_T}">● OUTBREAK</tspan> → <tspan fill="{IV}">PURGED</tspan>') +
            f'<clipPath id="cg"><rect x="30" y="104" width="{W-60}" height="{7*(S+G)+12}"/></clipPath>' + "".join(cells) + overlay +
            f'<g clip-path="url(#cg)"><circle class="rg rmh" cx="{n(px)}" cy="{n(py)}" r="{n(R)}" fill="none" stroke="{IV}" stroke-width="1.5"/></g>'
            f'<circle cx="{n(px)}" cy="{n(py)}" r="2" fill="{CRIM}"/>'
            + t(36, H - 20, "infection spreads from patient zero · the containment ring purges it · every cell is a real day", 10.5, MUT))
    return doc(W, H, "Containment grid: one year of commits",
               "A year of commits as a grid. A crimson infection spreads from patient zero, then an expanding containment ring purges it.",
               body, style)


def bodycount(user, counts, profile_repo="njuj"):
    cal = user["contributionsCollection"]["contributionCalendar"]
    repos = user["repositories"]
    stars = sum(x["stargazerCount"] for x in repos["nodes"])
    cur, best = streaks(counts)
    # the profile README repo (named after the account) is not a tool: 16 public repos = 15 tools + njuj/njuj
    tools = sum(1 for x in repos["nodes"] if x.get("name", "").lower() != profile_repo)
    stats = [("TOOLS BUILT", tools), ("STARS", stars), ("COMMITS / YEAR", cal["totalContributions"]),
             ("STREAK", cur), ("LONGEST", best)]
    if "followers" in user:  # optional: needs followers{totalCount} in the query; replaces the shields.io followers badge
        stats.append(("FOLLOWERS", user["followers"]["totalCount"]))
    W, H = 900, 290
    cw = (W - 72) / len(stats)
    out, css = [], []
    for k, (label, v) in enumerate(stats):
        cx = 36 + cw * k + cw / 2
        frames = [round(v * f) for f in (.1, .3, .55, .8, .95, 1)]
        for f_, val in enumerate(frames):
            t0 = .3 + k * .15 + f_ * .12
            last = f_ == len(frames) - 1
            cls = f"c{k}{f_}"
            css.append(f".{cls}{{animation:{'fade .2s' if last else 'fr .12s'} linear {t0:.2f}s {'both' if last else ''}}}")
            out.append(t(cx, 176, val, 44, IV if label not in ("STREAK", "LONGEST") else CRIM_T, "middle",
                         cls=f"s {cls} {'rm' if last else 'rmh'}", extra=' opacity="0"'))
        frac = min(1.0, math.log10(v + 1) / 3)  # orbital gauge: 1 → 1000 on a log scale
        circ = 2 * math.pi * 50
        out.append(f'<circle cx="{n(cx)}" cy="160" r="50" fill="none" stroke="{RULE2}" stroke-dasharray="1 3"/>'
                   f'<circle class="ga" cx="{n(cx)}" cy="160" r="50" fill="none" stroke="url(#gm)" stroke-width="1.6" stroke-linecap="round" '
                   f'stroke-dasharray="{circ*frac:.1f} {circ:.1f}" transform="rotate(-90 {n(cx)} 160)" style="--o:{circ*frac:.1f}"/>'
                   f'<circle cx="{n(cx + 50*math.sin(frac*2*math.pi))}" cy="{n(160 - 50*math.cos(frac*2*math.pi))}" r="2.6" fill="{IV}"/>')
        out.append(t(cx, 236, label, 10.5, MUT, "middle", 2))
    body = (head("§ 07 · BODY COUNT", "Body count", W) + "".join(out) +
            t(W / 2, 270, f'<tspan fill="{IV}">0</tspan> runtime dependencies · <tspan fill="{IV}">0</tspan> samples executed · '
              f'<tspan fill="{CRIM_T}">∞</tspan> logs read', 12, IVW, "middle", 2))
    style = (FADE + "@keyframes fr{from,to{opacity:1}}" + "".join(css) +
             "@keyframes ga{from{stroke-dashoffset:var(--o)}to{stroke-dashoffset:0}}.ga{animation:ga 2.4s cubic-bezier(.2,.7,.2,1) .3s both}")
    return doc(W, H, "Body count", "Live statistics: " + ", ".join(f"{l.lower()} {v}" for l, v in stats) +
               ". Zero runtime dependencies, zero samples executed.", body, style, metal("gm", DARK))


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/v2")
    user = fetch()
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    for name, text in (("heartbeat", heartbeat(days)), ("infection", infection(weeks)),
                       ("bodycount", bodycount(user, [d["contributionCount"] for d in days]))):
        (out / f"{name}.svg").write_text(text, encoding="utf-8", newline="\n")
    print("ok", len(days), "days")
