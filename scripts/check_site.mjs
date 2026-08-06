#!/usr/bin/env node

import { readFileSync } from 'node:fs';
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
  assert(source.includes('loadCommunityCases();'), `${relativePath} does not load community cases`);
  assert(source.includes('setupCaseModalInteractions();'), `${relativePath} does not initialize case details`);
}

function checkCommunityCases() {
  const payload = JSON.parse(read('data/community-cases.json'));
  assert(Array.isArray(payload.cases), 'community-cases.json must contain a cases array');
  assert(payload.meta?.count === payload.cases.length, 'community case metadata count is stale');
  assert(Array.isArray(payload.meta?.sources), 'community case source metadata is missing');
  assert(payload.meta.sources.length >= 2, 'community case data must include both upstream sources');

  let includedCount = 0;
  for (const source of payload.meta.sources) {
    assert(source.sourceRepository, 'community source repository is missing');
    assert(source.sourceCommit, `community source commit is missing for ${source.sourceRepository}`);
    assert(source.sourceLicense, `community source license is missing for ${source.sourceRepository}`);
    assert(source.availableCount >= source.includedCount, `invalid source counts for ${source.sourceRepository}`);
    includedCount += source.includedCount;
  }
  assert(includedCount === payload.cases.length, 'community source counts do not match case data');

  const ids = new Set();
  for (const item of payload.cases) {
    assert(item.id && !ids.has(item.id), `invalid or duplicate community case id: ${item.id}`);
    assert(item.title && item.prompt && item.image && item.caseUrl, `community case ${item.id} is incomplete`);
    ids.add(item.id);
  }
  return payload.cases.length;
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
const communityCaseCount = checkCommunityCases();
checkLatestXReadme();

console.log(`Site contract OK: 2 pages, ${communityCaseCount} community cases, README data synchronized`);
