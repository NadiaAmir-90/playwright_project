
import os 
from pathlib import Path
from dotenv import load_dotenv

#root dir resolve
BASE_DIR=Path(__file__).resolve().parent
load_dotenv(BASE_DIR/".env") #.env load

#django configuration
SECRET_KEY=os.getenv("SECRET_KEY")
DEBUG=os.getenv("DEBUG","False").lower()=="true"
ALLOWED_HOSTS=os.getenv("ALLOWED_HOSTS","localhost").split(",")

# Airbnb configuration
AIRBNB_BASE_URL = os.getenv("AIRBNB_BASE_URL", "https://www.airbnb.com/").strip()



# Browser configuration
BROWSER = os.getenv("BROWSER", "chromium").strip().lower()
HEADLESS=os.getenv("HEADLESS","TRUE").lower()=="true"
SLOW_MO=int(os.getenv("SLOW_MO",0))
DEFAULT_TIMEOUT=int(os.getenv("DEFAULT_TIMEOUT",30000))


#Screenshot configuration
SCREENSHOT_DIR = BASE_DIR / os.getenv("SCREENSHOT_DIR", "screenshots")

# Automation configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES",3))
