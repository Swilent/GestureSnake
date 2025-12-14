"""
UI管理模块
负责处理所有UI相关的显示和更新
"""

import cvzone
import time
from collections import deque
from game_config import *


class UIManager:
    """UI管理器类"""

    def __init__(self):
        """初始化UI管理器"""
        self.fps = 0
        self.last_fps_update = 0
        self.frame_times = deque(maxlen=10)

    def update_fps(self, frame_start_time, frame_count):
        """更新FPS计算"""
        frame_time = time.time() - frame_start_time
        self.frame_times.append(frame_time)

        # 每FPS_UPDATE_INTERVAL帧更新一次显示
        if frame_count - self.last_fps_update >= FPS_UPDATE_INTERVAL:
            if len(self.frame_times) > 0:
                avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                self.fps = 1 / avg_frame_time if avg_frame_time > 0 else 0
            self.last_fps_update = frame_count

    def draw_score(self, imgMain, score):
        """绘制得分"""
        cvzone.putTextRect(imgMain, f'Score: {score}', UI_SCORE_POSITION,
                           scale=UI_SCORE_SCALE, thickness=5, offset=10)

    def draw_restart_hint(self, imgMain):
        """绘制重新开始提示"""
        cvzone.putTextRect(imgMain, 'Press R to restart', UI_RESTART_POSITION,
                           scale=1, thickness=2, offset=5)

    def draw_fps(self, imgMain):
        """绘制FPS"""
        cvzone.putTextRect(imgMain, f'FPS: {self.fps:.1f}',
                           UI_FPS_POSITION,
                           scale=1, thickness=2, offset=5)

    def draw_hand_status(self, imgMain, hands):
        """绘制手势检测状态"""
        if hands:
            cvzone.putTextRect(imgMain, "✓ Hand Detected",
                               UI_HAND_STATUS_POSITION,
                               scale=1, thickness=2, offset=5, colorR=(0, 200, 0))
        else:
            cvzone.putTextRect(imgMain, "✗ No Hand Detected",
                               UI_HAND_STATUS_POSITION,
                               scale=1, thickness=2, offset=5, colorR=(0, 0, 200))

    def draw_game_over(self, imgMain, score):
        """绘制游戏结束画面"""
        cvzone.putTextRect(imgMain, "GAME OVER",
                           GAME_OVER_POSITION,
                           scale=GAME_OVER_SCALE, thickness=5, offset=20)
        cvzone.putTextRect(imgMain, f'Final Score: {score}',
                           FINAL_SCORE_POSITION,
                           scale=FINAL_SCORE_SCALE, thickness=4, offset=15)