#### 임상의학 데이터셋 관련 노트북
* [Clinical Manual Query](https://github.com/beeseosil/pub/blob/main/ct/dmc.ipynb)
	* 자원 소모가 큰 규제산업의 특성상, 임상시험 솔루션은 최소한의 입력 폼 구성에도 비교적 복잡한 정형 데이터 테이블을 여러 개 취급합니다. 이 노트북에서는 상용 임상시험 데이터 입력 플랫폼(CDMS)의 SAS 데이터셋을 SQL, saspy, SAS로 전처리, SAE listing 및 clinical context을 고려해 querying 합니다.

* [Trial 175](https://github.com/beeseosil/pub/blob/main/notebook4407d644ef.ipynb)
	* 과거 antiretroviral 임상시험의 실제 데이터셋으로, 레지멘에 대한 사전지식을 차치하고 ToE(잔여기간) 산출하였습니다. Assuming time-to-event based on baseline data including regimens, prior symptoms, and CD4 / CD8 cell count

* [14-day Ambulatory Assessment of Depression Symptoms](https://github.com/beeseosil/pub/blob/main/notebookc2020bf0c0.ipynb)
	* Enrollment screening이 PHQ-9이며 ICD-10 기반 longitudinal 응답이 endpoint인 데이터셋 전처리를 수행했으며, 시각화만을 통해 설문 문항의 유의성을 보였습니다.

* [CYP-GUIDES](https://github.com/beeseosil/pub/blob/main/notebook44f7ceb7b9.ipynb)
	* MDD 등 Depressive Disorder 관련 약물과 days-to-readmission가 endpoint인 데이터셋 전처리를 통해 정신과 약물에 대한 사전지식을 차치하고 시각화만으로 특정 약물(군)의 상관성과 환자 악화의 상관성 도출했으며, 경험상, 이들 약물은 실제로 off-label 등 문제가 있는 약물입니다.

* [Wisconsin Breast Cancer](https://github.com/beeseosil/pub/blob/main/notebook82dfb5c7b4.ipynb)
	* 유방 신생조직의 physical parameters가 endpoint인 데이터셋 전처리입니다.

* [UC Irvine Parkinson's Disease](https://github.com/beeseosil/pub/blob/main/notebook9846d2c254.ipynb)
	* 파킨슨병 관련 longitudinal parameters과 UPDRS가 endpoint인 데이터셋 전처리를 통해 선형회귀의 유용성을 보였습니다.

* [A South Korean Dataset for an Educational Purpose](https://github.com/beeseosil/nih.go.kr/koges/blob/main/qwer.ipynb)
	* This notebook demonstrates a exhaustive preprocessing and analysis on the deidentificated dataset with high-level healthcare topics (e.g. drink history)
 
