import time
import torch
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

# --- 상수 정의 ---
PREDICTION_INTERVAL_SECONDS = 10  # 10초 - 테스트 / 2분 - 실제
RETRAIN_INTERVAL_SECONDS = 6 * 3600 # 6시간

def main():
    print("This is LTPM!!!")

    while True:
        print("--- LTPM Phase 2 시작 ---")
        print("- Fast Loop: 실시간 예측 & 스케일링 -")
        # 1. Prometheus에서 RPS 값 수집

        # 2. 데이터 전처리 과정
        ## 1단계: 데이터 재구성
        ## 2단계: 리샘플링 및 결측치 처리
        ## 3단계: 시간 특징(Feature) 생성
        ## 4단계: 데이터 정규화 (StandardScaler)

        # 3. N분 뒤, 함수 호출량 예측
        ## 입력 준비
        ## 예측 수행
        ## De-normalization

        # 4. 적절한 함수 인스턴스 수 계산
        ## 함수 인스턴스 수(N) 계산

        # 5. 함수 인스턴스 수(Pod) 조절
        ## 계산된 N과 현재 Replicas 비교
        ## 다르다면, Replicas를 N으로 조정

        print("- Slow Loop: 점진적 학습 -")
        # 주기마다 모델 재학습

        print("--- LTPM Phase 2 종료 ---")
        time.sleep(PREDICTION_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
