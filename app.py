from db_utils import init_db, insert_menu_from_csv
from main_ui import run_app

if __name__ == "__main__":
    # Initialize DB and load menu
    init_db()
    insert_menu_from_csv("menu.csv")

    # Run Tkinter UI
    run_app()
