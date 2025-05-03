import requests
from bs4 import BeautifulSoup
import html2text
import os
from urllib.parse import urlparse

# === SETUP OUTPUT DIRECTORY ===
output_dir = "diy_articles"
os.makedirs(output_dir, exist_ok=True)

# === LIST EXISTING FILES ===
print("\U0001F4C1 Existing articles in diy_articles/:")
existing_files = [f for f in os.listdir(output_dir) if f.endswith(".md")]
if existing_files:
    for f in sorted(existing_files):
        print(f"  - {f}")
else:
    print("  (none)")

# === USER INPUT ===
url = input("\n\U0001F517 Enter Home Depot article URL to scrape: ").strip()

# === DERIVE CLEAN FILENAME FROM URL ===
def extract_slug_from_url(url):
    parts = urlparse(url).path.strip("/").split("/")
    for part in reversed(parts):
        if part and not part.isalnum():
            return part
    return "home-depot-article"

output_file = f"{extract_slug_from_url(url)}.md"
output_path = os.path.join(output_dir, output_file)

# === FETCH PAGE ===
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# === CLEAN OUT UNWANTED SECTIONS ===
for tag_id in ["header-static", "footer-static"]:
    tag = soup.find("div", {"id": tag_id})
    if tag:
        tag.decompose()

for tag_class in ["site-map", "breadcrumb", "sf-header", "sf-footer", "sf-mobile-footer"]:
    tags = soup.find_all("div", class_=tag_class)
    for tag in tags:
        tag.decompose()

# === REMOVE NAVIGATION BLOCKS ===
for nav in soup.find_all("nav"):
    nav.decompose()

# === HTML → MARKDOWN CONVERTER ===
markdown_converter = html2text.HTML2Text()
markdown_converter.ignore_links = False
markdown_converter.ignore_images = False
markdown_converter.body_width = 0

# === EXTRACT TITLE ===
title = soup.find("h1")
md_title = f"# {title.get_text(strip=True)}\n\n" if title else ""

# === EXTRACT TOC ===
toc_headings = soup.select(".toc-list-item")
toc_md = "## Table of Contents\n"
for i, li in enumerate(toc_headings, 1):
    link = li.find("a")
    if link:
        toc_md += f"{i}. [{link.text.strip()}](#{link['href'].lstrip('#')})\n"
toc_md += "\n"

# === EXTRACT MAIN CONTENT ===
main_content = soup.find("div", {"id": "main-content"}) or soup.find("article")
body_html = str(main_content) if main_content else ""
md_body = markdown_converter.handle(body_html)

# === FINAL CLEANUP OF MARKDOWN ===
def remove_junk_lines(lines):
    return [line for line in lines if not any(
        junk in line for junk in ["[Cart]", "[Home]", "©", "Shop All", "\u00a9"]
    ) and line.strip()]

lines = md_body.splitlines()
clean_md_body = "\n".join(remove_junk_lines(lines))

# === WRITE CLEAN MARKDOWN TO FILE ===
with open(output_path, "w", encoding="utf-8") as f:
    f.write(md_title + toc_md + clean_md_body)

print(f"\n✅ Saved article to: {output_path}")