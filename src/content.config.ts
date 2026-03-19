import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // Yeni loader sistemi: src/content/blog içindeki markdown dosyalarını tara
  loader: glob({ pattern: '**/[^_]*.{md,mdx}', base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(), // Tarih formatını otomatik dönüştür
    author: z.string(),
    tags: z.array(z.string()),
  }),
});

export const collections = { blog };