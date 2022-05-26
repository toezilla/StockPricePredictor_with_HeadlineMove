# **Stock Price Predictor with HeadlineMove**

---

## 1. 프로젝트 개요

### 1.1 프로젝트 배경 및 목적
주식 투자가 자산 관리의 보편적인 수단이 되면서, 미래 주가를 예측할 수 있는지 여부가 큰 관심사가 되고 있습니다.
미래 주가를 예측하는 전통적인 2가지 기법은 다음과 같습니다.
1) 기업의 가치를 분석해 미래의 주가를 예측하는 **기본적 분석(Fundamental Analysis)**, 
2) 수요와 공급의 원칙을 바탕으로 그래프 분석을 통해 미래의 주가를 예측하는 **기술적 분석(Technical Analysis)**

하지만, 인공지능이 발달하면서 전통적으로 미래 주가에 영향을 끼치 두 가지 요인인 '기업의 가치' 와 '수요와 공급' 이외의 우리가 알지 못하는 요인을 찾아 미래 주가를 예측하고자 하는 노력이 많아지고 있습니다.
저희는 그 중, 보편적으로 많은 사람들이 미래 주식 투자를 위해 참고하는 **뉴스 기사 데이터**를 활용해 미래 주가를 예측하고자 합니다.

### 1.2 프로젝트 구성원
- 인사이트 3기 **방나모**
  - 프로젝트 리드, error correction formula 개발, 전체 코드 리펙토링
- 인사이트 4기 **강석훈**
  - 주가 데이터 수집, 주가 데이터 전처리
- 인사이트 4기 **황승현**
  - 뉴스 데이터 수집, 뉴스 데이터 전처리, LSTM 모델링/학습

### 1.3 개발 환경
| module | version |
| --- | --- |
| Python | 3.8 |
| TensorFlow | 2.3.1 |
| Gensim | 3.8.3 |
| Pandas | 1.2.0 |
| Numpy | 1.19.2 |
| FinanceDataReader | 0.9.10 |

### 1.4 디렉토리 구성

```
+--data
      +--headline
      +--train_test
      +--vector
+--model
+--scaler
      +--train_scaler
```

| directory name | description |
| --- | --- |
| headline | This directory contains all Headline data |
| train_test | This directory contains test data used to measure model performance |
| vector | This directory contains sumed 100d vectorized Headline data |
| model | This directory contains Word2Vec model and LSTM model |
| scaler | This directory contains MinMaxScaler of sklearn |



<br>

## 2. 데이터 수집
- 뉴스 데이터
  - MK 데이터
    - 데이터 양: 142750개
    - 데이터 값: 연/월/일/시간/제목
    - 수집 기간: 18.10.26 ~ 20.11.27
  - 동아 데이터
    - 데이터 양: 23841개
    - 데이터 값: 연/월/일/시간/제목
    - 수집 기간: 18.01.01 ~ 20.12.20
  - 주가 데이터
    - 데이터 양: 

<br>

## 3. 데이터 전처리
1. 기본적은 전처리
- 특수문자 제거
- 문장 분리
- 띄어쓰기
- 중복 제거

2. 토크나이저(Tokenizer)
- Kkma
- Okt

<br>

## 4. 분석 내용
### 4.1 Methodology
![image](https://user-images.githubusercontent.com/98089273/170453655-5b6d5730-09bb-45cb-a182-a9a822cdc018.png)

### 4.2 Graph of Loss
![image](https://user-images.githubusercontent.com/98089273/170456719-2225b57d-c05e-4f13-84cc-f3e70c4ad396.png)

### 4.3 Error Correction
We did error corrction. Because we do not have enough data, so model shows over 3% error when using MAPE metric.

In addition, the goal of our project is not to predict an increase or decrease, but to precisely match the stock's next day's open, high, low, and close prices.

To achieve the goal, we made an assumption that the error of the previous day and that of the next day would be similar, because they both use almost the same data, and we made a formula. The formula is as follows.
![image](https://user-images.githubusercontent.com/98089273/170455690-4c5a5374-8608-41c3-b0f0-0bc77d6ca97a.png)

As shown in the table below, after calibration, we were able to obtain better model performance.
![image](https://user-images.githubusercontent.com/98089273/170455733-3129b0e8-3445-4e07-9cf2-e1e05f547801.png)

Prediction graph after correlation
![image](https://user-images.githubusercontent.com/98089273/170457198-3b751536-c03b-4795-81fd-63481aa68b35.png)

<br>

## 5. 분석 한계점
1. 뉴스 분석 과정에서 이따금씩 해당 산업과 관련성이 없는 뉴스도 같이 발견되어 예측 정확도가 예상보다 떨어진다.
3. 주식 가격에 나타나는 급격한 변동을 잘 에측하지 못한다.
4. 통신, 반도체, 제약 세 산업군의 주가 예측에 대한 내용이므로, 다른 산업군에 일반화시키기 힘들다.

<br>


### Link of Full Report
https://lovely-polka-e0b.notion.site/9dcfb84eee464495ab735b1908b962a1
