import logging
import os
import threading
import time
import urllib.error
import urllib.request
import webbrowser

import webview
from app import app

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}/dashboard"
LOG_PATH = "desktop.log"


def setup_logger():
    logger = logging.getLogger("desktop")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    fh = logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = setup_logger()


def start_flask():
    os.makedirs("instance", exist_ok=True)
    logger.info("Starting Flask server...")
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


def wait_for_server(url, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, ConnectionError) as exc:
            logger.debug(f"Waiting for server: {exc}")
            time.sleep(0.2)
    return False


def start_desktop():
    logger.info("Creating webview window.")
    webview.create_window(
        "Student Risk Dashboard",
        URL,
        width=1200,
        height=850,
    )

    backends = ["mshtml", "edgechromium", None]
    for gui in backends:
        try:
            if gui:
                logger.info(f"Trying pywebview backend: {gui}")
                webview.start(debug=True, gui=gui)
            else:
                logger.info("Trying pywebview default backend")
                webview.start(debug=True)
            logger.info("pywebview started successfully.")
            return
        except Exception as exc:
            logger.error(f"pywebview startup failed for gui={gui}: {exc}", exc_info=True)

    logger.error("pywebview could not start any backend. Falling back to the browser.")
    webbrowser.open(URL)
    input("Press ENTER to exit...")


if __name__ == "__main__":
    server_thread = threading.Thread(target=start_flask, daemon=True)
    server_thread.start()

    if not wait_for_server(URL):
        logger.error("ERROR: Flask server did not start in time.")
        webbrowser.open(URL)
        input("Press ENTER to exit...")
    else:
        start_desktop()
