import psutil#cpu, ram, net
import GPUtil#nvidia gpu - does NOT work with amd or intel.
from tkdial import Meter
import customtkinter as ctk#gui library, didn't use tkinter because ctk has more features and looks better
import otherMonitors#module script, provides functionality for the buttons
import time

#This is the main file, this is also where the dashboard is and the functions
#create(color, text, start, end, title, parent, radius, font) for creating meters
#add_Button(color, text, cmd) for creating buttons
#set_Meter(me, targ, rot) for smoothly setting the meter(dont ask why it's rot and not root)
#update_Info() updates the dashboard meters

#Colors 
background: str = "#0D1117"
bsecondary: str = "#2C323B"
blue: str = "#13B8FF"
emerald: str = "#10B981"

#for network, no touch plz
old_Network = psutil.net_io_counters()

threshold = 20

ram_Opened = False
disk_Opened = False
gpu_Opened = False
event_Opened = False

#for buttons, no touch plz
buttons: int = 0

old_Cpu = 100
old_Ram = 100
old_Gpu = 100

a = 0
b = 0
index = 0

def addEvent(text):
    try:
        otherMonitors.events[text] = {
            "Time": time.strftime("%H:%M:%S")
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass 

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
        width=240,
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

    me.anim_id = rot.after(35, lambda: set_Meter(me, targ, rot))

def update_Info() -> None:
    global old_Cpu
    global old_Gpu
    global old_Ram
    global old_Network
    global a
    global b
    global index

    updatesSnoozed = otherMonitors.snooze_States["updates"]
    allSnoozed = otherMonitors.snooze_States["all"]
    gpuusage=0

    usage = psutil.cpu_percent(interval=None)

    if GPUtil.getGPUs():
        gpu = GPUtil.getGPUs()[0]
        gpuusage = gpu.load * 100
        set_Meter(gpuUsageMeter, gpuusage, root)

    new_Network = psutil.net_io_counters()

    upload = 0
    download = 0

    if (new_Network.bytes_sent - old_Network.bytes_sent) / 1024 / 1024 > 0.1:
        upload = (new_Network.bytes_sent - old_Network.bytes_sent) / 1024 / 1024
        uploadMeter.text = " MB/s"
    else:
        upload = (new_Network.bytes_sent - old_Network.bytes_sent) / 1024
        uploadMeter.text = " KB/s"

    if (new_Network.bytes_recv - old_Network.bytes_recv) / 1024 / 1024 > 0.1:
        download = (new_Network.bytes_recv - old_Network.bytes_recv) / 1024 / 1024
        downloadMeter.text = " MB/s"
    else:
        download = (new_Network.bytes_recv - old_Network.bytes_recv) / 1024
        downloadMeter.text = " KB/s"

    old_Network = new_Network

    try:
        diskusage = psutil.disk_usage("C:\\").percent
    except FileNotFoundError:
        diskusage = 0

    ramusage = psutil.virtual_memory().percent

    set_Meter(cpuUsageMeter, usage, root)
    set_Meter(uploadMeter, upload, root)
    set_Meter(downloadMeter, download, root)
    set_Meter(ramUsageMeter, ramusage, root)
    set_Meter(diskUsageMeter, diskusage, root)

    #events

    cpu_Diff = usage-old_Cpu
    ram_Diff = ramusage-old_Ram
    gpu_Diff = gpuusage-old_Gpu

    if not allSnoozed:
        a+=1

        if not updatesSnoozed:
            b+=1

            if b == 5:
                index += 1
                addEvent(f"CPU Usage update, {usage}% ({index})")
                addEvent(f"GPU Usage update, {gpuusage}% ({index})")
                addEvent(f"RAM Usage update, {ramusage}% ({index})")
                b = 0
        if a == 5:
            index += 1
            old_Cpu = usage
            old_Ram = ramusage
            old_Gpu = gpuusage
            a = 0

    #processes = []

    if cpu_Diff > threshold:
        addEvent(f"CPU Spike, Spike > {threshold}% ({index})")

    if ram_Diff > threshold:
        addEvent(f"RAM Spike, Spike > {threshold}% ({index})")

    if gpu_Diff > threshold:
        addEvent(f"GPU Spike, Spike > {threshold}% ({index})")

    events = len(otherMonitors.events)

    if events > 9:
        events = "9+"

    eventViewer.configure(text=f"Event tracker({events})")

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

upload, uploadMeter = create("orange", " KB/s", 0, 100, "Net Send", root, 200, 16)
upload.grid(column=3, row=2)

download, downloadMeter = create("orange", " KB/s", 0, 100, "Net Receive", root, 200, 16)
download.grid(column=3, row=3)

ramUsageMeter.set_mark(81, 100, "red")

info = ctk.CTkLabel(
    root,
    text="       Statitron\n\nReal-time PC monitoring\n\n"
         "- CPU & GPU monitoring\n"
         "- RAM & disk monitoring\n"
         "- Network monitoring\n"
         "- Hardware spike tracking",
    font=("monogram", 24),
    text_color="white",
    fg_color=background,
    justify="left"
)

info.grid(column=1, row=3, sticky="nsew")

#Buttons

idDisk=add_Button(bsecondary, "More Info Disk", lambda: otherMonitors.createDiskMonitor(root, background))
idGpu=add_Button(bsecondary, "More Info Gpu", lambda: otherMonitors.createGpuMonitor(root, background, create, set_Meter))
idRam=add_Button(bsecondary, "More Info Ram", lambda: otherMonitors.createRamMonitor(root, background, create, set_Meter))
eventViewer=add_Button(bsecondary, "Event Tracker", lambda: otherMonitors.createEventTracker(root, background))

#starts updating info
update_Info()

root.rowconfigure(4, weight=1)

root.mainloop()