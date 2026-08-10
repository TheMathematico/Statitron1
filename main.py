import psutil
import GPUtil
from tkdial import Meter
import customtkinter as ctk

#Colors 
background = "#0D1117"
bsecondary = "#2C323B"
blue = "#13B8FF"
secondarytextcolor = "#1E3CE5"
emerald = "#10B981"

bad = "#C40F0F"
okay = "#C77A07"
great = "#157C16"

done = True

def set_Meter(me, targ):
    current = me.get()

    if abs(current-targ) <= 0.05:
        print("done!")
        return

    current += (targ-current) * 0.05
    me.set(current)

    root.after(2, lambda: set_Meter(me, targ))

def update_Info():
    usage = psutil.cpu_percent(interval=None)
    gpu = GPUtil.getGPUs()[0]
    gpuusage = gpu.load * 100
    print(usage)

    set_Meter(cpuUsageMeter, usage)
    set_Meter(gpuUsageMeter, gpuusage)

    root.after(2000, update_Info)

root = ctk.CTk()
root.title("Monitor")
root.geometry("500x500")
root.config(bg=background)

frametitle = ctk.CTkLabel(root, 
    text="Monitor", 
    font=("monogram", 32),
    fg_color=background, 
    text_color="white"
)

frametitle.pack(pady=10, padx=0)

cpuUsageMeter = Meter(root, 
    start=0, 
    end=100, 
    needle_color="white",
    state="disabled",
    border_color=background,
    fg=background,
    text_color=blue,
    scale_color=blue,
    text=" % C",
    text_font=("monogram", 16),
    radius=200
)

cpuUsageMeter.pack(anchor="nw", padx=0, pady=0)

gpuUsageMeter = Meter(root, 
    start=0, 
    end=100, 
    needle_color="white",
    state="disabled",
    border_color=background,
    fg=background,
    text_color=emerald,
    scale_color=emerald,
    text=" % G",
    text_font=("monogram", 16),
    radius=200
)

gpuUsageMeter.pack(anchor="nw", padx=0, pady=0)

update_Info()

root.mainloop()