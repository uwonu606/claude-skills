---
name: drawing
description: draw.io(.drawio) 파일로 구조도·흐름도·구성도·표지·일러스트를 그린다. 사람이 diagrams.net 에서 고칠 그림 파일이 필요할 때 쓴다. 대화 중 이해를 돕는 그림은 map, 데이터 차트는 dataviz 가 맡는다.
---

# 그림 그리기

사용자가 정한 것: 그림은 draw.io(`.drawio`) 파일 하나로 그린다. SVG는 아래 표에서 "SVG 조각"이라고 적힌 기능에만, 그 파일 안의 **SVG 조각**으로 넣는다. draw.io 파일은 사람이 diagrams.net 에서 열어 상자를 옮기고 글자와 색을 고칠 수 있고, SVG 조각은 그 안에서 그림 한 장으로만 다뤄지기 때문이다.

**SVG 조각**은 `shape=image;image=data:image/svg+xml,<SVG를 base64로>` 스타일의 cell 이다. style 이 `;`로 나뉘므로 `data:image/svg+xml;base64,` 꼴은 쓰지 않고 위 꼴로 쓴다.

## 기능 표

diagrams.net viewer 로 렌더해 확인한 것이다.

| 필요한 것 | 하는 법 |
|---|---|
| 상자, 화살표, 아이콘, 겹친 도형, 사람·사물 장면 | draw.io 도형과 라이브러리(`mxgraph.aws4.*` 등). 없는 shape 이름은 오류 없이 빈 네모로 그려지므로, 이름이 있는지 확신하지 못하는 아이콘은 기본 도형을 묶어 짓는다 |
| 반투명, 그러데이션 | draw.io: `opacity`, `gradientColor` |
| 손그림 선 | draw.io: `sketch=1` |
| 빛 번짐(glow) | draw.io: `shadow=1;shadowOffsetX=0;shadowOffsetY=0;shadowBlur=<n>;shadowColor=<색>;shadowOpacity=100` |
| 곡선을 따라 가는 글자 | draw.io: `shape=curvedText;noLabel=1;strokeColor=none;fillColor=none;arcStartY=<n>;arcMidY=<n>;arcEndY=<n>`. 값의 단위는 픽셀이다. 너비 220, 높이 80인 cell 에 `arcStartY=40;arcMidY=-40;arcEndY=40`을 주면 위로 굽은 아치로 그려지고, 0·1 같은 작은 값은 거의 곧게 그려진다. `noLabel=1`이 없으면 곧은 글자가 겹쳐 그려지고, `strokeColor=none;fillColor=none`이 없으면 둘레에 상자가 그려진다 |
| 그림(image cell)을 원·다각형·둥근 사각형으로 자르기 | draw.io: `clipPath=circle(50% at 50% 50%)`, `clipPath=polygon(50% 0%, 100% 100%, 0% 100%)` 처럼 CSS clip-path 값 |
| 자유 곡선 도형 | draw.io: `shape=stencil(<압축>)`. 압축(raw deflate 뒤 base64)한 값만 읽으므로 코드를 돌릴 수 있을 때만 쓴다 |
| image 가 아닌 도형을 다른 도형 모양으로 자르기(clip·mask) | SVG 조각 |
| 색 섞기(blend mode) | SVG 조각 |
| 사진·실사 질감, 붓 자국, 실사 3D 렌더 | 그 부분만 그리지 않고 나머지는 그린다 |

## 1. 그린다

**의도**: 사람이 받은 파일을 diagrams.net 에서 열어 글자를 고치고, 상자를 옮기고, 부분마다 색을 바꿀 수 있다.

- 표에 없는 기능은 draw.io 로 가장 가깝게 그리고, 2단계에서 그 기능과 그린 방식을 알린다.
- 요청에 적힌 글자는 글자 그대로 보이는 cell 의 value 로 넣는다.
- 화살표마다 `source`와 `target`을 상자 cell 에 건다. 좌표만 있는 화살표는 상자를 옮기면 떨어진다.
- 파일은 사용자가 정한 폴더, 정하지 않았으면 현재 폴더에 만든다.

**넘기는 것**: `.drawio` 파일 하나.

**완료 기준**:
- 그림 파일이 `.drawio` 하나이고 mxfile XML 로 읽힌다.
- SVG 조각마다 표에서 "SVG 조각"이라고 적힌 기능(`<clipPath>`·`<mask>`·`mix-blend-mode`)을 쓰는 요소만 담고, 안에 `<text>`가 없다.
- 요청이 그림에 넣으라고 한 이름·제목·라벨마다 보이는 cell 의 value 에 있다.
- 모든 edge 의 `source`·`target`이 보이는 vertex cell 이다.
- 상자에 딸린 아이콘은 상자와 같은 parent 나 group 에 있어 같이 움직인다.
- 요청이 따로 고치겠다고 한 부분마다 cell·layer 가운데 하나로 나뉘어 있다.

## 2. 알린다

**의도**: 사용자가 파일을 어디서 열고, 무엇을 SVG 조각으로 넣었고, 무엇을 그리지 못했고, 무엇은 열어 보지 못했는지 안다.

**넘기는 것**: 파일 경로, SVG 조각마다 그 기능, 표에 없어 가깝게 그린 기능, 그리지 않은 부분, 렌더해서 본 것과 보지 못한 것을 적은 답.

**완료 기준**: 답에 파일 경로가 있다. SVG 조각이 있으면 조각마다 기능이 적혔다. 표에 없는 기능이나 표에서 그리지 않는다고 적힌 기능이 요청에 있으면 그것이 적혔다. 렌더했으면 본 것이, 렌더하지 않았으면 보지 않았다는 것이 적혔다.
