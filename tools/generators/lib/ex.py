"""Excalidraw 문서 빌더 — diagram-maker 스킬의 references/excalidraw-patterns.md 규칙을 따른다."""
import json, random

class Doc:
    def __init__(self, seed=20260909):
        self.rand = random.Random(seed)
        self.els = []

    def _n(self):
        return self.rand.randint(10 ** 8, 2 * 10 ** 9)

    def _base(self, **kw):
        d = dict(angle=0, strokeColor="#1e1e1e", backgroundColor="transparent", fillStyle="solid",
                 strokeWidth=2, strokeStyle="solid", roughness=1, opacity=100, groupIds=[],
                 frameId=None, roundness=None, isDeleted=False, link=None, locked=False,
                 updated=1757400000000, version=1, seed=self._n(), versionNonce=self._n(),
                 boundElements=None)
        d.update(kw)
        return d

    def _label(self, cid, s, cx, cy, size=16):
        lines = s.split("\n")
        w = max(len(l) for l in lines) * size * 0.62
        h = len(lines) * size * 1.25
        return self._base(id=cid + "_t", type="text", x=round(cx - w / 2, 1), y=round(cy - h / 2, 1),
                          width=round(w, 1), height=round(h, 1), text=s, originalText=s,
                          fontSize=size, fontFamily=1, textAlign="center", verticalAlign="middle",
                          containerId=cid, lineHeight=1.25, autoResize=True)

    def rect(self, id, x, y, w, h, bg="#ffffff", label=None, size=16, dashed=False, round=True, shape="rectangle"):
        assert not label or (w >= 120 and h >= 60), "라벨이 있는 도형은 120x60 이상이어야 한다: " + id
        self.els.append(self._base(id=id, type=shape, x=x, y=y, width=w, height=h,
                                   backgroundColor=bg, strokeStyle="dashed" if dashed else "solid",
                                   roundness={"type": 3} if (round and shape == "rectangle") else None,
                                   boundElements=[{"id": id + "_t", "type": "text"}] if label else None))
        if label:
            self.els.append(self._label(id, label, x + w / 2, y + h / 2, size))
        return self

    def link(self, id, pts, label=None, dashed=False, head="arrow", size=16):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        rel = [[p[0] - pts[0][0], p[1] - pts[0][1]] for p in pts]
        self.els.append(self._base(id=id, type="arrow", x=pts[0][0], y=pts[0][1],
                                   width=max(xs) - min(xs), height=max(ys) - min(ys),
                                   strokeStyle="dashed" if dashed else "solid",
                                   roundness={"type": 2}, points=rel, lastCommittedPoint=None,
                                   startArrowhead=None, endArrowhead=head,
                                   startBinding=None, endBinding=None, elbowed=False,
                                   boundElements=[{"id": id + "_t", "type": "text"}] if label else None))
        if label:
            m = len(pts) // 2
            cx = (pts[m - 1][0] + pts[m][0]) / 2
            cy = (pts[m - 1][1] + pts[m][1]) / 2
            self.els.append(self._label(id, label, cx, cy, size))
        return self

    def note(self, id, s, x, y, size=16, color="#1e1e1e"):
        lines = s.split("\n")
        self.els.append(self._base(id=id, type="text", x=x, y=y,
                                   width=round(max(len(l) for l in lines) * size * 0.62, 1),
                                   height=round(len(lines) * size * 1.25, 1),
                                   strokeColor=color, text=s, originalText=s, fontSize=size,
                                   fontFamily=1, textAlign="left", verticalAlign="top",
                                   containerId=None, lineHeight=1.25, autoResize=True))
        return self

    def save(self, path):
        doc = {"type": "excalidraw", "version": 2, "source": "openclaw/diagram-maker",
               "elements": self.els,
               "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
        open(path, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        return len(self.els)

BLUE, PURPLE, TEAL, AMBER, GREY, RED = "#a5d8ff", "#d0bfff", "#c3fae8", "#ffd8a8", "#e9ecef", "#ffc9c9"
