#!/usr/bin/env python3
"""Generate the static homepage. Default: local draft; --publish requires a CV and portrait."""

import argparse
from html import escape
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Prepare launch files; does not upload or deploy")
    args = parser.parse_args()
    data = json.loads((ROOT / "content.json").read_text())
    cv = data.get("cv") or "assets/cv.pdf"
    cv_file = ROOT / cv
    has_cv = cv_file.is_file() and cv_file.read_bytes().startswith(b"%PDF-")
    if args.publish and not has_cv:
        parser.error("Add the revised CV at assets/cv.pdf before preparing the launch version.")

    portrait = data.get("portrait")
    if not portrait:
        portrait = next((f"assets/portrait.{suffix}" for suffix in ("jpg", "jpeg", "png", "webp") if (ROOT / f"assets/portrait.{suffix}").is_file()), None)
    if portrait and not (ROOT / portrait).is_file():
        raise FileNotFoundError(portrait)
    if args.publish and not portrait:
        parser.error("Add the portrait before preparing the launch version.")

    e = escape
    page_url = "https://" + data["domain"] + "/"
    style_version = hashlib.sha256((ROOT / "assets/site.css").read_bytes()).hexdigest()[:10]
    cv_link = f'<a href="{e(cv)}">CV <span class="link-note">(PDF)</span></a>' if has_cv else ""
    portrait_html = (f'<img class="portrait" src="{e(portrait)}" alt="Portrait of {e(data["name"])}" width="320" height="400" decoding="async">' if portrait else '<div class="portrait portrait-placeholder" role="img" aria-label="Portrait to be added"><span>Portrait</span></div>')
    pdf_icon = (ROOT / "assets/pdf-icon.svg").read_text().strip()
    papers = []
    for paper in data["papers"]:
        coauthors = ""
        if paper["coauthors"]:
            names = []
            for name in paper["coauthors"]:
                url = data.get("coauthor_urls", {}).get(name)
                names.append(f'<a href="{e(url)}">{e(name)}</a>' if url else e(name))
            joined = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
            coauthors = f'<p class="coauthors">with {joined}</p>'
        links = []
        if paper.get("pdf"):
            if not (ROOT / paper["pdf"]).is_file():
                raise FileNotFoundError(paper["pdf"])
            links.append(f'<a class="download-link" href="{e(paper["pdf"])}" aria-label="Download {e(paper["title"])} (PDF)">{pdf_icon}<span>Download</span></a>')
        if paper.get("cesifo_url"):
            links.append(f'<a href="{e(paper["cesifo_url"])}">CESifo version <span aria-hidden="true">↗</span></a>')
        resources = '<div class="paper-links">' + "".join(links) + '</div>' if links else ""
        abstract = ""
        if paper.get("abstract"):
            abstract = f'''<details class="abstract">
              <summary>Abstract <span class="expand-icon" aria-hidden="true"></span></summary>
              <p>{e(paper["abstract"])}</p>
            </details>'''
        papers.append(f'''<article class="paper" id="{e(paper['id'])}" aria-labelledby="{e(paper['id'])}-title">
            <h3 id="{e(paper['id'])}-title">{e(paper['title'])}</h3>
            {coauthors}
            <p class="paper-status">{e(paper['status'])}</p>
            {resources}
            {abstract}
          </article>''')

    person = {
        "@context": "https://schema.org", "@type": "Person", "name": data["name"],
        "url": page_url, "jobTitle": data["role"], "email": "mailto:" + data["email"],
        "affiliation": {"@type": "Organization", "name": data["affiliation"]},
        "knowsAbout": ["Macroeconomics", "Labor economics", "Innovation", "Entrepreneurship"],
    }
    if portrait:
        person["image"] = page_url + portrait
    robots = "index, follow" if args.publish else "noindex, nofollow"
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(data['name'])} | Economics | IIES, Stockholm University</title>
  <meta name="description" content="{e(data['description'])}">
  <meta name="author" content="{e(data['name'])}">
  <meta name="robots" content="{robots}">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#fcfcfa">
  <link rel="canonical" href="{page_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(data['name'])} | Economics">
  <meta property="og:description" content="{e(data['description'])}">
  <meta property="og:url" content="{page_url}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/site.css?v={style_version}">
  <script type="application/ld+json">{json.dumps(person, ensure_ascii=False).replace('<', chr(92) + 'u003c')}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <main id="main" class="wrap">
    <section class="intro" aria-labelledby="name">
      <div class="intro-main">
      <p class="eyebrow">Macroeconomics &amp; labor economics</p>
      <h1 id="name">{e(data['name'])}</h1>
      <div class="intro-copy">
        <p class="bio">{e(data['bio'])}</p>
        <div class="contact-links" aria-label="Contact and curriculum vitae">
          {cv_link}
          <a href="mailto:{e(data['email'])}">{e(data['email'])} <span aria-hidden="true">↗</span></a>
        </div>
      </div>
      </div>
      {portrait_html}
    </section>
    <section class="research" id="research" aria-labelledby="research-heading">
      <div class="section-label"><h2 id="research-heading">Research</h2></div>
      <div class="paper-list">
        {''.join(papers)}
      </div>
    </section>
  </main>
</body>
</html>
'''
    (ROOT / "index.html").write_text(html)
    (ROOT / "CNAME").write_text(data["domain"] + "\n")
    (ROOT / ".nojekyll").touch()
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n" + (f"Sitemap: {page_url}sitemap.xml\n" if args.publish else ""))
    sitemap = ROOT / "sitemap.xml"
    if args.publish:
        sitemap.write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{page_url}</loc><lastmod>{e(data["updated"])}</lastmod></url></urlset>\n')
    elif sitemap.exists():
        sitemap.unlink()
    cv_status = "CV linked" if has_cv else "CV omitted until supplied"
    print("Launch files prepared (not deployed)." if args.publish else f"Local draft generated; search indexing disabled; {cv_status}.")


if __name__ == "__main__":
    main()
