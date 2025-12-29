import pandas as pd
import matplotlib.pyplot as plt

# 1) CSV 읽기
df = pd.read_csv("data (1).csv")

# 2) 숫자형 변환(혹시 문자열로 읽히거나 빈칸이 있으면 NaN 처리)
cols = ["Duration", "Pulse", "Maxpulse", "Calories"]
for c in cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

print("=== head() ===")
print(df.head())
print("\n=== 결측치 개수 ===")
print(df[cols].isna().sum())

# 3) 결측치 처리 (간단하게: Calories 결측은 평균으로 채우기, 나머지는 결측 행 제거)
df["Calories"] = df["Calories"].fillna(df["Calories"].mean())
df = df.dropna(subset=["Duration", "Pulse", "Maxpulse"])

print("\n=== 요약통계 ===")
print(df[cols].describe())

# ----------------------------
# 4) 그래프 1: Duration별 평균 Calories 막대그래프
# ----------------------------
avg_cal_by_duration = df.groupby("Duration")["Calories"].mean().sort_index()

plt.figure(figsize=(8, 4))
plt.bar(avg_cal_by_duration.index.astype(str), avg_cal_by_duration.values)
plt.title("Average Calories by Duration")
plt.xlabel("Duration")
plt.ylabel("Average Calories")
plt.tight_layout()
plt.show()

# ----------------------------
# 5) 그래프 2: Pulse vs Calories 산점도
# ----------------------------
plt.figure(figsize=(6, 4))
plt.scatter(df["Pulse"], df["Calories"])
plt.title("Pulse vs Calories")
plt.xlabel("Pulse")
plt.ylabel("Calories")
plt.tight_layout()
plt.show()

# ----------------------------
# 6) 그래프 3: Calories 히스토그램 (분포)
# ----------------------------
plt.figure(figsize=(6, 4))
plt.hist(df["Calories"].dropna(), bins=10)
plt.title("Calories Distribution")
plt.xlabel("Calories")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ----------------------------
# 7) 그래프 4: index 순서대로 Pulse/Maxpulse 선그래프 (추세)
# ----------------------------
plt.figure(figsize=(8, 4))
plt.plot(df["Pulse"].values, label="Pulse")
plt.plot(df["Maxpulse"].values, label="Maxpulse")
plt.title("Pulse / Maxpulse Trend (Row Order)")
plt.xlabel("Row Index")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.show()
