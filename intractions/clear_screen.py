import os
import platform

# Interface for the screen clearer
class ScreenClearer:
    """
    Abstract class representing the interface for clearing the screen.
    """
    def clear(self):
        pass

# Concrete implementation for Windows
class WindowsScreenClearer(ScreenClearer):
    """
    Concrete implementation of ScreenClearer for Windows operating system.
    """
    def clear(self):
        """
        Clears the screen on Windows.
        """
        os.system('cls')

# Concrete implementation for Mac and Linux
class UnixScreenClearer(ScreenClearer):
    """
    Concrete implementation of ScreenClearer for Unix-like operating systems (Mac, Linux).
    """
    def clear(self):
        """
        Clears the screen on Unix-like operating systems.
        """
        os.system('clear')

# Factory to create the appropriate screen clearer based on the operating system
class ScreenClearerFactory:
    """
    Factory class to create the appropriate ScreenClearer based on the operating system.
    """
    def create_screen_clearer(self):
        """
        Creates a ScreenClearer instance based on the current operating system.
        
        Returns:
            ScreenClearer: Instance of a concrete ScreenClearer subclass.
        """
        system_platform = platform.system().lower()
        if system_platform == 'windows':
            return WindowsScreenClearer()
        else:
            return UnixScreenClearer()

def clear_screen_func():
    """
    Clears the screen based on the current operating system.
    """
    screen_clearer = ScreenClearerFactory().create_screen_clearer()
    screen_clearer.clear()