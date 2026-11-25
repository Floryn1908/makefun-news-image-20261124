// Entry for news-image-20261124 (Node 22, standard library only).
// The entry is one image summing up the world's news of Tuesday 24 November 2026:
// this program copies the front page in entry.png beside it to /output/entry.png,
// where the gate reads it. The judge compares images pairwise and picks the one
// that best sums up the day's world news, reading only what the image shows.
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
