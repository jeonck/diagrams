#!/usr/bin/env python3
"""스펙에서 다이어그램을 다시 찍어낸다.

  python3 tools/generators/build.py              # 전부 다시 생성
  python3 tools/generators/build.py order-class  # 한 장만
  python3 tools/generators/build.py --check      # 커밋본과 같은지 확인 (CI 용, 파일을 건드리지 않음)

--check 는 임시 폴더에 생성한 뒤 바이트 단위로 비교한다. 하나라도 다르면
스펙과 산출물이 어긋난 것이므로 1 로 끝난다.
"""
import filecmp, os, runpy, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(HERE, 'specs')
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
FORMATS = ('diagram.html', 'diagram.excalidraw')


def spec_files(only):
    names = sorted(f for f in os.listdir(SPECS)
                   if f.endswith('.py') and not f.startswith('_'))
    if only:
        want = {s if s.endswith('.py') else s + '.py' for s in only}
        missing = want - set(names)
        if missing:
            sys.exit('그런 스펙이 없습니다: ' + ', '.join(sorted(missing)))
        names = [n for n in names if n in want]
    return names


def run(names, out_root):
    env = dict(os.environ)
    if out_root:
        env['DIAGRAM_OUT_ROOT'] = out_root
    for n in names:
        r = subprocess.run([sys.executable, os.path.join(SPECS, n)],
                           env=env, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stdout + r.stderr)
            sys.exit('생성 실패: %s' % n)
        sys.stdout.write(r.stdout)


def check(names):
    tmp = tempfile.mkdtemp(prefix='diagram-check-')
    try:
        run(names, tmp)
        bad, seen = [], 0
        for n in names:
            slug = n[:-3]
            for proj in os.listdir(os.path.join(tmp, 'projects')):
                d = os.path.join(tmp, 'projects', proj, 'diagrams', slug)
                if not os.path.isdir(d):
                    continue
                for f in FORMATS:
                    got, want = os.path.join(d, f), os.path.join(REPO, 'projects', proj, 'diagrams', slug, f)
                    if not os.path.exists(got):
                        continue
                    seen += 1
                    if not os.path.exists(want):
                        bad.append('%s/%s — 커밋본이 없습니다' % (slug, f))
                    elif not filecmp.cmp(got, want, shallow=False):
                        bad.append('%s/%s — 스펙과 커밋본이 다릅니다' % (slug, f))
        if bad:
            print('\nbuild(generators): 어긋난 산출물 %d 개' % len(bad), file=sys.stderr)
            for b in bad:
                print('  - ' + b, file=sys.stderr)
            print('\n  스펙을 고쳤다면 `python3 tools/generators/build.py` 로 다시 찍고 커밋하세요.',
                  file=sys.stderr)
            return 1
        print('\nbuild(generators): 산출물 %d 개가 스펙과 일치합니다' % seen)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv):
    args = [a for a in argv if a != '--check']
    names = spec_files(args)
    if '--check' in argv:
        return check(names)
    run(names, None)
    print('\n%d 개 다시 생성했습니다.' % len(names))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
