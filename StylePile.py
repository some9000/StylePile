# A simple helper script for AUTOMATIC1111/stable-diffusion-webui.
# Enter your keywords and let the selections help you determine the look.
# https://replicate.com/methexis-inc/img2prompt has been an incredible help for improving the prompts.
# https://docs.google.com/document/d/1ZtNwY1PragKITY0F4R-f8CarwHojc9Wrf37d0NONHDg/ has been equally super important.
# Huge thanks to https://github.com/xram64 for helping fix the interface

# Portrait prompt - Portrait of an attractive young lady, flower field background
# Landscape prompt - mall house in the middle of a forest near a lake

# Negatives - watermark, label, text

# Seed - 666

import copy

import modules.scripts as scripts
import gradio as gr

from os import path
from modules.paths import script_path
from modules.shared import opts, cmd_opts, state

from modules.processing import process_images, Processed

ResultBefore = {
    "Not set":"", 
    "Photography":"High quality photo of ", 
    "Digital art":"Digital art of ", 
    "3D Rendering":"3D rendering of ", 
    "Painting":"Painting of ", 
    "Drawing":"Drawing of ", 
    "Vector art":"Vector art of "
}

ResultType = {
    "Not set":"", 
    "Photography":", 8K, Sharp, Realistic, Professional photograph, Masterpiece", 
    "Digital art":", featured on CGSociety, featured on ArtStation", 
    "3D Rendering":", art by senior artist, featured on CGSociety, featured on ArtStation, Maya 3D, ZBrush Central", 
    "Painting":"", 
    "Drawing":"", 
    "Vector art":", Unsplash, Behance"
}

ResultTypeNegatives = {
    "Not set":"", 
    "Photography":", Out of focus, Wedding photo, Frame, Painting, tumblr", 
    "Digital art":", 3D rendering, Screenshot, Software, UI", 
    "3D Rendering":", 2D art, Screenshot, Software, UI, computer screen, multiple poses, different poses", 
    "Painting":", ((Photography)), frame", 
    "Drawing":", Photography, Artifacts, Table, Paper, Pencils, Wall", 
    "Vector art":", ((Watermark)), ((Text)), Detailed, Gradients, Disproportionate, Noise"
}

ResultMood = {
    "Not set":"",
    "Happy":"happy ",
    "Sad":"sad ",
    "Frightened":"frightened ",
    "Angry":"angry ",
    "Surprised":"surprised ",
    "Disgusted":"disgusted ",
    "Embarrassed":"embarrassed ",
    "Amused":"amused ",
    "Guilty":"guilty ",
    "Proud":"proud ",
    "Ashamed":"ashamed ",
    "Relieved":"relieved ",
    "Satisfied":"satisfied ",
    "Evil":"evil ",
}

Artists= {
    "Not set":"",
    "Adi Granov":" by artist Adi Granow",
    "Akihido Yoshida":" by artist Akihido Yoshida",
    "Alex Grey":" by artist Alex Grey",
    "Alex Ross":" by artist Alex Ross",
    "Alexander Jansson":" by artist Alexander Jansson",
    "Alphonse Mucha":" by artist Alphonse Mucha",
    "Ansel Adams":" by artist Ansel Adams",
    "Artgerm":" by artist Artgerm",
    "Banksy":" by artist Banksy",
    "Beeple":" by artist Beeple",
    "Bob Eggleton":" by artist Bob Eggleton",
    "Boris Vallejo":" by artist Boris Vallejo",
    "Caspar David Friedrich":" by artist Caspar David Friedrich",
    "Chris Foss":" by artist Chris Foss",
    "Dan Mumford":" by artist Dan Mumford",
    "Donato Giancola":" by artist Donato Giancola",
    "Edvard Munch":" by artist Edvard Munch",
    "Esao Andrews":" by artist Esao Andrews",
    "Gediminas Pranckevicius":" by artist Gediminas Pranckevicius",
    "Gil Elvgren":" by artist Gil Elvgren",
    "Greg Manchess":" by artist Greg Manchess",
    "Greg Rutkowski":" by artist Greg Rutkowski",
    "Gustave Doré":" by artist Gustave Doré",
    "H.P. Lovecraft":" by artist H.P. Lovecraft",
    "H.R. Giger":" by artist H.R. Giger",
    "Huang Guangjian":" by artist Huang Guangjian",
    "Ilya Kuvshinov":" by artist Ilya Kuvshinov",
    "Irak Nadar":" by artist Irak Nadar",
    "Jack Kirby":" by artist Jack Kirby",
    "Jackson Pollock":" by artist Jackson Pollock",
    "James Gilleard":" by artist James Gilleard",
    "James Jean":" by artist James Jean",
    "Jason Chan":" by artist Jason Chan",
    "Jim Burns":" by artist Jim Burns",
    "Jim Phillips":" by artist Jim Phillips",
    "Joseph Leyendecker":" by artist Joseph Leyendecker",
    "Junji Ito":" by artist Junji Ito",
    "Lisa Frank":" by artist Lisa Frank",
    "Marc Simonetti":" by artist Marc Simonetti",
    "Makoto Shinkai":" by artist Makoto Shinkai",
    "M.C. Escher":" by artist M.C. Escher",
    "Peter Mohrbacher":" by artist Peter Mohrbacher",
    "Phil Noto":" by artist Phil Noto",
    "ROSSDRAWS":" by artist ROSSDRAWS",
    "Ruan Jia":" by artist Ruan Jia",
    "Sachin Teng":" by artist Sachin Teng",
    "Salvador Dali":" by artist Salvador Dali",
    "Shane Turner":" by artist Shane Turner",
    "Steve Ditko":" by artist Steve Ditko",
    "Ted Nasmith":" by artist Ted Nasmith",
    "Thomas Kinkade":" by artist Thomas Kinkade",
    "Tom Bagshaw":" by artist Tom Bagshaw",
    "Tomasz Alen":" by artist Tomasz Alen",
    "Victo Ngai":" by artist Victo Ngai",
    "Vincent DiFate":" by artist Vincent DiFate",
    "WLOP":" by artist WLOP",
    "Yoshitaka Amano":" by artist Yoshitaka Amano"
}

ResultStyle = {
    "Not set":"", 
    "Abstract Painting":", (((Abstract Painting)))",
    "Acrylic Painting":", (((Acrylic Painting)))",
    "Action Painting":", (((Action Painting)))",
    "Aestheticism Painting":", (((Aestheticism Painting)))",
    "Anamorphosis Painting":", (((Anamorphosis Painting)))", 
    "Anime Art":", (((Anime Art))), (((Anime Style)))",
    "Art Deco Painting":", (((Art Deco Painting)))",
    "Art nouveau Painting":", (((Art nouveau Painting)))",
    "Ashcan School Painting":", (((Ashcan School Painting)))",
    "Black and White Photography":", (((Black and White Photography)))",
    "Ballpoint Pen Drawing":", (((Ballpoint Pen Drawing)))",
    "Baroque Painting":", (((Baroque Painting)))",
    "Canvas Painting":", (((Canvas Painting)))",
    "Cartoon Painting":", (((Cartoon Painting)))",
    "Chalk Art":", (((Chalk Art)))",
    "Chinese Painting":", (((Chinese Painting)))",
    "Classicism Painting":", (((Classicism Painting)))",
    "Collage Painting":", (((Collage Painting)))",
    "Colored Pencil Drawing":", (((Colored Pencil Drawing)))",
    "Coloring Book":", (((Coloring Book Style)))",
    "Comic Book Art":", (((Comic Book Art)))",
    "Conceptual Art":", (((Conceptual Art)))",
    "Cubism Painting":", (((Cubism Painting)))",
    "Dadaism Painting":", (((Dadaism Painting)))",
    "De Stijl Painting":", (((De Stijl Painting)))",
    "Digital Painting":", (((Digital Painting)))",
    "Digital Photography":", (((Digital Photography)))",
    "Drip Painting":", (((Drip Painting)))",
    "Enamel Painting":", (((Enamel Painting)))",
    "Encaustic Painting":", (((Encaustic Painting)))",
    "Expressionism Painting":", (((Expressionism Painting)))",
    "Fauvism Style":", (((Fauvism Style)))",
    "Figurativism Painting":", (((Figurativism Painting)))",
    "Finger painting":", (((Finger painting)))",
    "Fresco Secco Painting":", (((Fresco Secco Painting)))",
    "Futurism ":", (((Futurism )))",
    "Genre Painting":", (((Genre Painting)))",
    "Glitter Glue Painting":", (((Glitter Glue Painting)))",
    "Gothic Painting":", (((Gothic Painting)))",
    "Gouache Painting":", (((Gouache Painting)))",
    "Hot Wax Painting":", (((Hot Wax Painting)))",
    "Impressionism Painting":", (((Impressionism Painting)))",
    "Ink Wash Painting":", (((Ink Wash Painting)))",
    "Japanese Painting":", (((Japanese Painting)))",
    "Korean Painting":", (((Korean Painting)))",
    "Landscape Painting":", (((Landscape Painting)))",
    "Line Art":", (((Line Art)))",
    "Linocut":", (((Linocut)))",
    "Lowpoly":", (((Lowpoly)))",
    "Marker Painting":", (((Marker Painting)))",
    "Miniature Painting":", (((Miniature Painting)))",
    "Modernism Painting":", (((Modernism Painting)))",
    "Mural Painting":", (((Mural Painting)))",
    "Oil Painting":", (((Oil Painting)))",
    "Black and White Photograph":", (((Black and White Photograph)))",
    "Pastel Painting":", (((Pastel Painting)))",
    "Pencil Drawing":", (((Pencil Drawing)))",
    "Photorealism":", (((Photorealism)))",
    "Pop Art painting":", (((Pop Art painting)))",
    "Realism":", (((Realism)))",
    "Retro Comic Book Style":", (((Retro Comic Book Style)))",
    "Reverse Glass Painting":", (((Reverse Glass Painting)))",
    "Still Life Painting":", (((Still Life Painting)))",
    "Surrealism Painting":", (((Surrealism Painting)))",
    "Tempera Painting":", (((Tempera Painting)))",
    "Velvet Painting":", (((Velvet Painting)))",
    "Watercolor Painting":", (((Watercolor Painting)))"
}

ResultColors = {
    "Not set":"", 
    "Primary colors":", ((primary colors))",
    "Vivid":", ((vivid)), ((vibrant)), ((colorful))",
    "Muted colors":", ((muted colors))",  
    "Grayscale":", ((grayscale))", 
    "Black and white":", ((black and white))", 
    "Infrared":", ((infrared))"
}

ImageView = {
    "Not set":"", 
    "Symmetrical":", symmetrical",
    "Tilt-shift":", Tilt-shift lens",
    "Long shot angle":", Long shot angle",
    "Medium shot angle":", Medium shot angle",
    "Wide shot angle":", Wide shot angle", 
    "Portrait":", (portrait), 50mm, bokeh", 
    "Extreme close-up angle":", Extreme close-up angle",
    "Macro":", macro", 
    "Microscopic":", microscopic", 
    "Isometric":", isometric", 
    "Panorama":", panorama, 360",
    "Fisheye lens":", Fisheye lens",
    "Overhead-angle":", Overhead-angle",
    "Birds eye view":", Shot from a birds eye camera angle"
}

FocusOn = {
    "No focus":"", 

    "Portraits":", portrait, two arms, two legs, 5 fingers per hand, perfect human hands, correct proportions",

    "Feminine+Attractive":", ((Feminine)), (effeminate), attractive, pretty, handsome, hypnotic, beautiful, elegant, sensual, two arms, two legs, 5 fingers per hand, perfect human hands, ideal proportions, correct proportions",

    "Masculine+Attractive":", ((Masculine)), (manly), attractive, pretty, handsome, hypnotic, rugged, buff, muscular, strong, two arms, two legs, 5 fingers per hand, perfect human hands, ideal proportions, correct proportions",

    "WaiFusion":", computer art, anime aesthetic, ((anime)), ((Feminine)), (effeminate), attractive, pretty, handsome, hypnotic, beautiful, elegant, sensual, two arms, two legs, 5 fingers per hand, perfect human hands, ideal proportions, correct proportions, ultrafine, detailed, ArtStation contest winner, trending on ArtStation, DeviantArt contest winner, HD",

    "Horrible Monsters":", monster, ugly, surgery, evisceration, morbid, cut, open, rotten, mutilated, deformed, disfigured, malformed, missing limbs, extra limbs, bloody, slimy, goo, Richard Estes, Audrey Flack, Ralph Goings, Robert Bechtle, Tomasz Alen Kopera, H.R.Giger, Joel Boucquemont, ArtStation, DeviantArt contest winner, thematic background",

    "Robots":", (((robot))), ((cyborg)), machine, futuristic, concept art by senior character artist, featured on zbrush central, trending on polycount, trending on ArtStation, CGSociety, hard surface modeling",
    
    "Retrofuturism":", ((retrofuturism)), (science fiction), dystopian art, ultrafine, detailed, future tech, by Clarence Holbrook Carter, by Ed Emshwiller, CGSociety, ArtStation contest winner, trending on ArtStation, DeviantArt contest winner, Fallout",

    "Propaganda":", propaganda poster, soviet poster, sovietwave",

    "Landscapes":", naturalism, land art, regionalism, shutterstock contest winner, trending on unsplash, featured on Flickr"
}

FocusOnNegatives = {
    "No focus":"", 

    "Portraits":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, missing arms, extra legs, missing legs, fused fingers, fused palms, coalesced fingers, broken fingers, broken fingernails, warped pupils, distorted face, fused bodyparts", 

    "Feminine+Attractive":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, extra arms, missing arms, extra legs, missing legs, fused fingers, coalesced fingers, broken fingers, broken fingernails, fused palms, warped pupils, distorted face, fused bodyparts",

    "Masculine+Attractive":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, missing arms, extra legs, missing legs, fused fingers, coalesced fingers, broken fingers, broken fingernails, fused palms, warped pupils, distorted face, fused bodyparts",

    "WaiFusion":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, missing arms, extra legs, missing legs, fused fingers, coalesced fingers, broken fingers, broken fingernails, fused palms, warped pupils, distorted face, fused bodyparts",

    "Horrible Monsters":", (attractive), pretty, smooth,cartoon, pixar, human",

    "Robots":", (((cartoon)))",
    
    "Retrofuturism":", extra limbs, malformed limbs, modern",

    "Propaganda":", extra limbs, malformed limbs, modern",

    "Landscapes":"((hdr)), ((terragen)), ((rendering)), (high contrast)"
}

# At some point in time it looked like adding a bunch of these negative prompts helps, but now I am not so sure...
AlwaysBad = ",((watermark)), (cropped), text, label, three views, two views, painting on wall, low quality, worst quality"
#AlwaysBad = ", (((cropped))), (((watermark))), ((logo)), ((barcode)), ((UI)), ((signature)), ((text)), ((label)), ((error)), ((title)), Incorrect proportions, stickers, markings, speech bubbles, lines, cropped, low quality, worst quality, artifacts"

class Script(scripts.Script):
    def title(self):
        return "StylePile"

    def ui(self, is_img2img):
        with gr.Group(): # as TabContainer:
            with gr.Tab("StylePile"):
                with gr.Row():
                    poBatchPrompt = gr.Textbox(show_label=False,placeholder="Enter multiple lines here to loop prompts, leave empty to use above prompt",lines=1)
                with gr.Row():
                    poResultType = gr.Dropdown(list(ResultType.keys()), label="Image type", value="Not set")
                    poResultMood = gr.Dropdown(list(ResultMood.keys()), label="Mood", value="Not set")
                    poResultColors = gr.Dropdown(list(ResultColors.keys()), label="Colors", value="Not set")
                    poImageView = gr.Dropdown(list(ImageView.keys()), label="View", value="Not set")
                    poFocusOn = gr.Dropdown(list(FocusOn.keys()),label = "Focus on", value="No focus")
                with gr.Row():
                    with gr.Column():
                        poResultStyle = gr.Radio(list(ResultStyle.keys()), label="Visual style", value="Not set")
                    with gr.Column():
                        poArtist = gr.Radio(list(Artists.keys()),label="Artist", value="Not set")

            with gr.Tab("Visual Style examples") as StyleTab:
                poVisualStyleHint = gr.Image(show_label=False,interactive=False,value=path.join(script_path, "scripts", "StyleGuide.png"))

            with gr.Tab("Artist examples") as ArtistTab:
                poArtistHint = gr.Image(show_label=False,interactive=False,value=path.join(script_path, "scripts", "Artists.png"))

            with gr.Tab("Help"):
                poHelpText = gr.Markdown(
                """
                ## Hello, StylePile here
                ### Introduction
                **StylePile** is basically a mix and match system for adding elements to prompts that affect the style of the result. Hence the name. By default, these elements are placed in a specific way and given strength values, so the result sort-of evolves. I have generated hundreds of images for each main **Image type** and tweaked the keywords to attempt giving expected results most of the time. Certainly, your suggestions for improvements are very welcome.
                ### Workflow
                For example, if you select the **Drawing** image type, then almost all results will look like drawings. Setting **Colors** will change the general use of color, and setting **View** will attempt to change how the subject is viewed. Attempt, because view appears to be the least reliable keyword. These elements are placed in order of influence.

                Moving on, adding a **Visual style** will affect how that drawing looks. Either it will be more realistic or artistic or look like a comic book etc. In general, this is a really strong element for getting the look you want. Beyond that, you can select an **Artist** and that will have an influence on the general look of the result. Examples of both these selections can be seen on respective tabs to the right of this one. 
                You can, and should, freely mix and match these settings to get different results. Classic painting styles affected or affecting 3D look quite interesting. If it feels like the style is too weak, raise CFG scale to 15, 20 or more.
                
                In addition you can use the Batch prompt field to have multiple lines of prompts with selected style elements processed in sequence. Try it out, it's great. The top prompt will be ignored if this is the case.
                ### Tips and tricks
                If you add your own artist, make sure to have "by artist" before their name. Depending on their popularity (or lack thereof) this appears to have a very tangible influence on the result.
                Parenthesis can be added to make parts of the prompt stronger. So **(((cute))) kitten** will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: **((promt))**. A strength modifier value can also be used, like this **(prompt:1.1)**. To save some typing you can select the line you want to make stronger and use **Ctrl+Shift+Arrow keys up** or **down** to add these parenthesis and change the value.

                Prompts can be split like **[A|B]** to sequentially use terms one after another on each step. **[cat|dog]** will produce a hybrid catdog.
                
                Using **[A:B:0.4]** will switch to other terms after the first one has been active for a certain percentage of steps. **[cat:dog:0.4]** will build a cat 40% of the time and then start turning it into a dog. This needs more steps to work properly.
                ### In conclusion
                I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute in some way, just visit https://github.com/some9000/StylePile
                """)
                
                poBatchPrompt.change(lambda tb: gr.update(lines=3) if ("\n" in tb) else gr.update(lines=2), inputs=[poBatchPrompt], outputs=[poBatchPrompt])

        return [poBatchPrompt, poResultType, poResultStyle, poResultMood, poResultColors, poImageView, poFocusOn, poArtist, poHelpText, poVisualStyleHint, poArtistHint] #, TabContainer]

    def run(self, p, poBatchPrompt: str, poResultType, poResultStyle, poResultMood, poResultColors, poImageView, poFocusOn, poArtist, poHelpText, poVisualStyleHint, poArtistHint): #, TabContainer):
        
        # Is the multiline empty?
        if not poBatchPrompt:
            # Combine all our parameters with user's prompt
            p.prompt = ResultBefore[poResultType] + ResultMood[poResultMood] + p.prompt + Artists[poArtist] + ResultType[poResultType] + ResultStyle[poResultStyle] + ResultColors[poResultColors] + ImageView[poImageView] + FocusOn[poFocusOn]

            p.negative_prompt += ResultTypeNegatives[poResultType] + FocusOnNegatives[poFocusOn] + AlwaysBad

            # Add information in command prompt window
            print(f"\nStylePile helping you make great art with:\nPositives: {p.prompt}\nNegatives: {p.negative_prompt}")
            print(f"Total elements in prompt: {p.prompt.count(',')+p.negative_prompt.count(',')}\n")

            # Process the image
            proc = process_images(p)
            return proc
        # Multiline is filled. Let's try to split the lines and process in sequence
        else:
            lines = [x.strip() for x in poBatchPrompt.splitlines()]
            lines = [x for x in lines if len(x) > 0]

            p.do_not_save_grid = True

            job_count = 0
            jobs = []

            for line in lines:
                if "--" in line:
                    try:
                        args = cmdargs(line)
                    except Exception:
                        print(f"Error parsing line [line] as commandline:", file=sys.stderr)
                        print(traceback.format_exc(), file=sys.stderr)
                        args = {"prompt": line}
                else:
                    args = {"prompt": line}

                n_iter = args.get("n_iter", 1)
                if n_iter != 1:
                    job_count += n_iter
                else:
                    job_count += 1

                jobs.append(args)

            state.job_count = job_count
            images = []

            # Boasting ;)
            print(f"\nStylePile helping you make great art going through {len(lines)} lines in {job_count} jobs:")

            for n, args in enumerate(jobs):
                state.job = f"{state.job_no + 1} out of {state.job_count}"

                copy_p = copy.copy(p)

                for k, v in args.items():
                    setattr(copy_p, k, v)

                copy_p.prompt = ResultBefore[poResultType] + ResultMood[poResultMood] + copy_p.prompt + Artists[poArtist] + ResultType[poResultType] + ResultStyle[poResultStyle] + ResultColors[poResultColors] + ImageView[poImageView] + FocusOn[poFocusOn]

                copy_p.negative_prompt += ResultTypeNegatives[poResultType] + FocusOnNegatives[poFocusOn] + AlwaysBad

                # Add information in command prompt window
                print(f"\nPositives: {copy_p.prompt}\nNegatives: {copy_p.negative_prompt}")
                # print(f"Total elements in prompt: {copy_p.prompt.count(',')+copy_p.negative_prompt.count(',')}\n")

                proc = process_images(copy_p)
                images += proc.images

            return Processed(p, images, p.seed, "")
