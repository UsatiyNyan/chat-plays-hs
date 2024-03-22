from dataclasses import dataclass

import pyautogui

from cph.utils.vec import Vec2


@dataclass
class WindowBB:
    begin: Vec2
    end: Vec2

    @property
    def width(self) -> int:
        return self.end.x - self.begin.x

    @property
    def height(self) -> int:
        return self.end.y - self.begin.y


def click(window: WindowBB, point: Vec2, button: str) -> bool:
    assert window.width > point.x
    assert window.height > point.y
    try:
        x = window.begin.x + point.x
        y = window.begin.y + point.y
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click(x, y, button=button)
        return True
    except pyautogui.FailSafeException:
        return False
