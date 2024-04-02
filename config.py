# this file is used for setting the configuration of the project
save_img = False                                        # whether to save the screenshots in the directory
ACHIEVEMENTS_FILE = "./2.1.xlsx"                        # the path of the achievements
counts = {}                                             # the numbers of the screenshots in the corresponding sets, use for name the images
SCROLL_VALUE = 26                                       # the screenshot rate, may be different in different devices
TESSDATA_PREFIX = r'./tesseract/tessdata'               # the path of tesseract(pre-set in the project)
TESSDATA_PATH = r'./tesseract/tesseract.exe'            # the path to executable application of tesseract
names = {
    "temp":"temp",
    "不屈者的荣光":"GloryOfTheUnyielding",
    "与你同行的回忆":"TheMemoriesWeShare",
    "众秘探奇":"FathomTheUnfathomable",
    "我，开拓者":"Trailblazer",
    "战意奔涌":"EagerForBattle",
    "果壳中的宇宙":"UniverseInANutshell",
    "流光遗痕":"VestigeOfLuminflux",
    "瞬息欢愉":"MonmentOfJoy",
    "通往群星的轨道":"TheRailUntoTheStar"
}                                                       # the name of different sets in the achievements



# the index of the characters locations
'''
the exit button location is calculated based on screen (2315,1317)
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
(2491, 90)    (97,6)
'''

location = {
    "screen": {
        "size": [2560, 1600],
        "title": [[7, 11],[21, 14]],
        "screen":[[6, 11],[98, 94]]
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
    }