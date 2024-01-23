
## Intro
Welcome to the folder containing all the BENNESAW BATE Racing data acquisition services. The entire system is Python and MatLab based.

This guide is split into two parts: a **User's Guide** and a **Developer's Guide**:
- If you will be working on these files (i.e. you are a data aq member), you will need to refer to the **Developer's Guide**
- Otherwise, the **User's Guide** should suffice for everyone else

_If you have any questions or need troubleshooting, feel free to reach out to Mathewos Samson on Teams, Discord or via email: msamson1@students.kennesaw.edu_
# parser setup
there are two options for using the parser:

1. download and extract the executable to run standalone (simplest but requires updates)

2. install python, clone repo, install packages and run script (more complicated but easier to update)

### downloading executable:

1. go to https://github.com/KSU-MS/KS5e-Data-Logging/actions/workflows/build-exe.yml?query=branch%3Adevelop+branch%3Amain++ 
    - you should see this: ![picture of workflow run page](readmepics/image.png)
2. click the workflow run (in this case `Merge pull request...`)

3. scroll down to the bottom of the page and click the artifact to download it:
    - ![picture of artifact download under workflow run](readmepics/image1.png)
    - your browser may alert you that you are downloading a virus, but trust the download and let it continue

4. once that download is complete, extract the contents of the .zip file

    - create 

5. download the latest .dbc file from the dbc gen repo https://github.com/KSU-MS/ksu-ms-dbc/releases 

6. 

##  manual python install
1. Python 3 is required, and may be installed here: https://www.python.org/downloads/. Make sure it is added to PATH
    - Python 3.8 is recommended to guarantee compatibility
2. For MatLab (OPTIONAL), you will need an education/work license to get it for free. Follow GT's instructions here: https://www.mathworks.com/academia/tah-portal/kennesaw-state-university-31081932.html
    - Really the only thing you need MatLab for is to plot the data after parsing. Otherwise, just having Python is enough
3. If you have not done so already, clone this GitHub repo or download it as a zip, extract, and save to somewhere safe
4. Change directory to the repo. All you have to do is `cd KS5e-Data-Logging`
5. optional step, create a python virtual environment by running these commands:
```python
pip install virtualenv
python -m virtualenv venv
.\venv\scripts\activate
pip install -r requirements.txt
```

(https://stackoverflow.com/questions/41972261/what-is-a-virtualenv-and-why-should-i-use-one)

6. Once you are here, download the needed pip libraries by issuing the command `pip install -r requirements.txt`

## User's Guide
If you are a user, everything you need to care about is in the `telemetry_exe` folder. Navigate to that directory.

There are two services: the **Live Console**, the **Parser and Plotter**

### Live Console
1. Either run the file `console_exe.py` with the Python Interpreter or issue the command `py -3 console_exe.py`
2. Select your source of data input and run it

### Parser and Plotter
1. Get the raw data CSVs from the SD card on the vehicle
2. Place them in the `Raw_Data` folder in this directory
3. Either run the file `parser_exe.py` with the Python Interpreter or issue the command `py -3 parser_exe.py`
4. Wait for the process to finish (a success message from `parser_exe.py` followed by termination)
5. You may now retrieve the parsed data from the `Parsed_Data` as well as the `Better_Parsed_Data` folder and the .mat file `output.mat`
   1. logs in `Parsed_Data` will be formatted a lil different than in `Better_Parsed_Data`, so peep both, but its the same data trust me

If you run the parser in the same raw data folder again, it will overwrite the files in `parsed-data` and `temp-parsed-data`

_The next steps are optional - only if you want to plot the results_

6. Open `dataPlots.m` in MatLab
7. In MatLab, first load `output.mat` by double clicking it on the sidebar. Then click run on `dataPlots.m`
    - This script will not execute fully if there is not enough data, and it will stop on the first plot it is missing data for