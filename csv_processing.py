import os
from os import path
from datetime import datetime
import csv

from werkzeug.utils import secure_filename
# -------------------------------------------------------------------------------------------------

def validate_user_upload(uploaded_file):
	print('Checking user upload..')

	filename = secure_filename(uploaded_file.filename)

	if filename:
		file_ext = path.splitext(filename)[1].lower()
		if file_ext != ".csv":
			error_msg = f'Error: Invalid file extension.'
			print(error_msg)
			return error_msg

		print('[No errors detected.]')
		print('-' * 100)
		return 1

	print('[Empty field submitted.]')
	return 2

# -------------------------------------------------------------------------------------------------
column_names = ['date', 'listeners', 'streams', 'followers']

def validate_csv(csv_file):
	print('Checking csv file..')

	with open(csv_file, encoding='utf-8-sig') as f:
		try:
			csv1 = list(csv.reader(f))
		except Exception as e:
			error_msg = f'Error: {e}'
			print(error_msg)
			return error_msg

	if csv1[0] != column_names:
		error_msg = 'CSV Error: Unexpected value(s) in header row.'
		print(error_msg)
		return error_msg

	for (i, row) in enumerate(csv1[1:], 1):
		if len(row) != 4:
			error_msg = f'CSV Error (row {i}): Unexpected row length.'
			print(error_msg)
			return error_msg

		if len(row[0]) != 10:
			error_msg = f'CSV Error (row {i}): Unexpected length for date value.'
			print(error_msg)
			return error_msg

		try:
			datetime.strptime(row[0], '%Y-%m-%d')
		except Exception as e:
			error_msg = f'CSV Error (row {i}): {e}'
			print(error_msg)
			return error_msg

		for j in (1, 2, 3):
			try:
				int(row[j])
			except Exception as e:
				error_msg = f'CSV Error (row {i}): {e}'
				print(error_msg)
				return error_msg

	print('[No errors detected.]')
	print('-' * 100)
	return 1

def merge_csv(latest_csv, master_csv, save_path=None):
	print('Preparing csv merge..')

	with open(latest_csv, encoding='utf-8-sig') as f1, open(master_csv) as f2:
		csv1 = list(csv.DictReader(f1))
		csv2 = list(csv.DictReader(f2))

	print('Identifying new rows for csv merge..')

	new_rows = [row for row in csv1 if row['date'] > csv2[-1]['date']]
	if new_rows:
		print(f'{len(new_rows)} NEW ROW(S) TO BE ADDED:')
		for (i, row) in enumerate(new_rows, 1):
			print(f'{i}. {row}')
	else:
		print('[NO NEW ROWS FOUND]')
	print()

	csv1_dates = [row['date'] for row in csv1]
	for row in csv2:
		if row['date'] not in csv1_dates:
			csv1.append(row)

	csv1.sort(key=lambda row: row['date'])

	if save_path is None:
		save_path = master_csv

	with open(save_path, 'w', newline='') as f:
		dictwriter = csv.DictWriter(f, fieldnames=column_names)

		dictwriter.writeheader()
		for row in csv1:
			dictwriter.writerow(row)

	print('[New csv file successfully merged.]')
	print('-' * 100)
	return csv1

def sort_csv(csv_file, save_path=None):
	print('Sorting csv file..')

	with open(csv_file, encoding='utf-8-sig') as f:
		csv1 = list(csv.DictReader(f))

	csv1.sort(key=lambda row: row['date'])

	if save_path is None:
		save_path = csv_file

	with open(save_path, 'w', newline='') as f:
		dictwriter = csv.DictWriter(f, fieldnames=column_names)

		dictwriter.writeheader()
		for row in csv1:
			dictwriter.writerow(row)

	print('[Csv file sorted.]')
	print('-' * 100)
	return csv1

# -------------------------------------------------------------------------------------------------
def process_csv(uploaded_file, master_csv, latest_csv, temp_csv, save_path=None):
	user_upload_checked = validate_user_upload(uploaded_file)

	if user_upload_checked == 1:
		uploaded_file.save(temp_csv)

		csv_checked = validate_csv(temp_csv)

		if csv_checked == 1:
			if not path.exists(master_csv):
				os.rename(temp_csv, master_csv)
				sort_csv(master_csv, save_path=save_path)
				return 1

			if path.exists(latest_csv):
				os.remove(latest_csv)

			os.rename(temp_csv, latest_csv)
			merge_csv(latest_csv, master_csv, save_path=save_path)
			return 1

		os.remove(temp_csv)
		error_msg = csv_checked
		return error_msg

	if user_upload_checked != 2:
		error_msg = user_upload_checked
		return error_msg

	return 2
