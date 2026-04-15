from __future__ import annotations

import ctypes
import time
from ctypes import wintypes

# Win32定数
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002
VK_RETURN = 0x0D
VK_CONTROL = 0x11
VK_T = 0x54
ULONG_PTR = ctypes.c_size_t


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class _INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD), ("u", _INPUTUNION)]


user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
user32.SendInput.restype = wintypes.UINT
user32.OpenClipboard.argtypes = (wintypes.HWND,)
user32.OpenClipboard.restype = wintypes.BOOL
user32.EmptyClipboard.argtypes = ()
user32.EmptyClipboard.restype = wintypes.BOOL
user32.SetClipboardData.argtypes = (wintypes.UINT, wintypes.HANDLE)
user32.SetClipboardData.restype = wintypes.HANDLE
user32.CloseClipboard.argtypes = ()
user32.CloseClipboard.restype = wintypes.BOOL

kernel32.GlobalAlloc.argtypes = (wintypes.UINT, ctypes.c_size_t)
kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
kernel32.GlobalLock.argtypes = (wintypes.HGLOBAL,)
kernel32.GlobalLock.restype = wintypes.LPVOID
kernel32.GlobalUnlock.argtypes = (wintypes.HGLOBAL,)
kernel32.GlobalUnlock.restype = wintypes.BOOL
kernel32.GlobalFree.argtypes = (wintypes.HGLOBAL,)
kernel32.GlobalFree.restype = wintypes.HGLOBAL


def _send_input(inputs: list[INPUT]) -> None:
    input_array = (INPUT * len(inputs))(*inputs)
    sent = user32.SendInput(len(inputs), input_array, ctypes.sizeof(INPUT))
    if sent != len(inputs):
        raise OSError(f"SendInput失敗: sent={sent}, expected={len(inputs)}, error={ctypes.get_last_error()}")


def _press_vk(vk: int) -> None:
    down = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=vk, wScan=0, dwFlags=0, time=0, dwExtraInfo=0))
    up = INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0),
    )
    _send_input([down, up])


def _press_unicode_char(ch: str) -> None:
    scan = ord(ch)
    down = INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=0, wScan=scan, dwFlags=KEYEVENTF_UNICODE, time=0, dwExtraInfo=0),
    )
    up = INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=0, wScan=scan, dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, time=0, dwExtraInfo=0),
    )
    _send_input([down, up])


def _press_ctrl_v() -> None:
    ctrl_down = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=VK_CONTROL, wScan=0, dwFlags=0, time=0, dwExtraInfo=0))
    v_down = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=ord("V"), wScan=0, dwFlags=0, time=0, dwExtraInfo=0))
    v_up = INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=ord("V"), wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0),
    )
    ctrl_up = INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=VK_CONTROL, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0),
    )
    _send_input([ctrl_down, v_down, v_up, ctrl_up])


def _set_clipboard_text(text: str) -> None:
    if not user32.OpenClipboard(None):
        raise OSError(f"OpenClipboard失敗: error={ctypes.get_last_error()}")

    h_global = None
    try:
        if not user32.EmptyClipboard():
            raise OSError(f"EmptyClipboard失敗: error={ctypes.get_last_error()}")

        encoded = (text + "\x00").encode("utf-16-le")
        h_global = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(encoded))
        if not h_global:
            raise OSError(f"GlobalAlloc失敗: error={ctypes.get_last_error()}")

        ptr = kernel32.GlobalLock(h_global)
        if not ptr:
            raise OSError(f"GlobalLock失敗: error={ctypes.get_last_error()}")

        try:
            ctypes.memmove(ptr, encoded, len(encoded))
        finally:
            kernel32.GlobalUnlock(h_global)

        if not user32.SetClipboardData(CF_UNICODETEXT, h_global):
            raise OSError(f"SetClipboardData失敗: error={ctypes.get_last_error()}")

        # SetClipboardData成功後はOS側がメモリ所有するため解放しない。
        h_global = None
    finally:
        user32.CloseClipboard()
        if h_global:
            kernel32.GlobalFree(h_global)


def send_command_input(command: str) -> None:
    """Minecraft向けに`T`でチャットを開き、貼り付け -> Enterを送信する。"""
    # `/`文字は貼り付け内容に含め、開く操作は物理キー(T)で行う。
    full_command = command if command.startswith("/") else f"/{command}"
    _set_clipboard_text(full_command)
    _press_vk(VK_T)
    time.sleep(0.03)
    _press_ctrl_v()
    time.sleep(0.03)
    _press_vk(VK_RETURN)
