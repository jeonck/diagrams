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
const ADR = /^(\d{4})-[a-z0-9]+(-[a-z0-9]+)*\.md$/;
const STATUSES = ['제안됨', '채택됨', '대체됨', '폐기됨'];

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

// ADR 은 파일 맨 앞의 JSON 머리말로 기계가 읽는다.
// YAML 파서를 들이지 않으려고 JSON 을 쓴다 — node 에 내장 파서가 없다.
function readDecision(project, file) {
  const where = `${project}/decisions/${file}`;
  if (!ADR.test(file)) fail(`${where}: 파일 이름은 0001-소문자-하이픈.md 형식이어야 합니다`);

  const raw = readFileSync(join(PROJECTS, project, 'decisions', file), 'utf8');
  const m = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/.exec(raw);
  if (!m) fail(`${where}: 파일 맨 앞에 --- 로 감싼 JSON 머리말이 있어야 합니다`);
  let head;
  try {
    head = JSON.parse(m[1]);
  } catch (err) {
    fail(`${where}: 머리말 JSON 을 읽지 못했습니다 — ${err.message}`);
  }
  requireStrings(head, ['title', 'status', 'date'], where);
  if (!STATUSES.includes(head.status)) {
    fail(`${where} 의 status "${head.status}" 는 쓸 수 없습니다 — ${STATUSES.join(', ')} 중 하나여야 합니다`);
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(head.date)) fail(`${where} 의 date 는 YYYY-MM-DD 형식이어야 합니다`);
  const diagrams = head.diagrams ?? [];
  if (!Array.isArray(diagrams) || diagrams.some((d) => typeof d !== 'string')) {
    fail(`${where} 의 diagrams 는 문자열 배열이어야 합니다`);
  }
  if (!m[2].trim()) fail(`${where}: 머리말 뒤에 본문이 없습니다`);

  // 본문이 가리키는 그림 파일이 실제로 있는지 본다. 깨진 이미지는 배포 뒤에야 보인다.
  const dir = join(PROJECTS, project, 'decisions');
  for (const [, alt, src] of m[2].matchAll(/!\[([^\]]*)\]\(([^)\s]+)\)/g)) {
    if (/^[a-z]+:/i.test(src) || src.startsWith('/')) continue;
    if (!existsSync(join(dir, src))) {
      fail(`${where}: 이미지 "${src}" (${alt || '설명 없음'}) 를 찾을 수 없습니다`);
    }
  }

  return {
    id: file.replace(/\.md$/, ''),
    number: file.slice(0, 4),
    project,
    title: head.title,
    status: head.status,
    date: head.date,
    diagrams,
    supersedes: head.supersedes ?? null,
    supersededBy: head.supersededBy ?? null,
    path: `projects/${project}/decisions/${file}`,
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
  const decisions = [];
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

    // ADR 은 선택 사항이다. 없는 프로젝트도 있을 수 있다.
    const adrDir = join(PROJECTS, pid, 'decisions');
    const myAdrs = existsSync(adrDir)
      ? readdirSync(adrDir).filter((f) => f.endsWith('.md')).sort().map((f) => readDecision(pid, f))
      : [];
    const slugs = new Set(mine.map((d) => d.id));
    const adrIds = new Set(myAdrs.map((a) => a.id));
    for (const a of myAdrs) {
      for (const d of a.diagrams) {
        if (!slugs.has(d)) fail(`${a.path} 가 없는 다이어그램 "${d}" 를 가리킵니다`);
      }
      for (const [key, ref] of [['supersedes', a.supersedes], ['supersededBy', a.supersededBy]]) {
        if (ref && !adrIds.has(ref)) fail(`${a.path} 의 ${key} "${ref}" 에 해당하는 ADR 이 없습니다`);
      }
      if (a.status === '대체됨' && !a.supersededBy) {
        fail(`${a.path}: status 가 대체됨이면 supersededBy 를 적어야 합니다`);
      }
    }
    decisions.push(...myAdrs);

    const covered = new Set(mine.map((d) => d.kind));
    projects.push({
      id: pid,
      ...meta,
      order: Number.isFinite(meta.order) ? meta.order : 999,
      count: mine.length,
      decisions: myAdrs.length,
      // 이 프로젝트에 아직 없는 대표 종류 = 남은 설계 산출물
      missing: catList.flatMap((c) => c.kinds.filter((k) => !covered.has(k)).map((k) => `${c.name}/${k}`)),
    });
    diagrams.push(...mine);
  }

  // 프로젝트 순서는 project.json 의 order 가 정한다. 폴더 이름순은 뜻이 없다.
  projects.sort((a, b) => a.order - b.order || a.name.localeCompare(b.name, 'ko'));
  const projectRank = new Map(projects.map((p, i) => [p.id, i]));

  diagrams.sort(
    (a, b) =>
      projectRank.get(a.project) - projectRank.get(b.project) ||
      phaseRank.get(a.phase) - phaseRank.get(b.phase) ||
      a.order - b.order ||
      a.title.localeCompare(b.title, 'ko')
  );

  // 다이어그램에서 결정으로 거꾸로 갈 수 있게 한다
  decisions.sort((a, b) => projectRank.get(a.project) - projectRank.get(b.project) || a.id.localeCompare(b.id));
  for (const d of diagrams) {
    d.decisions = decisions.filter((a) => a.project === d.project && a.diagrams.includes(d.id)).map((a) => a.id);
  }

  const phases = phaseList.map((p) => ({ ...p, count: diagrams.filter((d) => d.phase === p.id).length }));
  const coveredAll = new Set(diagrams.map((d) => d.kind));
  const categories = catList.map((c) => ({
    ...c,
    kinds: c.kinds.map((k) => ({ name: k, covered: coveredAll.has(k) })),
    count: diagrams.filter((d) => d.category === c.id).length,
  }));
  const tags = [...new Set(diagrams.flatMap((d) => d.tags))].sort((a, b) => a.localeCompare(b, 'ko'));

  return JSON.stringify({ phases, categories, tags, projects, diagrams, decisions }, null, 2) + '\n';
}

// ── README 표 ───────────────────────────────────────────────
function renderTable(index) {
  const phaseName = new Map(index.phases.map((p) => [p.id, p.name]));
  const lines = [
    START,
    '',
    `프로젝트 ${index.projects.length}개 · 다이어그램 ${index.diagrams.length}개입니다.`,
    '이 표는 `node tools/build-index.mjs` 가 만들므로 직접 고치지 마세요.',
  ];
  for (const p of index.projects) {
    const mine = index.diagrams.filter((d) => d.project === p.id);
    lines.push(
      '',
      `### ${p.name}`,
      '',
      `${p.summary}`,
      '',
      `\`projects/${p.id}/\` · ${p.status} · 다이어그램 ${p.count}개 · 설계 결정 ${p.decisions}개`
    );
    if (p.missing.length > 0) {
      lines.push('', `아직 그리지 않은 대표 종류 ${p.missing.length}개 — ${p.missing.join(', ')}`);
    }
    lines.push('', '| 단계 | 종류 | 다이어그램 | 요약 |', '| --- | --- | --- | --- |');
    for (const d of mine) {
      lines.push(`| ${phaseName.get(d.phase)} | ${d.kind} | [${d.title}](${SITE}#${d.id}/html) | ${d.summary} |`);
    }
  }
  lines.push('', END);
  return lines.join('\n');
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
