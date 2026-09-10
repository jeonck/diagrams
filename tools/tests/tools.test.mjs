// 도구가 잘못 동작하면 잡는다.
//
//   node --test tools/tests/
//
// 저장소를 임시 폴더로 통째로 복사해 그 안에서 진짜 명령을 돌린다.
// 도구들이 자기 파일 위치를 기준으로 경로를 잡으므로, 복사본 안의 도구는
// 복사본만 건드린다 — 진짜 저장소는 안전하다.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync, appendFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const COPY = ['projects', 'tools', 'phases.json', 'categories.json', 'diagrams.json', 'README.md', 'index.html'];

function sandbox(t) {
  const dir = mkdtempSync(join(tmpdir(), 'diagrams-test-'));
  for (const entry of COPY) cpSync(join(REPO, entry), join(dir, entry), { recursive: true });
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function run(dir, cmd, args) {
  const r = spawnSync(cmd, args.map((a) => (a.startsWith('tools/') ? join(dir, a) : a)), {
    cwd: dir,
    encoding: 'utf8',
  });
  return { code: r.status, out: (r.stdout || '') + (r.stderr || '') };
}

const index = (dir, ...args) => run(dir, 'node', ['tools/build-index.mjs', ...args]);
const fresh = (dir, ...args) => run(dir, 'node', ['tools/check-freshness.mjs', ...args]);
const draw = (dir, ...args) => run(dir, 'python3', ['tools/generators/build.py', ...args]);
const scaffold = (dir, ...args) => run(dir, 'node', ['tools/new-diagram.mjs', ...args]);

const meta = (dir, project, slug) => join(dir, 'projects', project, 'diagrams', slug, 'meta.json');
const readMeta = (p) => JSON.parse(readFileSync(p, 'utf8'));
const writeMeta = (p, m) => writeFileSync(p, JSON.stringify(m, null, 2) + '\n');
const adr = (dir, project, file) => join(dir, 'projects', project, 'decisions', file);

// ── build-index ───────────────────────────────────────────

test('깨끗한 저장소에서는 --check 가 통과한다', (t) => {
  const dir = sandbox(t);
  const r = index(dir, '--check');
  assert.equal(r.code, 0, r.out);
  assert.match(r.out, /최신입니다/);
});

test('두 번 만들어도 같은 diagrams.json 이 나온다', (t) => {
  const dir = sandbox(t);
  assert.equal(index(dir).code, 0);
  const first = readFileSync(join(dir, 'diagrams.json'), 'utf8');
  assert.equal(index(dir).code, 0);
  assert.equal(readFileSync(join(dir, 'diagrams.json'), 'utf8'), first);
});

test('meta.json 에 필수 항목이 빠지면 파일 이름과 함께 멈춘다', (t) => {
  const dir = sandbox(t);
  const p = meta(dir, 'order-platform', 'order-erd');
  const m = readMeta(p);
  delete m.summary;
  writeMeta(p, m);
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /order-erd\/meta\.json 에 summary 가 없습니다/);
});

test('phase 가 틀리면 쓸 수 있는 값을 알려준다', (t) => {
  const dir = sandbox(t);
  const p = meta(dir, 'order-platform', 'order-erd');
  writeMeta(p, { ...readMeta(p), phase: '설계' });
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /requirements, analysis, design, operations/);
});

test('kind 가 카테고리에 없으면 멈춘다', (t) => {
  const dir = sandbox(t);
  const p = meta(dir, 'order-platform', 'order-erd');
  writeMeta(p, { ...readMeta(p), kind: '없는종류' });
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /카테고리에 없습니다 — 쓸 수 있는 값: .*\(/);
});

test('슬러그가 프로젝트를 넘나들어 겹치면 멈춘다', (t) => {
  const dir = sandbox(t);
  cpSync(join(dir, 'projects/order-platform/diagrams/order-erd'),
         join(dir, 'projects/notify-hub/diagrams/order-erd'), { recursive: true });
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /중복됩니다/);
});

test('ADR 이 없는 다이어그램을 가리키면 멈춘다', (t) => {
  const dir = sandbox(t);
  const p = adr(dir, 'order-platform', '0001-order-as-state-machine.md');
  writeFileSync(p, readFileSync(p, 'utf8').replace('"order-state"', '"없는-그림"'));
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /없는 다이어그램 "없는-그림"/);
});

test('같은 그림을 basis 와 diagrams 양쪽에 적으면 멈춘다', (t) => {
  const dir = sandbox(t);
  const p = adr(dir, 'order-platform', '0006-manual-approval-before-production.md');
  writeFileSync(p, readFileSync(p, 'utf8').replace('"basis": ["value-stream"]', '"basis": ["cicd-pipeline"]'));
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /근거인지 결과인지 하나만 고르세요/);
});

test('대체됨인데 supersededBy 가 없으면 멈춘다', (t) => {
  const dir = sandbox(t);
  const p = adr(dir, 'order-platform', '0002-session-in-app-memory.md');
  // 머리말을 제대로 읽어 supersededBy 만 빼고 다시 쓴다
  const raw = readFileSync(p, 'utf8');
  const m = /^---\n([\s\S]*?)\n---\n/.exec(raw);
  const head = JSON.parse(m[1]);
  delete head.supersededBy;
  writeFileSync(p, '---\n' + JSON.stringify(head, null, 2) + '\n---\n' + raw.slice(m[0].length));
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /status 가 대체됨이면 supersededBy 를 적어야 합니다/);
});

test('본문이 없는 이미지를 가리키면 멈춘다', (t) => {
  const dir = sandbox(t);
  const p = adr(dir, 'order-platform', '0001-order-as-state-machine.md');
  appendFileSync(p, '\n![그림](assets/없는파일.png)\n');
  const r = index(dir, '--check');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /이미지 "assets\/없는파일\.png"/);
});

// ── check-freshness ───────────────────────────────────────

test('낡은 그림이 없으면 없다고 말하고 0 으로 끝난다', (t) => {
  const dir = sandbox(t);
  const r = fresh(dir);
  assert.equal(r.code, 0, r.out);
  assert.match(r.out, /낡았을 수 있는 다이어그램: 없음/);
});

test('결정이 그림보다 나중이면 결과 그림만 잡고 근거 그림은 안 잡는다', (t) => {
  const dir = sandbox(t);
  const p = adr(dir, 'order-platform', '0006-manual-approval-before-production.md');
  writeFileSync(p, readFileSync(p, 'utf8').replace('"date": "2026-09-08"', '"date": "2099-01-01"'));
  assert.equal(index(dir).code, 0);

  const r = fresh(dir);
  assert.match(r.out, /cicd-pipeline/);
  assert.doesNotMatch(r.out, /value-stream/);
  assert.equal(r.code, 0, '기본은 보고만 한다');
  assert.equal(fresh(dir, '--strict').code, 1, '--strict 는 1 로 끝난다');
});

// ── 생성기 ────────────────────────────────────────────────

test('스펙과 산출물이 맞으면 build.py --check 가 통과한다', (t) => {
  const dir = sandbox(t);
  const r = draw(dir, '--check');
  assert.equal(r.code, 0, r.out);
  assert.match(r.out, /일치합니다/);
});

test('그림 파일을 손으로 고치면 build.py --check 가 잡는다', (t) => {
  const dir = sandbox(t);
  appendFileSync(join(dir, 'projects/order-platform/diagrams/order-class/diagram.html'), '\n<!-- 손댐 -->\n');
  const r = draw(dir, '--check');
  assert.equal(r.code, 1);
  assert.match(r.out, /order-class\/diagram\.html/);
});

// ── new-diagram ───────────────────────────────────────────

test('새 그림을 만들면 그 자리에서 모든 검사가 통과한다', (t) => {
  const dir = sandbox(t);
  const r = scaffold(dir, 'order-platform/test-timeline',
    '--title', '시험 타임라인', '--phase', 'design', '--category', 'behavior',
    '--kind', '시퀀스', '--summary', '한 줄', '--template', 'sequence');
  assert.equal(r.code, 0, r.out);

  const m = readMeta(meta(dir, 'order-platform', 'test-timeline'));
  assert.equal(m.title, '시험 타임라인');
  assert.equal(m.phase, 'design');

  assert.equal(index(dir, '--check').code, 0, '목록이 이미 갱신돼 있어야 한다');
  assert.equal(draw(dir, '--check').code, 0, '그림이 이미 찍혀 있어야 한다');
});

test('이미 있는 슬러그로는 만들지 않는다', (t) => {
  const dir = sandbox(t);
  const r = scaffold(dir, 'notify-hub/order-erd',
    '--title', 'x', '--phase', 'design', '--category', 'structure',
    '--kind', '클래스', '--summary', 'y');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /이미 order-platform 에 있습니다/);
});

test('kind 를 틀리면 쓸 수 있는 값을 알려준다', (t) => {
  const dir = sandbox(t);
  const r = scaffold(dir, 'order-platform/test-x',
    '--title', 'x', '--phase', 'design', '--category', 'structure',
    '--kind', '없는것', '--summary', 'y');
  assert.notEqual(r.code, 0);
  assert.match(r.out, /쓸 수 있는 값: 클래스 \(Class\), 컴포넌트 \(Component\)/);
});
