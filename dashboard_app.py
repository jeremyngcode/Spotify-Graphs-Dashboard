from os import path
import webbrowser

from flask import (
	Flask, render_template, redirect, url_for, request,
	send_file, flash, abort
)
from werkzeug.exceptions import HTTPException

from csv_processing import process_csv
from functions import *
from input_validation import *
from plot_graphs import *
# -------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_pyfile("config.py")

SPOTIFY_MASTER_CSV = path.join(app.root_path, app.config['SPOTIFY_MASTER_CSV'])
SPOTIFY_LATEST_CSV = path.join(app.root_path, app.config['SPOTIFY_LATEST_CSV'])
SPOTIFY_GRAPH_IMG = path.join(app.root_path, app.config['SPOTIFY_GRAPH_IMG'])

TEMP_CSV = path.join(app.root_path, app.config['TEMP_CSV'])

dashboard = {
	1: 'Daily Streams / Listeners',
	2: 'Monthly Streams',
	3: 'Daily Average Streams per Listener'
}

# -------------------------------------------------------------------------------------------------
@app.route("/")
def home():
	if path.exists(SPOTIFY_MASTER_CSV):
		return redirect(url_for('default_dashboard', dashboard_id=1))
	else:
		return redirect(url_for('upload_csv'))

# -------------------------------------------------------------------------------------------------
@app.route("/dashboard/<int:dashboard_id>")
def default_dashboard(dashboard_id):
	if not path.exists(SPOTIFY_MASTER_CSV):
		return redirect(url_for('upload_csv'))

	df = make_dataframe(SPOTIFY_MASTER_CSV)
	total_streams = get_total_streams(df, 365, 28, 7, 1)

	if dashboard_id in (1, 3):
		minmax_datemonth = get_minmax_date(df)

		for n in (730, 365, 180, 90, 28):
			if len(df) >= n:
				last_xdays = n
				break
		else:
			last_xdays = len(df)

		suffix = 's' if last_xdays > 1 else ''
		titlebar_rangelabel = f'Last {last_xdays} Day{suffix}'

		if dashboard_id == 1:
			plot_graph_1(df, last_xdays=last_xdays,
				save_path=SPOTIFY_GRAPH_IMG
			)

		elif dashboard_id == 3:
			plot_graph_3(df, last_xdays=last_xdays,
				save_path=SPOTIFY_GRAPH_IMG
			)

	elif dashboard_id == 2:
		minmax_datemonth = get_minmax_month(df)

		df_monthly = make_dataframe_monthly(df)
		for n in (36, 24, 12):
			if len(df_monthly) >= n + 1:
				last_xmonths = n
				break
		else:
			last_xmonths = len(df_monthly) - 1

		suffix = 's' if last_xmonths > 1 else ''
		titlebar_rangelabel = f'Last {last_xmonths} Month{suffix}'

		plot_graph_2(df, df_monthly, last_xmonths=last_xmonths,
			save_path=SPOTIFY_GRAPH_IMG
		)

	return render_template("dashboard.html.j2",
		dashboard_id=dashboard_id,
		graph_title=dashboard[dashboard_id],
		total_streams=total_streams,
		minmax_datemonth=minmax_datemonth,
		titlebar_rangelabel=titlebar_rangelabel
	)

@app.route("/dashboard/<int:dashboard_id>/input")
def input_dashboard(dashboard_id):
	if not path.exists(SPOTIFY_MASTER_CSV):
		return redirect(url_for('upload_csv'))

	df = make_dataframe(SPOTIFY_MASTER_CSV)
	total_streams = get_total_streams(df, 365, 28, 7, 1)

	if dashboard_id in (1, 3):
		minmax_datemonth = get_minmax_date(df)
	elif dashboard_id == 2:
		minmax_datemonth = get_minmax_month(df)

	data = dict(
		dashboard_id=dashboard_id,
		graph_title=dashboard[dashboard_id],
		total_streams=total_streams,
		minmax_datemonth=minmax_datemonth,
		user_input=True
	)

	params = request.args.to_dict()

	if dashboard_id == 1:
		toggle_data = validate_toggles(
			params.get('show-streams'),
			params.get('show-listeners')
		)
		if not isinstance(toggle_data, dict):
			error_msg = toggle_data
			abort(400, description=error_msg)

		if params['last-xdays']:
			last_xdays = validate_lastx_input(
				minmax_datemonth[2], params['last-xdays']
			)
			if not isinstance(last_xdays, int):
				error_msg = last_xdays
				abort(400, description=error_msg)

			filtered_df = plot_graph_1(df,
				**toggle_data,
				last_xdays=last_xdays,
				save_path=SPOTIFY_GRAPH_IMG
			)

			suffix = 's' if last_xdays > 1 else ''
			range_label = f'Last {last_xdays} Day{suffix}'

		else:
			selected_date_range = validate_date_input(df,
				params['starting-date'],
				params['ending-date']
			)
			if len(selected_date_range) != 2:
				error_msg = selected_date_range
				abort(400, description=error_msg)

			filtered_df = plot_graph_1(df,
				**toggle_data,
				starting_date_input=selected_date_range[0],
				ending_date_input=selected_date_range[1],
				save_path=SPOTIFY_GRAPH_IMG
			)

			suffix = 's' if len(filtered_df) > 1 else ''
			range_label = f'Range: {len(filtered_df)} Day{suffix}'

		range_value_totalaverage = get_range_totalaverage(filtered_df)
		range_label_totalaverage = (
			f'{range_label} | Total',
			f'{range_label} | Daily Average'
		)

		starting_date = filtered_df['date'].iloc[0]
		ending_date = filtered_df['date'].iloc[-1]
		titlebar_rangelabel = f'{starting_date.date()} - {ending_date.date()}'

		return render_template("dashboard.html.j2",
			**data,
			range_value_totalaverage=range_value_totalaverage,
			range_label_totalaverage=range_label_totalaverage,
			titlebar_rangelabel=titlebar_rangelabel
		)

	elif dashboard_id == 2:
		toggle_data = validate_toggle(
			params.get('first-28days')
		)
		if not isinstance(toggle_data, dict):
			error_msg = toggle_data
			abort(400, description=error_msg)

		df_monthly = make_dataframe_monthly(df, **toggle_data)

		if params['last-xmonths']:
			last_xmonths = validate_lastx_input(
				minmax_datemonth[2], params['last-xmonths']
			)
			if not isinstance(last_xmonths, int):
				error_msg = last_xmonths
				abort(400, description=error_msg)

			filtered_df = plot_graph_2(df, df_monthly,
				**toggle_data,
				last_xmonths=last_xmonths,
				save_path=SPOTIFY_GRAPH_IMG
			)

			suffix = 's' if last_xmonths > 1 else ''
			range_label = f'Last {last_xmonths} Month{suffix}'

			range_value_totalaverage = get_range_totalaverage(filtered_df[:-1])

			ending_month = filtered_df['date'].iloc[-2]

		else:
			selected_month_range = validate_month_input(df_monthly,
				params['starting-month'],
				params['ending-month']
			)
			if len(selected_month_range) != 2:
				error_msg = selected_month_range
				abort(400, description=error_msg)

			filtered_df = plot_graph_2(df, df_monthly,
				**toggle_data,
				starting_month_input=selected_month_range[0],
				ending_month_input=selected_month_range[1],
				save_path=SPOTIFY_GRAPH_IMG
			)

			suffix = 's' if len(filtered_df) > 1 else ''
			range_label = f'Range: {len(filtered_df)} Month{suffix}'

			range_value_totalaverage = get_range_totalaverage(filtered_df)

			ending_month = filtered_df['date'].iloc[-1]

		range_label_totalaverage = (
			f'{range_label} | Total',
			f'{range_label} | Monthly Average'
		)

		starting_month = filtered_df['date'].iloc[0]
		titlebar_rangelabel = (
			f'{starting_month.strftime("%Y-%m")} - {ending_month.strftime("%Y-%m")}'
		)

		return render_template("dashboard.html.j2",
			**data,
			range_value_totalaverage=range_value_totalaverage,
			range_label_totalaverage=range_label_totalaverage,
			titlebar_rangelabel=titlebar_rangelabel
		)

	elif dashboard_id == 3:
		if params['last-xdays']:
			last_xdays = validate_lastx_input(
				minmax_datemonth[2], params['last-xdays']
			)
			if not isinstance(last_xdays, int):
				error_msg = last_xdays
				abort(400, description=error_msg)

			(filtered_df, daily_streams_per_listener) = plot_graph_3(df,
				last_xdays=last_xdays,
				save_path=SPOTIFY_GRAPH_IMG
			)

			suffix = 's' if last_xdays > 1 else ''
			range_label = f'Last {last_xdays} Day{suffix}'

		else:
			selected_date_range = validate_date_input(df,
				params['starting-date'],
				params['ending-date']
			)
			if len(selected_date_range) != 2:
				error_msg = selected_date_range
				abort(400, description=error_msg)

			(filtered_df, daily_streams_per_listener) = plot_graph_3(df,
				starting_date_input=selected_date_range[0],
				ending_date_input=selected_date_range[1],
				save_path=SPOTIFY_GRAPH_IMG
			)

			suffix = 's' if len(filtered_df) > 1 else ''
			range_label = f'Range: {len(filtered_df)} Day{suffix}'

		range_value_average = round(
			sum(daily_streams_per_listener) / len(daily_streams_per_listener), 3
		)
		range_label_average = f'{range_label} | Daily Average'

		starting_date = filtered_df['date'].iloc[0]
		ending_date = filtered_df['date'].iloc[-1]
		titlebar_rangelabel = f'{starting_date.date()} - {ending_date.date()}'

		return render_template("dashboard.html.j2",
			**data,
			range_value_average=range_value_average,
			range_label_average=range_label_average,
			titlebar_rangelabel=titlebar_rangelabel
		)

@app.route("/graph_plot")
def get_graph():
	return send_file(SPOTIFY_GRAPH_IMG)

# -------------------------------------------------------------------------------------------------
@app.route("/upload-csv", methods=['GET', 'POST'])
def upload_csv():
	if request.method == 'POST':
		uploaded_file = request.files['spotify-csv']

		csv_processed = process_csv(uploaded_file,
			SPOTIFY_MASTER_CSV, SPOTIFY_LATEST_CSV, TEMP_CSV
		)

		if csv_processed == 1:
			flash('CSV file uploaded successfully. &#9989;', 'success')
		elif csv_processed == 2:
			flash('Empty field submitted. &#10060;', 'error')
		else:
			error_msg = csv_processed
			abort(400, description=error_msg)		

		return redirect(url_for('default_dashboard', dashboard_id=1))

	if path.exists(SPOTIFY_MASTER_CSV):
		return redirect(url_for('default_dashboard', dashboard_id=1))

	return render_template("upload-csv.html.j2",
		dashboard_id=1,
		graph_title='Upload Spotify CSV'
	)

@app.post("/dashboard/<int:dashboard_id>")
@app.post("/dashboard/<int:dashboard_id>/input")
def upload_new_csv(dashboard_id):
	uploaded_file = request.files['spotify-csv']

	csv_processed = process_csv(uploaded_file,
		SPOTIFY_MASTER_CSV, SPOTIFY_LATEST_CSV, TEMP_CSV
	)

	if csv_processed == 1:
		flash('New CSV successfully merged. &#9989;', 'success')
	elif csv_processed == 2:
		flash('Empty field submitted. &#10060;', 'error')
	else:
		error_msg = csv_processed
		abort(400, description=error_msg)

	return redirect(url_for('default_dashboard', dashboard_id=dashboard_id))

# -------------------------------------------------------------------------------------------------
@app.errorhandler(HTTPException)
def handle_error(err):
	return render_template("errorhandler.html.j2",
		err_code=err.code,
		err_name=err.name,
		err_msg=err.description
	), err.code

# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	webbrowser.open(f"http://{app.config['HOST']}:{app.config['PORT']}")
	app.run(
		host=app.config['HOST'],
		port=app.config['PORT']
	)
