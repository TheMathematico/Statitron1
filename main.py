import psutil
import GPUtil
import customtkinter as ctk

#Colors 
background = "#0D1117"
bsecondary = "#2C323B"
textcolor = "#13B8FF"
secondarytextcolor = "#1E3CE5"

bad = "#C40F0F"
okay = "#C77A07"
great = "#157C16"

def create_section(name):
    frames = ctk.CTkFrame(frame, width=500, height=170, fg_color=background)
    frames.pack(padx=0, pady=10)

    title = ctk.CTkLabel(frames, text=name, font=("monogram", 40), text_color=secondarytextcolor, fg_color=background)
    title.pack(padx=0, pady=10)

    text = ctk.CTkLabel(frames, text="Please wait...", font=("monogram", 28), text_color=textcolor, fg_color=background)
    text.pack(padx=0, pady=0)

    return frames, text, title

def update_all():
    cpu_perc = psutil.cpu_percent(interval=0.5)
    cpusage.configure(text=f"CPU%: {cpu_perc}")

    ram = psutil.virtual_memory()
    ramusage.configure(text=f"Available: {round(ram.available / (1024**3), 1)} GB    Total: {round(ram.total / (1024**3), 1)} GB")#so long :(

    gpus = GPUtil.getGPUs()

    for gpu in gpus:
        gpusage.configure(text=f"GPU%: {round(gpu.load * 100, 1)}   VRAM used: {round(gpu.memoryUtil*100, 1)}%   Temp: {gpu.temperature} C")

        if gpu.load*100 < 30:
            gput.configure(text="GPU: Idle", text_color = great)
        elif gpu.load*100 < 80:
            gput.configure(text="GPU: Under load", text_color = okay)
        elif gpu.load*100 < 100:
            gput.configure(text="GPU: Under heavy load", text_color = bad)

    if cpu_perc > 40 and cpu_perc < 80:
        cput.configure(text="CPU: Under load", text_color = okay)
    elif cpu_perc > 80:
        cput.configure(text="CPU: Under heavy load", text_color = bad)
    else:
        cput.configure(text="CPU: Idle", text_color = great)

    root.after(1000, update_all)

root = ctk.CTk()
root.title("Usage")
root.geometry("500x500")

frame = ctk.CTkScrollableFrame(root, width=500, height=500, fg_color=background, corner_radius=0) 
frame.pack(pady=0, padx=0)

frametitle = ctk.CTkLabel(frame, text="PC monitor", font=("monogram", 40), text_color=textcolor) 
frametitle.pack(pady=10, padx=0)

cpu, cpusage, cput = create_section("CPU")
ram, ramusage, ramt = create_section("RAM")
gpu, gpusage, gput = create_section("GPU")

update_all()

root.mainloop()