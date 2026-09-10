"""스펙 파일들이 공통으로 쓰는 진입점 — lib/ 를 경로에 올리고 도구를 넘겨준다."""
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib')))

from emit import N, E, Z, emit, emit_seq  # noqa: E402,F401
