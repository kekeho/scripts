#!/usr/bin/env python3
import sys
import json
import openpyxl as px


def load_setting(setting_file_path):
    """setting go2jsl from settings.json

    Keywords arguments:
    setting_file_path -- Full path of settings.json
    """
    setting_json = open(setting_file_path, mode='r')
    settings_info = json.load(setting_json)

    return settings_info


def main():
    """main
    """
    load_setting("settings.json")


if __name__ == '__main__':
    main()
