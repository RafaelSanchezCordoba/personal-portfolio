# Project Context — Personal Developer Portfolio

## 1. Project Overview

Build a modern personal portfolio website for **Rafael Sánchez Córdoba**.

The portfolio should serve as both:

1. A professional personal website containing Rafael's CV, experience, skills and contact information.
2. A technical project portfolio where personal, university and professional projects can be documented in depth as case studies.

The current portfolio is built with Astro but is very simple. The new version should keep Astro unless there is a strong architectural reason to change it.

The main requirement is that new projects and project documentation must be publishable **without editing application code**.

---

## 2. Main Goal

The portfolio should not behave like a simple static CV website.

Each project should be documentable almost like a technical blog post or engineering case study, including:

- Rich text
- Headings
- Images
- Galleries
- Architecture diagrams
- Code snippets
- External links
- GitHub repository links
- Live demo links
- Technology stack
- Technical decisions
- Problems/challenges
- Results and lessons learned

**REVISED after a grilling session (see section 22).** "Without editing application code" does not require a headless CMS. Publishing a project is writing one MDX file in the repo and pushing — Astro Content Collections plus Zod validation gives type safety and the same "add a file, get a page" workflow that a CMS would, without a SaaS dependency, a schema layer, or a webhook to maintain. A CMS (Keystatic, git-based) stays an option for later if hand-writing MDX becomes a chore — see section 22.

---

## 3. Current Architectural Direction

### Frontend

Use:

- **Astro**
- **TypeScript**
- Prefer Astro-native components
- React only when real interactivity requires it

Astro is preferred because the portfolio is mainly content-driven and does not require a heavy client-side application.

---

### CMS

**REVISED — no CMS.** See section 22. Projects are Astro Content Collections: one MDX file per project under `src/content/projects/`, frontmatter validated with Zod (`src/content.config.ts`). The CV (experience, education, summary) is a local TypeScript file, `src/data/cv.ts`.

Reasoning: publishing happens a handful of times a year, and Rafael prioritised shipping fast over "no code at all." Sanity would have meant a SaaS account, a schema layer, GROQ queries, an API token, and a webhook — for a benefit (editing from a phone) that doesn't matter at this frequency. The property that does matter long-term — content lives as files in the repo, not trapped in someone else's database — is true from day one this way.

Keystatic (a git-based CMS that commits MDX to the repo through a visual editor) remains a good later upgrade if hand-writing MDX gets old — it can be installed on top of the existing content with no migration, because it expects exactly the file layout already in use.

---

### Production Hosting

The permanent production portfolio should be hosted on:

- **Vercel**

The intended custom domain is:

- **rafasanchez.dev**

The domain should ideally be purchased from an independent registrar rather than being tied to the hosting provider.

Preferred registrar:

- **Cloudflare Registrar**

Conceptually:

```text
Cloudflare Registrar / DNS
          ↓
   rafasanchez.dev
          ↓
        Vercel
          ↓
        Astro (Content Collections, no external CMS)
```

**Domain already purchased** at Cloudflare Registrar (as of the grilling session, section 22).

---

## 4. AWS Learning Project

Rafael is currently learning AWS and preparing for AWS certifications, starting with **AWS Certified AI Practitioner**.

The portfolio should also be used as the basis for a separate AWS learning project.

Important:

- AWS is **not intended to be the permanent production hosting platform**.
- The AWS deployment is a learning/demo environment.
- The AWS infrastructure may later be paused or destroyed to avoid ongoing costs.
- The permanent portfolio remains on Vercel.

**DECIDED (section 22): build → document → destroy, and it does not run alongside Vercel.** A static copy of the site is deployed to S3 + CloudFront once the Vercel site exists, fully documented (architecture diagram, screenshots, cost notes), then torn down — including the Route 53 hosted zone, which otherwise bills forever at a small but nonzero monthly cost. There is deliberately no live demo link for this case study: the screenshots and the architecture diagram *are* the deliverable, not a running service.

The AWS deployment itself should become one of the documented projects in the portfolio.

Possible project title:

> AWS Cloud Portfolio Deployment

Initial AWS architecture:

```text
GitHub
   ↓
GitHub Actions
   ↓
Astro Build
   ↓
Amazon S3
   ↓
Amazon CloudFront
   ↓
HTTPS / DNS
```

Likely AWS services:

- Amazon S3
- Amazon CloudFront
- AWS Certificate Manager
- Route 53 or DNS integration using a subdomain
- IAM
- CloudWatch
- AWS Budgets / billing alerts

Potential temporary domain:

```text
aws.rafasanchez.dev
```

The AWS S3 bucket should preferably remain private and be served through CloudFront using Origin Access Control.

Infrastructure as Code may be added later, probably using:

- Terraform

But the first deployment may intentionally be configured manually through the AWS Console so Rafael learns the purpose of each AWS service before automating it.

---

## 5. Content Publishing Workflow

One of the central requirements is:

> Rafael must be able to add a new project without touching source code.

**REVISED (section 22).** No CMS, no webhook. The workflow is:

```text
Write src/content/projects/<slug>/index.mdx
     ↓
git push
     ↓
Vercel detects the push and rebuilds
     ↓
getStaticPaths reads the Content Collection
     ↓
One static page per project, deployed
```

Example:

```text
/projects/ml-blade-defect-detection
/projects/portfolio-tracker
/projects/aws-cloud-portfolio
```

Adding a project is adding a file. No servers, no external services, no token to rotate. The tradeoff accepted deliberately: editing requires an editor and a git client, not a phone browser. That is fine at a publishing cadence of a handful of projects per year.

---

## 6. Portfolio Information Architecture

**DECIDED.** The MVP is deliberately smaller than the structure originally sketched here. Recruiters scan, they do not navigate — a dense single-scroll home beats eight thin pages.

MVP routes, and nothing else:

```text
/                     Home — CV as a web page
                      (hero, experience, education, featured projects)
/projects             Project index, cover-image grid
/projects/[slug]      Case study, generated from Sanity
```

Contact is an obfuscated `mailto:` link in the footer — no form, no backend.

Out of the MVP: Blog / Notes, `/now`, contact form, analytics. A separate `/about` page is not needed because the home *is* the about page. A separate `/cv` page is not needed for the same reason; the downloadable PDF covers the "give me the file" case.

---

## 7. Project Content Model

**IMPLEMENTED** as an Astro Content Collection, `src/content.config.ts`. Frontmatter fields, validated with Zod:

```text
title            string
description      string   — one line, used in the grid and featured list
date             date     — shown on the site on purpose, see section 12b
status           enum:  completed | in-progress | archived
type             enum:  data | software | cloud | automation | university
featured         boolean
cover            image() — required; the grid is built around cover images
coverAlt         string
tech             enum[]  — closed list, prevents "Next.js" vs "Nextjs" drift
github           url, optional
demo             url, optional
draft            boolean — excluded from the production build
```

No `slug` field — the file's location under `src/content/projects/` (e.g. `example-one/index.mdx`) is the id and the route.

No `externalLinks[]` — unused in practice; add back if a real project needs it. `github` and `demo` stay as plain fields rather than inline body links, so the same URL is never duplicated in two places.

---

## 8. Rich Project Content

**IMPLEMENTED — MDX, not structured blocks.** The body of each project is free-form MDX: paragraphs, headings, lists, links, and images are native Markdown; fenced code blocks render with Astro's built-in Shiki syntax highlighting; images are inline `![]()` referencing files colocated with the MDX. No custom block schema, no gallery/callout/timeline components in the MVP — add one only when a real project needs it and hand-writing the equivalent in Markdown is genuinely worse.

This replaces the Sanity Portable Text plan (see section 22): a single MDX file that Rafael writes with whatever headings a given project needs, plus the fixed frontmatter panel from section 7 for the hard data. A big project gets ten sections because they come naturally; a small one gets three paragraphs without looking unfinished.

---

## 9. Case Study Philosophy

Important projects should be presented as technical case studies rather than simple cards.

Possible structure:

```text
01 — Overview
02 — Problem
03 — My Role
04 — Solution
05 — Architecture
06 — Technology Choices
07 — Implementation
08 — Challenges
09 — Results / Impact
10 — Lessons Learned
```

This numbered structure is **not a schema** — it is a writing prompt. See section 8: content is free-form MDX, and this list is a checklist to consult while writing, not fixed fields to fill in.

Two levels of projects may be useful:

### Featured Case Studies

A small number of important, detailed projects. `featured: true` in the frontmatter (section 7).

Real candidates as of the grilling session (section 22) — see that section for the reasoning:

- The Siemens Energy ML model (blade defect detection, anonymised) — likely the strongest single project, currently undocumented anywhere
- `portfolio-tracker` — Trading 212 portfolio tracker with XIRR/P&L calculations, tests, and a daily Vercel cron
- `maitecrafs-production` — production kanban system for a real small business, with real (non-Rafael) users
- AWS Cloud Portfolio Deployment (section 4)

### Other Projects

Smaller projects with lighter documentation.

---

## 10. CV

The CV should not exist only as a PDF.

**DECIDED.** There is no separate `/cv` route — the home page *is* the CV. A downloadable PDF sits in `public/cv.pdf` behind a "Download CV" button (currently a placeholder file — see section 22).

**Source of truth: a local file in the repo**, `src/data/cv.ts` (plain TypeScript, no CMS — see section 22). The CV changes once or twice a year, and it gets edited while the site is being worked on anyway.

Projects live as MDX Content Collections (section 7) — that is where the no-code, add-a-file-and-publish workflow actually applies.

### CV content — deliberately out of scope here

An early student-era PDF CV was reviewed earlier in this project's history (skill-level bars, part-time jobs, an outdated "student" label — none of that survived). A current LaTeX CV exists with real content (Siemens Energy role, MSc in progress, etc.) but **Rafael has explicitly asked not to have the CV content analysed or decided in this document** — he will supply and edit `src/data/cv.ts` himself.

Until then, `cv.ts` ships with clearly marked `TODO` placeholders so the layout can be built, reviewed, and tested independently of the real content (section 22).

The HTML home originally proposed as `/cv` contains:

- Experience
- Education
- Skills
- Technologies
- Projects
- Contact

A downloadable PDF CV can also be provided.

The HTML version is preferred for SEO, accessibility and machine readability.

---

## 11. Technologies as Structured Content

**REVISED — a closed enum, not an entity (section 22).** A separate `technology` document type (with its own icon, category, URL) made sense as a referenceable CMS entity; it is unnecessary complexity for a handful of MDX files. Instead, `tech` in the project frontmatter (section 7) is a `z.enum([...])` of allowed technology names, maintained in `src/content.config.ts`. This gets almost the same benefit — the build fails if a project writes `"Nextjs"` while another writes `"Next.js"` — without a second collection.

Per-technology icons or pages, if ever wanted, are a ~20-line lookup map, added when there is an actual reason to render one.

---

## 12. Design Direction

**DECIDED.** See section 12b for the approved specification.

The site should feel:

- Modern
- Technical
- Professional
- Minimal but not generic
- Fast
- Content-first
- Suitable for recruiters and technical hiring managers

Avoid the stereotypical developer portfolio that is only:

```text
About
Projects
Contact
```

with generic project cards.

The goal is to communicate engineering thinking, architecture, decisions and measurable impact.

---

## 12b. Approved Visual Specification

Reference the direction borrows from: `braydoncoyer.dev` — but only its **lightness and typographic scale**, never its bento grid of rounded cards. Rounded card grids are explicitly rejected: they read as generic AI-generated layout.

### Layout — home

```text
minimal nav ("rs" left, links right)
─────────────────────────────────────────────
centred hero   round photo with a ring of air
               huge two-line headline
               (second line in the accent colour)
               summary paragraph
               "Ver proyectos" / "Descargar CV" buttons
─────────────────────────────────────────────
Experience     rows: year | role / company / description
─────────────────────────────────────────────
Education      same rows
─────────────────────────────────────────────
Projects       large-title rows with an arrow (from Sanity)
─────────────────────────────────────────────
footer         location | email
```

Section separators are hairlines that span the **full page width**, edge to edge.

### Tokens

| Role | Value |
|---|---|
| Page background | `#F7F6F3` — warm light, never pure white |
| Ink | `#17181A` — never pure black |
| Body secondary | `#514E49` |
| Muted | `#6F6C66` |
| Metadata | `#93908A` |
| Section rules | `#E6E4DE` |
| Row rules | `#EDEBE5` |
| Accent | `#B0552F` terracotta |

The accent appears rarely and only where it means something: the second headline line, links, and arrows. No coloured badges.

### Typography

- Display: **Manrope** 800, `letter-spacing: -0.03em`, `line-height: 1.05`
- Body: **Inter** 400/500
- Section labels: 11px, uppercase, `letter-spacing: 0.13em`, muted
- Row grid: 96px year column + content, 24px gap

### Hard rules

- **No `border-radius`** on buttons, rows or containers. The only round shape on the site is the portrait.
- No shadows, no gradients, no coloured badges, no card containers.
- Project index uses full-bleed cover images (`aspect-ratio: 4/3`) with the title *below* the image — not inside a card.

Dark mode uses the same design with ink and paper inverted, via Tailwind `dark:`. Post-MVP, once the light version is finished.

---

## 13. Rafael's Professional Profile

**NARROWED after a grilling session (section 22).** The original seven-area profile (software engineering, data/analytics, AI/ML, automation, cloud, digital transformation, business development) is broader than the evidence on disk supports today, and claiming all seven undermines credibility on the ones that are real.

**Working positioning: a data engineer who also ships the product around the data** — a BSc in Software Engineering specialised in data engineering, two years at Siemens Energy doing data engineering/analytics (Microsoft Fabric, Power BI, DAX) plus a production ML model, and two full-stack Next.js applications that turn that data work into something people actually use. This combination is what the evidence supports; project management interest is real but not senior enough yet to lead with — it belongs in the experience narrative, not the headline.

The profile widens honestly as evidence accumulates, not by writing more nouns in a list.

---

## 14. Existing / Potential Projects

**REVISED after inventorying the actual sibling project folders (section 22).** The Social Prediction Platform below was the original headline example; in reality it is a frontend-only baseline with no backend, stalled since May 2026 — not a case study yet. Two other, more mature projects were found and are stronger MVP candidates: `portfolio-tracker` (Trading 212 investment tracker: XIRR/P&L calculation, 27 unit tests, Vercel cron) and `maitecrafs-production` (production kanban system for a real small business, with real users who are not Rafael). Neither had a screenshot on disk as of the grilling session — cover images are a prerequisite, not an afterthought, given the cover-image grid in section 12b.

### Social Prediction Platform (not yet a real case study)

Web application for private groups to create social prediction bets using fictional points.

Existing/current stack includes:

- Next.js
- TypeScript
- Supabase
- PostgreSQL
- Supabase Realtime
- Vercel

---

### AWS Cloud Portfolio Deployment

The portfolio deployed as an AWS architecture learning exercise.

Likely topics to document:

- S3
- CloudFront
- IAM
- HTTPS
- DNS
- CI/CD
- Security
- Cost awareness
- Infrastructure lifecycle
- Potential Terraform implementation

---

### Machine Learning Projects

**Concrete candidate identified (section 22):** a machine learning model Rafael designed, trained, and deployed to production at Siemens Energy for blade-related analysis on the SG5X platform — ownership from data preparation through deployment and operational use. This is likely the strongest single project available and does not appear anywhere in the portfolio content yet. The underlying data is almost certainly confidential; the problem framing, modelling approach, validation, and deployment story are the anonymisable, publishable part. Requires a manager check before publishing.

Separately, `Data Engineering` (a Chicago bike-share ETL pipeline with dbt on Postgres) exists on disk but is a single ingestion script, stalled since February 2026 — not yet a case study. If the portfolio leans on the data-engineering side of the positioning in section 13, finishing this project is high-leverage: it is the closest thing to a publishable substitute for the Siemens Energy data work, which cannot be shown directly (real company data).

---

### Data / Analytics Projects

The portfolio should also support Power BI, Python and analytics projects where screenshots, charts, methodology and results are important.

---

### Automation / Digitalization Projects

Projects involving process automation, Power Automate, PowerApps, SharePoint or similar systems may also be included.

---

## 15. Future Idea — NOT MVP

A future feature has been discussed:

> AI Portfolio Assistant

Potentially using AWS / Amazon Bedrock and RAG so visitors could ask questions about Rafael's CV and projects.

Example:

> "What experience does Rafael have with machine learning?"

This feature is explicitly **out of scope for the current MVP**.

Do not design the initial architecture around this unless doing so requires almost no additional complexity.

---

## 16. Engineering Principles

When making architecture decisions, prioritize:

1. Simplicity
2. Maintainability
3. Fast page load
4. Good SEO
5. Accessibility
6. Low operational cost
7. Easy content publishing
8. Good developer experience
9. Strong technical portfolio value

Avoid unnecessary backend infrastructure.

Do not build a custom CMS unless there is a very strong reason.

Avoid adding services purely to make the architecture look more complex.

---

## 17. Current Technology Preference

Current preferred stack:

```text
Frontend:
Astro
TypeScript
Tailwind CSS v4

Content:
Astro Content Collections + MDX
No external CMS (Keystatic possible later — section 22)

Analytics:
Vercel Web Analytics (free tier, cookieless)

Permanent hosting:
Vercel

Domain:
rafasanchez.dev  (already purchased)

Registrar / DNS:
Cloudflare Registrar / Cloudflare DNS

Source control:
GitHub (public repo)
Working copy at ~/Developer, not inside iCloud Drive

CI/CD:
Vercel's own git integration — no separate GitHub Actions workflow needed for deployment

AWS learning environment (build, document, destroy — section 4):
S3
CloudFront
ACM
IAM
CloudWatch
Route 53 (temporary — destroyed with everything else)
Potential Terraform later
```

Language: **English only.** Rafael works and job-hunts in Denmark, where the tech working language is English; a bilingual site would double the maintenance burden of every case study for no real audience gain (section 22).

---

## 18. Open Decisions

### Resolved

| Topic | Decision |
|---|---|
| Visual design system | Approved — see section 12b |
| Styling approach | Tailwind CSS v4 |
| Navigation | Minimal: Home, Projects, CV, Contact |
| Home page structure | CV-as-web-page, single vertical scroll (section 12b) |
| Content model | Astro Content Collections + MDX, Zod-validated (section 7) — no CMS |
| Repository structure | Single Astro project at the repo root. No monorepo, no workspaces |
| Project filtering | Project-type filter row on `/projects`. Technology filtering deferred |
| Blog in MVP | No |
| `/now` page | No |
| Contact form | No — obfuscated `mailto:` link |
| CV source of truth | Local file `src/data/cv.ts` (section 10), content deferred to Rafael |
| Language | English only (section 17) |
| Analytics | Vercel Web Analytics, free tier only |
| Positioning | Data engineer who ships product — narrowed from a 7-area profile (section 13) |
| Project page structure | Free-form MDX body + fixed frontmatter panel (section 8) |
| Working directory | `~/Developer/personal-portfolio`, not iCloud Drive; GitHub is the backup |

### Still open (post-MVP)

- Dark mode
- Animation strategy
- Testing strategy (beyond the Zod schema failing the build on bad frontmatter)
- Whether a certifications section ships now or waits for the AWS AI Practitioner
- AWS lab implementation details
- Terraform vs AWS CDK vs manual-only infrastructure for the AWS lab
- Which projects make the v1 launch, and their cover images (section 22 — pending Rafael)
- Whether/when to add Keystatic on top of the MDX content

The coding assistant should challenge assumptions when there is a meaningful technical reason to do so.

---

## 18b. Implementation Milestones

1. ~~Record decisions in `context.md`~~ — done
2. ~~Repo — `git init`, GitHub repo, working copy moved to `~/Developer`~~ — done
3. ~~Scaffolding — Astro + TypeScript + Tailwind v4 + MDX, colour tokens, Manrope/Inter self-hosted~~ — done
4. ~~Home, `/projects`, `/projects/[slug]` built against placeholder `cv.ts` and two example MDX projects~~ — done
5. **Real content** — replace placeholder `cv.ts`, pick and write up the v1 projects (section 22), real cover images
6. **Pulish and deploy** — sitemap already wired via `@astrojs/sitemap`; still need a real `og.png`, Vercel deploy, domain, Vercel Web Analytics confirmed live
7. **Post-MVP** — dark mode, AWS lab (build → document → destroy, section 4), Keystatic if hand-writing MDX gets old

---

## 19. Expected Collaboration Style

Do not immediately generate the full application.

First:

1. Read and understand this context.
2. Discuss architecture and key decisions.
3. Identify important unknowns.
4. Propose a sensible MVP.
5. Break implementation into small milestones.
6. Only then begin coding.

Rafael is using the project partly to learn.

Therefore:

- Explain important architectural decisions.
- Avoid hiding complexity behind unexplained abstractions.
- Prefer incremental implementation.
- Do not introduce unnecessary services or frameworks.
- When several options are reasonable, explain the trade-offs.
- Keep the project production-quality but understandable.

---

## 20. Initial Definition of Success

The first meaningful release should allow Rafael to:

1. Visit `rafasanchez.dev`.
2. See a polished professional homepage.
3. View his profile / experience / CV.
4. Browse a projects page.
5. Open detailed project case studies.
6. Add a new project by writing an MDX file (section 5, revised).
7. Publish it without touching Astro page/component code.
8. Have Vercel automatically rebuild and deploy on `git push`.
9. Maintain the source code in GitHub.
10. Use the same portfolio codebase later for an AWS deployment case study, then tear that copy down (section 4).

---

## 21. Suggested First Discussion

**Done — see sections 12b, 18, and 22.** MVP pages, content model, project page structure, visual direction, repository structure, and the deployment workflow were all discussed and decided before implementation began.

Do not implement the future GenAI Portfolio Assistant yet.

---

## 22. Grilling Session — Decisions That Overrode the Original Plan

A structured grilling session challenged the plan above before scaffolding began. Kept here as the record of *why* things changed, since several sections above now read differently from how this document started.

**Sanity dropped.** The original "publish without code" requirement did not require a headless CMS, a schema layer, GROQ, an API token, and a webhook — for publishing a handful of projects a year. Content moved to Astro Content Collections (MDX + Zod). Keystatic (git-based CMS, commits MDX to the repo via a visual editor) is a documented later option, installable on the existing file layout with no migration, if hand-writing Markdown becomes tedious.

**Monorepo dropped.** With no Sanity Studio to host, there is nothing to put in a second workspace. Single Astro project at the repo root.

**English only, no bilingual toggle.** Rafael works and job-hunts in Denmark; the tech working language there is English. A second language multiplies the writing cost of every case study forever, for a market he isn't targeting.

**Positioning narrowed.** The original profile claimed seven areas (software engineering, data, AI/ML, automation, cloud, digital transformation, business development). An inventory of Rafael's actual projects and CV showed two years of real data-engineering/analytics work at Siemens Energy (Microsoft Fabric, Power BI, DAX) plus two solid full-stack Next.js apps — and effectively nothing published yet in the other areas. Working positioning: **data engineer who also ships the product around the data.** Widen the claim later, when evidence backs it, not before.

**The Siemens Energy ML model is the missing headline project.** Buried as one bullet in the CV: Rafael designed, trained, and deployed a production ML model for blade-related analysis (SG5X platform), end to end. Currently absent from the portfolio entirely. Likely the single strongest project available; needs a manager check on what can be shown before writing it up.

**Real project inventory replaced fictional placeholders.** The "Social Prediction Platform" case study named throughout this document earlier is a frontend-only baseline with no backend, stalled since May 2026 — not yet a real case study. Two stronger, more mature candidates exist and weren't in the original plan at all: `portfolio-tracker` (tested, deployed, financially real) and `maitecrafs-production` (production system with real external users). `Data Engineering` (Chicago bike-share pipeline, dbt + Postgres) is stalled but worth finishing if the data-engineering positioning needs a publishable substitute for the Siemens Energy work, which can't be shown directly.

**No project has a cover image yet**, and the approved visual direction (section 12b) is a cover-image grid. Producing real screenshots is now a tracked prerequisite for launch, not an afterthought.

**AWS lab: build, document, destroy — not a parallel deployment.** Running a second live copy of the site on AWS alongside Vercel would mean either maintaining two deployments of the same site or letting one go stale. Instead: deploy once, document thoroughly (architecture diagram, screenshots, cost notes), then tear everything down, including the Route 53 hosted zone. No live demo link on this case study — the writeup is the deliverable.

**Analytics: free tier only.** Vercel Web Analytics, cookieless, no cost. No paid analytics tool for a portfolio at this stage.

**CV content is explicitly out of scope for this document.** Rafael will write and maintain `src/data/cv.ts` himself; this file records structural and architectural decisions, not his career narrative.

**Practical fixes made during the same session:** the system clock was found ~3 weeks behind (broke npm's TLS certificate validation — fixed via `sntp` sync); the working copy was moved from iCloud Drive to `~/Developer` (iCloud syncing `node_modules`' tens of thousands of small files causes slow builds and occasional partial-sync corruption); the domain was already purchased at Cloudflare Registrar; the GitHub repo is public.
