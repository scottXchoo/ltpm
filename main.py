import time
import pandas as pd
from sklearn.preprocessing import StandardScaler


# --- 상수 정의 ---
PREDICTION_INTERVAL_SECONDS = 10  # 10초 - 테스트 / 2분 - 실제
RETRAIN_INTERVAL_SECONDS = 6 * 3600 # 6시간
LOOKBACK_WINDOW = 60 # ??

def main():
    print("This is LTPM")

    while True:
        print("--- 예측 시작 ---")
        # 1. Prometheus에서 데이터 가져오기
        # Prometheus 쿼리 결과와 유사한 가상 데이터
        mock_prometheus_response = [
            {
                'metric': {'function_name': 'printer'},
                'values': [[1721113200 + i*60, 10 + i%10 + np.random.rand()] for i in range(50)]
            },
            {
                'metric': {'function_name': 'payment-api'},
                'values': [[1721113200 + i*60, 50 + (i%20)*2 + np.random.rand()*5] for i in range(50)]
            }
        ]

        # 2. 데이터 전처리
        ## 데이터 재구성: 함수 이름을 key, 데이터프레임을 value로 하는 딕셔너리 생성
        all_func_data = {}
        for item in mock_prometheus_response:
            func_name = item['metric']['function_name']

            # Prometheus 데이터는 [타임스탬프, 값] 리스트로 제공
            df = pd.DataFrame(item['values'], columns=['time', 'rps'])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df['rps'] = pd.to_numeric(df['rps'], errors='coerce') # 변환 불가 값은 NaN으로 처리
            df = df.set_index('time')

            all_func_data[func_name] = df

        # -- 최종 데이터를 담을 리스트 ---
        all_X_samples, all_y_samples = [], []
        all_scalers = {}

        for func_name, df in all_func_data.items():
            # --- 2단계: 리샘플링 및 결측치 처리 ---
            ## 1분(1T) 간격으로 데이터 재정렬, 빈 값은 0으로 채움
            df_resampled = df.resample('1T').mean().fillna(0)

            # --- 3단계: 시간 특징(Feature) 생성 ---
            df_resampled['hour'] = df_resampled.index.hour
            df_resampled['day_of_week'] = df_resampled.index.dayofweek
            df_resampled['minute_of_hour'] = df_resampled.index.minute

            # --- 4단계: 데이터 정규화 (StandardScaler) ---
            ## 함수마다 데이터 분포가 다르므로, Scaler를 함수별로 생성하고 관리 필요
            scaler = StandardScaler() # 표준화(평균 0, 분산 1) 적용
            df_resampled['rps_scaled'] = scaler.fit_transform(df_resampled[['rps']])
            ## 정규화된 값은 rps_scaled 라는 새로운 칼럼에 저장
            all_scalers[func_name] = scaler

            # 모델에 입력할 최종 특징 선택
            features = df_resampled[['rps_scaled', 'hour', 'day_of_week', 'minute_of_hour']]

            # --- 5단계: 시퀀스 생성 (Sliding Window) ---
            X, y = [], []
            # 예측할 길이는 2분 뒤 1개의 포인트
            prediction_horizon = 1 # 모델이 한 번에 예측할 미래 시계열 데이터의 포인트 개수 (Ex. 2분 뒤 1개 값만 예측하겠다는 뜻)

            for i in range(len(features) - LOOKBACK_WINDOW - prediction_horizon + 1):
                # 과거 LOOKBACK_WINDOW 만큼의 데이터를 입력(X)으로 사용
                X.append(features.iloc[i: (i + LOOKBACK_WINDOW)].values) # iloc: 인덱스 번호로 행이나 열 선택하는 속성
                ## i번째부터 (i + LOOKBACK_WINDOW - 1)번째까지의 행을 선택하여 .values로 numpy 배열 변환

                # LOOKBACK_WINDOW 바로 다음 prediction_horizon만큼의 데이터를 정답(y)으로 사용
                y.append(features.iloc[i + LOOKBACK_WINDOW : i + LOOKBACK_WINDOW + prediction_horizon].values)

            if X and y:
                all_X_samples.extend(X)
                all_y_samples.extend(y)
        
        # --- PyTorch 텐서로 변환 ---
        X_tensor = torch.from_numpy(np.array(all_X_samples)).float()
        y_tensor = torch.from_numpy(np.array(all_y_samples)).float()

        # 3. N분 뒤 함수 호출량 예측
        ## 입력 준비
        ## 예측 수행
        ## De-normalization

        # 4. 적절한 함수 인스턴스 수 계산
        ## 함수 인스턴스 수(N) 계산
        
        # 5. 함수 인스턴스 수(Pod) 조절
        ## 계산된 N과 현재 Replicas 비교
        ## 다르다면, Replicas를 N으로 조정

        # 6. 모델 재학습

        print("--- 예측 완료 ---")
        time.sleep(PREDICTION_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()