# from fourier_grx.sdk.gamepad_controller import GamePad
import time
from fourier_core.operator.gamepad_controller import GamePad

# fourier-core/fourier_core/operator/gamepad_controller.py
if __name__ == "__main__":
    gamepad = GamePad()
    gamepad.start()
    try:
        while True:
            res = gamepad.read() 
            print(res)
            time.sleep(0.01)
    except KeyboardInterrupt:
        gamepad.stop()
