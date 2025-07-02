"""
防息屏引擎 - 核心逻辑模块
"""

import pyautogui
import threading
import time
import random
import ctypes
from typing import Callable, Optional


class ScreenProtectionEngine:
    """防息屏保护引擎"""
    
    def __init__(self, callback: Optional[Callable[[bool], None]] = None):
        self._running = False
        self._callback = callback
        self._methods = [
            self._mouse_micro_move,
            self._mouse_click_activity, 
            self._keyboard_activity,
            self._system_keep_alive
        ]
    
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
        """工作循环 - 四重防护机制"""
        while self._running:
            try:
                # 随机选择防护方法，增加不可预测性
                method = random.choice(self._methods)
                method()
                
                # 动态间隔：25-45秒（更频繁，更可靠）
                time.sleep(random.randint(25, 45))
                
            except Exception as e:
                print(f"防护引擎错误: {e}")
                self._running = False
                if self._callback:
                    self._callback(False)
                break
    
    def _mouse_micro_move(self):
        """方法1: 鼠标微动"""
        x, y = pyautogui.position()
        offset = random.randint(-2, 2)
        pyautogui.moveTo(x + offset, y + offset, duration=0.1)
    
    def _mouse_click_activity(self):
        """方法2: 鼠标轻微活动（更强信号）"""
        x, y = pyautogui.position()
        pyautogui.moveTo(x + 1, y + 1, duration=0.1)
        pyautogui.scroll(1)
        pyautogui.scroll(-1)  # 恢复滚动位置
    
    def _keyboard_activity(self):
        """方法3: 键盘活动（覆盖只检测键盘的系统）"""
        pyautogui.press('scrolllock')
        time.sleep(0.1)
        pyautogui.press('scrolllock')  # 恢复状态
    
    def _system_keep_alive(self):
        """方法4: 系统级防休眠（Windows API）"""
        try:
            # Windows API: 直接告诉系统保持活跃
            ES_CONTINUOUS = 0x80000000
            ES_DISPLAY_REQUIRED = 0x00000002
            ES_SYSTEM_REQUIRED = 0x00000001
            
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
            )
            
            time.sleep(0.5)
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            
        except:
            # API失败时降级为鼠标移动
            self._mouse_micro_move()
