import pandas as pd
import matplotlib.pyplot as plt

# csv 파일 불러오기
df = pd.read_csv('la-job.csv')

# 'pay' 컬럼에서 시급과 연봉 분리하기
df['hourly'] = df['pay'].str.contains('an hour')
df['pay'] = df['pay'].str.replace('an hour', '', regex=False).str.replace('$', '', regex=False).str.replace(',', '', regex=False)

# 시급이 범위로 표시된 경우 분리하고 평균 계산
df.loc[df['hourly'] == True, 'pay'] = df.loc[df['hourly'] == True, 'pay'].str.split('-').apply(lambda x: (float(x[0]) + float(x[1])) / 2 if len(x) > 1 else float(x[0]))

# 시급을 연봉으로 변환
df.loc[df['hourly'] == True, 'pay'] = df.loc[df['hourly'] == True, 'pay'].astype(float) * 40 * 50

# 'pay'에서 'a year', 'Up to', 'From'이 아닌 행만 선택하여 새로운 데이터프레임 생성
df_year = df[df['pay'].str.contains('a year', na=False) & ~df['pay'].str.contains('Up to', na=False) & ~df['pay'].str.contains('From', na=False)].copy()

# 'pay'에서 '$', ',' , 'a year' 제거
df_year['pay'] = df_year['pay'].str.replace(' a year', '', regex=False)

# '-'를 기준으로 최소 급여와 최대 급여를 나누고, 평균 급여 계산
df_year[['min_pay', 'max_pay']] = df_year['pay'].str.split('-', expand=True)
df_year['avg_pay'] = df_year[['min_pay', 'max_pay']].astype(float).mean(axis=1)

# 'job' 별로 'avg_pay'의 평균값 계산
avg_pay_by_job = df_year.groupby('job')['avg_pay'].mean()

# 결과 시각화
plt.figure(figsize=(10, 6))
avg_pay_by_job.plot(kind='bar')
plt.title('Average Pay by Job')
plt.xlabel('Job')
plt.ylabel('Average Pay')
plt.xticks(rotation=45)
plt.show()

# 'company' 별로 'avg_pay'의 평균값 계산
avg_pay_by_company = df_year.groupby('company')['avg_pay'].mean()

# 결과 시각화
plt.figure(figsize=(10, 6))
avg_pay_by_company.plot(kind='bar')
plt.title('Average Pay by Company')
plt.xlabel('Company')
plt.ylabel('Average Pay')
plt.xticks(rotation=45)
plt.show()
