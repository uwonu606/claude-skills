# 뛰어난 사람은 새 기술을 어떻게 익히는가: 과제·가설·피드백·점검 루프의 근거

## 질문과 결론 요약

질문: 뛰어난 사람이 새 기술(언어·프레임워크·도구·개념)을 익힐 때 쓴다는 "과제 주도 → 가설 → 빠른 피드백 → 자기 이해 점검" 루프와, 이를 관통하는 두 원칙(문법보다 개념, 작은 실험과 장난감 구현)은 실제로 근거가 있는가. 각 단계에서 무엇을 하고, 어떤 조건에서 통하고 안 통하는가.

**문법보다 개념(필요성은 확신, 순서는 반반).** 뛰어난 사람은 언어가 암시하는 실행 기계의 모델을 잡고 코드를 추적할 수 있게 한 뒤에 쓴다. 문제는 표면이 아니라 원리로 분류한다. 모델이 없으면 오개념이 생기고 새 맥락으로 옮겨지지 않는다는 근거는 두껍다. "모델을 먼저 가르치는 순서가 낫다"를 조작한 실험은 하나뿐이고 약하다.

**과제 주도(확신, 문턱은 반반).** 설명을 듣기 전에 문제를 붙드는 것은 개념 지식과 전이에서 통하고(메타분석 g=0.36), 절차 지식에서는 통하지 않는다(g=−0.03). 통하는 조건은 설명이 뒤따르고 내가 만든 해법 위에 얹히는 것이다. 얼마나 알아야 문제 먼저가 통하는지의 문턱은 메타분석이 재지 않았다.

**가설과 실험(확신).** 뛰어난 사람은 실험 전에 가설을 여럿 적어 가설을 가르는 실험을 설계한다. 어긋난 결과를 만나면 "내 가설의 증거 찾기"에서 "이 결과를 설명할 가설 찾기"로 목표를 바꾼다. 성패를 가른 것은 아이디어가 아니라 목표였다. 단, 근거는 학부생·아동의 실험실 과제이지 프로그래머가 아니다.

**빠른 피드백(내용은 확신, 빠르기는 반반).** 통하는 피드백은 과제에 붙어 있고 틀린 가설을 짚는다. 정답·상태·이전 시도 대비 변화를 보여 주고, 사람보다 기계가 준다. 자기(칭찬·비교)로 주의를 옮기는 피드백은 셋 중 하나꼴로 해롭다. "빠를수록 좋다"는 주효과는 없고 과제·학습자에 따라 갈린다. 확신하다 틀린 것은 더 잘 고쳐진다.

**자기 이해 점검(확신, 프로그래머 대상은 반반).** 이해했다는 느낌은 믿을 수 없다. 설명을 써 보거나 답을 가리고 꺼내 봐야 안다. 잘하는 학습자는 "모르겠다"를 훨씬 자주 말하고 그 뒤에 설명한다. 프로그래머 대상 실증은 소규모 초보자 연구뿐이며, 점검은 지식이 있을 때만 효과를 냈다.

**장난감 구현(반반).** 실무자 일곱은 서로 다른 이유 여섯을 댄다: 주장의 시험대, 새는 추상화, 내 모델에의 동화, 숨을 곳 없애기, 뺀 것으로 본질 드러내기, 진짜같은 기억. 이론(Papert, ICAP)이 뒷받침하지만 "장난감 구현이 읽기보다 낫다"를 직접 잰 실증은 없다. 다른 절의 기제(설명 착각, 꺼내 보기)와 연결되는 것은 내 추론이다.

**루프 전체.** 근거가 가장 두꺼운 단계는 점검과 과제 주도, 가장 얇은 단계는 장난감 구현이다. 앞선 노트가 못 푼 "먼저 만져 보는 것이 통하는 조건"에는 답이 나왔다(#과제 주도 의 조건 문단). 전문가 프로그래머를 관찰한 실증은 이번에도 없다.

## 앞선 노트와의 관계

`unfamiliar-repo-and-tech.md` 의 "## 처음 보는 기술" 절이 이 주제를 표 두 개로 다뤘고, 기술 쪽 실증이 얇다고 스스로 적었다. 이 노트는 그 절의 후속편이다. 거기서 확인한 출처는 다시 읽지 않고 "앞선 노트 참고"로만 가리킨다(목록은 #조사 방법). 새 출처 40여 개로 각 단계를 파고들고, 앞선 노트가 못 푼 질문에 답한다.

## 조사 방법

**검색과 열람.** 지시받은 출처를 WebSearch 로 찾고, 논문은 PDF 를 받아 텍스트를 뽑아 읽었다. 스캔본은 OCR 로 다시 읽었다. 읽기는 절별로 나눠 진행한 뒤 한 목소리로 정리했다. 본문에서는 "저자 연도"로 가리키고, 서지·URL·호스팅은 #출처 목록 에 있다.

**근거 종류와 확신 기준.** `실증` 은 실험·관찰·메타분석, `이론` 은 모델·틀·연구 종합, `실무자 의견` 은 경험에 바탕한 에세이·강연이다. 메타분석은 "실증(메타분석)"으로 따로 적고 효과 크기를 숫자로 적었다. 확신 정도는 실증 둘 이상이 어긋나지 않으면 확신, 실증 하나거나 이론+실무자면 반반, 실무자 의견뿐이면 감이다.

**앞선 노트의 출처.** Evans, Hermans, Norvig, Luu, Shrestha 2020, Robillard 2011, Chi 1993, How People Learn, Hatano 1986, Land 2005, Sweller 1988, Kahneman & Klein 2009, Keshav 2007, Matuschak 2019, Kerr 2025 는 앞선 노트에서 확인했다. 이 노트에서는 한 줄로만 인용한다.

**빼거나 대체한 것.** 남이 요약한 블로그·위키·슬라이드는 근거로 쓰지 않았다. Sorva 2013 은 유료라 같은 저자의 2012 박사논문 5장으로, Zimmerman 2007 은 저자의 2005 NRC 보고서 초고로, Prather 2018 은 초록과 같은 연구를 담은 저자 박사논문으로 대신했다.

Kapur 2016, Rubin 2013, Butterfield & Metcalfe 2001 은 초록만 확인했다. Schocken 외 2009 논문은 못 열어 책 서문으로 대신했다. 초록만 본 출처는 본문 주장의 근거로 약하게만 썼다.

**목록에 없던 추가 출처.** Butterfield & Metcalfe 2006(2001 데이터 재수록), Metcalfe 2017, Loksa & Ko 2016, Sweller·van Merriënboer·Paas 2019, Evans 2021 "Get better at programming by learning how things work", Klahr·Fay·Dunbar 1993 과 Schauble 1990(초록만)을 더했다.

**호스팅 주의.** Kapur 2008, Loibl 2017, Kalyuga 2003, Ericsson 1993, Klahr & Dunbar 1988, Hattie 2007, Kluger & DeNisi 1996, Dunlosky 2013, Flavell 1979, Feynman 1985, Papert 1980 1장, Hunt & Thomas 2000 은 제3자 미러로 읽었다. 내용은 원문 스캔이라 원 출처로 친다. 표에 "미러"로 표시했다.

**용어.** 메타인지는 자기가 얼마나 이해했는지 스스로 점검하는 능력이다. 전이는 배운 것을 새 상황에 옮겨 쓰는 것이다. 스키마는 머릿속에 굳은 문제 유형별 틀이다. 인지 부하는 작업 기억이 한 번에 감당하는 양이다. 효과 크기(d, g)는 두 집단 차이를 표준편차 단위로 잰 것으로, 0.2 가 작고 0.5 가 중간, 0.8 이 크다고 통상 읽는다.

개념 기계(notional machine)는 프로그래밍 언어가 암시하는 이상화된 실행 기계다. 개념 지식은 "왜·어떻게"를 아는 것, 절차 지식은 "정해진 절차를 수행"하는 것이다. 생산적 실패(productive failure)는 설명 전에 어려운 문제를 풀게 해 실패하게 하는 설계다. 전문성 역전은 초보자에게 좋은 방법이 숙련자에게는 해가 되는 현상이다.

학습 판단(JOL)은 "나중에 기억할 것 같은가"를 스스로 매긴 점수다. 바람직한 어려움은 당장의 수행을 떨어뜨리지만 장기 학습을 올리는 조건(간격, 시험, 교차)이다. 자기 설명은 예제의 각 단계를 스스로 설명하는 행동이다. 대비 사례는 한 특징만 다른 사례들을 나란히 놓은 것이다.

## 문법보다 개념

| 무엇을 하는가 | 안 하면 / 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 언어가 암시하는 실행 기계의 모델을 명시적으로 잡는다. 코드 한 줄이 상태를 어떻게 바꾸는지 추적할 수 있게 한다. | 가르치지 않아도 학습자는 제 나름의 기계 모델을 만든다. 영어·수학과의 표면 유사성에서 추측한 모델은 "a=b+1 을 방정식으로" 같은 오개념을 낳고, 한번 굳은 모델은 고치기가 새로 짓기보다 어렵다. | "안에서 무슨 일이 일어나는지 보여 주려 하지 않아도 학습자는 제 나름의 관점을 만든다. 도움 없이 만든 관점은 빈약하고 우연에 기대며 관찰된 행동의 많은 부분을 설명하지 못한다." 초보자의 문제 대부분은 "숨은, 시각적으로 표시되지 않는" 상태 변화에서 온다. | 실무자 의견·이론. du Boulay 1986(용어의 원출처). 이론(연구 종합). Sorva 2012. |
| 문법 오류와 개념 오류를 가르고 후자에 시간을 쓴다. | 초보자 오류의 최다 빈도는 문법이지만 "사소하고 표면적이며 쉽게 고쳐진다." 개념 모델의 오개념은 "은밀하고 바뀌지 않는다." | 지식을 문법·개념·전략 세 층으로 나누면 오개념은 개념 층의 오류이고, 그 뿌리는 자연어·수학·이전 지식이다. | 이론(연구 종합). Qian & Lehman 2017. |
| 쓰기 전에 읽고 추적한다. 손으로 변수 값을 적으며 코드를 따라간다. | 한 학기 뒤에도 12문제 중 4개 이하를 맞힌 학생이 23% 였다(556명). 추적을 종이에 쓴 학생은 75~77% 맞혔고 아무것도 안 쓴 학생은 50% 였다(56명 분석). | "많은 학생이 문제 풀이의 선행 조건인 지식과 기술이 없다. 빠진 것은 코드를 쓰는 능력보다 읽는 능력에 관련된다." 초보자는 추적할 때 작업 기억에 지나치게 기댄다. 쓰기 능력은 측정하지 않았다. | 실증. Lister 외 2004(7개국 941명). |
| 의미론 읽기(추적) → 문법 쓰기 → 템플릿 읽기 → 템플릿 쓰기 순서로 익힌다. | 코드 작성부터 시작한 집단은 추적 문항에서 뒤졌다. | "추적은 문법적으로 맞는 코드를 쓰는 것과 다른, 선행하는 기술이다." 의미론을 먼저 가르친 집단의 학습 이득이 60% 높았고(27점 중 3.89 vs 2.42) 그 이득만 중간고사를 예측했다(R²=.64). 조건 간 차이는 p<.05 에 못 미쳤다(사후 시험 d=.59, p<.12; 학습 이득 d=.40, p<.41). 37명·4시간이었다. | 실증(약함). Nelson·Xie·Ko 2017. 이론. Xie 외 2019(평가는 9명, 통계 검정 없음). |
| 표면(키워드·문법·대상)이 아니라 원리로 문제를 분류한다. | 초보자는 "스프링, 경사면" 같은 표면 특징으로 묶는다. | 전문가 8명은 "문제 풀이를 지배하는 물리 원리"로 24문제를 묶었고 초보자 8명은 표면 구조로 묶었다. 범주 개수는 같았다(8.4 vs 8.6). 발전한 초보자는 표면에 매인 채 원리로 옮겨 가기 시작했다. | 실증. Chi·Feltovich·Glaser 1981(앞선 노트의 1993 회고를 원문으로 확인). |
| 개념 기계를 "주의의 교육" 장치로 쓴다: 어떤 변수에 주목하고 무엇을 무시할지 배운다. | 학습자의 mental model 과 교사의 pedagogic device 를 섞어 쓴다. | 43개 개념 기계를 수집했지만 "효과를 검증한 연구는 드물고" 서로 비교한 연구는 더 드물다. 용어를 쓴 논문 중 정의한 것은 절반 미만(116편). | 이론(연구 종합·목록). Fincher 외 2020. |

**해석:** 출처는 셋이 "개념 기계"를 다르게 정의한다. du Boulay 와 Sorva 에게는 실행기의 추상이지 학습자의 mental model 이 아니고, Fincher 2020 에게는 교사의 교육 장치이며, Qian & Lehman 에게는 언어 독립적 mental model 이다. 서로 동의한다고 인용하면 안 된다.

"모델 먼저"를 받치는 것은 오개념의 원인 분석(이론)과 추적 능력 결손(실증)이다. 순서 자체를 조작한 실험은 Nelson 2017 하나이고 저자도 "약간의 증거"라 부른다. 내 해석으로는 "먼저"의 근거보다 "없으면 안 된다"의 근거가 두껍다. Chi 1981 은 물리학이라 프로그래밍과는 유비로만 이어진다.

**조건:** 모델 없이도 정형 연습 문제는 풀린다. du Boulay 는 성냥갑 컴퓨터 같은 모델 교육이 "새 문제에서는 효과가 컸지만 정형 연습에서는 차이가 없었다"고 하고, Sorva 는 모델이 필요해지는 때를 "템플릿이 없는 새 맥락으로 옮길 때"로 잡는다. 익숙한 패턴만 쓰는 과제라면 문법 먼저도 굴러간다.

## 과제 주도

| 무엇을 하는가 | 안 하면 / 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 설명을 듣기 전에 문제를 먼저 붙든다. 단, 설명이 뒤따르고 그 설명이 내가 만든 해법 위에 얹힐 때. | 설명 먼저는 절차 지식에서 같거나 낫고, 개념·전이에서 뒤진다. | 53개 연구 166개 비교. 문제 먼저가 개념 지식·전이에서 g=0.36 [0.20, 0.51]. 절차 지식은 g=−0.03. 설명이 학생 해법 위에 얹히면 0.56, 아니면 0.20. 집단 활동 0.49 vs 0.19. 여러 해법을 만든 증거가 있으면 0.47 vs 0.16. 대화형 설명 0.55 vs 독백 0.24. | 실증(메타분석). Sinha & Kapur 2021. |
| 문제 먼저는 대비 사례로 하거나, 뒤이은 설명이 내 해법을 다루게 한다. 둘 다 없으면 예제 먼저. | 두 요소 없이 문제만 먼저 풀면 "worked example 문헌과 같은 결론(설명 먼저가 낫다)"이 난다. | "문제 먼저는 대비 사례가 주어지거나 학생 해법 위에 설명이 쌓일 때만 학습을 돕는다." 기제는 연쇄다: 사전 지식 활성화 → 지식 공백 자각 → 심층 특징 인식. "실패를 자각하지 못하면 실패는 효과가 없다." | 이론(연구 종합). Loibl·Roll·Rummel 2017. |
| 탐색만으로 끝내지 않는다. 탐색 뒤에 강의·교재를 받는다. | 분석만 두 번 한 집단(16.7%)과 요약+강의(14.6%)는 분석+강의(43.8%)의 절반도 못 예측했다(36명). | "대비 사례의 차이를 알아차리는 것이 '말해 줄 때'를 만든다." "발견도 설명도 그 자체로는 깊은 이해에 충분하지 않았다. 초보자에게는 둘 다 필요했다." | 실증. Schwartz & Bransford 1998. |
| 틀리더라도 방법을 발명해 본다. 그 뒤에 자원(예제·강의)에서 배운다. | 발명 없이 배운 집단은 자원이 있어도 못 배웠고, 발명 집단은 자원이 없으면 발명 안 한 집단과 같았다. | "규범적으로는 틀린 산출물을 만드는 것이 그 자체로는 비효율적으로 보이지만 자원을 만날 때 나중에 갚는다." 준비 효과는 주제 특정적이었다. 자원은 worked example 이었다. | 실증. Schwartz & Martin 2004(9학년, 95명·102명). |
| 지원 없이 어려운 문제를 풀어 실패해 본다. | 지원받은 집단은 해답 품질이 높았지만(2.18 vs 1.42) 이후 개인 시험에서 뒤졌다. | 어려운 문제 뒤의 쉬운 문제라는 대비가 구조를 식별하게 한다. "좌절 역치와 몰입이 낮으면 생산적 실패가 안 된다." 두 조건 모두 설명 단계가 없어 순서 비교가 아니다. | 실증. Kapur 2008(11학년 309명, 인도). |
| 초보자일 때는 예제로, 스키마가 생기면 문제로. 예제는 서서히 걷는다. | 스키마 있는 학습자에게 예제는 "중복"이 되어 부담이 된다. | "초보자에게 효과적인 기법이 경험 있는 학습자에게는 효과를 잃거나 해가 된다." 낯선 문제의 수단-목적 탐색은 작업 기억을 잡아먹고 스키마 구성과 무관하다. 얼마나 알아야 뒤집히는지 숫자는 없다. | 이론(자기 실험 종합). Kalyuga·Ayres·Chandler·Sweller 2003(앞선 노트의 Hermans 인용을 원문으로 확인). |
| 지금 못 하는 것을 겨냥해 설계된 과제를, 즉각 피드백과 전적인 집중으로 반복한다. | "단순 반복은 특히 정확도를 자동으로 올리지 않는다." | 최고 바이올리니스트는 18세까지 혼자 연습 7,410시간, 좋은 연주자 5,301시간, 교사 지망 3,420시간. 의도적 연습은 "약점을 극복하기 위해 발명된 특정 과제"이며 "노력이 들고 본질적으로 즐겁지 않다." 교사가 "더 어려운 과제로 넘어갈 때"를 판단한다. | 실증·이론. Ericsson·Krampe·Tesch-Römer 1993. |

**해석:** 생산적 실패 진영과 인지 부하 진영은 세 가지에서 실제로 같은 말을 한다. 절차 숙련은 문제 먼저로 안 는다. 탐색 뒤에 설명·예제가 반드시 온다. 어린 학습자, 관련 사전 지식이 없는 학습자, 대비 사례도 해법 기반 설명도 없는 설계에서는 설명 먼저가 낫다.

실제로 갈리는 것은 "첫 단계의 문제 풀이가 무엇인가"다. 인지 부하 진영은 절차 문제의 수단-목적 탐색을 보고 절차 수행을 잰다. 생산적 실패 진영은 개념 발명을 보고 개념·전이를 잰다. 과제도 측정도 달라서, 겉보기 모순의 상당 부분은 내 해석으로는 과제와 측정의 불일치다.

Ericsson 1993 은 이 논쟁의 당사자가 아니다. 의도적 연습은 교사가 방법을 명시적으로 지시하고 과제를 설계하는 것을 전제하므로, 굳이 자리를 매기면 안내 쪽에 가깝다(반반). "현재 수준 바로 위 난이도"라는 흔한 정리는 1993 원문에 그 표현으로 없다.

**조건:** 이것이 앞선 노트가 못 푼 질문의 답이다. 먼저 만져 보는 것이 통하는 조건은 넷이다. 목표가 개념·전이다. 활성화할 사전 지식이 있어 특정한 방식으로 틀릴 수 있다. 설명이 뒤따르고 내 해법을 다룬다. 실패를 알아차릴 수 있다(Loibl 2017, Sinha & Kapur 2021, Schwartz 1998·2004).

안 통하는 조건도 넷이다. 절차 숙련이 목표다(g=−0.03). 초등 저학년(−0.09)이거나 영역 일반 기술(−0.17)이다. 설명 없이 탐색만 한다(Schwartz 1998 의 16.7%). 교재 복잡도가 높다(Sinha & Kapur 가 Ashman 2020 을 들어 경계 조건으로 꼽음).

"얼마나 알아야 하는가"의 문턱은 남는다. 메타분석은 학습자의 사전 지식 수준과 대조군의 worked example 사용 여부를 조절 변인으로 코딩하지 않았다. Loibl 은 "학생이 어느 정도 사전 지식과 아이디어를 가진 문제"를 전제로 둔다. Kalyuga 는 역전 지점의 숫자를 주지 않는다. 문턱은 반반이다.

## 가설과 실험

| 무엇을 하는가 | 안 하면 / 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 실험 전에 가능한 가설을 여럿 적는다. 그래야 가설을 가르는 실험을 설계한다. | 가설을 하나씩 검증하면 버리는 데 오래 걸리고, 정보가 많은 실험을 늦게 한다. "가설 사이를 구분하는 실험을 한 사람은 없었다." | 가설을 먼저 나열하게 한 10명은 전원이 평균 5.7회 실험으로 풀었다. 그냥 시작한 20명은 평균 15.2회. "여러 가설이 결과를 설명할 수 있음을 알았기 때문에 변별 실험을 했다." | 실증. Klahr & Dunbar 1988(BigTrak 로봇의 RPT 키, CMU 학부생). |
| 첫 가설이 죽으면 두 길 중 하나를 간다. 기억에서 새 틀을 짓거나(이론가), 가설 없이 변수를 바꿔 데이터를 모아 규칙을 귀납한다(실험가). | 반증된 가설을 붙든다. 반증 136건 중 76건에서 가설을 유지했다. 11번 결과 중 4번은 죽은 가설이 살아 있었다. | 이론가 7명은 11.4분·9.3회, 실험가 13명은 24.5분·18.3회. 실험가는 가설 없는 실험을 평균 6회 한 뒤 규칙을 찾았다. 이론가 전원과 실험가 1명만 프로그래밍 경험이 있었다. 갈림은 기술이 아니라 사전 지식이다. | 실증. Klahr & Dunbar 1988. |
| 어긋난 결과를 만나면 목표를 "내 가설에 맞는 증거 찾기"에서 "이 결과를 설명할 가설 찾기"로 바꾼다. | 전원이 어긋남을 알아차렸지만, "출력 0 을 찾겠다"는 목표를 유지한 13명은 전원이 증거를 왜곡했고 아무도 못 풀었다. | "큰 출력의 원인을 찾겠다"는 목표를 세운 사람은 성공 집단 7명 중 6명, 실패 집단 13명 중 1명. 원래 목표를 먼저 채워 준 2차 실험에서 정답이 20명 중 4명에서 14명으로. "아이디어 부족이었다면 이 조작이 효과가 없었을 것"이므로 원인은 목표 봉쇄다. | 실증. Dunbar 1993(McGill 학부생 40명, 유전자 억제 발견 과제). |
| 변수를 하나씩 통제하고, 기록을 남기고, 왜 그 전략이 통하는지 안다. | 좋은 결과가 나오면 원인으로 믿는 변수를 고정한 채 나머지만 바꾼다(54%). 이전 인과 믿음에 어긋나는 증거를 왜곡한다. "효과를 내는" 공학 목표로 실험한다. | 성공한 학생은 안정화 전 "진짜 실험"을 60~100% 했고 실패한 학생은 9~45%. "기록의 필요를 아는 것이 10~13세에 나타나며 성공과 직결됐다." 성공하는 사람은 "증거와 이론이 서로를 제약해야 함"을 안다. | 이론(연구 종합). Zimmerman 2005(2007 논문의 저자 초고). 실증(초록만). Schauble 1990, Klahr·Fay·Dunbar 1993. |

**해석:** 긍정 검증(내 가설이 맞으면 이렇게 될 것이다)은 거의 전원이 했지만 병목이 아니었다. 결과의 약 60% 가 어차피 반증이었기 때문이다. 갈린 것은 반증 뒤에 무엇을 하느냐다. 이론가와 실험가 중 어느 쪽이 "낫다"는 말은 원문에 없다. 어느 길이 열리는지를 사전 지식이 정한다.

프로그래머에게 옮기면(내 추론) 셋이다. 돌려 보기 전에 가능한 동작을 여럿 적는다. 그것들을 가르는 입력으로 돌린다. 막히면 약한 검증을 되풀이하지 말고 데이터 수집 모드로 전환한다. 근거는 장난감 로봇과 모의 유전학이라 방향만 옮길 수 있고 크기는 못 옮긴다.

**조건:** 이론가의 길은 관련 지식이 기억에 있을 때만 열린다. 없으면 실험가의 길뿐이고, 그 길은 두 배 걸리지만 결국 도달한다. Dunbar 의 2차 실험은 원래 목표를 채울 수 있는 환경이 있어야 목표 전환이 쉬워짐을 보인다. 기본으로 배운 모델(활성화)이 바로 증거를 왜곡하며 붙드는 모델이었다.

## 빠른 피드백

| 무엇을 하는가 | 안 하면 / 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 피드백이 과제에 붙어 있게 한다. 정답·바른 상태와 이전 시도 대비 변화를 보여 주고, 사람보다 기계가 준다. | 피드백 607개 효과 중 38% 가 성과를 떨어뜨렸다. 칭찬(.09), 낙담시키기(−.14), 자존감 위협(.08), 규범 비교가 주의를 과제에서 자기로 옮긴다. | 평균 d=0.41(23,663 관측). 정답 제공 .43 vs .25, 이전 시도 대비 변화 .55 vs .28, 컴퓨터 제공 .41 vs .23. "학습을 돕는 결정적 측면은 틀린 가설을 가리키는 능력이다." 복잡한 과제에서는 효과가 거의 없다(.03 vs .55). | 실증(메타분석)·이론. Kluger & DeNisi 1996. |
| 세 질문에 답하는 피드백을 찾는다: 어디로 가는가, 어떻게 가고 있는가, 다음은 무엇인가. 과제 → 처리 → 자기 조절 수준으로 옮긴다. | 자기(칭찬) 수준 피드백은 "학습 관련 정보가 거의 없어" 효과가 없다(d=0.14). | 12개 메타분석 196개 연구 6,972개 효과 크기의 평균 d=0.79. "잘못된 해석을 다룰 때 가장 강력하고, 이해가 아예 없을 때는 아니다. 낯선 자료라면 새 정보를 아는 것에 연결할 길이 없다." | 이론(메타분석 종합). Hattie & Timperley 2007. |
| 맞았는지만이 아니라 왜를 얻는다. 몰두하고 있을 때는 피드백으로 끊지 않는다. | "정답 여부 정보만으로는 학습에 큰 효용이 없다." "정답을 주지 않으면 사실상 아무 이득이 없다." | 형성 피드백의 요건은 확인+정교화. 지침: "과제에 초점을, 학습자에게가 아니라", "규범 비교를 하지 말라", "칭찬은 아끼라", "몰두한 학습자를 끊지 말라". | 이론(연구 종합). Shute 2008. 이론. Metcalfe 2017. |
| 빠르기는 과제에 맞춘다. 어려운 과제·절차 기술(프로그래밍 포함)·초보자·유지에는 즉시, 전이·쉬운 과제·상급자에게는 지연. | "빠를수록 좋다"는 주효과가 없다. 즉시 피드백은 "전이 때 없을 정보에 기대게 하고 덜 신중한 행동을 부추길 수 있다." | 53개 연구 메타: 시험 상황에서는 지연이 낫고(0.36) 수업 처리 상황에서는 즉시가 낫다(0.28). 지연 피드백의 효과는 쉬운 문항 −0.06, 중간 0.35, 어려운 문항 1.17. 프로그래밍 튜터에서 즉시 피드백+즉시 교정이 가장 빨랐고 시험 점수는 같았다. | 이론(연구 종합). Hattie & Timperley 2007(Kulik & Kulik 1988, Clariana 2000 인용). Shute 2008(Corbett & Anderson 2001 인용). |
| 확신하다 틀린 순간을 붙들고 그때 정답을 확인한다. | 확신이 낮은 오류는 덜 고쳐진다. | 첫 시험에서 틀린 답의 재시험 정답률: 낮은 확신 .61, 중간 .81, 높은 확신 .87. 기제는 놀람에 의한 주의 포착이다. 높은 확신 오류의 피드백 동안 동시 과제(음 탐지) 수행이 떨어졌다. 재시험이 늦어도 유지된다. | 실증. Butterfield & Metcalfe 2001(초록)·2006(2001 데이터 재수록, 실험 2개). 이론. Metcalfe 2017. 사실 문답 과제이지 디버깅이 아니다. |
| 프로그램의 상태와 흐름을 보이게 한다. 즉시 갱신은 전제일 뿐 목적이 아니다. | 코드 왼쪽·출력 오른쪽만 있는 라이브 코딩은 "재료 더미를 보여 주고 곧바로 수플레를 보여 주는 요리 프로그램"이다. | "프로그래머가 프로그램이 무엇을 하는지 볼 수 없으면 이해할 수 없다." "즉시 갱신은 흥미로운 무언가를 하기 위한 전제일 뿐이다. 프레임 속도를 올린다고 게임이 좋아지지 않는다." | 실무자 의견. Victor 2012. |

**해석:** 컴파일러와 테스트는 기계가 주고, 규범 비교가 없고, 과제에 붙어 있고, 대개 바른 상태를 보여 준다. Kluger & DeNisi 의 "돕는" 칸에 정확히 들어간다(내 추론). 하지만 빨간 테스트 하나는 확인만 있는 피드백이라 Shute 와 Metcalfe 가 낮게 매기는 종류다. Victor 의 주장은 그 빈자리(왜, 상태)를 채우라는 것으로 읽힌다.

Metcalfe 2017 은 즉시성을 주의의 대리 변수로 다시 읽는다. 실험실에서는 지연이, 교실에서는 즉시가 나았는데 차이는 "학습자가 피드백에 주의를 기울였는가"였다. 유일한 프로그래밍 교실 실험인 Rubin 2013 은 초록만 확인해 결과를 쓰지 못했다.

**조건:** "돌려서 깨지는 걸 보고 고친다"는 통념은 초보자·절차 기술·어려운 과제·과제 수준에서 지지된다. 세 가지로 제한된다. 상태와 이유가 함께 보여야 한다. 생각을 앞질러 오는 피드백은 의존을 낳고 전이를 해칠 수 있다. 틀릴 모델이 아예 없거나 과제가 너무 복잡하면 효과가 무너진다.

## 자기 이해 점검

| 무엇을 하는가 | 안 하면 / 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 예제의 각 단계를 원리에 연결해 스스로 설명한다. "모르겠다"를 자주 말하고 그 뒤에 설명한다. | 못하는 학생은 감시 발화의 85% 가 "이해했다"였고 "모르겠다"는 예제당 1.1회. 문제를 풀 때 예제로 돌아가 13줄씩 다시 읽었다(잘하는 학생은 1.6줄). | 잘하는 4명은 예제당 물리 설명 15.3개, 못하는 4명은 2.8개. 이해 실패 발화 9.3 vs 1.1. 설명 수와 문제 성공의 상관 r=.81. "못하는 학생은 자기가 이해하지 못한다는 사실을 모르는 듯하다." 사후 분류, 8명, 상관. | 실증. Chi·Bassok·Lewis·Reimann·Glaser 1989. |
| 이해했다는 느낌을 믿지 않고 설명을 써 본다. | 지퍼·변기 같은 장치의 작동을 7점으로 자평한 뒤 설명을 쓰게 하면 약 0.9점 떨어진다(97명). 사실·절차·이야기에서는 안 떨어진다. 경고를 줘도 안 사라진다. 독립 평가자는 설명 후 자평에 동의했다. | 설명 지식은 "끝 상태가 정해져 있지 않아 자기 시험이 어렵고", "설명을 만들 일이 드물어 과거 성패 정보가 적다." 보이는 기제를 내부 표상으로 착각하는 것이 가장 큰 요인이다. | 실증. Rozenblit & Keil 2002. |
| 답이 눈앞에 있을 때의 판단을 믿지 않는다. 답을 가리고 꺼내 본다. | 정방향 단어쌍(예측 78.1, 회상 78.8)은 정확했지만, 같이 보면 뻔하고 따로 보면 안 떠오르는 역방향 쌍은 75.7 로 예측하고 60.3 을 회상했다. | "예측하려면 시험 보는 사람의 관점을 취해야 하는데, 지금 아는 것을 떼어 놓아야 한다." 예측 50% 이상에 실제 회상 20% 미만인 경우도 있다. | 실증. Koriat & Bjork 2005. |
| 다시 읽는 대신 꺼내 본다. | 5분 뒤에는 다시 읽기가 낫지만(81% vs 75%) 2일 뒤 68 vs 54, 1주 뒤 56 vs 42 로 역전. 네 번 읽은 집단은 14.2회 읽고 40%, 한 번 읽고 세 번 시험한 집단은 3.4회 읽고 61%. 네 번 읽은 집단이 가장 자신 있었고 가장 못했다. | "시험은 학습을 재는 것만이 아니라 학습을 개선하는 강력한 수단이다." 학생은 단기 이득을 낳는 전략을 고른다. | 실증. Roediger & Karpicke 2006(120명·180명, 산문 회상). |
| 유창함을 학습으로 착각하지 않는다. 답을 안 보고 자기 시험을 끝까지 한 뒤에야 안다고 여긴다. | 76% 가 다시 읽는다. 검색 연습을 스스로 꼽은 학생은 11%. 자기 시험을 쓰는 이유의 70% 는 "얼마나 배웠나 알려고"이지 배우려고가 아니다. 간격 연습이 90% 에게 나았지만 72% 는 몰아서가 낫다고 믿었다. | "현재 수행과 유창함의 주관적 감각은 최근성·예측 가능성·학습 때만 있는 단서에 좌우된다." "가장 좋은 답은 단순하다. 답을 확인하지 않고 의미 있는 자기 시험을 끝까지 해 보라." | 이론(연구 종합). Bjork·Dunlosky·Kornell 2013. |
| 효용이 확인된 기법을 고른다. 연습 시험·간격 연습(높음), 자기 설명·교차 연습·정교화 질문(중간), 다시 읽기·밑줄·요약(낮음). | 학생 대부분이 다시 읽기와 밑줄을 쓴다. | 자기 설명이 중간인 이유: 근전이는 "거의 모든 연구"에서 확인됐지만 지연 후 유지는 다섯 연구뿐, 교실 검증 부족, 학습자 수준별 효과 미확인, 시간이 30~100% 더 든다(125분 vs 66분). 약한 학생은 설명 대신 바꿔 말하기를 한다. | 이론(근거 평가). Dunlosky 외 2013. |
| 프로그래밍 문제 풀이의 여섯 단계(문제 재해석, 유사 문제 탐색, 해법 탐색, 해법 평가, 구현, 구현 평가) 중 지금 어디인지 안다. | 초보자는 "대개 문제의 시작에서 막혀" 도움을 받아야 나아갔다. 1단계에서 틀린 개념 모델을 만들고 못 떨쳐낸다. 컴파일·테스트 통과가 "거의 다 됐다"는 거짓 위치 감각을 준다. | 여섯 단계를 가르치고 도움 요청 때 "어느 단계냐"를 물은 실험군 25명은 전략을 더 서술했고(p=.032), 자발 과제를 44% vs 17% 로 더 했고, 자기 효능감 변화의 효과 크기 0.71. 지정 과제 완료량은 같았다. 개입 4개가 묶여 있고 오전·오후 배정이 교란한다. | 실증. Loksa 외 2016(고등학생 48명, 2주). 실증(박사논문으로 확인). Prather 외 2018(31명 think-aloud, 다섯 어려움: Forming, Dislodging, Assumption, Location, Achievement). |
| 지식이 있어야 점검이 효과를 낸다는 것을 안다. | CS1 에서는 자기 조절 발화가 오류와 무관했다. CS2 에서만 이해 감시 1회당 오류 약 3개 감소, 계획 1회당 약 1개 감소. 자기 설명은 오류 약 1개 증가. | "자기 조절은 문제를 풀기에 충분한 지식이 함께 있을 때만 효과가 있다." "훈련된 자기 조절 기술이 있어도 지식이 없으면 지치고 좌절하게만 한다." 207편 리뷰: "인지 통제와 성과의 직접 연결은 약하고" 자기 효능감을 거친다. 자기 보고 척도는 "하는 것이 아니라 한다고 생각하는 것"을 잰다. | 실증. Loksa & Ko 2016(37명, CS2 는 16명, 상관). 이론(연구 종합). Prather 외 2020. 이론. Flavell 1979. |

**해석:** Flavell 1979 가 이름 붙인 "방금 들은 것을 이해하지 못한다는 갑작스러운 느낌"(메타인지 경험)이 전략을 바꾸는 방아쇠다. Chi 1989 의 "모르겠다" 발화가 바로 그것이고, 잘하는 학생은 그 뒤 85% 를 설명으로 이었다. 못하는 학생은 느낌 자체가 드물었다.

Loksa & Ko 2016 에서 자기 설명이 오류 증가와 상관한 것은 저자 해석으로 "막힐 때 더 말한다"이지 자기 설명이 해롭다는 뜻이 아니다. 16명 하위 모델의 계수라 수치는 약하다. Rozenblit & Keil 이 꼽은 착각의 두 원인, "만들 일이 드물다"와 "끝 상태가 없다"를 장난감 구현이 채운다는 것은 내 추론이지 검증된 것이 아니다.

**조건:** 점검은 지식 위에서만 통한다. Loksa & Ko 는 CS1 에서 무관·CS2 에서 유관을, Prather 2020 은 "내용 지식이 적은 영역에서는 메타인지 지식이 어렵다"를 말한다. 설명 착각은 "기제가 눈에 보이는" 장치에서 가장 크다. 겉으로 동작이 보이는 프레임워크에서 착각이 클 것이라는 것은 내 추론이다.

## 장난감 구현

| 무엇을 하는가 | 안 하면 / 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 남이 설명하는 동안 조건에 맞는 구체적 예를 머릿속에 짓고, 결론을 그 예에 대 본다. | 어휘를 모르면 판단을 못 한다고 여긴다. | "나는 계속 예를 만든다. … 결국 정리를 말하면 내 털 난 초록 공에는 안 맞는 헛소리라서 '거짓!'이라고 한다." "Hausdorff homomorphic 이 뭔지 몰라도 어느 쪽인지 안다." 단서: "정리가 보기만큼 어렵지 않았기 때문"이다. | 실무자 의견. Feynman 1985(미러). 칠판의 "What I cannot create, I do not understand" 는 Caltech 아카이브 사진으로 확인, 옆에 "TO LEARN:" 목록이 있다. |
| 추상화가 새는 곳을 손으로 구현한다. | "프레임워크가 자동으로 해 주는데 왜 역전파를 손으로 쓰냐"고 묻는다. | "역전파는 새는 추상화다. 층을 아무렇게나 쌓으면 마법처럼 된다고 믿는 함정에 빠지기 쉽다." 손으로 짜 본 사람은 시그모이드 포화·죽은 ReLU·RNN 기울기 폭발에서 "불안해진다." 시간이 나면 하는 "보너스"로 두고, "지적 호기심"이라는 이유는 약하다고 물리친다. | 실무자 의견. Karpathy 2016. |
| 외부 도구 없이 전부 손으로 쓴다. 매 줄을 넣을 자리까지 명시한다. | "마법과 혼란이 숨을 어두운 구석"이 남는다. | "해시 테이블을 매일 쓰지만 정말 이해하는가? 처음부터 만들고 나면 이해할 것이라 장담한다." "직접 만들어 보니 마법은 전혀 없었다. 그냥 코드였다." | 실무자 의견. Nystrom 2021. |
| NAND 게이트부터 컴퓨터를 만든다. 각 층을 추상(무엇)으로 정한 뒤 아래 층으로 구현(어떻게)한다. | "컴퓨터 안에서 무슨 일이 일어나는지 완전히는 모른다는 불편한 느낌"이 남는다. | "컴퓨터가 어떻게 작동하는지 이해하는 가장 좋은 방법은 처음부터 하나 만드는 것이라 믿는다." "만드는 데 시간을 들이는 독자는 읽기만으로는 얻을 수 없는 친밀한 이해를 얻는다." 큰 교훈은 "이 활동의 부수 효과로" 얻는다. | 실무자 의견. Nisan & Schocken 2005 서문·서론(저자 사이트 웨이백). |
| 일부러 작게 만들고 뺀 것을 적는다. 117줄 Lisp 해석기, 반 쪽짜리 맞춤법 교정기. | 산업용 구현은 "꽤 복잡하다." | 목적은 "가능한 한 간결하고 단순하게 본질을 보이는 것." 빠진 것 목록: call/cc, 꼬리 재귀, 100개 넘는 기본 함수, 오류 처리("Lispy 는 프로그래머가 완벽하길 기대한다"). 뛰어난 엔지니어 두 사람도 전공 밖의 기제에는 직관이 없었다. | 실무자 의견. Norvig(lispy, spell-correct). |
| 혼란을 사실 질문으로 쪼개고, 답을 찾은 뒤, 프로그램을 써서 이해를 시험한다. | 틀린 모델은 "명백하게 드러나지 않는다." 버그가 나고, 빨리 못 고치고, 물을 질문을 못 찾는다. | "'이해 시험' 단계가 정말 중요하다. 새 기능이나 버그 수정이나 그저 작동을 보여 주는 시험 프로그램을 쓰면 읽기만 한 것보다 훨씬 진짜같이 느껴지고 나중에 쓸 가능성이 훨씬 커진다." 한계: "모든 시스템을 다 이해하라는 건 무리다. 그래서 추상화가 있다." | 실무자 의견. Evans 2021(목록에 없던 추가 출처). |
| 새 분야 논문을 여러 번 훑으며 쉬운 사실부터 기억 카드로 만들고, 고아 질문을 피한다. | 처음부터 정독하면 배경이 없어 어렵다. | 대여섯 번 훑으니 "쉽게 이해되는 범위가 계속 넓어졌다." 카드를 만드는 행위 자체가 정교화 부호화다. 얻은 것은 "기초적 이해"이지 "직접 시스템을 만들 능력"은 아니었다. | 실무자 의견. Nielsen 2018. |
| 만드는 것을 지식 구축의 조건으로 본다. 기어 같은 "생각할 물건"이 추상을 머리에 들여온다. | "무엇이 이 활동을 학습이 풍부하게 만드는지 아무도 완전히는 모른다." | "무엇이든 내 모델 모음에 동화시킬 수 있으면 쉽고, 못 하면 고통스럽게 어렵다." 구성주의는 "학습자가 공개된 실체를 의식적으로 만드는 맥락에서 지식 구축이 특히 잘 일어난다"는 주장이다. 약한 주장(일부에게 맞다)과 강한 주장(모두에게 낫다)을 구분한다. | 이론. Papert 1980(미러), Papert & Harel 1991(저자 사이트). |
| 주어진 것을 넘어서는 산출물을 만든다. 베끼면 '능동'에 그친다. 설명하려면 당연히 여기던 것을 명시해야 한다. | 베낀 다이어그램, 지우고-옮기기 요약은 능동 수준으로 떨어진다. | "구성적 행동은 학습 자료에 주어진 것을 넘어서는 외부 산출물을 만드는 것." 수동<능동<구성<상호작용의 수준마다 약 8~10% 향상. "외부화 과정은 자기가 정말 아는지 감시할 기회를 준다." 프로그램 작성은 언급이 없다. | 이론. Chi & Wylie 2014. 실무자 의견. Hunt & Thomas 2000(고무 오리, 미러). |

**해석:** "장난감 구현이 읽기보다 낫다"를 직접 잰 실증은 없다. 실무자들이 대는 이유는 여섯이고 서로 다르다. 주장의 시험대(Feynman), 새는 추상화(Karpathy, Evans), 내 모델에의 동화(Papert), 숨을 곳 없애기(Nystrom, Nisan & Schocken, Hunt & Thomas), 뺀 것으로 본질 드러내기(Norvig), 진짜같은 기억(Evans, Nielsen).

이 이유들이 다른 절의 실증 기제와 맞물린다는 것은 내 추론이다. 설명을 만들면 착각이 드러나고(Rozenblit & Keil), 꺼내 보기가 다시 읽기를 이기며(Roediger), 주어진 것을 넘는 산출물이 베끼기를 이기고(Chi & Wylie), 확신하다 틀리면 더 잘 고쳐진다(Butterfield & Metcalfe). ICAP 에서 제 이해로 쓴 장난감은 구성, 베낀 코드는 능동이다.

**조건:** 저자들 스스로 한계를 단다. Feynman 은 정리가 보기만큼 어렵지 않아서 통했다고 한다. Karpathy 는 시간이 날 때의 보너스라 한다. Evans 는 진단 안 되는 버그가 방아쇠이고 모든 것을 이해할 필요는 없다고 한다. Nielsen 은 기초 이해까지라 한다. Papert 는 기어 경험을 모두에게 만들어 줄 수 없다고 한다.

장난감 구현은 "문제 먼저"의 한 형태이므로 #과제 주도 의 조건이 그대로 붙는다는 것이 내 추론이다. 사전 지식이 없는 초보자가 처음부터 짓는 것은 Kalyuga 가 말하는 수단-목적 탐색이 되기 쉽고, 뒤에 설명(원전, 참고 구현)이 따라야 한다.

## 루프 전체

| 단계 | 뛰어난 사람은 | 가장 강한 근거 | 근거 강도 |
|---|---|---|---|
| 문법보다 개념 | 실행 기계의 모델을 잡고 추적할 수 있게 한 뒤 쓴다. 표면이 아니라 원리로 분류한다. | Lister 2004(추적 결손), Chi 1981(원리 분류) | 필요성은 확신, 순서는 반반(Nelson 2017 하나) |
| 과제 주도 | 설명 전에 문제를 붙들되, 설명이 뒤따르고 내 해법을 다루게 한다. 절차 숙련은 예제로. | Sinha & Kapur 2021 메타(g=0.36, 절차 −0.03), Schwartz 1998·2004 | 확신, 사전 지식 문턱은 반반 |
| 가설과 실험 | 가설을 여럿 적고 가르는 실험을 한다. 어긋난 결과를 설명하는 것을 목표로 삼는다. | Klahr & Dunbar 1988, Dunbar 1993 | 확신, 단 프로그래머 대상이 아님 |
| 빠른 피드백 | 과제에 붙은, 정답·상태·변화를 보이는 피드백을 기계에서 받는다. 확신하다 틀린 순간을 붙든다. | Kluger & DeNisi 1996 메타(d=0.41, 38% 해로움), Butterfield & Metcalfe 2001·2006 | 내용은 확신, 빠르기는 반반 |
| 자기 이해 점검 | 이해했다는 느낌을 믿지 않고 설명·꺼내 보기로 확인한다. "모르겠다"를 자주 말한다. | Chi 1989, Rozenblit & Keil 2002, Roediger & Karpicke 2006 | 확신, 프로그래머 대상은 반반(Loksa, Prather) |
| 장난감 구현 | 작게 만들고 뺀 것을 적는다. 추상화가 새는 곳을 손으로 짠다. | 실무자 7명 + Papert, Chi & Wylie | 반반(직접 실증 없음) |

## 출처가 서로 어긋나는 지점

**예제 먼저(Sweller·Kalyuga) 대 문제 먼저(Kapur·Schwartz).** Kalyuga 2003 은 초보자에게 worked example 이 문제 풀이보다 낫다고 하고, Sinha & Kapur 2021 은 문제 먼저가 g=0.36 으로 낫다고 한다. 확인된 범위에서 둘은 절차 지식(문제 먼저 이득 없음), 설명의 필수성, 어린 학습자에서 같은 결론을 낸다.

남는 다툼은 "사전 지식이 거의 없는 초보자에게 안내 없는 문제가 낭비인가"다. 메타분석은 사전 지식 수준을 조절 변인으로 코딩하지 않았고 Kalyuga 는 역전 지점을 숫자로 주지 않는다. Sweller 2019 는 생산적 실패를 한 번도 언급하지 않는다. 이 한 점은 판정되지 않았다.

Kapur 2008 을 순서 비교의 원형으로 인용하면 안 된다. 두 조건 모두 설명 단계가 없고 조작 변인은 문제의 구조화 정도다. Sinha & Kapur 스스로도 "설계 충실도가 낮은 문제 먼저를 대조군과 비교해 나온 무효 결과로 생산적 실패의 비효과를 주장하는" 연구가 많다고 지적한다.

**피드백이 해로울 때(Kluger & DeNisi) 대 "빠른 피드백" 통념.** Kluger & DeNisi 는 빠르기를 재지 않았다. 해로운 셋 중 하나는 주의를 자기로 옮기는 피드백이지 느린 피드백이 아니다. 통념과 부딪히는 것은 Shute 와 Hattie 가 인용한 시점 연구다. 시험 상황과 어려운 문항에서는 지연이 나았고(1.17), 즉시성은 의존과 부주의를 낳을 수 있다.

Kluger & DeNisi 안에도 작은 불일치가 있다. 본문은 잦은 피드백이 효과를 키운다고 하지만 표 2 는 상위 사분위 .32, 하위 .39 로 반대다. Hattie 의 재인용도 표 쪽을 따른다. 억지로 합치지 않고 적어 둔다.

**자기 설명은 중간 효용(Dunlosky 2013) 대 좋은 학생의 표지(Chi 1989).** 둘은 다른 질문에 답한다. Chi 는 8명의 자발적 행동을 사후 분류한 상관이고, 저자도 "잘하는 학생이 애초에 법칙을 더 잘 알았을 수 있다"고 적는다. Dunlosky 는 프롬프트로 시킨 자기 설명을 처방할 근거의 넓이를 매겼고, 인용한 것은 Chi 1994 이지 1989 가 아니다.

Loksa & Ko 2016 이 한 겹을 더한다. CS2 에서 자기 설명 발화가 오류 증가와 상관했다. 저자 해석은 "막힐 때 더 말한다"다. 세 출처를 합치면 "자기 설명은 잘하는 사람의 표지이지만, 시킨다고 되지는 않고, 막혀서 하는 설명은 신호일 뿐"까지 말할 수 있다.

**이론가 대 실험가(Klahr & Dunbar).** 이론가가 두 배 빨랐다는 결과를 "가설을 먼저 세우는 편이 낫다"로 읽기 쉽지만 원문은 그렇게 말하지 않는다. 이론가 전원이 프로그래밍 경험자였다. 가설을 지을 지식이 없으면 실험가의 길뿐이고, 그 길도 도달한다. 갈림은 전략의 우열이 아니라 사전 지식이다.

**추적이 쓰기에 앞선다(Lister 2004·Xie 2019) 대 근거의 얇음.** Lister 는 쓰기를 측정하지 않았고 "추적이 선행 조건"이라는 것은 논문이 다음 연구로 넘긴 가정이다. Xie 2019 의 순서 이론은 그 가정 위에 서 있고 자체 평가는 9명이다. Nelson 2017 만 순서를 조작했고 p<.05 를 넘지 못했다. 이론은 세지만 실증은 얇다.

**개념 기계가 무엇인가.** du Boulay·Sorva(실행기의 추상, 학습자 모델이 아님), Fincher 2020(교사의 교육 장치), Qian & Lehman(언어 독립 mental model)이 다르다. 이 노트는 du Boulay 의 정의를 쓴다.

## 출처 목록

### 확인한 출처

| 출처 | 근거 종류 | 비고 |
|---|---|---|
| du Boulay, 1986, Some Difficulties of Learning to Program (J. Educational Computing Research 2(1)), http://www.sussex.ac.uk/Users/bend/papers/diffsofprogramming.pdf | 실무자 의견·이론 | 저자 공개본(스캔, OCR 로 읽음) |
| Sorva, 2012, Visual Program Simulation in Introductory Programming Education (Aalto 박사논문) 5장, https://aaltodoc.aalto.fi/items/d982d1ce-af44-465d-83b4-56a558fe9f26 | 이론(연구 종합) | 기관 저장소. Sorva 2013 TOCE 대신 |
| Fincher, Jeuring, Miller 외, 2020, Notional Machines in Computing Education: The Education of Attention (ITiCSE WGR), https://aaltodoc.aalto.fi/items/ceef5fe0-0b8b-4741-a563-877df32a9a8e | 이론(연구 종합·목록) | 기관 저장소(Aalto) |
| Nelson, Xie, Ko, 2017, Comprehension First (ICER), https://faculty.washington.edu/ajko/papers/Nelson2017PLTutor.pdf | 실증 | 저자 공개본 |
| Xie, Loksa, Nelson 외, 2019, A Theory of Instruction for Introductory Programming Skills (CSE 29), https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf | 이론·실증(9명) | 저자 공개본 |
| Lister 외, 2004, A Multi-National Study of Reading and Tracing Skills in Novice Programmers (ITiCSE WGR), https://opus.lib.uts.edu.au/bitstream/10453/4126/3/2004000904.pdf | 실증 | 기관 저장소(UTS) |
| Qian & Lehman, 2017, Students' Misconceptions and Other Difficulties in Introductory Programming (ACM TOCE 18(1)), https://dl.acm.org/doi/pdf/10.1145/3077618 | 이론(연구 종합) | 출판사 공개본(bronze), 웨이백 스냅샷으로 읽음 |
| Chi, Feltovich, Glaser, 1981, Categorization and Representation of Physics Problems by Experts and Novices (Cognitive Science 5), https://apps.dtic.mil/sti/pdfs/ADA100301.pdf | 실증 | 기관 저장소(DTIC, ONR 기술보고서판), 웨이백으로 읽음 |
| Kapur, 2008, Productive Failure (Cognition and Instruction 26(3)), https://arch.kuleuven.be/studeren/tall/artikels/productive-failure-kapur.pdf | 실증 | 미러(KU Leuven 강의 페이지) |
| Sinha & Kapur, 2021, When Problem Solving Followed by Instruction Works (RER 91(5)), https://www.research-collection.ethz.ch/handle/20.500.11850/490417 | 실증(메타분석) | 기관 저장소(ETH), 출판사 최종본 CC-BY |
| Loibl, Roll, Rummel, 2017, Towards a Theory of When and How Problem Solving Followed by Instruction Supports Learning (Educational Psychology Review 29), https://www.wright.edu/sites/www.wright.edu/files/uploads/2017/Mar/event/Loibl2016_TheoryProblemSolvingandInstruction.pdf | 이론(연구 종합) | 미러(Wright State 행사 업로드, 온라인 선공개판) |
| Schwartz & Bransford, 1998, A Time for Telling (Cognition and Instruction 16(4)), http://aaalab.stanford.edu/assets/papers/earlier/A_time_for_telling.pdf | 실증 | 저자 공개본 |
| Schwartz & Martin, 2004, Inventing to Prepare for Future Learning (Cognition and Instruction 22(2)), https://aaalab.stanford.edu/assets/papers/2004/Inventing_to_prepare_for_future_learning.pdf | 실증 | 저자 공개본 |
| Kalyuga, Ayres, Chandler, Sweller, 2003, The Expertise Reversal Effect (Educational Psychologist 38(1)), https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/The%20Expertise%20Reversal%20Effect.pdf | 이론(자기 실험 종합) | 미러(UOW 기관 저장소 사본의 재배포) |
| Ericsson, Krampe, Tesch-Römer, 1993, The Role of Deliberate Practice in the Acquisition of Expert Performance (Psychological Review 100(3)), https://gwern.net/doc/psychology/1993-ericsson.pdf | 실증·이론 | 미러(gwern.net) |
| Sweller, van Merriënboer, Paas, 2019, Cognitive Architecture and Instructional Design: 20 Years Later (Educational Psychology Review 31), https://ndownloader.figshare.com/files/50496330 | 이론 | 기관 저장소(UOW, figshare). 목록에 없던 추가 출처. 생산적 실패 언급 없음 |
| Klahr & Dunbar, 1988, Dual Space Search During Scientific Reasoning (Cognitive Science 12(1)), https://users.cs.northwestern.edu/~paritosh/papers/sketch-to-models/klahr-dunbar-dual-space-search-cogsci-1988.pdf | 실증·이론 | 미러(Northwestern 개인 페이지 스캔, 12·30쪽 누락) |
| Dunbar, 1993, Concept Discovery in a Scientific Domain (Cognitive Science 17(3)), http://www.dartmouth.edu/~kndunbar/cogsci93.pdf | 실증 | 저자 공개본(프리프린트), 웨이백으로 읽음 |
| Zimmerman, 2005, The Development of Scientific Reasoning Skills (NRC 위원회 보고서 초고), https://sites.nationalacademies.org/cs/groups/dbassesite/documents/webpage/dbasse_080105.pdf | 이론(연구 종합) | 저자 보고서, National Academies 호스팅. Zimmerman 2007 대신 |
| Hattie & Timperley, 2007, The Power of Feedback (RER 77(1)), https://simvilledev.ku.edu/sites/default/files/PD%20Resources/Hattie%20power%20of%20feedback[1].pdf | 이론(메타분석 종합) | 미러(Kansas 대 교원연수 페이지, 스캔을 OCR) |
| Kluger & DeNisi, 1996, The Effects of Feedback Interventions on Performance (Psychological Bulletin 119(2)), https://mrbartonmaths.com/resourcesnew/8.%20Research/Marking%20and%20Feedback/The%20effects%20of%20feedback%20interventions.pdf | 실증(메타분석)·이론 | 미러 |
| Shute, 2008, Focus on Formative Feedback (RER 78(1); ETS RR-07-11 판), https://myweb.fsu.edu/vshute/pdf/shute%202007_f.pdf | 이론(연구 종합) | 저자 공개본(보고서판) |
| Victor, 2012, Learnable Programming, https://worrydream.com/LearnableProgramming/ | 실무자 의견 | 저자 사이트 |
| Butterfield & Metcalfe, 2006, The Correction of Errors Committed with High Confidence (Metacognition and Learning 1), http://www.columbia.edu/cu/psychology/metcalfe/PDFs/Butterfield_Metcalfe_2006.pdf | 실증 | 저자 공개본. 2001 데이터를 재수록. 목록에 없던 추가 출처 |
| Metcalfe, 2017, Learning from Errors (Annual Review of Psychology 68), https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf | 이론(연구 종합) | 저자 공개본. 목록에 없던 추가 출처 |
| Chi, Bassok, Lewis, Reimann, Glaser, 1989, Self-Explanations (Cognitive Science 13(2)), https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chibassoklewisreimannglaser_0.pdf | 실증 | 저자 연구실 공개본(스캔을 OCR) |
| Chi & Wylie, 2014, The ICAP Framework (Educational Psychologist 49(4)), https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chiwylie2014icap_2.pdf | 이론 | 저자 연구실 공개본 |
| Rozenblit & Keil, 2002, The Misunderstood Limits of Folk Science (Cognitive Science 26(5)), https://pmc.ncbi.nlm.nih.gov/articles/PMC3062901/ | 실증 | 기관 저장소(PMC 저자 원고) |
| Bjork, Dunlosky, Kornell, 2013, Self-Regulated Learning: Beliefs, Techniques, and Illusions (Annual Review of Psychology 64), https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/RBjork_Dunlosky_Kornell_2012.pdf | 이론(연구 종합) | 저자 연구실 공개본 |
| Koriat & Bjork, 2005, Illusions of Competence in Monitoring One's Knowledge During Study (JEP:LMC 31(2)), https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/Koriat_RBjork_2005.pdf | 실증 | 저자 연구실 공개본 |
| Dunlosky, Rawson, Marsh, Nathan, Willingham, 2013, Improving Students' Learning With Effective Learning Techniques (PSPI 14(1)), https://www.whz.de/fileadmin/lehre/hochschuldidaktik/docs/dunloskiimprovingstudentlearning.pdf | 이론(근거 평가) | 미러(독일 대학 교수학습센터) |
| Roediger & Karpicke, 2006, Test-Enhanced Learning (Psychological Science 17(3)), https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf | 실증 | 저자 연구실 공개본 |
| Flavell, 1979, Metacognition and Cognitive Monitoring (American Psychologist 34(10)), https://jgregorymcverry.com/readings/flavell1979MetacognitionAndCogntiveMonitoring.pdf | 이론 | 미러(개인 사이트 스캔) |
| Loksa, Ko, Jernigan, Oleson, Mernagh, Burnett, 2016, Programming, Problem Solving, and Self-Awareness (CHI), https://faculty.washington.edu/ajko/papers/Loksa2016ProgrammingProblemSolving.pdf | 실증 | 저자 공개본 |
| Loksa & Ko, 2016, The Role of Self-Regulation in Programming Problem Solving Process and Success (ICER), https://faculty.washington.edu/ajko/papers/Loksa2016SelfRegulation.pdf | 실증 | 저자 공개본. 목록에 없던 추가 출처 |
| Prather, 2018, Beyond Automated Assessment: Building Metacognitive Awareness in Novice Programmers in CS1 (NSU 박사논문), https://nsuworks.nova.edu/gscis_etd/1030 | 실증 | 기관 저장소, 웨이백으로 읽음. Prather 외 2018 ICER 본문 대신 |
| Prather, Becker, Craig, Denny, Loksa, Margulieux, 2020, What Do We Think We Think We Are Doing? (ICER), https://hdl.handle.net/20.500.14694/10138 | 이론(연구 종합) | 기관 저장소(Georgia State) |
| Feynman, 1988, 칠판 사진 "Richard Feynman's blackboard at time of his death", https://digital.archives.caltech.edu/collections/Images/1.10-29/ | 실무자 의견(유물) | Caltech 아카이브 공식 |
| Feynman, 1985, Surely You're Joking, Mr. Feynman! "A Different Box of Tools" 장, https://archive.org/details/Surely-youre-joking-mr.-feynman | 실무자 의견 | 미러(archive.org 전자책 OCR) |
| Papert, 1980, Mindstorms 서문 "The Gears of My Childhood", http://www.papert.org/articles/GearsOfMyChildhood.html | 이론 | 저자 사이트. 1장은 미러(arvindguptatoys.com)로 읽음 |
| Papert & Harel, 1991, Situating Constructionism, http://www.papert.org/articles/SituatingConstructionism.html | 이론 | 저자 사이트 |
| Karpathy, 2016, Yes you should understand backprop, https://karpathy.medium.com/yes-you-should-understand-backprop-e2f06eab496b | 실무자 의견 | 저자 글, 웨이백 2017 캡처로 읽음 |
| Nystrom, 2021, Crafting Interpreters 1장 Introduction, https://craftinginterpreters.com/introduction.html | 실무자 의견 | 저자 사이트 |
| Nisan & Schocken, 2005, The Elements of Computing Systems 서문·서론, http://www.nand2tetris.org/chapters/preface.pdf | 실무자 의견 | 저자 사이트, 웨이백으로 읽음. Schocken 외 2009 논문 대신 |
| Norvig, (How to Write a (Lisp) Interpreter (in Python)), https://norvig.com/lispy.html | 실무자 의견 | 저자 사이트 |
| Norvig, How to Write a Spelling Corrector, https://norvig.com/spell-correct.html | 실무자 의견 | 저자 사이트 |
| Evans, 2021, Get better at programming by learning how things work, https://jvns.ca/blog/learn-how-things-work/ | 실무자 의견 | 저자 사이트. 목록에 없던 추가 출처 |
| Nielsen, 2018, Augmenting Long-term Memory, http://augmentingcognition.com/ltm.html | 실무자 의견 | 저자 사이트 |
| Hunt & Thomas, 2000, The Pragmatic Programmer "Rubber Ducking" (p.95), https://archive.org/details/AndrewHuntDavidThomasThePragmaticProgrammerFromJourneymanToMasterAddisonWesleyLongman2000 | 실무자 의견 | 미러(archive.org 전자책 OCR) |
| Kapur, 2016, Examining Productive Failure, Productive Success, Unproductive Failure, and Unproductive Success in Learning (Educational Psychologist 51(2)), https://repository.eduhk.hk/en/publications/examining-productive-failure-productive-success-unproductive-fail-5/ | 이론 | 초록만. 네 기제는 Sinha & Kapur 2021 이 인용한 Kapur & Bielaczyc 2012 로 대신 |
| Rubin, 2013, The Effectiveness of Live-Coding to Teach Introductory Programming (SIGCSE), https://doi.org/10.1145/2445196.2445388 | 실증 | 초록만. 결과 수치 미확인이라 근거로 쓰지 않음 |
| Butterfield & Metcalfe, 2001, Errors Committed with High Confidence Are Hypercorrected (JEP:LMC 27(6)), PubMed 11713883 | 실증 | 초록만. 데이터는 2006 논문의 재수록으로 확인 |
| Klahr, Fay, Dunbar, 1993, Heuristics for Scientific Experimentation (Cognitive Psychology 25), PubMed 8425385 | 실증 | 초록만 |
| Schauble, 1990, Belief Revision in Children (JECP 49), PubMed 2303776 | 실증 | 초록만 |

### 미확인 출처

| 출처 | 못 연 이유 | 대신 쓴 것 |
|---|---|---|
| Sorva, 2013, Notional Machines and Introductory Programming Education (ACM TOCE) | 유료. Semantic Scholar·Unpaywall 모두 공개본 없음 | 같은 저자의 2012 박사논문 5장 |
| Zimmerman, 2007, The Development of Scientific Thinking Skills in Elementary and Middle School (Developmental Review) | 유료. 저자 페이지 404 | 저자의 2005 NRC 보고서 초고 |
| Prather 외, 2018, Metacognitive Difficulties Faced by Novice Programmers (ICER) 본문 | ACM 봇 차단, 공개본 없음 | 초록 + 같은 연구를 담은 저자 박사논문 |
| Schocken, Nisan, Armoni, 2009, A Synthesis Course in Hardware Architecture, Compilers, and Software Engineering (SIGCSE) | 공개 PDF 없음. nand2tetris.org 에도 없음 | 책 서문·서론 |
| Falkner, Vivian, Falkner, 2014, Identifying Computer Science Self-Regulated Learning Strategies (ITiCSE) | 유료. Adelaide 저장소 링크 404 | 근거로 쓰지 않음 |
| Rubin, 2013 본문 | ACM 봇 차단, 저자 페이지에 링크 없음 | 초록만. 결과 수치를 쓰지 않음 |
| Kapur, 2016 본문 | 출판사 403, 기관 저장소는 메타데이터만 | 초록 + Sinha & Kapur 2021 의 인용 |
| Butterfield & Metcalfe, 2001 본문 | Columbia 연구실의 PDF 링크가 잘못된 파일 | 2006 논문의 재수록 데이터 |
| Ashman 외, 2020(교재 복잡도가 문제 먼저의 경계라는 연구) | 열지 않음 | Sinha & Kapur 2021 이 인용한 대로만 언급 |
| Kapur & Bielaczyc, 2012(생산적 실패의 네 기제) | 열지 않음 | Sinha & Kapur 2021 의 인용으로만 언급 |
| Kulik & Kulik 1988, Clariana 외 2000, Corbett & Anderson 2001(피드백 시점 연구) | 열지 않음 | Hattie & Timperley 2007 과 Shute 2008 의 인용으로만 언급 |
| Chi 외 1994(텍스트 자기 설명), Menekse 외 2013(ICAP 검증) | 열지 않음 | Dunlosky 2013 과 Chi & Wylie 2014 의 인용으로만 언급 |
