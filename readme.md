## Project-specific Scripts
### 레포 소개
* ct
   * [임상시험 데이터셋 (sas7bdat) 톺아보기](https://github.com/yuninze/pub/blob/main/ct/dm.ipynb)
   * [임상시험 데이터셋 DB Specification 톺아보기, mapper 내기](https://github.com/yuninze/pub/blob/main/ct/dma.ipynb)

* da
    * [경제 데이터 보기](https://github.com/yuninze/pub/blob/main/da/fin.ipynb)
    * API로 지정한 데이터를 받고, 결합, 업데이트, 보간 등 전처리하는 스크립트
    * 시계열 데이터 확인을 위한 래퍼와 Streamlit 대시보드 스크립트
    * Random Forest Regressor로 ICSA, Corporate Yield Spread로 전월 NFP 계산

* deprecated
    * CSV/JSON 변환, 기정 규칙에 따른 데이터 무결성 확인, 중복/불량 데이터 확인, tabular data 형태 변환 스크립트
    * 이미지의 무작위 지점에 무작위 크기의 이미지를 붙인 이미지 생성하는 스크립트
    * 화면 구간을 지속적으로 캡처하고 캡처 내 텍스트를 추출/저장하는 스크립트
    * 멀티트레딩 사용 blob 스크래퍼

* etl
    * SQL (sqlite3) 연습용 스크립트
    * 프로젝트 참여자 회계용 스프레드시트 전처리 스크립트

* bl
    * 붙여넣기한 데이터를 특정 형태의 tabular data로 구글 스프레드시트에 업데이트하는 스크립트
    * (실패) 명사 나열형 데이터를 Tf-Idf, Bagging, XGB (CUDA) 이용해서 자동 분류하기
      * 너무 특정적인 명사들 조합 피처가 나오지 않음 (score: 0.355)

### 향후 계획
* Free-form text 등 유의미한 단어 나열을 기정 딕셔너리 등에 따라 분류하기
