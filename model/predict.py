import sys
sys.path.append("../script/")
from readJson import readJson

def main(path):
    # read data
    datasets = readJson(path)
    
    # do on each test data
    for idx in range(len(datasets["fileName"])):
        pred = "attack 1"

        print(datasets["fileName"][idx], ": ", pred, sep='')
        

if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
