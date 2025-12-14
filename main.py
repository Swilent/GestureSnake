"""
主程序入口
整合所有模块，运行贪吃蛇游戏
"""

import cv2
import time
from game_config import *
from snake_game import SnakeGame
from ui_manager import UIManager
from hand_detector import HandDetectionManager


def main():
    """主游戏函数"""
    print("=" * 50)
    print("贪吃蛇游戏 - 模块化版本")
    print("=" * 50)
    print("游戏开始！移动食指控制蛇的方向")
    print("按 R 键重新开始")
    print("按 ESC 或 Q 退出游戏")
    print("=" * 50)

    # 初始化各个模块
    try:
        hand_manager = HandDetectionManager()
        game = SnakeGame()
        ui_manager = UIManager()
    except Exception as e:
        print(f"初始化失败: {e}")
        return

    # 游戏主循环
    frame_count = 0
    frame_delay = 1000 // TARGET_FPS  # 毫秒

    while True:
        frame_start_time = time.time()

        # 获取摄像头帧和手势
        result = hand_manager.get_frame_and_hands()
        if result[0] is None:
            print("无法读取摄像头")
            break

        img, hands, pointIndex = result

        # 处理手势输入
        if hands and not game.gameOver:
            currentHead = pointIndex
        elif not game.gameOver:
            # 如果没有检测到手势但游戏未结束，保持蛇头不动
            currentHead = game.previousHead if game.previousHead != (0, 0) else (100, 100)
        else:
            currentHead = game.previousHead

        # 更新游戏状态
        if game.gameOver:
            # 游戏结束画面
            ui_manager.draw_game_over(img, game.score)
            ui_manager.draw_hand_status(img, hands)
        else:
            # 更新蛇身
            game.update_snake_body(currentHead)

            # 检测碰撞
            if game.check_food_collision(currentHead):
                pass  # 更新已在函数内部完成

            if game.check_self_collision(currentHead, frame_count):
                game.gameOver = True
                print(f"Game Over! Final Score: {game.score}")

            # 绘制游戏元素
            game.draw_snake(img)
            game.draw_food(img)

            # 绘制UI
            ui_manager.draw_score(img, game.score)
            ui_manager.draw_restart_hint(img)
            ui_manager.draw_fps(img)
            ui_manager.draw_hand_status(img, hands)

        # 更新FPS
        ui_manager.update_fps(frame_start_time, frame_count)

        # 显示画面
        cv2.imshow("Snake Game - Modular Version", img)

        # 处理按键输入
        key = cv2.waitKey(max(1, frame_delay - int((time.time() - frame_start_time) * 1000)))

        if key in [27, ord('q'), ord('Q')]:  # ESC或Q退出
            print("游戏退出")
            break
        elif key == ord('r') or key == ord('R'):  # R重新开始
            game.reset_game()
            print("游戏已重置")

        frame_count += 1

    # 清理资源
    hand_manager.release()
    cv2.destroyAllWindows()
    print("游戏结束")


if __name__ == "__main__":
    main()