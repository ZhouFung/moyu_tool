"""
防息屏引擎 - 核心逻辑模块
"""

import pyautogui
import threading
import time
import random
from typing import Callable, Optional


class ScreenProtectionEngine:
    """防息屏保护引擎"""
    
    def __init__(self, callback: Optional[Callable[[bool], None]] = None):
        self._running = False
        self._callback = callback
        self._params = {
            'move_range': 2,
            'min_interval': 30,
            'max_interval': 60,
            'duration': 0.1
        }
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    def toggle_protection(self) -> bool:
        """切换保护状态"""
        self._running = not self._running
        if self._running:
            threading.Thread(target=self._work_loop, daemon=True).start()
        
        if self._callback:
            self._callback(self._running)
        return self._running
    
    def _work_loop(self):
        """工作循环"""
        while self._running:
            try:
                self._perform_micro_movement()
                time.sleep(random.randint(self._params['min_interval'], self._params['max_interval']))
            except Exception as e:
                print(f"引擎错误: {e}")
                self._running = False
                if self._callback:
                    self._callback(False)
                break
    
    def _perform_micro_movement(self):
        """执行微动"""
        x, y = pyautogui.position()
        offset = lambda: random.randint(-self._params['move_range'], self._params['move_range'])
        pyautogui.moveTo(x + offset(), y + offset(), duration=self._params['duration'])
