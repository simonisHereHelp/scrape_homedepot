# Home Depot DIY Web Content Scraper

**Keywords:** web scrape, Home Depot, DIYer, Markdown, LLM, Llama3, content extraction, Docusaurus

## 🧰 Purpose

This project scrapes and processes DIY article content from [HomeDepot.com](https://www.homedepot.com/c/diy_projects_and_ideas) to support **local LLM (Large Language Model) fine-tuning and retrieval augmentation**.

The goal is to enable a lightweight, locally run model (e.g., **LLaMa3-8B**) to understand and respond to natural language DIY queries by referencing grounded, image-supported guides and real product context.

## 🎯 Use Case: LLM Customization for DIY Assistants

The curated content is intended for:
- **RAG pipelines** (retrieval-augmented generation),
- **semantic search over home repair topics**, or
- **training/fine-tuning of LLaMa-based local models** on instructional data with product grounding.

## 📦 Extracted Article Elements

Each scrape captures the following:

### a) Visual and Title
- Primary banner image, contributor photo
- Article title and author attribution

### b) "How-To" Instructions (with Images)
- Step-by-step DIY process
- Each step includes relevant progress photos and links to required tools/materials

### c) Related Products and Guides
- Official product references from HomeDepot.com
- Additional internal links to related DIY tutorials

### d) Table of Contents and Metadata
- Extracts in-page TOC for structured navigation
- Metadata such as last updated date, source URL, and tags

---

## 📂 Output

- All files are written as `.md` Markdown format
- Output is saved to the `/diy_articles/` directory
- Filenames are derived from the article slug:
  
Example: diy_articles/how-to-measure-a-room-for-furniture.md


### ⚠️ Manual Cleanup Still Recommended

Although the output is structured and relatively clean, you may still need to:
- Remove unrelated site-wide nav/footer remnants
- Relabel or group product blocks for better RAG context
- Normalize image URLs or download images for local Docusaurus rendering

---

## 🔁 LLM Integration Plan

- Base Model: **Meta LLaMa3-8B**
- Input corpus: DIY articles with visual, procedural, and product context
- Intended tasks:
  - In-context routing for Docusaurus-based help docs
  - Finetuning for localized task resolution
  - Semantic similarity response to "how do I..." DIY queries

---

## 🚀 How to Use

1. Run `scrape.py`
2. When prompted, **paste a Home Depot article URL**
3. Output will appear under `/diy_articles/`

> This tool is CLI-based, but GUI and batch modes are possible for expansion.

---

Let me know if you want this in a downloadable PDF or included in the Docusaurus landing page as a contributor guide.
