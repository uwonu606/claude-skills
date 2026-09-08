# 처음 보는 레포지토리와 처음 보는 기술, 뛰어난 사람은 어떻게 접근하는가

## 질문과 결론 요약

질문: 처음 보는 레포지토리에, 그리고 처음 보는 기술(언어·프레임워크·도구·개념)에 접근하는 것이 뛰어난 사람은 무엇을 다르게 하는가.

**레포지토리.** 뛰어난 사람은 전체를 읽지 않는다. 과제에서 출발해 "이 코드가 무엇을 할 것이다"라는 가설을 세우고, 관련된 부분만 찾아 읽고, 바꾸고 돌려서 가설을 확인한다. 얻은 이해는 "목표 ↔ 코드" 대응으로 층을 이루게 조직한다. 초보자는 표면 단서(이름·증상)로 검색하다 실패하고, 줄 단위로 읽고, 국소 단서로 의도를 추측한다.

**기술.** 뛰어난 사람은 이미 아는 것과 대응시켜 빠르게 출발하되, 대응이 깨지는 지점을 의식한다. 문법보다 개념(작동 모델)을 먼저 잡고, 작은 실험과 장난감 구현으로 모델을 검증하며, 자기가 어디서 혼란스러운지 알아차린다. 지식을 표면이 아니라 원리로 분류한다.

**공통.** 둘 다 "과제 주도 → 가설 → 실행 환경에서 빠른 피드백 → 자기 이해 점검"이라는 같은 루프다. 갈리는 지점은 위험의 종류다. 레포에서는 너무 좁게 읽어 멀리 있는 상호작용을 놓치는 것이 위험이고, 기술에서는 옛 지식이 새 것에 잘못 대응되는 것이 위험이다. 레포의 답("왜 이렇게 했나")은 문서보다 사람과 이력에 있고, 기술의 답은 대체로 스펙·문서·예제에 있다.

## 조사 방법

**검색과 열람.** 지시받은 출처 목록을 WebSearch 로 하나씩 찾고, 논문은 PDF 를 받아 텍스트를 뽑아 읽었다. 블로그와 책 소개 페이지는 HTML 을 받아 본문을 읽었다. 본문에서는 출처를 "저자 연도"로 가리키고, 전체 서지·URL·근거 종류는 #출처 목록 에 있다.

**근거 종류.** `실증` 은 실험·현장 관찰 연구, `이론` 은 모델·틀의 제안이나 연구 종합, `실무자 의견` 은 경험에 바탕한 에세이·강연이다. 종류가 다르면 무게가 다르다. 한 출처가 둘을 겸하면 둘 다 적었다.

**빼거나 대체한 것.** 남이 요약한 블로그(understandlegacycode.com, 강의 슬라이드 등)는 근거로 쓰지 않았다. 열지 못한 출처는 근거로 세지 않았고, 무엇을 왜 못 열었고 무엇으로 대신했는지는 #출처 목록 의 미확인 표에 있다. Simon Willison 은 본인이 쓴 "낯선 코드베이스" 글을 찾지 못해 뺐다.

**목록에 없던 추가 출처.** 전문가-초보자 비교 실증이 우선이라는 지시에 따라 Koenemann & Robertson 1991, Fix·Wiedenbeck·Scholtz 1993, Vessey 1985, Letovsky & Soloway 1986, von Mayrhauser & Vans 1997 을 더했다.

신입 개발자 현장 연구로 Dagenais 외 2010 과 Begel & Simon 2008 을 더했다. 기술 쪽으로는 Shrestha 외 2020(새 언어 학습), Robillard & DeLine 2011(API 학습), Kahneman & Klein 2009(전문 직관의 조건)를 더했다.

**호스팅 주의.** Sweller 1988, Kahneman & Klein 2009, Naur 1985 와 Kent State 강의 페이지의 논문들은 저자나 출판사가 아닌 제3자가 올린 미러 PDF 로 읽었다. 내용은 원 논문 스캔이라 원 출처로 친다. 표에 "미러"로 표시했다.

**용어.** 다른 분야 용어는 처음 나올 때 한 줄로 푼다. 메타인지(metacognition)는 자기가 얼마나 이해했는지 스스로 점검하는 능력이다. 전이(transfer)는 이미 아는 것을 새 상황에 옮겨 쓰는 것이고, 간섭(interference)은 옛 지식이 새 학습을 방해하는 것이다. 스키마(schema)는 머릿속에 굳은 문제 유형별 틀이다. 비콘(beacon)은 코드가 무엇을 하는지 알려주는 눈에 띄는 표지, 예컨대 함수 이름이다.

## 처음 보는 레포지토리

세 묶음으로 나눈다. 무엇을 읽고 무엇을 안 읽는가, 어떻게 확인하는가, 이해를 어디서 얻고 어디에 남기는가.

### 읽을 범위

| 무엇을 하는가 | 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 과제에서 출발해 관련된 부분만 읽는다. 관련성을 세 층으로 나눈다: 고쳐야 할 코드, 그것과 상호작용하는 코드, 다른 코드를 찾는 데만 쓰는 코드(차트·main). | 신입은 "시작점" 자체를 찾는 질문("이 도메인 개념은 어떤 타입인가")을 훨씬 많이 한다. | "프로그램이 커지면 어떤 포괄적 전략도 비용상 불가능해진다." 실험에서 전문가 누구도 체계적으로 읽지 않았고, 프로시저의 1/4 은 아무도 안 봤다. | 실증. Koenemann & Robertson 1991(경력 4~15년 전문가 12명, 636줄 PASCAL 프로그램 수정). Sillito 외 2006(신입 9명 vs 현업 16명, 44종 질문 4범주). |
| 이름을 비콘 삼아 가설을 세우고, 가설이 없거나 깨질 때만 코드를 줄 단위로 읽는다. | 초보자와 덜 숙련된 전문가는 변수명 같은 촉발 단서로 추측만 하고 코드로 확인하지 않는다. | 이해는 위에서 아래로 가설을 정제하는 과정이며, 상향식 읽기는 "가설이 없거나 실패한 경우"와 직접 관련된 코드에만 쓰인다. | 실증. Koenemann & Robertson 1991. Fix 외 1993(Pennington 의 관찰을 인용). 이론 종합. von Mayrhauser & Vans 1995(Brooks 1983 의 가설 주도 모델 요약). |
| 넓게 먼저, 시스템 관점으로 본다. 코드를 덩어리(chunk)로 묶어 매끄럽게 훑는다. | 초보자는 깊이 우선으로 파고들거나, 넓게 보더라도 시스템 관점이 없다. 같은 곳을 되풀이 확인하는 불규칙한 탐색을 한다. | 덩어리로 묶는 능력이 전문성의 기준이었고, 그 능력이 탐색 전략과 강하게 연결됐다. | 실증. Vessey 1985(같은 회사 프로그래머 16명, 디버깅 발화 분석). 실증(신입 회고). Begel & Simon 2008 의 신입 T: "한 구멍을 깊게 파지 말고 모든 것을 넓게 알아야 한다." |
| 이해를 층으로 조직한다: 목표 ↔ 코드의 명시적 대응, 되풀이되는 패턴의 인식, 내부 연결, 원문 위치에 대한 근거. | 초보자의 표현은 이 다섯 특성이 없거나 싹만 있다. 표현이 문법 순서에 묶여 있다. | 전문가는 "여러 종류의 정보"를 뽑아 표현에 넣으며, 한두 차원이 아니라 이 전부에서 초보자와 갈린다. | 실증. Fix·Wiedenbeck·Scholtz 1993(초보 20명, 전문가 20명). 이론 종합. von Mayrhauser & Vans 1995: 전문가는 "문법이 아니라 알고리즘"으로 지식을 조직하고, 의심스러운 가설을 훨씬 빨리 버린다. |
| 먼저 제어 흐름 수준(프로그램 모델)을 잡고, 과제가 요구하면 문제 영역 수준(상황 모델)으로 올린다. | 초보자는 과제가 요구하지 않으면 상황 모델을 스스로 만들지 않는다. | 전문가 80명 실험에서 "절차적 단위"가 표현의 기본이었고, 나중 단계에서 과제 목표가 표현을 바꿨다. 문서화 과제에서 전문가와 초보자는 "상황 모델의 정교함에서 갈렸고 프로그램 모델에서는 갈리지 않았다." | 실증. Pennington 1987(전문 프로그래머 80명 + 40명). Burkhardt·Détienne·Wiedenbeck(초록만 확인). |

### 확인

| 무엇을 하는가 | 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 표면 단서(화면 증상, 그럴듯한 이름)로 검색을 시작하지 않는다. | 낯선 코드를 받은 개발자들은 검색의 88% 가 나중에 쓸모없었고, 시간의 약 36% 를 무관한 코드를 보는 데 썼다. 9명 중 8명이 "paint" 를 검색해 엉뚱한 메서드로 갔다. | 하나의 식별자가 코드의 목적을 다 담지 못한다("어휘 문제"). 탐색 단서가 잘못되면 실패한 검색이 이어진다. | 실증. Ko 외 2006(70분 과제, 항해에 시간의 35%). |
| 국소 단서로 의도를 추측하지 않고, 멀리 떨어진 코드와의 상호작용을 확인한다. | 시간 압박 아래 "국소 코드 맥락, 문서, 의미 있는 식별자"로 목표를 추측한다. 그럴듯하지만 틀린 결론에 이르거나 중복을 못 본다. | 계획(plan)이 코드 여기저기에 흩어져 있으면(delocalized) 국소 이해가 프로그램 전체에 대한 잘못된 이해가 된다. 체계적으로 읽은 사람만 실행 시 상호작용(인과 지식)을 얻어 수정에 성공했다. | 실증. Letovsky & Soloway 1986(전문가 4명 + 주니어 2명, 6명 중 3명만 완료). 실증(요약으로 확인). Littman 외 1987 을 Storey 2005 와 Koenemann & Robertson 1991 이 요약: "필요한 만큼" 전략은 상호작용을 놓쳤다. |
| 코드를 바꾸고 돌려서 배운다. 빌드해 실행하고, 일부러 깨뜨리고, 첫 주에 작은 버그를 고쳐 커밋한다. | 강의·일반 문서부터 시작한 신입은 느렸고 "컴파일 오류를 고치며 대체로 쓸모없는 문서를 읽는 외로운 여정"이 됐다. | 신입의 절반이 "소스를 컴파일해 제품을 돌릴 수 있게 된 순간"을 가장 값진 정보로 꼽았다. 코드베이스는 계속 바뀌어 학습 자료가 빨리 낡는다. "시스템은 바꿔 보아야만 이해할 수 있다." "디버깅은 새 코드베이스를 배우는 가장 좋은 방법 중 하나다." | 실증. Dagenais 외 2010(IBM 등 18개 프로젝트 신입 18명). 실무자 의견. Kerr 2025("HELLO JESS" 로 바꾸고 화면에서 본다), Evans 2022. |
| 현재 행동을 테스트로 고정한 뒤 바꾼다(특성화 테스트, characterization test). | 테스트 없이 "머리로 추론"하며 바꾸다가 보수적으로 굳고, 시스템을 더 어지럽힌다. | "소프트웨어 개발에서 가장 어려운 문제는 이해다." 추론으로 쌓은 이해는 매번 다시 추론해야 하지만, 테스트는 "근거 있는 이해"로 남는다. "똑똑함으로는 안 된다." | 실무자 의견. Feathers 2002. |
| 질문을 밖에 두고 답을 찾는다: 무엇을 찾는지 명시하고, 가설을 세우고, 코드로 확인하는 탐구(inquiry) 단위로 움직인다. | | 전문가 발화의 주된 사건이 "질문하기"와 "추측하기"였다. 신입은 코드베이스에 대한 44종의 질문을 던지며, 첫 세 범주(시작점 찾기, 그 위에 쌓기, 부분 그래프 이해)는 현업보다 신입에게 더 잦았다. | 실증. Sillito 외 2006. 이론 종합. Storey 2005(Letovsky 의 inquiry 요약). |

### 사람과 기록

| 무엇을 하는가 | 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| "왜 이렇게 했나"를 묻고, 답을 이력과 사람에게서 찾는다. | | 전문 개발자 179명이 꼽은 가장 어려운 질문은 의도와 근거(rationale)였다("왜 다른 방식으로 안 했나" 15건). 답을 찾는 한 전략은 "코드가 만들어진 이력을 찾아 맥락과 동기를 이해하는 것"이다. | 실증. LaToza & Myers 2010(371개 질문, 21범주). |
| 이론을 가진 사람 곁에서 일한다. 문서만으로는 이론이 넘어오지 않는다. | | 프로그래머가 가진 것은 텍스트가 아니라 "이론"이다: 코드가 세계의 어떤 일에 대응하는지, 각 부분이 왜 그런지, 수정 요구에 어떻게 응할지를 설명할 수 있는 지식. 새 프로그래머가 이 이론을 얻으려면 "텍스트와 문서에 친숙해질 기회로는 불충분하고, 이미 이론을 가진 프로그래머와 밀접하게 일할 기회가 필요하다." | 이론. Naur 1985. |
| 안내자에게 설치·코드 개요·과제 하나를 따라가는 걸음(walkthrough)을 받는다. 멘토에게 진행을 자주 확인받고, 막히면 오래 붙들지 않고 묻는다. | 진행 확인이 드문 팀의 신입은 묻기 전에 몇 시간에서 며칠을 혼자 붙들었고, "알아야 하는 줄 몰랐던" 정보를 놓쳤다. 신입은 "똑똑하고 생산적이며 실수 없음을 증명해야 한다"고 느끼면서 정작 역할의 기능적 측면은 아직 모른다. | "어떤 도구나 지도도 사람 안내자가 주는 정보의 풍부함을 대신할 수 없다." 잦은 진행 확인은 묻기 편한 환경과 선제적 힌트를 만든다. | 실증. Dagenais 외 2010. 실증. Begel & Simon 2008(마이크로소프트 신입 8명 2개월 관찰). |
| 질문을 잘 던진다: 아는 것을 먼저 말하고, 예/아니오로 답할 수 있게 좁히고, 가장 경험 많은 사람만 찾지 않고, 공개된 자리에서 묻는다. | | 사람은 내가 무엇을 원하는지 "마법처럼 짐작할 수 없다." 아는 것을 먼저 말하면 상대가 내 모델을 보고 고쳐 준다. | 실무자 의견. Evans "So you want to be a wizard", Evans "How to ask good questions". |
| 작업 집합을 머리 밖에 둔다: 두 창·두 모니터로 나란히 놓고 비교하고, "아, 이거였구나" 순간을 기록한다. | 개발자들은 관련 코드를 편집기 탭·스크롤 위치에 담아 두다가 잃어버리고 다시 찾았다. | 부분 그래프 사이의 비교 질문에는 나란히 보기가 도움이 됐다. 전문가는 외부 장치를 기억 보조로 더 쓴다. | 실증. Ko 외 2006, Sillito 외 2006. 이론 종합. Storey 2005(Détienne 인용). 실무자 의견. Beck 2022(첫 문장만 공개). |
| 코드 읽기를 별도의 기술로 여기고 훈련한다. 다른 사람이 쓴 프로그램 뒤에서 일해 본다. | 3학년 학생도 손가락을 첫 줄에 대고 위에서 아래로 읽는다. 읽기 전략을 배운 적이 없기 때문이다. | 개발자 시간의 약 58% 가 이해에 쓰이는데, 문화는 "쓰기"만 강조한다. "코드 읽기는 그 자체의 기술 집합을 요구한다." "다른 프로그래머 뒤에서 프로젝트를 하라. 원저자가 없을 때 이해하고 고치는 데 무엇이 드는지 보라." | 실증. Xia 외 2018(79명 3,244시간, 시니어가 유의미하게 적은 비율). 실무자 의견. Hermans 2022, Spinellis 2003(서문·소개), Norvig. |

**해석:** 위 표에서 시니어가 이해에 시간을 덜 쓴다는 Xia 의 결과는 "같은 도메인을 반복해서"라는 조건이 붙는다. 7년차 P1 의 말대로 "해 본 적 없는 새 프로젝트, 예컨대 Matlab 프로젝트라면 여전히 많은 시간을 쓴다." 뛰어남은 시간을 줄이는 것이 아니라, 어디에 시간을 쓰는지를 고르는 것으로 읽힌다.

## 처음 보는 기술

두 묶음이다. 아는 것을 어떻게 옮겨 쓰는가, 새 지식을 어떻게 조직하고 검증하는가.

### 아는 것을 옮기기

| 무엇을 하는가 | 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 새 언어를 이전 언어에 대응시켜 빠르게 출발한다. 필요한 기능만 그때그때 배우고(just-in-time), 치트 시트와 공식 문서와 기존 코드를 쓴다. | | 인터뷰한 전문가 16명 전원이 "필요한 만큼만 배우는 기회주의적 전략"을 썼다. 책은 참고용으로만: "그럴 시간이 없다." | 실증. Shrestha·Botta·Barik·Parnin 2020(경력 5~31년 16명 인터뷰). |
| 대응이 깨지는 지점을 의식한다. 크게 다른 언어(C# → Ruby, Python → SAS, C# → Rust 메모리 관리)로 갈 때는 "아무것도 대응시키지 않고 전부 새것으로" 다룬다. | 대응에 의존한 사람은 간섭에 걸린다. 여러 언어에 걸친 Stack Overflow 질문 450개 중 276개(61%)가 이전 언어 지식에서 온 잘못된 가정을 담고 있었다. | 대응은 "출발에는 유용하지만 두 언어가 크게 다를 때 간섭을 일으킨다." 한번 안 것은 지워지지 않는다: "배운 것을 되돌리는 일(unlearning)은 없다." | 실증. Shrestha 외 2020. 실무자 의견(연구자 강연). Hermans 2022: Haskell → JavaScript 는 양의 전이와 음의 전이가 함께 온다. 이론 종합. *How People Learn* 3장: "모든 새 학습은 이전 학습에 바탕한 전이를 포함한다." |
| 표면이 아니라 원리로 분류한다. 문제를 보면 "어떤 원리가 적용되는가"부터 잡는다. | 초보자는 "겉이 비슷한" 문제끼리(도르래, 경사면) 묶는다. | 전문가의 문제 스키마는 원리를 중심으로 조직돼 있고, 이 결과는 "과학자부터 택시 기사까지 많은 영역에서 재현됐다." | 실증(저자 회고로 확인). Chi 1993(Chi·Feltovich·Glaser 1981 회고). 이론 종합. *How People Learn* 2장 원칙 1·2. |
| 지식에 "언제 쓰는가"를 붙인다. API 라면 의도, 시나리오 ↔ API 대응, 내부가 어떻게 도는지(관통 가능성, penetrability)를 확인한다. | | 조건이 붙지 않은 지식은 관련 있어도 활성화되지 않는 "죽은 지식"이 된다. 마이크로소프트 개발자 440명 이상이 꼽은 가장 큰 장애는 의도 문서의 부재였다. "메서드 하나가 스레드 다섯 개를 만든다는 걸 알아야 쓸 수 있다." | 이론 종합. *How People Learn* 2장 원칙 3. 실증. Robillard & DeLine 2011. |
| 예제로 배우되, 돌아가는 것과 이해한 것을 구분한다. 좋은 예제는 관련 함수 몇 개를 함께 쓰는 "패턴 하나" 크기다. | 긴 예제는 "복사해서 돌릴 수 있게 해 주지만 이해했다는 뜻은 아니다." 신입들은 예제를 복사해 고쳤다. | 예제 활용은 API 학습 연구 전반에서 일관되게 관찰됐다. 메서드 하나짜리 조각은 쓸모가 적었다. | 실증. Robillard & DeLine 2011, Dagenais 외 2010. |
| 여러 언어·패러다임을 알아 둔다. | | Norvig 이 인용한 Perlis 의 말: "생각하는 방식을 바꾸지 않는 언어는 배울 가치가 없다." 반대 의견은 #출처가 서로 어긋나는 지점 에 있다. | 실무자 의견. Norvig. |

### 새 지식을 조직하고 검증하기

| 무엇을 하는가 | 초보자는 | 왜 (출처가 말하는 이유) | 근거 · 출처 |
|---|---|---|---|
| 문법보다 개념(작동 모델)을 먼저 잡는다. 기본 개념(예: 패킷이 무엇인가)을 알면 복잡한 것이 따라온다. | 개념 없이 문법부터 외운다. 24시간 만에 문법을 익혀도 "그 언어가 무엇에 좋고 나쁜지"는 못 배운다. | 장기 기억에 개념이 없으면 "다시 읽어도 안 된다." 반복은 소용없고 익숙함이 필요하다. 교육 실천에서는 개념(반복)을 먼저, 문법은 나중에 얹는다. | 실무자 의견. Hermans 2022, Evans "wizard", Norvig. |
| 혼란을 알아차리고 종류를 가른다: 모르는 개념(장기 기억), 한꺼번에 너무 많음(단기 기억), 알지만 조합이 안 됨(작업 기억). 종류마다 처방이 다르다. | "코드 읽기는 어렵다, 혼란스럽다"로 뭉뚱그려 무엇을 해야 할지 모른다. | "자기 이해와 오해를 이해하면" 혼란에서 나올 길이 생긴다. 전문가는 "현재 이해 수준을 점검하고 부족할 때 알아차리는" 메타인지를 보이며, 첫 해석에서 멈추지 않는다. | 실무자 의견(연구자 강연). Hermans 2022. 이론 종합. *How People Learn* 2장(전공 밖 문서를 읽은 역사학자 사례). 실무자 의견. Matuschak 2019: 책을 흡수하는 독자는 "이 생각은 …를 떠올리게 한다", "이 점은 …와 충돌한다", "어떻게 …인지 모르겠다"는 속말을 한다. |
| 모델이 깨진 순간을 붙든다. "5분이면 될 텐데 안 된다"는 어긋남을 조사한다. 대개 "빠진 것은 한두 가지"다. | 컴퓨터가 이상하게 굴면 그냥 넘긴다. | 어긋남은 모델의 구멍을 정확히 가리킨다. 부정 캐싱 하나를 알고 나자 그 뒤로 이해 못 할 문제가 없었다. | 실무자 의견. Evans 2023("Learning DNS in 10 years"). |
| 원전(스펙·RFC)을 특정 질문 하나를 들고 읽는다. 논문은 세 번 훑는다: 5~10분 개관, 1시간 내용, 그리고 "가상으로 재구현"하는 세 번째 읽기. | 처음부터 끝까지 순서대로 읽는다. | 질문이 있으면 "지루한 문서 전체가 아니라 문장 하나만 분석하면" 된다. Stack Overflow 답은 "정확한지 알 수 없어" 권위 있는 출처로 간다. 세 번째 읽기는 "숨은 실패와 가정"을 드러낸다. | 실무자 의견. Evans 2023, Keshav 2007. |
| 실험하고, 아주 나쁜 장난감 구현을 만든다. 실제 트래픽을 엿보고(dig, Wireshark), 남의 도메인에서 마음껏 망가뜨리고, 200줄짜리 DNS 리졸버를 쓴다. | | "컴퓨터 실험은 빠르고 싸고 대개 결과가 없다." 스스로 만든 "아주 나쁜 구현은 부당할 만큼 큰 자신감을 준다." 절차를 변형해 결과를 관찰해야 "각 단계의 어떻게와 왜"(개념 지식)가 생긴다. | 실무자 의견. Evans 2023. 이론. Hatano & Inagaki 1986. |
| 절차만 능숙한 전문가(routine)와 왜를 아는 전문가(adaptive)를 구분하고 후자를 겨냥한다. | | 적응적 전문가는 "절차를 효율적으로 수행할 뿐 아니라 그 의미와 대상의 본질을 이해"한다. 대상에 변동이 있을 때, 그리고 보상·평가 압박이 없어 장난스럽게 변형해 볼 때 생긴다. 보상이 걸리면 "안전 전략"으로 바뀐다. | 이론. Hatano & Inagaki 1986. |
| 통과해야 보이는 개념(threshold concept)이 있음을 안다. 넘기 전에는 새 생각이 조각조각으로만 배워진다. | 임계 개념을 못 넘은 학생은 "새 생각을 더 조각난 방식으로 배우는 것 외에 선택지가 거의 없다." | 임계 개념은 "이전에 닿을 수 없던 사고 방식을 여는 관문"이며, 변형적·비가역적·통합적이고, 종종 곤란하다. 예로 회계의 감가상각. | 이론. Land·Cousin·Meyer·Davies 2005. |
| 배우는 동안 인지 부하를 남긴다. 초보자는 스스로 문제를 풀기보다 예제로, 전문가는 그냥 밀고 나가도 된다(전문성 역전 효과). | 초보자가 수단-목적 분석으로 문제를 풀면 처리 용량이 그쪽에 다 쓰여 스키마가 안 생긴다. | "통상적 문제 풀이는 스키마 획득에 효과적이지 않다." 전문가에게는 밀고 나가기가 통하지만 "나한테 통한 것이 신입에게 통하리라" 여기면 안 된다. | 실증·이론. Sweller 1988. 실무자 의견(연구자 강연). Hermans 2022. |
| 피드백이 있는 환경, 전문가가 밀집한 환경에서 배운다. 자기 플레이를 녹화해 보고, 초고를 남에게 보이고, "조금 더 어려운 문제"를 계속 받는다. | 95번째 백분위에 갇힌 사람 대부분은 "자기 플레이를 관찰하거나 남에게 보이면 크게 나아진다는 걸 모른다." | 숙련된 직관에는 두 조건이 필요하다: "충분히 타당한 환경과 연습할 적절한 기회." 잘하는 사람의 머릿속 정보는 책으로 압축되지 않으므로 "학습 속도에 가장 좋은 것은 전문가로 가득한 환경"이다. 의도적 연습은 "지금 능력을 살짝 넘는 과제, 수행 분석, 오류 교정"이다. | 이론. Kahneman & Klein 2009. 실무자 의견. Luu "95%-ile isn't that good", "What to learn", "How I learned to program"(Glenn 이 "가능해 보이는 것보다 조금 어려운 문제"를 주고 80% 를 풀었다). Norvig. 이론 종합. *How People Learn* 3장. |

**해석:** 기술 쪽 실증은 레포 쪽보다 얇다. 전문가-초보자 차이는 물리·체스 같은 다른 영역에서 왔고(Chi, *How People Learn*), 프로그래머 대상 실증은 Shrestha 와 Robillard 둘이 사실상 전부다. 나머지는 이론과 실무자 의견이 메운다.

## 둘의 공통점과 차이

### 같은 원리

| 원리 | 레포에서 | 기술에서 |
|---|---|---|
| 과제 주도, 필요한 만큼 | "필요한 만큼(as-needed)" 전략, 관련성 세 층(Koenemann 1991). | "그때그때(just-in-time)" 학습, 필요한 기능만(Shrestha 2020). 두 논문 다 같은 단어 "opportunistic" 을 쓴다. |
| 가설 → 실행 환경에서 검증 | 비콘으로 가설, 코드로 확인, 바꾸고 돌리기(Koenemann, Dagenais, Kerr). | 모델 세우기, dig·Wireshark 로 엿보기, 장난감 구현(Evans). |
| 자기 이해 점검 | 의심스러운 가설을 빨리 버린다(von Mayrhauser & Vans 1995). 국소 추측을 경계한다(Letovsky & Soloway). | 혼란의 종류를 가른다(Hermans). 모델이 깨진 순간을 붙든다(Evans). 첫 해석에서 멈추지 않는다(*How People Learn*). |
| 지식의 조직 | 문법 순서가 아니라 목표 ↔ 코드 대응과 패턴(Fix 1993). | 표면이 아니라 원리(Chi). 조건이 붙은 지식(*How People Learn*). |
| 사람이 옮기는 암묵지 | 이론은 문서에 없다(Naur). 안내자와 멘토(Dagenais). | 잘하는 사람의 정보는 책에 압축되지 않는다(Luu). 전문가와 함께 일하기(Norvig). |
| 피드백 빠른 환경 | 첫 주에 커밋, 잦은 진행 확인(Dagenais). 테스트로 즉시 피드백(Feathers). | 실험은 싸고 결과가 없다(Evans). 타당한 환경과 연습 기회(Kahneman & Klein). |

### 갈리는 지점

| 축 | 레포 | 기술 | 갈리는 이유 (해석) |
|---|---|---|---|
| 주된 위험 | 너무 좁게 읽어 멀리 있는 상호작용을 놓친다(Letovsky & Soloway 1986, Littman 1987 요약). | 옛 지식이 새 것에 잘못 대응된다(Shrestha 2020, Hermans 2022). | 레포는 남이 만든 특정 인공물이라 아는 것이 거의 없고, 기술은 이미 아는 체계와 겹치는 새 체계다. 한쪽은 정보 부족, 다른 쪽은 정보 오염이 문제다. |
| 위험에 대한 대책 | 체계적 확인, 특성화 테스트, 이력과 사람에게 "왜" 묻기. | 대응이 깨지는 지점 목록(치트 시트), 개념 먼저, 원전 읽기. | 위와 같다. |
| 답이 있는 곳 | "왜 이렇게 했나"는 문서에 없고 이력과 사람에게 있다(LaToza & Myers 2010, Naur 1985). | 스펙·문서·예제에 대체로 있다(Evans 의 RFC, Robillard 의 문서). 없을 때 가장 큰 장애가 된다(Robillard). | 레포의 이론은 그 팀 안에서만 만들어졌고 기록되지 않았다. 기술은 여러 사람이 쓰라고 만든 것이라 설명이 존재한다. |
| 이해의 완성도 | 부분 이해로 충분하다. "제품의 5% 를 알지만 버그가 나면 어디를 볼지 안다"(Dagenais 의 P17). | 임계 개념은 넘기 전까지 조각난 이해에 머문다(Land 외 2005). 개념이 장기 기억에 없으면 반복이 소용없다(Hermans). | 레포 이해는 과제 단위로 소비되고, 기술 이해는 누적돼 다음 과제에 옮겨진다. |
| 시간의 쓰임 | 시니어는 같은 도메인의 반복으로 이해 시간이 준다(Xia 2018). | 전문가는 도움이 필요 없다고들 여기지만, Norvig 조차 C++ 에서 "늘 길을 잃었다"(Shrestha 외 2020 서두의 인터뷰). 16년이 "정상"이다(Evans). | 레포는 도메인 스키마가 재사용되고, 새 기술은 스키마 자체를 새로 짓는다. |

## 출처가 서로 어긋나는 지점

**체계적으로 읽을 것인가, 필요한 만큼만 읽을 것인가.** Littman 외 1987(요약으로 확인)은 체계적 전략을 쓴 사람만 수정에 성공했다고 했다. Koenemann & Robertson 1991 은 전문가 누구도 체계적으로 읽지 않았고, 필요한 만큼 전략으로 대체로 잘했다고 했다.

Koenemann 은 차이를 "우리 프로그램이 훨씬 컸다"로 설명하고, 필요한 만큼 전략이 상호작용을 놓치는 문제는 그대로 인정한다. 억지로 합치지 않는다. 확인된 범위에서 말할 수 있는 것은, 크기가 커지면 체계적 읽기가 불가능해지고 놓친 상호작용을 잡는 별도 장치(테스트, 확인 질문)가 필요하다는 것까지다.

**언어를 여러 개 배우는 것.** Norvig 은 패러다임이 다른 언어 여섯 개를 배우라고 한다. Luu 는 "Python 과 Ruby 입문서를 떼는 것은 아무 쓸모가 없었고, 특정 분야(알고리즘·네트워킹)를 배우는 편이 훨씬 나았을 것"이라고 한다. 둘 다 실무자 의견이다.

해석: Hermans 는 가까운 언어(C# → Java)는 거의 공짜지만 먼 언어는 음의 전이를 동반한다고 한다. 두 의견을 가르는 변수가 "얼마나 다른 언어를, 얼마나 깊이 배우는가"일 수 있다.

**"두려워 말고 만져 보라"는 조언.** Evans, Kerr, Dagenais 는 이른 실험을 권한다. Hermans 는 이 조언이 초보자에게는 해롭다고 비판하고, Sweller 1988 은 초보자의 문제 풀이가 스키마 획득을 방해한다는 실증을 댄다.

Hermans 자신이 "전문성 역전 효과"로 조정한다: 전문가에게는 통하고 초보자에게는 안 통한다. Dagenais 의 신입 중에도 도메인과 패러다임을 전혀 모르던 P6 에게는 강의가 맞았다. 어긋남이 아니라 조건부로 읽히지만, 그 조건(얼마나 알아야 실험이 통하는가)을 실증한 출처는 못 찾았다.

**무엇을 먼저 세우는가.** Brooks(von Mayrhauser 요약)는 위에서 아래로 가설을, Pennington 1987 은 제어 흐름 수준의 프로그램 모델을 먼저 세운다고 했다.

von Mayrhauser & Vans 1995·1997 은 셋 사이를 오간다는 통합 모델을 내놓았다. 1997년 관찰에서는 코드 경험이 없으면 프로그램 모델부터, 도메인 지식이 있으면 위에서 아래로 시작했다. 과제와 사전 지식에 따라 달라진다는 쪽으로 수렴하지만, 초기 모델들은 서로 다른 주장으로 출발했다.

## 출처 목록

### 확인한 출처

| 출처 | 근거 종류 | 비고 |
|---|---|---|
| Koenemann & Robertson, 1991, Expert Problem Solving Strategies for Program Comprehension (CHI), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/koenemann-1991.pdf | 실증 | 미러(Kent State 강의 페이지) |
| Sillito, Murphy, De Volder, 2006, Questions Programmers Ask During Software Evolution Tasks (FSE), https://www.cs.ubc.ca/~murphy/papers/other/asking-answering-fse06.pdf | 실증 | 저자 공개본 |
| Ko, Myers, Coblenz, Aung, 2006, An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks (TSE), https://www.cs.cmu.edu/~NatProg/papers/Ko2006SeekRelateCollect.pdf | 실증 | 저자 공개본 |
| Xia, Bao, Lo, Xing, Hassan, Li, 2018, Measuring Program Comprehension: A Large-Scale Field Study with Professionals (TSE), https://baolingfeng.github.io/papers/tsecomprehension.pdf | 실증 | 저자 공개본 |
| LaToza & Myers, 2010, Hard-to-Answer Questions about Code (PLATEAU), https://ecs.wgtn.ac.nz/foswiki/pub/Events/PLATEAU/2010Program/plateau10-latoza.pdf | 실증 | 워크숍 공식 페이지 |
| Dagenais, Ossher, Bellamy, Robillard, de Vries, 2010, Moving into a New Software Project Landscape (ICSE), https://www.cs.mcgill.ca/~martin/papers/icse2010.pdf | 실증 | 저자 공개본 |
| Begel & Simon, 2008, Novice Software Developers, All Over Again (ICER), https://andrewbegel.com/papers/icer-begel-2008.pdf | 실증 | 저자 공개본 |
| Fix, Wiedenbeck, Scholtz, 1993, Mental Representations of Programs by Novices and Experts (INTERCHI), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/Fix,%20Wiedenbeck,%20Scholtz%20-%20Mental%20representations%20of%20programs.pdf | 실증 | 미러 |
| Vessey, 1985, Expertise in Debugging Computer Programs: A Process Analysis (IJMMS), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/vessey85.pdf | 실증 | 미러 |
| Letovsky & Soloway, 1986, Delocalized Plans and Program Comprehension (IEEE Software), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/letovsky-1986-software.pdf | 실증 | 미러. 지시 목록의 Letovsky 1987 대신 확인된 것 |
| Pennington, 1987, Stimulus Structures and Mental Representations in Expert Comprehension of Computer Programs (Cognitive Psychology), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/pennington87.pdf | 실증 | 미러 |
| von Mayrhauser & Vans, 1995, Program Comprehension During Software Maintenance and Evolution (IEEE Computer), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/von_mayrhauser-1995.pdf | 이론(통합 모델, 앞선 모델 요약) | 미러 |
| von Mayrhauser & Vans, 1997, Program Understanding Behavior During Debugging of Large Scale Software (ESP), https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/von_mayrhauser97.pdf | 실증 | 미러 |
| Storey, 2005, Theories, Methods and Tools in Program Comprehension: Past, Present and Future (IWPC), https://www.ptidej.net/courses/inf6306/fall10/slides/course8/Storey06-TheoriesMethodsToolsProgramComprehension.pdf | 이론(개관) | 미러. Littman·Letovsky·Vessey·Détienne 요약의 출처 |
| Naur, 1985, Programming as Theory Building, https://gwern.net/doc/cs/algorithm/1985-naur.pdf | 이론 | 미러(OCR 본). pages.cs.wisc.edu 판은 텍스트 없는 스캔 |
| Feathers, 2002, Working Effectively With Legacy Code (Object Mentor 원고), http://www.accorsi.net/docs/WorkingEffectivelyWithLegacyCode.pdf | 실무자 의견 | 미러. objectmentor.com 원 링크는 죽음 |
| Spinellis, 2003, Code Reading: The Open Source Perspective, 저자 사이트의 소개·뒤표지, https://www.spinellis.gr/codereading/ , https://www.spinellis.gr/codereading/intro.html | 실무자 의견 | 책 본문은 미확인 |
| Shrestha, Botta, Barik, Parnin, 2020, Here We Go Again: Why Is It Difficult for Developers to Learn Another Programming Language? (ICSE), https://www.microsoft.com/en-us/research/wp-content/uploads/2020/05/herewegoagain_icse2020.pdf | 실증 | 저자 소속 기관 공개본 |
| Robillard & DeLine, 2011, A Field Study of API Learning Obstacles (ESE), https://www.cs.mcgill.ca/~martin/papers/ese2011.pdf | 실증 | 저자 공개본 |
| Chi, 1993, Experts' vs. Novices' Knowledge (Citation Classic, Chi·Feltovich·Glaser 1981 회고), https://garfield.library.upenn.edu/classics1993/A1993LZ47400001.pdf | 실증(저자 회고) | 1981 원문 대신 |
| Bransford, Brown, Cocking (eds.), 2000, How People Learn, 2장 How Experts Differ from Novices, https://www.nationalacademies.org/read/9853/chapter/5 | 이론(연구 종합) | 공식 공개본 |
| 같은 책 3장 Learning and Transfer, https://www.nationalacademies.org/read/9853/chapter/6 | 이론(연구 종합) | 공식 공개본 |
| Hatano & Inagaki, 1986, Two Courses of Expertise, https://eprints.lib.hokudai.ac.jp/dspace/bitstream/2115/25206/1/6_P27-36.pdf | 이론 | 홋카이도대 기관 저장소 |
| Land, Cousin, Meyer, Davies, 2005, Threshold Concepts and Troublesome Knowledge (3): Implications for Course Design and Evaluation, https://www.ee.ucl.ac.uk/~mflanaga/ISL04-pp53-64-Land-et-al.pdf | 이론 | Meyer & Land 2003 대신 |
| Sweller, 1988, Cognitive Load During Problem Solving: Effects on Learning (Cognitive Science, DOI 10.1207/s15516709cog1202_4), https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/Cognitive%20Load%20during%20problem%20solving.pdf | 실증·이론 | 미러. Wiley 원문은 403 |
| Kahneman & Klein, 2009, Conditions for Intuitive Expertise: A Failure to Disagree (American Psychologist), https://www.hansfagt.dk/Kahneman_and_Klein(2009).pdf | 이론 | 미러 |
| Keshav, 2007, How to Read a Paper (SIGCOMM CCR), https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf | 실무자 의견 | 미러 |
| Norvig, Teach Yourself Programming in Ten Years, https://norvig.com/21-days.html | 실무자 의견 | 저자 사이트 |
| Matuschak, 2019, Why Books Don't Work, https://andymatuschak.org/books/ | 실무자 의견 | 저자 사이트 |
| Luu, How I Learned to Program, https://danluu.com/learning-to-program/ | 실무자 의견 | 저자 사이트 |
| Luu, 95%-ile Isn't That Good, https://danluu.com/p95-skill/ | 실무자 의견 | 저자 사이트 |
| Luu, What to Learn, https://danluu.com/learn-what/ | 실무자 의견 | 저자 사이트 |
| Evans, 2023, New Talk: Learning DNS in 10 Years (본인 강연 전사), https://jvns.ca/blog/2023/05/08/new-talk-learning-dns-in-10-years/ | 실무자 의견 | 저자 사이트 |
| Evans, 2014, On Reading the Source Code, Not the Docs, https://jvns.ca/blog/2014/12/29/on-reading-the-source-code-not-the-docs/ | 실무자 의견 | 저자 사이트 |
| Evans, So You Want to Be a Wizard (강연 전사), https://jvns.ca/blog/so-you-want-to-be-a-wizard/ | 실무자 의견 | 저자 사이트 |
| Evans, 2022, Some Ways to Get Better at Debugging, https://jvns.ca/blog/2022/08/30/a-way-to-categorize-debugging-skills/ | 실무자 의견 | 저자 사이트 |
| Evans, How to Ask Good Questions, https://jvns.ca/blog/good-questions/ | 실무자 의견 | 저자 사이트 |
| Kerr, 2025, We Learn Systems by Changing Them, https://www.honeycomb.io/blog/learn-systems-by-changing | 실무자 의견 | 저자가 직접 쓴 회사 블로그 |
| Hermans, 2022, The Programmer's Brain (QCon 강연 전사), https://www.infoq.com/presentations/reading-code/ | 실무자 의견(연구자 강연) | 책 대신 |
| Beck, 2022, Add Comment, https://newsletter.kentbeck.com/p/add-comment | 실무자 의견 | 첫 문장만 공개, 나머지는 유료 |
| Burkhardt, Détienne, Wiedenbeck, Object-Oriented Program Comprehension: Effect of Expertise, Task and Phase, https://arxiv.org/abs/cs/0612004 | 실증 | 초록만 확인 |

### 미확인 출처

| 출처 | 왜 못 열었나 | 어떻게 다뤘나 |
|---|---|---|
| Roehm, Tiarks, Koschke, Maalej, 2012, How Do Professional Developers Comprehend Software? (ICSE) | 유료. Unpaywall·Semantic Scholar 모두 공개본 없음 | 근거로 쓰지 않음 |
| Maalej, Tiarks, Roehm, Koschke, 2014, On the Comprehension of Program Comprehension (TOSEM) | 유료 | 근거로 쓰지 않음 |
| Littman, Pinto, Letovsky, Soloway, 1987, Mental Models and Software Maintenance (JSS) | 유료 | Storey 2005 와 Koenemann 1991 의 요약을 그 출처 이름으로 인용 |
| Letovsky, 1987, Cognitive Processes in Program Comprehension (JSS) | 유료 | 같은 저자의 1986 IEEE Software 논문과 Storey 의 요약으로 대신 |
| Brooks, 1983, Towards a Theory of the Comprehension of Computer Programs | 유료. 열린 PDF 는 텍스트 없는 스캔 | von Mayrhauser & Vans 1995 와 Storey 2005 의 요약으로 언급 |
| Soloway & Ehrlich, 1984, Empirical Studies of Programming Knowledge (TSE) | 열린 두 PDF 모두 텍스트 없는 스캔 | 근거로 쓰지 않음 |
| Chi, Feltovich, Glaser, 1981, Categorization and Representation of Physics Problems by Experts and Novices | Wiley 403 | Chi 1993 회고와 How People Learn 으로 대신 |
| Glaser & Chi, 1988, Overview (The Nature of Expertise) | 텍스트 없는 스캔 | 근거로 쓰지 않음 |
| Meyer & Land, 2003, Threshold Concepts and Troublesome Knowledge: Linkages to Ways of Thinking and Practising (ETL Report 4) | 알려진 링크 넷 모두 죽음 | Land 외 2005 로 대신 |
| Adelson, 1981, Problem Solving and the Development of Abstract Categories in Programming Languages | Springer 봇 차단, 초록도 못 얻음 | 근거로 쓰지 않음 |
| Scholtz & Wiedenbeck, 1990, Learning Second and Subsequent Programming Languages: A Problem of Transfer | 유료 | 근거로 쓰지 않음 |
| Hermans, 2021, The Programmer's Brain (책) | 유료 책 | 저자 강연 전사로 대신 |
| Spinellis, 2003, Code Reading (책 본문) | 유료 책 | 저자 사이트의 소개·뒤표지만 |
| Feathers, 2004, Working Effectively with Legacy Code (책) | 유료 책 | 2002 원고로 대신 |
| Beck, 2022, Add Comment 본문 | 유료 | 공개된 첫 문장만 |
| Willison, "낯선 코드베이스" 관련 본인 글 | 검색으로 찾지 못함 | 뺌 |
| Ericsson 외 1993(의도적 연습), Bransford & Schwartz 1999(전이 재고) | 열지 않음 | Norvig 과 How People Learn 이 인용한 내용만 그들 이름으로 언급 |
