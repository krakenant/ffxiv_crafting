from python_imagesearch.imagesearch import imagesearch, region_grabber, imagesearcharea
from typing import Tuple, List
import pyautogui
from time import sleep
from datetime import datetime


def search_crafting_log(max_res: Tuple[int, int, int, int], timeout: int = 5):
    print('looking if crafting log is up')
    c = 0
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        im = region_grabber(max_res)
        pos = imagesearcharea("images/crafting/crafting_log.png", max_res[0], max_res[1], max_res[2], max_res[3], .8, im)
        if pos[0] != -1:
            print('crafting log window found')
            return True
        sleep(.1)
        c += 1
        t2 = datetime.now()
    return False


def click_synthesize(max_res: Tuple[int, int, int, int], timeout: int = 2):

    c = 0
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        im = region_grabber(max_res)
        pos = imagesearcharea("images/crafting/synthesize.png", max_res[0], max_res[1], max_res[2], max_res[3], .8, im)
        if pos[0] != -1:
            print('clicking synthesis')
            click_pos = (pos[0] + 40, pos[1] + 20)
            pyautogui.moveTo(click_pos[0], click_pos[1], duration=.05)
            sleep(.1)
            #pyautogui.leftClick(duration=.05)
            pyautogui.mouseDown()
            sleep(.01)
            pyautogui.mouseUp()
            return True
        sleep(.1)
        c += 1
    return False


def search_for_collectible_window(max_res: Tuple[int, int, int, int]):
    im = region_grabber(max_res)
    pos = imagesearcharea("images/crafting/yes_no_collectible.png", max_res[0], max_res[1], max_res[2], max_res[3], .95, im)
    if pos[0] != -1:
        return True, pos
    else:
        return False, None


def search_for_crafting_window(max_res: Tuple[int, int, int, int], timeout: int = 2, sleep_time: int = .1, crafting: bool = False):
    print('making sure crafting window is up')
    c = 0
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        im = region_grabber(max_res)
        pos = imagesearcharea("images/crafting/crafting_window.png", max_res[0], max_res[1], max_res[2], max_res[3], .8, im)
        if pos[0] != -1:
            if crafting:
                # print('Since crafting sleeping and checking again')
                sleep(sleep_time)
                collectible_window = search_for_collectible_window(max_res=max_res)
                if collectible_window[0]:
                    pos2 = collectible_window[1]
                    click_pos = (pos2[0] + 40, pos2[1] + 20)
                    print(click_pos)
                    pyautogui.moveTo(click_pos[0], click_pos[1], duration=.05)
                    pyautogui.mouseDown()
                    sleep(.01)
                    pyautogui.mouseUp()
                t2 = datetime.now()
            else:
                return True
        else:
            if crafting:
                return False
            sleep(sleep_time)
            c += 1
            t2 = datetime.now()
    print(f'Crafting window not found after {t2 - t1} seconds')
    return False


def escape(max_res: Tuple[int, int, int, int]):
    print('escaping')
    c = 0
    escape_window = False
    while c < 20:
        im = region_grabber(max_res)
        pos = imagesearcharea("images/escape_window.png", max_res[0], max_res[1], max_res[2], max_res[3], .8, im)
        if pos[0] != -1:
            escape_window = True
            pyautogui.press('esc')
        elif escape_window:
            print('escape window found and closed')
            return True
        else:
            print(f'escape window not found {c} times - pressing esc')
            pyautogui.press('esc')
        sleep(.5)
        c += 1
    return False


def main():
    runs = int(pyautogui.prompt(text='How many runs?', default=0))
    print(f'Must have crafting log up and on the recipe you want to make')
    wt = 4
    for i in range(wt):
        print(f'starting in {wt - i}')
        sleep(1)
    size_raw = pyautogui.size()
    max_res = (0, 0, size_raw[0], size_raw[1])
    crafting = True
    crun = 1
    while crafting:
        if crun >= runs and runs != 0:
            crafting = False
        crun += 1
        complete = False
        t1 = datetime.now()
        t5 = datetime.now()
        key_list: List[int] = []
        crafting_log = search_crafting_log(max_res=max_res)
        if crafting_log:
            synth_click = click_synthesize(max_res=max_res)
            if synth_click:
                craft_window = search_for_crafting_window(max_res=max_res)
                if craft_window:
                    sleep(.2)
                    print('Pressing -')
                    pyautogui.press('-')
                    craft_start = datetime.now()
                    craft_time = datetime.now() - craft_start
                    while craft_time.seconds < 50 and craft_window:
                        craft_window = search_for_crafting_window(max_res=max_res, timeout=50, sleep_time=1, crafting=True)

                        craft_time = datetime.now() - craft_start
                    print(craft_window)
                    if not craft_window:
                        complete = True

        if not complete:
            escape_failed = escape(max_res=max_res)
            if not escape_failed:
                print('something went really wrong - ending')
            crafting = False
    return


main()
