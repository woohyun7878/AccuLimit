##########
# SCRIPT #
##########

import subprocess
import os
import os.path
import re
import sys
import platform

SMC_BYTES_3C = re.compile(r"  BCLM  \[([a-z0-9]*)\s*\]  ([0-9a-f]+) \(bytes (.+)\)") # "  BCLM  [ui8 ]  60 (bytes 3c)"
VACTDISABLED = re.compile(r"VACTDisabled[\s]+0")  

def main():
    change_limit(smc_path, 50) # 50 IS A PLACEHOLDER
   

def get_smc_path(script_dir) -> str:
    smc_dir = os.path.join(script_dir, "smc")
    bin_path = os.path.join(smc_dir, "smc")
    
    if not os.path.exists(bin_path):
        current_dir = os.getcwd()
        os.chdir(smc_dir)
        out = subprocess.run(["make"], capture_output=True)
        os.chdir(current_dir)
        if out.returncode != 0:
            pass #ERROR: SMC Build Fail
        if not os.path.exists(bin_path):
            pass #ERROR: SMC binary does not exist at {}!".format(bin_path)

    return bin_path

def change_limit(smc_path, value):
    current_value = get_curr_limit(smc_path)
    if current_value is None:
        pass #ERROR: Failed to read battery information
    set = set_limit(smc_path, value)
    if not set:
        pass #ERROR: Failed to set battery limit

def set_limit(smc_path, value) -> int:

    if is_system_battery_care_activated():
        pass #ERROR: Please turn off battery care from System Preferences before proceeding.
    hex_value = hex(value).replace("0x", "")
    if hex_value is None or len(hex_value != 2):
        pass #ERROR: Hex conversion has failed, or the hex is too short.
    sudo = subprocess.run(["sudo", smc_path, "-k", "BCLM", "-w", hex_value], capture_output=True)
    if (sudo.returncode != 0):
        pass #ERROR: Failed to set battery limit
    return True

def get_curr_limit(smc_path) -> int:
    bclm = subprocess.run([smc_path, "-k", "BCLM", "-r"], capture_output=True)
    if (bclm.returncode != 0) or (len(bclm.stdout) == 0):
        pass #ERROR: Failed to read battery information
    parse_result = SMC_BYTES_3C.match(bclm.stdout.decode("utf-8").rstrip("\n"))

    if parse_result is None:
        pass #ERROR: SMC out parse failed or invalid
        
    ui8 = parse_result.group(1)
    curr_limit = int(parse_result.group(2))
    
    if ui8 != "ui8" or curr_limit < 20 or curr_limit > 100:
        pass #ERROR: Invalid SMC output! Type must be ui8 and limit must be between 20 ~ 100!
    
    return curr_limit

def is_system_battery_care_activated()-> bool:
    pmset = subprocess.run(["pmset", "-g"], capture_output=True)
    if (pmset.returncode != 0) or (len(pmset.stderr) != 0):
        pass #ERROR: pmset -g command fail
    if len(VACTDISABLED.findall(pmset.stdout.decode("utf-8").rstrip("\n"))) >= 1:
        return True
    return False

#######
# GUI #
#######
import PySimpleGUI as sg

sg.theme('DarkAmber')  

layout = [
    [sg.Text(text="AccuLimit", size=(20, 1), font=('Open Sans', 35), justification="center")],
    [sg.Text(text="Move slider to designate a charge limit.", size=(40, 1), font=('Open Sans', 15), justification="center", text_color="#EAD665")],
    [
        sg.Slider(
            range=(0, 100),
            default_value=50,
            orientation="h",
            size=(40, 15),
            font=('Open Sans', 15),
            key="slider",
            enable_events=True,
        )
    ],
    [sg.Text()]
    #,[sg.Button("Set", font=('Open Sans', 20), size=(4, 1), button_color="#D6C669", mouseover_colors="#A09660")]
]

window = sg.Window("Demo", layout, element_justification='c')

while True:
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break
    # Check OS and processor
    if platform.system() != "Darwin":
        pass #ERROR: Application is for OSX only
    if "Intel" not in platform.processor():
        pass #ERROR: Script must be run on Intel CPU

    script_dir = os.path.dirname(os.path.realpath(__file__))
    smc_path = get_smc_path(script_dir)
    event, values = window.read()
    
    limit_slider = int(values['slider'])
    if limit_slider != get_curr_limit(smc_path):
        change_limit(smc_path, limit_slider)

if not sg.WIN_CLOSED:
    window.close()

