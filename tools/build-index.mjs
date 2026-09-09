#!/usr/bin/env node
// diagrams/<slug>/meta.json 들을 훑어 diagrams.json 을 만든다.
//   node tools/build-index.mjs          쓰기
//   node tools/build-index.mjs --check  커밋본이 최신인지만 확인 (CI 용)

import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'diagrams');
const CATS = join(SRC, 'categories.json');
const OUT = join(ROOT, 'diagrams.json');

const FORMATS = { html: 'diagram.html', excalidraw: 'diagram.excalidraw' };
const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const fail = (msg) => {
  console.error('build-index: ' + msg);
  process.exit(1);
};

function readCategories() {
  if (!existsSync(CATS)) fail('diagrams/categories.json 이 없습니다');
  let list;
  try {
    list = JSON.parse(readFileSync(CATS, 'utf8'));
  } catch (err) {
    fail(`categories.json 을 읽지 못했습니다 — ${err.message}`);
  }
  if (!Array.isArray(list) || list.length === 0) fail('categories.json 은 비어 있지 않은 배열이어야 합니다');
  const seen = new Set();
  for (const c of list) {
    for (const key of ['id', 'name', 'summary']) {
      if (typeof c[key] !== 'string' || !c[key].trim()) fail(`categories.json 항목에 ${key} 가 없습니다`);
    }
    if (!SLUG.test(c.id)) fail(`categories.json 의 id "${c.id}" 는 소문자·숫자·하이픈만 쓸 수 있습니다`);
    if (seen.has(c.id)) fail(`categories.json 에 id "${c.id}" 가 두 번 나옵니다`);
    seen.add(c.id);
    if (!Array.isArray(c.kinds) || c.kinds.some((k) => typeof k !== 'string')) {
      fail(`categories.json 의 ${c.id}.kinds 는 문자열 배열이어야 합니다`);
    }
  }
  return list;
}

function readDiagram(id, categoryIds) {
  const dir = join(SRC, id);
  if (!SLUG.test(id)) fail(`폴더 이름 "${id}" 은 소문자·숫자·하이픈만 쓸 수 있습니다`);

  const metaPath = join(dir, 'meta.json');
  if (!existsSync(metaPath)) fail(`${id}/meta.json 이 없습니다`);

  let meta;
  try {
    meta = JSON.parse(readFileSync(metaPath, 'utf8'));
  } catch (err) {
    fail(`${id}/meta.json 을 읽지 못했습니다 — ${err.message}`);
  }

  for (const key of ['title', 'category', 'summary']) {
    if (typeof meta[key] !== 'string' || !meta[key].trim()) {
      fail(`${id}/meta.json 에 ${key} 가 없습니다`);
    }
  }
  if (!Array.isArray(meta.tags) || meta.tags.some((t) => typeof t !== 'string')) {
    fail(`${id}/meta.json 의 tags 는 문자열 배열이어야 합니다`);
  }
  if (!categoryIds.has(meta.category)) {
    fail(
      `${id}/meta.json 의 category "${meta.category}" 가 categories.json 에 없습니다 — ` +
        `쓸 수 있는 값: ${[...categoryIds].join(', ')}`
    );
  }

  const formats = {};
  for (const [name, file] of Object.entries(FORMATS)) {
    if (existsSync(join(dir, file))) formats[name] = `diagrams/${id}/${file}`;
  }
  if (!formats.html) fail(`${id}/diagram.html 이 없습니다 — 뷰어가 보여줄 것이 없습니다`);

  // updated 는 선택 사항이다. git 로그에서 뽑으면 커밋할 때마다 값이 바뀌어
  // --check 가 영원히 어긋나므로, 손으로 적는 YYYY-MM-DD 로 둔다.
  const updated = typeof meta.updated === 'string' ? meta.updated : null;
  if (updated && !/^\d{4}-\d{2}-\d{2}$/.test(updated)) {
    fail(`${id}/meta.json 의 updated 는 YYYY-MM-DD 형식이어야 합니다`);
  }
  return {
    id,
    title: meta.title,
    category: meta.category,
    tags: meta.tags,
    summary: meta.summary,
    order: Number.isFinite(meta.order) ? meta.order : 999,
    ...(updated ? { updated } : {}),
    formats,
  };
}

function build() {
  if (!existsSync(SRC)) fail('diagrams/ 폴더가 없습니다');
  const catList = readCategories();
  const catIds = new Set(catList.map((c) => c.id));

  const ids = readdirSync(SRC)
    .filter((name) => statSync(join(SRC, name)).isDirectory())
    .sort();
  if (ids.length === 0) fail('diagrams/ 아래에 다이어그램이 하나도 없습니다');

  const diagrams = ids.map((id) => readDiagram(id, catIds));
  diagrams.sort((a, b) => a.order - b.order || a.title.localeCompare(b.title, 'ko'));

  // 카테고리는 categories.json 에 적힌 순서를 그대로 따른다.
  // 비어 있는 카테고리도 빠뜨리지 않는다 — 아직 그리지 않은 칸이 보여야 하기 때문이다.
  const categories = catList.map((c) => ({
    ...c,
    count: diagrams.filter((d) => d.category === c.id).length,
  }));

  const tags = [...new Set(diagrams.flatMap((d) => d.tags))].sort((a, b) => a.localeCompare(b, 'ko'));

  return JSON.stringify({ categories, tags, diagrams }, null, 2) + '\n';
}

const json = build();
const count = JSON.parse(json).diagrams.length;

if (process.argv.includes('--check')) {
  const current = existsSync(OUT) ? readFileSync(OUT, 'utf8') : '';
  if (current !== json) {
    fail('diagrams.json 이 meta.json 들과 어긋납니다 — `node tools/build-index.mjs` 를 실행해 커밋하세요');
  }
  console.log(`build-index: diagrams.json 최신입니다 (${count}개)`);
} else {
  writeFileSync(OUT, json);
  console.log(`build-index: diagrams.json 갱신 (${count}개)`);
}
