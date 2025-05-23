# 영상 색상 타임라인 시각화 (Video Color Timeline Visualization)

## 프로젝트 개요

이 프로젝트는 Python 기반 도구로, 영상의 각 프레임에서 주요 색상을 추출해 타임라인으로 시각화함으로써 영상의 전체 색상 분위기와 변화를 한눈에 보여줍니다. 영상의 색상 팔레트가 시간에 따라 어떻게 변하는지 직관적으로 파악할 수 있습니다.

---

## 주요 기능

- **Streamlit & Gradio UI 동시 지원 (adapter 패턴)**
- **프레임을 균등 간격으로 추출하고 캐싱**
- **각 프레임별 상위 N개 색상(KMeans) 및 비율 계산**
- **프레임별 리트머스 바(세로 색상 바) 시각화**
- **단일/누적 리트머스 바 모드 토글**
- **프레임 개수, 위치, 색상 개수 슬라이더 제공**
- **Gradio: 3열(프레임|리트머스|설정) 가로 배치, Streamlit: 세로 배치**
- **main.py 플랫폼 런처로 웹에서 UI 선택 실행**

---

## 사용 방법

1. **환경 준비**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # (Windows)
   pip install -r requirements.txt
   ```

2. **분석할 영상 준비**
   - UI에서 영상 파일을 업로드하세요. (권장)
   - (직접 파일을 sample 폴더에 둘 필요 없이, UI 업로드 기능을 사용하세요)

3. **실행**
   - 권장: `python main.py` 실행 후 웹에서 UI(Gradio/Streamlit) 선택
   - (view_gradio.py, view_streamlit.py 직접 실행은 개발용이며, 일반 사용자는 main.py를 이용하세요)

4. **결과 확인**
   - UI에서 프레임 이미지, 리트머스 바, 슬라이더, 모드 토글 등 기능을 직접 확인하세요.

---

## 코드 구조

- `view_gradio.py` : Gradio UI 뷰
- `view_streamlit.py` : Streamlit UI 뷰
- `main.py` : Flask 기반 UI 런처(웹에서 Gradio/Streamlit 선택)
- `model.py` : 색상 추출, 리트머스 바 생성, 프레임 추출 등 핵심 함수
- `.st_tmp_frames/` : 임시 프레임/리트머스 바 이미지 저장 폴더

---

## 참고/활용 예시

- 각 프레임별 주요 색상 타임라인, 누적/단일 리트머스 바 비교, 디버그 콘솔 활용 등
- 포트폴리오, 실전 데이터 분석, 영상 색상 트렌드 분석 등에 활용 가능

---

## 업데이트 내역
- 2025-05-23: Streamlit/Gradio 구조 싱크, 누적/단일 리트머스 모드, adapter 구조 통합 등 최신화 