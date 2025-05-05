import tkinter as tk
import ctypes
import locale
import time
import threading
import i18n
import os
import json
import logging

# Налаштування логування
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('i18n_app')

# Шлях до директорії з файлами перекладу - використовуємо відносний шлях
LANG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang')
logger.info(f"Шлях до директорії з перекладами: {LANG_DIR}")

# Переконаємося, що директорія існує
if not os.path.exists(LANG_DIR):
    logger.warning(f"Директорія з перекладами не існує: {LANG_DIR}")
    os.makedirs(LANG_DIR, exist_ok=True)
    logger.info(f"Створено директорію для перекладів: {LANG_DIR}")

# Створюємо файли перекладів, якщо вони не існують
def create_translation_files():
    en_translation = {
        "title": "Media Player",
        "labelT": "Welcome to Media Player",
        "menuBar1": "File",
        "menuBar2": "Controls",
        "menuBar3": "Playlist",
        "menuBar4": "View",
        "menuBar5": "Help",
        "file1": "Open",
        "Control1": "Play",
        "Control2": "Pause",
        "Control3": "Stop",
        "Control4": "Next Track",
        "playlist1": "Add to Playlist",
        "playlist2": "Clear Playlist",
        "labelPl1": "Current playlist",
        "labelPl2": "Opened file",
        "labelPl3": "Playlist cleared",
        "themeD": "Dark Theme",
        "themeL": "Light Theme"
    }
    
    uk_translation = {
        "title": "Медіа Плеєр",
        "labelT": "Ласкаво просимо до Медіа Плеєра",
        "menuBar1": "Файл",
        "menuBar2": "Керування",
        "menuBar3": "Плейлист",
        "menuBar4": "Вигляд",
        "menuBar5": "Допомога",
        "file1": "Відкрити",
        "Control1": "Відтворити",
        "Control2": "Пауза",
        "Control3": "Стоп",
        "Control4": "Наступний трек",
        "playlist1": "Додати до плейлисту",
        "playlist2": "Очистити плейлист",
        "labelPl1": "Поточний плейлист",
        "labelPl2": "Відкритий файл",
        "labelPl3": "Плейлист очищено",
        "themeD": "Темна тема",
        "themeL": "Світла тема"
    }
    
    # Записуємо файли перекладів
    en_file = os.path.join(LANG_DIR, 'en.json')
    uk_file = os.path.join(LANG_DIR, 'uk.json')
    
    try:
        with open(en_file, 'w', encoding='utf-8') as f:
            json.dump(en_translation, f, ensure_ascii=False, indent=2)
        logger.info(f"Створено файл перекладу: {en_file}")
    except Exception as e:
        logger.error(f"Помилка при створенні файлу {en_file}: {str(e)}")
    
    try:
        with open(uk_file, 'w', encoding='utf-8') as f:
            json.dump(uk_translation, f, ensure_ascii=False, indent=2)
        logger.info(f"Створено файл перекладу: {uk_file}")
    except Exception as e:
        logger.error(f"Помилка при створенні файлу {uk_file}: {str(e)}")

# Створюємо файли перекладів
# create_translation_files()

# Налаштування i18n - ТІЛЬКИ ПІСЛЯ створення файлів!
i18n.load_path.append(LANG_DIR)
logger.info(f"Додано шлях до i18n: {LANG_DIR}")
logger.info(f"Всі шляхи в i18n: {i18n.load_path}")

i18n.set('filename_format', '{locale}.json')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')  # Встановлюємо початкову локаль
i18n.set('enable_memoization', True)  # Для кешування перекладів

# Перевірка, чи завантажилися переклади
logger.info(f"Поточна локаль: {i18n.get('locale')}")
logger.info(f"Запасна локаль: {i18n.get('fallback')}")

LANG_MAP = {
    'uk_UA': 'uk',
    'en_GB': 'en',
    'en_US': 'en'  # Додаємо для більшої сумісності
}

# Функція для перевірки наявності файлів перекладу
def check_translation_files():
    logger.info("Перевірка файлів перекладу...")
    for locale_code, lang in LANG_MAP.items():
        file_path = os.path.join(LANG_DIR, f"{lang}.json")
        if os.path.exists(file_path):
            logger.info(f"Знайдено файл перекладу: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Файл перекладу '{lang}' містить {len(data)} ключів: {list(data.keys())}")
            except json.JSONDecodeError:
                logger.error(f"Помилка декодування JSON в файлі: {file_path}")
            except Exception as e:
                logger.error(f"Помилка при читанні файлу {file_path}: {str(e)}")
        else:
            logger.error(f"Файл перекладу не знайдено: {file_path}")

# Функція для тестування перекладу
def test_translation(key, locale):
    try:
        current_locale = i18n.get('locale')
        logger.info(f"Поточна локаль перед тестом: {current_locale}")
        
        i18n.set('locale', locale)
        logger.info(f"Локаль змінена для тесту на: {locale}")
        
        # Вручну перевіряємо наявність перекладу
        file_path = os.path.join(LANG_DIR, f"{locale}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if key in data:
                    logger.info(f"Ключ '{key}' знайдено у файлі {locale}.json: {data[key]}")
                else:
                    logger.warning(f"Ключ '{key}' НЕ знайдено у файлі {locale}.json!")
        
        # Пробуємо отримати переклад через API
        try:
            translated = i18n.t(key, default=f"[{key}]")
            logger.info(f"Переклад ключа '{key}' з локалізацією '{locale}': '{translated}'")
            return translated
        except Exception as e:
            logger.error(f"Помилка при отриманні перекладу для ключа '{key}': {str(e)}")
            return f"[{key}]"
    except Exception as e:
        logger.error(f"Помилка в функції test_translation: {str(e)}")
        return f"[{key}]"

def set_language_by_locale(locale_code):
    lang = LANG_MAP.get(locale_code, 'en')
    previous_locale = i18n.get('locale')
    
    logger.info(f"Встановлення мови '{lang}' (з '{locale_code}')")
    i18n.set('locale', lang)
    
    logger.info(f"Змінено мову з '{previous_locale}' на '{lang}'")
    
    # Перезавантажуємо переклади для нової мови
    try:
        file_path = os.path.join(LANG_DIR, f"{lang}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                logger.info(f"Завантажено {len(translations)} перекладів для мови '{lang}'")
                
                # Додатково встановлюємо переклади напряму через публічний API
                for key, value in translations.items():
                    i18n.add_translation(key, value, locale=lang)
                    logger.debug(f"Додано переклад: {key} -> {value} ({lang})")
        else:
            logger.error(f"Файл перекладу не знайдено: {file_path}")
    except Exception as e:
        logger.error(f"Помилка при перезавантаженні перекладів: {str(e)}")

# Функція для прямого отримання перекладу без використання i18n
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
        logger.error(f"Помилка при отриманні перекладу напряму: {str(e)}")
        return f"[{key}]"

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
    check_translation_files()
    
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