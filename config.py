# this file is used for setting the configuration of the project
save_img = True                                        # whether to save the screenshots in the directory
ACHIEVEMENTS_FILE = "./2.2.xlsx"                        # the path of the achievements
counts = {}                                             # the numbers of the screenshots in the corresponding sets, used for name the images
TESSDATA_PREFIX = r'./tesseract/tessdata'               # the path of tesseract(pre-set in the project)
TESSDATA_PATH = r'./tesseract/tesseract.exe'            # the path to executable application of tesseract
global listener_stop_flag                               # called by the Main.py and KeyboardListener.py to stop the listener thread
global main_stop_flag                                   # called by the Main.py and KeyboardListener.py to stop the main thread
names = {
    "temp": "temp",
    "不屈者的荣光": "GloryOfTheUnyielding",
    "与你同行的回忆": "TheMemoriesWeShare",
    "众秘探奇": "FathomTheUnfathomable",
    "我，开拓者": "Trailblazer",
    "战意奔涌": "EagerForBattle",
    "果壳中的宇宙": "UniverseInANutshell",
    "流光遗痕": "VestigeOfLuminflux",
    "瞬息欢愉": "MonmentOfJoy",
    "通往群星的轨道": "TheRailUntoTheStar"
}              # the name of different sets in the achievements

global location

# the index of the characters locations
'''
the exit button location is calculated based on screen (2560,1600)
(198,180)(505,228)      (8,14)(21,18)   title
(179,177)(2494,1494)    (6,11)(98,94)   screen
these data is calculate based on a rectangle (2283,192)
(168,22)(464,65)	    (7,11)(21,34)   name
(171,73)(709,109)	    (7,38)(32,57)   description
(168,120)(896,153)	    (7,63)(40,80)   detail
(2091,49)(2216,91)      (91,25)(98,48)  finish mark
(2054,105)(2249,139)    (89,54)(99,73)  finish date
(2119,80)(2214,107)     (92,41)(97,56)  finish but not accept
(2059,59)(2249,133)     (90,30)(98,70)  not finish
'''
'''
the exit button location is calculated based on screen (1920,1080)
(146,119)(405,166)      (7,11)(21,16)   title
(121,115)(1871,1023)    (6,11)(98,95)   screen
these data is calculate based on a rectangle (1713,,144)
(124,18)(376,54)	    (7,13)(21,38)   name
(124,55)(778,81)	    (7,38)(45,57)   description
(124,90)(849,127)	    (7,63)(49,89)   detail
(1567,36)(1671,70)      (91,25)(98,49)  finish mark
(1541,79)(1690,104)     (89,54)(99,73)  finish date
(1602,58)(1662,85)      (93,41)(97,60)  finish but not accept
(1545,54)(1671,91)      (90,37)(98,64)  not finish
'''

location_list = {
    '2560*1600': {
        "screen": {
            "size": [2560, 1600],
            "title": [[7, 11],[21, 14]],
            "screen":[[6, 11],[98, 94]]
        },
        "scroll": {
            "type1_time": 26,
            "type1_length": -95,
            "type2_time": 7,
            "type2_length": -100
            },
        "description": {
            "name":[[7, 11],[30, 36]],
            "description":[[7, 38],[42, 60]],
            "detail":[[7, 63],[52, 80]]
            },
        "finish": {
            "finish":[[91, 25],[98, 48]],
            "date":[[89, 54],[99,73]],
            "notAccept":[[92, 41],[97, 56]],
            "notFinish":[[90, 30],[98, 70]]
            },
        "exit":[97, 6]
    },
    '1920*1080': {
        "screen": {
            "size": [1920, 1080],
            "title": [[7, 11],[21, 16]],
            "screen":[[6, 11],[98, 95]]
        },
        "scroll": {
            "type1_time": 26,
            "type1_length": -95,
            "type2_time": 7,
            "type2_length": -100
            },
        "description": {
            "name":[[7, 13],[21, 38]],
            "description":[[7, 38],[45, 57]],
            "detail":[[7, 63],[49, 89]]
            },
        "finish": {
            "finish":[[91, 25],[98, 49]],
            "date":[[89, 54],[99,73]],
            "notAccept":[[93, 41],[97, 60]],
            "notFinish":[[90, 37],[98, 64]]
            },
        "exit":[97, 6]
    }
}