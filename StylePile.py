# A simple helper script for AUTOMATIC1111/stable-diffusion-webui.
# Enter your keywords and let the selections help you determine the look.
# https://replicate.com/methexis-inc/img2prompt has been an incredible help for improving the prompts.
# https://docs.google.com/document/d/1ZtNwY1PragKITY0F4R-f8CarwHojc9Wrf37d0NONHDg/ has been equally super important.
# Huge thanks to https://github.com/xram64 for helping fix the interface

import modules.scripts as scripts
import gradio as gr
from os import path
from modules.paths import script_path

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
    "Digital art":", featured on cgsociety, featured on artstation", 
    "3D Rendering":", art by senior artist, featured on cgsociety, featured on artstation", 
    "Painting":"", 
    "Drawing":"", 
    "Vector art":", Unsplash, Behance"
}

ResultTypeNegatives = {
    "Not set":"", 
    "Photography":", Out of focus, Wedding photo, Frame, Painting, tumblr", 
    "Digital art":", 3D rendering", 
    "3D Rendering":", 2D art", 
    "Painting":", ((Photography)), frame", 
    "Drawing":", Photography, Artifacts, Table, Paper, Pencils, Wall", 
    "Vector art":", ((Watermark)), ((Text)), Detailed, Gradients, Disproportionate, Noise"
}

Artists= {
    "Not set":"",
    "Alex Grey":" by Alex Grey",
    "Alexander Jansson":" by Alexander Jansson",
    "Alphonse Mucha":" by Alphonse Mucha",
    "Ansel Adams":" by Ansel Adams",
    "Banksy":" by Banksy",
    "Beeple":" by Beeple",
    "Bob Eggleton":" by Bob Eggleton",
    "Caspar David Friedrich":" by Caspar David Friedrich",
    "Chris Foss":" by Chris Foss",
    "Dan Mumford":" by Dan Mumford",
    "Edvard Munch":"by Edvard Munch",
    "Esao Andrews":" by Esao Andrews",
    "Gediminas Pranckevicius":" by Gediminas Pranckevicius",
    "Greg Rutkowski":" by Greg Rutkowski",
    "Gustave Doré":" by Gustave Doré",
    "H.R. Giger":" by H.R. Giger",
    "H.P. Lovecraft":" by H.P. Lovecraft",
    "Jackson Pollock":" by Jackson Pollock",
    "James Jean":" by James Jean",
    "Jim Burns":" by Jim Burns",
    "Lisa Frank":" by Lisa Frank",
    "M.C. Escher":" by M.C. Escher",
    "Marc Simonetti":" by Marc Simonetti",
    "Peter Mohrbacher":" by Peter Mohrbacher",
    "Salvador Dali":"by Salvador Dali",
    "Ted Nasmith":" by Ted Nasmith",
    "Thomas Kinkade":" by Thomas Kinkade",
    "Victo Ngai":" by Victo Ngai",
    "Vincent DiFate":" by Vincent DiFate",
    "Wes Anderson":" by Vincent DiFate"
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

    "Portraits":", portrait, two arms, two legs, 5 fingers per hand, correct proportions",

    "Feminine+Attractive":", ((Feminine)), (effeminate), attractive, pretty, handsome, hypnotic, beautiful, elegant, sensual, two arms, two legs, 5 fingers per hand, ideal proportions, correct proportions",

    "Masculine+Attractive":", ((Masculine)), (manly), attractive, pretty, handsome, hypnotic, rugged, buff, muscular, strong, two arms, two legs, 5 fingers per hand, ideal proportions, correct proportions",

    "WaiFusion":", computer art, anime aesthetic, (((anime))), an ultrafine detailed painting, Artstation contest winner, trending on Artstation, deviantart contest winner, hd",

    "Horrible Monsters":", monster, ugly, surgery, evisceration, morbid, cut, open, rotten, mutilated, deformed, disfigured, malformed, missing limbs, extra limbs, bloody, slimy, goo, Richard Estes, Audrey Flack, Ralph Goings, Robert Bechtle, Tomasz Alen Kopera, H.R.Giger, Joel Boucquemont, artstation, thematic background",

    "Robots":", (((robot))), ((cyborg)), machine, futuristic, concept art by senior character artist, featured on zbrush central, trending on polycount, trending on Artstation, cgsociety, hard surface modeling",
    
    "Retrofuturism":", ((retrofuturism)), (science fiction), dystopian art, future tech, by Clarence Holbrook Carter, by Ed Emshwiller, cgsociety, Artstation contest winner, trending on Artstation, deviantart contest winner, Fallout",

    "Propaganda":", propaganda poster, soviet poster, sovietwave",

    "Landscapes":", naturalism, land art, regionalism, shutterstock contest winner, trending on unsplash, featured on flickr"
}

FocusOnNegatives = {
    "No focus":"", 

    "Portraits":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, extra limbs, missing limbs, fused fingers, fused palms, coalesced fingers, broken fingers, broken fingernails, warped pupils, distorted face, fused bodyparts", 

    "Feminine+Attractive":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, extra limbs, missing limbs, fused fingers, coalesced fingers, broken fingers, broken fingernails, fused palms, warped pupils, distorted face, fused bodyparts",

    "Masculine+Attractive":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, extra limbs, missing limbs, fused fingers, coalesced fingers, broken fingers, broken fingernails, fused palms, warped pupils, distorted face, fused bodyparts",

    "WaiFusion":", (((ugly))), (((disproportionate limbs))), ((corrupt palms)), incorrect anatomy, extra limbs, missing limbs, fused fingers, coalesced fingers, broken fingers, broken fingernails, fused palms, warped pupils, distorted face, fused bodyparts",

    "Horrible Monsters":", (attractive), pretty, smooth,cartoon, pixar, human",

    "Robots":", (((cartoon)))",
    
    "Retrofuturism":", extra limbs, malformed limbs, modern",

    "Propaganda":", extra limbs, malformed limbs, modern",

    "Landscapes":"((hdr)), ((terragen)), ((rendering)), (high contrast)"
}

# At some point in time it looked like adding a bunch of these negative prompts helps, but now I am not so sure...
AlwaysBad = ", (((cropped))), (((watermark))), ((error)), low quality, worst quality"
#AlwaysBad = ", (((cropped))), (((watermark))), ((logo)), ((barcode)), ((UI)), ((signature)), ((text)), ((label)), ((error)), ((title)), Incorrect proportions, stickers, markings, speech bubbles, lines, cropped, low quality, worst quality, artifacts"

class Script(scripts.Script):

    def title(self):
        return "StylePile"

    def ui(self, is_img2img):
        with gr.Group() as TabContainer:
            with gr.Tab("StylePile"):
                with gr.Row():
                    poResultType = gr.Dropdown(list(ResultType.keys()), label="Image type", value="Not set")
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
                ### Tips for better results
                Parenthesis can be added to make parts of the prompt stronger. So (((cute))) kitten will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: ((promt)).                
                Prompts can be split like [A|B] to sequentially use terms one after another on each step. [cat|dog] will produce a hybrid catdog.
                And using [A:B:0.4] will switch to other terms after the first one has been active for a certain percentage of steps. [cat:dog:0.4] will build a cat 40% of the time and then start turning it into a dog. This needs more steps to work properly.
                ### Conclusion
                I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute in some way just visit https://github.com/some9000/StylePile 
                """)
                
        return [poResultType, poResultStyle, poResultColors, poImageView, poFocusOn, poArtist, poHelpText, poVisualStyleHint, poArtistHint, TabContainer]

    def run(self, p, poResultType, poResultStyle, poResultColors, poImageView, poFocusOn, poArtist, poHelpText, poVisualStyleHint, poArtistHint, TabContainer):
        # Combine all our parameters with user's prompt
        
        p.prompt = ResultBefore[poResultType] + p.prompt + Artists[poArtist] + ResultType[poResultType] + ResultStyle[poResultStyle] + ResultColors[poResultColors] + ImageView[poImageView] + FocusOn[poFocusOn]

        p.negative_prompt += ResultTypeNegatives[poResultType] + FocusOnNegatives[poFocusOn] + AlwaysBad

        # Add information in command prompt window
        print(f"\nStylePile helping you make great art with:\nPositives:{p.prompt}\nNegatives: {p.negative_prompt}")
        print(f"Total elements in prompt: {1+p.prompt.count(',')+p.negative_prompt.count(',')}\n")

        proc = process_images(p)
        return proc
