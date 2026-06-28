import yfinance as yf
import pandas as pd

def calculate_kd(df, n=9):
    # 計算 RSV
    # RSV = (今日收盤價 - 最近n日最低價) / (最近n日最高價 - 最近n日最低價) * 100
    low_n = df['Low'].rolling(window=n).min()
    high_n = df['High'].rolling(window=n).max()
    
    rsv = (df['Close'] - low_n) / (high_n - low_n) * 100
    
    # 初始化 K 值與 D 值 (通常初始值設為 50)
    k_values = [50]
    d_values = [50]
    
    # 計算 KD
    # K_t = 2/3 * K_{t-1} + 1/3 * RSV_t
    # D_t = 2/3 * D_{t-1} + 1/3 * K_t
    for i in range(1, len(rsv)):
        if pd.isna(rsv.iloc[i]):
            k_values.append(50)
            d_values.append(50)
        else:
            k = (2/3 * k_values[-1]) + (1/3 * rsv.iloc[i])
            d = (2/3 * d_values[-1]) + (1/3 * k)
            k_values.append(k)
            d_values.append(d)
            
    df['K'] = k_values
    df['D'] = d_values
    return df

# 1. 下載 0050 股價數據
ticker = '0050.TW'
data = yf.download(ticker, start='2025-01-01')

# 2. 進行計算
df_kd = calculate_kd(data)

# 3. 顯示最近的數據
print(df_kd[['Close', 'K', 'D']].tail(10))
