import csv
from os import path
from random import randint
from datetime import date, timedelta
# -------------------------------------------------------------------------------------------------

csv_file1 = path.join(path.dirname(__file__), "sample-dataset-master.csv")
csv_file2 = path.join(path.dirname(__file__), "sample-dataset-latest.csv")

def random_date(year):
	try:
		date(year, 2, 29)
		days_in_year = 366
	except ValueError:
		days_in_year = 365

	random_days = randint(0, days_in_year-1)

	return date(year, 1, 1) + timedelta(days=random_days)

start_date = random_date(2016)
end_date = random_date(2023)

total_days_master = (end_date - start_date).days + 1
additional_days = 10
print(f'Total days in sample master dataset: {total_days_master}')
print()

listeners = 1
streams = 5
followers = 1

for i in range(1, total_days_master + additional_days + 1):
	if i == 1:
		dataset = [
			{
				'date': start_date.strftime('%Y-%m-%d'),
				'listeners': listeners,
				'streams': streams,
				'followers': followers
			}
		]
		column_names = list(dataset[0].keys())
		continue

	date = start_date + timedelta(days=i-1)

	while True:
		listener_delta = randint(-12, 20)
		if listeners + listener_delta >= 0:
			listeners += listener_delta
			break

	while True:
		stream_delta = randint(-50, 95)
		if streams + stream_delta >= 0:
			streams += stream_delta
			break

	while True:
		follower_delta = randint(-12, 18)
		if followers + follower_delta >= 0:
			followers += follower_delta
			break

	dataset.append(
		{
			column_names[0]: date.strftime('%Y-%m-%d'),
			column_names[1]: listeners,
			column_names[2]: streams,
			column_names[3]: followers
		}
	)

	if i == total_days_master:
		print(f'Writing data to {csv_file1}..')
		with open(csv_file1, 'w', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=column_names)

			writer.writeheader()
			writer.writerows(dataset)

with open(csv_file2, 'w', newline='') as f:
	print(f'Writing data to {csv_file2}..')
	writer = csv.DictWriter(f, fieldnames=column_names)

	writer.writeheader()
	writer.writerows(dataset[-1000:])
	print()
