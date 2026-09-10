// 새 다이어그램의 뼈대를 만든다.
//
//   node tools/new-diagram.mjs order-platform/order-timeline \
//     --title "주문 타임라인" --phase design --category behavior --kind 시퀀스 \
//     --summary "주문 한 건이 시간 축에서 어떻게 흐르는가" \
//     --tags 시퀀스,주문 --template sequence
//
// meta.json 과 스펙을 만들고, 그림을 한 번 찍고, 목록까지 갱신한다.
// 그래서 이 명령 하나로 뷰어에 바로 보인다 — 그 다음에 스펙의 좌표를 고치면 된다.

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..');
const SPECS = join(REPO, 'tools', 'generators', 'specs');
const SLUG = /^[a-z0-9][a-z0-9-]*$/;

const die = (msg) => {
  console.error('new-diagram: ' + msg);
  process.exit(1);
};

const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'));

// ── 인자 ──────────────────────────────────────────────────
const argv = process.argv.slice(2);
if (!argv.length || argv[0] === '--help' || argv[0] === '-h') {
  // 파일 맨 앞의 설명 덩어리만 도움말로 쓴다
  const head = [];
  for (const l of readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n')) {
    if (!l.startsWith('//')) break;
    head.push(l.replace(/^\/\/ ?/, ''));
  }
  console.log(head.join('\n'));
  process.exit(0);
}
const target = argv[0];
const opts = {};
for (let i = 1; i < argv.length; i += 2) {
  if (!argv[i].startsWith('--')) die(`옵션은 --이름 값 꼴이어야 합니다: "${argv[i]}"`);
  opts[argv[i].slice(2)] = argv[i + 1];
}

const [project, slug] = target.split('/');
if (!project || !slug) die('첫 인자는 <프로젝트>/<슬러그> 여야 합니다 (예: order-platform/order-timeline)');

// ── 검증 ──────────────────────────────────────────────────
const projectsDir = join(REPO, 'projects');
const projectIds = readdirSync(projectsDir).filter((n) => statSync(join(projectsDir, n)).isDirectory());
if (!projectIds.includes(project)) {
  die(`"${project}" 프로젝트가 없습니다 — 쓸 수 있는 값: ${projectIds.join(', ')}`);
}
if (!SLUG.test(slug)) die(`슬러그 "${slug}" 는 소문자·숫자·하이픈만 쓸 수 있습니다`);

// 슬러그는 프로젝트를 넘나들어 고유해야 한다 (뷰어 URL 해시가 슬러그 하나뿐이다)
for (const p of projectIds) {
  const dir = join(projectsDir, p, 'diagrams');
  if (existsSync(dir) && readdirSync(dir).includes(slug)) {
    die(`슬러그 "${slug}" 는 이미 ${p} 에 있습니다 — 다른 이름을 고르세요`);
  }
}

const phases = readJson(join(REPO, 'phases.json'));
const categories = readJson(join(REPO, 'categories.json'));

const need = (key, label) => {
  if (!opts[key] || !String(opts[key]).trim()) die(`--${key} (${label}) 가 필요합니다`);
  return String(opts[key]).trim();
};

const title = need('title', '제목');
const summary = need('summary', '한 줄 요약');

const phase = need('phase', 'SDLC 단계');
if (!phases.some((p) => p.id === phase)) {
  die(`phase "${phase}" 가 phases.json 에 없습니다 — 쓸 수 있는 값: ${phases.map((p) => p.id).join(', ')}`);
}
const category = need('category', '그림 종류 카테고리');
const cat = categories.find((c) => c.id === category);
if (!cat) {
  die(`category "${category}" 가 categories.json 에 없습니다 — 쓸 수 있는 값: ${categories.map((c) => c.id).join(', ')}`);
}
// kind 의 표준값은 한국어 이름이지만 영문 이름으로 적어도 받는다
const wanted = need('kind', '대표 종류');
const found = cat.kinds.find((k) => k.name === wanted || k.name_en === wanted);
if (!found) {
  die(
    `kind "${wanted}" 는 ${category} 카테고리에 없습니다 — 쓸 수 있는 값: ` +
      cat.kinds.map((k) => `${k.name} (${k.name_en})`).join(', ')
  );
}
const kind = found.name;

const tags = (opts.tags ?? '').split(',').map((t) => t.trim()).filter(Boolean);
const template = opts.template ?? 'box';
if (!['box', 'sequence'].includes(template)) die('--template 은 box 또는 sequence 입니다');

// 같은 프로젝트·단계 안에서 맨 뒤에 놓는다
const mine = join(projectsDir, project, 'diagrams');
let maxOrder = 0;
if (existsSync(mine)) {
  for (const d of readdirSync(mine)) {
    const f = join(mine, d, 'meta.json');
    if (!existsSync(f)) continue;
    const m = readJson(f);
    if (m.phase === phase && Number.isFinite(m.order)) maxOrder = Math.max(maxOrder, m.order);
  }
}
const order = Number.isFinite(Number(opts.order)) && opts.order !== undefined
  ? Number(opts.order)
  : maxOrder + 10;

const today = new Date().toISOString().slice(0, 10);

// ── meta.json ─────────────────────────────────────────────
mkdirSync(join(mine, slug), { recursive: true });
const meta = { title, phase, category, kind, tags, summary, updated: today, order };
writeFileSync(join(mine, slug, 'meta.json'), JSON.stringify(meta, null, 2) + '\n');

// ── 스펙 ──────────────────────────────────────────────────
const q = (s) => JSON.stringify(s); // 파이썬 문자열로도 그대로 쓸 수 있다
// 흔들림은 슬러그에서 뽑아 고정한다 — 다시 찍어도 같은 그림이 나온다
const seed = [...slug].reduce((n, c) => (n * 31 + c.charCodeAt(0)) % 9973, 7) + 1;

const boxSpec = `"""${title} — ${project}"""
from _bootstrap import N, E, Z, emit

# 좌표는 SVG 픽셀, 원점은 왼쪽 위입니다. 상자를 옮기면 거기 붙은 선도 함께 옮기세요.
# 색은 의미색 여섯 가지만 씁니다: input · process · storage · external · neutral · risk
nodes = [
 N(80, 150, 240, 90, 'input', '첫 단계', ['한 줄 설명']),
 N(420, 150, 240, 90, 'process', '가운데', ['한 줄 설명']),
 N(760, 150, 240, 90, 'storage', '끝', ['한 줄 설명']),
]
edges = [
 E([(320, 195), (420, 195)], '지나간다'),
 E([(660, 195), (760, 195)], '도착한다'),
]

emit(${q(project)}, ${q(slug)}, ${q(title)}, 1080, 420,
     ${q(title)}, ${q(summary)},
     nodes, edges, (),
     ['※ 아직 뼈대입니다 — 이 스펙을 고치고 build.py 로 다시 찍으세요.'],
     [], seed=${seed})
`;

const seqSpec = `"""${title} — ${project}"""
from _bootstrap import emit_seq

# 참여자 간격은 280 을 씁니다 — 다른 시퀀스 그림과 눈금이 맞습니다.
A, B, C = 130, 410, 690

emit_seq(${q(project)}, ${q(slug)}, ${q(title)}, 820, 560,
  ${q(title)}, ${q(summary)},
  [(A, 'external', '보내는 쪽', '누가'),
   (B, 'input', '받는 쪽', '무엇이'),
   (C, 'process', '처리하는 쪽', '어디서')],
  # (y, 출발, 도착, 라벨, 반환인가)
  [(220, A, B, '① 요청', False),
   (300, B, C, '② 넘긴다', False),
   (360, C, B, '결과', True),
   (420, B, A, '응답', True)],
  # 자기 자신에게 보내는 메시지 (cx, y0, y1, 라벨)
  [(B, 250, 276, '검증')],
  # 활성 구간 (cx, y0, y1, 색)
  [(A, 222, 418, 'external'), (B, 222, 418, 'input'), (C, 298, 358, 'process')],
  ['※ 아직 뼈대입니다 — 이 스펙을 고치고 build.py 로 다시 찍으세요.'],
  seed=${seed})
`;

const specPath = join(SPECS, slug + '.py');
if (existsSync(specPath)) die(`스펙 ${specPath} 가 이미 있습니다`);
writeFileSync(specPath, template === 'sequence' ? seqSpec : boxSpec);

// ── 찍고, 목록 갱신 ───────────────────────────────────────
const run = (cmd, args) => {
  try {
    return execFileSync(cmd, args, { cwd: REPO, encoding: 'utf8' });
  } catch (err) {
    console.error(err.stdout || '');
    console.error(err.stderr || '');
    die(`${cmd} ${args.join(' ')} 가 실패했습니다`);
  }
};
run('python3', ['tools/generators/build.py', slug]);
run('node', ['tools/build-index.mjs']);

console.log(`
new-diagram: ${project}/${slug} 를 만들었습니다.

  projects/${project}/diagrams/${slug}/meta.json
  projects/${project}/diagrams/${slug}/diagram.html
  projects/${project}/diagrams/${slug}/diagram.excalidraw
  tools/generators/specs/${slug}.py     ← 여기를 고치세요

다음 순서

  1. tools/generators/specs/${slug}.py 의 좌표와 문구를 고칩니다
  2. python3 tools/generators/build.py ${slug}
  3. python3 -m http.server 로 열어 #${slug}/html 에서 눈으로 봅니다
  4. 스펙과 산출물, meta.json, diagrams.json 을 함께 커밋합니다
`);
