#                            ,,                      ,,    ,,
#   .M"""bgd mm            `7MM         `7MM"""Mq.   db  `7MM
#  ,MI    "Y MM              MM           MM   `MM.        MM
#  `MMb.   mmMMmm `7M'   `MF'MM  .gP"Ya   MM   ,M9 `7MM    MM  .gP"Ya
#    `YMMNq. MM     VA   ,V  MM ,M'   Yb  MMmmdM9    MM    MM ,M'   Yb
#  .     `MM MM      VA ,V   MM 8M""""""  MM         MM    MM 8M""""""
#  Mb     dM MM       VVV    MM YM.    ,  MM         MM    MM YM.    ,
#  P"Ybmmd"  `Mbmo    ,V   .JMML.`Mbmmd'.JMML.     .JMML..JMML.`Mbmmd'
#                    ,V
#                 OOb"
#
# A helper script for AUTOMATIC1111/stable-diffusion-webui.
# Enter your keywords and let the selections help you determine the look.
# https://replicate.com/methexis-inc/img2prompt has been an incredible help for improving the prompts.
# https://docs.google.com/document/d/1ZtNwY1PragKITY0F4R-f8CarwHojc9Wrf37d0NONHDg/ has been equally super important.
# Thanks to https://github.com/xram64 for helping fix the interface
# Art movements from https://en.wikipedia.org/wiki/List_of_art_movements I threw out the ones that did not work

# Portrait prompt - Portrait of an attractive young lady,flower field background, (by artist [X]:1.3), square ratio
# Negative - missing limbs, extra limbs

# Landscape prompt - Small house in the middle of a forest,near a lake
# Action prompt - Astronaut floating in space,firing laser at alien ship,galaxy background

# Negatives - watermark,label,text

# 20 steps on Euler A
# Seed - 669

import copy
import os
import random
from os import listdir, path
from os.path import isfile, join

import modules.scripts as scripts
import gradio as gr
from modules.processing import Processed, process_images
from modules.shared import cmd_opts, opts, state

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

file_dir = os.path.dirname(os.path.realpath("__file__"))
ResourceDir = os.path.join(file_dir, f"extensions/StylePile/StylePile/")

def FilesInFolder(SourceFolder):
    return [file for file in os.listdir(SourceFolder)]

def FilesInFolderFullPath(SourceFolder):
    return [SourceFolder + file for file in os.listdir(SourceFolder)]

ResultNames = [
    "Photography",
    "Digital Artwork",
    "3D Rendering",
    "Painting",
    "Drawing",
    "Vector Art"
]

ResultTypeBefore = {
    "Photography": "High quality Professional Photo",
    "Digital Artwork": "Digital Artwork",
    "3D Rendering": "Professional 3D rendering",
    "Painting": "Painting",
    "Drawing": "Drawing",
    "Vector Art": "Vector image"
}

ResultTypePositives = {
    "Photography": ",HD,4K,8K,highly detailed,Sharp,Photo-realism,Professional photograph,Masterpiece",
    "Digital Artwork": ",Highly Detailed,Featured on CGSociety,Trending on ArtStation",
    "3D Rendering": ",Highly detailed,Art by senior Artist,Polycount,trending on CGSociety,trending on ArtStation",
    "Painting": " ",
    "Drawing": " ",
    "Vector Art": ",(Flat style:1.3),Illustration,Behance"
}

ResultTypeNegatives = {
    "Photography": ",Amateur,Low rated,Phone,Wedding,Frame,Painting,tumblr",
    "Digital Artwork": ",Scribbles,Low quality,Low rated,Mediocre,3D rendering,Screenshot,Software,UI",
    "3D Rendering": ",((Wireframe)),Polygons,Screenshot,Character design,Software,UI",
    "Painting": "Low quality,Bad composition,Faded,(Photography:1.5),(Frame:1.3)",
    "Drawing": ",Low quality,Photography,Artifacts,Table,Paper,Pencils,Pages,Wall",
    "Vector Art": ",(Watermark:1.5),(Text:1.3)"
}

ResultType = {
    "Not set": "",
    "Random": "Random",
}

ResultType.update(ResultTypePositives)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultDirectionList = FilesInFolder(ResourceDir + "Directions/")
ResultDirectionList = list(
    map(lambda x: x.replace(".jpg", ""), ResultDirectionList))
ResultDirection = ["Not set", "Random"] + ResultDirectionList

ResultDirectionImages = FilesInFolderFullPath(ResourceDir + "Directions/")
ResultDirectionImages = list(
    map(lambda x: x.replace("\\", "/"), ResultDirectionImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultMoodList = FilesInFolder(ResourceDir + "Moods/")
ResultMoodList = list(map(lambda x: x.replace(".jpg", ""), ResultMoodList))
ResultMood = ["Not set", "Random"] + ResultMoodList

ResultMoodImages = FilesInFolderFullPath(ResourceDir + "Moods/")
ResultMoodImages = list(map(lambda x: x.replace("\\", "/"), ResultMoodImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultArtistList = FilesInFolder(ResourceDir + "Artists/")
ResultArtistList = list(map(lambda x: x.replace(".jpg", ""), ResultArtistList))
Artists = ["Not set", "Random"] + ResultArtistList

ResultArtistImages = FilesInFolderFullPath(ResourceDir + "Artists/")
ResultArtistImages = list(
    map(lambda x: x.replace("\\", "/"), ResultArtistImages))

#ResultArtistColumn = "\n".join(str(item) for item in ResultArtistList)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ArtMovementList = FilesInFolder(ResourceDir + "Art Movements/")
ArtMovementList = list(map(lambda x: x.replace(".jpg", ""), ArtMovementList))
ArtMovements = ["Not set", "Random"] + ArtMovementList

ArtMovementImages = FilesInFolderFullPath(ResourceDir + "Art Movements/")
ArtMovementImages = list(
    map(lambda x: x.replace("\\", "/"), ArtMovementImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultColorList = {
    "Not set": "",
    "Primary Colors": ",((Primary Colors))",
    "Vivid": ",((vivid Colors)),((vibrant)),((colorful))",
    "Pastel Colors": ",((pastel Colors))",
    "Muted Colors": ",((muted Colors))",
    "Grayscale": ",((grayscale))",
    "Black and white": ",((black and white))",
    "Infrared": ",((Infrared))",
    "Technicolor": ",((Technicolor))",
    "Kinemacolor": ",((Kinemacolor))",
    "Kodachrome": ",((Kodachrome))",
    "Cinecolor": ",((Cinecolor))",
    "Agfacolor": ",((Agfacolor))",
    "Velvia": ",((Velvia))",
    "Provia": ",((Provia))",
    "Fujifilm Superia": ",((Fujifilm Superia))",
    "Kodak Ektar": ",((Kodak Ektar))",
    "Kodak Portra": ",((Kodak Portra))",
    "High Contrast": ",((High Contrast))",
    "Low Contrast": ",((Low Contrast))"
}

ResultColors = {
    "Not set": "",
    "Random": "Random",
}

ResultColors.update(ResultColorList)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

TipsAndTricks = [
    "Be specific. Add details in sequence, separated by commas. Like 'Cute black kitten, yellow eyes' + selecting Photography as image type, will get you to the result you want faster than just 'black kitten'.",
    "Try out random values. For example, set artist to random, crank up the batch count and enjoy the show. Mix and match random settings.",
    "If you add your own artist, I would recommend having 'by Artist' in front of their name. Depending on their popularity (or lack thereof) this appears to have a very tangible influence on the result.",
    "Mix and match artists from the dropdowns (or type your own) for some interesting results. Having one artist selected and other(s) set to random is also a nice way to find new looks with some amount of predictability.",
    "Parenthesis can be added to make parts of the prompt stronger. So ((cute kitten)) will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: ((promt)). A strength modifier value can also be used, like this (prompt:1.1).",
    "Prompts can be split like [A|B] to sequentially use terms, one after another on each step. For example **[cat|dog]** will produce a hybrid catdog.",
    "Using **[A:B:0.4]** will switch to other terms after the first one has been active for a certain percentage of steps. So [cat:dog:0.4] will build a cat 40% of the time and then start turning it into a dog. Usually this needs more steps to work properly.",
    "During long cold winter nights, you can turn your PC into a heater by generating hundreds of images non-stop.",
    "Feel free to share feedback and ideas on github: https://github.com/some9000/StylePile",
    "Some things work together, others don't. Like Photography doesn't work too great with many Art movements or Drawing will not become photorealistic just because that was selected."
]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

Preset = {
    "None": "",
    "Portraits": ",(close portrait:1.3),thematic background",
    "Feminine portrait": ",(close portrait:1.3),(Feminine:1.4),(beautiful:1.4),(attractive:1.3),handsome,calendar pose,perfectly detailed eyes,studio lighting,thematic background",
    "Masculine portrait": ",(close portrait:1.3),(Masculine:1.4),attractive,handsome,calendar pose,perfectly detailed eyes,studio lighting,thematic background",
    "WaiFusion": ",close portrait,(manga:1.3),beautiful,attractive,handsome,trending on ArtStation,DeviantArt contest winner,CGSociety,ultrafine,detailed,studio lighting",
    "Horrible Monsters": ",monster,ugly,surgery,evisceration,morbid,cut,open,rotten,mutilated,deformed,disfigured,malformed,missing limbs,extra limbs,bloody,slimy,goo,Richard Estes,Audrey Flack,Ralph Goings,Robert Bechtle,Tomasz Alen Kopera,H.R.Giger,Joel Boucquemont,ArtStation,DeviantArt contest winner,thematic background",
    "Robots": ",robot,((cyborg)),machine,futuristic,concept Art by senior character Artist,featured on zbrush central,trending on polycount,trending on ArtStation,CGSociety,hard surface modeling",
    "Retrofuturism": ",((retrofuturism)),(science fiction),dystopian Art,ultrafine,detailed,future tech,by Clarence Holbrook CArter,by Ed Emshwiller,CGSociety,ArtStation contest winner,trending on ArtStation,DeviantArt contest winner,Fallout",
    "Propaganda": ",propaganda poster,soviet poster,sovietwave",
    "Landscapes": ",naturalism,land Art,regionalism,shutterstock contest winner,trending on unsplash,featured on Flickr"
}

PresetNegatives = {
    "None": "",
    "Portraits": ",robot eyes,distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "Feminine portrait": ",robot eyes,distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "Masculine portrait": ",robot eyes,distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "WaiFusion": ",things on face,Unnatural anatomy,strange anatomy",
    "Horrible Monsters": ",(attractive),pretty,smooth,cArtoon,pixar,human",
    "Robots": ",cartoon",
    "Retrofuturism": ",extra limbs,malformed limbs,modern",
    "Propaganda": ",extra limbs,malformed limbs,modern",
    "Landscapes": ",((hdr)),((terragen)),((rendering)),(high contrast)"
}

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

# At some point in time it looked like adding a bunch of these negative prompts helps,but now I am not so sure...
AlwaysBad = ",((watermark)),(text),(overlay),getty images,(cropped),low quality,worst quality"


class Script(scripts.Script):
    # txt2img_prompt = None
    # img2img_prompt = None

    # def after_component(self, component, **kwargs):
    #     if kwargs.get('elem_id') == 'txt2img_prompt':
    #         self.txt2img_prompt = component
    #     if kwargs.get('elem_id') == 'img2img_prompt':
    #         self.img2img_prompt = component

    #def add_test_to_prompt(prompt):
    #    return prompt + " TEST"

    def title(self):
        return "StylePile"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        # test_button = gr.Button('TEST', elem_id="txt2img_test_button")
        # if self.txt2img_prompt is not None:
        #     test_button.click(fn=lambda x: x+" TEST", 
        #         inputs  = [self.txt2img_prompt],
        #         outputs = [self.txt2img_prompt])
            
        # if self.img2img_prompt is not None:
        #     test_button.click(fn=lambda x: x+" TEST", 
        #         inputs  = [self.img2img_prompt],
        #         outputs = [self.img2img_prompt])

        with gr.Tab("Parameters"):
            with gr.Row():
                with gr.Column():
                    ddCoreResultType = gr.Dropdown(
                        list(ResultType.keys()), label="Image type", value="Not set")
                    slResultTypeStrength = gr.Slider(
                        0, 2, value=1.3, step=0.05, show_label=False)
                with gr.Column():
                    ddResultDirection = gr.Dropdown(
                        ResultDirection, label="Direction", value="Not set")
                    slResultDirectionStrength = gr.Slider(
                        0, 2, value=1.0, step=0.05, show_label=False)
                with gr.Column():
                    ddResultMood = gr.Dropdown(
                        ResultMood, label="Mood", value="Not set")
                    slResultMoodStrength = gr.Slider(
                        0, 2, value=1.3, step=0.05, show_label=False)
                with gr.Column():
                    ddResultColors = gr.Dropdown(
                        list(ResultColors.keys()), label="Colors", value="Not set")
                with gr.Row():
                    cbChangeCount = gr.Checkbox(
                        value=True, label="Batch count = Sequence count")
                    cbShowTips = gr.Checkbox(
                        value=False, label="Show tips when generating")
                    ddPreset = gr.Dropdown(list(Preset.keys()), label="Style influence (incomplete)", value="None")

            with gr.Row():
                strSequentialPrompt = gr.Textbox(
                    lines=3, label="Sequential prompts [X]", placeholder="Insert [X] anywhere in main prompt to sequentially insert values from here. Random values will be added here or to main prompt.")
            with gr.Row():
                strSubSequentialPrompt = gr.Textbox(
                    lines=3, label="SubSequential prompts [Y]", placeholder="Insert [Y] in the final prompt <== to sequentially insert values from here (and increase prompt count). This is done after all other prompts and loops through all lines.")

            with gr.Row():
                strRandomPromptA = gr.Textbox(
                    lines=3, label="Random [A]", placeholder="Insert [A] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                strRandomPromptB = gr.Textbox(
                    lines=3, label="Random [B]", placeholder="Insert [B] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                strRandomPromptC = gr.Textbox(
                    lines=3, label="Random [C]", placeholder="Insert [C] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")

            with gr.Row():
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
                    
        with gr.Tab("Directions") as StyleTab:
            gr.Gallery(value=ResultDirectionImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Moods"):
            gr.Gallery(value=ResultMoodImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Artists"):
            gr.Gallery(value=ResultArtistImages, show_label=False).style(
                grid=(2, 2, 2, 2, 3, 3), container=False)
            
        with gr.Tab("Art movements"):
            gr.Gallery(value=ArtMovementImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)
            
        with gr.Tab("Info") as HelpTab:
            gr.Markdown(
                """
            ### Example images, adding your own
            Example images stored in the script folders are more than just images. Their filenames are used to create the **Direction**, **Mood**, **Artist** and Art **movement** dropdown selections. This gives you the ability to Add/Remove parameters as you wish. Just place an image in the folder and name it as the option you want to see in the dropdown. Delete image file to remove that option.
            
            In case you would like to suggest an artist be added to the roster, I would recommend making 8+ sample images first. To see if SD actually "knows" that artist and their style appears unique enough. The portraits you can see in the info pages were generated with the following settings:
            
            ### Sample portrait prompt
            Positive: Portrait of an attractive young lady,flower field background,(by [X]:1.3), square ratio
            Negative - missing limbs, extra limbs, watermark,label,text

            [X] is **Artist Name Surname** From my research adding **Artist** can really help to get the correct look.

            20 steps on Euler A
            Seed - 669 - batch of 4 images

            Generally that produces a fairly nice portrait with enough room to show off the given style. Do compare the results to the actual style. As SD will produce something it 'thinks' may be correct based on their name (guessing nationality, basing it on something that has mentioned a similar name etc) and that influences the results, but not in a good way.
            """)
            
        #with gr.Tab("Values"):
        #    with gr.Row():
        #        gr.Markdown("""Here you can copy all the available Directions, Moods, Artists or Styles in case you want to try out all the possible values. Just copy and paste into the X or Y fields, insert [X] or [Y] into your main prompt and enjoy the show.""")
        #    with gr.Row():
        #        gr.Textbox(label="Direction", value="Insert [X] anywhere in main prompt to sequentially insert values from here. Random values will be added here or to main prompt.")
        #        gr.Textbox(label="Mood", value="Hmmm")
        #        gr.Textbox(label="Artists", value=ResultArtistColumn)
        #        gr.Textbox(label="Styles", value="\n".join(str(item) for item in ArtMovementList))  
                
        with gr.Tab("Help"):
            gr.Markdown(
                """
            ## Hello, StylePile here
            ### Introduction
            **StylePile** is a mix and match system for adding elements to prompts that affect the style of the result. Hence the name. By default, these elements are placed in a specific order and given strength values. Which means the result sort-of evolves. I have generated thousands of images for each main **Image type** and tweaked the keywords to attempt giving expected results most of the time. Certainly, your suggestions for improvements are very welcome.
            ### Base workflow
            You select extra settings in this script and then hit the standard orange **Generate** button to get results.
            
            For example, if you select the **Painting** image type, then almost all results will look like Paintings. Selecting **Mood** will have a certain influence on the overall look in some way (if it's something humanoid it may show emotion, but also colors and overall feel may change). Setting **Colors** will change the general tonality of the result. And setting **View** will attempt to change how the subject is viewed. Attempt, because view appears to be the least reliable keyword. These elements are placed in order of influence and supported by certain strength values. These basic settings produce very quick results close to the general look you want.
            ![]({path.join(ResourceDir,"Artists.jpg") ''})
            Moving on, adding a **Art movement** will combine with **Image type** to influence how the result generally looks. These styles are based on classic and modern Painting/Art/design movements (which I picked after hours and thousands of samples of testing) and can have a strong influence on the end result. Either it will be more realistic or artistic, or look like a comic book etc. In general, this is a really strong element for getting the look you want. Its influence can be adjusted with the slider above. Experiment with the values, keeping in mind that anything above 1.5 will start becoming a mess. In a similar way, but more focused, you can select an **Artist** and, of course, that will have a very visible effect on the result as well. Currently there are 135 artists, 55 art styles and 25 emotions available for selection and represented with preview images.

            Strength of these settings has been preset at 1.3, as that appears to be the golden ratio for getting good results. Sometimes very low settings have an interesting result as well. You can, and should, freely mix and match these settings to get different results. Classic Painting styles affected or affecting 3D look quite interesting. Photography can look cool with some of the brighter, more artistic styles etc. Sometimes raising CFG scale to 15,20 or more also helps to REALLY push the style onto the image.

            ### Advanced workflow
            StylePile can overtake the generation process, allowing you to generate a large amount of different results with very little extra work. There are two types of variables you can use: [X] and [R]. When you add an [X] to your prompt, it sequentially takes values from the **Sequential prompts** text area. You can have dozens of lines there and they will be processed in sequence. When you add [R] to the prompt a value from the **Random** text area will be inserted in its place. By combining these a huge variety in prompts is very easy to do.

            When using this, **Batch count** will move through the prompts and **Batch size** will set how many copies with the given prompt to make. If the seed is not random, it will increase with each batch size step. Any random elements will still be picked randomly.

            ### Tips and tricks
            If you add your own Artist, I would recommend having "by Artist" in front of their name. Depending on their popularity (or lack thereof) this appears to have a very tangible influence on the result.

            Parenthesis can be added to make parts of the prompt stronger. So **((cute kitten))** will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: **((promt))**. A strength modifier value can also be used, like this **(prompt:1.1)**. To save some typing you can select the line you want to make stronger and use **Ctrl+Shift+Arrow keys up** or **down** to add these parenthesis and change the value. As you can see by default values on most sliders, 1.3 seems like a good stArting point if you want to see some impact.

            Prompts can be split like **[A|B]** to sequentially use terms, one after another on each step. For example **[cat|dog]** will produce a hybrid catdog.

            Using **[A:B:0.4]** will switch to other terms after the first one has been active for a certain percentage of steps. So **[cat:robot:0.4]** will build a cat 40% of the time and then start turning it into a robot. Usually this needs more steps to work properly.

            ### In conclusion
            I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute in some way*, just visit https://github.com/some9000/StylePile
            *Hey, if you have a 12Gb graphics card just laying around I'm happy to take it (:
            """)

        return [cbChangeCount,
                strSequentialPrompt,
                strSubSequentialPrompt,
                strRandomPromptA,
                strRandomPromptB,
                strRandomPromptC,
                slResultTypeStrength,
                ddCoreResultType,
                ddResultDirection,
                slResultDirectionStrength,
                ddResultMood,
                slResultMoodStrength,
                ddResultColors,
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
                cbShowTips,
                ddPreset
                ]

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

    def run(self, p,
            cbChangeCount,
            strSequentialPrompt: str,
            strSubSequentialPrompt: str,
            strRandomPromptA: str,
            strRandomPromptB: str,
            strRandomPromptC: str,
            slResultTypeStrength,
            ddCoreResultType,
            ddResultDirection,
            slResultDirectionStrength,
            ddResultMood,
            slResultMoodStrength,
            ddResultColors,
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
            cbShowTips,
            ddPreset
            ):

        # If it's all empty just exit function.
        if len(p.prompt) == 0:
            print(
                f"\nEmpty prompt! It helps to have at least some guidance for SD. Remember to insert an [X], [A] or [B] into main prompt if you want to use variable values.")
            return

        # Batch lines present?
        BatchLines = [x.strip() for x in strSequentialPrompt.splitlines()]
        LineCount = len(BatchLines)

        SubBatchLines = [x.strip()
                         for x in strSubSequentialPrompt.splitlines()]
        SubLineCount = len(SubBatchLines)

        TempText = ""
        SubTempText = ""

        images = []
        infotexts = []

        # Overtake amounts of things to generate so we can go through different variables
        JobCount = p.n_iter
        p.n_iter = 1

        IterCount = p.batch_size
        p.batch_size = 1

        # If we have [X] variables use their amount, unless unchecked
        if cbChangeCount == True and len(strSequentialPrompt) > 0:
            JobCount = LineCount

        SubCycleCount = 1

        if SubLineCount > 0:
            SubCycleCount = SubLineCount

        # Any random lines present?
        RandomLinesA = [r.strip() for r in strRandomPromptA.splitlines()]
        RandomLinesB = [r.strip() for r in strRandomPromptB.splitlines()]
        RandomLinesC = [r.strip() for r in strRandomPromptC.splitlines()]

        # So the progress bar works correctly
        state.job_count = JobCount * IterCount * SubCycleCount

        CurrentChoice = 0
        SubCurrentChoice = 0

        FinalResultDirection = ""

        for x in range(JobCount):
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
                    AllMovements += ",(" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthA) + ")"
                else:
                    AllMovements += ",(" + selArtMovementA + ":" + str(selArtMovementStrengthA) + ")"

            if selArtMovementB != "Not set":
                if selArtMovementB == "Random":
                    AllMovements += ",(" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthB) + ")"
                else:
                    AllMovements += ",(" + selArtMovementB + ":" + str(selArtMovementStrengthB) + ")"

            if selArtMovementC != "Not set":
                if ArtMovements[selArtMovementC] == "Random":
                    AllMovements += ",(" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthC) + ")"
                else:
                    AllMovements += ",(" + selArtMovementC + ":" + str(selArtMovementStrengthC) + ")"

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            for y in range(IterCount):

                # Copy of the main prompt module to make batches, I guess...
                #copy_p = copy.copy(p)

                #if copy_p.seed != -1:  # and 'p.seed' in locals():
                #    copy_p.seed += SeedStep
                #    SeedStep += 1

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # Clear the variables so random selection can work
                FinalResultMood = ""
                FinalResultColors = ""

                # Preset the selection variables
                MainType = ""

                TypeFront = ""
                TypePositives = ""
                TypeNegatives = ""

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # If main prompt isn't empty...
                if ResultType[ddCoreResultType] != "":
                    # If it is random, give it a random value
                    if ResultType[ddCoreResultType] == "Random":
                        MainType = random.choice(ResultNames)
                    # otherwise use the selected value
                    else:
                        MainType = ddCoreResultType

                    # Format our variables to merge into positive prompt...
                    TypeFront = "(" + ResultTypeBefore[MainType] + \
                        ":" + str(slResultTypeStrength) + ") of "
                    TypePositives = ResultTypePositives[MainType]
                    TypeNegatives = ResultTypeNegatives[MainType]

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                if ddResultDirection != "Not set":
                    if ddResultDirection == "Random":
                        FinalResultDirection = " (" + random.choice(
                            ResultDirectionList) + ":" + str(slResultDirectionStrength) + ") "
                    else:
                        FinalResultDirection = " (" + ddResultDirection + \
                            ":" + str(slResultDirectionStrength) + ") "

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # Pick the mood
                if ddResultMood != "Not set":
                    if ddResultMood == "Random":
                        FinalResultMood = ",(" + random.choice(ResultMoodList) + \
                            ":" + str(slResultMoodStrength) + ") "
                    else:
                        FinalResultMood = ",(" + ddResultMood + \
                            ":" + str(slResultMoodStrength) + ") "

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # If present, add batch element, otherwise remove that reference
                TempText = ""
                if LineCount > 0:
                    if len(BatchLines[CurrentChoice % LineCount]) > 0:
                        TempText = BatchLines[CurrentChoice % LineCount]

                #TempText = copy_p.prompt.replace("[X]", TempText)
                TempText = p.prompt.replace("[X]", TempText)

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # If present, add random element, otherwise remove that reference
                if len(RandomLinesA) > 0:
                    TempText = TempText.replace(
                        "[A]", random.choice(RandomLinesA))
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

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # Colors
                if ResultColors[ddResultColors] == "Random":
                    FinalResultColors = random.choice(
                        list(ResultColorList.values()))
                else:
                    FinalResultColors = ResultColors[ddResultColors]

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # Our main prompt composed of all the selected elements
                MainPositive = TypeFront + FinalResultDirection + FinalResultMood + TempText + \
                    AllArtists + TypePositives + AllMovements + \
                    FinalResultColors + Preset[ddPreset]

                #MainNegative = copy_p.negative_prompt
                MainNegative = p.negative_prompt

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                for z in range(SubCycleCount):
                    # Copy of the main prompt module to make batches, I guess...
                    copy_p = copy.copy(p)

                    if copy_p.seed != -1:  # and 'p.seed' in locals():
                        copy_p.seed += SeedStep

                    SubTempText = ""
                    if SubLineCount > 0:
                        if len(SubBatchLines[SubCurrentChoice % SubLineCount]) > 0:
                            SubTempText = SubBatchLines[SubCurrentChoice %
                                                        SubLineCount]

                    TempText = MainPositive.replace("[Y]", SubTempText)

                    # Clean up positive prompt
                    TempText = " ".join(TempText.split())
                    TempText = TempText.replace(",,", ",")
                    TempText = TempText.replace(" ,", ",")
                    TempText = TempText.replace(",", ",")
                    TempText = TempText.strip(",")
                    TempText = TempText.strip()

                    copy_p.prompt = TempText

                    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                    # Clean up negative prompt
                    TempText = MainNegative + TypeNegatives + \
                        AlwaysBad + PresetNegatives[ddPreset]

                    TempText = " ".join(TempText.split())
                    TempText = TempText.replace(",,", ",")
                    TempText = TempText.replace(" ,", ",")
                    TempText = TempText.replace(",", ",")
                    TempText = TempText.strip(",")
                    TempText = TempText.strip()

                    copy_p.negative_prompt = TempText

                    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->
                    # Add information in command prompt window and process the image

                    print(f"\n\n[Prompt {x+1}/{JobCount}][Iteration {y+1}/{IterCount}][SubPrompt {z}/{SubLineCount} {SubTempText}][Seed {int(copy_p.seed)}] >>> Positives <<< {copy_p.prompt} >>> Negatives <<< {copy_p.negative_prompt}\n")

                    proc = process_images(copy_p)
                    infotexts += proc.infotexts
                    images += proc.images

                    SubCurrentChoice += 1
            
            SeedStep += 1
            CurrentChoice += 1

        p.batch_size = JobCount
        p.n_iter = IterCount

        if cbShowTips:
            print(
                f"\n\nStylePile processing complete. Here's a random tip:\n{random.choice(TipsAndTricks)}\n")

        return Processed(p=p, images_list=images, seed=p.seed, info=infotexts[0], infotexts=infotexts)
