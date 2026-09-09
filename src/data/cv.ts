// TODO: replace every field below with real content. This is scaffolding data
// so the layout can be built and reviewed before the CV content is final.

export const profile = {
  name: "Rafael Sánchez Córdoba",
  headline: "Software engineer", // TODO: final positioning, still under discussion
  location: "Aarhus, Denmark",
  email: "rafasanchezcordoba@gmail.com",
  // Short, informal line shown on the home hero. TODO: write the real one — see the portfolio chat for rejected drafts.
  heroTagline: "TODO — one informal line for the home hero.",
  // Longer professional summary, shown on /resume only.
  summary:
    "Software Engineering graduate completing an MSc in Technology-Based Business Development at Aarhus University, with two years of experience at Siemens Energy in an international engineering environment. Experienced in translating requirements into technical solutions, data and automation, validating outputs, and coordinating across engineering, operations, and project teams. Structured, quality-focused, and proactive in solving problems and managing multiple priorities.",
  cvPdfHref: "/cv.pdf", // TODO: upload the actual PDF to /public/cv.pdf
};

export type ExperienceEntry = {
  years: string;
  role: string;
  org: string;
  description?: string[];
};

export const experience: ExperienceEntry[] = [
  {
    years: "Aug 2024 -- Present",
    role: "Student Assistant | Engineering Data and Technical Support",
    org: "Siemens Energy · Brande, Denmark",
    description: [
      "Supported engineering and project teams across a global wind program, coordinating technical inputs, requirements, open actions, and follow-up across multiple stakeholders.",
      "Translated engineering and operational requirements into structured data models, reporting solutions, and automated workflows using Python, SQL, and Power BI.",
      "Validated data quality, system outputs, and technical reporting, identifying inconsistencies and coordinating corrective actions with relevant engineering stakeholders.",
      "Integrated information from multiple operational systems using REST APIs, supporting reliable data flow and alignment between different technical sources.",
      "Designed, trained, tested, and deployed a machine learning model into production, taking ownership from requirements and development through validation and operational use.",
      "Worked closely with engineering, operations, and management in a structured environment requiring quality, attention to detail, prioritisation, and clear technical communication.",
    ],
  },
  {
    years: "Aug 2023 – Jan 2024",
    role: "Full-stack Developer Intern",
    org: "Magtel · Córdoba, Spain",
    description: [
      "Supported the design and implementation of software solutions during a business-critical systems migration, translating user and system requirements into technical components.",
      "Developed and maintained software using Angular, TypeScript, C#, SQL, and REST APIs, collaborating with developers and stakeholders within an Agile/Scrum team.",
    ],
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
    years: "Exp. Jan 2027",
    program: "MSc in Technology-Based Business Development",
    org: "Aarhus University, Denmark",
  },
  {
    years: "Jan 2025",
    program: "BSc in Software Engineering",
    org: "VIA University College, Denmark",
  },
];
