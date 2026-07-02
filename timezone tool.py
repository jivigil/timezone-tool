import tkinter as tk
from tkinter import ttk
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess

# Simple timezone map (Windows tz id → display + IANA fallback)
TIMEZONES = {
    "New York": ("America/New_York", "Eastern Standard Time"),
    "Los Angeles": ("America/Los_Angeles", "Pacific Standard Time"),
    "Chicago": ("America/Chicago", "Central Standard Time"),
    "London": ("Europe/London", "GMT Standard Time"),
    "Paris": ("Europe/Paris", "Romance Standard Time"),
    "Tokyo": ("Asia/Tokyo", "Tokyo Standard Time"),
    "Shanghai": ("Asia/Shanghai", "China Standard Time"),
}

root = tk.Tk()
root.title("Time Zone Tool")
root.geometry("320x180")

selected = tk.StringVar(value="New York")

dropdown = ttk.Combobox(
    root,
    textvariable=selected,
    values=list(TIMEZONES.keys()),
    state="readonly"
)
dropdown.pack(pady=10)

label = tk.Label(root, text="", font=("Arial", 14))
label.pack(pady=10)


def update_clock():
    city = selected.get()
    iana = TIMEZONES[city][0]

    now = datetime.now(ZoneInfo(iana))
    label.config(text=now.strftime("%Y-%m-%d\n%H:%M:%S"))

    root.after(1000, update_clock)


def set_timezone():
    city = selected.get()
    windows_tz = TIMEZONES[city][1]

    try:
        subprocess.run(
            ["tzutil", "/s", windows_tz],
            check=True
        )
        label.config(text="Time zone updated!\n(reopen if needed)")
    except Exception as e:
        label.config(text=str(e))


btn = tk.Button(root, text="Set System Time Zone", command=set_timezone)
btn.pack(pady=5)

update_clock()
root.mainloop()
