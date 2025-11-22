import os
import sys
import json

dataFolderPath = ""
dreamJournalFolderPath = ""

def get_asset(relative_path):
    relative_path = "assets/" + relative_path
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_default_settings():
    settings_path = get_asset("settings.json")
    with open(settings_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    global dataFolderPath
    settings_path = os.path.join(dataFolderPath, "settings.json")
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f)

def load_files():
    global dataFolderPath
    global dreamJournalFolderPath
    folderPath = os.environ.get("LOCALAPPDATA")
    dataFolderPath = os.path.join(folderPath, "Night Cloud")
    os.makedirs(dataFolderPath, exist_ok=True)
    dreamJournalFolderPath = os.path.join(dataFolderPath, "dream journal")
    os.makedirs(dreamJournalFolderPath, exist_ok=True)
    settingsFolderPath = os.path.join(dataFolderPath, "settings.json")
    settings = None
    if not os.path.exists(settingsFolderPath):
        settings = get_default_settings()
        with open(settingsFolderPath, "w", encoding="utf-8") as f:
            json.dump(settings, f)
    else:
        with open(settingsFolderPath, "r", encoding="utf-8") as f:
            settings = json.load(f)
    return dreamJournalFolderPath, settings

def get_a_journal(monthAndYear):
    global dreamJournalFolderPath
    journalFolderPath = os.path.join(dreamJournalFolderPath, monthAndYear)
    os.makedirs(journalFolderPath, exist_ok=True)
    return journalFolderPath

def get_a_nc_file(monthAndYear, day):
    if type(day) != str:
        day = str(day)
    dreamJournalMonth = get_a_journal(monthAndYear)
    dream = os.path.join(dreamJournalMonth, "day_" + day + ".nc")
    return dream