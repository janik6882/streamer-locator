# pip3 install maxminddb-geolite2

from geolite2 import geolite2
import socket, subprocess
import json
import requests
cmd = r"C:\Program Files\Wireshark\tshark.exe"

# if ethernet try
# cmd = r"C:\Program Files\Wireshark\tshark.exe -i ethernet"

# you can list all your interfaces by running "tshark.exe --list-interfaces"
# then if for instance you want to use the 4th try:
# cmd = r"C:\Program Files\Wireshark\tshark.exe -i 4"


def get_own_ip():
    r = requests.get("https://api64.ipify.org/?format=json")
    data = json.loads(r.content)
    return data["ip"]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
my_ip = socket.gethostbyname(socket.gethostname())
own_ip = get_own_ip()
reader = geolite2.reader()

def get_ip_location(ip):
    location = reader.get(ip)

    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown"

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown"

    return country, subdivision, city

last_ip = ""
for line in iter(process.stdout.readline, b""):
    columns = str(line).split(" ")

    if "SKYPE" in columns or "UDP" in columns:

        # for different tshark versions
        if "->" in columns:
            src_ip = columns[columns.index("->") - 1]
        elif "\\xe2\\x86\\x92" in columns:
            src_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
        else:
            continue

        if src_ip == my_ip or src_ip == own_ip or last_ip==src_ip:
            continue

        try:
            country, sub, city = get_ip_location(src_ip)
            print(">>> " + src_ip + " " + country + ", " + sub + ", " + city)
            last_ip = src_ip
        except:
            try:
                real_ip = socket.gethostbyname(src_ip)
                country, sub, city = get_ip_location(real_ip)
                print(">>> " + real_ip + " " + country + ", " + sub + ", " + city)
                last_ip = real_ip
            except:
                print("Not found")
