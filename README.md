# rafasanchez.dev

Personal portfolio and technical case studies for Rafael Sánchez Córdoba. Built with Astro, deployed on Vercel at [rafasanchez.dev](https://rafasanchez.dev).

The site is content-driven: the CV lives in one TypeScript file, each project is one MDX file, and publishing is a commit. There is no CMS, no database and nothing running at request time — the whole site builds to static files.

## Stack

- **Astro 7** — static output, MDX integration, sitemap
- **Tailwind CSS 4** via the Vite plugin
- **TypeScript** (`npx astro check` for type checking; `@astrojs/check` is installed)
- **Vercel** for hosting and Web Analytics
- Fonts self-hosted through Fontsource (Inter, Manrope)

Node `>=22.12.0` (`.nvmrc` pins 22).

## Commands

```sh
npm install      # install dependencies
npm run dev      # dev server on localhost:4321
npm run build    # static build to ./dist/
npm run preview  # serve the build locally
```

## Structure

```text
src/
├── content.config.ts          Zod schema for the projects collection
├── content/projects/          one folder per case study
│   └── <slug>/
│       ├── index.mdx          the case study
│       ├── assets/            screenshots and rendered diagrams
│       └── diagram-sources/   scripts that generate those diagrams
├── data/cv.ts                 profile, experience, education
├── pages/
│   ├── index.astro            home: intro, CV, featured projects
│   ├── projects/index.astro   project list with type filters
│   ├── projects/[...slug].astro
│   └── 404.astro
├── layouts/BaseLayout.astro
├── components/                Nav, Footer, Row
└── styles/global.css          design tokens and prose styles
public/                        favicon, og image, cv.pdf
```

## Adding a project

Create `src/content/projects/<slug>/index.mdx`. The route follows the folder name, so that slug becomes `/projects/<slug>`. Frontmatter is validated by `src/content.config.ts` at build time — a typo fails the build rather than shipping a broken page.

```mdx
---
title: "Project title"
description: "One or two sentences."
date: 2026-09-24
status: completed        # completed | in-progress | archived
type: cloud              # data | software | cloud | automation | university
featured: false          # true also shows it on the home page
cover: ./assets/cover.png
coverAlt: "Description of the cover image."
tech: ["Astro", "TypeScript"]
github: "https://github.com/..."   # optional
demo: "https://..."                # optional
draft: false             # true hides it from every listing and route
---
```

Two constraints worth knowing before writing:

- `tech` is a **closed enum**. Add new entries to the `TECH` array in `src/content.config.ts` first, or the build fails.
- `cover` must be a **raster** image (PNG/JPG). The project grid resizes it with `widths`, which an SVG cannot satisfy.

Put images in the project's own `assets/` folder and import them — Astro optimises them to WebP and generates responsive sources. For SVG diagrams, import with `?url` and render them as a plain `<img>`:

```mdx
import { Image } from "astro:assets";
import shot from "./assets/screenshot.png";
import diagramUrl from "./assets/diagram.svg?url";
```

MDX does not accept HTML comments. Use `{/* ... */}`, and keep them on **one line** — Prettier mangles multi-line MDX comments into broken markdown emphasis.

## Diagrams

Case studies that include diagrams keep the generator next to them in `diagram-sources/`, as a Python script using only the standard library. Running it rewrites the SVGs in `../assets/`. That keeps diagrams editable and reviewable as text instead of as binary exports from a drawing tool.

## Branches

- `main` — production. Vercel deploys from here.
- `dev` — integration branch; merges into `main`.
- `aws-deployment` — a separate exercise that deploys a copy of this site to S3 + CloudFront with Terraform and GitHub Actions. Its `infrastructure/` and `.github/workflows/` folders exist **only on that branch** and are deliberately not merged. The case study at `/projects/aws-static-deployment` documents it and links to that branch, so it should not be deleted.

## Licence

Source code is available for reference. The written content, CV, images and case studies are not licensed for reuse.
