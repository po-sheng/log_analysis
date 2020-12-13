import os
import sys
import json
from multiprocessing import Pool

def multi_P(filePath):
    beat = []
    with open(filePath) as f:
        for line in f.readlines():
            data = json.loads(line)
            beat.append(data)

    if filePath.endswith("packetbeat.json"):
        return "packet", beat
    elif filePath.endswith("winlogbeat.json"):
        return "winlog", beat

def readJson(path):
    datasets = {}
    label2idx = {}
    idx2label = {}
    count = 0
    
    datasets["packet"] = []
    datasets["winlog"] = []
    datasets["fileName"] = []

    multi_data = []

    labels = os.listdir(path)
    labels = sorted(labels)
    
    for label in labels:
        labelPath = path + label
        beats = os.listdir(labelPath)
        datasets["fileName"].append(label)
        
        if len(label2idx) == 0 or label not in label2idx.keys():
            label2idx[label] = count
            idx2label[count] = label
            count += 1

        for beat in beats:
            filePath = labelPath + "/" + beat
            multi_data.append(filePath)
#============================================================================
# Ordinary methods
            packet = []
            winlog = []
            line_cnt = 0
            arrow = "=>"
            with open(filePath) as f:
                lines = f.readlines()
                for line in lines:
                    # Some cool try
                    if line_cnt % (len(lines)//100) == 0 and len(arrow) <= 102:
                        space = "" if len(arrow) - 2 == 100 else "  " if len(arrow) - 2 < 10 else " "
                        print("Reading json file for "+label+" |"+arrow+(" "*(102-len(arrow)))+"| "+space+str(len(arrow)-2)+"%", end='\r', flush=True)
                        arrow = "=" + arrow 
                    line_cnt += 1

                    data = json.loads(line)
                    
                    if beat.startswith("packet"):
                        packet.append(data)
                    elif beat.startswith("winlog"):
                        winlog.append(data)

            if beat.startswith("packet"):
                datasets["packet"].append(packet)
            elif beat.startswith("winlog"):
                datasets["winlog"].append(winlog)
#============================================================================
# Multi process methods

#     with Pool(len(multi_data)) as p:
#         ndata = p.map(multi_P, multi_data)
#     
#     for data in ndata:
#         if data[0] == "packet":
#             datasets["packet"].append(data[1])
#         elif data[0] == "winlog":
#             datasets["winlog"].append(data[1])
#============================================================================
    print()
    return datasets

if __name__ == "__main__":
    datasets = readJson("../dataset/Train/")

    print(len(datasets["packet"]))

