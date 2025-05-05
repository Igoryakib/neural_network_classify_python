import tkinter as tk
import ctypes
import locale
import time
import threading
import i18n
import os
import json
import logging

LANG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang')
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('i18n_app')

i18n.load_path.append(LANG_DIR)
i18n.set('filename_format', '{locale}.json')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')  
i18n.set('enable_memoization', True) 

LANG_MAP = {
    'uk_UA': 'uk',
    'en_GB': 'en',
    'en_US': 'en'
}


def get_translation(key, locale='en'):
    try:
        file_path = os.path.join(LANG_DIR, f"{locale}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                if key in translations:
                    return translations[key]
        return f"[{key}]"
    except Exception as e:
        # logger.error(f"Помилка при отриманні перекладу напряму: {str(e)}")
        return f"[{key}]"


def set_language_by_locale(locale_code):
    lang = LANG_MAP.get(locale_code, 'en')
    i18n.set('locale', lang)
    print(f"[DEBUG] Встановлена мова: {lang}")
    print(f"[DEBUG] Переклад 'title': {i18n.t('title')}")
    

def update_ui_texts():
    logger.info("Оновлення інтерфейсу користувача")
    current_locale = i18n.get('locale')
    logger.info(f"Поточна локаль при оновленні UI: {current_locale}")
    
    # Отримуємо текст заголовка напряму з файлу
    title_text = get_translation('title', current_locale)
    logger.info(f"Заголовок вікна: {title_text}")
    root.title(title_text)
    
    # Отримуємо текст мітки напряму з файлу
    label_text = get_translation('labelT', current_locale)
    logger.info(f"Текст мітки: {label_text}")
    label.config(text=label_text)
    
    # Скидаємо меню
    root.config(menu=None)

    # Оновлюємо меню
    create_menu()

def create_menu():
    logger.info("Створення меню")
    global menu_bar, menu_file, menu_controls, menu_playlist, menu_view, menu_help
    
    current_locale = i18n.get('locale')
    
    menu_bar = tk.Menu(root)

    # File menu
    menu_file = tk.Menu(menu_bar, tearoff=0)
    file_text = get_translation('file1', current_locale)
    menu_file.add_command(label=file_text, accelerator="Ctrl+O",
                         command=lambda: label.config(text=file_text))
    
    menubar_text = get_translation('menuBar1', current_locale)
    menu_bar.add_cascade(label=menubar_text, menu=menu_file)
    
    # Controls menu
    menu_controls = tk.Menu(menu_bar, tearoff=0)
    control_keys = ['Control1', 'Control2', 'Control3', 'Control4']
    for key in control_keys:
        control_text = get_translation(key, current_locale)
        menu_controls.add_command(label=control_text, 
                                  command=lambda t=control_text: label.config(text=t))
    
    menubar_text = get_translation('menuBar2', current_locale)
    menu_bar.add_cascade(label=menubar_text, menu=menu_controls)
    
    # Playlist menu
    menu_playlist = tk.Menu(menu_bar, tearoff=0)
    playlist_items = [
        ('playlist1', 'labelPl1'),
        ('file1', 'labelPl2'),
        ('playlist2', 'labelPl3')
    ]
    
    for menu_key, label_key in playlist_items:
        menu_text = get_translation(menu_key, current_locale)
        label_text = get_translation(label_key, current_locale)
        menu_playlist.add_command(label=menu_text, 
                                  command=lambda t=label_text: label.config(text=t))
    
    menubar_text = get_translation('menuBar3', current_locale)
    menu_bar.add_cascade(label=menubar_text, menu=menu_playlist)
    
    # View menu
    menu_view = tk.Menu(menu_bar, tearoff=0)
    dark_text = get_translation('themeD', current_locale)
    menu_view.add_radiobutton(label=dark_text, value="Dark", variable=themeVar,
                             command=lambda: label.config(text=dark_text, bg="black", fg="white"))
    
    light_text = get_translation('themeL', current_locale)
    menu_view.add_radiobutton(label=light_text, value="Light", variable=themeVar,
                             command=lambda: label.config(text=light_text, bg="white", fg="black"))
    
    menubar_text = get_translation('menuBar4', current_locale)
    menu_bar.add_cascade(label=menubar_text, menu=menu_view)
    
    # Help menu
    menu_help = tk.Menu(menu_bar, tearoff=0)
    help_text = get_translation('menuBar5', current_locale)
    menu_help.add_command(label=help_text, 
                         command=lambda: label.config(text=help_text))
    menu_bar.add_cascade(label=help_text, menu=menu_help)

    root.config(menu=menu_bar)

def get_current_language():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    kbd_layout = user32.GetKeyboardLayout(thread_id)
    lang_id = kbd_layout & 0xFFFF
    locale_code = locale.windows_locale.get(lang_id)
    logger.debug(f"Поточна розкладка: {locale_code}")
    return locale_code

def watch_language_change(interval=0.5):
    last_lang = None
    while True:
        current_lang = get_current_language()
        if current_lang != last_lang and current_lang in LANG_MAP:
            logger.info(f"Розкладка змінена на: {current_lang}")
            last_lang = current_lang
            
            # Викликаємо в головному потоці Tkinter
            root.after(0, lambda: set_language_by_locale(last_lang))
            root.after(10, update_ui_texts)
        time.sleep(interval)

# Основна функція для запуску програми
def main():
    global root, label, themeVar
    
    logger.info("Запуск програми")
    
    # Перевіряємо файли перекладу
    # check_translation_files()
    
    # Встановлюємо початкову мову 
    initial_locale = get_current_language() or 'en_US'
    logger.info(f"Початкова локаль: {initial_locale}")
    set_language_by_locale(initial_locale)
    
    # Створюємо головне вікно
    root = tk.Tk()
    
    # Отримуємо переклад для заголовка вікна
    title_text = get_translation('title', i18n.get('locale'))
    root.title(title_text)
    root.geometry("570x400+350+0")
    
    # Змінні для теми
    themeVar = tk.StringVar(value=get_translation('themeL', i18n.get('locale')))
    
    # Створюємо основний віджет мітки
    label = tk.Label(
        text=get_translation('labelT', i18n.get('locale')),
        bg="white",
        width=35,
        height=15,
        bd=0,
        relief="solid",
        font=("Arial", 10),
    )
    label.pack(padx=5, pady=55)
    
    # Створюємо меню
    create_menu()
    
    # Запускаємо потік для відстеження зміни мови
    threading.Thread(target=watch_language_change, daemon=True).start()
    
    # Запускаємо головний цикл Tkinter
    logger.info("Запуск головного циклу Tkinter")
    root.mainloop()

if __name__ == "__main__":
    main()

# def update_ui_texts():
#     root.title(i18n.t('title'))
#     label.config(text=i18n.t('labelT'))

    
#     root.config(menu=None)

   
#     global menu_bar, menu_file, menu_controls, menu_playlist, menu_view, menu_help

#     menu_bar = tk.Menu(root)

#     # File
#     menu_file = tk.Menu(menu_bar, tearoff=0)
#     menu_file.add_command(label=i18n.t('file1'), accelerator="Ctrl+O",
#                           command=lambda: label.config(text=i18n.t('file1')))
#     menu_bar.add_cascade(label=i18n.t('menuBar1'), menu=menu_file)

#     # Controls
#     menu_controls = tk.Menu(menu_bar, tearoff=0)
#     menu_controls.add_command(label=i18n.t('Control1'), command=lambda: label.config(text=i18n.t('Control1')))
#     menu_controls.add_command(label=i18n.t('Control2'), command=lambda: label.config(text=i18n.t('Control2')))
#     menu_controls.add_command(label=i18n.t('Control3'), command=lambda: label.config(text=i18n.t('Control3')))
#     menu_controls.add_command(label=i18n.t('Control4'), command=lambda: label.config(text=i18n.t('Control4')))
#     menu_bar.add_cascade(label=i18n.t('menuBar2'), menu=menu_controls)

#     # Playlist
#     menu_playlist = tk.Menu(menu_bar, tearoff=0)
#     menu_playlist.add_command(label=i18n.t('playlist1'), command=lambda: label.config(text=i18n.t('labelPl1')))
#     menu_playlist.add_command(label=i18n.t('file1'), command=lambda: label.config(text=i18n.t('labelPl2')))
#     menu_playlist.add_command(label=i18n.t('playlist2'), command=lambda: label.config(text=i18n.t('labelPl3')))
#     menu_bar.add_cascade(label=i18n.t('menuBar3'), menu=menu_playlist)

#     # View
#     menu_view = tk.Menu(menu_bar, tearoff=0)
#     menu_view.add_radiobutton(label=i18n.t('themeD'), value="Dark", variable=themeVar,
#                               command=lambda: label.config(text="Dark", bg="black", fg="white"))
#     menu_view.add_radiobutton(label=i18n.t('themeL'), value="Light", variable=themeVar,
#                               command=lambda: label.config(text=i18n.t('themeL'), bg="white", fg="black"))
#     menu_bar.add_cascade(label=i18n.t('menuBar4'), menu=menu_view)

#     # Help
#     menu_help = tk.Menu(menu_bar, tearoff=0)
#     menu_help.add_command(label=i18n.t('menuBar5'), command=lambda: label.config(text=i18n.t('menuBar5')))
#     menu_bar.add_cascade(label=i18n.t('menuBar5'), menu=menu_help)

#     root.config(menu=menu_bar)



# def get_current_language():
#     user32 = ctypes.windll.user32
#     hwnd = user32.GetForegroundWindow()
#     thread_id = user32.GetWindowThreadProcessId(hwnd, None)
#     kbd_layout = user32.GetKeyboardLayout(thread_id)
#     lang_id = kbd_layout & 0xFFFF
#     return locale.windows_locale.get(lang_id)


# def watch_language_change(interval=0.5):
#     last_lang = None
#     while True:
#         current_lang = get_current_language()
#         if current_lang != last_lang:
#             print(f"Розкладка змінена на: {current_lang}")
#             last_lang = current_lang
#             set_language_by_locale(last_lang)
#             root.after(0, update_ui_texts)
#         time.sleep(interval)

# threading.Thread(target=watch_language_change, daemon=True).start()

# root = tk.Tk()
# root.title(i18n.t('title'))
# root.geometry("570x400+350+0")

# border = tk.IntVar(value=0)
# bg_color = tk.StringVar(value=i18n.t('themeL'))

# label = tk.Label(
#  text=i18n.t('labelT'),
#  bg="white",
#  width=35,
#  height=15,
#  bd=0,
#  relief="solid",
#  font=("Arial", 10),
#  )
# label.pack(padx=5, pady=55)


# #menu bar
# menu_bar = tk.Menu(root)
# menu_file = tk.Menu(menu_bar, tearoff=0)
# themeVar = tk.StringVar(value=i18n.t('themeL'))

# #file
# menu_file.add_command(
#  label=i18n.t('file1'),
#  accelerator="Ctrl+O",
#  command=lambda: label.config(text=i18n.t('file1'))
# )

# menu_bar.add_cascade(
#  label=i18n.t('menuBar1'),
#  menu=menu_file
# )
# #controls
# menu_controls = tk.Menu(menu_bar, tearoff=0)
# menu_controls.add_command(
#  label=i18n.t('Control1'),
#  command=lambda: label.config(text=i18n.t('Control1'))
# )
# menu_controls.add_command(
#  label=i18n.t('Control2'),
#  command=lambda: label.config(text=i18n.t('Control2'))
# )
# menu_controls.add_command(
#  label=i18n.t('Control3'),
#  command=lambda: label.config(text=i18n.t('Control3'))
# )
# menu_controls.add_command(
#  label=i18n.t('Control4'),
#  command=lambda: label.config(text=i18n.t('Control4'))
# )
# menu_bar.add_cascade(
#  label=i18n.t('menuBar2'),
#  menu=menu_controls
# )
# #playlist
# menu_playlist = tk.Menu(menu_bar, tearoff=0)
# menu_playlist.add_command(
#  label=i18n.t('playlist1'),
#  command=lambda: label.config(text=i18n.t('labelPl1'))
# )
# menu_playlist.add_command(
#  label=i18n.t('file1'),
#  command=lambda: label.config(text=i18n.t('labelPl2'))
# )

# menu_playlist.add_command(
#  label=i18n.t('playlist2'),
#  command=lambda: label.config(text=i18n.t('labelPl3'))
# )

# menu_bar.add_cascade(
#  label=i18n.t('menuBar3'),
#  menu=menu_playlist
# )
# #view
# menu_view = tk.Menu(menu_bar, tearoff=0)

# menu_view.add_radiobutton(
#  label=i18n.t('themeD'),
#  value="Dark",
#  variable=themeVar,
#  command=lambda: label.config(text="Dark", bg="black", fg="white")
# )

# menu_view.add_radiobutton(
#  label=i18n.t('themeL'),
#  value="Light",
#  variable=themeVar,
#  command=lambda: label.config(text=i18n.t('themeL'),  bg="white", fg="black")
# )

# menu_bar.add_cascade(
#  label=i18n.t('menuBar4'),
#  menu=menu_view
# )

# #help
# menu_help = tk.Menu(menu_bar, tearoff=0)
# menu_help.add_command(
#  label=i18n.t('menuBar5'),
#  command=lambda: label.config(text=i18n.t('menuBar5'))
# )

# menu_bar.add_cascade(
#  label=i18n.t('menuBar5'),
#  menu=menu_help
# )




# root.config(menu=menu_bar)
# root.mainloop()
