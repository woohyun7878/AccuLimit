# AccuLimit
### Brought to you by Woohyun Michael Jo . . .
## A limiter for your precious Macbook battery (Intel Only)
Rechargeable batteries, or accumulators, lose significant capacity if kept at full charge. If you are a casual gamer 
like myself or perform graphic-intensive work on a mac, you probably keep your mac plugged in. I developed this 
script with a simple GUI to limit the maximum battery charge on my mac; this way, you can keep the mac plugged in without
worrying about capacity loss.

The name "AccuLimit" comes from ACCU batteries (accumulators)

Function
------------------------
You can use the slider to set the battery charge limit at anywhere from 20% ~ 100%
If your current charge is over the battery limit, your Mac will discharge (use the internal battery instead of the power adapter)
until the battery level falls to the limit.

Requirements
------------------------
```
# 1. python3 
brew install python3

# 2. pip
python3 -m ensurepip --upgrade 
# based on you path settings, change python3 to python, py, or whatever you use

# 3. other requirements 
python3 -m pip install -r requirements.txt

# 4. Turn off system battery care function from System Preferences
```

Running the script
------------------------
```
# Simply run the script, and GUI will pop up
python3 main.py

# When you move the slider, terminal will ask for your password
password: [ENTER YOUR PASSWORD]

# You may also need to allow /scm/scm to be executed in the Security/Privacy preference pane
```

Acknowledgements
------------------------
SMC files are taken from [smcFanControl](https://github.com/hholtmann/smcFanControl "smcFanControl"). 

Notes
------------------------
1. The script executes root system functions, and I do not take responsibility for any damage it may cause. (I didn't encounter any)
2. M1 Macs are NOT supported. I may develop one for M1 Macs if I switch to one as my daily driver.