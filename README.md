- 2 steps to run the code
    - `cd model`        
        - get into the model directory
    - `python3 predict.py /path/to/dataset`
        - run our code

- Dataset hierarchy
    Logs\n
    |- Train\n
    |   |-- Attack_<ID> (e.g. Attack_1)\n
    |   |   |--- winlogbeat.json\n
    |   |   |--- packetbeat.json\n
    |\n
    |- Test\n
    |   |-- Test_<ID> (e.g. Test_1)\n
    |   |   |--- winlogbeat.json\n
    |   |   |--- packetbeat.json\n
    |\n
    

- File explanation
    - model/predict.py
        - Main function, do rule-based classifier
    - script/readJson.py
        - input dataset path and read the json file for backward application
