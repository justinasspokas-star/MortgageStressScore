#!/usr/bin/env python3
"""Static site SEO sanity checks; no Google Search Console access or false indexing claims."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://mortgagestressscore.com"
errors = []

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = []
        self.robots = []
        self.links = []
        self.h1 = 0
        self.description = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "canonical" in (a.get("rel") or "").split():
            self.canonical.append(a.get("href",""))
        if tag == "meta" and a.get("name","").lower() == "robots":
            self.robots.append(a.get("content","").lower())
        if tag == "meta" and a.get("name","").lower() == "description":
            self.description = bool(a.get("content","").strip())
        if tag == "h1": self.h1 += 1
        if tag == "a" and a.get("href"): self.links.append(a["href"])

sitemap = ROOT / "sitemap.xml"
robots = ROOT / "robots.txt"
if not sitemap.exists(): errors.append("Missing sitemap.xml")
if not robots.exists(): errors.append("Missing robots.txt")
else:
    if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots.read_text(encoding="utf-8"):
        errors.append("robots.txt is missing the absolute sitemap declaration")

listed = set()
if sitemap.exists():
    try:
        x = ET.parse(sitemap)
        locs = x.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        for n in locs:
            url = (n.text or "").strip()
            if url in listed: errors.append(f"Duplicate sitemap URL: {url}")
            listed.add(url)
            parsed = urlparse(url)
            if parsed.scheme != "https" or parsed.netloc != "mortgagestressscore.com":
                errors.append(f"Unexpected sitemap host/scheme: {url}")
                continue
            rel = unquote(parsed.path.lstrip("/")) or "index.html"
            if not (ROOT / rel).is_file(): errors.append(f"Sitemap target is missing: {url}")
        for mod in x.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod"):
            if mod.text:
                try: date.fromisoformat(mod.text.strip())
                except ValueError: errors.append(f"Malformed lastmod: {mod.text}")
    except ET.ParseError as exc:
        errors.append(f"Invalid sitemap XML: {exc}")

checked = 0
for file in ROOT.glob("*.html"):
    if file.name in ("fo-verify.html", "google562df6fdb8d9394a.html"):
        continue
    scan = Scan()
    scan.feed(file.read_text(encoding="utf-8"))
    checked += 1
    expected = ORIGIN + ("/" if file.name == "index.html" else "/" + file.name)
    if scan.h1 != 1: errors.append(f"{file.name}: expected 1 H1, got {scan.h1}")
    if not scan.description: errors.append(f"{file.name}: missing description")
    if len(scan.canonical) != 1: errors.append(f"{file.name}: expected one canonical, got {scan.canonical}")
    is_noindex = any("noindex" in s for s in scan.robots)
    if is_noindex and expected in listed:
        errors.append(f"{file.name}: noindex page appears in sitemap")
    if expected in listed and (is_noindex or scan.canonical != [expected]):
        errors.append(f"{file.name}: sitemap canonical/indexing conflict")
    for href in scan.links:
        parsed = urlparse(href)
        if parsed.scheme in ("mailto", "tel") or href.startswith("#"): continue
        if parsed.scheme and parsed.scheme not in ("http","https"): continue
        if parsed.netloc and parsed.netloc != "mortgagestressscore.com": continue
        local = unquote(parsed.path)
        if parsed.netloc:
            local = local.lstrip("/")
        elif local.startswith("/"):
            local = local.lstrip("/")
        if not local: local = "index.html"
        if local.endswith("/"): local += "index.html"
        if not (ROOT / local).is_file():
            errors.append(f"{file.name}: local link missing: {href}")

print(f"SEO audit: {checked} HTML documents, {len(listed)} sitemap URLs, {len(errors)} issues")
for e in errors: print("ERROR:", e)
if errors: sys.exit(1)
print("PASS: HTML structure, local links, noindex, canonical, sitemap and robots consistency.")
