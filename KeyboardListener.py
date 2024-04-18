from pynput import keyboard
import config


def on_press(key):
    try:
        if str(key) ==  r"'\x03'" or str(key) == r"'\x1a'":
            config.main_stop_flag = True
            config.listener_stop_flag = True
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc or config.listener_stop_flag:
        # 停止监听
        return False

# 创建监听器
def Listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    Listener()
