#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MU Auto Bai - Tu dong chay bai theo toa do cho MU Online (Fast Mu & cac server private).

Tinh nang:
  - Doc toa do nhan vat bang OCR (region tren man hinh) -> di ve bai da set.
  - Vong san quai: spam phim skill, nhat do, buff dinh ky.
  - Tu dong uong HP/MP dua theo mau pixel cua thanh mau/mana.
  - Tu dong quay lai bai khi bi lech ra ngoai ban kinh.
  - Hotkey toan cuc: F8 bat/tat, F9 panic (dung khan cap).
  - GUI Tkinter de chinh cau hinh & luu config.

Chay tren WINDOWS. MU la game DirectX nen dung pydirectinput de gui phim/chuot.

    python muauto.py

Xem README.md de biet cach cai dat va tinh chinh toa do vung OCR / thanh mau.
"""

import json
import os
import sys
import time
import random
import threading
import traceback

# ---- Import cac thu vien phu thuoc (chiu loi mem de GUI van mo duoc de config) ----
_IMPORT_ERRORS = {}

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except Exception as e:  # pragma: no cover
    print("Thieu Tkinter (thuong co san trong Python tren Windows):", e)
    raise

try:
    import pydirectinput
    pydirectinput.PAUSE = 0.0
    pydirectinput.FAILSAFE = False
except Exception as e:
    pydirectinput = None
    _IMPORT_ERRORS["pydirectinput"] = str(e)

try:
    import pyautogui
    pyautogui.FAILSAFE = False
except Exception as e:
    pyautogui = None
    _IMPORT_ERRORS["pyautogui"] = str(e)

try:
    import mss
except Exception as e:
    mss = None
    _IMPORT_ERRORS["mss"] = str(e)

try:
    import numpy as np
except Exception as e:
    np = None
    _IMPORT_ERRORS["numpy"] = str(e)

try:
    import keyboard as kb
except Exception as e:
    kb = None
    _IMPORT_ERRORS["keyboard"] = str(e)

try:
    import pytesseract
    from PIL import Image
except Exception as e:
    pytesseract = None
    _IMPORT_ERRORS["pytesseract"] = str(e)


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
EXAMPLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.example.json")


def default_config():
    with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config():
    path = CONFIG_PATH if os.path.exists(CONFIG_PATH) else EXAMPLE_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# =====================================================================================
#  INPUT: gui phim / chuot vao game
# =====================================================================================
def press_key(key, hold=False):
    """Nhan 1 phim vao game. Tra ve True neu gui duoc."""
    if not key:
        return False
    if pydirectinput is not None:
        try:
            if hold:
                pydirectinput.keyDown(key)
            else:
                pydirectinput.press(key)
            return True
        except Exception:
            pass
    if pyautogui is not None:
        try:
            pyautogui.press(key)
            return True
        except Exception:
            pass
    return False


def release_key(key):
    if not key:
        return
    if pydirectinput is not None:
        try:
            pydirectinput.keyUp(key)
        except Exception:
            pass


def click_at(x, y, button="left", jitter=True):
    """Click chuot tai vi tri man hinh (dung de di chuyen trong MU)."""
    if jitter:
        x += random.randint(-3, 3)
        y += random.randint(-3, 3)
    if pydirectinput is not None:
        try:
            pydirectinput.moveTo(int(x), int(y))
            pydirectinput.click(int(x), int(y), button=button)
            return True
        except Exception:
            pass
    if pyautogui is not None:
        try:
            pyautogui.click(int(x), int(y), button=button)
            return True
        except Exception:
            pass
    return False


# =====================================================================================
#  MAN HINH: chup vung, doc mau, OCR toa do
# =====================================================================================
def screen_size():
    if pyautogui is not None:
        try:
            return pyautogui.size()
        except Exception:
            pass
    return (1920, 1080)


def grab_region(region):
    """region = [left, top, width, height]. Tra ve numpy array RGB hoac None."""
    if mss is None or np is None:
        return None
    left, top, w, h = region
    with mss.mss() as sct:
        raw = sct.grab({"left": int(left), "top": int(top), "width": int(w), "height": int(h)})
        arr = np.asarray(raw)  # BGRA
    return arr[:, :, :3][:, :, ::-1].copy()  # -> RGB


def get_pixel(x, y):
    if mss is None or np is None:
        return (0, 0, 0)
    with mss.mss() as sct:
        raw = sct.grab({"left": int(x), "top": int(y), "width": 1, "height": 1})
        px = np.asarray(raw)[0, 0]
    return (int(px[2]), int(px[1]), int(px[0]))  # RGB


def bar_fill_ratio(x, y, full_color, empty_color):
    """Uoc luong % day cua thanh mau/mana dua vao mau pixel tai (x,y).

    So khoang cach mau toi 'full' va 'empty' -> ti le 0..1.
    """
    px = np.array(get_pixel(x, y), dtype=float)
    full = np.array(full_color, dtype=float)
    empty = np.array(empty_color, dtype=float)
    d_full = np.linalg.norm(px - full)
    d_empty = np.linalg.norm(px - empty)
    total = d_full + d_empty
    if total < 1e-6:
        return 1.0
    return float(d_empty / total)  # gan 'full' -> ratio cao


def ocr_coords(region, tesseract_cmd=None):
    """Doc toa do dang 'x,y' hoac 'x y' tu vung region. Tra ve (x, y) hoac None."""
    if pytesseract is None:
        return None
    if tesseract_cmd and os.path.exists(tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    img = grab_region(region)
    if img is None:
        return None
    try:
        pil = Image.fromarray(img).convert("L")
        # nhi phan hoa nhe de OCR de doc so trang tren nen toi
        pil = pil.point(lambda p: 255 if p > 130 else 0)
        pil = pil.resize((pil.width * 3, pil.height * 3))
        txt = pytesseract.image_to_string(
            pil, config="--psm 7 -c tessedit_char_whitelist=0123456789,: "
        )
    except Exception:
        return None
    digits = []
    cur = ""
    for ch in txt:
        if ch.isdigit():
            cur += ch
        else:
            if cur:
                digits.append(int(cur))
                cur = ""
    if cur:
        digits.append(int(cur))
    if len(digits) >= 2:
        return (digits[0], digits[1])
    return None


# =====================================================================================
#  BOT: vong lap chinh
# =====================================================================================
class AutoBot:
    def __init__(self, cfg, log_fn):
        self.cfg = cfg
        self.log = log_fn
        self.running = False
        self.thread = None
        self._stop = threading.Event()
        self.status = "Dung"
        self.cur_coord = None

    def start(self):
        if self.running:
            return
        self._stop.clear()
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.running = False
        # nha cac phim dang giu (neu attack_hold)
        for k in self.cfg["hunt"].get("attack_keys", []):
            release_key(k)
        self.status = "Dung"
        self.log("[BOT] Da dung.")

    def _jit(self, base):
        if self.cfg.get("safety", {}).get("human_jitter", True):
            return base * random.uniform(0.85, 1.15)
        return base

    def _run(self):
        try:
            delay = int(self.cfg.get("safety", {}).get("start_delay_sec", 3))
            self.log(f"[BOT] Bat dau sau {delay}s - hay dua chuot vao cua so game...")
            for _ in range(delay * 10):
                if self._stop.is_set():
                    return
                time.sleep(0.1)

            hunt = self.cfg["hunt"]
            pots = self.cfg["potions"]
            spot = self.cfg["spot"]
            ocr = self.cfg["coord_ocr"]

            t0 = time.time()
            last_attack = 0.0
            last_pickup = 0.0
            last_buff = 0.0
            last_pot = 0.0
            last_pot_check = 0.0
            last_coord_read = 0.0
            last_recenter = 0.0
            max_run = float(self.cfg.get("safety", {}).get("max_runtime_min", 0)) * 60.0

            self.status = "Dang chay"
            self.log("[BOT] Dang san bai...")

            while not self._stop.is_set():
                now = time.time()

                if max_run > 0 and (now - t0) > max_run:
                    self.log("[BOT] Het thoi gian gioi han. Dung.")
                    break

                # --- Doc toa do & di ve bai ---
                if ocr.get("enabled") and (now - last_coord_read) >= self._jit(ocr.get("read_interval", 1.0)):
                    last_coord_read = now
                    coord = ocr_coords(ocr.get("region"), ocr.get("tesseract_cmd"))
                    if coord:
                        self.cur_coord = coord
                        dx = spot["target_x"] - coord[0]
                        dy = spot["target_y"] - coord[1]
                        dist = (dx * dx + dy * dy) ** 0.5
                        self.status = f"Toa do {coord} | cach bai {dist:.0f}"
                        if dist > spot.get("radius", 8):
                            self._walk_toward(dx, dy, spot)
                            last_recenter = now
                            continue  # uu tien di ve bai truoc khi danh

                # --- Recenter dinh ky (khong OCR thi click ve giua man hinh) ---
                if not ocr.get("enabled") and (now - last_recenter) >= self._jit(spot.get("recenter_every", 6.0)):
                    last_recenter = now
                    sw, sh = screen_size()
                    click_at(sw // 2, sh // 2, button="right")

                # --- Uong HP/MP ---
                if pots.get("enabled") and (now - last_pot_check) >= pots.get("check_interval", 0.4):
                    last_pot_check = now
                    if (now - last_pot) >= pots.get("pot_cooldown", 0.6):
                        if self._check_pot(pots):
                            last_pot = now

                # --- Buff dinh ky ---
                if hunt.get("buff_keys") and (now - last_buff) >= self._jit(hunt.get("buff_interval", 60.0)):
                    last_buff = now
                    for k in hunt["buff_keys"]:
                        press_key(k)
                        time.sleep(0.15)
                    self.log("[BOT] Buff lai.")

                # --- Nhat do ---
                if hunt.get("pickup_key") and (now - last_pickup) >= self._jit(hunt.get("pickup_interval", 2.5)):
                    last_pickup = now
                    press_key(hunt["pickup_key"])

                # --- Danh quai ---
                if (now - last_attack) >= self._jit(hunt.get("attack_interval", 0.25)):
                    last_attack = now
                    for k in hunt.get("attack_keys", []):
                        press_key(k, hold=hunt.get("attack_hold", False))

                time.sleep(0.03)

        except Exception:
            self.log("[BOT] LOI:\n" + traceback.format_exc())
        finally:
            self.running = False
            self.status = "Dung"

    def _walk_toward(self, dx, dy, spot):
        """Di chuyen nhan vat ve huong bai bang cach click len mat dat.

        Trong MU, click chuot trai len mat dat = di bo ve do. Ta click lech tam
        man hinh theo huong (dx,dy) mot doan walk_step_px.
        """
        sw, sh = screen_size()
        cx, cy = sw // 2, sh // 2  # nhan vat luon o giua man hinh
        norm = (dx * dx + dy * dy) ** 0.5 or 1.0
        step = spot.get("walk_step_px", 90)
        # Truc toa do MU: X tang sang phai-xuong, Y tang trai-xuong (tuy server).
        # Quy uoc don gian: dx>0 di sang phai man hinh, dy>0 di xuong.
        tx = cx + (dx / norm) * step
        ty = cy + (dy / norm) * step
        move_cmd = self.cfg["hunt"].get("move_cmd_key")
        if move_cmd:
            press_key(move_cmd)  # mo o chat /move neu server ho tro (nang cao)
        click_at(tx, ty, button="left")
        time.sleep(self._jit(spot.get("walk_click_delay", 0.35)))

    def _check_pot(self, pots):
        used = False
        try:
            hp = pots["hp_bar"]
            ratio = bar_fill_ratio(hp["x"], hp["y"], pots["full_color"], pots["empty_color"])
            if ratio < hp.get("threshold", 0.55):
                press_key(pots.get("hp_key"))
                self.log(f"[POT] HP {ratio:.0%} -> uong mau.")
                used = True
        except Exception:
            pass
        try:
            mp = pots["mp_bar"]
            ratio = bar_fill_ratio(mp["x"], mp["y"], pots["full_color"], pots["empty_color"])
            if ratio < mp.get("threshold", 0.30):
                press_key(pots.get("mp_key"))
                self.log(f"[POT] MP {ratio:.0%} -> uong mana.")
                used = True
        except Exception:
            pass
        return used


# =====================================================================================
#  GUI
# =====================================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MU Auto Bai - Fast Mu")
        self.root.geometry("560x640")
        self.cfg = load_config()
        self.bot = AutoBot(self.cfg, self.log)
        self.vars = {}
        self._build()
        self._register_hotkeys()
        self._poll_status()
        if _IMPORT_ERRORS:
            self.log("[!] Thieu thu vien (cai bang: pip install -r requirements.txt):")
            for k, v in _IMPORT_ERRORS.items():
                self.log(f"    - {k}: {v}")

    def _build(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        f_main = ttk.Frame(nb)
        f_spot = ttk.Frame(nb)
        f_hunt = ttk.Frame(nb)
        f_pot = ttk.Frame(nb)
        nb.add(f_main, text="Chinh")
        nb.add(f_spot, text="Bai / Toa do")
        nb.add(f_hunt, text="San quai")
        nb.add(f_pot, text="HP/MP")

        # --- Tab Chinh ---
        top = ttk.Frame(f_main)
        top.pack(fill="x", pady=6)
        self.btn_toggle = ttk.Button(top, text="BAT (F8)", command=self.toggle)
        self.btn_toggle.pack(side="left", padx=4)
        ttk.Button(top, text="Luu config", command=self.save).pack(side="left", padx=4)
        ttk.Button(top, text="Lay toa do chuot", command=self.pick_mouse).pack(side="left", padx=4)

        self.lbl_status = ttk.Label(f_main, text="Trang thai: Dung", foreground="#0a0")
        self.lbl_status.pack(anchor="w", padx=4)

        ttk.Label(f_main, text="Nhat ky:").pack(anchor="w", padx=4)
        self.txt = tk.Text(f_main, height=18, wrap="word")
        self.txt.pack(fill="both", expand=True, padx=4, pady=4)

        # --- Tab Bai ---
        self._row(f_spot, "Ten bai", ["spot", "name"])
        self._row(f_spot, "Toa do X dich", ["spot", "target_x"], int)
        self._row(f_spot, "Toa do Y dich", ["spot", "target_y"], int)
        self._row(f_spot, "Ban kinh (o)", ["spot", "radius"], int)
        self._row(f_spot, "Buoc di (px moi click)", ["spot", "walk_step_px"], int)
        self._row(f_spot, "Delay sau moi click di (s)", ["spot", "walk_click_delay"], float)
        self._chk(f_spot, "Bat doc toa do OCR", ["coord_ocr", "enabled"])
        self._row(f_spot, "Vung OCR [L,T,W,H]", ["coord_ocr", "region"], "list")
        self._row(f_spot, "Duong dan tesseract.exe", ["coord_ocr", "tesseract_cmd"])
        self._row(f_spot, "Chu ky doc toa do (s)", ["coord_ocr", "read_interval"], float)

        # --- Tab San quai ---
        self._row(f_hunt, "Phim danh (cach nhau dau phay)", ["hunt", "attack_keys"], "csv")
        self._chk(f_hunt, "Giu phim danh (hold)", ["hunt", "attack_hold"])
        self._row(f_hunt, "Chu ky danh (s)", ["hunt", "attack_interval"], float)
        self._row(f_hunt, "Phim nhat do", ["hunt", "pickup_key"])
        self._row(f_hunt, "Chu ky nhat do (s)", ["hunt", "pickup_interval"], float)
        self._row(f_hunt, "Phim buff (cach dau phay)", ["hunt", "buff_keys"], "csv")
        self._row(f_hunt, "Chu ky buff (s)", ["hunt", "buff_interval"], float)

        # --- Tab HP/MP ---
        self._chk(f_pot, "Bat auto pot", ["potions", "enabled"])
        self._row(f_pot, "Phim uong mau (HP)", ["potions", "hp_key"])
        self._row(f_pot, "Phim uong mana (MP)", ["potions", "mp_key"])
        self._row(f_pot, "Pixel HP bar X", ["potions", "hp_bar", "x"], int)
        self._row(f_pot, "Pixel HP bar Y", ["potions", "hp_bar", "y"], int)
        self._row(f_pot, "Nguong HP (0..1)", ["potions", "hp_bar", "threshold"], float)
        self._row(f_pot, "Pixel MP bar X", ["potions", "mp_bar", "x"], int)
        self._row(f_pot, "Pixel MP bar Y", ["potions", "mp_bar", "y"], int)
        self._row(f_pot, "Nguong MP (0..1)", ["potions", "mp_bar", "threshold"], float)
        ttk.Button(f_pot, text="Test doc HP/MP bay gio", command=self.test_bars).pack(anchor="w", padx=6, pady=6)

    # -- helpers tao form --
    def _get(self, path):
        cur = self.cfg
        for p in path:
            cur = cur[p]
        return cur

    def _set(self, path, val):
        cur = self.cfg
        for p in path[:-1]:
            cur = cur[p]
        cur[path[-1]] = val

    def _row(self, parent, label, path, cast=str):
        fr = ttk.Frame(parent)
        fr.pack(fill="x", padx=6, pady=3)
        ttk.Label(fr, text=label, width=28).pack(side="left")
        var = tk.StringVar()
        val = self._get(path)
        if cast == "csv":
            var.set(",".join(map(str, val)))
        elif cast == "list":
            var.set(",".join(map(str, val)))
        else:
            var.set("" if val is None else str(val))
        ent = ttk.Entry(fr, textvariable=var)
        ent.pack(side="left", fill="x", expand=True)
        self.vars[tuple(path)] = (var, cast)
        return var

    def _chk(self, parent, label, path):
        fr = ttk.Frame(parent)
        fr.pack(fill="x", padx=6, pady=3)
        var = tk.BooleanVar(value=bool(self._get(path)))
        ttk.Checkbutton(fr, text=label, variable=var).pack(side="left")
        self.vars[tuple(path)] = (var, "bool")

    def _collect(self):
        for path, (var, cast) in self.vars.items():
            path = list(path)
            if cast == "bool":
                self._set(path, bool(var.get()))
                continue
            raw = var.get().strip()
            try:
                if cast is int:
                    self._set(path, int(float(raw)))
                elif cast is float:
                    self._set(path, float(raw))
                elif cast == "csv":
                    self._set(path, [s.strip() for s in raw.split(",") if s.strip()])
                elif cast == "list":
                    self._set(path, [int(float(s)) for s in raw.split(",") if s.strip()])
                else:
                    self._set(path, None if raw == "" else raw)
            except Exception:
                pass

    # -- actions --
    def save(self):
        self._collect()
        save_config(self.cfg)
        self.log("[OK] Da luu config.json")

    def toggle(self):
        if self.bot.running:
            self.bot.stop()
            self.btn_toggle.config(text="BAT (F8)")
        else:
            self._collect()
            self.bot.cfg = self.cfg
            self.bot.start()
            self.btn_toggle.config(text="TAT (F8)")

    def panic(self):
        self.bot.stop()
        self.btn_toggle.config(text="BAT (F8)")
        self.log("[PANIC] Dung khan cap (F9).")

    def pick_mouse(self):
        if pyautogui is None:
            self.log("[!] Can pyautogui de lay toa do chuot.")
            return
        self.log("[i] Dua chuot toi vi tri can lay, giu yen 3s...")

        def worker():
            time.sleep(3)
            x, y = pyautogui.position()
            self.log(f"[i] Toa do chuot: X={x} Y={y}")
        threading.Thread(target=worker, daemon=True).start()

    def test_bars(self):
        self._collect()
        p = self.cfg["potions"]
        try:
            hp = bar_fill_ratio(p["hp_bar"]["x"], p["hp_bar"]["y"], p["full_color"], p["empty_color"])
            mp = bar_fill_ratio(p["mp_bar"]["x"], p["mp_bar"]["y"], p["full_color"], p["empty_color"])
            self.log(f"[TEST] HP~{hp:.0%}  MP~{mp:.0%}  (nguong HP<{p['hp_bar']['threshold']}, MP<{p['mp_bar']['threshold']})")
        except Exception as e:
            self.log(f"[TEST] Loi doc bar: {e}")

    def _register_hotkeys(self):
        if kb is None:
            self.log("[!] Khong co thu vien 'keyboard' -> hotkey toan cuc tat. Dung nut trong GUI.")
            return
        try:
            kb.add_hotkey(self.cfg["hotkeys"].get("toggle", "f8"), lambda: self.root.after(0, self.toggle))
            kb.add_hotkey(self.cfg["hotkeys"].get("panic", "f9"), lambda: self.root.after(0, self.panic))
            self.log(f"[OK] Hotkey: {self.cfg['hotkeys'].get('toggle','f8').upper()} bat/tat, "
                     f"{self.cfg['hotkeys'].get('panic','f9').upper()} panic.")
        except Exception as e:
            self.log(f"[!] Dang ky hotkey loi (thu chay bang quyen Admin): {e}")

    def _poll_status(self):
        st = self.bot.status
        self.lbl_status.config(text=f"Trang thai: {st}",
                               foreground="#0a0" if self.bot.running else "#a00")
        self.root.after(400, self._poll_status)

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        try:
            self.txt.insert("end", f"{ts}  {msg}\n")
            self.txt.see("end")
        except Exception:
            print(msg)


def main():
    if os.name != "nt":
        print("[!] Luu y: app nay thiet ke cho Windows. Tren OS khac chi mo duoc GUI de config.")
    root = tk.Tk()
    app = App(root)

    def on_close():
        try:
            app.bot.stop()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
