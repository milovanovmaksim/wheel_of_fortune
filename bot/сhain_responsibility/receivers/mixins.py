from gui.keybord.keyboard import Keyboard
from gui.menu.menu import Menu


class MenuMixins:
    def set_buttons(self):
        self.buttons = self.get_menu()

    def get_menu(self):
        menu = Menu()
        buttons = menu.buttons
        return buttons


class KeyboardMixin:
    def get_keyboard(self):
        menu = Keyboard()
        return menu.buttons
