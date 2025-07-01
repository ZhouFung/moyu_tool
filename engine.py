"""
防息屏引擎 - 核心逻辑模块
处理系统保持活跃的核心功能
"""

import pyautogui
import threading
import time
import random
from typing import Callable, Optional


class ScreenProtectionEngine:
    """防息屏保护引擎"""
    
    def __init__(self, status_callback: Optional[Callable[[bool], None]] = None):
        """
        初始化保护引擎
        
        Args:
            status_callback: 状态变化回调函数
        """
        self._is_running = False
        self._worker_thread = None
        self._status_callback = status_callback
        
        # 工作参数
        self.move_range = 2  # 鼠标移动范围（像素）
        self.min_interval = 30  # 最小间隔（秒）
        self.max_interval = 60  # 最大间隔（秒）
        self.move_duration = 0.1  # 移动持续时间（秒）
    
    @property
    def is_running(self) -> bool:
        """获取运行状态"""
        return self._is_running
    
    def start_protection(self) -> bool:
        """
        启动防息屏保护
        
        Returns:
            bool: 启动是否成功
        """
        if self._is_running:
            return False
            
        self._is_running = True
        self._worker_thread = threading.Thread(target=self._protection_worker, daemon=True)
        self._worker_thread.start()
        
        if self._status_callback:
            self._status_callback(True)
            
        return True
    
    def stop_protection(self) -> bool:
        """
        停止防息屏保护
        
        Returns:
            bool: 停止是否成功
        """
        if not self._is_running:
            return False
            
        self._is_running = False
        
        if self._status_callback:
            self._status_callback(False)
            
        return True
    
    def toggle_protection(self) -> bool:
        """
        切换保护状态
        
        Returns:
            bool: 切换后的状态
        """
        if self._is_running:
            self.stop_protection()
        else:
            self.start_protection()
        return self._is_running
    
    def _protection_worker(self):
        """保护工作线程"""
        while self._is_running:
            try:
                # 获取当前鼠标位置
                current_x, current_y = pyautogui.position()
                
                # 计算微小的移动偏移
                offset_x = random.randint(-self.move_range, self.move_range)
                offset_y = random.randint(-self.move_range, self.move_range)
                
                # 执行微小移动
                pyautogui.moveTo(
                    current_x + offset_x,
                    current_y + offset_y,
                    duration=self.move_duration
                )
                
                # 随机间隔等待
                sleep_time = random.randint(self.min_interval, self.max_interval)
                time.sleep(sleep_time)
                
            except Exception as e:
                # 发生错误时停止保护
                print(f"保护引擎错误: {e}")
                self._is_running = False
                if self._status_callback:
                    self._status_callback(False)
                break
    
    def get_status_info(self) -> dict:
        """
        获取状态信息
        
        Returns:
            dict: 包含状态信息的字典
        """
        return {
            'is_running': self._is_running,
            'move_range': self.move_range,
            'interval_range': f"{self.min_interval}-{self.max_interval}秒",
            'move_duration': self.move_duration
        }
