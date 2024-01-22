from datetime import datetime
import pandas as pd
# -------------------------------------------------------------------------------------------------

def validate_date_input(df, starting, ending):
	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

	if starting == '':
		starting_date = df['date'].iloc[0]
	else:
		try:
			starting_date = datetime.strptime(starting, '%Y-%m-%d')
		except Exception as e:
			print('Error (starting date input):', e)
			error_msg = 'Error: Invalid starting date input.'
			return error_msg

	if ending == '':
		ending_date = df['date'].iloc[-1]
	else:
		try:
			ending_date = datetime.strptime(ending, '%Y-%m-%d')
		except Exception as e:
			print('Error (ending date input):', e)
			error_msg = 'Error: Invalid ending date input.'
			return error_msg

	for date in (starting_date, ending_date):
		if date not in list(df['date']):
			date = date.strftime('%Y-%m-%d')
			error_msg = f'Error: Date input "{date}" not found in csv file.'
			return error_msg

	if ending_date < starting_date:
		error_msg = 'Error: Ending date cannot be before starting date.'
		return error_msg

	return (starting_date, ending_date)

def validate_month_input(df_monthly, starting, ending):
	if starting == '':
		starting_month = df_monthly['date'].iloc[0]
	else:
		try:
			starting_month = datetime.strptime(starting, '%Y-%m')
		except Exception as e:
			print('Error (starting month input):', e)
			error_msg = 'Error: Invalid starting month input.'
			return error_msg

	if ending == '':
		ending_month = df_monthly['date'].iloc[-1]
	else:
		try:
			ending_month = datetime.strptime(ending, '%Y-%m')
		except Exception as e:
			print('Error (ending month input):', e)
			error_msg = 'Error: Invalid ending month input.'
			return error_msg

	for month in (starting_month, ending_month):
		if month not in list(df_monthly['date']):
			month = month.strftime('%Y-%m')
			error_msg = f'Error: Month input "{month}" not found in csv file.'
			return error_msg

	if ending_month < starting_month:
		error_msg = 'Error: Ending month cannot be before starting month.'
		return error_msg

	return (starting_month, ending_month)

def validate_lastx_input(max_x, last_x):
	try:
		n = int(last_x)
	except Exception as e:
		print('Error (integer input):', e)
		error_msg = 'Error: Invalid integer input for "Last X Days/Months".'
		return error_msg

	if not (1 <= n <= max_x):
		error_msg = 'Error: Integer value for "Last X Days/Months" must be within csv range.'
		return error_msg

	return n

def validate_toggles(show_streams, show_listeners):
	for toggle_input in (show_streams, show_listeners):
		if toggle_input not in ('on', None):
			error_msg = 'Error: Invalid toggle input.'
			return error_msg

	if (show_streams, show_listeners) == (None, None):
		error_msg = (
			'Error: At least one of "Show Streams" / "Show Listeners" '
			'toggles must be checked.'
		)
		return error_msg

	toggle_data = dict(
		show_streams=bool(show_streams),
		show_listeners=bool(show_listeners)
	)

	return toggle_data

def validate_toggle(first_28days):
	if first_28days not in ('on', None):
		error_msg = 'Error: Invalid toggle input.'
		return error_msg

	toggle_data = dict(
		first_28days=bool(first_28days)
	)

	return toggle_data
