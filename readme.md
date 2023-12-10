#### 데이터 전후처리 시범
   * [Wisconsin Breast Cancer](https://github.com/yuninze/pub/blob/main/notebook82dfb5c7b4.ipynb)
     * 유방 신생조직의 physical parameters가 endpoint인 데이터셋 전처리 시범
   * [CYP-GUIDES](https://github.com/yuninze/pub/blob/main/notebook44f7ceb7b9.ipynb)
     * MDD 관련 약물과 days-to-readmission가 endpoint인 데이터셋 전처리 시범
   * [UC Irvine Parkinson's Disease](https://github.com/yuninze/pub/blob/main/notebook9846d2c254.ipynb)
     * 파킨슨병 관련 longitudinal parameters과 UPDRS가 endpoint인 데이터셋 전처리 시범
   * [Clinical Manual Query](https://github.com/yuninze/pub/blob/main/ct/dmc.ipynb)
        * 상용 CDMS의 데이터셋을 바탕으로 py2sas(saspy), SAS, SQL을 통해 SAE listing 및 Clinical Querying

#### 기타
* da
    * [경제 데이터 확인](https://github.com/yuninze/pub/blob/main/da/fin.ipynb)
        * API로 정형 데이터를 획득, 업데이트, 저장 및 수반 전후처리 수행
        * EDA 수행, K-Folding Ridge로 주요 지표의 예측값 산출
* etl
    * SQL(sqlite3) 연습, 프로젝트 참여자 회계용 스프레드시트 전처리 스크립트

* bl
    * 붙여넣기한 데이터를 특정 형태로 Google Sheets에 올리는 스크립트
    * 나열된 명사를 Tf-Idf, Bagging, XGBoost로 분류하는 스크립트

* deprecated
    * CSV/JSON 변환, 기정 규칙에 따른 데이터 무결성 확인, 중복/불량 데이터 확인, 정형 데이터 전후처리 스크립트
    * 이미지의 무작위 지점에 무작위 크기의 이미지를 붙인 이미지 생성하는 스크립트
    * 화면 구간을 지속적으로 캡처하고 캡처 내 텍스트를 추출/저장하는 스크립트
    * 멀티트레딩 사용 blob 스크래퍼
