"""
手势检测模块
负责处理摄像头和手势检测
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
from game_config import *


class HandDetectionManager:
    """手势检测管理器"""

    def __init__(self):
        """初始化手势检测"""
        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("无法打开摄像头")

        # 设置摄像头参数
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)

        # 初始化手势检测器
        self.detector = HandDetector(
            detectionCon=HAND_DETECTION_CONFIDENCE,
            maxHands=MAX_HANDS
        )

    def get_frame_and_hands(self):
        """获取摄像头帧和检测手势"""
        # 读取帧
        success, img = self.cap.read()
        if not success:
            return None, None, None

        # 水平翻转
        img = cv2.flip(img, 1)

        # 检测手势
        hands, img = self.detector.findHands(img, flipType=False)

        # 获取食指位置
        if hands:
            lmList = hands[0]['lmList']
            pointIndex = tuple(lmList[8][0:2])
        else:
            pointIndex = None

        return img, hands, pointIndex

    def release(self):
        """释放资源"""
        if self.cap:
            self.cap.release()