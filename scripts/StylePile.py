#                            ,,                      ,,    ,,
#   .M"""bgd mm            `7MM         `7MM"""Mq.   db  `7MM
#  ,MI    "Y MM              MM           MM   `MM.        MM
#  `MMb.   mmMMmm `7M"   `MF"MM  .gP"Ya   MM   ,M9 `7MM    MM  .gP"Ya
#    `YMMNq. MM     VA   ,V  MM ,M"   Yb  MMmmdM9    MM    MM ,M"   Yb
#  .     `MM MM      VA ,V   MM 8M""""""  MM         MM    MM 8M""""""
#  Mb     dM MM       VVV    MM YM.    ,  MM         MM    MM YM.    ,
#  P"Ybmmd"  `Mbmo    ,V   .JMML.`Mbmmd".JMML.     .JMML..JMML.`Mbmmd"
#                    ,V
#                 OOb"
#
# A helper extension for AUTOMATIC1111/stable-diffusion-webui and forks.
# Enter your keywords and let the selections help you determine the look.
# Thanks to xram64, maxaudron, jpsieben7, missionfloyd, Kilvoctu, catboxanon
# and ESPECIALLY ChatGPT for their help.

# Art movements from https://en.wikipedia.org/wiki/List_of_art_movements
# I threw out the ones that did not work and then added a mountain more
# from personal research.

#git push origin new-branch-name

import os
import re
import copy
import random
import math
import itertools

from os import listdir, path
from os.path import isfile, join

import xml.etree.ElementTree as ET

from decimal import Decimal, ROUND_HALF_UP

import modules.scripts as scripts
from modules.script_callbacks import on_ui_tabs

import gradio as gr
from modules.processing import Processed, process_images
from modules.shared import cmd_opts, opts, state

# Our main work folders
file_dir = os.path.dirname(os.path.realpath("__file__"))
ResourceDir = os.path.join(scripts.basedir(), f"StylePile/")

def calculate_value(sum_of_values, strength):
    if sum_of_values > 30:
        raise ValueError("Sum of values cannot exceed 30")

    base_value = 3 * strength + 2
    proportion = sum_of_values / 30
    result = base_value * proportion

    if result % 1 < 0.5:
        return int(result)
    else:
        return int(result) + 1

# Functions for filling the dropdowns from image names
def FilesInFolder(SourceFolder):
    return [file for file in os.listdir(SourceFolder) if file.endswith(".jpg")]

def JPGFilesInFolderFullPath(SourceFolder):
    return [os.path.join(SourceFolder, file) for file in os.listdir(SourceFolder) if file.endswith(".jpg")]

def XMLFilesInFolder(SourceFolder):
    return [file for file in os.listdir(SourceFolder) if file.endswith(".xml")]

<<<<<<< HEAD
def FuseThatPrompt(prompt,A,B,C):
    prompt=A+B+C
    return join(prompt)
=======
PresetXMLFiles = XMLFilesInFolder(ResourceDir)
PresetXMLFiles = list(map(lambda x: x.replace(".xml", ""), PresetXMLFiles))
Presets = ["Not set"] + PresetXMLFiles

# This sets up the default prompt that is used for all the sample images
def InsertDefaultPrompt(prompt,seed,batchcount,batchsize,width,height):
    prompt='Portrait of an attractive young lady,flower field background, square ratio'
    seed=669
    batchcount=1
    batchsize=4
    width=512
    height=512
    return [prompt,seed,batchcount,batchsize,width,height]
>>>>>>> 8c25c38 (Update)

def SaveAPreset(PresetName):
    # Ask for a filename
    # filename = input("Please enter a filename: ")

    # Create the XML file
    xml_file = open(ResourceDir + PresetName + ".xml", "w")

        # Write the root element
        xml_file.write("<Preset>\n")

        # Write the variables to the file with CDATA sections and default values
        xml_file.write("<Info>" + (Info or " ") + "</Info>\n")
        xml_file.write("<Positive>" + (Positive or " ") + "</Positive>\n")
        xml_file.write("<Negative>" + (Negative or " ") + "</Negative>\n")
        xml_file.write("<X>" + (X or "") + "</X>\n")
        xml_file.write("<Y>" + (Y or "") + "</Y>\n")
        xml_file.write("<A>" + (A or "") + "</A>\n")
        xml_file.write("<B>" + (B or "") + "</B>\n")
        xml_file.write("<C>" + (C or "") + "</C>\n")
        xml_file.write("<D>" + (D or "") + "</D>\n")
        xml_file.write("<E>" + (E or "") + "</E>\n")
        xml_file.write("<F>" + (F or "") + "</F>\n")

        # Close the root element
        xml_file.write("</Preset>\n")

<<<<<<< HEAD
    # Close the file
    xml_file.close()
    return PresetName
=======
        # Close the file
        xml_file.close()
        return PresetName
>>>>>>> 8c25c38 (Update)

def LoadAPreset(PresetName):
    if PresetName == "Not set/clear":
        Info = ""
        Positive = ""
        Negative = ""
        X = ""
        Y = ""
        A = ""
        B = ""
        C = ""
        D = ""
        E = ""
        F = ""

<<<<<<< HEAD
        return PresetName, Info, Positive, Negative, X, Y, A, B, C, D, E, F
=======
    # Check if the file exists and is not empty
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract values from the XML elements and assign them to variables
            Info = root.find('Info').text if root.find('Info') is not None else ''
            Positive = root.find('Positive').text if root.find('Positive') is not None else ''
            Negative = root.find('Negative').text if root.find('Negative') is not None else ''
            X = root.find('X').text if root.find('X') is not None else ''
            Y = root.find('Y').text if root.find('Y') is not None else ''
            A = root.find('A').text if root.find('A') is not None else ''
            B = root.find('B').text if root.find('B') is not None else ''
            C = root.find('C').text if root.find('C') is not None else ''
            D = root.find('D').text if root.find('D') is not None else ''
            E = root.find('E').text if root.find('E') is not None else ''
            F = root.find('F').text if root.find('F') is not None else ''

            # ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

            # Need to update the dropdown here somehow
            gr.update(visible=True)

            # ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

            return PresetName, Info, Positive, Negative, X, Y, A, B, C, D, E, F

        except ET.ParseError as e:
            print(f"Error: Failed to parse '{file_path}': {e}")
            return None
>>>>>>> 8c25c38 (Update)
    else:
        file_path = ResourceDir + PresetName + ".xml"

        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Extract values from the XML elements and assign them to variables
                Info = root.find("Info").text if root.find("Info") is not None else ""
                Positive = root.find("Positive").text if root.find("Positive") is not None else ""
                Negative = root.find("Negative").text if root.find("Negative") is not None else ""
                X = root.find("X").text if root.find("X") is not None else ""
                Y = root.find("Y").text if root.find("Y") is not None else ""
                A = root.find("A").text if root.find("A") is not None else ""
                B = root.find("B").text if root.find("B") is not None else ""
                C = root.find("C").text if root.find("C") is not None else ""
                D = root.find("D").text if root.find("D") is not None else ""
                E = root.find("E").text if root.find("E") is not None else ""
                F = root.find("F").text if root.find("F") is not None else ""

                return PresetName, Info, Positive, Negative, X, Y, A, B, C, D, E, F
            except:
                Info = ""
                Positive = ""
                Negative = ""
                X = ""
                Y = ""
                A = ""
                B = ""
                C = ""
                D = ""
                E = ""
                F = ""

                return PresetName, Info, Positive, Negative, X, Y, A, B, C, D, E, F


# This sets up the default prompt+settings that is used for all the sample images
def InsertDefaultPrompt(txt2img_steps,sl_auto_adjust_strength,prompt,negative,seed,batchcount,batchsize,width,height):
    prompt = "closeup portrait of attractive woman, flower field background"
    negative = "bad, garbage, incorrect proportions"
    seed=669
    batchcount=1
    batchsize=4
    width=512
    height=512
    sl_auto_adjust_strength = 4
    txt2img_steps = 20
    return [txt2img_steps,sl_auto_adjust_strength,prompt,negative,seed,batchcount,batchsize,width,height]

def set_dimensions(dimensions):
    width, height = map(int, dimensions.split('x'))
    return [width,height]

# Function to clean up text (final prompts mostly)
def clean_text(text):
    replacements = [(",,", ","), (" ,", ","), (", ", ","), ("( ", "("), (" )", ")"), (" ]", "]"), ("[ ", "["), (" :", ":"), (": ", ":"), ("  ", " ")]
    for old, new in replacements:
        while old in text:
            text = text.replace(old, new)
    return text.strip()

def convert_newlines_to_commas(line):
    line = line.replace("to", ",").replace("step", ",").strip()
    lines = line.strip().split('\n')
    if len(lines) > 2:
        return ','.join(lines)
    else:
        return line

def all_combinations(line):
    line = convert_newlines_to_commas(line)
    values = line.split(',')
    result = []

    for i in range(1, len(values) + 1):
        for subset in itertools.permutations(values, i):
            result.append(','.join(subset))

    return '\n'.join(result)

def all_shuffles(line):
    line = convert_newlines_to_commas(line)
    values = line.split(',')
    result = []

    for shuffle in itertools.permutations(values):
        result.append(','.join(shuffle))

    return '\n'.join(result)

def all_combinations_relative_sequence(line):
    values = line.split(',')
    result = []

    for i in range(1, len(values) + 1):
        partial_line = ','.join(values[:i])
        combinations = all_combinations(partial_line)
        result.append('\n'.join(combinations))

    return '\n'.join(result)

def all_shuffles_relative_sequence(line):
    values = line.split(',')
    result = []

    for i in range(len(values), len(values) + 1):  # Only include full-length permutations
        partial_line = ','.join(values[:i])
        shuffles = all_shuffles(partial_line)
        result.append('\n'.join(shuffles))

    return '\n'.join(result)


def a_to_b_step_c(input_string):
    try:
        # Split the input string and convert the values to Decimal
        temp = convert_newlines_to_commas(input_string)
        a, b, c = map(Decimal, temp.split(','))

        # Check if the step is non-zero
        if c != 0:
            result = []
            current = a
            while (c > 0 and current <= b) or (c < 0 and current >= b):
                result.append(round(float(current), 2))
                current += c
            return '\n'.join(map(str, result))
    except (ValueError, ArithmeticError):
        # If the input string cannot be split into three numeric values
        pass

    return input_string


# Load dropdowns for options without images in folders - a .txt file list
def load_list_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

file_path = (ResourceDir + "Data/" + "Concepts.txt")
ElementConcept = load_list_from_file(file_path)

ResultConcept = ["Not set","Random"] + ElementConcept

ResultNames = [
    "Photograph",
    "Digital Artwork",
    "3D Rendering",
    "Painting",
    "Drawing",
    "Vector Art",
    "Mixed media"
]

ResultTypeBefore = {
    "Photograph": "Photograph",
    "Digital Artwork": "Digital Artwork",
    "3D Rendering": "3D Rendered Artwork",
    "Painting": "Painting",
    "Drawing": "Hand drawn Artwork",
    "Vector Art": "Vector image",
    "Mixed media": "Mixed media Artwork"
}
    
ResultTypePositives = {
    "Photograph": ",4K",
    "Digital Artwork" : ",ArtStation,Dribbble",
    "3D Rendering": ",CGSociety",
    "Painting": ",Fine Art America,Saatchi Art",
    "Drawing": ",Saatchi Art,ArtStation,ArtNet",
    "Vector Art": ",Behance,Dribble",
    "Mixed media": " "
}

# At some point in time it looked like adding a bunch of these negative prompts helps,but now I am not so sure...
AlwaysBad = "(((text))),((watermark)),signature,low quality,worst quality"

ResultTypeNegatives = {
    "Photograph": " ",
    "Digital Artwork": "Screenshot",
    "3D Rendering": "Wireframe,Polygons,Screenshot",
    "Painting": "Brush,Art tools", 
    "Drawing": "Pencils,Art tools", 
    "Vector Art": " ", 
    "Mixed media": " "
}

ResultType = {
    "Not set": "",
    "Random": "Random",
}

ResultType.update(ResultTypePositives)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultExecutionList = FilesInFolder(ResourceDir + "Execution/")
ResultExecutionList = list(map(lambda x: x.replace(".jpg", ""), ResultExecutionList))
ResultExecutionList.sort()
ResultExecution = ["Not set", "Random"] + ResultExecutionList

ResultExecutionImages = JPGFilesInFolderFullPath(ResourceDir + "Execution/")
ResultExecutionImages = list(
    map(lambda x: x.replace("\\", "/"), ResultExecutionImages))

ResultExecutionB = ResultExecution

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultMoodList = FilesInFolder(ResourceDir + "Mood/")
ResultMoodList = list(map(lambda x: x.replace(".jpg", ""), ResultMoodList))
ResultMoodList.sort()
ResultMood = ["Not set", "Random"] + ResultMoodList

ResultMoodImages = JPGFilesInFolderFullPath(ResourceDir + "Mood/")
ResultMoodImages = list(map(lambda x: x.replace("\\", "/"), ResultMoodImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultArtistList = ResultMoodList = FilesInFolder(ResourceDir + "Moods/")
(ResourceDir + "Artists/")
ResultArtistList = list(map(lambda x: x.replace(".jpg", ""), ResultArtistList))
ResultArtistList.sort()
Artists = ["Not set", "Random"] + ResultArtistList

ResultArtistImages = JPGFilesInFolderFullPath(ResourceDir + "Artists/")
ResultArtistImages = list(map(lambda x: x.replace("\\", "/"), ResultArtistImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ArtMovementList = FilesInFolder(ResourceDir + "Art Movements/")
ArtMovementList = list(map(lambda x: x.replace(".jpg", ""), ArtMovementList))
ArtMovementList.sort()
ArtMovements = ["Not set", "Random"] + ArtMovementList

ArtMovementImages = JPGFilesInFolderFullPath(ResourceDir + "Art Movements/")
ArtMovementImages = list(map(lambda x: x.replace("\\", "/"), ArtMovementImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultColorList = FilesInFolder(ResourceDir + "Colors/")
ResultColorList = list(map(lambda x: x.replace(".jpg", ""), ResultColorList))
ResultColorList.sort()
ResultColor = ["Not set", "Random"] + ResultColorList

ResultColorImages = JPGFilesInFolderFullPath(ResourceDir + "Colors/")
ResultColorImages = list(map(lambda x: x.replace("\\", "/"), ResultColorImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

PresetXMLFiles = XMLFilesInFolder(ResourceDir)
PresetXMLFiles = list(map(lambda x: x.replace(".xml", ""), PresetXMLFiles))
Presets = ["Not set"] + PresetXMLFiles

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

with open(ResourceDir + "Data/Subjects.txt", "r+") as tf:
    Subjects = [line.rstrip() for line in tf]

with open(ResourceDir + "Data/Actions.txt", "r+") as tf:
    Actions = [line.rstrip() for line in tf]

with open(ResourceDir + "Data/Locations.txt", "r+") as tf:
    Locations = [line.rstrip() for line in tf]

with open(ResourceDir + "Data/Lines.txt", "r+") as tf:
    Lines = [line.rstrip() for line in tf]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

class Script(scripts.Script):
    def __init__(self):
        self.txt2img_prompt = gr.Textbox()
        self.img2img_prompt = gr.Textbox()
        self.txt2img_neg_prompt = gr.Textbox()

        self.txt2img_seed = gr.Number()
        self.txt2img_width = gr.Slider()
        self.txt2img_height = gr.Slider()

        self.txt2img_batch_count = gr.Slider()
        self.txt2img_batch_size = gr.Slider()

        self.txt2img_steps = gr.Slider()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

# At some point in time it looked like adding a bunch of these negative prompts helps,but now I am not so sure...
AlwaysBad = ",panel,logo,text,watermark,signature"

class Script(scripts.Script):
    txt2img_prompt = None
    img2img_prompt = None
    txt2img_seed = None
    txt2img_width = None
    txt2img_height = None
    txt2img_batch_count = None
    txt2img_batch_size = None

    def after_component(self, component, **kwargs):
        if component.elem_id == "txt2img_prompt":
            self.txt2img_prompt = component
            return self.txt2img_prompt
        if component.elem_id == "img2img_prompt":
            self.img2img_prompt = component
            return self.img2img_prompt
        if component.elem_id == "txt2img_neg_prompt":
            self.txt2img_neg_prompt = component
            return self.txt2img_neg_prompt

        if component.elem_id == "txt2img_seed":
           self.txt2img_seed = component
           return self.txt2img_seed
        if component.elem_id == "txt2img_width":
            self.txt2img_width = component
            return self.txt2img_width
        if component.elem_id == "txt2img_height":
            self.txt2img_height = component
            return self.txt2img_height

        if component.elem_id == "txt2img_batch_count":
            self.txt2img_batch_count = component
            return self.txt2img_batch_count
        if component.elem_id == "txt2img_batch_size":
            self.txt2img_batch_size = component
            return self.txt2img_batch_size

        if component.elem_id == "txt2img_steps":
            self.txt2img_steps = component
            return self.txt2img_steps

    def title(self):
        return "StylePile"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        gr.Markdown("-")
        with gr.Tab("StylePile"):
            if self.txt2img_prompt is not None:
                with gr.Accordion("Main generation parameters"):
                    with gr.Accordion("Automagic™ value adjustment, keywords, testing and tools",open=False):
                        with gr.Row():
                            strPrefix = gr.Textbox(lines=1,label="Prefix/Prompt keyword",placeholder="Type here")
                            sl_auto_adjust_strength = gr.Slider(minimum=0, maximum=8, value=0, step=1,label="Auto value strength")
                            strSuffix = gr.Textbox(lines=1,label="Suffix/End keywords",placeholder="Type here")
                        with gr.Row():
                            # Set a preset batch count
                            batch_dropdown = gr.inputs.Dropdown(
                                label="Batch count x Batch size",
                                choices=["1x1", "4x1", "8x1","16x1","32x1","1x4","4x4","8x4","16x4","32x4","1x8","2x8","4x8"],
                                default="1x1"
                                )
                            batch_dropdown.change(
                                fn = set_dimensions,
                                inputs = [batch_dropdown],
                                outputs = [self.txt2img_batch_count,self.txt2img_batch_size]
                                    )

                            # Enters the standard prompt used for all sample images with correct settings
                            bTestPrompt = gr.Button("Default prompt")
                            bTestPrompt.click(fn=InsertDefaultPrompt,
                                inputs  = [self.txt2img_steps,sl_auto_adjust_strength,self.txt2img_prompt,self.txt2img_neg_prompt,self.txt2img_seed,self.txt2img_batch_count,self.txt2img_batch_size,self.txt2img_width,self.txt2img_height],
                                outputs  = [self.txt2img_steps,sl_auto_adjust_strength,self.txt2img_prompt,self.txt2img_neg_prompt,self.txt2img_seed,self.txt2img_batch_count,self.txt2img_batch_size,self.txt2img_width,self.txt2img_height])

                            # Loads an example prompt that was generated by Bing AI :)
                            bInspireMe = gr.Button("Random prompt")
                            bInspireMe.click(fn=lambda x: random.choice(Lines) +",", 
                                inputs  = [self.txt2img_prompt],
                                outputs = [self.txt2img_prompt])

                            # Set a preset dimension
                            dimensions_dropdown = gr.inputs.Dropdown(
                                label="Dimension presets",
                                choices=["384x512", "512x512", "512x384","512x768","768x768","768x512","768x1024","1024x1024","1024x768"],
                                default="512x512"
                                )
                            dimensions_dropdown.change(
                                fn = set_dimensions,
                                inputs = [dimensions_dropdown],
                                outputs = [self.txt2img_width,self.txt2img_height]
                                    )

                        
                    with gr.Row():
                        with gr.Column():
                            ddResultConcept = gr.Dropdown(
                            ResultConcept, label="Concept/Direction/Adjective [CONCEPT]", value="Not set")
                            slResultConceptStrength = gr.Slider(
                                0, 2, value=1.0, step=0.05, show_label=False)

                            ddResultMood = gr.Dropdown(
                                ResultMood, label="Mood/Feeling [MOOD]", value="Not set")
                            slResultMoodStrength = gr.Slider(
                                0, 2, value=1.0, step=0.05, show_label=False)

                            ddResultColor = gr.Dropdown(
                                ResultColor, label="Palette/Color influence [COLOR]", value="Not set")
                            slResultColorStrength = gr.Slider(
                                0, 2, value=1.0, step=0.05, show_label=False)

                        with gr.Column():
                            ddCoreResultType = gr.Dropdown(
                                list(ResultType.keys()), label="Image type/Technology [TYPE]", value="Not set")   
                            slResultTypeStrength = gr.Slider(
                                0, 2, value=1.3, step=0.05, show_label=False)

                            ddResultExecution = gr.Dropdown(
                                ResultExecution, label="Result execution/General approach [RESULT]", value="Not set")
                            slResultExecutionStrength = gr.Slider(
                                0, 2, value=1.3, step=0.05, show_label=False)

                            ddResultExecutionB = gr.Dropdown(
                                ResultExecutionB, label="Result execution/General approach [RESULTB]", value="Not set")
                            slResultExecutionBStrength = gr.Slider(
                                0, 2, value=1.3, step=0.05, show_label=False)
                    with gr.Row():
                        gr.Markdown(
                            """
                            *You can enter the square bracket [KEYWORDS] in your prompt and a random one will be inserted in its place.*
                            """)
            with gr.Accordion("Artists [ARTIST] and Art movements [MOVEMENT]",open=False):
                with gr.Row():
                    with gr.Column():
                        selArtistA = gr.Dropdown(Artists, label="Artist", value="Not set")
                        sliImageArtistStrengthA = gr.Slider(0, 2, value=1.0, step=0.05, label="Influence")
                        selArtistB = gr.Dropdown(Artists, label="Artist", value="Not set")
                        sliImageArtistStrengthB = gr.Slider(0, 2, value=1.0, step=0.05, label="Influence")
                        selArtistC = gr.Dropdown(Artists, label="Artist", value="Not set")
                        sliImageArtistStrengthC = gr.Slider(0, 2, value=1.0, step=0.05, label="Influence")
                    with gr.Column():
                        selArtMovementA = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                        selArtMovementStrengthA = gr.Slider(0, 2, value=1.0, step=0.05, label="Influence")
                        selArtMovementB = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                        selArtMovementStrengthB = gr.Slider(0, 2, value=1.0, step=0.05, label="Influence")
                        selArtMovementC = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                        selArtMovementStrengthC = gr.Slider(0, 2, value=1.0, step=0.05, label="Influence")
                with gr.Row():
                    gr.Markdown(
                        """
                        *You can enter the square bracket [KEYWORDS] in your prompt and a random one will be inserted in its place.*
                        """)
            with gr.Accordion("Variables and Prompt presets",open=False):
                with gr.Row():
                    strSequentialPrompt = gr.Textbox(
                        lines=3, label="Sequential prompts [X]", placeholder="Insert [X] anywhere in main prompt to sequentially insert values from here. Random values will be added here or to main prompt.")
                with gr.Row():
                    b_all_combinations = gr.Button("All possible combinations")
                    b_all_combinations.click(fn=all_combinations, 
                        inputs  = [strSequentialPrompt],
                        outputs = [strSequentialPrompt])

                    b_all_shuffles = gr.Button("All possible shuffles")
                    b_all_shuffles.click(fn=all_shuffles, 
                        inputs  = [strSequentialPrompt],
                        outputs = [strSequentialPrompt])

                    b_all_shuffles = gr.Button("A to B step C")
                    b_all_shuffles.click(fn=a_to_b_step_c, 
                        inputs  = [strSequentialPrompt],
                        outputs = [strSequentialPrompt])

                    b_clear_field = gr.Button("Clear")
                    b_clear_field.click(fn=lambda x: "", 
                        inputs  = [],
                        outputs = [strSequentialPrompt])

                with gr.Row():
                    strSubSequentialPrompt = gr.Textbox(
                        lines=3, label="SubSequential prompts [Y]", placeholder="Insert [Y] in the final prompt <== to sequentially insert values from here (and increase prompt count). This is done after all other prompts and loops through all lines.")

                with gr.Row():
                    with gr.Column():
                        strRandomPromptA = gr.Textbox(
                            lines=3, label="Random [A]", placeholder="Insert [A] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                        strRandomPromptB = gr.Textbox(
                            lines=3, label="Random [B]", placeholder="Insert [B] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                        strRandomPromptC = gr.Textbox(
                            lines=3, label="Random [C]", placeholder="Insert [C] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                    with gr.Column():
                        strRandomPromptD = gr.Textbox(
                            lines=3, label="Random [D]", placeholder="Insert [D] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                        strRandomPromptE = gr.Textbox(
                            lines=3, label="Random [E]", placeholder="Insert [E] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                        strRandomPromptF = gr.Textbox(
                            lines=3, label="Random [F]", placeholder="Insert [F] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                
                with gr.Row(): 
                    strPresetInfo = gr.Textbox(lines=4,label="Preset information",placeholder="You can type a short description or instructions for this preset here and it will be saved/displayed depending on what button you press.")

                with gr.Row(): # Saving and Loading
                    # Create a Gradio input field for PresetName
                    strPresetName = gr.Textbox(lines=1,label="Preset name",placeholder="Type here")

                    # Load a preset from XML
                    ddPresets = gr.Dropdown(Presets,label="Select Preset",value="Not set/clear")
                    ddPresets.change(
                        fn = LoadAPreset,
                        inputs = [ddPresets],
                        outputs = [strPresetName,strPresetInfo,self.txt2img_prompt,self.txt2img_neg_prompt,strSequentialPrompt,strSubSequentialPrompt,strRandomPromptA,strRandomPromptB,strRandomPromptC,strRandomPromptD,strRandomPromptE,strRandomPromptF]
                        )

                    # Save a preset to XML
<<<<<<< HEAD
                    bSavePreset = gr.Button(value="Save Preset",size="sm")
=======
                    bSavePreset = gr.Button(value='Save Preset',size='sm')
>>>>>>> 8c25c38 (Update)
                    bSavePreset.click(
                        fn=SaveAPreset,
                        inputs = [strPresetName,strPresetInfo,self.txt2img_prompt,self.txt2img_neg_prompt,strSequentialPrompt,strSubSequentialPrompt,strRandomPromptA,strRandomPromptB,strRandomPromptC,strRandomPromptD,strRandomPromptE,strRandomPromptF],
                        outputs = [ddPresets]
                        )
<<<<<<< HEAD
=======

                    # Load a preset from XML
                    ddPresets = gr.Dropdown(Presets,label="Select Preset",value="Not set")
                    ddPresets.change(
                        fn = LoadAPreset,
                        inputs = [ddPresets],
                        outputs = [ddPresets,strPresetInfo,self.txt2img_prompt,self.txt2img_neg_prompt,strSequentialPrompt,strSubSequentialPrompt,strRandomPromptA,strRandomPromptB,strRandomPromptC,strRandomPromptD,strRandomPromptE,strRandomPromptF]
                        )
                
                    # bLoadPreset = gr.Button('Load Preset')
                    # bLoadPreset.click(
                    #     fn = LoadAPreset,
                    #     inputs = [ddPresets],
                    #     outputs = [ddPresets,strPresetInfo,self.txt2img_prompt,self.txt2img_neg_prompt,strSequentialPrompt,strSubSequentialPrompt,strRandomPromptA,strRandomPromptB,strRandomPromptC,strRandomPromptD,strRandomPromptE,strRandomPromptF]
                    #     )

            with gr.Accordion("Artists and Art movements",open=False):
                with gr.Column():
                    selArtistA = gr.Dropdown(Artists, label="Artist", value="Not set")
                    sliImageArtistStrengthA = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtistB = gr.Dropdown(Artists, label="Artist", value="Not set")
                    sliImageArtistStrengthB = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtistC = gr.Dropdown(Artists, label="Artist", value="Not set")
                    sliImageArtistStrengthC = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                with gr.Column():
                    selArtMovementA = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                    selArtMovementStrengthA = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtMovementB = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                    selArtMovementStrengthB = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtMovementC = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                    selArtMovementStrengthC = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
>>>>>>> 8c25c38 (Update)

            with gr.Accordion("Prompt tools",open=False):
                with gr.Row():
                    gr.Markdown(
                        """
                        This is not StylePile specific, just described and made easier to insert into your prompt. It will always be added to the end of the Positives field.
                        """)
                with gr.Row():
                    with gr.Accordion("Attention/emphasis"):
                        with gr.Row():
                            with gr.Column(scale=1):
                                gr.Markdown(
                                    """
                                    An attention/emphasis modifier value can be added to parts of the prompt like this **(A:1.3)** < this part would be about 30% stronger. To save some typing you can select the line you want to make stronger and use **Ctrl+Shift+Arrow keys up** or **down** to add these parenthesis and change the value. 1.3 seems like a good starting point if you want to see some impact. Interestingly, adding **very** as a keyword may have a similar or even stronger effect.
                                    """
                                )
                            with gr.Column(scale=3):
                                tbAdjustStrength = gr.Textbox(label="Adjust strength", placeholder="Enter prompt here")
                                sbAdjustStrength = gr.Slider(0.1, 2.0, value=1.3, step=0.1, label="Strength") 
                                bAdjustStrength = gr.Button("Insert")
                with gr.Row():
                    with gr.Accordion("Morph from-to"):
                        with gr.Row():
                            with gr.Column(scale=1):
                                gr.Markdown(
                                    """
                                    You can start with a prompt element and then, after a certain percentage of steps, start converting this prompt into something else. Basically it looks like [A:B:0.5] with A being the first part to do, B being what it should be morphing into and 0.5 representing a percentage of when it should start the conversion process. Thus in case of 0.5 that is 50% of the whole process.
                                    """)
                            with gr.Column(scale=3):
                                tbMorphFrom = gr.Textbox(label="Morph from", placeholder="Prompt A")
                                tbMorphTo = gr.Textbox(label="Morph to", placeholder="Prompt B")
                                sbMorphStrength = gr.Slider(0.05, 0.95, value=0.5, step=0.05, label="Starting point")    
                                bInsertMorph = gr.Button("Insert")
                with gr.Row():
                    with gr.Accordion("Alternating words"):
                        with gr.Row():
                            with gr.Column(scale=1):  
                                gr.Markdown(
                                    """
                                    You can mix two prompt elements where each step they get swapped. It looks like [A|B] thus processing A each odd step and B each even step. This may produce some interesting results or just make a mess.
                                    """)
                            with gr.Column(scale=3):
                                tbBounceFrom = gr.Textbox(label="Bounce from", placeholder="Prompt A")
                                rbBounceTo = gr.Textbox(label="Bounce to", placeholder="Prompt B")  
                                bBounce = gr.Button("Insert")
                with gr.Row():
                    gr.Markdown(
                        """
                        These last two sections appear to benefit from increasing sampling steps and CFG scale.
                        """)
                
                if self.txt2img_prompt is not None:
                    bAdjustStrength.click(fn=lambda p,x,y: p + "(" + x + ":" + str(y) + ")",
                        inputs  = [self.txt2img_prompt,tbAdjustStrength,sbAdjustStrength],
                        outputs = [self.txt2img_prompt])

                    bInsertMorph.click(fn=lambda p,x,y,z: p + "[" + x + ":" + y + ":" + str(z) + "]",
                        inputs  = [self.txt2img_prompt,tbMorphFrom,tbMorphTo,sbMorphStrength],
                        outputs = [self.txt2img_prompt])

                    bBounce.click(fn=lambda p,x,y: p + "[" + x + "|" + y + "]",
                        inputs  = [self.txt2img_prompt,tbBounceFrom,rbBounceTo],
                        outputs = [self.txt2img_prompt])
                    
                if self.img2img_prompt is not None:
                    bAdjustStrength.click(fn=lambda p,x,y: p + "(" + x + ":" + str(y) + ")",
                        inputs  = [self.img2img_prompt,tbAdjustStrength,sbAdjustStrength],
                        outputs = [self.img2img_prompt])

                    bInsertMorph.click(fn=lambda p,x,y,z: p + "[" + x + ":" + y + ":" + str(z) + "]",
                        inputs  = [self.img2img_prompt,tbMorphFrom,tbMorphTo,sbMorphStrength],
                        outputs = [self.img2img_prompt])

                    bBounce.click(fn=lambda p,x,y: p + "[" + x + "|" + y + "]",
                        inputs  = [self.img2img_prompt,tbBounceFrom,rbBounceTo],
                        outputs = [self.img2img_prompt])


        with gr.Tab("Looks") as StyleTab:
            gr.Markdown(
                """
                **Result execution/General approach**
                This strongly influences in what direction the result 
                """
                )
            gr.Gallery(value=ResultExecutionImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Mood"):
            gr.Gallery(value=ResultMoodImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Artists"):
            gr.Gallery(value=ResultArtistImages, show_label=False).style(
                grid=(2, 2, 2, 2, 3, 3), container=False)
            
        with gr.Tab("Art movements"):
            gr.Gallery(value=ArtMovementImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)
            
        with gr.Tab("Colors"):
            gr.Gallery(value=ResultColorImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)
                
        with gr.Tab("Help"):
            gr.Markdown(
                """
                ## Hello, StylePile here
                ### Introduction
                **StylePile** is a mix and match system for adding elements to prompts that affect the style of the result. Hence the name. By default, these elements are placed in a specific order and given strength values. Which means the result sort-of evolves. I have generated thousands of images for each main **Image type** and tweaked the keywords to attempt giving expected results most of the time. Certainly, your suggestions for improvements are very welcome.
                ### Base workflow
                You select extra settings in this script and then hit the standard orange **Generate** button to get results.
                
                For example, if you select the **Painting** image type, then almost all results will look like Paintings. Selecting **Mood** will have a certain influence on the overall look in some way (if it"s something humanoid it may show emotion, but also colors and overall feel may change). Setting **Colors** will change the general tonality of the result. And setting **View** will attempt to change how the subject is viewed. Attempt, because view appears to be the least reliable keyword. These elements are placed in order of influence and supported by certain strength values. These basic settings produce very quick results close to the general look you want.
                ![]({path.join(ResourceDir,"Artists.jpg") ""})
                Moving on, adding a **Art movement** will combine with **Image type** to influence how the result generally looks. These styles are based on classic and modern Painting/Art/design movements (which I picked after hours and thousands of samples of testing) and can have a strong influence on the end result. Either it will be more realistic or artistic, or look like a comic book etc. In general, this is a really strong element for getting the look you want. Its influence can be adjusted with the slider above. Experiment with the values, keeping in mind that anything above 1.5 will start becoming a mess. In a similar way, but more focused, you can select an **Artist** and, of course, that will have a very visible effect on the result as well. Currently there are 135 artists, 55 art styles and 25 emotions available for selection and represented with preview images.

                Strength of these settings has been preset at 1.3, as that appears to be the golden ratio for getting good results. Sometimes very low settings have an interesting result as well. You can, and should, freely mix and match these settings to get different results. Classic Painting styles affected or affecting 3D look quite interesting. Photography can look cool with some of the brighter, more artistic styles etc. Sometimes raising CFG scale to 15,20 or more also helps to REALLY push the style onto the image.

                ### Advanced workflow
                StylePile can overtake the generation process, allowing you to generate a large amount of different results with very little extra work. There are two types of variables you can use: [X] and [R]. When you add an [X] to your prompt, it sequentially takes values from the **Sequential prompts** text area. You can have dozens of lines there and they will be processed in sequence. When you add [R] to the prompt a value from the **Random** text area will be inserted in its place. By combining these a huge variety in prompts is very easy to do.

                When using this, **Batch count** will move through the prompts and **Batch size** will set how many copies with the given prompt to make. If the seed is not random, it will increase with each batch size step. Any random elements will still be picked randomly.

                ### Tips and tricks
                If you add your own Artist, I would recommend having **by Artist** in front of their name. Depending on their popularity (or lack thereof) this appears to have a very tangible influence on the result. In general, most of the elements that influence the look appear to work best with a certain strength boost, hence the 1.3 default values.
                Another thing to keep in mind is relationships between keywords and type of content. For example, if you want a reasonably realistic looking image of an alien cyborg. Selecting **Photo** will mostly produce fairly clumsy results. But, if you select **3D rendering** and **Realistic, Ultrarealistic** or **Ultra detailed** as direction, the result may actually be closer to what you expect. The opposite is true as well. There are certain things that you will not get to look realistic no matter what the modifiers are if Image type is not set to **Photo**. Try kittens.
                In general just experiment with **Image type** and **Direction**. An easy way to do it is selecting random settings, a high batch count and then checking the keywords on the results you like.
                ### Modifiers
                Elements of the prompt can be modified to have a certain strength or change over time. Normally you do this by typing into the prompt, but here I have added tools that will actually insert pre-formatted text so it is easier to understand what it should look like. Note that it doesn"t have to be a single word, it is a part of the prompt, so it can be several words or a full sentence. Also note that it will be added to the end of the prompt no matter where the cursor was due to limitations of gradio.

                ### Example images, adding your own selections to dropdowns
                Example images stored in the script folders are more than just images. Their filenames are used to create the **Direction**, **Mood**, **Artist** and Art **movement** dropdown selections. This gives you the ability to Add/Remove parameters as you wish. Just place an image in the folder and name it as the option you want to see in the dropdown. Delete image file to remove that option.
                
                In case you would like to suggest an artist be added to the roster, I would recommend making 8+ sample images first. To see if SD actually "knows" that artist and their style appears unique enough. The portraits you can see in the info pages were generated with the following settings:
                
                ### Sample portrait prompt
                Positive: Portrait of an attractive young lady,flower field background,(by [X]:1.3), square ratio
                Negative - missing limbs, extra limbs, watermark,label,text

                [X] is **Artist Name Surname** From my research adding **Artist** can really help to get the correct look.

                20 steps on Euler A
                Seed - 669 - batch of 4 images

                Generally that produces a fairly nice portrait with enough room to show off the given style. Do compare the results to the actual style. As SD will produce something it "thinks" may be correct based on their name (guessing nationality, basing it on something that has mentioned a similar name etc) and that influences the results, but not in a good way.

                ### In conclusion
                I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute in some way*, just visit https://github.com/some9000/StylePile

                *Hey, if you have a 8+Gb graphics card just laying around I"m happy to take it (:
            """)

        return [sl_auto_adjust_strength,
                strPrefix,
                ddResultConcept,
                slResultConceptStrength,
                strSequentialPrompt,
                strSubSequentialPrompt,
                strRandomPromptA,
                strRandomPromptB,
                strRandomPromptC,
                strRandomPromptD,
                strRandomPromptE,
                strRandomPromptF,
                slResultTypeStrength,
                ddCoreResultType,
                ddResultExecution,
                slResultExecutionStrength,
                ddResultExecutionB,
                slResultExecutionBStrength,
                ddResultMood,
                slResultMoodStrength,
                ddResultColor,
                slResultColorStrength,
                selArtMovementStrengthA,
                selArtMovementA,
                selArtMovementStrengthB,
                selArtMovementB,
                selArtMovementStrengthC,
                selArtMovementC,
                sliImageArtistStrengthA,
                selArtistA,
                sliImageArtistStrengthB,
                selArtistB,
                sliImageArtistStrengthC,
                selArtistC,
                strSuffix
                ]

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

    def run(self, p,
            sl_auto_adjust_strength,
            strPrefix: str,
            ddResultConcept,
            slResultConceptStrength,
            strSequentialPrompt: str,
            strSubSequentialPrompt: str,
            strRandomPromptA: str,
            strRandomPromptB: str,
            strRandomPromptC: str,
            strRandomPromptD: str,
            strRandomPromptE: str,
            strRandomPromptF: str,
            slResultTypeStrength,
            ddCoreResultType,
            ddResultExecution,
            slResultExecutionStrength,
            ddResultExecutionB,
            slResultExecutionBStrength,
            ddResultMood,
            slResultMoodStrength,
            ddResultColor,
            slResultColorStrength,
            selArtMovementStrengthA,
            selArtMovementA,
            selArtMovementStrengthB,
            selArtMovementB,
            selArtMovementStrengthC,
            selArtMovementC,
            sliImageArtistStrengthA,
            selArtistA,
            sliImageArtistStrengthB,
            selArtistB,
            sliImageArtistStrengthC,
            selArtistC,
            strSuffix
            ):

        # If it"s all empty just exit function.
        if len(p.prompt) == 0:
            print(
                f"\nEmpty prompt! It helps to have at least some guidance for SD. Remember to insert an [X], [A] or [B] into main prompt if you want to use variable values.")
            return

<<<<<<< HEAD
        auto_step_scale = 0
        small_step_scale = 2
        large_step_scale = 6

        auto_cfg_scale = 0
        small_cfg_increase = 1
        large_cfg_increase = 3

        if ddResultConcept != "Not set":
            auto_step_scale += small_step_scale
            auto_cfg_scale += small_cfg_increase
        
        if ddResultMood != "Not set":
            auto_step_scale += small_step_scale
            auto_cfg_scale += small_cfg_increase

        if ddResultColor != "Not set":
            auto_step_scale += small_step_scale
            auto_cfg_scale += small_cfg_increase

        if ddCoreResultType != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase
            
        if ddResultExecution != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase 

        if ddResultExecutionB != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase

        if selArtMovementA != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase

        if selArtMovementB != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase

        if selArtMovementC != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase

        if selArtistA != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase 

        if selArtistB != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase 

        if selArtistC != "Not set":
            auto_step_scale += large_step_scale
            auto_cfg_scale += large_cfg_increase
=======
        # Batch lines present?
        if strSequentialPrompt is not None:
            BatchLines = [x.strip() for x in strSequentialPrompt.splitlines()]
            LineCount = len(BatchLines)
        else:
            BatchLines = []
            LineCount = 0

        # SubBatch lines present?
        if strSubSequentialPrompt is not None:
            SubBatchLines = [x.strip() for x in strSubSequentialPrompt.splitlines()]
            SubLineCount = len(SubBatchLines)
        else:
            SubBatchLines = []
            SubLineCount = 0
>>>>>>> 8c25c38 (Update)

        TempText = ""
        SubTempText = ""

        images = []
        seeds = []
        prompts = []
        infotexts = []

        # Any random lines present?
        if strRandomPromptA is not None:
            RandomLinesA = [r.strip() for r in strRandomPromptA.splitlines()]
        else:
            RandomLinesA = []
        
        if strRandomPromptB is not None:
            RandomLinesB = [r.strip() for r in strRandomPromptB.splitlines()]
        else:
            RandomLinesB = []

        if strRandomPromptC is not None:
            RandomLinesC = [r.strip() for r in strRandomPromptC.splitlines()]
        else:
            RandomLinesC = []
        
        if strRandomPromptD is not None:
            RandomLinesD = [r.strip() for r in strRandomPromptD.splitlines()]
        else:
            RandomLinesD = []

        if strRandomPromptE is not None:
            RandomLinesE = [r.strip() for r in strRandomPromptE.splitlines()]
        else:
            RandomLinesE = []

        if strRandomPromptF is not None:
            RandomLinesF = [r.strip() for r in strRandomPromptF.splitlines()]
        else:
            RandomLinesF = []

        # Overtake amounts of things to generate so we can go through different variables
        
        # Batch lines present?
        if strSequentialPrompt is not None:
            BatchLines = [x.strip() for x in strSequentialPrompt.splitlines()]
            LineCount = len(BatchLines)
        else:
            BatchLines = []
            LineCount = 0

        # SubBatch lines present?
        if strSubSequentialPrompt is not None:
            SubBatchLines = [x.strip() for x in strSubSequentialPrompt.splitlines()]
            SubLineCount = len(SubBatchLines)
        else:
            SubBatchLines = []
            SubLineCount = 0
        
        SequentialPromptCount = 1
        SubSequentialPromptCount = 1

        # If we have [X] variables use their amount, unless unchecked
<<<<<<< HEAD
        if LineCount > 0:
            SequentialPromptCount = LineCount
        else:
            SequentialPromptCount = 1
        
        # If we have [Y] variables use their amount, unless unchecked
=======
        if cbChangeCount == True and LineCount > 0:
            MainJobCount = LineCount

        SubCycleCount = 1

>>>>>>> 8c25c38 (Update)
        if SubLineCount > 0:
            SubSequentialPromptCount = SubLineCount
        else:
            SubSequentialPromptCount = 1


        # Overtake initial iterat
        # p.n_iter = 1

        UserBatchCount = p.n_iter 
        p.n_iter = 1
        
        UserBatchSize = p.batch_size
        p.batch_size = 1

        FinalResultExecution = ""

        # So the progress bar works correctly
        state.job_count = UserBatchCount * UserBatchSize * SequentialPromptCount  * SubSequentialPromptCount

        JobCounter = 1
        TotalJobCounter = UserBatchCount * UserBatchSize * SequentialPromptCount  * SubSequentialPromptCount

        for a in range(UserBatchCount):
            SeedStep = 0

            AllMovements = ""
            AllArtists = ""

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            # Large artist selection
            if selArtistA != "Not set":
                # If Random is selected then pick a random artist
                if selArtistA == "Random":
                    AllArtists += ",(by Artist " + random.choice(ResultArtistList) + \
                        ":" + str(sliImageArtistStrengthA) + ")"
                # otherwise use the selected value
                else:
                    AllArtists += ",(by Artist " + selArtistA + \
                        ":" + str(sliImageArtistStrengthA) + ")"

            if selArtistB != "Not set":
                if selArtistB == "Random":
                    AllArtists += ",(by Artist " + random.choice(ResultArtistList) + \
                        ":" + str(sliImageArtistStrengthB) + ")"
                else:
                    AllArtists += ",(by Artist " + selArtistB + \
                        ":" + str(sliImageArtistStrengthB) + ")"

            if selArtistC != "Not set":
                if selArtistC == "Random":
                    AllArtists += ",(by Artist " + random.choice(ResultArtistList) + \
                        ":" + str(sliImageArtistStrengthC) + ")"
                else:
                    AllArtists += ",(by Artist " + selArtistC + \
                        ":" + str(sliImageArtistStrengthC) + ")"

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            # Large style selection
            if selArtMovementA != "Not set":
                if selArtMovementA == "Random":
                    AllMovements += " (" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthA) + ")"
                else:
                    AllMovements += " (" + selArtMovementA + ":" + str(selArtMovementStrengthA) + ")"

            if selArtMovementB != "Not set":
                if selArtMovementB == "Random":
                    AllMovements += " (" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthB) + ")"
                else:
                    AllMovements += " (" + selArtMovementB + ":" + str(selArtMovementStrengthB) + ")"

            if selArtMovementC != "Not set":
                if selArtMovementC == "Random":
                    AllMovements += " (" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthC) + ")"
                else:
                    AllMovements += " (" + selArtMovementC + ":" + str(selArtMovementStrengthC) + ")"

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            # Clear the variables so random selection can work
            FinalResultMood = ""
            FinalResultColor = ""
            FinalConcept = ""

            # Preset the selection variables
            MainType = ""

            TypeFront = ""
            TypePositives = ""
            TypeNegatives = ""

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            if ddResultConcept != "Not set":
                if ddResultConcept == "Random":
                    if slResultConceptStrength == 1:
                        FinalConcept = " " + random.choice(ElementConcept) + " "
                    else:
                        FinalConcept = " (" + random.choice(ElementConcept) + ":" + str(slResultConceptStrength) + ") "  
                else:
                    if slResultConceptStrength == 1:
                        FinalConcept = " " + ddResultConcept + " "
                    else:
                        FinalConcept = " (" + ddResultConcept + ":" + str(slResultConceptStrength) + ") "
            else:
                FinalConcept = ""

            # If main prompt isn"t empty...
            if ResultType[ddCoreResultType] != "":
            # If it is random, give it a random value
                if ResultType[ddCoreResultType] == "Random":
                    MainType = random.choice(ResultNames)
                # otherwise use the selected value
                else:
                    MainType = ddCoreResultType

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            if ddResultExecution != "Not set":
                if ddResultExecution == "Random":
                    FinalResultExecution = " (" + random.choice(
                        ResultExecutionList) + ":" + str(slResultExecutionStrength) + ") style "
                else:
                    FinalResultExecution = " (" + ddResultExecution + \
                        ":" + str(slResultExecutionStrength) + ") style "
            else:
                FinalResultExecution = ""

            if ddResultExecutionB != "Not set":
                if ddResultExecutionB == "Random":
                    FinalResultExecutionB = " (" + random.choice(
                        ResultExecutionList) + ":" + str(slResultExecutionBStrength) + ") style "
                else:
                    FinalResultExecutionB = " (" + ddResultExecutionB + \
                        ":" + str(slResultExecutionBStrength) + ") "
            else:
                FinalResultExecutionB = ""

            if FinalResultExecution != "" and FinalResultExecutionB != "":
                FinalResultExecution = FinalResultExecution + " and " + FinalResultExecutionB + " "
            else:
                if FinalResultExecution != "" or FinalResultExecutionB != "":
                    FinalResultExecution = FinalResultExecution + FinalResultExecutionB + " "

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            # Pick the mood
            if ddResultMood != "Not set":
                if ddResultMood == "Random":
                    FinalResultMood = " (" + random.choice(ResultMoodList) + \
                        ":" + str(slResultMoodStrength) + ") "
                else:
                    FinalResultMood = " (" + ddResultMood + \
                        ":" + str(slResultMoodStrength) + ") "

            # Colors
            if ddResultColor!= "Not set":
                if ddResultColor == "Random":
                    FinalResultColor = ",(" + random.choice(ResultColorList) + " color:" + str(slResultColorStrength) + ") "
                else:
                    TempText = TempText.replace("[A]", "")

                if len(RandomLinesB) > 0:
                    TempText = TempText.replace(
                        "[B]", random.choice(RandomLinesB))
                else:
                    TempText = TempText.replace("[B]", "")

                if len(RandomLinesC) > 0:
                    TempText = TempText.replace(
                        "[C]", random.choice(RandomLinesC))
                else:
                    TempText = TempText.replace("[C]", "")

                if len(RandomLinesD) > 0:
                    TempText = TempText.replace(
                        "[D]", random.choice(RandomLinesD))
                else:
                    TempText = TempText.replace("[D]", "")

                if len(RandomLinesE) > 0:
                    TempText = TempText.replace(
                        "[E]", random.choice(RandomLinesE))
                else:
                    TempText = TempText.replace("[E]", "")

                if len(RandomLinesF) > 0:
                    TempText = TempText.replace(
                        "[F]", random.choice(RandomLinesF))
                else:
                    TempText = TempText.replace("[F]", "")

                    if LineCount > 0:
                        if len(BatchLines[XChoice % LineCount]) > 0:
                            TempVariable = BatchLines[XChoice % LineCount]
                    
                    TempText = p.prompt.replace("[X]", " " + TempVariable + " ").replace("[x]", " " + TempVariable + " ")
                    XChoice += 1
                    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->
                        
                

                # If main prompt isn't empty...
                if MainType != "":
                    # Format our variables to merge into positive prompt...
                    TypeFront = " (" + FinalConcept + " " + ResultTypeBefore[MainType] + \
                        ":" + str(slResultTypeStrength) + ") of "
                    TypePositives = ResultTypePositives[MainType]
                    #TypeNegatives = ResultTypeNegatives[MainType]

                # Our main prompt composed of all the selected elements
                MainPositive = AllMovements + TypeFront + FinalResultExecution + FinalResultMood + TempText + \
                    AllArtists + TypePositives + \
                    FinalResultColor + Preset[ddPreset]

                    for y in range(SubSequentialPromptCount):
                        copy_p = copy.copy(p)

                        if copy_p.seed != -1:  # and "p.seed" in locals():
                            copy_p.seed += SeedStep

                        MainNegative = copy_p.negative_prompt

                        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                        #for z in range(SubSequentialPromptCount):
                            # Copy of the main prompt module to make batches, I guess...

                        # Replace [Y] with SubTempText if available, and increment YChoice
                        if SubLineCount > 0 and len(SubBatchLines[YChoice % SubLineCount]) > 0:
                            TempVariable = SubBatchLines[YChoice % SubLineCount]

                        TempText = MainPositive.replace("[Y]", " " + TempVariable + " ").replace("[y]", " " + TempVariable + " ")
                        YChoice += 1

                        # Replace the random 
                        TempText = replace_keywords_with_random_terms(TempText, RandomLinesA, r"(?i)\[A\]")
                        TempText = replace_keywords_with_random_terms(TempText, RandomLinesB, r"(?i)\[B\]")
                        TempText = replace_keywords_with_random_terms(TempText, RandomLinesC, r"(?i)\[C\]")
                        TempText = replace_keywords_with_random_terms(TempText, RandomLinesD, r"(?i)\[D\]")
                        TempText = replace_keywords_with_random_terms(TempText, RandomLinesE, r"(?i)\[E\]")
                        TempText = replace_keywords_with_random_terms(TempText, RandomLinesF, r"(?i)\[F\]")

                        TempText = replace_keywords_with_random_terms(TempText, ElementConcept, r"(?i)\[CONCEPT\]")
                        TempText = replace_keywords_with_random_terms(TempText, ResultNames, r"(?i)\[TYPE\]")
                        TempText = replace_keywords_with_random_terms(TempText, ResultExecutionList, r"(?i)\[RESULT\]")
                        TempText = replace_keywords_with_random_terms(TempText, ResultMoodList, r"(?i)\[MOOD\]")
                        TempText = replace_keywords_with_random_terms(TempText, ResultColorList, r"(?i)\[COLOR\]")
                        TempText = replace_keywords_with_random_terms(TempText, ResultArtistList, r"(?i)\[ARTIST\]")
                        TempText = replace_keywords_with_random_terms(TempText, ArtMovementList, r"(?i)\[MOVEMENT\]")

                        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                    # Clean up positive prompt
                    TempText = " ".join(TempText.split())
                    TempText = TempText.replace(",,", ",")
                    TempText = TempText.replace(" ,", ",")
                    TempText = TempText.replace(",", ",")
                    TempText = TempText.replace("( ", "(")
                    TempText = TempText.replace(" )", ")")
                    TempText = TempText.strip(",")
                    TempText = TempText.strip()

                    copy_p.prompt = TempText

                        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                    # Clean up negative prompt
                    TempText = MainNegative + TypeNegatives + \
                        AlwaysBad + PresetNegatives[ddPreset]

                    TempText = " ".join(TempText.split())
                    TempText = " ".join(TempText.split())
                    TempText = TempText.replace(",,", ",")
                    TempText = TempText.replace(" ,", ",")
                    TempText = TempText.replace(",", ",")
                    TempText = TempText.replace("( ", "(")
                    TempText = TempText.replace(" )", ")")
                    TempText = TempText.strip(",")
                    TempText = TempText.strip()

                    copy_p.negative_prompt = TempText

                    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->
                    # Add information in command prompt window and process the image

                        if state.skipped == False and state.interrupted == False:
                            if sl_auto_adjust_strength > 0:
                                copy_p.steps += calculate_value(auto_step_scale,sl_auto_adjust_strength)
                                copy_p.cfg_scale += calculate_value(auto_cfg_scale,sl_auto_adjust_strength)
                                print(f"[Automagic level: {sl_auto_adjust_strength}] [Auto steps: {copy_p.steps}] [Auto Config scale: {copy_p.cfg_scale}]")
                            print(f"[{JobCounter}/{TotalJobCounter}] [Batch count {a+1}/{UserBatchCount}] [Batch size {b+1}/{UserBatchSize}] [[X] prompt {x+1}/{SequentialPromptCount}] [[Y] prompt {y+1}/{SubSequentialPromptCount}] [Seed {int(copy_p.seed)}]\n>>> Positives <<< {copy_p.prompt}\n>>> Negatives <<< {copy_p.negative_prompt}\n")
                        
                        JobCounter += 1

                        proc = process_images(copy_p)
                        infotexts += proc.infotexts
                        images += proc.images
                        seeds.append(proc.seed)
                        prompts.append(proc.prompt)

                SeedStep += 1

        p.batch_size = UserBatchCount * SequentialPromptCount  
        p.n_iter = SubSequentialPromptCount

        return Processed(p=p, images_list=images, seed=p.seed, all_seeds=seeds, all_prompts=prompts, info=infotexts[0], infotexts=infotexts)