import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
from core.app import App

if __name__ == "__main__":
    with App() as alexApp:
        alexApp.start()
