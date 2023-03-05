import os
import re
from collections import namedtuple
from screeninfo import get_monitors

STEAM_PATH = '...' # Путь к папке Steam
STEAM_APP = STEAM_PATH + '\\steam.exe'
GAME_CONFIG = STEAM_PATH + '\\userdata\\143355847\\config\\localconfig.vdf'
GAME_ID = '1046930'


def main():
    def get_resolution():
        Resolution = namedtuple('Resolution', ['width', 'height'])
        for m in get_monitors():
            if m.is_primary:
                return Resolution(str(m.width), str(m.height))

    def change_config(monitor_resolution):
        width, height = monitor_resolution.width, monitor_resolution.height
        with open(GAME_CONFIG, 'r') as config:
            input_text = config.read()

        pattern = r'("1046930"\s*{[^()]+"LaunchOptions"\s+)"([^"]*)"'
        match = re.search(pattern, input_text)
        if match:
            inner_pattern = r'-w\s(\d+)\s+-h\s(\d+)'
            inner_match = re.search(inner_pattern, match.group(2))
            if inner_match:
                if inner_match.group(1) == width and inner_match.group(2) == height:
                    return False
            result_text = input_text.replace(match.group(0), f'{match.group(1)}"-w {width} -h {height}"')
        else:
            pattern = r'"1046930"\n\t*{(\n\t+)'
            match = re.search(pattern, input_text)
            if match:
                result_text = input_text.replace(
                    match.group(0), match.group(0) + f'"LaunchOptions"		"-w {width} -h {height}"' + match.group(1)
                )
        with open(GAME_CONFIG, 'w') as config:
            config.write(result_text)
            return True

    if change_config(get_resolution()):
        os.system('taskkill /f /IM steam.exe')
    os.system(f'start {STEAM_APP}')


if __name__ == '__main__':
    main()
