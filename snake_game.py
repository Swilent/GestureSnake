"""
贪吃蛇游戏核心逻辑
包含游戏类和所有游戏相关的功能
"""

import math
import random
import cvzone
import cv2
import numpy as np
from collections import deque
from game_config import *


class SnakeGame:
    """贪吃蛇游戏类"""

    def __init__(self):
        """初始化游戏"""
        # 蛇身相关属性
        self.points = []  # 存储蛇身点
        self.lengths = []  # 存储每段的长度
        self.currentLength = 0
        self.allowedLength = INITIAL_LENGTH
        self.previousHead = (0, 0)

        # 性能优化相关
        self.points_array = None  # 用于存储转换后的点数组
        self.last_points_count = 0  # 记录上次的点数量

        # 食物相关属性
        self.imgFood = cv2.imread(FOOD_IMAGE, cv2.IMREAD_UNCHANGED)
        if self.imgFood is None:
            raise FileNotFoundError(f"无法加载食物图片: {FOOD_IMAGE}")
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = self.randomFoodLocation()

        # 游戏状态
        self.score = 0
        self.gameOver = False

        # 性能监控
        self.lastCollisionCheck = 0
        self.frame_times = deque(maxlen=10)  # 存储最近10帧的时间用于计算平均FPS

    def randomFoodLocation(self):
        """生成随机的食物位置"""
        x = random.randint(FOOD_MARGIN, SCREEN_WIDTH - FOOD_MARGIN)
        y = random.randint(FOOD_MARGIN, SCREEN_HEIGHT - FOOD_MARGIN)
        return (x, y)

    def update_snake_body(self, currentHead):
        """更新蛇身"""
        cx, cy = currentHead
        px, py = self.previousHead

        # 如果是第一个点，直接添加
        if self.previousHead == (0, 0):
            self.points.append([cx, cy])
            self.lengths.append(0)
            self.previousHead = (cx, cy)
            self.last_points_count = len(self.points)
            return

        # 计算移动距离
        distance = math.hypot(cx - px, cy - py)

        # 如果有足够移动才添加新点
        if distance > MIN_MOVE_DISTANCE:
            self.points.append([cx, cy])
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = (cx, cy)

            # 长度控制
            while self.currentLength > self.allowedLength and len(self.points) > 1:
                self.currentLength -= self.lengths[0]
                self.points.pop(0)
                self.lengths.pop(0)

    def check_food_collision(self, currentHead):
        """检查是否吃到食物"""
        cx, cy = currentHead
        fx, fy = self.foodPoint

        if (fx - self.wFood // 2 < cx < fx + self.wFood // 2 and
            fy - self.hFood // 2 < cy < fy + self.hFood // 2):
            self.foodPoint = self.randomFoodLocation()
            self.allowedLength += LENGTH_INCREASE
            self.score += 1
            return True
        return False

    def check_self_collision(self, currentHead, frame_count):
        """检查自碰撞"""
        # 限制检测频率
        if frame_count - self.lastCollisionCheck < COLLISION_CHECK_INTERVAL:
            return False

        self.lastCollisionCheck = frame_count

        if len(self.points) < 4:
            return False

        cx, cy = currentHead

        # 创建多边形点进行碰撞检测
        pts = np.array(self.points[:-2], np.int32)
        pts = pts.reshape((-1, 1, 2))

        minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

        return -1 <= minDist <= 1

    def draw_snake(self, imgMain):
        """绘制蛇身"""
        if len(self.points) > 1:
            # 优化：复用numpy数组
            if self.points_array is None or len(self.points) != self.last_points_count:
                self.points_array = np.array(self.points, dtype=np.int32)
                self.last_points_count = len(self.points)
            else:
                self.points_array[:] = np.array(self.points, dtype=np.int32)

            # 使用polylines绘制整个蛇身
            cv2.polylines(imgMain, [self.points_array], False,
                         SNAKE_COLOR, SNAKE_THICKNESS)

            # 绘制蛇头
            head = tuple(self.points_array[-1])
            cv2.circle(imgMain, head, HEAD_RADIUS, HEAD_COLOR, cv2.FILLED)

        elif len(self.points) == 1:
            cv2.circle(imgMain, tuple(self.points[0]), HEAD_RADIUS,
                      HEAD_COLOR, cv2.FILLED)

    def draw_food(self, imgMain):
        """绘制食物"""
        fx, fy = self.foodPoint
        imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                   (fx - self.wFood // 2, fy - self.hFood // 2))

    def reset_game(self):
        """重置游戏状态"""
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = INITIAL_LENGTH
        self.previousHead = (0, 0)
        self.score = 0
        self.gameOver = False
        self.foodPoint = self.randomFoodLocation()
        self.points_array = None
        self.last_points_count = 0