"""Generates assets/lab.svg and assets/orbit.svg.  Run: python scripts/gen_profile.py assets
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
print("ok")
