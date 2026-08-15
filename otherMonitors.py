import psutil
import GPUtil
import customtkinter as ctk
from tkdial import Meter
import time
#this file contains the functionality for all the buttons aka all the monitors the buttons open

#globals
old_diskr = 0
old_diskw = 0

snooze_States = {
    "all": False,
    "updates": False
}

gpu_open = False
ram_open = False
disk_open = False
event_open = False

events = {}
labels = []

#Helper functions
def hover(l, t):
    l.configure(text=t)

def Label(text: str, monitor, color: str):
    return ctk.CTkLabel(
        monitor,
        text=text,
        font=("monogram", 24),
        fg_color=color,
        text_color="white"
    )

def createEvent(event, color, bg, parent, w, h, pad):
    #the frame is here for later ease of updating, since later if i wanted can add more widgets
    eventFrame = ctk.CTkFrame(parent, width=w, height=h, bg_color=bg,  fg_color=bg, corner_radius=0)
    eventFrame.pack(padx=0, pady=pad, anchor="w")
    eventFrame.pack_propagate(False)

    detailss = ctk.CTkButton(
        eventFrame, 
        text=event, 
        font=("monogram", 24), 
        fg_color=color,
        bg_color=color,
        corner_radius=0,
        text_color="white",
        border_width=2,
        width=w,
        hover_color="red",
        command=lambda: (events.pop(event), labels.pop(labels.index(detailss)), eventFrame.destroy())
    )

    detailss.pack(padx=0, pady=0, side="left")

    if "update" in event.lower():
        detailss.configure(fg_color = "brown")

    return detailss

def toggle_Variable(obj, originalColor, name):
    global snooze_States

    var = getattr(obj, "snoozed")

    snooze_States[name] = not snooze_States[name]

    setattr(obj, "snoozed", not var)

    if var == True: obj.configure(fg_color = originalColor)
    else: obj.configure(fg_color = "red")

def ClearEvents():
    global events, labels
    events = {}

    for v in labels:
        v.master.destroy()

    labels = []

#Monitor functions
def createGpuMonitor(root, color: str, create, set):
    global gpu_open

    if gpu_open == True:
        return
    else:
        gpu_open = True

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"370x170+{x}+{y}")
    Monitor.title("Gpu monitor")
    Monitor.attributes("-topmost", True)

    def close():
        global gpu_open

        gpu_open = False
        Monitor.destroy()

    Monitor.protocol("WM_DELETE_WINDOW", lambda: close())

    gpu_uframe, gpu_umeter = create("green", " %", 0, 100, "GPU Usage", Monitor, 120, 10)
    gpu_uframe.grid(column=0, row=0)

    gpu_hframe, gpu_hmeter = create("green", " C", 0, 100, "GPU Temp", Monitor, 120, 10)
    gpu_hframe.grid(column=1, row=0)

    gpu_vframe, gpu_vmeter = create("green", " %", 0, 100, "GPU VRAM Used", Monitor, 120, 10)
    gpu_vframe.grid(column=2, row=0)

    def update():
        gpu = GPUtil.getGPUs()[0]

        usage = gpu.load * 100
        heat = gpu.temperature
        utilization = gpu.memoryUtil*100

        set(gpu_umeter, usage, Monitor)
        set(gpu_hmeter, heat, Monitor)
        set(gpu_vmeter, utilization, Monitor)

        Monitor.after(1000, update)

    update()

def createDiskMonitor(root, color: str):
    global disks
    global disk_open

    if disk_open == True:
        return
    else:
        disk_open = True

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"400x300+{x}+{y}")
    Monitor.title("Disk monitor")
    Monitor.attributes("-topmost", True)

    def close():
        global disk_open

        disk_open = False
        Monitor.destroy()

    Monitor.protocol("WM_DELETE_WINDOW", lambda: close())

    PSFrame = ctk.CTkScrollableFrame(Monitor, width=350, height=300, fg_color=color, bg_color=color, scrollbar_button_color="white", scrollbar_button_hover_color="grey") 
    #PartitionScrollableFrame is what PSFrame stands for.
    #I DONT UNDERSTAND WHY I SET THE GEOMETRY TO 300X300 AND IF I SET THE PSFRAME TO 300X300 IT DOESNT FIT 
    PSFrame.pack(padx=0, pady=0, anchor="center")

    for partition in psutil.disk_partitions():
        try:
            device = partition.device[:2]
            p = psutil.disk_usage(partition.device)
            ptotal = round(p.total / (1024**3), 1)
            pused = round(p.used / (1024**3), 1)
            ppercent = p.percent

            text = Label(f"{device}: {pused} GB/{ptotal} GB ({ppercent}% used)", PSFrame, color)
            text.pack(padx=0, pady=5, anchor="center")

            if ppercent > 85:
                text.configure(text_color="red")
            elif ppercent > 70:
                text.configure(text_color="orange")
        except PermissionError:
            pass

    gap = Label("Total IO Counters all drives", PSFrame, color)
    gap.pack(padx=0, pady=15)

    writeSpeedL = Label("Loading..", PSFrame, color)
    writeSpeedL.pack(padx=0, pady=5)

    readSpeedL = Label("Loading..", PSFrame, color)
    readSpeedL.pack(padx=0, pady=5)

    def update():
        global old_diskr
        global old_diskw

        io = psutil.disk_io_counters()

        read = io.read_bytes
        write = io.write_bytes

        new_diskr = round((read - old_diskr), 1)
        new_diskw = round((write - old_diskw), 1)

        #if the read speed is more than 1 mb, display it in MB/s, else KB/s    
        if new_diskr / (1024 ** 2) > 1:
            new_diskr /= (1024 ** 2)
            readSpeedL.configure(text=f"{round(new_diskr, 1)} MB/s READ")
        else:
            new_diskr /= 1024
            readSpeedL.configure(text=f"{round(new_diskr, 1)} KB/s READ")

        #if the write speed is more than 1 mb, display it in MB/s, else KB/s    
        if new_diskw / (1024 ** 2) > 1:
            new_diskw /= (1024 ** 2)
            writeSpeedL.configure(text=f"{round(new_diskw, 1)} MB/s WRITE")
        else:
            new_diskw /= 1024
            writeSpeedL.configure(text=f"{round(new_diskw, 1)} KB/s WRITE")

        old_diskw = write
        old_diskr = read

        Monitor.after(1000, update)

    update()

def createRamMonitor(root, color: str, create, set):
    global ram_open

    if ram_open == True:
        return
    else:
        ram_open = True

    ramtotal = round(psutil.virtual_memory().total / (1024**3), 1)

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"240x160+{x}+{y}")
    Monitor.title(f"RAM monitor ({ramtotal} GB)")
    Monitor.attributes("-topmost", True)

    def close():
        global ram_open

        ram_open = False
        Monitor.destroy()

    Monitor.protocol("WM_DELETE_WINDOW", lambda: close())
    
    ram_UFrame, ramU_Meter = create("pink", " %", 0, 100, "RAM Used", Monitor, 120, 12)
    ram_UFrame.grid(row=0, column=0)

    ram_Frame, ram_Meter = create("cyan", " GB", 0, ramtotal, f"RAM Used/{ramtotal}GB", Monitor, 120, 12)
    ram_Frame.grid(row=0, column=1)

    def update():
        ram = psutil.virtual_memory()
        used = round(ram.used / (1024**3), 1)
        percent = round(ram.percent, 1)

        set(ramU_Meter, percent, Monitor)
        set(ram_Meter, used, Monitor)

        Monitor.after(1000, update)

    update()

#this is the main feature, event tracker. Displays all recent events(events such as cpu, ram, net, disk spike)
def createEventTracker(root, color: str):
    global labels
    global event_open

    if event_open:
        return
    else:
        event_open = True

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"500x300+{x}+{y}")
    Monitor.title("Event tracker")
    Monitor.attributes("-topmost", True)

    controlFrame = ctk.CTkFrame(Monitor, corner_radius=0, fg_color=color, bg_color=color, width=485, height=50)
    controlFrame.pack(padx=0, pady=0, anchor="center")
    controlFrame.pack_propagate(False)

    snoozeUpdates = ctk.CTkButton(
        controlFrame, 
        text="Snooze Updates",
        font=("monogram", 16), 
        fg_color="Purple", 
        bg_color=color,
        hover_color="red",
        command=lambda: toggle_Variable(snoozeUpdates, "Purple", "updates")
    )

    setattr(snoozeUpdates, "snoozed", snooze_States["updates"])

    if snooze_States["updates"] == True:
        snoozeUpdates.configure(fg_color="red")

    snoozeUpdates.pack(padx=5, pady=0, side="left")

    snoozeAll = ctk.CTkButton(
        controlFrame, 
        text="Snooze All", 
        font=("monogram", 16),
        fg_color="Olive", 
        bg_color="Black",
        hover_color="red",
        command=lambda: toggle_Variable(snoozeAll, "Olive", "all")
    )

    setattr(snoozeAll, "snoozed", snooze_States["all"])

    if snooze_States["all"] == True:
        snoozeAll.configure(fg_color="red")

    snoozeAll.pack(padx=0, pady=0, side="left")

    timeLabel = Label(time.strftime("%H:%M:%S"), controlFrame, color)
    timeLabel.pack(padx=5, pady=0, side="left")

    delButton = ctk.CTkButton(
        controlFrame, 
        font=("monogram", 16), 
        text="C", 
        fg_color="red", 
        bg_color=color,
        command=ClearEvents
    )

    delButton.pack(padx=5, pady=0, side="left")

    eventFrame = ctk.CTkScrollableFrame(Monitor, corner_radius=0, fg_color=color, width=485, height=250)
    eventFrame.pack(padx=0, pady=0, anchor="center")

    def close():
        global labels
        global event_open

        event_open = False
        labels = []
        Monitor.destroy()

    Monitor.protocol("WM_DELETE_WINDOW", lambda: close())

    def update():
        timeLabel.configure(text=time.strftime("%H:%M:%S"))

        if len(events) != len(labels):
            for i in range(len(labels), len(events)):

                thing = list(events.keys())[i]

                a = createEvent(thing, "orange", color, eventFrame, 500, 30, 2)

                def bindHover(widget, text, time):
                    widget.bind("<Enter>", lambda event: hover(widget, time))
                    widget.bind("<Leave>", lambda event: hover(widget, text))

                bindHover(a, thing, events[thing]["Time"])
                labels.append(a)

        Monitor.after(1000, update)

    update()







