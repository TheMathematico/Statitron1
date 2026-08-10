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

old_Network = psutil.net_io_counters()

def create(color, text, start, end, title, parent):
    frame = ctk.CTkFrame(parent, width=30, height=30, fg_color=background, corner_radius=0)

    titl = ctk.CTkLabel(frame, text=title, font=("monogram", 24), text_color="white", bg_color=background)
    titl.grid(column=0, row=0)

    meter = Meter(
        master=frame,
        start=start, 
        end=end, 
        needle_color="white",
        state="disabled",
        border_color=background,
        fg=background,
        text_color=color,
        scale_color=color,
        border_width=0,
        text=text,
        text_font=("monogram", 16),
        radius=200
    )
    meter.grid(row=1, column=0)

    return frame, meter

def set_Meter(me, targ):
    current = me.get()

    if hasattr(me, "anim_id"):
        root.after_cancel(me.anim_id)

    if abs(current-targ) <= 0.05:
        return

    current += (targ-current) * 0.05
    me.set(current)

    me.anim_id = root.after(2, lambda: set_Meter(me, targ))

def update_Info():
    global old_Network

    usage = psutil.cpu_percent(interval=None)
    gpu = GPUtil.getGPUs()[0]
    gpuusage = gpu.load * 100

    new_Network = psutil.net_io_counters()

    upload = 0
    download = 0

    if (new_Network.bytes_sent - old_Network.bytes_sent) / 1024 > 1:
        upload = (new_Network.bytes_sent - old_Network.bytes_sent) / 1024 / 1024
    else:
        upload = (new_Network.bytes_sent - old_Network.bytes_sent) / 1024

    if (new_Network.bytes_recv - old_Network.bytes_recv) / 1024 > 1:
        download = (new_Network.bytes_recv - old_Network.bytes_recv) / 1024 / 1024
    else:
        download = (new_Network.bytes_recv - old_Network.bytes_recv) / 1024

    old_Network = new_Network

    diskusage = psutil.disk_usage("C:\\")

    ramusage = psutil.virtual_memory().percent

    print(usage)

    set_Meter(cpuUsageMeter, usage)
    set_Meter(gpuUsageMeter, gpuusage)
    set_Meter(uploadMeter, upload)
    set_Meter(downloadMeter, download)
    set_Meter(ramUsageMeter, ramusage)
    set_Meter(diskUsageMeter, diskusage.percent)

    root.after(1000, update_Info)

root = ctk.CTk()
root.title("Monitor")
root.geometry("700x800")
root.config(bg=background)

frametitle = ctk.CTkLabel(root, 
    text="Monitor", 
    font=("monogram", 32),
    fg_color=background, 
    text_color="white"
)

frametitle.grid(column=1, row=0, padx=100)

cpu, cpuUsageMeter = create(blue, " %", 0, 100, "CPU Usage", root)
cpu.grid(column=0, row=1)

cpuUsageMeter.set_mark(80, 100, "red")

gpu, gpuUsageMeter = create(emerald, " %", 0, 100, "GPU Usage", root)
gpu.grid(column=0, row=2)

gpuUsageMeter.set_mark(80, 100, "red")

disk, diskUsageMeter = create("yellow", " %", 0, 100, "Disk Used", root)
disk.grid(column=0, row=3)

diskUsageMeter.set_mark(80, 100, "red")

ram, ramUsageMeter = create("pink", " %", 0, 100, "Ram Space", root)
ram.grid(column=3, row=1)

upload, uploadMeter = create("orange", " kbps", 0, 100, "Net Send", root)
upload.grid(column=3, row=2)

download, downloadMeter = create("orange", " kbps", 0, 100, "Net Receive", root)
download.grid(column=3, row=3)

ramUsageMeter.set_mark(80, 100, "red")

update_Info()

root.mainloop()