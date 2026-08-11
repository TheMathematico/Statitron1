import psutil#cpu, ram, net
import GPUtil#nvidia gpu - does NOT work with amd or intel.
from tkdial import Meter
import customtkinter as ctk#gui library, didn't use tkinter because ctk has more features and looks better
import otherMonitors#module script, provides functionality for the buttons
import wmi

#This is the main file, this is also where the dashboard is and the functions
#create(color, text, start, end, title, parent, radius, font) for creating meters
#add_Button(color, text, cmd) for creating buttons
#set_Meter(me, targ, rot) for smoothly setting the meter(dont ask why it's rot and not root)
#update_Info() updates the dashboard meters

#Colors 
background: str = "#0D1117"
bsecondary: str = "#2C323B"
blue: str = "#13B8FF"
secondaryTextColor: str = "#1E3CE5"
emerald: str = "#10B981"

#Status colors, used for the meters.
bad: str = "#C40F0F"
okay: str = "#C77A07"
great: str = "#157C16"

#for network, no touch plz
old_Network = psutil.net_io_counters()

#for buttons, no touch plz
buttons: int = 0

def create(color: str, text: str, start: int, end: int, title: str, parent, radius: int, font: tuple):
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
        text_font=("monogram", font),
        radius=radius
    )

    meter.grid(row=1, column=0)

    return frame, meter

def add_Button(color: str, text: str, cmd):
    global buttons
    buttons += 1

    btn = ctk.CTkButton(
        buttonsFrame, 
        text=text, 
        font=("monogram", 32),
        bg_color=background,
        fg_color=color,
        corner_radius=10,
        text_color="white",
        width=200,
        height=50   
    )

    if cmd != 0:
        btn.configure(command=cmd)

    btn.grid(column=1, row=buttons, pady=8)
    return btn

def set_Meter(me, targ: int, rot) -> None:
    current = me.get()

    if hasattr(me, "anim_id"):
        rot.after_cancel(me.anim_id)

    if abs(current-targ) <= 0.05:
        return

    current += (targ-current) * 0.05
    me.set(current)

    me.anim_id = rot.after(50, lambda: set_Meter(me, targ, rot))

def update_Info() -> None:
    global old_Network #for measuring network speeds,
    #see it's usage  lines 108-123

    usage = psutil.cpu_percent(interval=None)

    if len(GPUtil.getGPUs()) > 0:
        gpu = GPUtil.getGPUs()[0]
        gpuusage = gpu.load * 100

    new_Network = psutil.net_io_counters()

    upload = 0
    download = 0

    if (new_Network.bytes_sent - old_Network.bytes_sent) / 1024 / 1024 > 0.1:
        upload = (new_Network.bytes_sent - old_Network.bytes_sent) / 1024 / 1024
        uploadMeter.text = " mbps"
    else:
        upload = (new_Network.bytes_sent - old_Network.bytes_sent) / 1024
        uploadMeter.text = " kbps"

    if (new_Network.bytes_recv - old_Network.bytes_recv) / 1024 / 1024 > 0.1:
        download = (new_Network.bytes_recv - old_Network.bytes_recv) / 1024 / 1024
        downloadMeter.text = " mbps"
    else:
        download = (new_Network.bytes_recv - old_Network.bytes_recv) / 1024
        downloadMeter.text = " kbps"

    old_Network = new_Network

    diskusage = psutil.disk_usage("C:\\")

    ramusage = psutil.virtual_memory().percent

    set_Meter(cpuUsageMeter, usage, root)

    if len(GPUtil.getGPUs()) > 0:
        set_Meter(gpuUsageMeter, gpuusage, root)

    set_Meter(uploadMeter, upload, root)
    set_Meter(downloadMeter, download, root)
    set_Meter(ramUsageMeter, ramusage, root)
    set_Meter(diskUsageMeter, diskusage.percent, root)

    root.after(1000, update_Info)

root = ctk.CTk()
root.title("Monitor")
root.geometry("700x720")
root.config(bg=background)

#Text at the very top of the window(root)
frametitle = ctk.CTkLabel(root, 
    text="Dashboard", 
    font=("monogram", 32),
    fg_color=background, 
    text_color="white"
)
frametitle.grid(column=1, row=0, padx=100)

#Frame for the buttons
buttonsFrame = ctk.CTkFrame(root, width=100, height=100, fg_color=background, bg_color= background)
buttonsFrame.grid(column=1, row=1, columnspan=2, rowspan=2, sticky="nsew", padx=10, pady=10)

buttonsFrame.grid_columnconfigure(0, weight=1)
buttonsFrame.grid_columnconfigure(1, weight=1)
buttonsFrame.grid_columnconfigure(2, weight=1)

#statsFrame = ctk.CTkFrame(root, 100, 100, fg_color=bsecondary, bg_color=background)
#statsFrame.grid(row=3, column=1, rowspan=2, columnspan=2)

#meters
#for set_mark, it's set to 81 instead of 80 because when it's set to 80 the red overlaps to 79 on the meter
cpu, cpuUsageMeter = create(blue, " %", 0, 100, "CPU Usage", root, 200, 16)
cpu.grid(column=0, row=1)

cpuUsageMeter.set_mark(81, 100, "red")

gpu, gpuUsageMeter = create(emerald, " %", 0, 100, "GPU Usage", root, 200, 16)
gpu.grid(column=0, row=2)

gpuUsageMeter.set_mark(81, 100, "red")

disk, diskUsageMeter = create("yellow", " %", 0, 100, "Disk Used", root, 200, 16)
disk.grid(column=0, row=3)

diskUsageMeter.set_mark(81, 100, "red")

ram, ramUsageMeter = create("pink", " %", 0, 100, "Ram Used", root, 200, 16)
ram.grid(column=3, row=1)

upload, uploadMeter = create("orange", " kbps", 0, 100, "Net Send", root, 200, 16)
upload.grid(column=3, row=2)

download, downloadMeter = create("orange", " kbps", 0, 100, "Net Receive", root, 200, 16)
download.grid(column=3, row=3)

ramUsageMeter.set_mark(81, 100, "red")

#Buttons

idDisk=add_Button(bsecondary, "More Info Disk", lambda: otherMonitors.createDiskMonitor(root, background))
idGpu=add_Button(bsecondary, "More Info Gpu", lambda: otherMonitors.createGpuMonitor(root, background, create, set_Meter))
idDisk=add_Button(bsecondary, "More Info Disk", lambda: otherMonitors.createRamMonitor(root, background, create, set_Meter))
eventViewer=add_Button(bsecondary, "Event Tracker", 0)

#starts updating info
update_Info()

otherMonitors.createRamMonitor(root, background, create, set_Meter)

root.mainloop()