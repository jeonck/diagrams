#!/usr/bin/env node
// projects/<project>/diagrams/<slug>/meta.json 들을 훑어 diagrams.json 과
// README 의 다이어그램 표를 만든다.
//   node tools/build-index.mjs          쓰기
//   node tools/build-index.mjs --check  커밋본이 최신인지만 확인 (CI 용)

import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const PROJECTS = join(ROOT, 'projects');
const OUT = join(ROOT, 'diagrams.json');
const DOC = join(ROOT, 'README.md');
const SITE = 'https://jeonck.github.io/diagrams/';
const START = '<!-- diagrams:start -->';
const END = '<!-- diagrams:end -->';

const FORMATS = { html: 'diagram.html', excalidraw: 'diagram.excalidraw' };
const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const fail = (msg) => {
  console.error('build-index: ' + msg);
  process.exit(1);
};

function readJson(path, what) {
  if (!existsSync(path)) fail(`${what} 이(가) 없습니다 — ${path}`);
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (err) {
    fail(`${what} 을(를) 읽지 못했습니다 — ${err.message}`);
  }
}

function requireStrings(obj, keys, what) {
  for (const key of keys) {
    if (typeof obj[key] !== 'string' || !obj[key].trim()) fail(`${what} 에 ${key} 가 없습니다`);
  }
}

// ── 전역 분류 ───────────────────────────────────────────────
function readTaxonomy(file, what, extra = () => {}) {
  const list = readJson(join(ROOT, file), file);
  if (!Array.isArray(list) || list.length === 0) fail(`${file} 은 비어 있지 않은 배열이어야 합니다`);
  const seen = new Set();
  for (const item of list) {
    requireStrings(item, ['id', 'name', 'summary'], `${file} 항목`);
    if (!SLUG.test(item.id)) fail(`${file} 의 id "${item.id}" 는 소문자·숫자·하이픈만 쓸 수 있습니다`);
    if (seen.has(item.id)) fail(`${file} 에 id "${item.id}" 가 두 번 나옵니다`);
    seen.add(item.id);
    extra(item);
  }
  return list;
}

// ── 다이어그램 하나 ─────────────────────────────────────────
function readDiagram(project, id, categories, phaseIds) {
  const dir = join(PROJECTS, project, 'diagrams', id);
  if (!SLUG.test(id)) fail(`${project}/${id}: 폴더 이름은 소문자·숫자·하이픈만 쓸 수 있습니다`);

  const where = `${project}/${id}/meta.json`;
  const meta = readJson(join(dir, 'meta.json'), where);
  requireStrings(meta, ['title', 'phase', 'category', 'kind', 'summary'], where);

  if (!phaseIds.has(meta.phase)) {
    fail(`${where} 의 phase "${meta.phase}" 가 phases.json 에 없습니다 — 쓸 수 있는 값: ${[...phaseIds].join(', ')}`);
  }
  if (!categories.has(meta.category)) {
    fail(`${where} 의 category "${meta.category}" 가 categories.json 에 없습니다 — 쓸 수 있는 값: ${[...categories.keys()].join(', ')}`);
  }
  const kinds = categories.get(meta.category).kinds;
  if (!kinds.includes(meta.kind)) {
    fail(`${where} 의 kind "${meta.kind}" 는 ${meta.category} 카테고리에 없습니다 — 쓸 수 있는 값: ${kinds.join(', ')}`);
  }
  if (!Array.isArray(meta.tags) || meta.tags.some((t) => typeof t !== 'string')) {
    fail(`${where} 의 tags 는 문자열 배열이어야 합니다`);
  }
  // updated 는 선택 사항이다. git 로그에서 뽑으면 커밋할 때마다 값이 바뀌어
  // --check 가 영원히 어긋나므로, 손으로 적는 YYYY-MM-DD 로 둔다.
  const updated = typeof meta.updated === 'string' ? meta.updated : null;
  if (updated && !/^\d{4}-\d{2}-\d{2}$/.test(updated)) {
    fail(`${where} 의 updated 는 YYYY-MM-DD 형식이어야 합니다`);
  }

  const formats = {};
  for (const [name, file] of Object.entries(FORMATS)) {
    if (existsSync(join(dir, file))) formats[name] = `projects/${project}/diagrams/${id}/${file}`;
  }
  if (!formats.html) fail(`${project}/${id}/diagram.html 이 없습니다 — 뷰어가 보여줄 것이 없습니다`);

  return {
    id,
    project,
    title: meta.title,
    phase: meta.phase,
    category: meta.category,
    kind: meta.kind,
    tags: meta.tags,
    summary: meta.summary,
    order: Number.isFinite(meta.order) ? meta.order : 999,
    ...(updated ? { updated } : {}),
    formats,
  };
}

const dirsIn = (path) => readdirSync(path).filter((n) => statSync(join(path, n)).isDirectory()).sort();

function build() {
  const catList = readTaxonomy('categories.json', '카테고리', (c) => {
    if (!Array.isArray(c.kinds) || c.kinds.some((k) => typeof k !== 'string')) {
      fail(`categories.json 의 ${c.id}.kinds 는 문자열 배열이어야 합니다`);
    }
  });
  const phaseList = readTaxonomy('phases.json', '설계 단계');
  const catMap = new Map(catList.map((c) => [c.id, c]));
  const phaseIds = new Set(phaseList.map((p) => p.id));
  const phaseRank = new Map(phaseList.map((p, i) => [p.id, i]));

  if (!existsSync(PROJECTS)) fail('projects/ 폴더가 없습니다');
  const projectIds = dirsIn(PROJECTS);
  if (projectIds.length === 0) fail('projects/ 아래에 프로젝트가 하나도 없습니다');

  const diagrams = [];
  const projects = [];
  const seenSlugs = new Map();

  for (const pid of projectIds) {
    if (!SLUG.test(pid)) fail(`프로젝트 폴더 "${pid}" 는 소문자·숫자·하이픈만 쓸 수 있습니다`);
    const meta = readJson(join(PROJECTS, pid, 'project.json'), `${pid}/project.json`);
    requireStrings(meta, ['name', 'summary'], `${pid}/project.json`);

    const dgDir = join(PROJECTS, pid, 'diagrams');
    if (!existsSync(dgDir)) fail(`${pid}/diagrams/ 폴더가 없습니다`);
    const mine = dirsIn(dgDir).map((id) => {
      // 뷰어 URL 해시가 slug 하나뿐이므로 프로젝트를 넘나들어 고유해야 한다
      if (seenSlugs.has(id)) fail(`다이어그램 slug "${id}" 가 ${seenSlugs.get(id)} 와 ${pid} 에 중복됩니다`);
      seenSlugs.set(id, pid);
      return readDiagram(pid, id, catMap, phaseIds);
    });
    if (mine.length === 0) fail(`${pid} 에 다이어그램이 하나도 없습니다`);

    const covered = new Set(mine.map((d) => d.kind));
    projects.push({
      id: pid,
      ...meta,
      count: mine.length,
      // 이 프로젝트에 아직 없는 대표 종류 = 남은 설계 산출물
      missing: catList.flatMap((c) => c.kinds.filter((k) => !covered.has(k)).map((k) => `${c.name}/${k}`)),
    });
    diagrams.push(...mine);
  }

  diagrams.sort(
    (a, b) =>
      a.project.localeCompare(b.project) ||
      phaseRank.get(a.phase) - phaseRank.get(b.phase) ||
      a.order - b.order ||
      a.title.localeCompare(b.title, 'ko')
  );

  const phases = phaseList.map((p) => ({ ...p, count: diagrams.filter((d) => d.phase === p.id).length }));
  const coveredAll = new Set(diagrams.map((d) => d.kind));
  const categories = catList.map((c) => ({
    ...c,
    kinds: c.kinds.map((k) => ({ name: k, covered: coveredAll.has(k) })),
    count: diagrams.filter((d) => d.category === c.id).length,
  }));
  const tags = [...new Set(diagrams.flatMap((d) => d.tags))].sort((a, b) => a.localeCompare(b, 'ko'));

  return JSON.stringify({ phases, categories, tags, projects, diagrams }, null, 2) + '\n';
}

// ── README 표 ───────────────────────────────────────────────
function renderTable(index) {
  const phaseName = new Map(index.phases.map((p) => [p.id, p.name]));
  const rows = index.diagrams.map((d) => {
    const link = `[${d.title}](${SITE}#${d.id}/html)`;
    return `| ${phaseName.get(d.phase)} | ${d.kind} | ${link} | ${d.summary} |`;
  });
  const p = index.projects[0];
  return [
    START,
    '',
    `**${p.name}** — ${p.summary}`,
    '',
    `설계 단계순으로 ${index.diagrams.length}개입니다. 파일은 \`projects/<프로젝트>/diagrams/<slug>/\` 에 있고,`,
    '이 표는 `node tools/build-index.mjs` 가 만들므로 직접 고치지 마세요.',
    '',
    '| 단계 | 종류 | 다이어그램 | 요약 |',
    '| --- | --- | --- | --- |',
    ...rows,
    '',
    END,
  ].join('\n');
}

function spliceDoc(table) {
  const doc = readFileSync(DOC, 'utf8');
  const a = doc.indexOf(START);
  const b = doc.indexOf(END);
  if (a === -1 || b === -1 || b < a) fail(`README.md 에 ${START} / ${END} 표시가 없습니다`);
  return doc.slice(0, a) + table + doc.slice(b + END.length);
}

const json = build();
const parsed = JSON.parse(json);
const count = parsed.diagrams.length;
const doc = spliceDoc(renderTable(parsed));

if (process.argv.includes('--check')) {
  if ((existsSync(OUT) ? readFileSync(OUT, 'utf8') : '') !== json) {
    fail('diagrams.json 이 meta.json 들과 어긋납니다 — `node tools/build-index.mjs` 를 실행해 커밋하세요');
  }
  if (readFileSync(DOC, 'utf8') !== doc) {
    fail('README.md 의 다이어그램 표가 어긋납니다 — `node tools/build-index.mjs` 를 실행해 커밋하세요');
  }
  console.log(`build-index: diagrams.json · README 표 최신입니다 (${count}개)`);
} else {
  writeFileSync(OUT, json);
  writeFileSync(DOC, doc);
  console.log(`build-index: diagrams.json · README 표 갱신 (${count}개)`);
}

// 아직 그리지 않은 대표 종류는 실패가 아니라 남은 설계 산출물이다.
for (const p of parsed.projects) {
  if (p.missing.length > 0) {
    console.log(`build-index: ${p.name} 에 아직 없는 산출물 ${p.missing.length}개 — ${p.missing.join(', ')}`);
  }
}
