import PySimpleGUI as sg
from tkinter import * 

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
            font=('Open Sans', 20),
            key="slider",
            enable_events=True,
        )
    ],
    [sg.Text()]
    #,[sg.Button("Set", font=('Open Sans', 20), size=(4, 1), button_color="#D6C669", mouseover_colors="#A09660")]
]

window = sg.Window("Demo", layout, element_justification='c')

while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    limit_slider = int(values['slider'])
    


    
