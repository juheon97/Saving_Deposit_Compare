![logo](/uploads/7228566721541314e7251348ae568a19/logo.png)

## 📑 프로젝트 주제 및 기간

- 예금 적금 비교 및 상품 추천
- 2024-11-18 ~ 2024-11-26

## 🕹️ 프로젝트 주요 기능

- 전체 상품 조회
- 나라별 환율 계산기
- 추천 상품 (나이대 별 가장 많이 선택된 top 3 상품)
- KaKao Map API 은행 위치 및 정보 제공
- AI Chat Bot 과 기본 옵션 대답
- 커뮤니티 CRUD 기능
- 유저가 담은 상품 예금 적금 상품의 이자 및 수익 계산
- 비밀번호 찾기 및 임시 비밀번호 생성  

## 💻 팀원

- 송주헌
- 조혜정


## 📺 개발환경


- <img src="https://img.shields.io/badge/Framework-%23121011?style=for-the-badge">![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
- <img src="https://img.shields.io/badge/Language-%23121011?style=for-the-badge">![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


## 🎋 ERD

![ERD](/uploads/739706989c6fb164bd281029b106fe2f/ERD.PNG)

## 🛍️ 프로젝트 폴더 구조

# 프로젝트 구조



```bash
Frontend
src/
├── assets/            # 이미지, 스타일 등 정적 파일
├── router/            # Vue Router 설정
├── store/             # Vuex store
├── components/        # 공통 컴포넌트
└── views/             # 페이지 컴포넌트
    ├── SearchView/
    ├── SignupView/
    ├── RecommendView/
    ├── ProfileView/
    ├── password.vue
    ├── MainView/
    ├── MapView/
    ├── LoginView/
    ├── HomeView/
    ├── FindPasswordView/
    └── ExchangeView/
Backend
bashCopy├── accounts/          # 사용자 계정 관리
├── boards/            # 게시판 관리
├── deposit_saving_apps/  # 예금/적금 관리
└── exchanges/          

```

# 💼 기능 상세 설명

### 환율 계산기

![환율계산](/uploads/231c8d8f13cc454f2023e9fd4fb921e8/환율계산.gif)

- 나라별로 계산하기 버튼이 있습니다
- 전체 나라 보기 후 나라들을 선택하여 계산 할 수 있습니다.

### 프로필 부분

![프로필이미지변경](/uploads/6a4e7776eb015f2ac8a8997dea5be4ad/프로필이미지변경.gif)

- 로컬 컴퓨터에서 파일을 선택 하면 프로필 이미지가 변경됩니다.

![정보수정](/uploads/4150f6def6284afbc65a4413fee3782d/정보수정.gif)
- 유저의 정보 및 적금 예금 수를 수정 할 수 있습니다.
- 적금 예금의 금액은 입력칸 및에 적힌 금액만큼 수정 할 수 있습니다

![적예금계산](/uploads/675d2e3bec4635b9f3aa7c5fb0a302e4/적예금계산.gif)

- 유저가 담은 상품 리스트의 상세 페이지를 볼 수 있습니다
- 상세보기에서는 우대 및 기본 금리가 적혀있습니다
- 아래 달리기 버튼을 누르면 해당 상품 금리를 유저가 적은 적금 예금 수치에 맞게 계산해줍니다.

![비밀번호변경2](/uploads/4bec862a5c31f1f3d879a7e4418ba90f/비밀번호변경2.gif)

- 유저가 비밀번호를 수정 할 수 있습니다.
- 현재 비밀 번호, 변경된 비밀 번호가 틀릴 시 상황에 맞는 에러메시지가 나옵니다.
- 변경 후에는 로그아웃 처리가 됩니다.

### 조회

![조회_로그인_비로그인_차이](/uploads/39a903e6dbf6fe3cf358fb82f172a20c/조회_로그인_비로그인_차이.gif)

- 조회 페이지엔 전체, 적금, 예금 상품을 필터하여 찾아 볼 수 있습니다
- 또한 가입 방법 필터가 있습니다
- 상세보기 시 해당 우대 및 기본 금리의 차이를 보여주는 그래프가 나옵니다
- 비교 버튼 누를 시 최대 4개까지 선택하여 해당 상품들의 정보를 볼 수 있습니다

### 추천 알고리즘

![추천알고리즘](/uploads/cfdc8ecb788e183b592f7598be4613fb/추천알고리즘.gif)

- 각 유저별 나이를 베이스로 가장 많이 선택된 상품 top 3가 나옵니다
- 하단에 각 유저별 나이를 베이스로 각 상품의 카운트 된 횟 수가 나옵니다.

### 챗봇 

![챗봇](/uploads/c4ca2b6233633998ba5b6238feba0e1b/챗봇.gif)

- 챗봇 기능을 구현하였습니다.
- 유저가 챗봇을 통해서 다양한 정보를 물어볼 수 잇습니다.

### 커뮤니티

![커뮤니티](/uploads/e6388a6504cdbc3fae7f89d85f372735/커뮤니티.gif)

- 유저들이 직접 게시글을 등록할 수 있습니다.
- 기본적인 CRUD 기능을 구현하였습니다
- 각 게시물에 댓글을 달 수 있고, 댓글 및 게시글의 좋아요를 할 수 있습니다

### 지도

![지도구현](/uploads/faa2df1d6487fec6d1e77e9afce7afb6/지도구현.gif)

- 한국에 있는 은행들을 검색 할 수 있는 지도를 구현하였습니다
- API는 KAKAO MAP API를 사용하였습니다
- 검색 진행 시 하단에 해당 은행 리스트가 나오고 해당 은행 클릭 시 지도가 동적으로 움직입니다.

### 비밀번호 찾기

![비밀번호찾기](/uploads/79970be5f4aea06f4564594679f630f2/비밀번호찾기.gif)

- 유저의 아이디와 이메일을 사용하여 임시 비밀 번호를 부여해줍니다.
- 아이디는 중복해서 생성 할 수 없게하여 기능을 구현하였습니다.
