from os import environ
from dotenv import load_dotenv
from pathlib import Path
# -------------------------------------------------------------------------------------------------

load_dotenv()

# Flask config
SECRET_KEY = environ.get('APP_SECRET_KEY')
MAX_CONTENT_LENGTH = 250*1024

# Custom config
HOST, PORT = "localhost", 8080

SPOTIFY_MASTER_CSV = Path("user_uploads/spotify_master.csv")
SPOTIFY_LATEST_CSV = Path("user_uploads/spotify_latest.csv")
SPOTIFY_GRAPH_IMG = Path("graph_plot/spotify-graph.png")

TEMP_CSV = Path("user_uploads/spotify_temp.csv")
