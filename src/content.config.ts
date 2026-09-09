import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const TECH = [
  'Astro', 'TypeScript', 'JavaScript', 'React', 'Next.js', 'Angular',
  'Node.js', 'Python', 'Java', 'C#', '.NET',
  'PostgreSQL', 'Supabase', 'Prisma', 'SQL',
  'Power BI', 'DAX', 'Microsoft Fabric', 'Power Automate',
  'AWS', 'S3', 'CloudFront', 'Terraform',
  'Tailwind CSS', 'TanStack Query',
] as const;

const projects = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/projects' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    status: z.enum(['completed', 'in-progress', 'archived']),
    type: z.enum(['data', 'software', 'cloud', 'automation', 'university']),
    featured: z.boolean().default(false),
    cover: image(),
    coverAlt: z.string(),
    tech: z.array(z.enum(TECH)),
    github: z.string().url().optional(),
    demo: z.string().url().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { projects };
