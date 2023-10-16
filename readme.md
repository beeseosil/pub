#### 임상 데이터 관련
   * [CYP-GUIDES](https://github.com/yuninze/pub/blob/main/notebook44f7ceb7b9.ipynb)
     * MDD 관련 약물과 days-to-readmission가 endpoint인 시험의 데이터셋 전처리 시범
   * [PD Dataset](https://github.com/yuninze/pub/blob/main/notebook9846d2c254.ipynb)
     * 파킨슨병 관련 임상 parameter과 UPDRS가 endpoint인 시험의 데이터셋 전처리 시범
   * [Clinical Manual Query](https://github.com/yuninze/pub/blob/main/ct/dmc.ipynb)
        * cubeCDMS 데모 sas7bdat을 바탕으로 py2sas(saspy), SAS, SQL을 통해 SAE Reconciliation Listing 및 Clinical Manual Querying
   * [임상시험 데이터셋 확인 3](https://github.com/yuninze/pub/blob/main/ct/dmb.ipynb)
        * LB 등 일부 도메인을 SDTM-like로 바꾸는 후처리
   * [임상시험 데이터셋 확인 2](https://github.com/yuninze/pub/blob/main/ct/dma.ipynb)
        * SDTM 매핑 테이블을 데이터 스펙 클래스로 두고 CRF의 속성 확인 및 edit check
   * [임상시험 데이터셋 확인 1](https://github.com/yuninze/pub/blob/main/ct/dm.ipynb)
        * CRF Item 구조를 확인하고 모의 LB 데이터 생성

#### 기타
* da
    * [경제 데이터 확인](https://github.com/yuninze/pub/blob/main/da/fin.ipynb)
        * API로 정형 데이터를 획득, 업데이트, 저장 및 수반 전후처리 수행
        * EDA 수행, K-Folding Ridge로 주요 지표의 예측값 산출
* etl
    * SQL(sqlite3) 연습용 스크립트
    * 프로젝트 참여자 회계용 스프레드시트 전처리 스크립트

* bl
    * 붙여넣기한 데이터를 특정 형태의 정형 데이터로 스프레드시트에 업데이트하는 스크립트
    * 명사 나열형 데이터를 Tf-Idf, Bagging, XGBoost로 자동 분류하는 스크립트

* deprecated
    * CSV/JSON 변환, 기정 규칙에 따른 데이터 무결성 확인, 중복/불량 데이터 확인, 정형 데이터 전후처리 스크립트
    * 이미지의 무작위 지점에 무작위 크기의 이미지를 붙인 이미지 생성하는 스크립트
    * 화면 구간을 지속적으로 캡처하고 캡처 내 텍스트를 추출/저장하는 스크립트
    * 멀티트레딩 사용 blob 스크래퍼

#### 계획
* [React:Next.js 공부](https://github.com/yuninze/yeonsup/tree/master/web/nxtjs)
* MedDRA, WHODRUG:ATC 등 나열 명사들의 auto-encoding
