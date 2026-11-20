"""Rebuilds the ARSENAL badge block in README.md. Tools without a simple-icons logo get a small drawn glyph (data URI)."""
import base64, re, urllib.parse

G = {  # 24x24 stroke glyphs
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "lens": '<circle cx="10" cy="10" r="6"/><path d="M14.5 14.5L21 21M7 10h6"/>',
    "bug": '<rect x="8" y="7" width="8" height="13" rx="4"/><path d="M12 7V3M8 11H3M8 16H3M16 11h5M16 16h5M5 6l3 3M19 6l-3 3"/>',
    "graph": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M11 7.5L6 16.5M13 7.5l5 9M7.5 19h9"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2"/><path d="M12 1v5M12 18v5M1 12h5M18 12h5"/>',
    "braces": '<path d="M9 3H8a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5a2 2 0 0 0 2 2h1M15 3h1a2 2 0 0 1 2 2v4a2 2 0 0 0 2 2 2 2 0 0 0-2 2v5a2 2 0 0 1-2 2h-1"/>',
    "ram": '<rect x="2" y="7" width="20" height="9" rx="1"/><path d="M6 10v3M10 10v3M14 10v3M18 10v3M5 16v3M19 16v3"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9L7 7M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    "chef": '<path d="M7 14a4 4 0 1 1 1.5-7.7 4.5 4.5 0 0 1 8 0A4 4 0 1 1 17 14v6H7zM7 17h10"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "prompt": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M6 9l3 3-3 3M11 15h6"/>',
    "wing": '<path d="M3 19c7-1 13-5 18-14-3 1.5-6 1.5-8 .5 1 2 0 4-2 5 1 1 .5 3-1.5 4-2 .5-4 2-6.5 4.5zM8 15l4-3M11 12.5l4-4"/>',
}


def badge(name, color, logo):
    if logo in G:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{G[logo]}</svg>'
        lg = urllib.parse.quote("data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode(), safe="")
    else:
        lg = f"{logo}&logoColor={color}"
    return f'  <img src="https://img.shields.io/badge/{name}-0b0f17?style=for-the-badge&logo={lg}" alt="{name.replace("--", "-").replace("_", " ")}"/>'


ROWS = [
    ("ff0055", [("x86--64_ASM", "chip"), ("IDA", "lens"), ("x64dbg", "bug"), ("Ghidra", "graph"), ("dnSpy", "dotnet"), ("Detect_It_Easy", "target"), ("YARA", "braces")]),
    ("00e5ff", [("Volatility", "ram"), ("Sysinternals", "gear"), ("CyberChef", "chef"), ("Nmap", "eye"), ("Metasploit", "metasploit"), ("VirusTotal", "virustotal")]),
    ("00ff9c", [("Kali_Linux", "kalilinux"), ("Arch_Linux", "archlinux"), ("VirtualBox", "virtualbox"), ("Wireshark", "wireshark"), ("Burp_Suite", "burpsuite"), ("Obsidian", "obsidian")]),
    ("b388ff", [("Claude_Code", "claude"), ("Codex", "prompt"), ("Hermes_Agent", "wing"), ("Cursor", "cursor"), ("MCP", "modelcontextprotocol"), ("GitHub_Actions", "githubactions")]),
]
block = '<p align="center">\n' + "\n  <br/>\n".join("\n".join(badge(n, c, l) for n, l in row) for c, row in ROWS) + "\n</p>"
s = open("README.md", encoding="utf-8").read()
s, n = re.subn(r'<p align="center">\n  <img src="https://img\.shields\.io/badge/x86--64_ASM.*?</p>', lambda m: block, s, flags=re.S)
assert n == 1
open("README.md", "w", encoding="utf-8", newline="\n").write(s)
print("ok")
