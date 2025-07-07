# H2-Ammonia Simulator

이 시뮬레이터는 연간 암모니아 목표 생산량을 기준으로 필요한 재생에너지/수전해 설비 용량을 산정하고,
CAPEX, OPEX, LCOA (암모니아 생산단가)를 계산합니다.

## 주요 기능

- 태양광, 풍력, ESS, 수소탱크 조건 입력
- 그리드 전력 또는 재생에너지 기반 선택 가능
- 연간 10만톤 암모니아 기준 역산
- LCOA 계산 및 시각화

## 실행 방법

```bash
streamlit run app/h2_nh3_streamlit_app.py
```
