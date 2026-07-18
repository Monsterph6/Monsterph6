#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MU Auto Bai SS21 - Tu dong chay bai theo toa do cho MU Online Season 21 (Fast Mu).

Thiet ke cho loi choi BANG CHUOT cua SS21:
  - Chuot TRAI  = di chuyen (click xuong dat)
  - Chuot PHAI  = danh skill tai vi tri con tro
  - MU Helper   = auto co san trong game (bat/tat bang phim Home), tu danh + nhat do + uong pot

App nay dong vai "nguoi canh toa do":
  1. Doc toa do nhan vat bang OCR -> neu lech khoi bai thi TAT MU Helper, chuot trai
     di ve bai, toi noi BAT lai MU Helper (che do "helper" - khuyen dung).
  2. Hoac tu danh bang chuot phai xoay quanh nhan vat (che do "mouse") neu ban
     khong muon dung MU Helper.
  - Camera MU la isometric nen huong X/Y trong game != huong ngang/doc man hinh.
    App co nut TU HIEU CHINH: tu click thu 2 huong, doc toa do thay doi, tinh ra
    ma tran chuyen huong game -> man hinh.

Hotkey: F8 bat/tat, F9 dung khan cap. Chay tren WINDOWS bang quyen Administrator.

    python muauto.py
"""

import json
import os
import re
import sys
import time
import math
import random
import threading
import traceback

# ---- Import thu vien (chiu loi mem de GUI van mo duoc de config) ----
_IMPORT_ERRORS = {}

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
EXAMPLE_PATH = os.path.join(BASE_DIR, "config.example.json")


def load_config():
    path = CONFIG_PATH if os.path.exists(CONFIG_PATH) else EXAMPLE_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# =====================================================================================
#  INPUT: chuot / phim
# =====================================================================================
def press_key(key):
    if not key:
        return False
    if pydirectinput is not None:
        try:
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


def type_chat(text, enter_delay=0.25):
    """Go 1 lenh vao khung chat cua MU: Enter -> go lenh -> Enter."""
    if not text:
        return False
    ok = press_key("enter")
    time.sleep(enter_delay)
    typed = False
    if pydirectinput is not None:
        try:
            pydirectinput.typewrite(text, interval=0.03)
            typed = True
        except Exception:
            pass
    if not typed and pyautogui is not None:
        try:
            pyautogui.write(text, interval=0.03)
            typed = True
        except Exception:
            pass
    time.sleep(enter_delay)
    press_key("enter")
    return ok and typed


def click_at(x, y, button="left", jitter=True, move_first=True):
    """Click chuot tai (x, y) man hinh. Tra ve True neu gui duoc."""
    if jitter:
        x += random.randint(-4, 4)
        y += random.randint(-4, 4)
    x, y = int(x), int(y)
    if pydirectinput is not None:
        try:
            if move_first:
                pydirectinput.moveTo(x, y)
                time.sleep(0.02)
            pydirectinput.click(x, y, button=button)
            return True
        except Exception:
            pass
    if pyautogui is not None:
        try:
            pyautogui.click(x, y, button=button)
            return True
        except Exception:
            pass
    return False


# =====================================================================================
#  CUA SO GAME (Win32): tim cua so, doc title (Level/RR/GR), vi tri client
# =====================================================================================
_SELECTED_HWND = None  # cua so game nguoi dung chon trong GUI (uu tien tuyet doi)


def set_selected_hwnd(hwnd):
    global _SELECTED_HWND
    _SELECTED_HWND = hwnd


def _window_title_of(hwnd):
    try:
        import ctypes
        user32 = ctypes.windll.user32
        n = user32.GetWindowTextLengthW(hwnd)
        if n <= 0:
            return ""
        buf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, buf, n + 1)
        return buf.value
    except Exception:
        return ""


def list_windows():
    """Liet ke cac cua so dang mo: [(hwnd, title, ten_exe), ...]."""
    if os.name != "nt":
        return []
    out = []
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        def exe_of(hwnd):
            try:
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                # PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                h = kernel32.OpenProcess(0x1000, False, pid.value)
                if not h:
                    return ""
                try:
                    buf = ctypes.create_unicode_buffer(512)
                    size = wintypes.DWORD(512)
                    if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
                        return os.path.basename(buf.value)
                finally:
                    kernel32.CloseHandle(h)
            except Exception:
                pass
            return ""

        @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        def cb(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                title = _window_title_of(hwnd)
                if title.strip():
                    out.append((hwnd, title, exe_of(hwnd)))
            return True

        user32.EnumWindows(cb, 0)
    except Exception:
        pass
    return out


def _find_game_window(title_substr):
    """Tim cua so game. Uu tien cua so da CHON trong GUI; sau do moi tim theo
    tu khoa title. Tra ve (hwnd, title) hoac None."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        user32 = ctypes.windll.user32
        # 1) Cua so nguoi dung da chon (chinh xac nhat, ho tro mo nhieu acc)
        if _SELECTED_HWND and user32.IsWindow(_SELECTED_HWND):
            return (_SELECTED_HWND, _window_title_of(_SELECTED_HWND))
        # 2) Tim theo tu khoa
        if not title_substr:
            return None
        for hwnd, title, _exe in list_windows():
            if title_substr.lower() in title.lower():
                return (hwnd, title)
        return None
    except Exception:
        return None


def get_game_title(title_substr):
    """Tra ve chuoi title day du cua cua so game, hoac None."""
    r = _find_game_window(title_substr)
    return r[1] if r else None


def parse_title_stats(title):
    """Phan tich title kieu FASTMU:
    [FASTMU] [Char: MonsF] [Level: 400 + 451] [RR: 14 / GR: 0] - ServerTime: ...
    Tra ve dict {char, level, master, rr, gr} (thieu truong nao thi None).
    """
    if not title:
        return None
    out = {"char": None, "level": None, "master": None, "rr": None, "gr": None}
    m = re.search(r"Char:\s*([^\]]+)\]", title)
    if m:
        out["char"] = m.group(1).strip()
    m = re.search(r"Level:\s*(\d+)(?:\s*\+\s*(\d+))?", title)
    if m:
        out["level"] = int(m.group(1))
        out["master"] = int(m.group(2)) if m.group(2) else None
    m = re.search(r"RR:\s*(\d+)", title)
    if m:
        out["rr"] = int(m.group(1))
    m = re.search(r"GR:\s*(\d+)", title)
    if m:
        out["gr"] = int(m.group(1))
    if out["level"] is None and out["rr"] is None:
        return None
    return out


def get_client_rect(title_substr):
    """Vi tri + kich thuoc vung client cua cua so game tren man hinh.
    Tra ve (left, top, width, height) hoac None."""
    r = _find_game_window(title_substr)
    if not r:
        return None
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        hwnd = r[0]
        rc = wintypes.RECT()
        if not user32.GetClientRect(hwnd, ctypes.byref(rc)):
            return None
        pt = wintypes.POINT(0, 0)
        user32.ClientToScreen(hwnd, ctypes.byref(pt))
        return (pt.x, pt.y, rc.right - rc.left, rc.bottom - rc.top)
    except Exception:
        return None


# =====================================================================================
#  MAN HINH: chup vung, doc mau, OCR toa do
# =====================================================================================
def screen_size():
    if pyautogui is not None:
        try:
            s = pyautogui.size()
            return (s[0], s[1])
        except Exception:
            pass
    return (1920, 1080)


def grab_region(region):
    """region = [left, top, width, height] -> numpy RGB hoac None."""
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
    """Uoc luong % day cua thanh mau/mana theo mau pixel tai (x, y)."""
    px = np.array(get_pixel(x, y), dtype=float)
    full = np.array(full_color, dtype=float)
    empty = np.array(empty_color, dtype=float)
    d_full = np.linalg.norm(px - full)
    d_empty = np.linalg.norm(px - empty)
    total = d_full + d_empty
    if total < 1e-6:
        return 1.0
    return float(d_empty / total)


def ocr_coords(region, tesseract_cmd=None):
    """Doc toa do 'x, y' tu vung region. Tra ve (x, y) hoac None."""
    if pytesseract is None:
        return None
    if tesseract_cmd and os.path.exists(tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    img = grab_region(region)
    if img is None:
        return None
    try:
        pil = Image.fromarray(img).convert("L")
        pil = pil.point(lambda p: 255 if p > 130 else 0)
        pil = pil.resize((pil.width * 3, pil.height * 3))
        txt = pytesseract.image_to_string(
            pil, config="--psm 7 -c tessedit_char_whitelist=0123456789,: "
        )
    except Exception:
        return None
    digits, cur = [], ""
    for ch in txt:
        if ch.isdigit():
            cur += ch
        else:
            if cur:
                digits.append(int(cur))
                cur = ""
    if cur:
        digits.append(int(cur))
    # Toa do MU nam trong 0..255
    nums = [d for d in digits if 0 <= d <= 255]
    if len(nums) >= 2:
        return (nums[0], nums[1])
    return None


def ocr_number(region, tesseract_cmd=None, max_val=9999):
    """Doc 1 con so (vd: level) tu vung region. Tra ve int hoac None."""
    if pytesseract is None:
        return None
    if tesseract_cmd and os.path.exists(tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    img = grab_region(region)
    if img is None:
        return None
    try:
        pil = Image.fromarray(img).convert("L")
        pil = pil.point(lambda p: 255 if p > 130 else 0)
        pil = pil.resize((pil.width * 3, pil.height * 3))
        txt = pytesseract.image_to_string(
            pil, config="--psm 7 -c tessedit_char_whitelist=0123456789"
        )
    except Exception:
        return None
    cur = "".join(ch for ch in txt if ch.isdigit())
    if not cur:
        return None
    try:
        val = int(cur)
    except ValueError:
        return None
    return val if 0 < val <= max_val else None


# =====================================================================================
#  BOT
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
        self.helper_on = False

    # ---------- vong doi ----------
    def start(self):
        if self.running:
            return
        self._stop.clear()
        self.running = True
        self.helper_on = False
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.running = False
        self.status = "Dung"
        self.log("[BOT] Da dung. (MU Helper trong game giu nguyen trang thai hien tai)")

    def _jit(self, base):
        if self.cfg.get("safety", {}).get("human_jitter", True):
            return base * random.uniform(0.85, 1.15)
        return base

    # ---------- cua so game ----------
    def _client_rect(self):
        """(left, top, w, h) cua vung client game; fallback = toan man hinh."""
        rect = get_client_rect(self.cfg.get("window_title", ""))
        if rect:
            return rect
        sw, sh = screen_size()
        return (0, 0, sw, sh)

    def _abs_region(self, region):
        """Doi region [L,T,W,H] tuong doi cua so game -> toa do man hinh tuyet doi."""
        if not region:
            return region
        if self.cfg.get("coord_ocr", {}).get("relative_to_window", True):
            l, t, _, _ = self._client_rect()
            return [region[0] + l, region[1] + t, region[2], region[3]]
        return region

    def _center(self):
        """Tam cua so game (noi nhan vat dung)."""
        l, t, w, h = self._client_rect()
        return (l + w // 2, t + h // 2)

    def title_stats(self):
        return parse_title_stats(get_game_title(self.cfg.get("window_title", "")))

    # ---------- huong di: game -> man hinh ----------
    def _game_to_screen(self, dx, dy):
        """Chuyen vector (dx, dy) trong GAME thanh vector man hinh theo ma tran axis."""
        ax = self.cfg["axis"]["x_screen"]
        ay = self.cfg["axis"]["y_screen"]
        sx = dx * ax[0] + dy * ay[0]
        sy = dx * ax[1] + dy * ay[1]
        n = math.hypot(sx, sy)
        if n < 1e-6:
            return (0.0, 0.0)
        return (sx / n, sy / n)

    def read_coord(self):
        ocr = self.cfg["coord_ocr"]
        return ocr_coords(self._abs_region(ocr.get("region")), ocr.get("tesseract_cmd"))

    def calibrate_axis(self):
        """Tu hieu chinh huong: click thu 2 huong man hinh, xem toa do game doi the nao.

        Ket qua: ma tran game->man hinh luu vao config["axis"].
        """
        ax = self.cfg["axis"]
        step = ax.get("calib_step_px", 140)
        wait = ax.get("calib_wait", 2.0)
        cx, cy = self._center()

        self.log("[CALIB] Bat dau hieu chinh huong di (dung yen, khong dung chuot)...")
        p0 = self.read_coord()
        if not p0:
            self.log("[CALIB] Khong doc duoc toa do. Kiem tra vung OCR truoc.")
            return False

        # Buoc 1: click sang PHAI man hinh
        click_at(cx + step, cy, jitter=False)
        time.sleep(wait)
        p1 = self.read_coord()
        # Buoc 2: click XUONG man hinh
        click_at(cx, cy + step, jitter=False)
        time.sleep(wait)
        p2 = self.read_coord()
        if not p1 or not p2:
            self.log("[CALIB] Doc toa do that bai giua chung. Thu lai.")
            return False

        # dG1 = thay doi game khi di theo (+1, 0) man hinh; dG2 = theo (0, +1) man hinh
        dg1 = (p1[0] - p0[0], p1[1] - p0[1])
        dg2 = (p2[0] - p1[0], p2[1] - p1[1])
        det = dg1[0] * dg2[1] - dg1[1] * dg2[0]
        if abs(det) < 1e-6 or (dg1 == (0, 0)) or (dg2 == (0, 0)):
            self.log(f"[CALIB] Du lieu xau (dg1={dg1}, dg2={dg2}). Nhan vat co di chuyen khong?")
            return False

        # Ma tran M: man hinh -> game la [[dg1x, dg2x], [dg1y, dg2y]] (chuan hoa theo step)
        # Ta can game -> man hinh: nghich dao M roi nhan step.
        inv = [
            [dg2[1] / det, -dg2[0] / det],
            [-dg1[1] / det, dg1[0] / det],
        ]
        # Cot 1: huong man hinh cho +X game; cot 2: cho +Y game
        x_screen = [inv[0][0], inv[1][0]]
        y_screen = [inv[0][1], inv[1][1]]
        # Chuan hoa do dai 1
        for v in (x_screen, y_screen):
            n = math.hypot(v[0], v[1])
            if n > 1e-9:
                v[0], v[1] = v[0] / n, v[1] / n
        self.cfg["axis"]["x_screen"] = [round(x_screen[0], 3), round(x_screen[1], 3)]
        self.cfg["axis"]["y_screen"] = [round(y_screen[0], 3), round(y_screen[1], 3)]
        self.log(f"[CALIB] Xong! +X game -> man hinh {self.cfg['axis']['x_screen']}, "
                 f"+Y game -> {self.cfg['axis']['y_screen']}. Nho bam 'Luu config'.")
        return True

    # ---------- MU Helper ----------
    def _helper_toggle(self):
        key = self.cfg["attack"].get("helper_toggle_key", "home")
        press_key(key)

    def _helper_set(self, want_on):
        if want_on == self.helper_on:
            return
        self._helper_toggle()
        self.helper_on = want_on
        self.log(f"[HELPER] {'BAT' if want_on else 'TAT'} MU Helper (phim "
                 f"{self.cfg['attack'].get('helper_toggle_key', 'home').upper()}).")

    # ---------- vong lap chinh ----------
    def _run(self):
        try:
            delay = int(self.cfg.get("safety", {}).get("start_delay_sec", 3))
            self.log(f"[BOT] Bat dau sau {delay}s - dua chuot vao cua so game...")
            for _ in range(delay * 10):
                if self._stop.is_set():
                    return
                time.sleep(0.1)

            atk = self.cfg["attack"]
            pots = self.cfg["potions"]
            spot = self.cfg["spot"]
            ocr = self.cfg["coord_ocr"]
            rst = self.cfg.get("reset", {})
            mode = atk.get("mode", "helper")

            t0 = time.time()
            last_reset_check = 0.0
            last_coord_read = 0.0
            last_attack = 0.0
            last_pickup = 0.0
            last_pot = 0.0
            last_pot_check = 0.0
            last_helper_change = 0.0
            last_progress = time.time()
            prev_dist = None
            angle_i = 0
            max_run = float(self.cfg.get("safety", {}).get("max_runtime_min", 0)) * 60.0
            at_spot = False

            self.status = "Dang chay"
            self.log(f"[BOT] Che do danh: {mode.upper()} | Bai: "
                     f"({spot['target_x']}, {spot['target_y']}) ban kinh {spot.get('radius', 10)}")

            while not self._stop.is_set():
                now = time.time()

                if max_run > 0 and (now - t0) > max_run:
                    self.log("[BOT] Het thoi gian gioi han. Dung.")
                    break

                # ===== 0) Auto reset / grand reset =====
                if rst.get("enabled") and (now - last_reset_check) >= rst.get("check_interval", 20.0):
                    last_reset_check = now
                    if self._check_reset(rst, mode):
                        # vua reset xong: cho nhan vat hoi sinh o lang roi di lai
                        at_spot = False
                        prev_dist = None
                        last_progress = time.time()
                        continue

                # ===== 1) Doc toa do & quyet dinh di hay danh =====
                if ocr.get("enabled") and (now - last_coord_read) >= self._jit(ocr.get("read_interval", 1.0)):
                    last_coord_read = now
                    coord = self.read_coord()
                    if coord:
                        self.cur_coord = coord
                        dx = spot["target_x"] - coord[0]
                        dy = spot["target_y"] - coord[1]
                        dist = math.hypot(dx, dy)
                        self.status = f"Toa do {coord} | cach bai {dist:.0f} o"

                        if dist > spot.get("radius", 10):
                            # --- Lech bai: tat helper (neu dang bat) roi di ve ---
                            at_spot = False
                            if mode == "helper" and self.helper_on and \
                               (now - last_helper_change) > atk.get("helper_rearm_delay", 3.0):
                                self._helper_set(False)
                                last_helper_change = now
                            if not self.helper_on:
                                self._walk_toward(dx, dy, spot)
                            # phat hien ket (khong tien bo)
                            if prev_dist is None or dist < prev_dist - 1:
                                last_progress = now
                                prev_dist = dist
                            elif (now - last_progress) > spot.get("stuck_timeout", 8.0):
                                self._unstick(spot)
                                last_progress = now
                                prev_dist = None
                            continue
                        else:
                            # --- Dang o trong bai ---
                            prev_dist = None
                            last_progress = now
                            if not at_spot:
                                at_spot = True
                                self.log(f"[BOT] Da toi bai {coord}.")
                            if mode == "helper" and not self.helper_on and \
                               (now - last_helper_change) > atk.get("helper_rearm_delay", 3.0):
                                self._helper_set(True)
                                last_helper_change = now
                    else:
                        self.status = "Khong doc duoc toa do (OCR)"

                if not ocr.get("enabled"):
                    at_spot = True  # khong OCR: coi nhu luon o bai
                    if mode == "helper" and not self.helper_on:
                        self._helper_set(True)
                        last_helper_change = now

                # ===== 2) Danh bang chuot phai (che do "mouse") =====
                if mode == "mouse" and at_spot and \
                   (now - last_attack) >= self._jit(atk.get("mouse_interval", 0.5)):
                    last_attack = now
                    angle_i = (angle_i + 1) % max(1, int(atk.get("mouse_angles", 8)))
                    self._mouse_attack(angle_i, atk)

                # ===== 3) Nhat do (tuy chon, chi can o che do "mouse") =====
                pk_int = float(atk.get("pickup_interval", 0) or 0)
                if mode == "mouse" and pk_int > 0 and atk.get("pickup_key") and \
                   (now - last_pickup) >= self._jit(pk_int):
                    last_pickup = now
                    press_key(atk["pickup_key"])

                # ===== 4) Auto pot (tuy chon - Helper thuong tu lo) =====
                if pots.get("enabled") and (now - last_pot_check) >= pots.get("check_interval", 0.4):
                    last_pot_check = now
                    if (now - last_pot) >= pots.get("pot_cooldown", 0.6):
                        if self._check_pot(pots):
                            last_pot = now

                time.sleep(0.03)

        except Exception:
            self.log("[BOT] LOI:\n" + traceback.format_exc())
        finally:
            self.running = False
            self.status = "Dung"

    def _walk_toward(self, dx, dy, spot):
        """Chuot trai click xuong dat theo huong bai (da qua ma tran isometric)."""
        cx, cy = self._center()
        ux, uy = self._game_to_screen(dx, dy)
        step = spot.get("walk_step_px", 110)
        click_at(cx + ux * step, cy + uy * step, button="left")
        time.sleep(self._jit(spot.get("walk_click_delay", 0.45)))

    def _unstick(self, spot):
        """Bi ket (khong tien bo): click sang huong ngau nhien de lach vat can."""
        cx, cy = self._center()
        a = random.uniform(0, 2 * math.pi)
        step = spot.get("walk_step_px", 110)
        self.log("[BOT] Co ve bi ket, thu lach sang huong khac...")
        click_at(cx + math.cos(a) * step, cy + math.sin(a) * step, button="left")
        time.sleep(0.6)

    def _mouse_attack(self, angle_i, atk):
        """Chuot phai (skill) tai diem xoay quanh nhan vat."""
        cx, cy = self._center()
        n = max(1, int(atk.get("mouse_angles", 8)))
        a = (2 * math.pi / n) * angle_i + random.uniform(-0.2, 0.2)
        r = atk.get("mouse_radius_px", 170) * random.uniform(0.8, 1.1)
        click_at(cx + math.cos(a) * r, cy + math.sin(a) * r, button="right")

    def _check_reset(self, rst, mode):
        """Kiem tra level -> go /reset, du RR -> go /grandreset.

        Uu tien doc Level/RR tu TITLE cua so game (kieu FASTMU:
        "[Level: 400 + 451] [RR: 14 / GR: 0]") - chinh xac 100%.
        Khong co title thi fallback OCR vung level_region.
        Tra ve True neu vua reset (de vong lap chinh lam moi trang thai di bai).
        """
        stats = self.title_stats()
        if stats and stats.get("level") is not None:
            lvl = stats["level"]
            src = "title"
        else:
            lvl = ocr_number(self._abs_region(rst.get("level_region")),
                             self.cfg["coord_ocr"].get("tesseract_cmd"))
            src = "ocr"
        if lvl is None:
            return False
        need = int(rst.get("reset_level", 400))
        if stats:
            self.status = (f"Lv {lvl}/{need} RR {stats.get('rr')} "
                           f"GR {stats.get('gr')} | {self.status}")
        if lvl < need:
            return False

        self.log(f"[RESET] Level {lvl} >= {need} (nguon: {src}) -> chuan bi reset...")
        # Tat MU Helper truoc khi go lenh (de phim Enter khong bi nuot)
        if mode == "helper" and self.helper_on:
            self._helper_set(False)
        time.sleep(0.8)

        type_chat(rst.get("reset_command", "/reset"))
        self.log(f"[RESET] Da gui lenh {rst.get('reset_command', '/reset')}")
        time.sleep(float(rst.get("post_reset_wait", 6.0)))

        # Xac nhan reset qua title (level tut xuong / RR tang)
        new_stats = self.title_stats()
        if new_stats and new_stats.get("rr") is not None:
            rst["resets_done"] = new_stats["rr"]
            self.log(f"[RESET] RR hien tai (tu title): {new_stats['rr']}"
                     + (f", GR: {new_stats['gr']}" if new_stats.get("gr") is not None else ""))
            if new_stats.get("level") is not None and new_stats["level"] >= need:
                self.log("[RESET] Level chua tut sau khi go lenh - co the lenh sai "
                         "hoac thieu dieu kien (zen/point?). Kiem tra lai!")
        else:
            rst["resets_done"] = int(rst.get("resets_done", 0)) + 1
            self.log(f"[RESET] Tong so lan reset (dem noi bo): {rst['resets_done']}")
        try:
            save_config(self.cfg)  # luu bo dem de tat app khong mat
        except Exception:
            pass

        if rst.get("grand_enabled") and \
           int(rst.get("resets_done", 0)) >= int(rst.get("grand_after_resets", 100)):
            type_chat(rst.get("grand_command", "/grandreset"))
            self.log(f"[RESET] RR {rst['resets_done']} >= "
                     f"{rst.get('grand_after_resets')} -> da gui "
                     f"{rst.get('grand_command', '/grandreset')}!")
            rst["resets_done"] = 0
            try:
                save_config(self.cfg)
            except Exception:
                pass
            time.sleep(float(rst.get("post_reset_wait", 6.0)))

        # Quay lai map san (neu co lenh /move)
        mv = (rst.get("after_reset_move_cmd") or "").strip()
        if mv:
            type_chat(mv)
            self.log(f"[RESET] Da gui lenh ve map: {mv}")
            time.sleep(3.0)
        return True

    def _bar_ratio(self, pots, bar):
        """% day cua 1 thanh/qua cau. Mau full/empty rieng tung bar (HP do, MP xanh)."""
        x, y = bar["x"], bar["y"]
        if pots.get("relative_to_window", True):
            l, t, _, _ = self._client_rect()
            x, y = x + l, y + t
        full = bar.get("full", pots.get("full_color", [180, 40, 40]))
        empty = bar.get("empty", pots.get("empty_color", [40, 15, 15]))
        return bar_fill_ratio(x, y, full, empty)

    def _check_pot(self, pots):
        used = False
        try:
            hp = pots["hp_bar"]
            ratio = self._bar_ratio(pots, hp)
            if ratio < hp.get("threshold", 0.55):
                press_key(pots.get("hp_key"))
                self.log(f"[POT] HP {ratio:.0%} -> uong mau.")
                used = True
        except Exception:
            pass
        try:
            mp = pots["mp_bar"]
            ratio = self._bar_ratio(pots, mp)
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
        self.root.title("MU Auto Bai - Season 21 (Fast Mu)")
        self.root.geometry("580x680")
        self.cfg = load_config()
        self.bot = AutoBot(self.cfg, self.log)
        self.vars = {}
        self._build()
        self._register_hotkeys()
        self._poll_status()
        self.root.after(300, lambda: self.refresh_windows(silent=True))
        if _IMPORT_ERRORS:
            self.log("[!] Thieu thu vien (cai bang: pip install -r requirements.txt):")
            for k, v in _IMPORT_ERRORS.items():
                self.log(f"    - {k}: {v}")

    def _build(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        f_main = ttk.Frame(nb)
        f_spot = ttk.Frame(nb)
        f_atk = ttk.Frame(nb)
        f_rst = ttk.Frame(nb)
        f_pot = ttk.Frame(nb)
        nb.add(f_main, text="Chinh")
        nb.add(f_spot, text="Bai / Toa do")
        nb.add(f_atk, text="Danh quai")
        nb.add(f_rst, text="Reset")
        nb.add(f_pot, text="HP/MP (tuy chon)")

        # --- Tab Chinh ---
        # Chon cua so game tu danh sach (chinh xac, ho tro mo nhieu acc)
        fw = ttk.LabelFrame(f_main, text="Cua so game MU")
        fw.pack(fill="x", padx=4, pady=6)
        fw1 = ttk.Frame(fw)
        fw1.pack(fill="x", padx=4, pady=4)
        self.win_var = tk.StringVar()
        self.cbo_win = ttk.Combobox(fw1, textvariable=self.win_var, state="readonly")
        self.cbo_win.pack(side="left", fill="x", expand=True, padx=2)
        self.cbo_win.bind("<<ComboboxSelected>>", self.on_pick_window)
        ttk.Button(fw1, text="Lam moi", width=10, command=self.refresh_windows).pack(side="left", padx=2)
        self._win_list = []

        top = ttk.Frame(f_main)
        top.pack(fill="x", pady=6)
        self.btn_toggle = ttk.Button(top, text="BAT (F8)", command=self.toggle)
        self.btn_toggle.pack(side="left", padx=4)
        ttk.Button(top, text="Luu config", command=self.save).pack(side="left", padx=4)
        ttk.Button(top, text="Lay toa do chuot", command=self.pick_mouse).pack(side="left", padx=4)

        top2 = ttk.Frame(f_main)
        top2.pack(fill="x", pady=2)
        ttk.Button(top2, text="Test doc toa do (OCR)", command=self.test_ocr).pack(side="left", padx=4)
        ttk.Button(top2, text="Test title (Level/RR/GR)", command=self.test_title).pack(side="left", padx=4)
        ttk.Button(top2, text="Hieu chinh huong di (auto)", command=self.calibrate).pack(side="left", padx=4)

        self.lbl_status = ttk.Label(f_main, text="Trang thai: Dung", foreground="#a00")
        self.lbl_status.pack(anchor="w", padx=4, pady=2)

        ttk.Label(f_main, text="Nhat ky:").pack(anchor="w", padx=4)
        self.txt = tk.Text(f_main, height=18, wrap="word")
        self.txt.pack(fill="both", expand=True, padx=4, pady=4)

        # --- Tab Bai / Toa do ---
        self._row(f_spot, "Tu khoa title cua so game", ["window_title"])
        self._row(f_spot, "Ten bai", ["spot", "name"])
        self._row(f_spot, "Toa do X dich", ["spot", "target_x"], int)
        self._row(f_spot, "Toa do Y dich", ["spot", "target_y"], int)
        self._row(f_spot, "Ban kinh bai (o)", ["spot", "radius"], int)
        self._row(f_spot, "Buoc di (px moi click)", ["spot", "walk_step_px"], int)
        self._row(f_spot, "Delay sau moi click di (s)", ["spot", "walk_click_delay"], float)
        ttk.Separator(f_spot).pack(fill="x", pady=4)
        self._chk(f_spot, "Bat doc toa do OCR", ["coord_ocr", "enabled"])
        self._row(f_spot, "Vung OCR [L,T,W,H]", ["coord_ocr", "region"], "list")
        self._row(f_spot, "Duong dan tesseract.exe", ["coord_ocr", "tesseract_cmd"])
        self._row(f_spot, "Chu ky doc toa do (s)", ["coord_ocr", "read_interval"], float)

        # --- Tab Danh quai ---
        fr = ttk.Frame(f_atk)
        fr.pack(fill="x", padx=6, pady=4)
        ttk.Label(fr, text="Che do danh", width=28).pack(side="left")
        self.mode_var = tk.StringVar(value=self.cfg["attack"].get("mode", "mouse"))
        ttk.Radiobutton(fr, text="Chuot phai (khuyen dung)", variable=self.mode_var,
                        value="mouse").pack(side="left", padx=2)
        ttk.Radiobutton(fr, text="MU Helper", variable=self.mode_var,
                        value="helper").pack(side="left", padx=2)
        ttk.Label(f_atk, foreground="#555", wraplength=520, justify="left", text=(
            "Chuot phai: app tu danh skill bang chuot phai xoay quanh nhan vat "
            "(dung cho server da DONG MU Helper nhu FASTMU).\n"
            "MU Helper: chi dung neu server cho phep - toi bai app bam Home de BAT auto "
            "trong game, lech bai thi TAT -> di ve -> BAT lai."
        )).pack(anchor="w", padx=8, pady=4)
        ttk.Separator(f_atk).pack(fill="x", pady=4)
        self._row(f_atk, "Phim bat/tat MU Helper", ["attack", "helper_toggle_key"])
        self._row(f_atk, "Delay doi trang thai Helper (s)", ["attack", "helper_rearm_delay"], float)
        ttk.Separator(f_atk).pack(fill="x", pady=4)
        self._row(f_atk, "Ban kinh danh chuot phai (px)", ["attack", "mouse_radius_px"], int)
        self._row(f_atk, "Chu ky danh (s)", ["attack", "mouse_interval"], float)
        self._row(f_atk, "So huong xoay", ["attack", "mouse_angles"], int)
        self._row(f_atk, "Phim nhat do (de trong = tat)", ["attack", "pickup_key"])
        self._row(f_atk, "Chu ky nhat do (0 = tat)", ["attack", "pickup_interval"], float)

        # --- Tab Reset ---
        ttk.Label(f_rst, foreground="#555", wraplength=520, justify="left", text=(
            "Auto reset cho server co RESET / GRAND RESET (Fast Mu):\n"
            "App doc LEVEL bang OCR; du level thi tu go lenh reset vao chat, "
            "tu dem so lan reset de go lenh grand reset khi du moc, roi ve map va chay lai bai.\n"
            "Vung OCR level: khung [L,T,W,H] om sat con so level tren man hinh "
            "(dung nut 'Lay toa do chuot' o tab Chinh)."
        )).pack(anchor="w", padx=8, pady=4)
        self._chk(f_rst, "Bat auto reset", ["reset", "enabled"])
        self._row(f_rst, "Vung OCR level [L,T,W,H]", ["reset", "level_region"], "list")
        self._row(f_rst, "Level de reset", ["reset", "reset_level"], int)
        self._row(f_rst, "Lenh reset", ["reset", "reset_command"])
        self._row(f_rst, "Chu ky kiem tra level (s)", ["reset", "check_interval"], float)
        self._row(f_rst, "Cho sau khi reset (s)", ["reset", "post_reset_wait"], float)
        self._row(f_rst, "Lenh ve map sau reset (vd /move lorencia)", ["reset", "after_reset_move_cmd"])
        ttk.Separator(f_rst).pack(fill="x", pady=4)
        self._chk(f_rst, "Bat auto GRAND reset", ["reset", "grand_enabled"])
        self._row(f_rst, "Lenh grand reset", ["reset", "grand_command"])
        self._row(f_rst, "Grand reset sau bao nhieu lan reset", ["reset", "grand_after_resets"], int)
        self._row(f_rst, "So lan reset da dem (tu dong)", ["reset", "resets_done"], int)
        fr_rst = ttk.Frame(f_rst)
        fr_rst.pack(fill="x", padx=6, pady=4)
        ttk.Button(fr_rst, text="Test doc level (OCR)", command=self.test_level).pack(side="left", padx=2)
        ttk.Button(fr_rst, text="Gui lenh reset ngay", command=self.manual_reset).pack(side="left", padx=2)

        # --- Tab HP/MP ---
        ttk.Label(f_pot, foreground="#555", wraplength=520, justify="left", text=(
            "SS21: MU Helper trong game da tu uong pot, nen phan nay MAC DINH TAT.\n"
            "Chi bat neu ban dung che do 'Chuot phai' va muon app tu canh mau."
        )).pack(anchor="w", padx=8, pady=4)
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

    # -- helpers form --
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
        if cast in ("csv", "list"):
            var.set(",".join(map(str, val)))
        else:
            var.set("" if val is None else str(val))
        ttk.Entry(fr, textvariable=var).pack(side="left", fill="x", expand=True)
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
        self.cfg["attack"]["mode"] = self.mode_var.get()

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

    def test_ocr(self):
        self._collect()

        def worker():
            c = self.bot.read_coord()
            if c:
                self.log(f"[OCR] Doc duoc toa do: {c}")
            else:
                self.log("[OCR] KHONG doc duoc. Chinh lai 'Vung OCR [L,T,W,H]' cho om sat so toa do.")
        threading.Thread(target=worker, daemon=True).start()

    def calibrate(self):
        if self.bot.running:
            self.log("[!] Dung bot truoc khi hieu chinh.")
            return
        self._collect()
        self.bot.cfg = self.cfg
        self.log("[CALIB] Se click thu 2 huong sau 3s - dam bao cua so game dang mo, nhan vat dung noi trong...")

        def worker():
            time.sleep(3)
            self.bot.calibrate_axis()
        threading.Thread(target=worker, daemon=True).start()

    def test_level(self):
        self._collect()

        def worker():
            lvl = ocr_number(self.cfg["reset"].get("level_region"),
                             self.cfg["coord_ocr"].get("tesseract_cmd"))
            if lvl is not None:
                self.log(f"[OCR] Level doc duoc: {lvl}")
            else:
                self.log("[OCR] KHONG doc duoc level. Chinh lai 'Vung OCR level' cho om sat con so.")
        threading.Thread(target=worker, daemon=True).start()

    def manual_reset(self):
        self._collect()
        cmd = self.cfg["reset"].get("reset_command", "/reset")
        self.log(f"[RESET] Se go '{cmd}' vao game sau 3s - dua chuot vao cua so game...")

        def worker():
            time.sleep(3)
            type_chat(cmd)
            self.log(f"[RESET] Da gui lenh {cmd}")
        threading.Thread(target=worker, daemon=True).start()

    def test_bars(self):
        self._collect()
        self.bot.cfg = self.cfg
        p = self.cfg["potions"]
        try:
            hp = self.bot._bar_ratio(p, p["hp_bar"])
            mp = self.bot._bar_ratio(p, p["mp_bar"])
            self.log(f"[TEST] HP~{hp:.0%}  MP~{mp:.0%}")
        except Exception as e:
            self.log(f"[TEST] Loi doc bar: {e}")

    def refresh_windows(self, silent=False):
        """Nap lai danh sach cua so dang mo vao combobox."""
        self._win_list = list_windows()
        kw = (self.cfg.get("window_title") or "").lower()
        # Uu tien day cua so giong game len dau danh sach
        self._win_list.sort(key=lambda w: 0 if (kw and kw in w[1].lower()) else 1)
        vals = [f"{title}   [{exe}]" if exe else title for _hw, title, exe in self._win_list]
        self.cbo_win["values"] = vals
        if not vals:
            if not silent:
                self.log("[WIN] Khong liet ke duoc cua so (chi chay tren Windows).")
            return
        # Tu chon san cua so khop tu khoa
        if kw:
            for i, (_hw, title, _exe) in enumerate(self._win_list):
                if kw in title.lower():
                    self.cbo_win.current(i)
                    self.on_pick_window()
                    break
        if not silent:
            self.log(f"[WIN] Tim thay {len(vals)} cua so. Chon dung cua so MU trong danh sach.")

    def on_pick_window(self, _event=None):
        i = self.cbo_win.current()
        if i < 0 or i >= len(self._win_list):
            return
        hwnd, title, exe = self._win_list[i]
        set_selected_hwnd(hwnd)
        self.log(f"[WIN] Da chon cua so: {title}" + (f" ({exe})" if exe else ""))
        # Luu tu khoa on dinh de lan sau tu nhan lai cua so
        # (title FASTMU doi lien tuc vi co level/gio server -> dung phan on dinh)
        m = re.search(r"Char:\s*[^\]]+\]", title)
        if m:
            kw = m.group(0).rstrip("]")
        else:
            kw = title.split("]")[0].lstrip("[") if "]" in title else title[:20]
        kw = kw.strip()
        if kw:
            self.cfg["window_title"] = kw
            v = self.vars.get(("window_title",))
            if v:
                v[0].set(kw)
        st = parse_title_stats(title)
        if st:
            self.log(f"[WIN] Nhan dien: Char={st['char']} Level={st['level']} "
                     f"RR={st['rr']} GR={st['gr']}")

    def test_title(self):
        self._collect()
        self.bot.cfg = self.cfg
        title = get_game_title(self.cfg.get("window_title", ""))
        if not title:
            self.log(f"[TITLE] Khong tim thay cua so chua '{self.cfg.get('window_title')}'. "
                     "Sua o 'Tu khoa title cua so game' (tab Bai/Toa do).")
            return
        self.log(f"[TITLE] {title}")
        st = parse_title_stats(title)
        if st:
            self.log(f"[TITLE] Char={st['char']} Level={st['level']}"
                     + (f"+{st['master']}" if st.get("master") else "")
                     + f" RR={st['rr']} GR={st['gr']}")
        else:
            self.log("[TITLE] Khong phan tich duoc Level/RR/GR tu title (se dung OCR).")

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
        self.lbl_status.config(text=f"Trang thai: {self.bot.status}",
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
