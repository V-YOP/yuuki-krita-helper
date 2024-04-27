import ctypes

# Define constants and types required for the Win32 API calls
HWND_BROADCAST = 0xFFFF
WM_USER = 0x400
WM_SYSCOMMAND = 0x112
WM_COMMAND = 0x111
WM_CLOSE = 0x10

# Win32 API functions
SendMessage = ctypes.windll.user32.SendMessageW
FindWindow = ctypes.windll.user32.FindWindowW
Shell_NotifyIcon = ctypes.windll.shell32.Shell_NotifyIconW

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_ulong),
        ('hWnd', ctypes.c_void_p),
        ('uID', ctypes.c_uint),
        ('uFlags', ctypes.c_uint),
        ('uCallbackMessage', ctypes.c_uint),
        ('hIcon', ctypes.c_void_p),
        ('szTip', ctypes.c_wchar * 128),
        ('dwState', ctypes.c_ulong),
        ('dwStateMask', ctypes.c_ulong),
        ('szInfo', ctypes.c_wchar * 256),
        ('uTimeout', ctypes.c_uint),
        ('szInfoTitle', ctypes.c_wchar * 64),
        ('dwInfoFlags', ctypes.c_ulong),
    ]

def show_notification(title, message, icon=None):
    nid = NOTIFYICONDATA()
    nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
    nid.hWnd = FindWindow(None, "Python Notification")  # Use your window title here
    nid.uID = 1
    nid.uFlags = 0x00000010 | 0x00000001  # NIF_MESSAGE | NIF_ICON
    nid.uCallbackMessage = WM_USER + 20  # User-defined message for notifications
    # nid.hIcon = ctypes.windll.shell32.ShellExecuteW(0, "open", "notepad.exe", None, None, 1)
    nid.szTip = title[:128]
    nid.szInfo = message[:256]
    nid.szInfoTitle = title[:64]
    nid.dwInfoFlags = 0x00000001  # NIIF_INFO

    Shell_NotifyIcon(0x00000000, ctypes.byref(nid))  # NIM_ADD

# Usage example
if __name__ == "__main__":
    show_notification("Python Notifica11tion", "Hello from Python using Win32 API!")
