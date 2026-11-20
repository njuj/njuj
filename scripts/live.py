"""Live panels from real GitHub data: heartbeat.svg, infection.svg, bodycount.svg.

Run daily by .github/workflows/live.yml. Locally: GH_TOKEN=$(gh auth token) python scripts/live.py assets
Standard library only.
"""
import json, math, os, sys, urllib.request
from pathlib import Path

USER = "njuj"
FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
LINE, DIM, TXT = "#1b2533", "#6e7681", "#c9d1d9"
GREEN, CYAN, RED, GOLD = "#00ff9c", "#00e5ff", "#ff0055", "#ffd166"
Q = """query($u:String!){user(login:$u){
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


def streaks(counts):
    """(current, longest). Today may still be empty, so the current streak may end yesterday."""
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


def svg(w, h, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
            f'<defs><style>{style}</style></defs><rect width="{w}" height="{h}" rx="14" fill="#06080d"/>{body}'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/></svg>')


def heartbeat(days):
    W, H, N, base = 900, 190, 60, 120
    days = days[-N:]
    step = (W - 60) / N
    d, x = [f"M30 {base}"], 30.0
    for day in days:
        c = day["contributionCount"]
        if c:
            h = 14 + min(c, 25) * 2.6
            d.append(f"H{x+step*.25:.1f} l{step*.08:.1f} -5 l{step*.08:.1f} 5 l{step*.08:.1f} 8 l{step*.1:.1f} -{h+8:.1f} l{step*.1:.1f} {h+16:.1f} l{step*.08:.1f} -16")
        x += step
        d.append(f"H{x:.1f}")
    path = " ".join(d)
    last = next((dd["date"] for dd in reversed(days) if dd["contributionCount"]), "never")
    today = days[-1]["contributionCount"]
    status = (f'<tspan fill="{GREEN}">ALIVE</tspan> · {today} commits today' if today else
              f'<tspan fill="{RED}">FLATLINE</tspan> · last signal {last}')
    grid = "".join(f'<line x1="{30+i*step*5:.1f}" y1="40" x2="{30+i*step*5:.1f}" y2="170" stroke="{RED}" stroke-opacity=".07"/>' for i in range(N // 5 + 1))
    body = (grid +
            f'<text x="30" y="30" font-size="11" letter-spacing="3" fill="{DIM}">VITALS · LAST {N} DAYS · 1 BEAT = 1 DAY OF COMMITS</text>'
            f'<text x="{W-30}" y="30" text-anchor="end" font-size="11" letter-spacing="2" fill="{TXT}">{status}</text>'
            f'<path d="{path}" fill="none" stroke="{RED}" stroke-width="5" opacity=".18"/>'
            f'<path class="ecg" d="{path}" fill="none" stroke="{RED}" stroke-width="2" stroke-linejoin="round" pathLength="1000"/>'
            f'<circle r="4" fill="#fff"><animateMotion dur="7s" repeatCount="indefinite" path="{path}" keyPoints="0;1;1" keyTimes="0;.8;1" calcMode="linear"/>'
            f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.8;.81;1" dur="7s" repeatCount="indefinite"/></circle>')
    style = ('.ecg{stroke-dasharray:1000;animation:draw 7s linear infinite}'
             '@keyframes draw{0%{stroke-dashoffset:1000}80%{stroke-dashoffset:0}100%{stroke-dashoffset:0;opacity:0}}')
    return svg(W, H, body, style)


def level(c, peak):
    return 0 if not c else 1 + min(3, int(4 * c / (peak + 1)))


def infection(weeks):
    S, G = 13, 3
    W, H = 30 * 2 + len(weeks) * (S + G), 7 * (S + G) + 90
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1)
    calm = ["#141a24", "#0b4a3a", "#0a7a58", "#00b87a", GREEN]
    hot = ["#3a0614", "#80002a", "#b3003b", "#e0004a", RED]
    ox, oy = len(weeks) * 0.55, 3  # patient zero
    maxd = math.hypot(max(ox, len(weeks) - ox), 4)
    cells = []
    for i, w in enumerate(weeks):
        for d in w["contributionDays"]:
            j = int(__import__("datetime").date.fromisoformat(d["date"]).isoweekday() % 7)
            lv = level(d["contributionCount"], peak)
            a = .05 + .4 * math.hypot(i - ox, j - oy) / maxd
            b = .55 + .3 * i / len(weeks)
            kt = f"0;{a:.3f};{a+.02:.3f};{b:.3f};{b+.02:.3f};{b+.05:.3f};1"
            vals = f"{calm[lv]};{calm[lv]};{hot[lv]};{hot[lv]};{CYAN};{calm[lv]};{calm[lv]}"
            cells.append(f'<rect x="{30+i*(S+G)}" y="{50+j*(S+G)}" width="{S}" height="{S}" rx="3" fill="{calm[lv]}">'
                         f'<title>{d["date"]}: {d["contributionCount"]}</title>'
                         f'<animate attributeName="fill" values="{vals}" keyTimes="{kt}" dur="9s" repeatCount="indefinite"/></rect>')
    sweep_x0, sweep_x1 = 30, 30 + len(weeks) * (S + G)
    body = (f'<text x="30" y="32" font-size="11" letter-spacing="3" fill="{DIM}">CONTAINMENT GRID · ONE YEAR OF COMMITS</text>'
            f'<text x="{W-30}" y="32" text-anchor="end" font-size="11" letter-spacing="2" fill="{RED}">● OUTBREAK <tspan fill="{DIM}">→</tspan> <tspan fill="{CYAN}">PURGED</tspan></text>'
            + "".join(cells) +
            f'<rect y="44" width="3" height="{7*(S+G)+6}" fill="{CYAN}" opacity="0"><animate attributeName="x" values="{sweep_x0};{sweep_x0};{sweep_x1};{sweep_x1}" keyTimes="0;.55;.85;1" dur="9s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;.9;.9;0;0" keyTimes="0;.549;.55;.85;.851;1" dur="9s" repeatCount="indefinite"/></rect>'
            f'<text x="30" y="{H-18}" font-size="10.5" fill="{DIM}">infection spreads from patient zero · the scanner cleans it · every cell is a real day</text>')
    return svg(W, H, body)


def bodycount(user, counts):
    cal = user["contributionsCollection"]["contributionCalendar"]
    repos = user["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    cur, best = streaks(counts)
    stats = [("TOOLS BUILT", repos["totalCount"], GREEN), ("STARS", stars, GOLD), ("COMMITS / YEAR", cal["totalContributions"], CYAN),
             ("STREAK", cur, RED), ("LONGEST", best, RED)]
    W, H = 900, 170
    cw = (W - 60) / len(stats)
    out = []
    for k, (label, n, col) in enumerate(stats):
        cx = 30 + cw * k + cw / 2
        # count-up: a few frames shown one after another
        frames = [round(n * f) for f in (.1, .3, .55, .8, .95, 1)]
        for f, v in enumerate(frames):
            t0, t1 = .3 + k * .15 + f * .12, .3 + k * .15 + (f + 1) * .12
            hide = '' if f == len(frames) - 1 else f'<set attributeName="opacity" to="0" begin="{t1:.2f}s" fill="freeze"/>'
            out.append(f'<text x="{cx:.0f}" y="88" text-anchor="middle" font-size="40" font-weight="800" fill="{col}" opacity="0">{v}'
                       f'<set attributeName="opacity" to="1" begin="{t0:.2f}s" fill="freeze"/>{hide}</text>')
        out.append(f'<text x="{cx:.0f}" y="112" text-anchor="middle" font-size="10.5" letter-spacing="2" fill="{DIM}">{label}</text>')
        if k:
            out.append(f'<line x1="{30+cw*k:.0f}" y1="50" x2="{30+cw*k:.0f}" y2="112" stroke="{LINE}"/>')
    body = (f'<text x="30" y="30" font-size="11" letter-spacing="3" fill="{DIM}">BODY COUNT</text>' + "".join(out) +
            f'<text x="{W/2}" y="148" text-anchor="middle" font-size="12" letter-spacing="2" fill="{TXT}">'
            f'<tspan fill="{GREEN}">0</tspan> runtime dependencies · <tspan fill="{GREEN}">0</tspan> samples executed · '
            f'<tspan fill="{RED}">∞</tspan> logs read</text>')
    return svg(W, H, body)


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
    user = fetch()
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    for name, text in (("heartbeat", heartbeat(days)), ("infection", infection(weeks)),
                       ("bodycount", bodycount(user, [d["contributionCount"] for d in days]))):
        (out / f"{name}.svg").write_text(text, encoding="utf-8", newline="\n")
    print("ok", len(days), "days")
