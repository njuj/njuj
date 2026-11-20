"""Generates the static animated panels in assets/ (intro, lab, orbit, case files, footer).  Run: python scripts/gen_profile.py assets
Pure SVG: SMIL + CSS keyframes, no JS (GitHub strips scripts)."""
import math, random, sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1])
FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
BG, LINE, DIM, TXT = "#0b0f17", "#1b2533", "#6e7681", "#c9d1d9"
GREEN, CYAN, RED, GOLD, VIOLET = "#00ff9c", "#00e5ff", "#ff0055", "#ffd166", "#b388ff"
rnd = random.Random(1337)


def fade(t, body):
    return f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>{body}</g>'


# ---------------------------------------------------------------- lab.svg
def lab():
    W, H = 900, 470
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" xml:space="preserve" style="white-space:pre">',
         '<defs><style>.blink{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}'
         '.scan{animation:s 3.2s linear infinite}@keyframes s{0%{transform:translateY(0)}100%{transform:translateY(330px)}}'
         '.pulse{animation:p 1.6s ease-in-out infinite}@keyframes p{50%{opacity:.25}}'
         '.beat{animation:hb 2.4s ease-in-out infinite}@keyframes hb{0%,100%{opacity:.15}12%{opacity:.55}24%{opacity:.2}36%{opacity:.5}}'
         '.glitch{animation:gl 7s steps(1) infinite}@keyframes gl{0%,93%,100%{transform:none;opacity:1}94%{transform:translate(-6px,2px);opacity:.6}95%{transform:translate(5px,-1px)}96%{transform:translate(-2px,0);opacity:.85}}'
         '.whisper{animation:w 9s steps(1) infinite}@keyframes w{0%,78%,86%,100%{opacity:0}79%,81%,83%{opacity:.9}80%,82%{opacity:.2}}'
         '.flash{animation:f 7s steps(1) infinite}@keyframes f{0%,93%,97%,100%{opacity:0}94%{opacity:.18}95%{opacity:.05}96%{opacity:.12}}</style>'
         f'<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#ff0033" stop-opacity="0"/><stop offset="1" stop-color="#ff0033" stop-opacity=".5"/></radialGradient>'
         f'<pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern>'
         f'<linearGradient id="sg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".18"/></linearGradient>'
         f'<pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{GREEN}" stroke-opacity=".04"/></pattern></defs>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="{LINE}"/><rect width="{W}" height="{H}" rx="12" fill="url(#g)"/>',
         f'<path d="M.5 12.5a12 12 0 0 1 12-12h{W-25}a12 12 0 0 1 12 12v24h-{W-1}z" fill="#0f1520"/><line x1=".5" y1="36.5" x2="{W-.5}" y2="36.5" stroke="{LINE}"/>',
         '<circle cx="22" cy="18.5" r="6" fill="#ff5f56"/><circle cx="42" cy="18.5" r="6" fill="#ffbd2e"/><circle cx="62" cy="18.5" r="6" fill="#27c93f"/>',
         f'<text x="{W/2}" y="23" text-anchor="middle" font-size="12" fill="{DIM}">unmask — dissecting FpsBooster_v2.1.zip — never executed</text>',
         f'<text x="{W-18}" y="23" text-anchor="end" font-size="11" fill="{RED}" class="pulse">● REC</text>']

    # left: the delivery chain, stage by stage
    o.append(f'<text x="28" y="66" font-size="11" letter-spacing="3" fill="{CYAN}">// DELIVERY CHAIN</text>')
    stages = [("FpsBooster_v2.1.zip", "ZIP · 2 files", TXT),
              ("FpsBooster.exe", ".NET · bait assembly", TXT),
              ("Resources.resources", "2 entries · 1 blob 58 KB", TXT),
              ("icon_data", "XOR · 12-byte key recovered", GOLD),
              ("njRAT 0.7d", "config decrypted ✖", RED)]
    t = 0.6
    for i, (name, info, col) in enumerate(stages):
        y = 92 + i * 66
        if i:
            o.append(f'<line x1="44" y1="{y-50}" x2="44" y2="{y-16}" stroke="{CYAN}" stroke-opacity=".6" stroke-dasharray="34" stroke-dashoffset="34">'
                     f'<animate attributeName="stroke-dashoffset" to="0" begin="{t-.35:.2f}s" dur=".35s" fill="freeze"/></line>')
        node = (f'<circle cx="44" cy="{y}" r="13" fill="{BG}" stroke="{col}" stroke-width="1.6"/>'
                f'<text x="44" y="{y+4.5}" text-anchor="middle" font-size="12" font-weight="700" fill="{col}">{i+1}</text>'
                f'<text x="70" y="{y-2}" font-size="15" font-weight="700" fill="{col}">{esc(name)}</text>'
                f'<text x="70" y="{y+16}" font-size="11.5" fill="{DIM}">{esc(info)}</text>')
        if i == len(stages) - 1:
            node += f'<circle cx="44" cy="{y}" r="13" fill="none" stroke="{RED}" class="pulse"><animate attributeName="r" values="13;22;13" dur="1.6s" repeatCount="indefinite"/></circle>'
        o.append(fade(t, node))
        t += 0.75

    # right: hex dump that resolves into the decrypted configuration
    X0 = 440
    o.append(f'<line x1="{X0-16}" y1="52" x2="{X0-16}" y2="{H-58}" stroke="{LINE}"/>')
    o.append(f'<text x="{X0}" y="66" font-size="11" letter-spacing="3" fill="{CYAN}">// CONFIG · AES / XOR → PLAINTEXT</text>')
    o.append(f'<g clip-path="inset(0)"><rect class="scan" x="{X0-10}" y="52" width="{W-X0-8}" height="38" fill="url(#sg)"/></g>')
    fields = [("C2", "kira-lab-c2[.]ddns[.]net:5552", RED),
              ("Victim tag", "HacKed", TXT),
              ("Mutex", "q8R2vT6yN4kP1mXw", TXT),
              ("Installs as", "%AppData%\\Windows Update.exe", TXT),
              ("Persistence", "Run key · Startup copy", GOLD),
              ("BSOD on kill", "yes", GOLD),
              ("Telegram bot", "not used", DIM),
              ("Provider", "No-IP · dynamic DNS", CYAN)]
    t0 = t - 0.3
    for i, (k, v, col) in enumerate(fields):
        y = 98 + i * 34
        ft = t0 + i * 0.32
        o.append(fade(ft - .4, f'<text x="{X0}" y="{y}" font-size="11.5" fill="{DIM}">{esc(k)}</text>'))
        # three frames of noise, then the value
        n = max(len(v), 8)
        frames = ["".join(rnd.choice("0123456789abcdef") for _ in range(n)) for _ in range(3)]
        for j, fr in enumerate(frames):
            a, b = ft - .4 + j * .13, ft - .4 + (j + 1) * .13
            o.append(f'<text x="{X0+128}" y="{y}" font-size="13.5" fill="{DIM}" opacity="0">{fr}'
                     f'<set attributeName="opacity" to="1" begin="{a:.2f}s"/><set attributeName="opacity" to="0" begin="{b:.2f}s" fill="freeze"/></text>')
        o.append(fade(ft, f'<text x="{X0+128}" y="{y}" font-size="13.5" font-weight="700" fill="{col}">{esc(v)}</text>'))

    # footer: the take-down
    te = t0 + len(fields) * .32 + .5
    fy = H - 34
    o.append(f'<line x1=".5" y1="{fy-24}" x2="{W-.5}" y2="{fy-24}" stroke="{LINE}"/>')
    o.append(fade(te, f'<text x="28" y="{fy}" font-size="13.5"><tspan fill="{GREEN}" font-weight="700">[✓] </tspan>'
                      f'<tspan fill="{TXT}">report </tspan><tspan fill="{RED}" font-weight="700">kira-lab-c2[.]ddns[.]net</tspan>'
                      f'<tspan fill="{TXT}"> → No-IP abuse · all victims cut off</tspan></text>'))
    o.append(fade(te + .6, f'<text x="{W-28}" y="{fy}" text-anchor="end" font-size="13.5" fill="{GREEN}">no hack-back <tspan class="blink">█</tspan></text>'))
    # horror layer: everything above glitches, scanlines, a heartbeat of red at the edges
    body = "".join(o[1:])
    o = [o[0], f'<g class="glitch">{body}</g>',
         f'<rect width="{W}" height="{H}" rx="12" fill="url(#crt)" pointer-events="none"/>',
         f'<rect width="{W}" height="{H}" rx="12" fill="url(#vig)" class="beat"/>',
         f'<rect width="{W}" height="{H}" rx="12" fill="{RED}" class="flash"/>',
         f'<text x="{W/2}" y="{H/2+8}" text-anchor="middle" font-size="30" font-weight="800" fill="{RED}" letter-spacing="8" class="whisper">IT RAN WHILE YOU SLEPT</text>',
         '</svg>']
    return "".join(o)


# ---------------------------------------------------------------- orbit.svg
def hexa(cx, cy, r):
    """A hexagon: the background is a chip-like lattice of them."""
    return " ".join(f"{cx + r * math.cos(math.pi / 3 * k + math.pi / 6):.1f},{cy + r * math.sin(math.pi / 3 * k + math.pi / 6):.1f}" for k in range(6))


def orbit():
    W, H, CX, CY = 980, 640, 490, 330
    inner = [("REVERSE ENGINEERING", "IDA · x64dbg · dnSpy · Ghidra", RED),
             ("MALWARE ANALYSIS", "njRAT · XWorm · loaders", RED),
             ("DFIR", "event logs · memory · hooks", CYAN),
             ("WINDOWS INTERNALS", "kernel drivers · BYOVD", CYAN),
             ("TOOL BUILDING", "15 zero-dep tools", GREEN)]
    outer = [("BUG BOUNTY", "web appsec · Burp", GOLD),
             ("AI SECURITY", "prompt injection · slop", VIOLET),
             ("VM LABS", "Kali · Arch · VirtualBox", GREEN),
             ("SECOND BRAIN", "Obsidian · 3k-node galaxy", VIOLET),
             ("CTF & CRACKMES", "HTB · THM · crackmes.one", GOLD),
             ("FULL-STACK", "PHP · React · Node", CYAN),
             ("nyx CYBERTOOL", "100 tools · one terminal", GREEN)]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<defs><style>.spin{animation:r 120s linear infinite;transform-origin:490px 330px}.rspin{animation:r 80s linear infinite reverse;transform-origin:490px 330px}'
         '@keyframes r{to{transform:rotate(360deg)}}.glow{animation:g 3s ease-in-out infinite}@keyframes g{50%{opacity:.35}}</style>'
         f'<radialGradient id="core"><stop offset="0" stop-color="{RED}" stop-opacity=".45"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient></defs>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{LINE}"/>',
         f'<text x="28" y="38" font-size="11" letter-spacing="3" fill="{GOLD}">// OBSESSIONS · what I break, build and study</text>']
    # background: a slowly turning lattice of hexagons, like a die shot
    o.append('<g class="spin" opacity=".55">')
    for ring, (rr, n, size) in enumerate(((0, 1, 46), (128, 8, 22), (232, 16, 18), (330, 24, 16))):
        for k in range(n):
            a = 2 * math.pi * k / n + ring * .2
            x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
            o.append(f'<polygon points="{hexa(x, y, size)}" fill="none" stroke="{GOLD}" stroke-opacity="{.22 - ring*.04:.2f}"/>')
    o.append('</g>')
    # orbits
    for r, col, cls in ((166, CYAN, "spin"), (290, VIOLET, "rspin")):
        o.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{col}" stroke-opacity=".18" stroke-dasharray="2 6"/>')
        o.append(f'<g class="{cls}"><circle cx="{CX + r}" cy="{CY}" r="3" fill="{col}"/><circle cx="{CX - r}" cy="{CY}" r="2" fill="{col}" opacity=".6"/></g>')
    # core
    o.append(f'<circle cx="{CX}" cy="{CY}" r="70" fill="url(#core)" class="glow"/>')
    o.append(f'<polygon points="{hexa(CX, CY, 48)}" fill="{BG}" stroke="{RED}" stroke-width="1.5"/>')
    # the eye: lids close every few seconds, the iris drifts as if it follows you
    o.append(f'<g><animateTransform attributeName="transform" type="scale" additive="sum" values="1 1;1 1;1 .05;1 1;1 1" keyTimes="0;.9;.94;.98;1" dur="5s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 0;0 {CY*.95:.1f};0 0;0 0" keyTimes="0;.9;.94;.98;1" dur="5s" repeatCount="indefinite"/>'
             f'<path d="M{CX-36},{CY} Q{CX},{CY-30} {CX+36},{CY} Q{CX},{CY+30} {CX-36},{CY}Z" fill="#160208" stroke="{RED}" stroke-width="1.4"/>'
             f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-9 -2;-9 -2;8 2;8 2;0 0" keyTimes="0;.15;.4;.55;.85;1" dur="9s" repeatCount="indefinite"/>'
             f'<circle cx="{CX}" cy="{CY}" r="12" fill="{RED}" opacity=".85"/><circle cx="{CX}" cy="{CY}" r="5" fill="#000"/><circle cx="{CX+4}" cy="{CY-4}" r="1.8" fill="#fff" opacity=".8"/></g></g>')
    o.append(f'<text x="{CX}" y="{CY+66}" text-anchor="middle" font-size="13" font-weight="800" fill="{RED}" letter-spacing="6" class="glow">KIRA</text>')
    o.append(f'<text x="{CX}" y="{CY+82}" text-anchor="middle" font-size="9.5" fill="{DIM}" letter-spacing="2">i see every process you run</text>')

    def nodes(items, rx, ry, start, t0):
        out, t = [], t0
        for i, (title, sub, col) in enumerate(items):
            a = start + 2 * math.pi * i / len(items)
            x, y = CX + rx * math.cos(a), CY + ry * math.sin(a)
            dist = math.hypot(x - CX, y - CY) - 50
            out.append(f'<line x1="{CX + 50*math.cos(a):.1f}" y1="{CY + 50*math.sin(a):.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-opacity=".35" '
                       f'stroke-dasharray="{dist:.0f}" stroke-dashoffset="{dist:.0f}"><animate attributeName="stroke-dashoffset" to="0" begin="{t:.2f}s" dur=".5s" fill="freeze"/></line>')
            # a packet that keeps flowing out along the spoke
            out.append(f'<circle r="2.2" fill="{col}" opacity="0"><set attributeName="opacity" to=".9" begin="{t+.5:.2f}s" fill="freeze"/>'
                       f'<animateMotion path="M{CX:.1f},{CY:.1f} L{x:.1f},{y:.1f}" dur="{2.2 + i*.17:.2f}s" begin="{t+.5:.2f}s" repeatCount="indefinite"/></circle>')
            anchor = "middle" if abs(math.cos(a)) < .3 else ("start" if math.cos(a) > 0 else "end")
            dx = 0 if anchor == "middle" else (12 if anchor == "start" else -12)
            dy = -16 if (anchor == "middle" and math.sin(a) < 0) else (26 if anchor == "middle" else 4)
            out.append(fade(t + .4, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{BG}" stroke="{col}" stroke-width="1.6"/>'
                                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{col}" class="glow"/>'
                                    f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}" font-size="12.5" font-weight="700" fill="{col}" letter-spacing="1">{esc(title)}</text>'
                                    f'<text x="{x+dx:.1f}" y="{y+dy+15:.1f}" text-anchor="{anchor}" font-size="10.5" fill="{DIM}">{esc(sub)}</text>'))
            t += .28
        return out, t

    a, t = nodes(inner, 200, 132, -math.pi / 2, .5)
    b, _ = nodes(outer, 330, 250, -math.pi / 4, t)
    o += a + b
    o.append(f'<text x="{W-28}" y="{H-22}" text-anchor="end" font-size="11" fill="{DIM}">0x4B495241 · rendered as pure SVG</text>')
    o.append('</svg>')
    return "".join(o)


(OUT / "lab.svg").write_text(lab(), encoding="utf-8", newline="\n")
(OUT / "orbit.svg").write_text(orbit(), encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- intro.svg
def emblem(t0=0.2):
    """KIRA emblem in a 460x460 box: hexagon, K, a red eye where the arms meet. Draws itself in from t0 seconds."""
    C, JX, JY = 230, 206, 222
    hexp = lambda R: " ".join(f"{C+R*math.cos(math.radians(-90+60*i)):.1f},{C+R*math.sin(math.radians(-90+60*i)):.1f}" for i in range(6))
    ticks = "".join(
        f'<line x1="{C+196*math.cos(a):.1f}" y1="{C+196*math.sin(a):.1f}" x2="{C+(206 if i % 5 else 214)*math.cos(a):.1f}" y2="{C+(206 if i % 5 else 214)*math.sin(a):.1f}" '
        f'stroke="{GREEN}" stroke-opacity="{.25 if i % 5 else .6}" stroke-width="2"/>' for i in range(60) for a in [math.radians(i * 6)])
    return (f'<defs><linearGradient id="e-ink" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>'
            f'<clipPath id="e-hx"><polygon points="{hexp(176)}"/></clipPath><clipPath id="e-band"><rect x="0" y="112" width="460" height="232"/></clipPath>'
            f'<filter id="e-glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<radialGradient id="e-core"><stop offset="0" stop-color="{RED}" stop-opacity=".4"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient></defs>'
            + fade(t0, f'<g>{ticks}<animateTransform attributeName="transform" type="rotate" from="0 {C} {C}" to="360 {C} {C}" dur="60s" repeatCount="indefinite"/></g>')
            + f'<polygon points="{hexp(186)}" fill="#0a0f16" stroke="url(#e-ink)" stroke-width="7" stroke-linejoin="round" filter="url(#e-glow)" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
              f'<animate attributeName="stroke-dashoffset" to="0" begin="{t0:.2f}s" dur="1.2s" fill="freeze"/></polygon>'
            + f'<polygon points="{hexp(168)}" fill="none" stroke="{GREEN}" stroke-opacity=".25" stroke-width="1.5" stroke-dasharray="6 6"/>'
            + fade(t0 + 1.1, f'<g clip-path="url(#e-hx)"><g filter="url(#e-glow)" clip-path="url(#e-band)" class="jit">'
                             f'<rect x="146" y="112" width="44" height="232" fill="url(#e-ink)"/>'
                             f'<line x1="{JX}" y1="{JY}" x2="330" y2="98" stroke="url(#e-ink)" stroke-width="42"/>'
                             f'<line x1="{JX}" y1="{JY}" x2="335" y2="358" stroke="url(#e-ink)" stroke-width="42"/></g></g>')
            + fade(t0 + 1.9, f'<circle cx="{JX}" cy="{JY+4}" r="70" fill="url(#e-core)" class="beat"/>'
                             f'<g transform="translate({JX} {JY+4})"><g><animateTransform attributeName="transform" type="scale" values="1 0;1 1;1 1;1 .05;1 1" keyTimes="0;.06;.92;.96;1" dur="6s" begin="{t0+1.9:.2f}s" repeatCount="indefinite"/>'
                             f'<g transform="translate({-JX} {-JY-4})" filter="url(#e-glow)">'
                             f'<path d="M{JX-52} {JY+4} Q{JX} {JY-38} {JX+52} {JY+4} Q{JX} {JY+46} {JX-52} {JY+4}Z" fill="#06080d" stroke="{RED}" stroke-width="5"/>'
                             f'<g><circle cx="{JX}" cy="{JY+4}" r="16" fill="{RED}"/><ellipse cx="{JX}" cy="{JY+4}" rx="4.5" ry="12" fill="#06080d"/><circle cx="{JX+6}" cy="{JY-3}" r="3" fill="#fff" opacity=".85"/>'
                             f'<animateTransform attributeName="transform" type="translate" values="0 0;-14 0;-14 0;12 0;12 0;0 0" keyTimes="0;.1;.4;.5;.8;1" dur="7s" repeatCount="indefinite"/></g>'
                             f'</g></g></g>')
            + fade(t0 + 2.4, f'<text x="{C}" y="388" text-anchor="middle" font-size="17" font-weight="700" letter-spacing="9" fill="{GREEN}" opacity=".85">KIRA</text>'
                             f'<text x="{C}" y="86" text-anchor="middle" font-size="11" letter-spacing="3" fill="{RED}" opacity=".8">0x4B495241</text>'))


def intro():
    W, H, FX, FY = 900, 320, 190, 160
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<defs><style>'
         '.rain{animation:rn 6s linear infinite}@keyframes rn{from{transform:translateY(-320px)}to{transform:translateY(320px)}}'
         '.scanl{animation:sl 2.2s ease-in-out 3 alternate forwards}@keyframes sl{from{transform:translateY(-70px)}to{transform:translateY(70px)}}'
         '.jit{animation:j 4s steps(1) infinite}@keyframes j{0%,88%,100%{transform:none}89%{transform:translate(-4px,1px)}91%{transform:translate(3px,-2px)}93%{transform:translate(-1px,0)}}'
         '.rgbr{animation:jr 4s steps(1) infinite}@keyframes jr{0%,88%,100%{transform:translate(0,0);opacity:0}89%,93%{transform:translate(5px,0);opacity:.8}}'
         '.rgbc{animation:jc 4s steps(1) infinite}@keyframes jc{0%,88%,100%{transform:translate(0,0);opacity:0}89%,93%{transform:translate(-5px,0);opacity:.8}}'
         '.blink{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}'
         '.beat{animation:hb 2.4s ease-in-out infinite}@keyframes hb{0%,100%{opacity:.12}12%{opacity:.45}24%{opacity:.15}36%{opacity:.4}}'
         '</style>'
         f'<radialGradient id="vig" r=".8"><stop offset=".5" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".45"/></radialGradient>'
         f'<pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".4"/></pattern>'
         f'<clipPath id="fp"><polygon points="{" ".join(f"{FX+80*math.cos(math.radians(-90+60*i)):.1f},{FY+80*math.sin(math.radians(-90+60*i)):.1f}" for i in range(6))}"/></clipPath></defs>',
         f'<rect width="{W}" height="{H}" rx="14" fill="#06080d"/>']
    # hex rain: columns of bytes falling, dim red, brighter heads
    for c in range(0, W, 26):
        col = "".join(f'<tspan x="{c+6}" dy="16">{rnd.randrange(256):02X}</tspan>' for _ in range(40))
        delay, dur = -rnd.random() * 6, 4 + rnd.random() * 5
        o.append(f'<text class="rain" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s" y="0" font-size="11" fill="{RED}" opacity="{.08 + rnd.random()*.14:.2f}">{col}</text>')
    # the KIRA emblem builds itself, the eye opens, then the scanner checks it
    o.append(f'<g transform="translate({FX-230*.4:.1f} {FY-230*.4:.1f}) scale(.4)">{emblem()}</g>')
    o.append(f'<g clip-path="url(#fp)"><rect class="scanl" x="{FX-70}" y="{FY-2}" width="140" height="4" fill="{CYAN}" opacity=".9"><set attributeName="opacity" to="0" begin="6.5s" fill="freeze"/></rect></g>')
    # status lines under the print
    steps = [(.6, "VERIFYING SIGNATURE", DIM), (2.4, "MATCHING 1,337,420 RECORDS", DIM), (4.4, "MATCH · 99.97%", GOLD), (5.2, "IDENTITY CONFIRMED", GREEN)]
    for i, (t, s, col) in enumerate(steps):
        o.append(fade(t, f'<text x="{FX}" y="{FY + 124 + 0*i}" text-anchor="middle" font-size="11" letter-spacing="2" fill="{col}">{s}</text>'
                         + (f'<set attributeName="opacity" to="0" begin="{steps[i+1][0]:.2f}s" fill="freeze"/>' if i < len(steps) - 1 else '')))
    # name: RGB-split glitch
    nx, ny = 560, 150
    name = f'font-size="92" font-weight="800" letter-spacing="14" text-anchor="middle"'
    o.append(fade(5.4, f'<g class="jit"><text class="rgbr" x="{nx}" y="{ny}" {name} fill="{RED}">KIRA</text>'
                       f'<text class="rgbc" x="{nx}" y="{ny}" {name} fill="{CYAN}">KIRA</text>'
                       f'<text x="{nx}" y="{ny}" {name} fill="#e9edf2">KIRA</text></g>'))
    o.append(fade(6.0, f'<text x="{nx}" y="{ny+38}" text-anchor="middle" font-size="13" letter-spacing="3" fill="{TXT}">MALWARE HUNTER · REVERSE ENGINEER · DFIR</text>'
                       f'<text x="{nx}" y="{ny+58}" text-anchor="middle" font-size="13" letter-spacing="3" fill="{DIM}">BUG HUNTER · WEB DEV · VIBE CODER · TOOL BUILDER</text>'))
    o.append(fade(6.6, f'<text x="{nx}" y="{ny+100}" text-anchor="middle" font-size="12" letter-spacing="4" fill="{GREEN}">ACCESS GRANTED <tspan class="blink">█</tspan></text>'))
    o.append(fade(0, f'<text x="24" y="28" font-size="10.5" letter-spacing="2" fill="{RED}">● SESSION 0x4B495241 · TRACE ACTIVE</text>'))
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#crt)"/><rect width="{W}" height="{H}" rx="14" fill="url(#vig)" class="beat"/>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/></svg>')
    return "".join(o)


# ---------------------------------------------------------------- case files
CASES = [("unmask", "RAT CONFIGS", "Fake cheats that drop njRAT / XWorm", "Unwraps every stage, decrypts the C2 config", "30 tests · never runs the sample"),
         ("ghost-hunter", "MEMORY FORENSICS", "Code injected into running processes", "Shellcode, hollowing, hooks, stomped modules", "28 tests · read-only"),
         ("driver-guard", "KERNEL · BYOVD", "Signed drivers used to kill antivirus", "LOLDrivers by file + Authenticode hash", "14 tests · hash matches Windows"),
         ("evtx-hunter", "DFIR · EVENT LOGS", "Attackers hiding in Windows logs", "Own .evtx parser, ATT&CK rules, hidden records", "39 tests · zero deps"),
         ("panoptes", "NETWORK · C2", "Beacons, DGAs, DNS exfiltration", "Every lookup and the program behind it", "21 tests · DNS trap"),
         ("unwrap", "DEOBFUSCATION", "Obfuscated PowerShell, JS, VBS, batch", "Peels it layer by layer, never executes", "95 tests · checked vs real interpreters")]


def case(n, name, area, subject, method, status, accent):
    W, H = 600, 230
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<defs><style>.stamp{animation:st .35s cubic-bezier(.2,1.6,.4,1) both;animation-delay:2.6s;transform-origin:500px 60px}'
         '@keyframes st{from{transform:rotate(-14deg) scale(2.4);opacity:0}to{transform:rotate(-14deg) scale(1);opacity:.85}}</style></defs>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="#0d1018" stroke="{LINE}"/>',
         f'<path d="M0 14a14 14 0 0 1 14-14h150l18 20H{W-14}a14 14 0 0 1 14 14v10H0z" fill="#121726"/>',
         f'<text x="22" y="24" font-size="10.5" letter-spacing="3" fill="{DIM}">CASE FILE #{n:03d} · {esc(area)}</text>',
         f'<rect x="0" y="40" width="4" height="{H-40}" fill="{accent}"/>',
         f'<text x="26" y="78" font-size="28" font-weight="800" fill="#e9edf2">{esc(name)}</text>']
    rows = [("SUBJECT", subject), ("METHOD", method), ("STATUS", status)]
    for i, (k, v) in enumerate(rows):
        y = 116 + i * 30
        o.append(f'<text x="26" y="{y}" font-size="10.5" letter-spacing="2" fill="{DIM}">{k}</text>')
        o.append(f'<text x="118" y="{y}" font-size="13" fill="{TXT if i < 2 else GREEN}">{esc(v)}</text>')
        wbar = min(9 * len(v) + 8, 460)
        o.append(f'<rect x="114" y="{y-14}" width="{wbar}" height="19" fill="#000"><animate attributeName="width" from="{wbar}" to="0" begin="{.6 + i*.6:.1f}s" dur=".45s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".7 0 .3 1"/></rect>')
    o.append(f'<g class="stamp"><rect x="430" y="40" width="140" height="40" rx="4" fill="none" stroke="{RED}" stroke-width="3"/>'
             f'<text x="500" y="67" text-anchor="middle" font-size="17" font-weight="800" letter-spacing="3" fill="{RED}">CLASSIFIED</text></g>')
    o.append(f'<text x="{W-22}" y="{H-16}" text-anchor="end" font-size="11" fill="{DIM}">open file ↗</text></svg>')
    return "".join(o)


# ---------------------------------------------------------------- footer
def footer():
    W, H = 900, 150
    msg = "THE LOGS NEVER LIE"
    hexmsg = " ".join(f"{ord(c):02X}" for c in msg)
    flat = f"M40 70 H360 l10 -26 l10 52 l10 -40 l8 14 H{W-40}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">'
            '<defs><style>.blink{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}</style></defs>'
            f'<rect width="{W}" height="{H}" rx="14" fill="#06080d"/>'
            f'<path d="{flat}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="1100" stroke-dashoffset="1100" opacity=".8">'
            f'<animate attributeName="stroke-dashoffset" to="0" dur="2.6s" begin=".2s" fill="freeze"/></path>'
            + fade(2.9, f'<text x="{W/2}" y="112" text-anchor="middle" font-size="15" font-weight="800" letter-spacing="6" fill="{RED}">CONNECTION TERMINATED <tspan class="blink">_</tspan></text>')
            + fade(3.6, f'<text x="{W/2}" y="134" text-anchor="middle" font-size="10.5" letter-spacing="2" fill="#3a4250">{hexmsg}</text>')
            + f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/></svg>')


for i, (name, area, subj, meth, stat) in enumerate(CASES, 1):
    (OUT / f"case-{name}.svg").write_text(case(i, name, area, subj, meth, stat, [RED, RED, GREEN, CYAN, VIOLET, GOLD][i - 1]), encoding="utf-8", newline="\n")
(OUT / "intro.svg").write_text(intro(), encoding="utf-8", newline="\n")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8", newline="\n")
print("ok")
