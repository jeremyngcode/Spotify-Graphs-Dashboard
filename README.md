Spotify Graphs Dashboard
========================
A simple and fast dashboard app for visualizing streams/listeners data from a Spotify artist's CSV file.

Intro / The Problem
-------------------
As an [artist on Spotify](https://open.spotify.com/artist/6mdGjVrAY95ecXnVgtefti), I actually had never been very satisfied with the Spotify for Artists dashboard. When they announced in 2023 that they were limiting the available data to just the past 2 years plus year-to-date, that was about when I decided it was time I built my own dashboard.

The initial idea was to:
1. Enable artists to visualize their full data from day 1.
2. Allow for unlimited date range filtering as opposed to just 1 year.

Then along the way, I decided I might as well add in some extra utility, a significant one being monthly data.

The following is a quick 40-second showcase of the dashboard UI:

https://github.com/jeremyngcode/Spotify-Graphs-Dashboard/assets/156220343/86bfb581-5195-4e1d-ad0d-36188ad001ab

Using The Dashboard
-------------------
1. Download your latest Spotify CSV data from [Spotify for Artists](https://artists.spotify.com).
2. In [config.py](config.py), fill in `SECRET_KEY` with a random string. I have also provided a .env template file to use with `load_dotenv()`.
3. Run [dashboard_app.py](dashboard_app.py).

### Uploading CSV
The first time dashboard_app.py is run, you will be prompted to upload your Spotify CSV file which will be saved as "spotify_master.csv" in the filesystem. This master CSV file is retrieved in subseuqent runs of the dashboard app and is where all graph plots retrieve data from.

If there is a new CSV upload, all missing date entries are appended to it and it becomes the new master CSV file.

- **Example:** <br>
  Master CSV date range: 2016-01-01 - 2024-01-20 <br>
  New CSV date range: 2022-01-01 - 2024-01-23 (past 2 years plus year-to-date)

  2016-01-01 - 2021-12-31 data from master CSV is appended to the new CSV and saved as the new master CSV.

### Plotting Graphs
There are 3 main graph plots:
1. Daily Streams / Listeners
2. Monthly Streams
3. Daily Average Streams per Listener

1 and 3 are daily line graphs with a default plot for data from the last 730 days (2 years), while 2 is a monthly bar graph with a default plot for data from the last 36 months (3 years). If your master CSV does not have that much data yet, it will default to a lower number that accommodates.

- When plotting using the datepicker form, the 'Last X Days/Months' input is prioritized over a date range input. If this field is empty, then the empty starting and/or ending date field is assumed to be the earliest and latest date in the master CSV respectively.

- When using the 'Last X Months' input field for monthly streams, the current month (assumed to be the month of the latest date entry in the master CSV) is always excluded from data calculations, but it will still be plotted. That means that if the current month is 2024 Jan and you input 12, the 12 months total and monthly average streams displayed will be based on 2023 Jan to 2023 Dec, but 2024 Jan will stil be included in the plot (13 bars in total).

  I figured this probably makes better sense for practicality reasons, since an uncompleted month would skew averages. You can still use the month range inputs if and when this isn't the desired behaviour.

### Data Boxes
At the default plot pages, the 5 data boxes above the graph will always display streams for (in order from left to right):
1. Lifetime
2. Last 365 days
3. Last 28 days
4. Last 7 days
5. Last day

If the datepicker form was used to plot, the pale orange boxes will display data derived from your selected date range instead, while the other boxes remain the same.

### Sample Data Generator
For anyone who isn't a Spotify artist, I've included [sample_data_generator.py](sample-csv-data/sample_data_generator.py) if you want to play around with the dashboard. Running this script will output the files "sample-dataset-master.csv" and "sample-dataset-latest.csv" in the same directory. The former is meant to be uploaded when you run the dashboard app for the first time, and the latter is meant to be your 'new' CSV file from Spotify.

Dev Notes
---------
I had initially handled new CSV uploads by just appending the new date entries into the master CSV file. This works on assumption that all the old data is the same as in the master, but Spotify has provided conflicting data before. And so, at every new upload, I needed to decide on which data to use as truth - master or new? I thought it was best to assume that the latest provided CSV file from Spotify would always be the most accurate, hence why I decided on appending missing date entries to the new CSV file and then saving it as the new master CSV.

Closing Thoughts
----------------
This is one of my most significant and satisfying projects so far. After learning and practising Python for a few months and then picking up HTML/CSS soon after, it was finally time to connect backend and frontend work! I gotta say, CSS was kinda tedious, but a lot of fun nevertheless. And I thought Jinja was pretty cool too. Now I'm just looking forward to starting JavaScript soon. 😁

#### Notable libraries used / learned for this project:
- [Flask](https://pypi.org/project/Flask/)
- [Jinja](https://pypi.org/project/Jinja2/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [pandas](https://pypi.org/project/pandas/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

![sample-dashboard](https://github.com/jeremyngcode/Spotify-Graphs-Dashboard/assets/156220343/6e4f51dd-7650-4679-a535-d907f55d105a)
