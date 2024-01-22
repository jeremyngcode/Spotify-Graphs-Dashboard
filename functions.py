import pandas as pd
# -------------------------------------------------------------------------------------------------

def make_dataframe(csv_file, incl_followers=False):
	cols = ['date', 'listeners', 'streams']
	if incl_followers:
		cols.append('followers')

	df = pd.read_csv(csv_file, usecols=cols)

	for (stream_count, index) in zip(df['streams'], df.index):
		if stream_count > 0:
			starting_index = index
			break
	df = df[starting_index:].reset_index(drop=True)

	return df

def make_dataframe_monthly(df, first_28days=False):
	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

	if first_28days:
		df_first28 = df[df['date'].dt.day <= 28]

		df_monthly = df_first28.groupby(
			pd.Grouper(key='date', freq='MS')
			)['streams'].sum().reset_index()
	else:
		df_monthly = df.groupby(
			pd.Grouper(key='date', freq='MS')
			)['streams'].sum().reset_index()

	return df_monthly

def get_total_streams(df, *last_xdays):
	lifetime_streams = int(df['streams'].sum())
	total_streams = {'lifetime': f'{lifetime_streams:,}'}

	for x in last_xdays:
		if len(df) >= x:
			last_xdays_streams = int(df['streams'].tail(x).sum())
			total_streams[f'last_{x}'] = f'{last_xdays_streams:,}'
		else:
			total_streams[f'last_{x}'] = '???'

	return total_streams

def get_minmax_date(df):
	min_date = df['date'].iloc[0]
	max_date = df['date'].iloc[-1]

	max_xdays = len(df)

	return (min_date, max_date, max_xdays)

def get_minmax_month(df):
	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
	min_date = df['date'].iloc[0]
	max_date = df['date'].iloc[-1]

	min_month = min_date.strftime('%Y-%m')
	max_month = max_date.strftime('%Y-%m')

	# Not inclusive of current month
	max_xmonths = (
		(max_date.year - min_date.year) * 12
		+ (max_date.month - min_date.month)
	)

	return (min_month, max_month, max_xmonths)

def get_range_totalaverage(filtered_df):
	range_total = int(filtered_df['streams'].sum())
	range_average = round(range_total / len(filtered_df))

	range_total = f'{range_total:,}'
	range_average = f'{range_average:,}'

	return (range_total, range_average)
