import modules.scripts as scripts
import gradio as gr
import os

from modules.processing import process_images, Processed
#from modules.shared import opts

# not yet

#BASE_STEPS=40
#BASE_SCALE=10

ResultType = {
    "Not set":"", 
    "Photography":", ((photograph)), highly detailed, sharp focus, 4k", 
    "Digital art":", ((digital art)), (digital illustration), 4k, trending on artstation, trending on cgsociety, cinematic, agfacolor", 
    "Painting":", ((painting, canvas, fine art)), detailed", 
    "Sketch":", ((sketch, drawing)), pencil art, graphite, colored pencil, charcoal art, high contrast, 2 bit", 
    "Classic Comics":", ((storybook drawing, graphic novel, comic book)), Jack Kirby, Frank Miller, Steve Ditko, John Romita, Neal Adams", 
    "Modern Comics":", ((comic book)), Jim Lee, john romita jr, Cory Walker, ryan ottley",
    "Manga":", ((manga,anime)), Katsuhiro Otomo, Naoki Urasawa, Hiroya Oku, Hiromu Arakawa, Junji Ito,danbooru, zerochan art, kyoto animation"
}

ResultTypeNegatives = {
    "Not set":"", 
    "Photography":", art, painting, rendering, drawing, sketch", 
    "Digital art":", photography, painting, signature", 
    "Painting":", photography, rendering, signature, wall", 
    "Sketch":", photography, rendering, painting, signature, text, margin", 
    "Classic Comics":", ((logo)), (title), text, speech bubbles, panels, signature, ((barcode)), margin, sticker", 
    "Modern Comics":", ((logo)), (title), text, speech bubbles, panels, signature, ((barcode)), margin, sticker", 
    "Manga":", ((logo)), (title), text, panels, speech bubbles, signature, ((barcode)), margin, sticker" 
}

ResultStyle = {
    "Not set":"", 
    "Realism":", ((realistic)),(realism)", 
    "Photorealism":", ((photorealism))", 
    "Hyperrealism":", (hyperrealism)", 
    "Surrealism":", (surrealism)", 
    "Modern Art":", (modern art)", 
    "Painterly":", (painterly)", 
    "Abstract":", (abstract art), ", 
    "Pop Art":", (pop art)", 
    "Impressionist":", (impressionist art)", 
    "Cubism":", (cubism)", 
    "Fantasy":", (fantasy art)"
}

ResultColors = {
    "Not set":"", 
    "Warm":", warm", 
    "Cool":", cool", 
    "Colorful":", colorful", 
    "Saturated":", saturated", 
    "Low saturation":", low coloration", 
    "Desaturated":", desaturated", 
    "Grayscale":", grayscale", 
    "Black and white":", black and white", 
    "Complementary":", complementary-colors", 
    "Non-complementary":", non-complementary colors", 
    "Chaotic":"chaotic colors", 
    "HDR":"HDR", 
    "Light":"light"
}

ImageView = {
    "Not set":"", 
    "Fisheye lens":", fisheye lens, 10mm, zoomed out, F/22.0, very far away, sharp", 
    "Super wide angle":", super wide angle, 20mm, zoomed out, F/11.0, far away, sharp", 
    "Wide angle":", wide angle, 25mm, 35mm, zoomed out, F/5.6, medium distance, sharp", 
    "Portrait lens":", portrait lens, 50mm, F/2.8, 1m away", 
    "Telephoto lens":", telephoto lens, 100mm, F/5.6, far away, sharp", 
    "Super telephoto":", super telephoto lens, F/11.0, 200mm, 300mm, very far away, sharp", 
    "Macro lens":", macro lens, extremely close, extremely detailed"
}

ImageStyle = {
    "No focus":"", 
    "Portrait":"", 
    "Pretty people":", Norman Rockwell, Franz Xaver Winterhalter, Jeremy Mann, Artgerm, Ilya Kuvshinov, Anges Cecile, Michael Garmash",
    "Monsters":", monster, ugly, surgery, morbid, cut, open, rotten, mutilated, deformed, disfigured, malformed, missing limbs, extra limbs, bloody, slimy, goo, Richard Estes, Audrey Flack, Ralph Goings, Robert Bechtle, Tomasz Alen Kopera, H.R.Giger, Joel Boucquemont, artstation",
    "Landscapes":"", 
    "Scenes":", warm"
}

ImageStyleNegatives = {
    "No focus":"", 
    "Portrait":", ((ugly)), ((duplicate)), (morbid), ((mutilated)), (mutated), (deformed), (disfigured), (extra limbs), (malformed limbs), (missing arms), (missing legs), (extra arms), (extra legs), (fused fingers), (too many fingers), long neck, low quality, worst quality", 
    "Pretty people":", ((ugly)), (mutilated), (bad anatomy), (bad proportions), bad hands, text, error, missing fingers, extra digit, cropped, low quality, worst quality",
    "Monsters":"",
    "Landscapes":", low quality, noise, lowres", 
    "Scenes":", warm"
}

class Script(scripts.Script):

    def title(self):
        return "StylePile"

    def ui(self, is_img2img):

        with gr.Blocks(css=".gradio-container {background-color: red}"):

            with gr.Row():
                poResultType = gr.Radio(list(ResultType.keys()), label="Image type", value="Not set")
                poResultStyle = gr.Radio(list(ResultStyle.keys()), label="Visual style", value="Not set")
                poResultColors = gr.Radio(list(ResultColors.keys()), label="Colors", value="Not set")
                poImageView = gr.Radio(list(ImageView.keys()), label="View", value="Not set")
                
            with gr.Row():
                poImageStyle = gr.Radio(list(ImageStyle.keys()), label="Focus on (Adds extra prompts to improve results)", value="No focus")
            
            #with gr.Row():
            #    TextToShow = gr.Text(value=poResultType, label="Extra keywords", visible=True, placeholder="Selected keywords will appear here")

        return [poResultType, poResultStyle, poResultColors, poImageView, poImageStyle]

    def run(self, p, poResultType, poResultStyle, poResultColors, poImageView, poImageStyle):
        p.do_not_save_grid = True
        # Add the prompt from above
        p.prompt += ResultType[poResultType] + ResultStyle[poResultStyle] + ResultColors[poResultColors] + ImageView[poImageView] + ImageStyle[poImageStyle]
        p.negative_prompt += ResultTypeNegatives[poResultType] + ImageStyleNegatives[poImageStyle]
      
#        p.cfg_scale=BASE_SCALE
#        p.steps = BASE_STEPS

        proc = process_images(p)
        return proc