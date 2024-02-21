import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
# -------------------------------------------------------------------------------------------------

mpl.use('AGG')

def plot_graph_1(df, show_streams=True, show_listeners=True,
	starting_date_input=None, ending_date_input=None,
	last_xdays=None, save_path=None):

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

	# Filter for selected range
	if last_xdays:
		df2 = df.tail(last_xdays)
	else:
		df2 = df[df['date'].between(starting_date_input, ending_date_input)]

	df2.reset_index(drop=True, inplace=True)
	
	print(f'Selected date range:\n{df2}')
	print()

	# Begin plot ---------->
	# Values for y-axis
	daily_streams = tuple(df2['streams'])
	daily_listeners = tuple(df2['listeners'])

	# Create figure and write labels
	(fig, ax1) = plt.subplots(figsize=(14, 5.6), facecolor='whitesmoke')
	fig.subplots_adjust(top=0.92, bottom=0.12, left=0.08, right=0.92)

	ax1.set_title('Spotify Daily Streams / Listeners', fontsize=16)

	# Plot graph
	print('Plotting graph..')

	if show_streams:
		ax1.plot(df2['date'], daily_streams, color='orange', linewidth=1, label='Streams')
		ax1.fill_between(df2['date'], 0, daily_streams, color='bisque', alpha=0.6)

	if show_listeners:
		ax1.plot(df2['date'], daily_listeners, color='limegreen', linewidth=1, label='Listeners')
		ax1.fill_between(df2['date'], 0, daily_listeners, color='aquamarine', alpha=0.6)

	ax1.legend(facecolor='whitesmoke')
	print()

	# Plot grid lines
	ax1.grid(axis='x', which='major',
		color='darkgrey', alpha=0.2, linewidth=0.8, linestyle='-'
	)
	_set_yaxis1(ax1)

	# Save graph
	if save_path:
		print('Saving graph..')
		fig.savefig(save_path)

	plt.close()

	print('-' * 100)
	return df2

# -------------------------------------------------------------------------------------------------
def plot_graph_2(df, df_monthly, first_28days=False,
	starting_month_input=None, ending_month_input=None,
	last_xmonths=None, save_path=None):

	# Filter for selected range
	if last_xmonths:
		df2 = df_monthly.tail(last_xmonths + 1) # Inclusive of current month
	else:
		df2 = df_monthly[df_monthly['date'].between(starting_month_input, ending_month_input)]

	df2.reset_index(drop=True, inplace=True)
	
	print(f'Selected month range:\n{df2}')
	print()

	# Begin plot ---------->
	# Values for y-axis
	monthly_streams = tuple(df2['streams'])

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
	last_day = df['date'].iloc[-1]
	ending_month = df2['date'].iloc[-1]

	if (ending_month.year, ending_month.month) == (last_day.year, last_day.month):
		if first_28days and last_day.day > 28:
			n = last_day.day - 28
			last_day_streams = df['streams'].iloc[-1-n]
		else:
			last_day_streams = df['streams'].iloc[-1]
	else:
		last_day_streams = None

	# Create figure and write labels
	(fig, ax1) = plt.subplots(figsize=(14, 5.6), facecolor='whitesmoke')
	fig.subplots_adjust(top=0.92, bottom=0.15, left=0.08, right=0.92)

	title = 'Spotify Monthly Streams'
	if first_28days:
		title += ' (1st 28 Days)'
	ax1.set_title(title, fontsize=16)

	# Plot graph
	print('Plotting graph..')

	bar_color = 'sandybrown'
	if first_28days:
		bar_color = 'coral'
	ax1.bar(df2.index, monthly_streams, color=bar_color, label='Streams')

	if last_day_streams:
		bottom = monthly_streams[-1] - last_day_streams
		ax1.bar(df2.index[-1], last_day_streams,
			bottom=bottom, color='springgreen', label='Last Day'
		)

	if len(df2) >= 12:
		n = max(monthly_streams)
		ax1.bar(monthly_streams.index(n), n, color='gold', label='Best Month')

	ax1.legend(facecolor='whitesmoke')
	print()

	# Set x-tick values and labels
	print('Setting x-tick values and labels..')

	if len(df2) > 12 * 6:
		i = 0
		if df2['date'].iloc[0].month % 2 == 0:
			i = 1
		xticks = df2.index[i::2]
		xtick_labels = [date.strftime('%Y-%m') for date in df2['date'].iloc[i::2]]
	else:
		xticks = df2.index
		xtick_labels = [date.strftime('%Y-%m') for date in df2['date']]

	ax1.set_xticks(xticks)

	df2_lengths = (15, 18, 24, 33, 45)
	for (rotation_i, n) in enumerate(df2_lengths):
		if len(df2) <= n:
			ax1.set_xticklabels(xtick_labels, rotation=rotation_i * 15)
			if rotation_i >= 2:
				ax1.set_xticklabels(xtick_labels,
					horizontalalignment='right', rotation_mode='anchor'
				)
			break
	else:
		ax1.set_xticklabels(xtick_labels, rotation=90)

	for x in ax1.get_xticklabels():
		if x.get_text().endswith('01'):
			x.set_color('blue')

	print(f'x-ticks: {xticks}')
	print(f'x-tick labels: {xtick_labels}')
	print()

	_set_yaxis1(ax1)

	# Save graph
	if save_path:
		print('Saving graph..')
		fig.savefig(save_path)

	plt.close()

	print('-' * 100)
	return df2

# -------------------------------------------------------------------------------------------------
def plot_graph_3(df,
	starting_date_input=None, ending_date_input=None,
	last_xdays=None, save_path=None):

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

	# Filter for selected range
	if last_xdays:
		df2 = df.tail(last_xdays)
	else:
		df2 = df[df['date'].between(starting_date_input, ending_date_input)]

	df2.reset_index(drop=True, inplace=True)
	
	print(f'Selected date range:\n{df2}')
	print()

	# Begin plot ---------->
	# Values for y-axis
	daily_streams_per_listener = tuple(df2['streams'] / df2['listeners'])

	# Create figure and write labels
	(fig, ax1) = plt.subplots(figsize=(14, 5.6), facecolor='whitesmoke')
	fig.subplots_adjust(top=0.92, bottom=0.12, left=0.08, right=0.92)

	ax1.set_title('Spotify Daily Average Streams per Listener', fontsize=16)

	# Plot graph
	print('Plotting graph..')

	ax1.plot(df2['date'], daily_streams_per_listener,
		color='orange', linewidth=1, label='Streams per Listener'
	)
	ax1.fill_between(df2['date'], 0, daily_streams_per_listener,
		color='bisque', alpha=0.6
	)

	ax1.legend(facecolor='whitesmoke')
	print()

	# Plot grid lines
	ax1.grid(axis='x', which='major',
		color='darkgrey', alpha=0.2, linewidth=0.8, linestyle='-'
	)
	(_, ax2) = _set_yaxis1(ax1)
	for ax in (ax1, ax2):
		ax.yaxis.set_major_formatter('{x:,.2f}')

	# Save graph
	if save_path:
		print('Saving graph..')
		fig.savefig(save_path)

	plt.close()

	print('-' * 100)
	return (df2, daily_streams_per_listener)

# -------------------------------------------------------------------------------------------------
def _set_yaxis1(ax1):
	# Set and format y-tick values and labels
	ax1.set_ylim(bottom=0)
	yticks_major = ax1.get_yticks()

	ax2 = ax1.twinx()

	for ax in (ax1, ax2):
		ax.set_yticks(yticks_major)
		ax.yaxis.set_major_formatter('{x:,.0f}')
		ax.yaxis.set_minor_locator(AutoMinorLocator())

	yticks_minor = ax1.get_yticks(minor=True)

	# Plot horizontal lines for each major/minor y-tick
	for ytick in yticks_major:
		ax1.axhline(y=ytick, color='darkgrey', alpha=0.6, linewidth=0.8, linestyle='--')
	for ytick in yticks_minor:
		ax1.axhline(y=ytick, color='darkgrey', alpha=0.15, linewidth=0.8, linestyle='-')

	return (ax1, ax2)
