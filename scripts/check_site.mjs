#!/usr/bin/env node

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));

function read(relativePath) {
  return readFileSync(join(root, relativePath), 'utf8');
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function checkPage(relativePath) {
  const source = read(relativePath);
  const ids = [...source.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
  const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
  assert(duplicates.length === 0, `${relativePath} has duplicate ids: ${duplicates.join(', ')}`);

  const requiredIds = [
    'prompt-board-grid',
    'prompt-board-search',
    'prompt-board-source',
    'prompt-board-favorites',
    'prompt-board-more',
    'case-modal',
    'case-modal-title',
    'case-modal-prompt',
    'case-modal-favorite',
    'case-modal-share',
  ];
  for (const id of requiredIds) {
    assert(ids.includes(id), `${relativePath} is missing #${id}`);
  }

  const inlineScripts = [...source.matchAll(/<script>\s*([\s\S]*?)<\/script>/g)].map(
    (match) => match[1],
  );
  assert(inlineScripts.length > 0, `${relativePath} has no inline application script`);
  for (const script of inlineScripts) new Function(script);
  assert(source.includes('loadCaseLibrary();'), `${relativePath} does not load the case library`);
  assert(source.includes('case-library.json'), `${relativePath} does not use canonical case data`);
  assert(source.includes('canonicalCaseId'), `${relativePath} does not resolve case aliases`);
  assert(source.includes('setupCaseModalInteractions();'), `${relativePath} does not initialize case details`);
  assert(source.includes('activeSource'), `${relativePath} does not track source filters`);
  assert(source.includes('prompt-board-source'), `${relativePath} does not initialize source filters`);
  assert(source.includes("deferSectionLoad('readme'"), `${relativePath} loads README eagerly`);
  assert(source.includes("cache: 'default'"), `${relativePath} disables browser caching`);
  if (relativePath === 'index.html') {
    assert(source.includes("deferSectionLoad('latest-x-prompts'"), `${relativePath} loads latest X data eagerly`);
  }
}

function promptHash(prompt) {
  const normalized = prompt.toLowerCase().trim().replace(/\s+/g, ' ');
  return createHash('sha256').update(normalized, 'utf8').digest('hex');
}

function checkCaseLibrary() {
  const payload = JSON.parse(read('data/case-library.json'));
  assert(payload.schemaVersion === '1.0.0', 'case library schema version is unsupported');
  assert(Array.isArray(payload.cases), 'case-library.json must contain a cases array');
  assert(payload.meta?.totalRecords === payload.cases.length, 'case library total is stale');

  const ids = new Set();
  const localeCounts = new Map();
  for (const item of payload.cases) {
    assert(item.id && !ids.has(item.id), `invalid or duplicate case id: ${item.id}`);
    assert(item.title && item.prompt && item.category?.key, `case ${item.id} is incomplete`);
    assert(item.promptHash === promptHash(item.prompt), `case ${item.id} has a stale prompt hash`);
    assert(item.source?.key && item.source?.kind, `case ${item.id} has no source`);
    if (item.source.kind === 'community') {
      assert(item.source.repository && item.source.license, `case ${item.id} lacks attribution`);
    }
    ids.add(item.id);
    localeCounts.set(item.locale, (localeCounts.get(item.locale) || 0) + 1);
  }
  const aliases = payload.meta?.aliases || {};
  for (const [alias, canonicalId] of Object.entries(aliases)) {
    assert(!ids.has(alias) && ids.has(canonicalId), `invalid case alias: ${alias}`);
  }
  const shared = localeCounts.get('und') || 0;
  assert(payload.meta.viewCounts['zh-CN'] === shared + (localeCounts.get('zh-CN') || 0), 'Chinese view count is stale');
  assert(payload.meta.viewCounts.en === shared + (localeCounts.get('en') || 0), 'English view count is stale');
  JSON.parse(read('schema/case-library.schema.json'));
  return payload.meta;
}

function checkSkill() {
  const skill = read('skills/manage-gpt-image-cases/SKILL.md');
  const agent = read('skills/manage-gpt-image-cases/agents/openai.yaml');
  assert(skill.startsWith('---\nname: manage-gpt-image-cases\n'), 'skill frontmatter is invalid');
  assert(!skill.includes('TODO'), 'skill still contains TODO placeholders');
  assert(agent.includes('$manage-gpt-image-cases'), 'skill default prompt does not invoke the skill');
  assert(read('skills/manage-gpt-image-cases/references/case-schema.md').includes('Source Adapter Contract'), 'skill schema reference is incomplete');
}

function checkLatestXReadme() {
  const payload = JSON.parse(read('data/latest-prompts.json'));
  const readme = read('README.md');
  const start = readme.indexOf('<!-- latest-x-prompts:start -->');
  const end = readme.indexOf('<!-- latest-x-prompts:end -->');
  assert(start !== -1 && end > start, 'README latest X markers are missing');
  const section = readme.slice(start, end);
  assert(
    section.includes(`更新时间：\`${payload.meta.generated_at_utc}\``),
    'README latest X timestamp is stale',
  );
  assert(section.includes(`条目数：\`${payload.meta.count}\``), 'README latest X count is stale');
}

checkPage('index.html');
checkPage('en/index.html');
const caseMeta = checkCaseLibrary();
checkSkill();
checkLatestXReadme();

console.log(
  `Site contract OK: 2 pages, ${caseMeta.totalRecords} canonical cases, ` +
  `${caseMeta.duplicateRecordsRemoved} duplicates removed, Skill and README synchronized`,
);
