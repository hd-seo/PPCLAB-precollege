# PPCLAB-precollege
# 💊 약물 상담 시뮬레이션: 숨겨진 단서를 찾아라!

**강원대학교 약학대학 Pre-College 프로그램 교육 자료**

## 📌 개요 (Overview)

본 프로젝트는 강원대학교 약학대학 연구실(머신러닝 및 데이터 분석 기반 임상약학 연구)에서 강원도 내 고등학생들을 위해 개발한 인터랙티브 약물 상담 시뮬레이션입니다. "Pre-College 프로그램"의 일환으로, 학생들이 약사의 중요한 업무 중 하나인 **안전한 약물 상담** 과정을 체험하고, 이 과정이 어떻게 **데이터 기반 의사결정** 및 **머신러닝(기계학습)**의 원리와 연결될 수 있는지 간접적으로 경험하도록 설계되었습니다.

학생들은 가상의 환자 시나리오를 통해 약사가 되어, 환자에게 적절한 질문을 던지고 숨겨진 단서(위험 요인)를 찾아내어 안전한 약물 사용 결정을 내리는 과정을 체험합니다.

## ✨ 시뮬레이션 특징 (Features)

* **Streamlit 기반 인터랙티브 웹 애플리케이션:** 별도의 프로그램 설치 없이 웹 브라우저를 통해 쉽게 접근하고 실행할 수 있습니다.
* **현실적인 환자 상담 시나리오:**
    * 두통을 호소하는 환자가 방문합니다.
    * 환자는 플레이어가 처음에는 알 수 없는 숨겨진 위험 요인(예: 특정 약물 복용, 예정된 시술)을 가지고 있습니다.
* **사용자 주도적 정보 수집:**
    * 학생(플레이어)이 직접 환자에게 할 질문을 선택합니다.
    * 선택한 질문에 따라 환자로부터 다양한 정보를 얻게 되며, 이는 결과에 큰 영향을 미칩니다.
* **의사결정나무(Decision Tree) 원리 체험:**
    * 각각의 질문과 답변은 의사결정나무의 가지처럼 다음 단계를 결정합니다.
    * 어떤 정보를 먼저 확인하고, 어떻게 판단하는지에 따라 최종 결과(환자의 안전)가 달라집니다.
* **즉각적인 피드백 및 점수 시스템:**
    * '안전 상담 점수'를 통해 자신의 선택이 얼마나 안전했는지 직관적으로 알 수 있습니다.
    * 선택에 따른 결과(성공, 주의, 위험 상황 등)가 즉시 제공됩니다.
* **반복 학습 및 힌트 시스템:**
    * 첫 플레이에서 중요한 정보를 놓쳤을 경우, 다음 플레이 시 관련 질문의 중요성을 알려주는 힌트가 제공됩니다. (머신러닝 모델이 데이터를 통해 '학습'하고 성능을 개선하는 과정에 비유)

## 🚀 실행 방법 (How to Run / Access)

* **웹에서 바로 실행:**
    * 본 시뮬레이션은 Streamlit Community Cloud를 통해 배포되어, 제공된 URL을 통해 웹 브라우저에서 바로 접속하여 체험할 수 있습니다.

* **로컬 환경에서 실행 (개발자용):**
    1.  이 GitHub 저장소를 클론(`git clone`)하거나 다운로드합니다.
    2.  프로젝트 폴더로 이동합니다.
    3.  필요한 라이브러리를 설치합니다: `pip install -r requirements.txt`
    4.  터미널에서 다음 명령어를 실행합니다: `streamlit run app.py`

## 🎯 학습 목표 및 기대 효과 (Learning Objectives)

* **정보의 중요성 인지:** 안전한 약물 사용을 위해 환자로부터 정확하고 충분한 정보를 얻는 것의 중요성을 깨닫습니다.
* **의사결정 과정 체험:** 제한된 정보 속에서 최선의 결정을 내리기 위한 논리적 사고 과정을 경험합니다.
* **머신러닝 기초 원리 이해:**
    * 데이터(환자 정보)를 기반으로 규칙을 만들고 예측(안전한 약물 선택)하는 과정을 통해 의사결정나무 등 머신러닝의 기본 개념을 직관적으로 이해합니다.
    * 반복적인 시뮬레이션과 피드백을 통해 '학습'하고 더 나은 결정을 내리는 과정이 머신러닝 모델의 학습 과정과 유사함을 체험합니다.
* **분야 흥미 유발:** 약학, 데이터 과학, 인공지능 분야에 대한 학생들의 관심과 흥미를 높입니다.

## 🔗 머신러닝과의 연결 (Connection to Machine Learning)

이 시뮬레이션은 다음과 같은 측면에서 머신러닝, 특히 **의사결정나무(Decision Tree)** 모델과 연결됩니다.

1.  **질문 = 특징(Feature) 선택:** 약사가 환자에게 하는 각 질문은 머신러닝 모델이 예측을 위해 사용하는 데이터의 '특징(feature)'과 유사합니다. 어떤 질문을 하느냐(어떤 특징을 사용하느냐)에 따라 결과가 달라집니다.
2.  **답변 = 특징 값(Feature Value) & 분기:** 환자의 답변은 특정 특징의 '값'에 해당하며, 이 값에 따라 의사결정나무의 다음 '가지(branch)'로 이동하듯 상담의 다음 단계가 결정됩니다.
3.  **결정 규칙 학습:** 플레이어가 여러 번 시뮬레이션을 반복하고 힌트를 통해 개선해나가는 과정은, 머신러닝 모델이 많은 데이터를 통해 "어떤 질문(특징)을 어떤 순서로 고려해야 최적의 결과(예측)를 얻을 수 있는지"에 대한 '결정 규칙'을 학습하는 과정과 유사합니다.
4.  **숨겨진 위험 = 예측 오류:** 중요한 질문을 놓쳐 환자의 숨겨진 위험 요인을 파악하지 못하고 잘못된 약물을 추천하는 것은, 모델이 중요한 특징을 간과하여 예측 오류를 범하는 것과 비슷합니다. "알 수 없는 이유로 환자가 위험에 빠졌다"는 결과는 데이터 부족 또는 잘못된 특징 선택으로 인한 모델의 실패를 상징적으로 보여줍니다.

본 시뮬레이션을 통해 학생들은 복잡한 데이터를 분석하고, 그 안에서 패턴을 찾아 최적의 의사결정을 내리는 머신러닝의 핵심 아이디어를 재미있게 체험할 수 있습니다.

## 🛠️ 사용된 기술 (Tech Stack)

* Python
* Streamlit

## 👨‍🔬 만든 사람들 (Credits)

* 강원대학교 약학대학 맞춤형 약료학 연구실 서현덕
    * 본 프로그램은 강원대학교 약학대학의 Pre-College 프로그램의 일환으로 제작되었습니다.






## 📄 라이선스 (License)

This project is licensed under the MIT License.
Copyright (c) 2024 [강원대학교 약학대학 맞춤형 약료학 연구실]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
