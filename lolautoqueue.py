import pyautogui
import time
import logging
import win32gui
import win32con
import os
import sys
from PIL import Image, ImageDraw
import pystray
from threading import Thread, Event

# Configure logging
logging.basicConfig(filename='match_accept.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Event to signal the background thread to stop
stop_event = Event()

# Function to check if the League of Legends client is minimized
def is_window_minimized(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd != 0:
        placement = win32gui.GetWindowPlacement(hwnd)
        # Check if the window is minimized
        return placement[1] == win32con.SW_SHOWMINIMIZED
    return False

# Function to locate and click the accept button
def click_accept_button(image):
    try:
        logging.info("Attempting to locate the accept button on screen.")
        button_location = pyautogui.locateOnScreen(image, confidence=0.8)
        if button_location:
            logging.info("Accept button found, attempting to click.")
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            logging.info("Match accepted!")
        else:
            logging.warning("Accept button not found.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

def main_loop():
    # Get the path to the image file included with PyInstaller
    if getattr(sys, 'frozen', False):
        # The application is frozen
        script_dir = sys._MEIPASS
    else:
        # The application is not frozen
        script_dir = os.path.dirname(__file__)

    image_path = os.path.join(script_dir, 'accept_button.png')
    
    if not os.path.exists(image_path):
        logging.error(f"Image file not found at path: {image_path}")
        return
    
    logging.info(f"Image file found at path: {image_path}")

    game_window_title = "League of Legends"  # Title of the game window
    while not stop_event.is_set():
        if not is_window_minimized(game_window_title):
            click_accept_button(image_path)
        else:
            logging.info("Game window is minimized.")
        stop_event.wait(5)  # Check every 5 seconds instead of every second

def create_image():
    # Generate an image and draw a pattern
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=(255, 255, 255))
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=(255, 255, 255))

    return image

def on_quit(icon, item):
    logging.info("Shutting down lolautoqueue application.")
    stop_event.set()
    icon.stop()
    sys.exit()

def setup_tray_icon():
    icon = pystray.Icon("lolautoqueue", create_image(), "LoL Auto Queue", pystray.Menu(
        pystray.MenuItem('R u winning son?', on_quit)
    ))
    icon.run()

if __name__ == "__main__":
    background_thread = Thread(target=main_loop)
    background_thread.start()
    setup_tray_icon()
    background_thread.join()
