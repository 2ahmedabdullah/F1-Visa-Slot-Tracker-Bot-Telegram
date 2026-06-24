#website.py
import subprocess
import time
import random
import pyautogui
import threading

# 📍 the CALIBRATED MOUSE COORDINATES & HARDWARE INTERACTION LOCKS
TARGET_X = 426  
TARGET_Y = 520  
mouse_lock = threading.Lock()  

def calculate_bezier_points(start_x, start_y, end_x, end_y):
    """Generates a pure list of explicit (x, y) coordinates using cubic math."""
    p1_x = start_x + (end_x - start_x) * random.uniform(0.25, 0.5) + random.randint(-20, 20)
    p1_y = start_y + (end_y - start_y) * random.uniform(0.25, 0.5) + random.randint(-20, 20)
    
    p2_x = start_x + (end_x - start_x) * random.uniform(0.5, 0.75) + random.randint(-20, 20)
    p2_y = start_y + (end_y - start_y) * random.uniform(0.5, 0.75) + random.randint(-20, 20)

    num_steps = random.randint(18, 32)
    points = []
    
    for t in np.linspace(0, 1, num_steps):
        x = (1-t)**3 * start_x + 3*(1-t)**2 * t * p1_x + 3*(1-t) * t**2 * p2_x + t**3 * end_x
        y = (1-t)**3 * start_y + 3*(1-t)**2 * t * p1_y + 3*(1-t) * t**2 * p2_y + t**3 * end_y
        points.append((int(x), int(y)))
        
    return points

def human_mouse_move(target_x, target_y):
    """Moves the mouse to target coordinates using a randomized natural path."""
    start_x, start_y = pyautogui.position()
    if abs(start_x - target_x) < 2 and abs(start_y - target_y) < 2:
        return
        
    path_points = calculate_bezier_points(start_x, start_y, target_x, target_y)
    for pt_x, pt_y in path_points:
        pyautogui.moveTo(pt_x, pt_y)
        time.sleep(random.uniform(0.008, 0.015)) 

def human_click(target_x, target_y):
    """Moves to target, hovers organically with micro jitter wiggles, and clicks."""
    initial_x = target_x + random.randint(-4, 4)
    initial_y = target_y + random.randint(-4, 4)
    
    human_mouse_move(initial_x, initial_y)
    time.sleep(random.uniform(0.1, 0.2))  
    
    hover_steps = random.randint(2, 3)
    current_x, current_y = initial_x, initial_y
    
    for _ in range(hover_steps):
        wiggle_x = current_x + random.choice([-2, -1, 1, 2])
        wiggle_y = current_y + random.choice([-2, -1, 1, 2])
        
        if abs(wiggle_x - target_x) <= 6 and abs(wiggle_y - target_y) <= 6:
            pyautogui.moveTo(wiggle_x, wiggle_y, duration=random.uniform(0.05, 0.12))
            current_x, current_y = wiggle_x, wiggle_y
            
    time.sleep(random.uniform(0.05, 0.15))  
    
    pyautogui.mouseDown(button='left')
    time.sleep(random.uniform(0.07, 0.14))  
    pyautogui.mouseUp(button='left')



def run_browser_pipeline(browser_name, exe_path, flag):
    url = "https://www.usvisascheduling.com"
    if not os.path.exists(exe_path): return

    print(f"🚀 [Thread-{browser_name}] Launching {browser_name}...")
    try:
        subprocess.Popen([exe_path, flag, url], shell=False)
    except Exception as e:
        print(f"❌ [Thread-{browser_name}] Process Spawn Failure: {e}")
        return

    time.sleep(random.uniform(6.5, 9.5))

    with mouse_lock:
        print(f"🎯 [{browser_name}] Acquired UI hardware control cursor...")
        try:
            human_click(TARGET_X, TARGET_Y)
            time.sleep(random.uniform(1.8, 3.4))
            
            human_click(TARGET_X, TARGET_Y)
            time.sleep(random.uniform(4.1, 6.7))
            
            human_click(TARGET_X, TARGET_Y)
            time.sleep(random.uniform(11.2, 16.4))

            human_click(TARGET_X, TARGET_Y)
            print(f"✅ [{browser_name}] Humanized macro sequence successfully delivered.")
        except Exception as err:
            print(f"⚠️ [Thread-{browser_name}] Humanized mouse control error: {err}")


def open_visa_portals_parallel():
    global BROWSER_PIPELINE_RUNNING
    chrome_exe = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    edge_exe = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    
    try:
        # chrome_thread = threading.Thread(target=run_browser_pipeline, args=("Chrome", chrome_exe, "--incognito"), daemon=True)
        # edge_thread = threading.Thread(target=run_browser_pipeline, args=("Edge", edge_exe, "--inprivate"), daemon=True)
        
        # chrome_thread.start()
        time.sleep(random.uniform(1.5, 3.0)) 
        # edge_thread.start()
        
        time.sleep(45.0)
    finally:
        BROWSER_PIPELINE_RUNNING = False
        print("🔄 [System Engine] Browser automation context cleared. Portal re-auth paths unlocked.")