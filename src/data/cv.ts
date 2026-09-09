// TODO: replace every field below with real content. This is scaffolding data
// so the layout can be built and reviewed before the CV content is final.

export const profile = {
  name: 'Rafael Sánchez Córdoba',
  headline: 'Software engineer', // TODO: final positioning, still under discussion
  location: 'Aarhus, Denmark',
  email: 'rafasanchezcordoba@gmail.com',
  summary:
    'TODO — one paragraph. What you build, for whom, and the throughline across your work (software, data, automation).',
  cvPdfHref: '/cv.pdf', // TODO: upload the actual PDF to /public/cv.pdf
};

export type ExperienceEntry = {
  years: string;
  role: string;
  org: string;
  description?: string;
};

export const experience: ExperienceEntry[] = [
  {
    years: '2024 —',
    role: 'TODO — current role',
    org: 'TODO — company · location',
    description: 'TODO — scope and one quantified outcome.',
  },
  {
    years: '2023',
    role: 'Full-stack developer intern',
    org: 'Magtel',
    description: 'Migrated an internal management system from Laravel views to Angular.',
  },
];

export type EducationEntry = {
  years: string;
  program: string;
  org: string;
  description?: string;
};

export const education: EducationEntry[] = [
  {
    years: 'TODO —',
    program: 'TODO — MSc programme',
    org: 'TODO — university · location',
  },
  {
    years: '2021 — 2025',
    program: 'BEng in Software Engineering',
    org: 'VIA University College, Denmark',
  },
];
