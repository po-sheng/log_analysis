import sys
import numpy as np
sys.path.append("../script/")
from readJson import readJson

def main(path):
    # read data
    datasets = readJson(path)
    
    # do on each test data
    for idx in range(len(datasets["fileName"])):
        packet = datasets["packet"][idx]
        winlog = datasets["winlog"][idx]
        name = datasets["fileName"][idx]

        DDOS_count = 0
        port_count = {}
        login_count = 0
        sql_count = 0
        phishing = False
        
        # Discriminate DDOS, brute force, sql injection and port scan by packet beat destination port
        packet_count = len(packet)
        for packetLog in packet:
            if "destination" in packetLog.keys() and "ip" in packetLog["destination"].keys() and "port" in packetLog["destination"].keys() and "host" in packetLog.keys() and "ip" in packetLog["host"].keys():
                # Fulfill DDOS counter
                if packetLog["destination"]["ip"] == packetLog["host"]["ip"][1] and packetLog["destination"]["port"] == 80:
                    DDOS_count += 1
                
                # Fulfill port scan counter
                if packetLog["destination"]["ip"] == packetLog["host"]["ip"][1]:
                    port = packetLog["destination"]["port"]
                    if port in port_count.keys():
                        port_count[port] += 1
                    else:
                        port_count[port] = 1

            # Fulfill brute force and sql injection counter
            if "url" in packetLog.keys() and "query" in packetLog["url"].keys():
                query = packetLog["url"]["query"]
                if query.startswith("Login"):
                    login_count += 1
                if query.find("SELECT") != -1:
                    sql_count += 1
        
        # Discriminate phishing email winlog beat 
        step = 0
        for winLog in winlog:
            if "winlog" in winLog.keys() and "event_data" in winLog["winlog"].keys() and "ProcessName" in winLog["winlog"]["event_data"].keys():
                process = winLog["winlog"]["event_data"]["ProcessName"]
                if step == 0 and process.find("cmd.exe") != -1:
                    step = 1
                elif step == 1 and process.find("Adobe") != -1:
                    phishing = True
#                 elif step == 2 and process.find("tar.exe") != -1:
#                     phishing = True
        
        if sql_count > 10:
            pred = "attack 5"
            print(name, ": ", pred, sep='')
            continue
        
        # Phishing email
        if phishing:
            pred = "attack 4"
            print(name, ": ", pred, sep='')
            continue
        
        # Brute force
        if login_count > 1000 or login_count / packet_count > 0.7:
            pred = "attack 1"
            print(name, ": ", pred, sep='')
            continue
        
        # Port scan
        if len(port_count.keys()) > 1000 or len(port_count.keys()) / packet_count > 0.7:
            pred = "attack 3"
            print(name, ": ", pred, sep='')
            continue

        # DDOS
        if DDOS_count / packet_count > 0.7:
            pred = "attack 2"
            print(name, ": ", pred, sep='')
            continue
        
        cmp = []
        cmp.append(login_count / 1000)
        cmp.append(DDOS_count / packet_count)
        cmp.append(len(port_count.keys()) / 1000)
        cmp.append(0)
        cmp.append(sql_count / 10)

        pred = "attack "
        pred += str(np.argmax(np.array(cmp)) + 1)
        
        print(name, ": ", pred, sep='')
        
if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
        
