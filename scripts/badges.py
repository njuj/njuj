"""Rebuilds the ARSENAL badge block in README.md. Official logos (assets/logos, one-colour masks) are recoloured per row."""
import base64, io, re, urllib.parse
from pathlib import Path

LOGOS = Path(__file__).resolve().parent.parent / "assets" / "logos"  # official logos as one-colour masks

G = {  # 24x24 stroke glyph for tools with no logo of their own
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
}


def badge(name, color, logo):
    if (LOGOS / f"{logo}.png").exists():
        from PIL import Image
        m = Image.open(LOGOS / f"{logo}.png").getchannel("A")
        im = Image.new("RGBA", m.size, tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) + (255,)); im.putalpha(m)
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        lg = urllib.parse.quote("data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), safe="")
    elif (LOGOS / f"{logo}.svg").exists():
        svg = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', f'fill="#{color}"', (LOGOS / f"{logo}.svg").read_text(encoding="utf-8"))
        lg = urllib.parse.quote("data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode(), safe="")
    elif logo in G:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{G[logo]}</svg>'
        lg = urllib.parse.quote("data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode(), safe="")
    else:
        lg = f"{logo}&logoColor={color}"
    return f'  <img src="https://img.shields.io/badge/{name}-0b0f17?style=for-the-badge&logo={lg}" alt="{name.replace("--", "-").replace("_", " ")}"/>'


ROWS = [
    ("ff0055", [("x86--64_ASM", "chip"), ("IDA", "ida"), ("x64dbg", "x64dbg"), ("Ghidra", "ghidra"), ("dnSpy", "dotnet"), ("Detect_It_Easy", "die"), ("YARA", "yara")]),
    ("00e5ff", [("Volatility", "volatility"), ("Sysinternals", "sysinternals"), ("CyberChef", "cyberchef"), ("Nmap", "nmap"), ("Metasploit", "metasploit"), ("VirusTotal", "virustotal")]),
    ("00ff9c", [("Kali_Linux", "kalilinux"), ("Arch_Linux", "archlinux"), ("VirtualBox", "virtualbox"), ("Wireshark", "wireshark"), ("Burp_Suite", "burpsuite"), ("Obsidian", "obsidian")]),
    ("b388ff", [("Claude_Code", "claude"), ("Codex", "openai"), ("Hermes_Agent", "hermes"), ("Cursor", "cursor"), ("MCP", "modelcontextprotocol"), ("GitHub_Actions", "githubactions")]),
]
block = '<p align="center">\n' + "\n  <br/>\n".join("\n".join(badge(n, c, l) for n, l in row) for c, row in ROWS) + "\n</p>"
s = open("README.md", encoding="utf-8").read()
s, n = re.subn(r'<p align="center">\n  <img src="https://img\.shields\.io/badge/x86--64_ASM.*?</p>', lambda m: block, s, flags=re.S)
assert n == 1
open("README.md", "w", encoding="utf-8", newline="\n").write(s)
print("ok")
