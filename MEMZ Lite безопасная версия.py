import tkinter as tk
import pygame
import pyautogui
import random
import threading
import sys
import time
import keyboard  # Убедись, что установлена: pip install keyboard

# Набор страшных кракозябр
GLITCH_CHARS = "☠☣⚡⚠𝕾𝕺𝕾☠☣⚙⚔𝕯𝕰𝕬𝕿𝕳☄❄Ψ☠☤𓂺🪓🩸🪱"
COMP_CHARS = "0100110101ABCDEFXYZ[]{}//\\\\$$##@@!!"

def generate_glitch_text():
    length = random.randint(15, 25)
    return "".join(random.choice(GLITCH_CHARS + COMP_CHARS) for _ in range(length))

is_running = True

# Функция экстренного выключения
def emergency_exit():
    global is_running
    is_running = False
    print("\n[!] Рофл-вирус успешно выключен через F4!")
    pygame.quit()
    sys.exit()

# --- ДВИЖЕНИЕ ОКАН ---
def move_window(win, root, dx, dy):
    if not is_running:
        return
    try:
        w = win.winfo_width()
        h = win.winfo_height()
        x = win.winfo_x()
        y = win.winfo_y()
        
        if w <= 1 or h <= 1:
            w, h = 300, 120
            
        new_x = x + dx
        new_y = y + dy
        
        if new_x < 0 or new_x > root.winfo_screenwidth() - w:
            dx = -dx
        if new_y < 0 or new_y > root.winfo_screenheight() - h:
            dy = -dy
            
        win.geometry(f"+{new_x}+{new_y}")
        root.after(16, lambda: move_window(win, root, dx, dy))
    except Exception:
        pass

# --- СПАМ ЛЕТАЮЩИМИ ОКНАМИ ---
def start_tkinter_spam():
    global is_running
    
    root = tk.Tk()
    root.withdraw() 
    
    def spawn_window():
        if not is_running:
            root.destroy()
            return
            
        win = tk.Toplevel(root)
        win.title(generate_glitch_text()[:8])
        win.attributes("-topmost", True)  # Поверх туннеля Pygame!
        
        w, h = 300, 120
        x = random.randint(0, root.winfo_screenwidth() - w)
        y = random.randint(0, root.winfo_screenheight() - h)
        win.geometry(f"{w}x{h}+{x}+{y}")
        
        glitch_text = f"CRITICAL_FAIL:\n{generate_glitch_text()}"
        label = tk.Label(win, text=glitch_text, font=("Courier", 10, "bold"), fg="red", padx=10, pady=10)
        label.pack()
        
        btn = tk.Button(win, text=" OK ", command=lambda: [win.destroy(), spawn_window(), spawn_window()])
        btn.pack(pady=5)
        
        dx = random.choice([-5, -3, 3, 5])
        dy = random.choice([-5, -3, 3, 5])
        
        win.update()
        move_window(win, root, dx, dy)
        
        root.after(1000, spawn_window)

    spawn_window()
    
    while is_running:
        try:
            root.update()
            time.sleep(0.01)
        except Exception:
            break
    try:
        root.destroy()
    except Exception:
        pass

# --- ДРОЖАНИЕ КУРСОРA ---
def mouse_jitter():
    while is_running:
        if random.random() < 0.2:
            try:
                mx, my = pyautogui.position()
                pyautogui.moveTo(mx + random.randint(-25, 25), my + random.randint(-25, 25))
            except Exception:
                pass
        time.sleep(0.03)

# --- ГЛАВНЫЙ ГРАФИЧЕСКИЙ ХОЛСТ (ТУННЕЛЬ И НЕГАТИВ) ---
def start_pure_chaos():
    global is_running
    
    pygame.init()
    screen_info = pygame.display.Info()
    sw, sh = screen_info.current_w, screen_info.current_h
    
    # Открываем жесткое полноэкранное окно, которое закроет всё
    screen = pygame.display.set_mode((sw, sh), pygame.NOFRAME)
    
    # Готовим базовый холст: делаем первичный снимок экрана
    screenshot = pyautogui.screenshot()
    current_surface = pygame.image.fromstring(screenshot.tobytes(), screenshot.size, screenshot.mode)
    
    clock = pygame.time.Clock()
    
    # Горячая клавиша F4 на выключение регистрируется глобально
    keyboard.add_hotkey('f4', emergency_exit)
    
    # Теперь безопасно запускаем окна и мышь
    threading.Thread(target=start_tkinter_spam, daemon=True).start()
    threading.Thread(target=mouse_jitter, daemon=True).start()
    
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        try:
            # Магия туннеля: мы берем предыдущий сгенерированный кадр, а не рабочий стол!
            offset = 15
            new_w = sw - (offset * 2)
            new_h = sh - (offset * 2)
            
            # Сжимаем картинку внутрь
            scaled_img = pygame.transform.smoothscale(current_surface, (new_w, new_h))
            
            # Очищаем холст и вставляем уменьшенную картинку по центру
            current_surface.fill((0, 0, 0))
            current_surface.blit(scaled_img, (offset, offset))
            
            # Эффект инверсии (негатив) каждого кадра на аппаратном уровне
            pxarray = pygame.PixelArray(current_surface)
            pxarray.invert()
            del pxarray
            
            # Выводим безумие на монитор
            screen.blit(current_surface, (0, 0))
            pygame.display.flip()
            
        except Exception as e:
            print(f"Ошибка рендеринга: {e}")
            
        clock.tick(15)  # Ограничение скорости, чтобы туннель затягивало плавно и эпично

    pygame.quit()

if __name__ == "__main__":
    print("=== ЗАПУСК ПОЛНОЙ ИСПРАВЛЕННОЙ ВЕРСИИ ===")
    print("ДЛЯ ОТМЕНЫ НАЖМИ: F4")
    start_pure_chaos()
    sys.exit()
