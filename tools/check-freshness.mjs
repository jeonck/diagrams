// 다이어그램이 낡았는지 본다.
//
//   node tools/check-freshness.mjs            보고만 한다 (종료코드 0)
//   node tools/check-freshness.mjs --strict   낡은 게 있으면 1 로 끝난다
//
// 두 가지를 본다.
//
//   1. 결정보다 뒤처진 그림 — 그 결정이 만든(diagrams) 그림이 결정보다 오래됐다.
//      결정의 근거로 본(basis) 그림은 세지 않는다 — 결정이 바뀌어도 근거는 그대로다.
//      커밋된 날짜만 쓰므로 git 없이도 돌아간다.
//   2. 코드보다 뒤처진 그림 — meta.json 의 sources 에 적힌 경로가 updated 이후에
//      바뀌었다. git 로그를 보므로 전체 이력이 있어야 한다 (fetch-depth: 0).
//
// 낡음은 "틀렸다" 가 아니라 "확인해 보라" 는 신호다. 그래서 기본은 보고만 한다.

import { execFileSync } from 'node:child_process';
import { appendFileSync, readFileSync, existsSync } from 'node:fs';

const STRICT = process.argv.includes('--strict');
const INDEX = 'diagrams.json';

function lastChange(paths) {
  // 해당 경로들을 마지막으로 건드린 커밋 날짜 (YYYY-MM-DD). 이력이 없으면 null.
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%cs', '--', ...paths], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return out || null;
  } catch {
    return null;
  }
}

function hasFullHistory() {
  try {
    const shallow = execFileSync('git', ['rev-parse', '--is-shallow-repository'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return shallow === 'false';
  } catch {
    return false;
  }
}

if (!existsSync(INDEX)) {
  console.error(`check-freshness: ${INDEX} 가 없습니다. 먼저 node tools/build-index.mjs 를 돌리세요.`);
  process.exit(1);
}

const index = JSON.parse(readFileSync(INDEX, 'utf8'));
const adr = new Map(index.decisions.map((a) => [a.id, a]));
const projectName = new Map(index.projects.map((p) => [p.id, p.name]));

const stale = [];
const withSources = index.diagrams.filter((d) => d.sources?.length);
const full = hasFullHistory();

for (const d of index.diagrams) {
  // 1. 결정보다 뒤처졌나
  for (const id of d.staleBy ?? []) {
    const a = adr.get(id);
    if (!a) continue;
    stale.push({
      id: d.id,
      project: d.project,
      updated: d.updated,
      why: `결정 ${a.number} (${a.title}) 가 ${a.date} 에 정해졌습니다`,
    });
  }

  // 2. 코드보다 뒤처졌나
  if (!d.sources?.length || !full) continue;
  const when = lastChange(d.sources);
  if (when && d.updated && when > d.updated) {
    stale.push({
      id: d.id,
      project: d.project,
      updated: d.updated,
      why: `코드(${d.sources.join(', ')})가 ${when} 에 바뀌었습니다`,
    });
  }
}

const lines = [];
const basisLinks = index.decisions.reduce((n, a) => n + (a.basis?.length ?? 0), 0);
lines.push(
  `다이어그램 ${index.diagrams.length}개 · sources 를 적은 그림 ${withSources.length}개` +
  ` · 근거로만 걸린 링크 ${basisLinks}건 (낡음 판정에서 제외)`
);
if (withSources.length && !full) {
  lines.push('※ 얕은 클론이라 코드 변경일을 볼 수 없습니다 — 결정 기준으로만 검사했습니다.');
}

if (stale.length === 0) {
  lines.push('');
  lines.push('낡았을 수 있는 다이어그램: 없음');
} else {
  lines.push('');
  lines.push(`낡았을 수 있는 다이어그램 ${stale.length}건`);
  lines.push('');
  for (const s of stale) {
    lines.push(`  ${s.id}  (${projectName.get(s.project) ?? s.project}, 수정 ${s.updated})`);
    lines.push(`    ${s.why}`);
  }
  lines.push('');
  lines.push('  그림을 확인하고, 고쳤거나 볼 필요가 없었다면 meta.json 의 updated 를 오늘 날짜로 바꾸세요.');
}

const text = lines.join('\n');
console.log('check-freshness: ' + text);

// GitHub Actions 에서는 잡 요약에도 남긴다
if (process.env.GITHUB_STEP_SUMMARY) {
  const body = stale.length
    ? ['## 낡았을 수 있는 다이어그램', '', '| 다이어그램 | 수정 | 이유 |', '|---|---|---|',
       ...stale.map((s) => `| \`${s.id}\` | ${s.updated} | ${s.why} |`)].join('\n')
    : '## 다이어그램 최신성\n\n낡았을 수 있는 다이어그램이 없습니다.';
  appendFileSync(process.env.GITHUB_STEP_SUMMARY, body + '\n');
}

process.exit(STRICT && stale.length ? 1 : 0);
