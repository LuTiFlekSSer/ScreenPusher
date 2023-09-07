import telebot
import time
import win32api
import config
import pyscreenshot


class ScreenPusher:
    def __init__(self, token, user_list):
        self._BOT = telebot.TeleBot(token=token)
        self._USER_LIST = user_list

    def _make_screenshot(self, path_for_save='./tmp.jpg'):
        screenshot = pyscreenshot.grab()
        screenshot.save(path_for_save)

    def _notify_users(self, text='', path_to_img='./tmp.jpg'):
        with open(path_to_img, 'rb') as img:
            for user in self._USER_LIST:
                try:
                    self._BOT.send_document(user, img, caption=text)
                except Exception:
                    pass

    def screenshot_worker(self, text="Новый скриншот"):
        while True:
            time.sleep(0.1)
            if win32api.GetKeyState(0x04) < 0:
                try:
                    self._make_screenshot()
                    self._notify_users(text=text)
                except Exception as e:
                    self._notify_users(text=f"Произошла ошибка: {e}")

            if win32api.GetKeyState(0x79) < 0:
                break


if __name__ == '__main__':
    sp = ScreenPusher(token=config.BOT_TOKEN, user_list=config.USER_LIST)
    sp.screenshot_worker(text=config.TEXT_FOR_SEND)
