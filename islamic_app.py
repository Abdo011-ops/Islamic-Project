#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
عبد الرحمن للخدمات الإسلامية - Rebuilt in CustomTkinter
===================================================
Author: AI Coding Agent (AI Studio Build)
Compatibility: Python 3.8+
Dependencies:
    pip install customtkinter Pillow arabic-reshaper python-bidi

This script recreates the visual layout, deep teal palette,
and interactive functionalities of the Islamic services dashboard.
"""

import sys
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

# Optional Arabic Reshaping for native operating system rendering of RTL scripts
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL = True
except ImportError:
    HAS_RTL = False

def render_arabic(text):
    """
    Utility handler to solve Right-to-Left (RTL) and character shaping 
    limitations within standard Tkinter rendering systems.
    """
    if not HAS_RTL:
        return text  # Return raw text if reshaping library is not installed
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception:
        return text

class IslamicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("عبد الرحمن للخدمات الإسلامية")
        self.geometry("450x850")
        self.resizable(False, False)
        
        # Determine and apply the aesthetic color scheme (Teal Forest theme)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")  # Basic theme baseline

        self.bg_color = "#061E1B"
        self.card_color = "#113C36"
        self.accent_color = "#e5b842"
        self.fg_color = "#FFFFFF"
        self.sub_text_color = "#B2C6C3"
        
        # Apply dark background matching the user interface
        self.configure(fg_color=self.bg_color)

        # Counter State for Tasbih (السبحة)
        self.tasbih_count = 0
        self.current_dhikr_idx = 0
        self.dhikr_phrases = [
            "سبحان الله",
            "الحمد لله",
            "الله أكبر",
            "لا إله إلا الله",
            "أستغفر الله"
        ]

        # --- Base Layout Setup ---
        # Main responsive canvas grid
        self.grid_rowconfigure(0, weight=0) # Top bar
        self.grid_rowconfigure(1, weight=0) # Welcome Greetings
        self.grid_rowconfigure(2, weight=0) # Prayer card (Hero)
        self.grid_rowconfigure(3, weight=1) # Interactive Features Grid
        self.grid_rowconfigure(4, weight=0) # Search bar footer
        self.grid_columnconfigure(0, weight=1)

        # Create Layout Elements
        self.create_top_bar()
        self.create_greetings()
        self.create_prayer_card()
        self.create_features_grid()
        self.create_bottom_search_bar()
        
        # Start Clock threads / timers
        self.update_countdown_clock()

    # ==========================================
    # 1. TOP UTILITY BAR MODULE
    # ==========================================
    def create_top_bar(self):
        top_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        top_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(15, 0))
        top_frame.grid_columnconfigure(0, weight=1)

        # Left Menu Hambuger Icon Fallback (|| structure or ☰)
        menu_btn = ctk.CTkButton(
            top_frame, 
            text="☰", 
            width=30, 
            height=30,
            fg_color="transparent",
            text_color=self.accent_color,
            font=("Cairo", 18, "bold"),
            hover_color=self.card_color,
            command=self.show_side_menu
        )
        menu_btn.grid(row=0, column=0, sticky="w")

        # Right Audio / Notification Indicator Icon Fallback
        notif_btn = ctk.CTkButton(
            top_frame,
            text="🔔",
            width=30,
            height=30,
            fg_color="transparent",
            text_color=self.accent_color,
            font=("Cairo", 15),
            hover_color=self.card_color,
            command=self.toggle_notifications
        )
        notif_btn.grid(row=0, column=1, sticky="e")

    # ==========================================
    # 2. APP HEADING & GREETINGS
    # ==========================================
    def create_greetings(self):
        greet_frame = ctk.CTkFrame(self, fg_color="transparent")
        greet_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 15))
        greet_frame.grid_columnconfigure(0, weight=1)

        # "السلام عليكم" - Greeting Header
        lbl_salam = ctk.CTkLabel(
            greet_frame,
            text=render_arabic("السلام عليكم"),
            font=("Cairo", 22, "bold"),
            text_color=self.fg_color,
            anchor="center"
        )
        lbl_salam.grid(row=0, column=0, pady=(0, 2))

        # "مرحباً بك في تطبيق" - Subtext
        lbl_welcome = ctk.CTkLabel(
            greet_frame,
            text=render_arabic("مرحباً بك في تطبيق"),
            font=("Cairo", 14),
            text_color=self.sub_text_color,
            anchor="center"
        )
        lbl_welcome.grid(row=1, column=0, pady=(0, 2))

        # Application Title: "عبد الرحمن للخدمات الإسلامية"
        lbl_app_name = ctk.CTkLabel(
            greet_frame,
            text=render_arabic("عبد الرحمن للخدمات الإسلامية"),
            font=("Cairo", 15, "bold"),
            text_color=self.accent_color,
            anchor="center"
        )
        lbl_app_name.grid(row=2, column=0)

    # ==========================================
    # 3. PRAYER TIME HERO CARD WITH IMAGES/INFO
    # ==========================================
    def create_prayer_card(self):
        # Card outer container
        self.card_frame = ctk.CTkFrame(
            self,
            fg_color=self.card_color,
            border_width=1,
            border_color="rgba(229, 184, 66, 0.15)",
            corner_radius=18
        )
        self.card_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.card_frame.grid_columnconfigure(0, weight=1)
        self.card_frame.grid_columnconfigure(1, weight=1)

        # --- Content Panel Left (Text & Info) ---
        info_sub_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        info_sub_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Location Icon and City Lbl
        city_text = "📍  " + "الرياض"
        lbl_city = ctk.CTkLabel(
            info_sub_frame,
            text=render_arabic(city_text),
            font=("Cairo", 14, "bold"),
            text_color=self.accent_color,
            anchor="w"
        )
        lbl_city.pack(anchor="w", pady=(0, 4))

        # Hijri Date Label
        lbl_date = ctk.CTkLabel(
            info_sub_frame,
            text=render_arabic("الأثنين 20 ذو القعدة 1445 هـ"),
            font=("Cairo", 11),
            text_color=self.sub_text_color,
            anchor="w"
        )
        lbl_date.pack(anchor="w", pady=(0, 15))

        # Prayer Name
        lbl_prayer_name = ctk.CTkLabel(
            info_sub_frame,
            text=render_arabic("الفجر"),
            font=("Cairo", 24, "bold"),
            text_color=self.fg_color,
            anchor="w"
        )
        lbl_prayer_name.pack(anchor="w", pady=(0, 2))

        # Prayer Time (Clock Face style)
        lbl_prayer_time = ctk.CTkLabel(
            info_sub_frame,
            text="04:15",
            font=("JetBrains Mono", 32, "bold"),
            text_color=self.accent_color,
            anchor="w"
        )
        lbl_prayer_time.pack(anchor="w")

        # --- Right Panel (Visual Mosque Placeholder) ---
        mosque_sub_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        mosque_sub_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        
        # Creating a beautiful vector style silhouette / default background inside Tkinter
        # Note: If you want to load a real image, use PIL and copy a beautiful mosque.png alongside this.
        try:
            # We attempt to render an placeholder or loaded image
            # image = Image.open("mosque_preview.png")
            # ctk_img = ctk.CTkImage(light_image=image, dark_image=image, size=(160, 120))
            # lbl_img = ctk.CTkLabel(mosque_sub_frame, image=ctk_img, text="")
            # lbl_img.pack(fill="both", expand=True)
            pass
        except Exception:
            # Fallback illustration using a beautiful customtkinter box with mosque silhouette fallback icon
            lbl_fallback = ctk.CTkLabel(
                mosque_sub_frame,
                text="🕌",
                font=("Cairo", 80),
                text_color=self.accent_color
            )
            lbl_fallback.pack(fill="both", expand=True, pady=10)

        # --- Bottom Bar / Countdown Footer (Frosted Glass style strip) ---
        countdown_strip = ctk.CTkFrame(
            self.card_frame,
            fg_color="rgba(0, 0, 0, 0.2)" if isDark else "rgba(15, 45, 40, 0.1)",
            corner_radius=0,
            height=38
        )
        countdown_strip.grid(row=1, column=0, columnspan=2, sticky="ew")
        countdown_strip.grid_columnconfigure(0, weight=1)
        countdown_strip.grid_columnconfigure(1, weight=1)

        # Left: Target Description
        self.lbl_target_desc = ctk.CTkLabel(
            countdown_strip,
            text=render_arabic("الوقت المتبقي لـ الفجر"),
            font=("Cairo", 12),
            text_color=self.sub_text_color
        )
        self.lbl_target_desc.grid(row=0, column=0, sticky="w", padx=15, pady=6)

        # Right: Dynamic Remaining Countdown Timer
        self.lbl_timer_val = ctk.CTkLabel(
            countdown_strip,
            text="06:34:21  ⏱",
            font=("JetBrains Mono", 13, "bold"),
            text_color=self.accent_color
        )
        self.lbl_timer_val.grid(row=0, column=1, sticky="e", padx=15, pady=6)

    # ==========================================
    # 4. INTERACTIVE FEATURES BENTO GRID (6 ITEMS)
    # ==========================================
    def create_features_grid(self):
        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=15)
        
        # 3 Columns structure to match pixel layout perfectly
        grid_container.grid_columnconfigure(0, weight=1)
        grid_container.grid_columnconfigure(1, weight=1)
        grid_container.grid_columnconfigure(2, weight=1)
        
        grid_container.grid_rowconfigure(0, weight=1)
        grid_container.grid_rowconfigure(1, weight=1)

        # Defining Card Models (Title, Icon/Symbol, Click Event Callback)
        # Note: RTL rendering is applied directly to the labels.
        features = [
            # Row 1
            {
                "title_ar": "المصحف", "icon": "📖", "col": 0, "row": 0,
                "command": self.open_quran_viewer, "border_color": "rgba(229, 184, 66, 0.15)"
            },
            {
                "title_ar": "أذكار", "icon": "🛡️", "col": 1, "row": 0,
                "command": self.open_adhkar_window, "border_color": self.accent_color
            },
            {
                "title_ar": "مواقيت الصلاة", "icon": "🕌", "col": 2, "row": 0,
                "command": self.open_prayer_times, "border_color": "rgba(229, 184, 66, 0.15)"
            },
            # Row 2
            {
                "title_ar": "المكتبة الصوتية", "icon": "🎧", "col": 0, "row": 1,
                "command": self.open_audio_library, "border_color": "rgba(229, 184, 66, 0.15)"
            },
            {
                "title_ar": "السبحة", "icon": "📿", "col": 1, "row": 1,
                "command": self.open_tasbih_meter, "border_color": "rgba(229, 184, 66, 0.15)"
            },
            {
                "title_ar": "المزيد", "icon": "💬", "col": 2, "row": 1,
                "command": self.open_more_options, "border_color": "rgba(229, 184, 66, 0.15)"
            },
        ]

        for item in features:
            # Feature Glassy Button Subframe
            card = ctk.CTkFrame(
                grid_container,
                fg_color=self.card_color,
                border_width=1,
                border_color=item["border_color"],
                corner_radius=16,
                cursor="hand2"
            )
            card.grid(row=item["row"], column=item["col"], padx=5, pady=5, sticky="nsew")
            
            # Pack simple layouts inside cards
            card.grid_rowconfigure(0, weight=1)
            card.grid_rowconfigure(1, weight=0)
            card.grid_columnconfigure(0, weight=1)

            # High contrast circular visual background for icon
            icon_lbl = ctk.CTkLabel(
                card,
                text=item["icon"],
                font=("Segoe UI Emoji", 32) if sys.platform == "win32" else ("Cairo", 36),
                text_color=self.accent_color
            )
            icon_lbl.grid(row=0, column=0, pady=(15, 5))

            # Feature arabic text label
            text_lbl = ctk.CTkLabel(
                card,
                text=render_arabic(item["title_ar"]),
                font=("Cairo", 12, "bold"),
                text_color=self.fg_color
            )
            text_lbl.grid(row=1, column=0, pady=(0, 15))

            # Bind mouse clicks on both fram, icon, and labels securely to fire actions
            for widget in [card, icon_lbl, text_lbl]:
                widget.bind("<Button-1>", lambda event, cmd=item["command"]: cmd())

    # ==========================================
    # 5. SEARCH & VOICE INPUT INTEGRATED BASES
    # ==========================================
    def create_bottom_search_bar(self):
        bar_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        bar_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 25))
        bar_frame.grid_columnconfigure(0, weight=1)

        # Rounded Glass Search container
        search_sub = ctk.CTkFrame(
            bar_frame,
            fg_color=self.card_color,
            border_width=1,
            border_color="rgba(229, 184, 66, 0.15)",
            corner_radius=30,
            height=50
        )
        search_sub.grid(row=0, column=0, sticky="ew")
        search_sub.grid_columnconfigure(0, weight=0) # Left green Mic
        search_sub.grid_columnconfigure(1, weight=1) # Entry field
        search_sub.grid_columnconfigure(2, weight=0) # Right Search Icon

        # Left: Interactive voice microphone container custom button (round emerald structure)
        mic_btn = ctk.CTkButton(
            search_sub,
            text="🎙",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="#18524D" if isDark else "#D0E5E2",
            text_color=self.accent_color,
            hover_color=self.bg_color,
            font=("Segoe UI Emoji", 14, "bold"),
            command=self.activate_voice_search
        )
        mic_btn.grid(row=0, column=0, padx=(8, 4), pady=5)

        # Middle: Text placeholder field
        placeholder_text = render_arabic("...ابحث بصوتك عن أي آية أو موضوع")
        self.search_entry = ctk.CTkEntry(
            search_sub,
            placeholder_text=placeholder_text,
            fg_color="transparent",
            border_width=0,
            font=("Cairo", 12),
            text_color=self.fg_color,
            placeholder_text_color=self.sub_text_color,
            justify="right"
        )
        self.search_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.trigger_search())

        # Right: Glass magnifier icon
        search_icon = ctk.CTkLabel(
            search_sub,
            text="🔍",
            font=("Segoe UI Emoji", 13),
            text_color=self.accent_color
        )
        search_icon.grid(row=0, column=2, padx=(2, 15))

    # ==========================================
    # INTERACTIVE ACTION LISTENERS
    # ==========================================
    def update_countdown_clock(self):
        """
        Dynamically ticks the remaining countdown down to Fajr or target prayers.
        Recomputes simulated ticking delta per second.
        """
        now = datetime.datetime.now()
        # Mocking ticking counter
        remaining_seconds = (23 * 3600 + 45 * 60) - (now.hour * 3600 + now.min * 60 + now.second)
        if remaining_seconds < 0:
            remaining_seconds += 24 * 3600
        
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60
        seconds = remaining_seconds % 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.lbl_timer_val.configure(text=f"{time_str}  ⏱")
        
        # Periodic looping every 1000mS
        self.after(1000, self.update_countdown_clock)

    def trigger_search(self):
        query = self.search_entry.get()
        if not query:
            return
        messagebox.showinfo(
            render_arabic("بحث"),
            render_arabic(f"جاري البحث عن: '{query}' في سور المصحف...")
        )

    def activate_voice_search(self):
        messagebox.showinfo(
            render_arabic("البحث الصوتي"),
            render_arabic("جاري تفعيل الميكروفون لالتقاط تلاوتك أو موضوع البحث...")
        )

    def show_side_menu(self):
        messagebox.showinfo(
            render_arabic("القائمة الكاملة"),
            render_arabic("تم فتح القائمة الجانبية للتطبيق - عبد الرحمن للخدمات الإسلامية.")
        )

    def toggle_notifications(self):
        messagebox.showinfo(
            render_arabic("التنبيهات"),
            render_arabic("تم تفعيل تنبيهات الأذان والذكر لمدينة الرياض بنجاح.")
        )

    # --- Grid Buttons Handlers ---
    def open_quran_viewer(self):
        win = ctk.CTkToplevel(self)
        win.title(render_arabic("المصحف الشريف"))
        win.geometry("400x500")
        win.configure(fg_color=self.bg_color)
        
        lbl = ctk.CTkLabel(
            win, 
            text=render_arabic("📖 المصحف الشريف"), 
            font=("Cairo", 18, "bold"),
            text_color=self.accent_color
        )
        lbl.pack(pady=15)

        tb = ctk.CTkTextbox(win, width=340, height=360, fg_color=self.card_color)
        tb.pack(pady=10)
        
        tb.insert("1.0", render_arabic("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n\n") +
                       render_arabic("الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ (2) الرَّحْمَٰنِ الرَّحِيمِ (3) مَالِكِ يَوْمِ الدِّينِ (4) إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ (5) اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ (6) صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ (7)"))
        tb.configure(state="disabled")

    def open_adhkar_window(self):
        win = ctk.CTkToplevel(self)
        win.title(render_arabic("أذكار المسلم"))
        win.geometry("400x500")
        win.configure(fg_color=self.bg_color)

        lbl = ctk.CTkLabel(
            win,
            text=render_arabic("🛡️ أذكار الصباح والمساء"),
            font=("Cairo", 18, "bold"),
            text_color=self.accent_color
        )
        lbl.pack(pady=15)

        # Frame for quick counter interactions
        dhikr_box = ctk.CTkFrame(win, fg_color=self.card_color, corner_radius=12)
        dhikr_box.pack(padx=20, pady=10, fill="both", expand=True)

        txt_dhikr = ctk.CTkLabel(
            dhikr_box,
            text=render_arabic("يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ،\nوَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ."),
            font=("Cairo", 13),
            text_color=self.fg_color,
            wraplength=300
        )
        txt_dhikr.pack(pady=30)

        self.adhkar_count = 3
        count_lbl = ctk.CTkLabel(
            dhikr_box,
            text=f"العدد المتبقي: {self.adhkar_count}",
            font=("Cairo", 14, "bold"),
            text_color=self.accent_color
        )
        count_lbl.pack(pady=10)

        def count_down():
            if self.adhkar_count > 0:
                self.adhkar_count -= 1
                count_lbl.configure(text=f"العدد المتبقي: {self.adhkar_count}")
                if self.adhkar_count == 0:
                    messagebox.showinfo("تم الذكر", "جزاك الله خيراً! لقد أكملت هذا الذكر.")
                    win.destroy()

        tap_btn = ctk.CTkButton(
            dhikr_box,
            text=render_arabic("اضغط للتكرار"),
            fg_color=self.accent_color,
            text_color="#000000",
            hover_color="#DEC04E",
            font=("Cairo", 12, "bold"),
            command=count_down
        )
        tap_btn.pack(pady=20)

    def open_prayer_times(self):
        win = ctk.CTkToplevel(self)
        win.title(render_arabic("مواقيت الصلاة"))
        win.geometry("380x480")
        win.configure(fg_color=self.bg_color)

        lbl = ctk.CTkLabel(
            win,
            text=render_arabic("🕌 جدول مواقيت الصلاة"),
            font=("Cairo", 18, "bold"),
            text_color=self.accent_color
        )
        lbl.pack(pady=15)

        times_frame = ctk.CTkFrame(win, fg_color=self.card_color, corner_radius=12)
        times_frame.pack(padx=20, pady=10, fill="both", expand=True)

        prayers = [
            ("الفجر", "04:15"),
            ("الشروق", "05:32"),
            ("الظهر", "12:02"),
            ("العصر", "15:28"),
            ("المغرب", "18:42"),
            ("العشاء", "20:05")
        ]

        for idx, (p_name, p_time) in enumerate(prayers):
            row_f = ctk.CTkFrame(times_frame, fg_color="transparent")
            row_f.pack(fill="x", padx=15, pady=8)
            
            # Left time
            lbl_time = ctk.CTkLabel(row_f, text=p_time, font=("JetBrains Mono", 14, "bold"), text_color=self.accent_color)
            lbl_time.pack(side="left")
            
            # Right English name & Arabic name
            lbl_name = ctk.CTkLabel(row_f, text=render_arabic(p_name), font=("Cairo", 13, "bold"), text_color=self.fg_color)
            lbl_name.pack(side="right")

    def open_audio_library(self):
        messagebox.showinfo(
            render_arabic("المكتبة الصوتية"),
            render_arabic("المكتبة الصوتية: جاري تحميل التلاوات والأدعية بصوت مشاهير القراء...")
        )

    def open_tasbih_meter(self):
        # Secondary Custom Tasbih Counter window popup!
        win = ctk.CTkToplevel(self)
        win.title(render_arabic("السبحة الإلكترونية"))
        win.geometry("380x450")
        win.configure(fg_color=self.bg_color)

        lbl_head = ctk.CTkLabel(
            win,
            text=render_arabic("السبحة الإلكترونية"),
            font=("Cairo", 18, "bold"),
            text_color=self.accent_color
        )
        lbl_head.pack(pady=15)

        tasbih_box = ctk.CTkFrame(win, fg_color=self.card_color, corner_radius=16)
        tasbih_box.pack(padx=20, pady=10, fill="both", expand=True)

        # Dynamic Dhikr Phrase Label
        self.lbl_dhikr_text = ctk.CTkLabel(
            tasbih_box,
            text=render_arabic(self.dhikr_phrases[self.current_dhikr_idx]),
            font=("Cairo", 18, "bold"),
            text_color=self.fg_color
        )
        self.lbl_dhikr_text.pack(pady=20)

        # Big Digital Counter
        self.lbl_big_counter = ctk.CTkLabel(
            tasbih_box,
            text=f"{self.tasbih_count:03d}",
            font=("JetBrains Mono", 54, "bold"),
            text_color=self.accent_color
        )
        self.lbl_big_counter.pack(pady=15)

        # Actions for counter increments
        def tap_tasbih():
            self.tasbih_count += 1
            self.lbl_big_counter.configure(text=f"{self.tasbih_count:03d}")
            
        def reset_tasbih():
            self.tasbih_count = 0
            self.lbl_big_counter.configure(text="000")

        def cycle_dhikr():
            self.current_dhikr_idx = (self.current_dhikr_idx + 1) % len(self.dhikr_phrases)
            self.lbl_dhikr_text.configure(text=render_arabic(self.dhikr_phrases[self.current_dhikr_idx]))

        # Click Tap big Button
        tap_btn = ctk.CTkButton(
            tasbih_box,
            text=render_arabic("تسبيح (اضغط للتسبيح)"),
            height=50,
            fg_color="#18524D",
            text_color=self.fg_color,
            hover_color="#1F6660",
            font=("Cairo", 14, "bold"),
            command=tap_tasbih
        )
        tap_btn.pack(pady=10, fill="x", padx=40)

        # Utility actions Row
        act_row = ctk.CTkFrame(tasbih_box, fg_color="transparent")
        act_row.pack(fill="x", padx=40, pady=10)

        btn_cycle = ctk.CTkButton(
            act_row,
            text=render_arabic("تغيير الذكر"),
            width=100,
            fg_color="transparent",
            text_color=self.accent_color,
            hover_color="#113C36",
            font=("Cairo", 11, "bold"),
            command=cycle_dhikr
        )
        btn_cycle.pack(side="left")

        btn_reset = ctk.CTkButton(
            act_row,
            text=render_arabic("تصفير"),
            width=100,
            fg_color="transparent",
            text_color="red",
            hover_color="#113C36",
            font=("Cairo", 11, "bold"),
            command=reset_tasbih
        )
        btn_reset.pack(side="right")

    def open_more_options(self):
        messagebox.showinfo(
            render_arabic("عبد الرحمن للخدمات الإسلامية"),
            "إصدار التطبيق: 1.0.0\n" +
            "تطوير وإعادة بناء باستخدام CustomTkinter بنجاح.\n\n" +
            "تقبل الله منا ومنكم صالح الأعمال."
        )


if __name__ == "__main__":
    # Workaround for high DPI screen displays (Retina/4K windows spacing)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = IslamicApp()
    app.mainloop()
