import os
import importlib
import logging
from typing import Dict, Callable
from spotipy import Spotify

from config import OPERATIONS_FOLDER
from spotify_client import get_spotify_client
from menu_utils import print_menu, get_user_choice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_operations() -> Dict[str, Callable[[Spotify], None]]:
    operations = {}
    for filename in os.listdir(OPERATIONS_FOLDER):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"playlist_operations.{module_name}")
                if hasattr(module, 'execute') and hasattr(module, 'MENU_OPTION'):
                    operations[module.MENU_OPTION] = module.execute
            except ImportError as e:
                logger.error(f"Failed to import {module_name}: {e}")
    return operations

def main() -> None:
    sp = get_spotify_client()
    if not sp:
        logger.error("Failed to authenticate. Exiting.")
        return

    operations = load_operations()
    
    while True:
        print_menu(operations)
        choice = get_user_choice(operations)
        
        if choice == 'exit':
            print("Exiting the program. Goodbye!")
            break
        
        if choice in operations:
            try:
                operations[choice](sp)
            except Exception as e:
                logger.error(f"Error executing operation '{choice}': {e}")
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
