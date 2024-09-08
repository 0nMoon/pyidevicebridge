import subprocess
import time
import progressbar

def display_stage(stage_name):
    print(f"\n[Stage] {stage_name}")

def display_progress(message, total_steps):
    bar = progressbar.ProgressBar(maxval=total_steps, widgets=[
        progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(total_steps):
        time.sleep(0.1)  # Simulate work being done
        bar.update(i + 1)
    bar.finish()
    print(f"{message}... Done!\n")

def find_connected_devices():
    display_stage("Stage 1: Finding all connected USB devices...")
    display_progress("Detecting iOS devices", 10)

    try:
        result = subprocess.run(['idevice_id', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        devices = result.stdout.decode().splitlines()

        if devices:
            print("Connected iOS devices found:")
            for device in devices:
                display_progress(f"Checking device {device}", 5)
                device_info = subprocess.run(['ideviceinfo', '-u', device], stdout=subprocess.PIPE)
                device_info_output = device_info.stdout.decode().lower()

                if "iphone" in device_info_output or "ipad" in device_info_output:
                    print(f"Device: {device} (iPhone or iPad)")
                    get_device_info(device)
                else:
                    print(f"Device: {device} (Not an iPhone or iPad)")
        else:
            print("No iOS devices connected.")
    except FileNotFoundError:
        print("libimobiledevice not installed or idevice_id command not found.")
    
    display_stage("Stage 1 Completed.")

def get_device_info(udid):
    display_stage("Stage 2: Fetching Device Information...")
    display_progress(f"Gathering information for device {udid}", 10)
    
    try:
        device_info = subprocess.run(['ideviceinfo', '-u', udid], stdout=subprocess.PIPE)
        device_info_output = device_info.stdout.decode().splitlines()

        serial_number = None
        device_name = None

        for line in device_info_output:
            if "SerialNumber" in line:
                serial_number = line.split(":")[1].strip()
            if "DeviceName" in line:
                device_name = line.split(":")[1].strip()

        print(f"\nDevice Information for {device_name}:")
        print(f"UDID: {udid}")
        print(f"Serial Number: {serial_number}")

        
        list_running_processes(udid)

    except subprocess.CalledProcessError as e:
        print(f"Error fetching information for device {udid}: {e}")

    display_stage("Stage 2 Completed.")

def list_running_processes(udid):
    display_stage("Stage 3: Listing Running Processes...")
    display_progress("Fetching running processes on the device", 15)
    
    try:
        
        process_list = subprocess.run(['idevicedebug', '-u', udid, 'list'], stdout=subprocess.PIPE)
        process_output = process_list.stdout.decode().splitlines()

        if process_output:
            print("\nRunning processes on the device (PID - Process Name):")
            for process in process_output:
                print(process)

            
            process_id = input("\nEnter the Process ID to hook into (e.g., 12345): ")

            
            attach_to_process(udid, process_id)
        else:
            print("No processes found or device might not have any active processes.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error listing processes: {e}")
    
    display_stage("Stage 3 Completed.")

def attach_to_process(udid, process_id):
    try:
        print(f"\nAttaching to process {process_id}...")
        attach_command = subprocess.run(['idevicedebug', '-u', udid, 'attach', process_id], stdout=subprocess.PIPE)
        attach_output = attach_command.stdout.decode()
        
        print(f"Attached to process {process_id}. Debugger output:\n")
        print(attach_output)
    except subprocess.CalledProcessError as e:
        print(f"Error attaching to process {process_id}: {e}")

find_connected_devices()
