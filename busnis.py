import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes

# בדיקה אם התוכנית רצה בהרשאות מנהל
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def open_port_forever():
    if not is_admin():
        messagebox.showerror("שגיאה", "יש להריץ את התוכנית כמנהל כדי לפתוח פורט אמיתי")
        return

    port_text = entry_custom.get().strip()
    try:
        port = int(port_text)
    except:
        messagebox.showerror("שגיאה", "מספר פורט לא חוקי")
        return

    # מחיקת כלל קודם אם קיים
    subprocess.run(f'netsh advfirewall firewall delete rule name="OpenPort {port}"', shell=True)
    
    cmd = f'netsh advfirewall firewall add rule name="OpenPort {port}" protocol=TCP dir=in localport={port} action=allow'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        messagebox.showinfo("הצלחה", f"פורט {port} פתוח ברמת המערכת עד שתחליט לסגור אותו")
    else:
        messagebox.showerror("שגיאה", f"לא ניתן לפתוח פורט:\n{result.stderr}")

def close_port_forever():
    if not is_admin():
        messagebox.showerror("שגיאה", "יש להריץ את התוכנית כמנהל כדי לסגור פורט אמיתי")
        return

    port_text = entry_custom.get().strip()
    try:
        port = int(port_text)
    except:
        messagebox.showerror("שגיאה", "מספר פורט לא חוקי")
        return

    cmd = f'netsh advfirewall firewall delete rule name="OpenPort {port}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        messagebox.showinfo("הצלחה", f"פורט {port} נסגר מהרשת")
    else:
        messagebox.showerror("שגיאה", f"לא ניתן לסגור פורט:\n{result.stderr}")

# --- GUI ---
root = tk.Tk()
root.title("פתח וסגור פורט אמיתי")
root.geometry("400x150")
root.configure(bg="#e8f0f7")

tk.Label(root, text="פורט:", font=("Arial", 14), bg="#e8f0f7").pack(pady=5)
entry_custom = tk.Entry(root, font=("Arial", 14), width=10, justify="center")
entry_custom.pack()
entry_custom.insert(0, "8080")

frame_buttons = tk.Frame(root, bg="#e8f0f7")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="פתח פורט למערכת", command=open_port_forever,
          bg="#4CAF50", fg="white", font=("Arial", 12), width=15).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="סגור פורט במערכת", command=close_port_forever,
          bg="#FF9800", fg="white", font=("Arial", 12), width=15).grid(row=0, column=1, padx=5)

root.mainloop()
