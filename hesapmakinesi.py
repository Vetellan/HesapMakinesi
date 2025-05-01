import tkinter as tk
from tkinter import ttk
try:
    from tkcalendar import DateEntry
except ImportError:
    # tkcalendar yüklü değilse, kurulum gerekli olabilir
    raise

class HesapMakinesiApp:
    def __init__(self, root):
        self.root = root
        root.title("Hesap Makinesi")
        root.resizable(False, False)

        # Tema renkleri
        self.dark_bg = "#2b2b2b"
        self.dark_fg = "#ffffff"
        self.dark_button_bg = "#3c3f41"
        self.dark_button_fg = "#ffffff"
        self.light_bg = "#ffffff"
        self.light_fg = "#000000"
        self.light_button_bg = "#f0f0f0"
        self.light_button_fg = "#000000"
        self.dark_mode = True  # Başlangıç teması koyu

        # Arkaplan rengini ayarla (başlangıçta koyu tema)
        root.configure(bg=self.dark_bg)

        # Hesap makinesi ekranı (Label olarak)
        self.display_label = tk.Label(root, text="", anchor="e", bg=self.dark_button_bg, 
                                      fg=self.dark_button_fg, relief="sunken", font=("Arial", 12))
        # Ekranı üstte, tüm sütunlara yayılacak şekilde yerleştir
        self.display_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="we")

        # Geçmiş ve Tarih için çerçeveler (Frame)
        self.history_frame = tk.Frame(root, bg=self.dark_bg)
        self.date_frame = tk.Frame(root, bg=self.dark_bg)

        # Geçmiş paneli bileşenleri
        self.history_list = tk.Listbox(self.history_frame, height=8, width=40)
        self.history_list.pack(side="top", fill="both", expand=True, padx=5, pady=(5, 0))
        self.clear_hist_button = tk.Button(self.history_frame, text="🗑 Temizle", command=self.clear_history)
        self.clear_hist_button.pack(side="top", pady=5)

        # Tarih paneli bileşenleri
        self.start_date = DateEntry(self.date_frame, width=10)
        self.end_date = DateEntry(self.date_frame, width=10)
        self.diff_button = tk.Button(self.date_frame, text="Fark Hesapla", command=self.calculate_date_difference)
        self.date_result_label = tk.Label(self.date_frame, text="", bg=self.dark_bg, fg=self.dark_fg)
        # Tarih paneli yerleşimi
        self.start_date.grid(row=0, column=0, padx=5, pady=5)
        self.end_date.grid(row=0, column=1, padx=5, pady=5)
        self.diff_button.grid(row=0, column=2, padx=5, pady=5)
        self.date_result_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        # Başlangıçta geçiş paneli (history/date) seçimi
        self.current_panel = None
        

        # Üst kontrol düğmeleri: Geçmiş, Tarih, Tema
        self.history_btn = tk.Button(root, text="📄 Geçmiş", command=lambda: self.show_panel("history"))
        self.date_btn = tk.Button(root, text="📅 Tarih", command=lambda: self.show_panel("date"))
        self.theme_btn = tk.Button(root, text="⚙", command=self.toggle_theme)
        # Yerleşim: üst kontrol düğmeleri
        self.history_btn.grid(row=1, column=0, padx=5, pady=5)
        self.date_btn.grid(row=1, column=1, padx=5, pady=5)
        # Ayarlar/tema düğmesini en sağa yasla (column 3 sağ)
        self.theme_btn.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        # (Not: column 2 boş bırakılarak sağ tarafta boşluk bırakılmıştır)
        
        # Varsayılan olarak geçmiş panelini göster (tarih paneli gizli)
        self.show_panel("history")

        # Yüzde hesaplama paneli (Frame)
        self.percent_frame = tk.Frame(root, bg=self.dark_bg)
        self.percent_frame.grid(row=9, column=0, columnspan=4, sticky="we")
        # Yüzde paneli bileşenleri
        self.percent_title = tk.Label(self.percent_frame, text="Yüzde Hesaplama", bg=self.dark_bg, fg=self.dark_fg)
        self.base_entry = tk.Entry(self.percent_frame, width=10)
        self.perc1_entry = tk.Entry(self.percent_frame, width=5)
        self.perc2_entry = tk.Entry(self.percent_frame, width=5)
        self.perc3_entry = tk.Entry(self.percent_frame, width=5)
        self.calc_percent_button = tk.Button(self.percent_frame, text="Hesapla", command=self.calculate_percentages)
        # Yüzde paneli yerleşimi
        self.percent_title.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="w")
        self.base_entry.grid(row=1, column=0, padx=5, pady=5)
        self.perc1_entry.grid(row=1, column=1, padx=5, pady=5)
        self.perc2_entry.grid(row=1, column=2, padx=5, pady=5)
        self.perc3_entry.grid(row=1, column=3, padx=5, pady=5)
        self.calc_percent_button.grid(row=1, column=4, padx=5, pady=5)
        # Yüzde sonuç etiketi (çok satırlı sonuçlar buraya yazılır)
        self.percent_result_label = tk.Label(self.percent_frame, text="", bg=self.dark_bg, fg=self.dark_fg, justify="left")
        self.percent_result_label.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="w")

        # Hesap makinesi tuş takımı (sayılar ve işlemler)
        self.buttons = []
        btn_defs = [
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3),
            ('0', 7, 0), ('.', 7, 1), ('C', 7, 2), ('+', 7, 3),
            ('=', 8, 0, 4)  # '=' düğmesi 4 sütunu birden kapsıyor
        ]
        for (text, r, c, *cs) in btn_defs:
            colspan = cs[0] if cs else 1
            self.create_button(text, r, c, colspan)
        # Tuş takımı sütunlarını uniform yap (eşit genişlik)
        for col in range(4):
            root.grid_columnconfigure(col, weight=1, uniform="buttons")

        # İlk temayı uygula (koyu tema başlangıç)
        self.apply_theme()

    def create_button(self, text, row, col, colspan=1):
        # Her tuş için işlev ataması
        if text == 'C':
            cmd = self.clear_display    # C = Ekranı temizle (clear entry)
        elif text == '=':
            cmd = self.calculate_result  # = sonuç hesapla
        else:
            cmd = lambda t=text: self.button_click(t)  # diğer durum: rakam veya operatör ekle
        btn = tk.Button(self.root, text=text, command=cmd, bg=self.dark_button_bg, fg=self.dark_button_fg)
        btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")
        self.buttons.append(btn)

    def button_click(self, char):
        # Eğer son işlem '=' ise ve şimdi sayı giriliyorsa, yeni giriş için ekranı temizle
        if getattr(self, 'last_action', None) == 'equals':
            if char.isdigit() or char == '.':
                self.display_label.config(text="")  # yeni bir sayıyla başla
        # Ekrandaki mevcut ifadeyi al ve yeni karakteri ekle
        current_text = self.display_label.cget("text")
        new_text = current_text + char
        self.display_label.config(text=new_text)
        self.last_action = 'input'

    def clear_display(self):
        # Hesap makinesi ekranını temizle
        self.display_label.config(text="")
        self.last_action = 'clear'

    def calculate_result(self):
        expr = self.display_label.cget("text")
        try:
            result = eval(expr)  # İfadeyi değerlendir (aritmetik hesaplama)
            # Sonucu string olarak formatla
            if isinstance(result, float):
                # Tam sayıysa nokta sıfırlarını at
                if result.is_integer():
                    result_str = str(int(result))
                else:
                    result_str = str(round(result, 10))
                    # Gereksiz sıfırları at (örn. 5.2000 -> 5.2)
                    if '.' in result_str:
                        result_str = result_str.rstrip('0').rstrip('.')
            else:
                result_str = str(result)
        except Exception:
            result_str = "Hata"  # Hatalı ifade
        # Sonucu ekranda göster
        self.display_label.config(text=result_str)
        # Geçmişe ekle (eğer hata yoksa ve ifade boş değilse)
        if expr and result_str != "Hata":
            history_entry = f"{expr} = {result_str}"
            self.history_list.insert("end", history_entry)
        self.last_action = 'equals'

    def calculate_percentages(self):
        # Ana sayı ve yüzde değerlerini al
        try:
            base = float(self.base_entry.get())
        except ValueError:
            return  # Geçersiz sayı girdisi
        perc_values = []
        for entry in (self.perc1_entry, self.perc2_entry, self.perc3_entry):
            val = entry.get().strip()
            if not val:
                continue
            try:
                perc = float(val)
            except ValueError:
                continue
            perc_values.append(perc)
        if not perc_values:
            return  # Yüzde alanları boş veya geçersiz ise işlem yapma

        # Yüzde sonuçlarını hesapla
        lines = []
        for perc in perc_values:
            result = base * perc / 100.0
            # Sonucu formatla (tam sayı ise .0 at)
            if float(result).is_integer():
                result_str = str(int(result))
            else:
                result_str = str(round(result, 10))
                if '.' in result_str:
                    result_str = result_str.rstrip('0').rstrip('.')
            # Sonucu "x% = y" formatında satıra ekle
            lines.append(f"{perc}% = {result_str}")
        output_text = "\n".join(lines)
        self.percent_result_label.config(text=output_text)
        # (Not: Bu sonuçlar geçmişe eklenmez)

    def calculate_date_difference(self):
        # İki DateEntry alanından tarihleri al
        try:
            d1 = self.start_date.get_date()
            d2 = self.end_date.get_date()
        except Exception:
            import datetime
            try:
                # Eğer get_date çalışmazsa (örn. tkcalendar yoksa), string olarak parse etmeyi dene
                d1 = datetime.datetime.strptime(self.start_date.get(), "%m/%d/%y").date()
                d2 = datetime.datetime.strptime(self.end_date.get(), "%m/%d/%y").date()
            except Exception:
                self.date_result_label.config(text="Tarih Hatası")
                return
        # Gün farkını hesapla
        diff_days = abs((d2 - d1).days)
        result_text = f"{diff_days} gün fark var"
        self.date_result_label.config(text=result_text)
        # (Tarih hesaplaması sonucu geçmişe eklenmez)

    def clear_history(self):
        # Geçmiş listesini temizle
        self.history_list.delete(0, "end")

    def show_panel(self, panel):
        # Geçmiş ve Tarih panelleri arasında geçiş yap
        if panel == "history":
            if self.current_panel != "history":
                # Tarih panelini gizle, Geçmiş panelini göster
                self.date_frame.grid_remove()
                self.history_frame.grid(row=2, column=0, columnspan=4, sticky="nwe")
                self.current_panel = "history"
        elif panel == "date":
            if self.current_panel != "date":
                # Geçmiş panelini gizle, Tarih panelini göster
                self.history_frame.grid_remove()
                self.date_frame.grid(row=2, column=0, columnspan=4, sticky="nwe")
                self.current_panel = "date"
        # Seçili panel düğmesinin görünümünü (kabartma) güncelle
        if self.current_panel == "history":
            self.history_btn.config(relief="sunken")
            self.date_btn.config(relief="raised")
        else:
            self.history_btn.config(relief="raised")
            self.date_btn.config(relief="sunken")

    def toggle_theme(self):
        # Tema bayrağını değiştir
        self.dark_mode = not self.dark_mode
        # Yeni temayı uygula
        self.apply_theme()

    def apply_theme(self):
        # Geçerli temaya göre renkleri belirle
        if self.dark_mode:
            bg = self.dark_bg; fg = self.dark_fg
            btn_bg = self.dark_button_bg; btn_fg = self.dark_button_fg
        else:
            bg = self.light_bg; fg = self.light_fg
            btn_bg = self.light_button_bg; btn_fg = self.light_button_fg
        # Arkaplanlar
        self.root.configure(bg=bg)
        self.history_frame.configure(bg=bg)
        self.date_frame.configure(bg=bg)
        self.percent_frame.configure(bg=bg)
        # Ekran label'ı
        self.display_label.configure(bg=btn_bg, fg=btn_fg)
        # Geçmiş paneli
        self.clear_hist_button.configure(bg=btn_bg, fg=btn_fg)
        # (Geçmiş listesi listbox olarak default beyaz bırakıldı)
        # Tarih paneli
        self.diff_button.configure(bg=btn_bg, fg=btn_fg)
        self.date_result_label.configure(bg=bg, fg=fg)
        # Üst kontrol düğmeleri
        self.history_btn.configure(bg=btn_bg, fg=btn_fg)
        self.date_btn.configure(bg=btn_bg, fg=btn_fg)
        self.theme_btn.configure(bg=btn_bg, fg=btn_fg)
        # Yüzde paneli
        self.percent_title.configure(bg=bg, fg=fg)
        self.calc_percent_button.configure(bg=btn_bg, fg=btn_fg)
        self.percent_result_label.configure(bg=bg, fg=fg)
        # Sayısal tuş takımı düğmeleri
        for btn in self.buttons:
            btn.configure(bg=btn_bg, fg=btn_fg)

# Uygulamayı çalıştırmak için (doğrudan bu kodu çalıştırıyorsanız):
if __name__ == "__main__":
    root = tk.Tk()
    app = HesapMakinesiApp(root)
    root.mainloop()
