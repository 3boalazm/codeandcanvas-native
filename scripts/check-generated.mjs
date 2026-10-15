#!/usr/bin/env node
// Regenerate in isolation; check committed output without rewriting the workspace.
import { cpSync, mkdtempSync, readdirSync, readFileSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const root = fileURLToPath(new URL('../',import.meta.url));
const temp = mkdtempSync(join(tmpdir(),'cc-generated-'));
try {
  for (const file of ['scripts','partials','index.html','erp/index.html','assets/js/erp-data.js']) cpSync(join(root,file),join(temp,file),{recursive:true});
  execFileSync('python3',['scripts/gen-pages.py'],{cwd:temp,stdio:'pipe'});
  execFileSync(process.execPath,['scripts/sync-chrome.mjs'],{cwd:temp,stdio:'pipe'});
  execFileSync(process.execPath,['scripts/gen-ar.mjs'],{cwd:temp,stdio:'pipe'});
  const files=[];
  function walk(dir){for(const e of readdirSync(dir,{withFileTypes:true})){if(['scripts','partials'].includes(e.name))continue;const p=join(dir,e.name);if(e.isDirectory())walk(p);else files.push(relative(temp,p));}}
  walk(temp);
  const stale=files.filter(f=>!existsSync(join(root,f))||!readFileSync(join(root,f)).equals(readFileSync(join(temp,f))));
  if(stale.length){console.error('Generated output is stale. Run npm run generate:\n'+stale.join('\n'));process.exitCode=1;}
  else console.log(`Generator parity: ${files.length} outputs match isolated regeneration.`);
} finally {rmSync(temp,{recursive:true,force:true});}
