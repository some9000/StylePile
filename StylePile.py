# A simple helper script for AUTOMATIC1111/stable-diffusion-webui.
# Enter your keywords and let the selections help you determine the look.
# https://replicate.com/methexis-inc/img2prompt has been an incredible help for improving the prompts.
# https://docs.google.com/document/d/1ZtNwY1PragKITY0F4R-f8CarwHojc9Wrf37d0NONHDg/ has been equally super important.
# Huge thanks to https://github.com/xram64 for helping fix the interface

# Portrait prompt - Portrait of an attractive young lady,flower field background, [X], square ratio
# Neagative - missing limbs, extra limbs, watermark,label,text
# Landscape prompt - Small house in the middle of a forest,near a lake
# Action prompt - Astronaut floating in space,firing laser at alien ship,galaxy background

# Negatives - watermark,label,text

# 20 steps on Euler A
# Seed - 666

import copy

import modules.scripts as scripts
import gradio as gr

import os
from os.path import isfile,join
from os import listdir

from os import path
from modules.paths import script_path
from modules.shared import opts,cmd_opts,state

from modules.processing import process_images,Processed

import random

BeforeResultType = {
    "Not set":"",
    "Photography":"High quality Professional Photo",
    "Digital Artwork":"Digital Artwork",
    "3D Rendering":"Professional 3D rendering",
    "Painting":"Painting",
    "Drawing":"Drawing",
    "Vector Art":"Vector illustration"
}

ResultType = {
    "Not set":"",
    "Photography":",8K,highly detailed,Sharp,Photo-realism,Professional photograph,Masterpiece",
    "Digital Artwork":",highly detailed,featured on CGSociety,trending on ArtStation",
    "3D Rendering":",highly detailed,Art by senior Artist,Polycount,trending on CGSociety,trending on ArtStation",
    "Painting":"",
    "Drawing":"",
    "Vector Art":",detailed,Flat style,Illustration,Unsplash,Behance,icons8"
}

ResultTypeNegatives = {
    "Not set":"",
    "Photography":",Out of focus,Wedding,Frame,Painting,tumblr",
    "Digital Artwork":",3D rendering,Screenshot,Software,UI",
    "3D Rendering":",((Wireframe)),Polygons,Screenshot,Software,UI",
    "Painting":",((Photography)),(frame)",
    "Drawing":",Photography,Artifacts,Table,Paper,Pencils,Pages,Wall",
    "Vector Art":",Photography,Artifacts,Table,Paper,Pencils,Pages"
}

ResultMood = {
    "Not set":"",
    "Amusing":" (Amusing:1.33) ",
    "Angry":" (Angry:1.33) ",
    "Cosy":" (Cosy:1.33) ",
    "Depressing":" (Depressing:1.33) ",
    "Disgusting":" (Disgusting:1.33) ",
    "Embarrassing":" (Embarrassing:1.33) ",
    "Energetic":" (Energetic:1.33) ",
    "Evil":" (Evil:1.33) ",
    "Fearful":" (Fearful:1.33) ",
    "Frightening":" (Frightening:1.33) ",
    "Grim":" (Grim:1.33) ",
    "Guilty":" (Guilty:1.33) ",
    "Happy":" (Happy:1.33) ",
    "Hopeful":" (Hopeful:1.33) ",
    "Hopeless":" (Hopeless:1.33) ",
    "Lonely":" (Lonely:1.33) ",
    "Lustful":" (Lustful:1.33) ",
    "Peaceful":" (Peaceful:1.33) ",
    "Proud":" (Proud:1.33) ",
    "Relieving":" (Relieving:1.33) ",
    "Romantic":" (Romantic:1.33) ",
    "Sad":" (Sad:1.33) ",
    "Satisfying":" (Satisfying:1.33) ",
    "Shameful":" (Shameful:1.33) ",
    "Surprising":" (Surprising:1.33) "
}

Artists= {
    "Not set":"",
    "Aboudia":"by Artist Aboudia",
    "Adi Granov":"by Artist Adi Granov",
    "Akihiko Yoshida":"by Artist Akihiko Yoshida",
    "Al Williamson":"by Artist Al Williamson",
    "Albert Lynch":"by Artist Albert Lynch",
    "Alex Grey":"by Artist Alex Grey",
    "Alex Ross":"by Artist Alex Ross",
    "Alex Toth":"by Artist Alex Toth",
    "Alexander Jansson":"by Artist Alexander Jansson",
    "Alphonse Mucha":"by Artist Alphonse Mucha",
    "Andrew Loomis":"by Artist Andrew Loomis",
    "Artgerm":"by Artist Artgerm",
    "Babajide Olatunji":"by Artist Babajide Olatunji",
    "Barbara Kruger":"by Artist Barbara Kruger",
    "Beeple":"by Artist Beeple",
    "Bob Byerley":"by Artist Bob Byerley",
    "Bob Eggleton":"by Artist Bob Eggleton",
    "Bob Peak":"by Artist Bob Peak",
    "Boris Vallejo":"by Artist Boris Vallejo",
    "Carmine Infantino":"by Artist Carmine Infantino",
    "Caspar David Friedrich":"by Artist Caspar David Friedrich",
    "Charlie Bowater":"by Artist Charlie Bowater",
    "Chris Foss":"by Artist Chris Foss",
    "Clive Barker":"by Artist Clive Barker",
    "Coles Phillips":"by Artist Coles Phillips",
    "Curt Swan":"by Artist Curt Swan",
    "Dan Mumford":"by Artist Dan Mumford",
    "Diego Rivera":"by Artist Diego Rivera",
    "Donato Giancola":"by Artist Donato Giancola",
    "Dorina Costras":"by Artist Dorina Costras",
    "Edith Head":"by Artist Edith Head",
    "Edmund Dulac":"by Artist Edmund Dulac",
    "Edvard Munch":"by Artist Edvard Munch",
    "Erin Hanson":"by Artist Erin Hanson",
    "Esao Andrews":"by Artist Esao Andrews",
    "Esteban Maroto":"by Artist Esteban Maroto",
    "Eyvind Earle":"by Artist Eyvind Earle",
    "Fujishima Takeji":"by Artist Fujishima Takeji",
    "Gediminas Pranckevicius":"by Artist Gediminas Pranckevicius",
    "Gene Colan":"by Artist Gene Colan",
    "Georgy Kurasov":"by Artist Georgy Kurasov",
    "Gil Elvgren":"by Artist Gil Elvgren",
    "Gil Kane":"by Artist Gil Kane",
    "Greg Manchess":"by Artist Greg Manchess",
    "Greg Rutkowski":"by Artist Greg Rutkowski",
    "Gustave Doré":"by Artist Gustave Doré",
    "H.P. Lovecraft":"by Artist H.P. Lovecraft",
    "H.R. Giger":"by Artist H.R. Giger",
    "Henry Clive":"by Artist Henry Clive",
    "Hiroshi Nagai":"by Artist Hiroshi Nagai",
    "Hsiao-Ron Cheng":"by Artist Hsiao-Ron Cheng",
    "Huang Guangjian":"by Artist Huang Guangjian",
    "Ilya Kuvshinov":"by Artist Ilya Kuvshinov",
    "J.C. Leyendecker":"by Artist J.C. Leyendecker",
    "Jack Kirby":"by Artist Jack Kirby",
    "Jackson Pollock":"by Artist Jackson Pollock",
    "James Gilleard":"by Artist James Gilleard",
    "James Gurney":"by Artist James Gurney",
    "James Jean":"by Artist James Jean",
    "Jason Chan":"by Artist Jason Chan",
    "Jason Edmiston":"by Artist Jason Edmiston",
    "Jeremy Lipking":"by Artist Jeremy Lipking",
    "Jian Chong Min":"by Artist Jian Chong Min",
    "Jim Burns":"by Artist Jim Burns",
    "Joao Ruas":"by Artist Joao Ruas",
    "Joe Kubert":"by Artist Joe Kubert",
    "John Romita Jr":"by Artist John Romita Jr",
    "Joseph Leyendecker":"by Artist Joseph Leyendecker",
    "Junji Ito":"by Artist Junji Ito",
    "Kadir Nelson":"by Artist Kadir Nelson",
    "Kawase Hasui":"by Artist Kawase Hasui",
    "Kehinde Wiley":"by Artist Kehinde Wiley",
    "Koho Shoda":"by Artist Koho Shoda",
    "Krenz CushArt":"by Artist Krenz CushArt",
    "Leonid Afremov":"by Artist Leonid Afremov",
    "Lisa Frank":"by Artist Lisa Frank",
    "Loish":"by Artist Loish",
    "M.C. Escher":"by Artist M.C. Escher",
    "Madhvi Parekh":"by Artist Madhvi Parekh",
    "Makoto Shinkai":"by Artist Makoto Shinkai",
    "Marc Chagall":"by Artist Marc Chagall",
    "Marc Simonetti":"by Artist Marc Simonetti",
    "Masamune Shirow":"by Artist Masamune Shirow",
    "Miho Hirano":"by Artist Miho Hirano",
    "Mort Kunstler":"by Artist Mort Kunstler",
    "Njideka Akunyili Crosby":"by Artist Njideka Akunyili Crosby",
    "Norman Rockwell":"by Artist Norman Rockwell",
    "Pang Xunqin":"by Artist Pang Xunqin",
    "Paul Signac":"by Artist Paul Signac",
    "Peter Elson":"by Artist Peter Elson",
    "Peter Mohrbacher":"by Artist Peter Mohrbacher",
    "Phil Noto":"by Artist Phil Noto",
    "Raymond Swanland":"by Artist Raymond Swanland",
    "Rene Magritte":"by Artist Rene Magritte",
    "Rhads":"by Artist Rhads",
    "Richard Corben":"by Artist Richard Corben",
    "Rob Gonsalves":"by Artist Rob Gonsalves",
    "Robert McCall":"by Artist Robert McCall",
    "Romero Britto":"by Artist Romero Britto",
    "RossDraws":"by Artist RossDraws",
    "Ruan Jia":"by Artist Ruan Jia",
    "Ryan Pancoast":"by Artist Ryan Pancoast",
    "Sachin Teng":"by Artist Sachin Teng",
    "Salvador Dali":"by Artist Salvador Dali",
    "Sam Gilliam":"by Artist Sam Gilliam",
    "Scott Listfield":"by Artist Scott Listfield",
    "Shane Turner":"by Artist Shane Turner",
    "Simon Stalenhag":"by Artist Simon Stalenhag",
    "Stephan Martinière":"by Artist Stephan Martinière",
    "Steve Ditko":"by Artist Steve Ditko",
    "Syd Mead":"by Artist Syd Mead",
    "Takashi Murakami":"by Artist Takashi Murakami",
    "Tara McPherson":"by Artist Tara McPherson",
    "Tarsila do Amaral":"by Artist Tarsila do Amaral",
    "Ted Nasmith":"by Artist Ted Nasmith",
    "Thomas Blackshear":"by Artist Thomas Blackshear",
    "Thomas Kinkade":"by Artist Thomas Kinkade",
    "Tom Bagshaw":"by Artist Tom Bagshaw",
    "Tom Lovell":"by Artist Tom Lovell",
    "Tomasz Alen":"by Artist Tomasz Alen",
    "Toshi Yoshida":"by Artist Toshi Yoshida",
    "Trina Robbins":"by Artist Trina Robbins",
    "Tsutomu Nihei":"by Artist Tsutomu Nihei",
    "Victo Ngai":"by Artist Victo Ngai",
    "Vincent DiFate":"by Artist Vincent DiFate",
    "Wadim Kashin":"by Artist Wadim Kashin",
    "Walter Crane":"by Artist Walter Crane",
    "Wangechi Mutu":"by Artist Wangechi Mutu",
    "Wayne Barlowe":"by Artist Wayne Barlowe",
    "Will Barnet":"by Artist Will Barnet",
    "William Dodge":"by Artist William Dodge",
    "WLOP":"by Artist WLOP",
    "Yayoi Kusama":"by Artist Yayoi Kusama",
    "Yoji Shinkawa":"by Artist Yoji Shinkawa",
    "Yoshitaka Amano":"by Artist Yoshitaka Amano"
}

ResultStyle = {
    "Not set":"",
    "Abstract ":"Abstract Art",
    "Acidwave":"Acidwave Artwork",
    "Acrylic":"Acrylic",
    "Aestheticism ":"Aestheticism Art",
    "Anime":"Pixiv,Anime",
    "Art Deco":"Art Deco Painting",
    "Nouveau":"Art Nouveau",
    "Ashcan School Style":"Ashcan School Style",
    "Avant-garde":"Avant-garde Painting",
    "Ballpoint Pen":"Ballpoint Pen Artwork",
    "Baroque":"Baroque Painting",
    "Classicism":"Classicism",
    "CoBrA":"CoBrA Painting",
    "Colored Pencil":"Colored Pencil Drawing",
    "Constructivism":"Constructivism Painting",
    "Cubism":"Cubism",
    "Dreamcore ":"Dreamcore Art",
    "Drip":"Drip Painting",
    "Encaustic":"Encaustic Painting",
    "Expressionism":"Expressionism",
    "Fauvism":"Fauvism",
    "Finger Painting":"Finger Painting",
    "Futurism":"Futurism Painting",
    "Gothic":"Gothic Painting",
    "Gouache":"Gouache",
    "Hot Wax":"Hot Wax Painting",
    "Impressionism":"Impressionism",
    "Ink Wash":"Ink Wash",
    "Japanese":"Japanese Artwork",
    "Korean":"Korean Painting",
    "Line Art":"Line Art Drawing",
    "Linocut":"Linocut",
    "Lowpoly":"Lowpoly",
    "Manga":"Manga Painting",
    "Marker":"Marker Painting",
    "Modern Comics":"Marvel Comics Art,DC Comics Art,Image comics Art,Dark Horse Comics Art",
    "Mural":"Mural Painting",
    "Neoclassicism":"Neoclassicism",
    "Oil Painting":"Oil Painting Style",
    "Pastel":"Pastel Painting",
    "Pencil ":"Pencil Art",
    "Photorealism ":"Photorealism Art",
    "Pixel Art":"Atari graphics 16-bit Pixel Art",
    "Pop Art":"Pop Art",
    "Pop Surrealism":"Pop Surrealism",
    "Psychedelic ":"Psychedelic Art",
    "Realism":"Realism",
    "Renaissance":"Renaissance",
    "Rococo":"Rococo Painting",
    "Sprite Artwork":"Low resolution Sprite Art",
    "Street Art":"Street Art Painting",
    "Suprematism":"Suprematism",
    "Vaporwave":"Vaporwave digital Painting",
    "Vintage Comics":"Vintage Comic Art",
    "Watercolor":"Watercolor Painting",
}

ResultColors = {
    "Not set":"",
    "Primary Colors":",((primary Colors))",
    "Vivid":",((vivid Colors)),((vibrant)),((colorful))",
    "Pastel Colors":",((pastel Colors))",
    "Muted Colors":",((muted Colors))",
    "Grayscale":",((grayscale))",
    "Black and white":",((black and white))",
    "Infrared":",((infrared))"
}

ImageView = {
    "Not set":"",
    "Symmetrical":",Symmetrical",
    "Tilt-shift":",Tilt-shift lens",
    "Long shot angle":",Long shot angle",
    "Medium shot angle":",Medium shot angle",
    "Wide shot angle":",Wide shot angle",
    "Portrait":",(portrait),50mm,bokeh",
    "Extreme close-up angle":",Extreme close-up angle",
    "Macro":",Macro",
    "Microscopic":",Microscopic",
    "Isometric":",Isometric",
    "Panorama":",Panorama,360",
    "Fisheye lens":",Fisheye lens",
    "Overhead-angle":",Overhead-angle",
    "Birds eye view":",Shot from a birds eye camera angle"
}

FocusOn = {
    "No focus":"",

    "Portraits":",(close portrait:1.6),thematic background",
    "Feminine portrait":",(close portrait:1.6),(Feminine:1.6),(beautiful:1.7),(attractive:1.6),handsome,calendar pose,perfectly detailed eyes,studio lighting,thematic background",
    "Masculine portrait":",(close portrait:1.6),(Masculine:1.4),attractive,handsome,calendar pose,perfectly detailed eyes,studio lighting,thematic background",

    "WaiFusion":",close portrait,(manga:1.3),beautiful,attractive,handsome,trending on ArtStation,DeviantArt contest winner,CGSociety,ultrafine,detailed,studio lighting",

    "Horrible Monsters":",monster,ugly,surgery,evisceration,morbid,cut,open,rotten,mutilated,deformed,disfigured,malformed,missing limbs,extra limbs,bloody,slimy,goo,Richard Estes,Audrey Flack,Ralph Goings,Robert Bechtle,Tomasz Alen Kopera,H.R.Giger,Joel Boucquemont,ArtStation,DeviantArt contest winner,thematic background",

    "Robots":",robot,((cyborg)),machine,futuristic,concept Art by senior character Artist,featured on zbrush central,trending on polycount,trending on ArtStation,CGSociety,hard surface modeling",
    
    "Retrofuturism":",((retrofuturism)),(science fiction),dystopian Art,ultrafine,detailed,future tech,by Clarence Holbrook CArter,by Ed Emshwiller,CGSociety,ArtStation contest winner,trending on ArtStation,DeviantArt contest winner,Fallout",

    "Propaganda":",propaganda poster,soviet poster,sovietwave",

    "Landscapes":",naturalism,land Art,regionalism,shutterstock contest winner,trending on unsplash,featured on Flickr"
}

FocusOnNegatives = {
    "No focus":"",

    "Portraits":",distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "Feminine portrait":",distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "Masculine portrait":",distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",

    "WaiFusion":" things on face,Unnatural anatomy,strange anatomy",

    "Horrible Monsters":",(attractive),pretty,smooth,cArtoon,pixar,human",

    "Robots":",cArtoon",
    
    "Retrofuturism":",extra limbs,malformed limbs,modern",

    "Propaganda":",extra limbs,malformed limbs,modern",

    "Landscapes":"((hdr)),((terragen)),((rendering)),(high contrast)"
}

# At some point in time it looked like adding a bunch of these negative prompts helps,but now I am not so sure...
# AlwaysBad = ",((watermark)),(text),(overlays),getty images,(cropped),low quality,worst quality"
AlwaysBad = ",((watermark)),(text),(overlays),signature"

class Script(scripts.Script):
    def title(self):
        return "StylePile"

    def ui(self,is_img2img,title="StylePile"):
        file_dir = os.path.dirname(os.path.realpath("__file__"))
        ResourceDir = os.path.join(file_dir,f"scripts/StylePile/")

        with gr.Column():
            with gr.Row():
                with gr.Column():
                    cbChangeCount = gr.Checkbox(value=True,label="Set Batch count to Sequential prompt count")
                    strSequentialPrompt = gr.Textbox(lines=5,label="Sequential prompts [X]",placeholder="Insert [X] anywhere in main prompt to sequentially insert values from here.")
                    strRandomPrompt = gr.Textbox(lines=5,label="Random prompts [R]",placeholder="Insert [R] anywhere in main prompt to randomly insert values from here.")
                with gr.Column():
                    slResultTypeStrength = gr.Slider(0,2,value=2.0,step=0.1,label="Image type strength")
                    ddResultType = gr.Dropdown(list(ResultType.keys()),label="Image type",value="Not set")
                    ddResultMood = gr.Dropdown(list(ResultMood.keys()),label="Mood",value="Not set")
                    ddResultColors = gr.Dropdown(list(ResultColors.keys()),label="Colors",value="Not set")
                    ddResultView = gr.Dropdown(list(ImageView.keys()),label="View",value="Not set")
                    ddFocusOn = gr.Dropdown(list(FocusOn.keys()),label = "Focus on (unfinished)",value="No focus")
            with gr.Row():
                with gr.Column():
                    sliImageStyleStrength = gr.Slider(0,2,value=1.3,step=0.1,label="Visual style strength")
                    selResultStyle = gr.Dropdown(list(ResultStyle.keys()),label="Visual style",value="Not set")
                with gr.Column():
                    sliImageArtistStrength = gr.Slider(0,2,value=1.3,step=0.1,label="Artist influence")
                    selArtist = gr.Dropdown(list(Artists.keys()),label="Artist",value="Not set")

        with gr.Accordion(label="Examples, Help and Tips",open=False):
            with gr.Tab("Style examples") as StyleTab:         
                imVisualStyleHint = gr.Image(show_label=False,interactive=False,value=path.join(ResourceDir,"Styles.png"))

            with gr.Tab("Artist examples") as ArtistTab:
                imArtistHint = gr.Image(show_label=False,interactive=False,value=path.join(ResourceDir,"Artists.png"))

            with gr.Tab("Mood examples") as MoodTab:
                imArtistHint = gr.Image(show_label=False,interactive=False,value=path.join(ResourceDir,"Mood.png"))

            with gr.Tab("Help") as HelpTab:
                mdHelpText = gr.Markdown(
                """
                ## Hello, StylePile here
                ### Introduction
                **StylePile** is a mix and match system for adding elements to prompts that affect the style of the result. Hence the name. By default, these elements are placed in a specific order and given strength values. Which means the result sort-of evolves. I have generated thousands of images for each main **Image type** and tweaked the keywords to attempt giving expected results most of the time. Certainly, your suggestions for improvements are very welcome.
                ### Base workflow
                For example, if you select the **Painting** image type, then almost all results will look like Paintings. Selecting **Mood** will have a certain influence on the overall look in some way (if it's something humanoid it may show emotion, but also colors and overall feel may change). Setting **Colors** will change the general tonality of the result. And setting **View** will attempt to change how the subject is viewed. Attempt, because view appears to be the least reliable keyword. These elements are placed in order of influence and supported by certain strength values. These basic settings produce very quick results close to the general look you want.

                Moving on, adding a **Visual style** will combine with **Image type** to influence how the result generally looks. These styles are based on classic and modern Painting/Art/design movements (which I picked after hours and thousands of samples of testing) and can have a strong influence on the end result. Either it will be more realistic or artistic, or look like a comic book etc. In general, this is a really strong element for getting the look you want. Its influence can be adjusted with the slider above. Experiment with the values, keeping in mind that anything above 1.5 will start becoming a mess. In a similar way, but more focused, you can select an **Artist** and, of course, that will have a very visible effect on the result as well. Currently there are 135 artists, 55 art styles and 25 emotions available for selection and represented with preview images.

                Strength of these settings has been preset at 1.3, as that appears to be the golden ratio for getting good results. Sometimes very low settings have an interesting result as well. You can, and should, freely mix and match these settings to get different results. Classic Painting styles affected or affecting 3D look quite interesting. Photography can look cool with some of the brighter, more artistic styles etc. Sometimes raising CFG scale to 15,20 or more also helps to REALLY push the style onto the image.

                ### Advanced workflow
                StylePile can overtake the generation process, allowing you to generate a large amount of different results with very little extra work. There are two types of variables you can use: [X] and [R]. When you add an [X] to your prompt, it sequentially takes values from the **Sequential prompts** text area. You can have dozens of lines there and they will be processed in sequence. When you add [R] to the prompt a value from the **Random prompts** text area will be inserted in its place. By combining these a huge variety in prompts is very easy to do.

                When using this, **Batch count** will move through the prompts and **Batch size** will set how many copies with the given prompt to make. If the seed is not random, it will increase with each batch size step. Any random elements will still be picked randomly.

                ### Tips and tricks
                If you add your own Artist, I would recommend having "by Artist" in front of their name. Depending on Artist's popularity (or lack thereof) this appears to have a very tangible influence on the result.

                Parenthesis can be added to make pArts of the prompt stronger. So **((cute kitten))** will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: **((promt))**. A strength modifier value can also be used, like this **(prompt:1.1)**. To save some typing you can select the line you want to make stronger and use **Ctrl+Shift+Arrow keys up** or **down** to add these parenthesis and change the value. As you can see by default values on most sliders, 1.3 seems like a good stArting point if you want to see some impact.

                Prompts can be split like **[A|B]** to sequentially use terms, one after another on each step. For example **[cat|dog]** will produce a hybrid catdog.

                Using **[A:B:0.4]** will switch to other terms after the first one has been active for a certain percentage of steps. So **[cat:dog:0.4]** will build a cat 40% of the time and then stArt turning it into a dog. Usually this needs more steps to work properly.

                ### In conclusion
                I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute in some way*, just visit https://github.com/some9000/StylePile
                *Hey, if you have a 12Gb graphics card just laying around I'm happy to take it (:
                """)
 

        return [cbChangeCount,
            strSequentialPrompt,
            strRandomPrompt,
            slResultTypeStrength,
            ddResultType,
            ddResultMood,
            ddResultColors,
            ddResultView,
            ddFocusOn,
            sliImageStyleStrength,
            selResultStyle,
            sliImageArtistStrength,
            selArtist,
        ]

    def run(self, p,
        cbChangeCount,
        strSequentialPrompt: str,
        strRandomPrompt: str,
        slResultTypeStrength,
        ddResultType,
        ddResultMood,
        ddResultColors,
        ddResultView,
        ddFocusOn,
        sliImageStyleStrength,
        selResultStyle,
        sliImageArtistStrength,
        selArtist,
    ):
        
        # If it's all empty just exit function.
        if len(p.prompt) == 0:
            print(f"\nEmpty prompt! It helps to have at least some guidance for SD. Remember to insert an [X] or [R] into main prompt if you want to use variable values.")
            return
        
        p.do_not_save_grid = True

        # Preset the selection variables
        MainType = ""
        MainStyle = ""
        MainArtist = ""

        if BeforeResultType[ddResultType] != "":
            MainType = "(" + BeforeResultType[ddResultType] + ":" + str(slResultTypeStrength) + ") of "
        
        if ResultStyle[selResultStyle] != "":
            MainStyle = ",(" + ResultStyle[selResultStyle] + ":" + str(sliImageStyleStrength) + ")"

        if Artists[selArtist] != "":
            MainArtist = " (" + Artists[selArtist] + ":" + str(sliImageArtistStrength) + ")"

        # Batch lines present?
        BatchLines = [x.strip() for x in strSequentialPrompt.splitlines()]
        LineCount = len(BatchLines)

        # Any random lines present?
        RandomLines = [r.strip() for r in strRandomPrompt.splitlines()]

        images = []

        JobCount = p.n_iter
        IterCount = p.batch_size

        # If we have [X] variables use their amount, unless unchecked
        if cbChangeCount == True and len(strSequentialPrompt) > 0:
            JobCount = LineCount
            # Overtake amounts of things to generate so we can go through different variables
        
        p.batch_size = 1
        p.n_iter = 1

        # Boasting ;)
        print(f"\nStylePile helping you make great Art going through {JobCount} lines, {IterCount} iterations each:")

        CurrentChoice = 0
        TempText = ""

        for x in range(JobCount):
            for y in range(IterCount):
                #Copy of the main prompt module to make batches, I guess...
                copy_p = copy.copy(p)

                if p.seed != -1 and 'p.seed' in locals():
                    copy_p.seed = p.seed + y

                # If present, add batch element, otherwise remove that reference
                TempText = ""
                if LineCount > 0:
                    if len(BatchLines[CurrentChoice % LineCount]) > 0:
                        TempText = BatchLines[CurrentChoice % LineCount]
                        #TempText = str(BatchPrompts[CurrentChoice % LineCount].get('prompt'))

                TempText = copy_p.prompt.replace("[X]",TempText)

                # If present, add random element, otherwise remove that reference
                if len(RandomLines) > 0:
                    TempText = TempText.replace("[R]",random.choice(RandomLines))
                else:
                    TempText = TempText.replace("[R]","")

                # Our main prompt composed of all the selected elements
                TempText = MainType + ResultMood[ddResultMood] + TempText + MainArtist + ResultType[ddResultType] + MainStyle + ResultColors[ddResultColors] + ImageView[ddResultView] + FocusOn[ddFocusOn]

                # Clean up positive prompt
                TempText = " ".join(TempText.split())
                TempText = TempText.replace(" ,",",")
                TempText = TempText.replace(",",",")
                TempText = TempText.strip(",")
                TempText = TempText.strip()

                copy_p.prompt = TempText 

                # Clean up negative prompt
                TempText = p.negative_prompt + ResultTypeNegatives[ddResultType] + FocusOnNegatives[ddFocusOn] + AlwaysBad

                TempText = " ".join(TempText.split())
                TempText = TempText.replace(" ,",",")
                TempText = TempText.replace(",",",")
                TempText = TempText.strip(",")
                TempText = TempText.strip()

                copy_p.negative_prompt = TempText

                # Add information in command prompt window
                
                print(f"[Prompt {x+1}/{JobCount}|Iteration {y+1}/{IterCount}|Seed {copy_p.seed}] >>> Positives <<< {copy_p.prompt} >>> Negatives <<< {copy_p.negative_prompt}")

                proc = process_images(copy_p)
                images += proc.images
            CurrentChoice += 1

        p.batch_size = JobCount
        p.n_iter = IterCount
        
        return Processed(p,images,p.seed,"")
        print(f"\nStylePile processing complete. Have a nice day.")