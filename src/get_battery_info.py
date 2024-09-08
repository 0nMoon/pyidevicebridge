import subprocess

def get_battery_level(udid):
    try:
        
        device_info = subprocess.run(['ideviceinfo', '-u', udid], stdout=subprocess.PIPE)
        device_info_output = device_info.stdout.decode().splitlines()

        
        battery_level = None
        for line in device_info_output:
            if "BatteryCurrentCapacity" in line:
                battery_level = line.split(":")[1].strip()
                break
            elif "BatteryLevel" in line:
                battery_level = line.split(":")[1].strip()
                break
        
        if battery_level:
            return int(battery_level)  # Return battery level as an integer
        else:
            return None  # Return None if battery level wasn't found
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    udid = "your_device_udid_here"  
    battery = get_battery_level(udid)
    if battery is not None:
        print(f"Battery Level: {battery}%")
    else:
        print("Battery information not available.")
