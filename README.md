# Isabella Maassen — research website

A single-page academic website at **https://isabellamaassen.com/**, using the GitHub account **imaassen**.

The approved website was published with GitHub Pages on November 9, 2026. The custom domain is verified and HTTPS is enforced. The CV and portrait are linked from the homepage at `assets/cv.pdf` and `assets/portrait.jpg`. The launch build enables search indexing and generates a sitemap.

## Preview

Open `index.html` in a browser, or run this from this folder:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8000`.

## Content and design

- `content.json`: introduction, email, paper titles, coauthors, coauthor profile URLs, statuses, and abstracts.
- `assets/site.css`: typography, spacing, and responsive layout.
- `papers/`: the three supplied PDFs, copied without modifying their contents.
- `tools/build.py`: generates `index.html`, the domain file, and search metadata using Python's standard library. No packages or installation are needed.

The homepage and abstracts are ordinary HTML, and expandable abstracts work without JavaScript. The fonts use the visitor's system sans-serif fonts; no third-party font service, tracking, or cookie banner is required by this implementation.

The PDF download symbol is the Font Awesome 4.7 `file-pdf-o` glyph, embedded locally from `assets/pdf-icon.svg`. Its copyright and SIL Open Font License notice are retained in `assets/FONT-AWESOME-LICENSE.txt`; no external icon font is loaded.

The paper order follows the supplied list. No paper is designated as a job market paper. The mobility paper is listed as a working paper, matching the revised CV, without a download or abstract until those are supplied.

The main monopsony download is the supplied January 2026 PDF. A separate link leads to the 2025 CESifo working-paper page (No. 11820), which has a longer title and a different abstract. The website abstract comes from the attached January 2026 draft. The other two abstracts come from their supplied PDFs. Line wrapping and line-break hyphenation have been normalized; wording has not been rewritten.

## Make an update

Edit `content.json`, then regenerate the version intended for the live website:

```sh
python3 tools/build.py --publish
```

Use JSON syntax: double-quoted keys and strings, and commas between entries. Keep PDF filenames and links consistent. Update the `updated` date when making substantive changes. Preview the result, then commit and push to `main` to deploy it. To make a private local draft with indexing disabled, run the build without `--publish` and do not push that draft.

## Update the CV

The revised `IsabellaMaassen_CV.pdf` supplied on November 9, 2026 has been moved to `assets/cv.pdf` without changing its contents and is linked beside the email address. For future updates, replace `assets/cv.pdf` and regenerate the draft. The homepage now includes expected PhD completion in June 2027 and lists the mobility paper as a working paper. Detailed education, teaching, grants, presentations, service, and references remain in the linked CV to keep the homepage compact.

## Update the portrait

The website uses `assets/portrait.jpg`, a 584 × 876 web copy of the supplied `DSC01839.jpg` (solid dark top). Embedded EXIF, XMP, camera, editing, Photoshop, ICC, and comment metadata have been removed. The original has a standard sRGB profile, so the web copy uses normal browser sRGB interpretation. The selected photo is downsampled and stored as a progressive JPEG for a smaller download; it is not retouched.

Both original photos are preserved unchanged in `.private/portraits/`, excluded by `.gitignore`. Keep these local originals out of public uploads and deployment packages; only `assets/portrait.jpg` belongs in the published website.

For future updates, create a metadata-free copy at `assets/portrait.jpg` and regenerate the draft. The image is shown beside the introduction on desktop and smaller beside the name on phones. Its frame uses a 4:5 crop controlled by `object-position` in `assets/site.css`.

## Publication build

Follow `LAUNCH-CHECKLIST.md`. Preparing launch files requires the revised CV and portrait:

```sh
python3 tools/build.py --publish
```

This command only writes local files. It does not create a repository, upload files, change DNS, or deploy the site.

For future updates after launch, use `--publish` so the live version remains indexable. Running the default command deliberately produces a draft with indexing disabled.

## GitHub Pages

The working repository is `imaassen/isabellamaassen.github.io`, cloned locally. Make website changes in this repository going forward. The generated site can be served directly from its main branch and root folder, with no framework, build service, or paid hosting. GitHub's free Pages plan uses a public repository, so upload only when the site and paper versions are ready to be public.

Custom domain: `isabellamaassen.com` (already recorded in the local `CNAME` file). Porkbun routes the root domain using an `ALIAS` to `imaassen.github.io` and `www` using a `CNAME` to the same target. Keep the GitHub and Google verification TXT records in place.

Source for domain configuration: [GitHub custom-domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

Google Search Console ownership is verified, and `https://isabellamaassen.com/sitemap.xml` was successfully submitted and read on November 9, 2026. See `LAUNCH-CHECKLIST.md` for remaining profile links and indexing follow-up.

## Website icon

The favicon is a pale blue circle (`#dfeaf1`) with navy uppercase IM (`#254d67`). Matching versions are provided as SVG, a 96px PNG for Google and other consumers, a root `favicon.ico` with 16/32/48px sizes, and a 180px Apple touch icon. The generated homepage declares each version. Keep these URLs stable; Google refreshes its cached search icon after recrawling and processing the homepage and icon.
