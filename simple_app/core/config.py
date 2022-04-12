from os import getenv, path
from dotenv import load_dotenv


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
env = load_dotenv()