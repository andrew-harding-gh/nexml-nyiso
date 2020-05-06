# The purpose of this script is to extrapolate daily
# NYC population data from yearly NYC population data
import pandas as pd



# yearly_population_df = pd.read_csv('../raw_data/nyc_population.csv', sep='\t', names=['year', 'population', 'yearly growth rate'])

df = pd.read_csv('../raw_data/nyc_population.csv', sep='\t')
df2 = pd.date_range(start='2/1/2005', end='3/30/2020').to_frame(index=False, name='date')
df2['year'] = df2.date.dt.year
df2['day_of_year'] = df2.date.dt.dayofyear
df3 = df2.join(df.set_index('year'), on='year')
df3['daily_population_change'] = df3.apply(lambda x: (x.day_of_year/df3[df3['year'] == x.year].shape[0]) * (df[df['year'] == x.year + 1].iloc[0].population - x.population), axis=1)
df3['total_daily_population'] = df3['daily_population_change'] + df3['population']
print('bp')
