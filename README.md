- 2 steps to run the code
    - `cd model`        
        - get into the model directory
    - `python3 predict.py /path/to/dataset`
        - run our code

- Dataset hierarchy
    Logs\r 
    |- Train\r
    |   |-- Attack_<ID> (e.g. Attack_1)\r
    |   |   |--- winlogbeat.json\r
    |   |   |--- packetbeat.json\r
    |\r
    |- Test\r
    |   |-- Test_<ID> (e.g. Test_1)\r
    |   |   |--- winlogbeat.json\r
    |   |   |--- packetbeat.json\r
    |\r
    

- File explanation
    - model/predict.py
        - Main function, do rule-based classifier
    - script/readJson.py
        - input dataset path and read the json file for backward application
