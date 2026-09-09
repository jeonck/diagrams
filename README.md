# diagrams

다이어그램 모음.

공개 주소: **https://jeonck.github.io/diagrams/**
(`main` 에 푸시하면 `.github/workflows/pages.yml` 이 GitHub Pages로 자동 배포합니다.)

## 뷰어

- [`index.html`](index.html) — 저장소의 다이어그램을 브라우저에서 바로 보는 뷰어.
  SVG/HTML 버전은 iframe으로, Excalidraw 버전은 페이지에 내장된 간이 렌더러로 그립니다.
  외부 스크립트·CDN을 전혀 쓰지 않으며, `#mvc/excalidraw` 같은 해시로 특정 다이어그램·형식을 바로 열 수 있습니다.

  Excalidraw 미리보기는 `fetch`로 파일을 읽기 때문에 `file://`로 직접 열면 동작하지 않습니다.
  저장소 폴더에서 `python3 -m http.server` 를 실행해 `http://localhost:8000` 으로 열거나, GitHub Pages로 보세요.
  (뷰어의 "파일 열기…" 버튼으로 `.excalidraw` 파일을 직접 선택하면 `file://`에서도 볼 수 있습니다.)

## MVC

- [`mvc/mvc-diagram.html`](mvc/mvc-diagram.html) — MVC(Model–View–Controller) 패턴의 대표 구조.
  브라우저로 열면 바로 볼 수 있는 단일 HTML 파일이며, 외부 리소스 없이 인라인 SVG로만 그려졌고 라이트/다크 모드를 모두 지원합니다.
- [`mvc/mvc-diagram.excalidraw`](mvc/mvc-diagram.excalidraw) — 같은 내용의 편집 가능한 Excalidraw 버전.
  [excalidraw.com](https://excalidraw.com) 캔버스에 끌어다 놓으면 열립니다.
