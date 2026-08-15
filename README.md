# Statitron

Statitron is a computer monitoring tool that monitors hardware usage using Python.

It monitors:

- CPU usage
- GPU usage
- RAM usage
- Disk usage
- Disk read and write
- Network receive and send
- Hardware spikes

The GPU monitoring only works with NVIDIA GPUs.

## Python Libraries
This program uses a custom font called monogram.
You can install it by double clicking the included file called "monogram.ttf".
Installing the font isn't necessary, but it looks prettier.

- **GPUtil** - for monitoring the GPU
- **psutil** - for monitoring network, disk, RAM, and CPU
- **CustomTkinter** - for the GUI
- **Meter from tkdial** - for displaying stats on a meter
- **time** - for timestamps

## Dashboard

The main window is a dashboard with 6 meters and buttons to open additional menus.

The dashboard shows:

- CPU usage
- GPU usage
- RAM usage in percent
- Network receive and send

## Additional Menus

There are 4 buttons that open additional windows:

- More Info Disk
- More Info RAM
- More Info GPU
- Event Tracker

### More Info Disk

Shows how much each partition on your computer is being used in GB and percent.

It also tracks how much all disks are writing and reading in total.

### More Info RAM

Shows RAM usage in percent and GB.

### More Info GPU

Shows GPU usage in percent, GPU temperature, and VRAM usage in percent.

### Event Tracker

The Event Tracker shows updates on GPU, CPU, and RAM usage every 10 seconds.

It also detects when the GPU, CPU, or RAM has a spike of over 20%.

You are able to:

- Snooze the 10-second updates
- Snooze all events, including both updates and spikes
- Clear all events, including updates and spikes

## Notes
Net and disk display read/write speed like KB/s, MB/s. However, they are actually KiB/s and MiB/s.
It's written KB/s and MB/s for simplicity.

Also, the GPU usage on the GPU monitor and GPU usage meter(on the dashboard) will show different values, not because one of them is measuring inaccurately but
because they aren't synchronized which means they measure at different times.
I didn't consider that a problem so I didn't fix it.

This program only works on windows.
