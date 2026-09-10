import json
import os
import random
import threading
import time
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

import wave
import math
import struct

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

def create_beep_wav(filename, freq=1000, duration_ms=40, volume=0.1):
    if os.path.exists(filename):
        return
    sample_rate = 44100
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    try:
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            for i in range(n_samples):
                t = float(i) / sample_rate
                value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * t))
                # Fade in and fade out to avoid clicks
                if i < 400: value = int(value * (i / 400))
                if i > n_samples - 400: value = int(value * ((n_samples - i) / 400))
                data = struct.pack('<h', value)
                wav_file.writeframesraw(data)
    except Exception:
        pass

SOUND_ENABLED = False
start_sound = None
stop_sound = None
try:
    pygame.mixer.init()
    # Frequencies and volumes are kept low for a soft, pleasant sound
    create_beep_wav("start_beep.wav", freq=600, duration_ms=100, volume=0.03)
    create_beep_wav("stop_beep.wav", freq=300, duration_ms=100, volume=0.03)
    start_sound = pygame.mixer.Sound("start_beep.wav")
    stop_sound = pygame.mixer.Sound("stop_beep.wav")
    SOUND_ENABLED = True
except Exception:
    pass

from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# CustomTkinter Theme Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Constants
KEY_ALIASES = {
    "space": "space", "enter": "enter", "tab": "tab", "esc": "esc", "escape": "esc",
    "backspace": "backspace", "shift": "shift", "ctrl": "ctrl", "control": "ctrl",
    "alt": "alt", "win": "cmd", "windows": "cmd", "cmd": "cmd", "up": "up",
    "down": "down", "left": "left", "right": "right", "insert": "insert",
    "delete": "delete", "home": "home", "end": "end", "pageup": "page_up",
    "pagedown": "page_down",
}

SPECIAL_KEYS = {name: getattr(Key, value) for name, value in KEY_ALIASES.items() if hasattr(Key, value)}
MOUSE_BUTTONS_MAP = {"left": Button.left, "middle": Button.middle, "right": Button.right}

# Keyboard Layouts
KEYBOARD_LAYOUTS = {
    "English QWERTY": [
        ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
        ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "backspace"],
        ["tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
        ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "enter"],
        ["shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "shift_r"],
        ["ctrl", "win", "alt", "space", "alt_r", "fn", "ctrl_r"]
    ],
    "Türkçe Q": [
        ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
        ['"', "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "-", "backspace"],
        ["tab", "q", "w", "e", "r", "t", "y", "u", "ı", "o", "p", "ğ", "ü", ","],
        ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ş", "i", "enter"],
        ["shift", "<", "z", "x", "c", "v", "b", "n", "m", "ö", "ç", ".", "shift_r"],
        ["ctrl", "win", "alt", "space", "alt_r", "fn", "ctrl_r"]
    ],
    "Français AZERTY": [
        ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
        ["²", "&", "é", '"', "'", "(", "-", "è", "_", "ç", "à", ")", "=", "backspace"],
        ["tab", "a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "^", "$", "*"],
        ["caps", "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "ù", "enter"],
        ["shift", "<", "w", "x", "c", "v", "b", "n", ",", ";", ":", "!", "shift_r"],
        ["ctrl", "win", "alt", "space", "alt_r", "fn", "ctrl_r"]
    ],
    "Deutsch QWERTZ": [
        ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
        ["^", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "ß", "´", "backspace"],
        ["tab", "q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü", "+", "#"],
        ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä", "enter"],
        ["shift", "<", "y", "x", "c", "v", "b", "n", "m", ",", ".", "-", "shift_r"],
        ["ctrl", "win", "alt", "space", "alt_r", "fn", "ctrl_r"]
    ],
    "Español QWERTY": [
        ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
        ["º", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "'", "¡", "backspace"],
        ["tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "`", "+", "ç"],
        ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ñ", "´", "enter"],
        ["shift", "<", "z", "x", "c", "v", "b", "n", "m", ",", ".", "-", "shift_r"],
        ["ctrl", "win", "alt", "space", "alt_r", "fn", "ctrl_r"]
    ],
    "Italiano QWERTY": [
        ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
        ["\\", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "'", "ì", "backspace"],
        ["tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "è", "+", "ù"],
        ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ò", "à", "enter"],
        ["shift", "<", "z", "x", "c", "v", "b", "n", "m", ",", ".", "-", "shift_r"],
        ["ctrl", "win", "alt", "space", "alt_r", "fn", "ctrl_r"]
    ]
}

# Translations
LANGUAGES = {
    "English": {
        "title": "KEYPULSE 3.0 // CYBER DASHBOARD",
        "subtitle": "MACRO CONSOLE v3.0",
        "status_ready": "SYSTEM: READY",
        "status_active": "SYSTEM: ACTIVE",
        "status_wait": "Waiting for trigger [{}]...",
        "status_run": "Macro is running...",
        "status_stop": "Macro stopped.",
        "ev_idle": "Listener is idle",
        "ev_active": "Listener is active",
        "ev_assign_wait": "Assignment: Listening...",
        "ev_assign_succ": "Assignment successful: {}",
        "prof_saved": "Profile saved successfully.",
        "prof_loaded": "Profile loaded.",
        "err_title": "Error",
        "err_num": "Please enter duration in correct numerical format.",
        "live_telemetry": "> LIVE TELEMETRY",
        "leg_trigger": " Trigger Key",
        "leg_action": " Action Key",
        "btn_settings": "SETTINGS / PROFILES",
        "btn_start": "START",
        "btn_stop": "STOP",
        "sec_trigger": "TRIGGER",
        "sec_trigger_desc": "Initiation key",
        "lbl_trigger_key": "Trigger Keyboard Key:",
        "btn_assign": "Assign Key",
        "sec_action": "ACTION",
        "sec_action_desc": "Action to execute",
        "act_opt_key": "Press Key",
        "act_opt_mouse": "Mouse Click",
        "mouse_left": "Left Click",
        "mouse_middle": "Middle Click",
        "mouse_right": "Right Click",
        "sec_protocol": "PROTOCOL",
        "sec_protocol_desc": "Timing configuration",
        "rep_opt_inf": "Infinite",
        "rep_opt_time": "Timed",
        "lbl_duration": "Duration (h:m:s):",
        "lbl_interval": "Interval (s):",
        "vis_title": "> KEYBOARD [{}] / MOUSE",
        "vis_subtitle": "LIVE MONITOR",
        "set_title": "> SYSTEM SETTINGS",
        "set_lang": "App Language",
        "set_kbd": "Keyboard Layout",
        "set_game": "Game Mode (±20% Delay Variance)",
        "set_sound": "Sound Alerts (On/Off)",
        "set_prof": "Profile Management",
        "btn_load": "Load Profile",
        "btn_save": "Save Profile",
        "mouse_L": "L",
        "mouse_M": "M",
        "mouse_R": "R",
        "assign_listen": "Listening..."
    },
    "Türkçe": {
        "title": "KEYPULSE 3.0 // CYBER DASHBOARD",
        "subtitle": "MAKRO KONSOL v3.0",
        "status_ready": "SISTEM: HAZIR",
        "status_active": "SISTEM: AKTIF",
        "status_wait": "Tetikleyici bekleniyor [{}]...",
        "status_run": "Makro calisiyor...",
        "status_stop": "Makro durduruldu.",
        "ev_idle": "Dinleyici pasif",
        "ev_active": "Dinleyici aktif",
        "ev_assign_wait": "Atama: Dinleniyor...",
        "ev_assign_succ": "Atama basarili: {}",
        "prof_saved": "Profil basariyla kaydedildi.",
        "prof_loaded": "Profil yuklendi.",
        "err_title": "Hata",
        "err_num": "Lutfen sureleri dogru (sayisal) formatta girin.",
        "live_telemetry": "> CANLI TELEMETRI",
        "leg_trigger": " Tetikleyici Tuş",
        "leg_action": " Aksiyon Tuşu",
        "btn_settings": "AYARLAR / PROFILLER",
        "btn_start": "BAŞLAT]",
        "btn_stop": "DURDUR",
        "sec_trigger": "TETİKLEYİCİ",
        "sec_trigger_desc": "Başlatma tuşu",
        "lbl_trigger_key": "Tetik Klavye Tuşu:",
        "btn_assign": "Tuş Ata",
        "sec_action": "AKSİYON",
        "sec_action_desc": "Yürütülecek işlem",
        "act_opt_key": "Tusa bas",
        "act_opt_mouse": "Fare tiklat",
        "mouse_left": "Sol tiklama",
        "mouse_middle": "Orta tiklama",
        "mouse_right": "Sag tiklama",
        "sec_protocol": "PROTOKOL",
        "sec_protocol_desc": "Zamanlama ayarı",
        "rep_opt_inf": "Suresiz",
        "rep_opt_time": "Sureli",
        "lbl_duration": "Sure (sa:dk:sn):",
        "lbl_interval": "Aralik (sn):",
        "vis_title": "> KLAVYE [{}] / FARE",
        "vis_subtitle": "CANLI IZLEME",
        "set_title": "> SISTEM AYARLARI",
        "set_lang": "Uygulama Dili (App Language)",
        "set_kbd": "Klavye Dili",
        "set_game": "Oyun Modu (±%20 Gecikme Sapması)",
        "set_sound": "Sesli Bildirimler (Açık/Kapalı)",
        "set_prof": "Profil Yönetimi",
        "btn_load": "Profili Yükle",
        "btn_save": "Profili Kaydet",
        "mouse_L": "SOL",
        "mouse_M": "M",
        "mouse_R": "SAG",
        "assign_listen": "Dinleniyor..."
    }
}

# Colors for Cyber Aesthetic
CYBER_BG = "#080d14"
CYBER_PANEL = "#0b141f"
CYBER_ACCENT = "#00e5ff"
CYBER_GREEN = "#00ff9d"
CYBER_RED = "#ff2a2a"
CYBER_TEXT = "#d9f7ff"
CYBER_DIM_TEXT = "#6f8997"

class MacroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Internal State
        self.internal_act_type = "key" # "key" or "mouse"
        self.internal_act_mouse_val = "left" # "left", "middle", "right"
        self.internal_rep_mode = "inf" # "inf" or "time"
        
        self.trigger_value = ctk.StringVar(value="f8")
        self.action_key_value = ctk.StringVar(value="space")
        self.duration_hours = ctk.StringVar(value="0")
        self.duration_minutes = ctk.StringVar(value="1")
        self.duration_seconds = ctk.StringVar(value="0")
        self.interval = ctk.StringVar(value="0.10")
        
        self.game_mode = ctk.BooleanVar(value=False)
        self.sound_alerts = ctk.BooleanVar(value=True)
        self.app_language = ctk.StringVar(value="English")
        self.keyboard_layout = ctk.StringVar(value="English QWERTY")
        
        self.t = LANGUAGES[self.app_language.get()]
        
        self.title(self.t["title"])
        self.geometry("1100x750")
        self.minsize(1050, 700)
        self.configure(fg_color=CYBER_BG)

        # Controllers & Threading
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()
        self.keyboard_listener = None
        self.stop_event = threading.Event()
        self.worker = None
        
        self.is_running = False
        self.action_running = False
        self.trigger_is_down = False
        self.capture_trigger = False
        self.capture_target = None
        self._shift_pressed = False
        
        # Widget References for i18n
        self.i18n = {}
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=320)

        self._build_sidebar()
        self._build_dashboard()
        
        self._update_all_texts()
        
        self.trigger_value.trace_add("write", self._update_visualizer)
        self.action_key_value.trace_add("write", self._update_visualizer)
        self.keyboard_layout.trace_add("write", self._on_layout_change)
        self.app_language.trace_add("write", self._on_language_change)
        
        self._update_visualizer()
        
        self.protocol("WM_DELETE_WINDOW", self.close)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color=CYBER_PANEL)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        try:
            logo_img = ctk.CTkImage(light_image=Image.open("logo.png"), dark_image=Image.open("logo.png"), size=(60, 60))
            logo_label = ctk.CTkLabel(self.sidebar, image=logo_img, text="")
            logo_label.grid(row=0, column=0, padx=20, pady=(25, 0), sticky="w")
            
            title_label = ctk.CTkLabel(self.sidebar, text="KEYPULSE", font=("Consolas", 24, "bold"), text_color=CYBER_ACCENT)
            title_label.grid(row=0, column=0, padx=(90, 20), pady=(25, 0), sticky="w")
        except Exception:
            ctk.CTkLabel(self.sidebar, text="KEYPULSE", font=("Consolas", 32, "bold"), text_color=CYBER_ACCENT).grid(row=0, column=0, padx=20, pady=(30, 0), sticky="w")

        self.i18n['subtitle'] = ctk.CTkLabel(self.sidebar, text="", font=("Consolas", 10, "bold"), text_color=CYBER_DIM_TEXT)
        self.i18n['subtitle'].grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        status_frame = ctk.CTkFrame(self.sidebar, fg_color=CYBER_BG, corner_radius=8, border_width=1, border_color="#1f5268")
        status_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        
        self.status_dot = ctk.CTkLabel(status_frame, text="●", font=("Segoe UI", 24), text_color=CYBER_GREEN)
        self.status_dot.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.i18n['status_var'] = ctk.CTkLabel(status_frame, text="", font=("Consolas", 14, "bold"), text_color=CYBER_TEXT)
        self.i18n['status_var'].pack(anchor="w", padx=15)
        self.i18n['status_detail'] = ctk.CTkLabel(status_frame, text="", font=("Consolas", 11), text_color=CYBER_DIM_TEXT, wraplength=250, justify="left")
        self.i18n['status_detail'].pack(anchor="w", padx=15, pady=(0, 10))

        event_frame = ctk.CTkFrame(self.sidebar, fg_color=CYBER_BG, corner_radius=8)
        event_frame.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self.i18n['live_telemetry'] = ctk.CTkLabel(event_frame, text="", font=("Consolas", 11, "bold"), text_color=CYBER_ACCENT)
        self.i18n['live_telemetry'].pack(anchor="w", padx=10, pady=(10, 0))
        self.i18n['event_var'] = ctk.CTkLabel(event_frame, text="", font=("Consolas", 10), text_color=CYBER_TEXT, wraplength=250, justify="left")
        self.i18n['event_var'].pack(anchor="w", padx=10, pady=(5, 10))

        legend_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        legend_frame.grid(row=4, column=0, padx=15, pady=10, sticky="ew")
        
        l1 = ctk.CTkFrame(legend_frame, fg_color="transparent")
        l1.pack(fill="x", pady=2)
        ctk.CTkLabel(l1, text="■", text_color=CYBER_GREEN, font=("Segoe UI", 16)).pack(side="left")
        self.i18n['leg_trigger'] = ctk.CTkLabel(l1, text="", text_color=CYBER_DIM_TEXT, font=("Consolas", 10))
        self.i18n['leg_trigger'].pack(side="left")
        
        l2 = ctk.CTkFrame(legend_frame, fg_color="transparent")
        l2.pack(fill="x", pady=2)
        ctk.CTkLabel(l2, text="■", text_color=CYBER_ACCENT, font=("Segoe UI", 16)).pack(side="left")
        self.i18n['leg_action'] = ctk.CTkLabel(l2, text="", text_color=CYBER_DIM_TEXT, font=("Consolas", 10))
        self.i18n['leg_action'].pack(side="left")

        self.i18n['btn_settings'] = ctk.CTkButton(self.sidebar, text="", font=("Consolas", 12, "bold"), 
                                          fg_color="#1f5268", text_color=CYBER_TEXT, hover_color=CYBER_ACCENT, 
                                          height=40, command=self.open_settings)
        self.i18n['btn_settings'].grid(row=6, column=0, padx=15, pady=(10, 5), sticky="ew")

        self.start_button = ctk.CTkButton(self.sidebar, text="", font=("Consolas", 18, "bold"), 
                                          fg_color=CYBER_ACCENT, text_color="#000000", hover_color="#00b3cc", 
                                          height=60, command=self.toggle_running)
        self.start_button.grid(row=7, column=0, padx=15, pady=(5, 20), sticky="ew")
        self.i18n['btn_start'] = self.start_button

    def _build_dashboard(self):
        self.dash = ctk.CTkFrame(self, fg_color="transparent")
        self.dash.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        dash = self.dash
        
        dash.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        dash.grid_rowconfigure(0, weight=0)
        dash.grid_rowconfigure(1, weight=1)
        
        # 01 TETIKLEYICI (Row 0, Col 0)
        t_frame = ctk.CTkFrame(dash, fg_color=CYBER_PANEL, corner_radius=10, border_width=1, border_color="#1f5268")
        t_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(t_frame, text="01", font=("Consolas", 48, "bold"), text_color="#131f2d").place(relx=0.95, rely=0.1, anchor="ne")
        self.i18n['sec_trigger'] = ctk.CTkLabel(t_frame, text="", font=("Consolas", 14, "bold"), text_color=CYBER_TEXT)
        self.i18n['sec_trigger'].pack(anchor="w", padx=15, pady=(15, 0))
        self.i18n['sec_trigger_desc'] = ctk.CTkLabel(t_frame, text="", font=("Consolas", 10), text_color=CYBER_DIM_TEXT)
        self.i18n['sec_trigger_desc'].pack(anchor="w", padx=15, pady=(0, 15))
        
        t_inner = ctk.CTkFrame(t_frame, fg_color="transparent")
        t_inner.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.i18n['lbl_trigger_key'] = ctk.CTkLabel(t_inner, text="", font=("Consolas", 12), text_color=CYBER_DIM_TEXT)
        self.i18n['lbl_trigger_key'].pack(anchor="w", pady=(0, 5))
        
        self.trigger_entry = ctk.CTkEntry(t_inner, textvariable=self.trigger_value, state="readonly", fg_color=CYBER_BG, text_color=CYBER_TEXT, height=35)
        self.trigger_entry.pack(fill="x", pady=5)
        
        self.i18n['btn_assign_1'] = ctk.CTkButton(t_inner, text="", fg_color="#1f5268", hover_color=CYBER_ACCENT, height=35, command=self._arm_trigger_capture)
        self.i18n['btn_assign_1'].pack(fill="x", pady=5)

        # 02 ACTION (Row 0, Col 1)
        a_frame = ctk.CTkFrame(dash, fg_color=CYBER_PANEL, corner_radius=10, border_width=1, border_color="#1f5268")
        a_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(a_frame, text="02", font=("Consolas", 48, "bold"), text_color="#131f2d").place(relx=0.95, rely=0.1, anchor="ne")
        self.i18n['sec_action'] = ctk.CTkLabel(a_frame, text="", font=("Consolas", 14, "bold"), text_color=CYBER_TEXT)
        self.i18n['sec_action'].pack(anchor="w", padx=15, pady=(15, 0))
        self.i18n['sec_action_desc'] = ctk.CTkLabel(a_frame, text="", font=("Consolas", 10), text_color=CYBER_DIM_TEXT)
        self.i18n['sec_action_desc'].pack(anchor="w", padx=15, pady=(0, 15))
        
        a_inner = ctk.CTkFrame(a_frame, fg_color="transparent")
        a_inner.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.action_type_menu = ctk.CTkOptionMenu(a_inner, values=["dummy"], command=self._on_action_type_change,
                                                  fg_color=CYBER_BG, button_color="#1f5268", button_hover_color=CYBER_ACCENT, height=35)
        self.action_type_menu.pack(fill="x", pady=5)
        
        self.simple_act_dynamic_frame = ctk.CTkFrame(a_inner, fg_color="transparent")
        self.simple_act_dynamic_frame.pack(fill="x", pady=5)
        
        self.action_mouse_menu = ctk.CTkOptionMenu(self.simple_act_dynamic_frame, values=["dummy"], command=self._on_mouse_val_change,
                                                   fg_color=CYBER_BG, button_color="#1f5268", height=35)
        self.simple_act_entry = ctk.CTkEntry(self.simple_act_dynamic_frame, textvariable=self.action_key_value, state="readonly", fg_color=CYBER_BG, text_color=CYBER_TEXT, height=35)
        
        self.i18n['btn_assign_2'] = ctk.CTkButton(a_inner, text="", fg_color="#1f5268", hover_color=CYBER_ACCENT, height=35, command=self._arm_action_capture)
        self.i18n['btn_assign_2'].pack(fill="x", pady=5)

        # 03 LOOP (Row 0, Col 2)
        l_frame = ctk.CTkFrame(dash, fg_color=CYBER_PANEL, corner_radius=10, border_width=1, border_color="#1f5268")
        l_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(l_frame, text="03", font=("Consolas", 48, "bold"), text_color="#131f2d").place(relx=0.95, rely=0.1, anchor="ne")
        self.i18n['sec_protocol'] = ctk.CTkLabel(l_frame, text="", font=("Consolas", 14, "bold"), text_color=CYBER_TEXT)
        self.i18n['sec_protocol'].pack(anchor="w", padx=15, pady=(15, 0))
        self.i18n['sec_protocol_desc'] = ctk.CTkLabel(l_frame, text="", font=("Consolas", 10), text_color=CYBER_DIM_TEXT)
        self.i18n['sec_protocol_desc'].pack(anchor="w", padx=15, pady=(0, 15))
        
        l_inner = ctk.CTkFrame(l_frame, fg_color="transparent")
        l_inner.pack(fill="x", padx=15, pady=(0, 15))
        
        self.repeat_mode_menu = ctk.CTkOptionMenu(l_inner, values=["dummy"], command=self._on_repeat_mode_change,
                                                  fg_color=CYBER_BG, button_color="#1f5268", height=35)
        self.repeat_mode_menu.pack(fill="x", pady=5)
        
        self.time_frame = ctk.CTkFrame(l_inner, fg_color="transparent")
        self.time_frame.pack(fill="x", pady=5)
        self.i18n['lbl_duration'] = ctk.CTkLabel(self.time_frame, text="", font=("Consolas", 11), text_color=CYBER_DIM_TEXT)
        self.i18n['lbl_duration'].pack(side="left", padx=(0, 5))
        ctk.CTkEntry(self.time_frame, textvariable=self.duration_hours, width=35, height=30, fg_color=CYBER_BG, text_color=CYBER_TEXT).pack(side="left")
        ctk.CTkLabel(self.time_frame, text=":", text_color=CYBER_ACCENT).pack(side="left")
        ctk.CTkEntry(self.time_frame, textvariable=self.duration_minutes, width=35, height=30, fg_color=CYBER_BG, text_color=CYBER_TEXT).pack(side="left")
        ctk.CTkLabel(self.time_frame, text=":", text_color=CYBER_ACCENT).pack(side="left")
        ctk.CTkEntry(self.time_frame, textvariable=self.duration_seconds, width=35, height=30, fg_color=CYBER_BG, text_color=CYBER_TEXT).pack(side="left")

        self.int_frame = ctk.CTkFrame(l_inner, fg_color="transparent")
        self.int_frame.pack(fill="x", pady=5)
        self.i18n['lbl_interval'] = ctk.CTkLabel(self.int_frame, text="", font=("Consolas", 12), text_color=CYBER_DIM_TEXT)
        self.i18n['lbl_interval'].pack(side="left", padx=(0, 10))
        ctk.CTkEntry(self.int_frame, textvariable=self.interval, width=80, height=30, fg_color=CYBER_BG, text_color=CYBER_TEXT).pack(side="left")

        # 04 VISUALIZER
        self._build_visualizer(dash)

    def _build_visualizer(self, parent):
        self.vis_frame = ctk.CTkFrame(parent, fg_color=CYBER_PANEL, corner_radius=10, border_width=1, border_color="#1f5268")
        self.vis_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        
        top_bar = ctk.CTkFrame(self.vis_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=15, pady=(15, 5))
        self.i18n['vis_title'] = ctk.CTkLabel(top_bar, text="", font=("Consolas", 14, "bold"), text_color=CYBER_ACCENT)
        self.i18n['vis_title'].pack(side="left")
        self.i18n['vis_subtitle'] = ctk.CTkLabel(top_bar, text="", font=("Consolas", 10), text_color=CYBER_DIM_TEXT)
        self.i18n['vis_subtitle'].pack(side="left", padx=15)
        
        self.vis_content = ctk.CTkFrame(self.vis_frame, fg_color=CYBER_BG, corner_radius=8)
        self.vis_content.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.kb_vis = ctk.CTkFrame(self.vis_content, fg_color="transparent")
        self.mouse_vis = ctk.CTkFrame(self.vis_content, fg_color="transparent")
        
        self.key_labels = {}
        self._draw_keyboard()
                
        # Build Mouse
        self.mouse_labels = {}
        m_container = ctk.CTkFrame(self.mouse_vis, fg_color="transparent")
        m_container.pack(expand=True)
        m_top = ctk.CTkFrame(m_container, fg_color="transparent")
        m_top.pack(pady=5)
        
        self.mouse_labels["left"] = ctk.CTkLabel(m_top, text="L", width=70, height=100, fg_color="#131f2d", text_color=CYBER_TEXT, corner_radius=25, font=("Consolas", 12, "bold"))
        self.mouse_labels["left"].pack(side="left", padx=5)
        
        self.mouse_labels["middle"] = ctk.CTkLabel(m_top, text="M", width=35, height=55, fg_color="#131f2d", text_color=CYBER_TEXT, corner_radius=15, font=("Consolas", 10, "bold"))
        self.mouse_labels["middle"].pack(side="left", padx=5)
        
        self.mouse_labels["right"] = ctk.CTkLabel(m_top, text="R", width=70, height=100, fg_color="#131f2d", text_color=CYBER_TEXT, corner_radius=25, font=("Consolas", 12, "bold"))
        self.mouse_labels["right"].pack(side="left", padx=5)
        
        ctk.CTkLabel(m_container, text="KEYPULSE", width=185, height=140, fg_color="#131f2d", text_color=CYBER_DIM_TEXT, corner_radius=45, font=("Consolas", 16, "bold")).pack(pady=5)

    def open_settings(self):
        w = ctk.CTkToplevel(self)
        w.title("Settings")
        w.geometry("380x420")
        w.configure(fg_color=CYBER_PANEL)
        w.grab_set()
        w.focus()
        
        ctk.CTkLabel(w, text=self.t["set_title"], font=("Consolas", 16, "bold"), text_color=CYBER_ACCENT).pack(anchor="w", padx=20, pady=(20, 10))
        
        f1 = ctk.CTkFrame(w, fg_color=CYBER_BG, corner_radius=8)
        f1.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(f1, text=self.t["set_lang"], font=("Consolas", 12), text_color=CYBER_TEXT).pack(anchor="w", padx=15, pady=(10, 2))
        ctk.CTkOptionMenu(f1, variable=self.app_language, values=list(LANGUAGES.keys()), fg_color=CYBER_PANEL, button_color="#1f5268").pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(f1, text=self.t["set_kbd"], font=("Consolas", 12), text_color=CYBER_TEXT).pack(anchor="w", padx=15, pady=(5, 2))
        ctk.CTkOptionMenu(f1, variable=self.keyboard_layout, values=list(KEYBOARD_LAYOUTS.keys()), fg_color=CYBER_PANEL, button_color="#1f5268").pack(fill="x", padx=15, pady=(0, 15))
                          
        f2 = ctk.CTkFrame(w, fg_color=CYBER_BG, corner_radius=8)
        f2.pack(fill="x", padx=20, pady=5)
        ctk.CTkSwitch(f2, text=self.t["set_game"], variable=self.game_mode, progress_color=CYBER_GREEN, button_color="#ffffff", button_hover_color="#e0e0e0", font=("Consolas", 10)).pack(anchor="w", padx=15, pady=15)
        ctk.CTkSwitch(f2, text=self.t["set_sound"], variable=self.sound_alerts, progress_color=CYBER_GREEN, button_color="#ffffff", button_hover_color="#e0e0e0", font=("Consolas", 10)).pack(anchor="w", padx=15, pady=(0, 15))
                      
        f3 = ctk.CTkFrame(w, fg_color=CYBER_BG, corner_radius=8)
        f3.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(f3, text=self.t["set_prof"], font=("Consolas", 12), text_color=CYBER_TEXT).pack(anchor="w", padx=15, pady=(10, 5))
        btn_f = ctk.CTkFrame(f3, fg_color="transparent")
        btn_f.pack(fill="x", padx=15, pady=(0, 15))
        ctk.CTkButton(btn_f, text=self.t["btn_load"], width=130, fg_color="#1f5268", hover_color=CYBER_ACCENT, command=self.load_profile).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_f, text=self.t["btn_save"], width=130, fg_color="#1f5268", hover_color=CYBER_ACCENT, command=self.save_profile).pack(side="left")

    # --- UI Updaters ---

    def _update_all_texts(self):
        lang = self.app_language.get()
        if lang not in LANGUAGES:
            lang = "English"
        self.t = LANGUAGES[lang]
        self.title(self.t["title"])
        
        for key, widget in self.i18n.items():
            if key in ("status_var", "status_detail", "event_var", "btn_assign_1", "btn_assign_2"):
                continue
            if key == "vis_title":
                widget.configure(text=self.t[key].format(self.keyboard_layout.get().split()[0].upper()))
            elif key == "btn_start":
                widget.configure(text=self.t[key].format(self.trigger_value.get().upper()))
            else:
                widget.configure(text=self.t[key])
                
        # Status text fallback mapping
        if self.is_running:
            self.i18n["status_var"].configure(text=self.t["status_active"])
            self.i18n["status_detail"].configure(text=self.t["status_wait"].format(self.trigger_value.get().upper()))
            self.i18n["event_var"].configure(text=self.t["ev_active"])
        else:
            self.i18n["status_var"].configure(text=self.t["status_ready"])
            self.i18n["status_detail"].configure(text=self.t["status_stop"])
            self.i18n["event_var"].configure(text=self.t["ev_idle"])
            
        if not self.capture_trigger:
            self.i18n["btn_assign_1"].configure(text=self.t["btn_assign"])
            self.i18n["btn_assign_2"].configure(text=self.t["btn_assign"])
            
        # Update OptionMenus
        self.action_type_menu.configure(values=[self.t["act_opt_key"], self.t["act_opt_mouse"]])
        self.action_mouse_menu.configure(values=[self.t["mouse_left"], self.t["mouse_middle"], self.t["mouse_right"]])
        self.repeat_mode_menu.configure(values=[self.t["rep_opt_inf"], self.t["rep_opt_time"]])
        
        # Set current option menu values based on internal state
        if self.internal_act_type == "key":
            self.action_type_menu.set(self.t["act_opt_key"])
            self.simple_act_entry.pack(fill="x", expand=True)
            self.action_mouse_menu.pack_forget()
            self.i18n["btn_assign_2"].configure(state="normal", fg_color="#1f5268")
        else:
            self.action_type_menu.set(self.t["act_opt_mouse"])
            self.action_mouse_menu.pack(fill="x", expand=True)
            self.simple_act_entry.pack_forget()
            self.i18n["btn_assign_2"].configure(state="disabled", fg_color="#1a2530")
            
        mouse_map = {"left": "mouse_left", "middle": "mouse_middle", "right": "mouse_right"}
        self.action_mouse_menu.set(self.t[mouse_map[self.internal_act_mouse_val]])
        
        if self.internal_rep_mode == "inf":
            self.repeat_mode_menu.set(self.t["rep_opt_inf"])
            self.time_frame.pack_forget()
        else:
            self.repeat_mode_menu.set(self.t["rep_opt_time"])
            self.time_frame.pack(fill="x", pady=5, before=self.int_frame)
            
        self.mouse_labels["left"].configure(text=self.t["mouse_L"])
        self.mouse_labels["middle"].configure(text=self.t["mouse_M"])
        self.mouse_labels["right"].configure(text=self.t["mouse_R"])

    def _on_action_type_change(self, val):
        if val == self.t["act_opt_mouse"]:
            self.internal_act_type = "mouse"
            self.internal_act_mouse_val = "left"
        else:
            self.internal_act_type = "key"
            self.action_key_value.set("space")
        self._update_all_texts()
        self._update_visualizer()
            
    def _on_mouse_val_change(self, val):
        for k, v in {"left": "mouse_left", "middle": "mouse_middle", "right": "mouse_right"}.items():
            if val == self.t[v]:
                self.internal_act_mouse_val = k
        self._update_visualizer()

    def _on_repeat_mode_change(self, val):
        if val == self.t["rep_opt_inf"]: self.internal_rep_mode = "inf"
        else: self.internal_rep_mode = "time"
        self._update_all_texts()

    def _on_language_change(self, *args):
        self._update_all_texts()

    def _on_layout_change(self, *args):
        self.i18n['vis_title'].configure(text=self.t["vis_title"].format(self.keyboard_layout.get().split()[0].upper()))
        self._draw_keyboard()
        self._update_visualizer()

    def _draw_keyboard(self):
        for child in self.kb_vis.winfo_children(): child.destroy()
        self.key_labels.clear()
        
        layout_name = self.keyboard_layout.get()
        kb_rows = KEYBOARD_LAYOUTS.get(layout_name, KEYBOARD_LAYOUTS["English QWERTY"])
        
        for r, row_keys in enumerate(kb_rows):
            row_f = ctk.CTkFrame(self.kb_vis, fg_color="transparent")
            row_f.pack(pady=4)
            for key in row_keys:
                w = 40
                if key in ("space",): w = 240
                elif key in ("enter", "shift", "shift_r", "caps", "backspace", "tab"): w = 70
                elif key in ("ctrl", "ctrl_r", "win", "alt", "alt_r", "fn"): w = 50
                
                disp = key.upper().replace("_R", "")
                lbl = ctk.CTkLabel(row_f, text=disp, width=w, height=35, fg_color="#131f2d", text_color=CYBER_TEXT, corner_radius=6, font=("Consolas", 10, "bold"))
                lbl.pack(side="left", padx=4)
                self.key_labels[key.replace("_r", "")] = lbl
                if key == "shift_r": self.key_labels["shift"] = lbl 

    def _update_visualizer(self, *args):
        if not hasattr(self, 'key_labels'): return
        
        for lbl in self.key_labels.values(): lbl.configure(fg_color="#131f2d", text_color=CYBER_TEXT)
        for lbl in self.mouse_labels.values(): lbl.configure(fg_color="#131f2d", text_color=CYBER_TEXT)
            
        t_val = str(self.trigger_value.get()).lower()
        a_val = str(self.action_key_value.get()).lower()

        if self.internal_act_type == "mouse":
            self.kb_vis.pack_forget()
            self.mouse_vis.pack(expand=True, pady=10)
            m_val = self.internal_act_mouse_val
            if m_val in self.mouse_labels:
                self.mouse_labels[m_val].configure(fg_color=CYBER_ACCENT, text_color="#000000")
        else:
            self.mouse_vis.pack_forget()
            self.kb_vis.pack(expand=True, pady=10)
            if t_val in self.key_labels:
                self.key_labels[t_val].configure(fg_color=CYBER_GREEN, text_color="#000000")
            if a_val in self.key_labels:
                if a_val != t_val:
                    self.key_labels[a_val].configure(fg_color=CYBER_ACCENT, text_color="#000000")
                else:
                    self.key_labels[a_val].configure(fg_color="#33ffaa", text_color="#000000")

    # --- Capture Logic ---
    
    def _arm_trigger_capture(self):
        self.capture_trigger = True
        self.capture_target = "trigger"
        self.i18n["btn_assign_1"].configure(text=self.t["assign_listen"], fg_color=CYBER_RED)
        self.bind("<KeyPress>", self._capture_key)
        self.i18n["event_var"].configure(text=self.t["ev_assign_wait"])
        self._show_overlay()

    def _arm_action_capture(self):
        self.capture_trigger = True
        self.capture_target = "simple_action"
        self.i18n["btn_assign_2"].configure(text=self.t["assign_listen"], fg_color=CYBER_RED)
        self.bind("<KeyPress>", self._capture_key)
        self.i18n["event_var"].configure(text=self.t["ev_assign_wait"])
        self._show_overlay()
        
    def _show_overlay(self):
        if hasattr(self, "overlay_frame") and self.overlay_frame.winfo_exists():
            return
        self.overlay_frame = ctk.CTkFrame(self.dash, fg_color="#080d14", corner_radius=10, border_color=CYBER_ACCENT, border_width=2)
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        txt = "Bir tuşa basın..." if self.app_language.get() == "Türkçe" else "Press any key..."
        lbl = ctk.CTkLabel(self.overlay_frame, text=txt, font=("Consolas", 32, "bold"), text_color=CYBER_ACCENT)
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def _hide_overlay(self):
        if hasattr(self, "overlay_frame") and self.overlay_frame.winfo_exists():
            self.overlay_frame.destroy()

    def _capture_key(self, event):
        if not self.capture_trigger: return
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"): return
        
        key = event.keysym.lower()
        if key == "return": key = "enter"
        elif key == "escape": key = "esc"
        elif key == "prior": key = "page_up"
        elif key == "next": key = "page_down"
        
        if event.char and event.char.isprintable() and len(event.char) == 1 and key not in ("space",):
            key = event.char.lower()
        
        if self.capture_target == "trigger":
            self.trigger_value.set(key)
            self.i18n["btn_assign_1"].configure(text=self.t["btn_assign"], fg_color="#1f5268")
            self.i18n["btn_start"].configure(text=self.t["btn_start"].format(key.upper()))
        elif self.capture_target == "simple_action":
            self.action_key_value.set(key)
            self.i18n["btn_assign_2"].configure(text=self.t["btn_assign"], fg_color="#1f5268")
            
        self.capture_trigger = False
        self.capture_target = None
        self.unbind("<KeyPress>")
        self.i18n["event_var"].configure(text=self.t["ev_assign_succ"].format(key))
        self._hide_overlay()

    # --- Profile Save/Load ---

    def save_profile(self):
        data = {
            "trigger_value": self.trigger_value.get(),
            "internal_act_type": self.internal_act_type,
            "action_key_value": self.action_key_value.get(),
            "internal_act_mouse_val": self.internal_act_mouse_val,
            "internal_rep_mode": self.internal_rep_mode,
            "duration_hours": self.duration_hours.get(),
            "duration_minutes": self.duration_minutes.get(),
            "duration_seconds": self.duration_seconds.get(),
            "interval": self.interval.get(),
            "game_mode": self.game_mode.get(),
            "sound_alerts": self.sound_alerts.get(),
            "keyboard_layout": self.keyboard_layout.get(),
            "app_language": self.app_language.get()
        }
        try:
            with open("profile.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.i18n["event_var"].configure(text=self.t["prof_saved"])
        except Exception as e:
            messagebox.showerror(self.t["err_title"], str(e))

    def load_profile(self):
        if not os.path.exists("profile.json"): return
        try:
            with open("profile.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.trigger_value.set(data.get("trigger_value", "F8"))
            self.internal_act_type = data.get("internal_act_type", "key")
            self.action_key_value.set(data.get("action_key_value", "space"))
            self.internal_act_mouse_val = data.get("internal_act_mouse_val", "left")
            self.internal_rep_mode = data.get("internal_rep_mode", "inf")
            self.duration_hours.set(data.get("duration_hours", "0"))
            self.duration_minutes.set(data.get("duration_minutes", "1"))
            self.duration_seconds.set(data.get("duration_seconds", "0"))
            self.interval.set(data.get("interval", "0.10"))
            self.game_mode.set(data.get("game_mode", False))
            self.sound_alerts.set(data.get("sound_alerts", True))
            self.keyboard_layout.set(data.get("keyboard_layout", "English QWERTY"))
            self.app_language.set(data.get("app_language", "English"))
            
            self._update_all_texts()
            self.i18n["event_var"].configure(text=self.t["prof_loaded"])
        except Exception as e:
            messagebox.showerror(self.t["err_title"], str(e))

    # --- Macro Logic ---
    
    def _play_sound(self, mode):
        if not self.sound_alerts.get() or not SOUND_ENABLED: return
        def play():
            if mode == "start" and start_sound:
                start_sound.play()
            elif mode == "stop" and stop_sound:
                stop_sound.play()
        threading.Thread(target=play, daemon=True).start()

    def toggle_running(self):
        if self.is_running: self.stop_macro()
        else: self.start_macro()

    def start_macro(self):
        # Format and validate interval
        try:
            interval = float(self.interval.get())
            if interval <= 0: interval = 0.01
        except ValueError:
            interval = 0.10
        self.interval.set(f"{interval:.2f}")

        # Format and validate duration
        if self.internal_rep_mode == "time":
            try: h = int(self.duration_hours.get())
            except ValueError: h = 0
            if h < 0: h = 0
            
            try: m = int(self.duration_minutes.get())
            except ValueError: m = 0
            if m < 0: m = 0
            elif m > 59: m = 59
            
            try: s = int(self.duration_seconds.get())
            except ValueError: s = 0
            if s < 0: s = 0
            elif s > 59: s = 59

            self.duration_hours.set(str(h))
            self.duration_minutes.set(str(m))
            self.duration_seconds.set(str(s))

            duration = (h * 3600) + (m * 60) + s
        else:
            duration = 0

        self.active_trigger_value = self.trigger_value.get().strip()
        self.active_act_type = self.internal_act_type
        self.active_act_key = self.action_key_value.get().strip()
        self.active_act_mouse = self.internal_act_mouse_val
        self.active_rep_mode = self.internal_rep_mode
        self.active_duration = duration
        self.active_interval = interval
        
        self.stop_event.clear()
        self.is_running = True
        self.action_running = False
        self.trigger_is_down = False
        
        self.start_button.configure(text=self.t["btn_stop"], fg_color=CYBER_RED, hover_color="#cc0000")
        self.i18n["status_var"].configure(text=self.t["status_active"])
        self.i18n["status_detail"].configure(text=self.t["status_wait"].format(self.active_trigger_value.upper()))
        self.status_dot.configure(text_color=CYBER_ACCENT)
        self.i18n["event_var"].configure(text=self.t["ev_active"])
        
        self._start_listeners()

    def stop_macro(self):
        self.stop_event.set()
        self.action_running = False
        self.is_running = False
        self._stop_listeners()
        
        self.start_button.configure(text=self.t["btn_start"].format(self.trigger_value.get().upper()), fg_color=CYBER_ACCENT, hover_color="#00b3cc")
        self.i18n["status_var"].configure(text=self.t["status_ready"])
        self.i18n["status_detail"].configure(text=self.t["status_stop"])
        self.status_dot.configure(text_color=CYBER_GREEN)
        self.i18n["event_var"].configure(text=self.t["ev_idle"])

    def _start_listeners(self):
        self.keyboard_listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release)
        self.keyboard_listener.start()

    def _stop_listeners(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None

    def _on_key_press(self, key):
        if not self.is_running: return
        if self.capture_trigger: return
        
        if key == Key.esc and self._shift_pressed:
            self.after(0, self.stop_macro)
            return
            
        if key in (Key.shift, Key.shift_l, Key.shift_r):
            self._shift_pressed = True

        if self._key_matches(key, self.active_trigger_value) and not self.trigger_is_down:
            self.trigger_is_down = True
            self._toggle_action()

    def _on_key_release(self, key):
        if self.capture_trigger: return
        if key in (Key.shift, Key.shift_l, Key.shift_r):
            self._shift_pressed = False
        if self.is_running:
            if self._key_matches(key, self.active_trigger_value):
                self.trigger_is_down = False

    def _key_matches(self, key, wanted):
        wanted = wanted.lower()
        if isinstance(key, KeyCode) and key.char: return key.char.lower() == wanted
        if hasattr(key, "name"): return key.name.lower().replace("_", "") == wanted.replace("_", "").lower()
        return str(key).lower().replace("key.", "") == wanted

    def _toggle_action(self):
        if self.action_running:
            self.stop_event.set()
            self.action_running = False
            self.after(0, lambda: self.i18n["status_detail"].configure(text=self.t["status_stop"]))
            self._play_sound("stop")
        else:
            self.stop_event.clear()
            self.action_running = True
            self.worker = threading.Thread(target=self._run_actions, daemon=True)
            self.worker.start()
            self.after(0, lambda: self.i18n["status_detail"].configure(text=self.t["status_run"]))
            self._play_sound("start")

    def _run_actions(self):
        deadline = None if self.active_rep_mode == "inf" else time.monotonic() + self.active_duration
        while not self.stop_event.is_set() and (deadline is None or time.monotonic() < deadline):
            
            self._perform_single_action()
            
            if self.stop_event.is_set(): break
                
            wait_time = self.active_interval
            if self.game_mode.get():
                wait_time = random.uniform(wait_time * 0.8, wait_time * 1.2)
                
            if deadline is not None:
                wait_time = min(wait_time, max(0, deadline - time.monotonic()))
            
            if wait_time > 0:
                self.stop_event.wait(wait_time)
                
        self.action_running = False
        if self.is_running:
            self.after(0, lambda: self.i18n["status_detail"].configure(text=self.t["status_wait"].format(self.active_trigger_value.upper())))

    def _perform_single_action(self):
        if self.active_act_type == "mouse":
            btn = MOUSE_BUTTONS_MAP.get(self.active_act_mouse, Button.left)
            try:
                self.mouse_controller.click(btn)
            except Exception:
                pass
        else:
            key_name = self.active_act_key.lower()
            key = SPECIAL_KEYS.get(key_name)
            if key is None:
                if len(key_name) == 1:
                    key = KeyCode.from_char(key_name)
                else:
                    key = key_name
            try:
                self.keyboard_controller.press(key)
                self.keyboard_controller.release(key)
            except Exception as e:
                print(f"Failed to press key {key_name}: {e}")

    def close(self):
        self.stop_macro()
        self.destroy()

if __name__ == "__main__":
    app = MacroApp()
    app.mainloop()
