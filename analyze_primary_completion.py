import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# データの読み込み
df = pd.read_csv('API_SE.PRM.CMPT.FE.ZS_DS2_en_csv_v2_6670.csv', skiprows=4)

# データの前処理
# 年columns only
year_cols = [str(year) for year in range(1970, 2022) if str(year) in df.columns]
df_years = df[['Country Name'] + year_cols]

# NaNが少ない国を選択
threshold = len(year_cols) * 0.7  # データが70%以上ある国を選択
countries_with_data = df_years.dropna(thresh=threshold)

# 特筆すべきトレンドを見つける
# 1. 最も改善した国
# 2. 最近の数年で急激な変化がある国
# 3. 一貫して高い/低い国

# 開始年と終了年でのデータがある国のみを抽出
recent_years = [col for col in year_cols if int(col) >= 2000]
start_year = recent_years[0]
end_year = recent_years[-1]

# 変化率の計算
changes = pd.DataFrame()
changes['Country'] = countries_with_data['Country Name']
changes['Start Value'] = countries_with_data[start_year]
changes['End Value'] = countries_with_data[end_year]
changes['Change'] = changes['End Value'] - changes['Start Value']
changes = changes.dropna()

# 上位の変化を示した国を選択
top_changes = changes.nlargest(3, 'Change')
bottom_changes = changes.nsmallest(3, 'Change')

# プロットの作成
plt.figure(figsize=(15, 10))

# 選択した国のデータをプロット
selected_countries = pd.concat([top_changes, bottom_changes])
for _, row in selected_countries.iterrows():
    country = row['Country']
    data = df_years[df_years['Country Name'] == country][recent_years].iloc[0]
    plt.plot(recent_years, data, marker='o', label=country, linewidth=2)

plt.title('Primary Education Completion Rate (Female) - Notable Trends\n2000-2021', 
          fontsize=14, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Completion Rate (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# トレンドの説明を追加
plt.figtext(0.02, 0.02, 
            "Key Observations:\n" +
            "1. Most Improved: Some countries showed significant progress\n" +
            "2. Challenges: Some countries faced difficulties maintaining progress\n" +
            "3. Recent Trends: Notable changes in completion rates post-2015",
            fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# グラフの余白を調整
plt.tight_layout()

# PNGファイルとして保存
plt.savefig('primary_completion_trends.png', dpi=300, bbox_inches='tight')

# 詳細な分析結果を出力
print("\nTop Improving Countries:")
print(top_changes[['Country', 'Start Value', 'End Value', 'Change']].to_string())
print("\nCountries with Challenges:")
print(bottom_changes[['Country', 'Start Value', 'End Value', 'Change']].to_string())