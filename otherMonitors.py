import psutil
import GPUtil
import customtkinter as ctk
from tkdial import Meter

#In this file are the functions for button functionality(more info gpu, more info disk, event tracker,
#settings)
#createGpuMonitor(root, color, create(function for creating the meter), set(function for setting it))
#createDiskMonitor(root, color), also uses the function in this script called Label(text, color)
#for text
#createEventTracker()
#createSettings()

#these variables live here because i couldnt figure out why they werent being accessed in the function
#no matter what i did :/
old_diskr = 0
old_diskw = 0

#displays gpu temp, utilization and used vram.
def createGpuMonitor(root, color: str, create, set):
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"370x170+{x}+{y}")
    Monitor.title("Gpu monitor")
    Monitor.attributes("-topmost", True)

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

def Label(text: str, monitor, color: str):
    return ctk.CTkLabel(
        monitor,
        text=text,
        font=("monogram", 24),
        fg_color=color,
        text_color="white"
    )

def createEvent(event, detail, time, color, parent, w, h, pad):
    #the frame is here for later ease of updating, since later if i wanted can add more widgets
    eventFrame = ctk.CTkFrame(parent, width=w, height=h, fg_color=color, corner_radius=0)
    eventFrame.pack(padx=0, pady=pad, anchor="w")
    eventFrame.pack_propagate(False)

    detailss = ctk.CTkButton(
        eventFrame, 
        text=event, 
        font=("monogram", 24), 
        fg_color=color, 
        text_color="white",
        border_width=2,
        border_color="black",
        width=w,
        hover_color="red",
        command=lambda: eventFrame.destroy()
    )

    detailss.pack(padx=0, pady=0, side="left")

    return detailss

#(the disk monitor displays info using text(labels) instead of meters)
def createDiskMonitor(root, color: str):
    global disks

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"400x300+{x}+{y}")
    Monitor.title("Disk monitor")
    Monitor.attributes("-topmost", True)

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

#displays gpu temp, utilization and used vram.
def createRamMonitor(root, color: str, create, set):
    ramtotal = int(psutil.virtual_memory().total / (1024**3)) + 1#it always gave the memory -1, hence +1

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"240x160+{x}+{y}")
    Monitor.title(f"RAM monitor ({ramtotal} GB)")
    Monitor.attributes("-topmost", True)
    
    ram_UFrame, ramU_Meter = create("pink", " %", 0, 100, "RAM Used", Monitor, 120, 12)
    ram_UFrame.grid(row=0, column=0)

    ram_Frame, ram_Meter = create("cyan", " Gb", 0, ramtotal, f"RAM Used/{ramtotal}GB", Monitor, 120, 12)
    ram_Frame.grid(row=0, column=1)

    def update():
        ram = psutil.virtual_memory()
        used = round(ram.used / (1024**3), 1)
        percent = round(ram.percent, 1)

        set(ramU_Meter, percent, Monitor)
        set(ram_Meter, used, Monitor)

        Monitor.after(1000, update)

    update()

events = {
    "CPU Spike >80%": {
        "Detail": "Chrome.exe 5->21%",
        "Time": "18:06"
    },

    "GPU Spike >80%": {
        "Detail": "Discord.exe 14->18%",
        "Time": "12:09"
    },

    "RAM Spike >80%": {
        "Detail": "Roblox.exe 5->91%",
        "Time": "00:06"
    }    
}

def hover(l, t):
    l.configure(text=t)

#this is the main feature, event tracker. Displays all recent events(events such as cpu, ram, net, disk spike)
def createEventTracker(root, color: str, color2: str, create, set):

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()

    labels = []

    Monitor = ctk.CTkToplevel(root, fg_color=color)
    Monitor.geometry(f"500x300+{x}+{y}")
    Monitor.title("Gpu monitor")
    Monitor.attributes("-topmost", True)

    eventFrame = ctk.CTkScrollableFrame(Monitor, corner_radius=0, fg_color=color, width=485, height=300)
    eventFrame.pack(padx=0, pady=0, anchor="center")

    def update():

        if len(events) != len(labels):
            for i in range(len(labels), len(events)):

                thing = list(events.keys())[i]

                a = createEvent(thing, events[thing]["Detail"], events[thing]["Time"], color, eventFrame, 500, 20, 5)

                def bindHover(widget, text, detail, time):
                    widget.bind("<Enter>", lambda event: hover(widget, f"{detail} : {time}"))
                    widget.bind("<Leave>", lambda event: hover(widget, text))

                bindHover(a, thing, events[thing]["Detail"], events[thing]["Time"])
                labels.append(a)

        Monitor.after(1000, update)

    update()







