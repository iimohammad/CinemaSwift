import os
import platform

# Interface for the screen clearer
class ScreenClearer:
    def clear(self):
        pass

# Concrete implementation for Windows
class WindowsScreenClearer(ScreenClearer):
    def clear(self):
        os.system('cls')

# Concrete implementation for Mac and Linux
class UnixScreenClearer(ScreenClearer):
    def clear(self):
        os.system('clear')

# Factory to create the appropriate screen clearer based on the operating system
class ScreenClearerFactory:
    def create_screen_clearer(self):
        system_platform = platform.system().lower()
        if system_platform == 'windows':
            return WindowsScreenClearer()
        else:
            return UnixScreenClearer()

def clear_screen_func():
    screen_clearer = ScreenClearerFactory().create_screen_clearer()
    screen_clearer.clear()