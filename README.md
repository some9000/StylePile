![Top](https://user-images.githubusercontent.com/17021558/232333865-604dbff8-de69-4eed-9b71-c2d8050243d1.png)
StylePile is an extension for https://github.com/AUTOMATIC1111/stable-diffusion-webui designed to help you efficiently generate diverse results without delving deep into the technical aspects of the prompt. The images shown above and below were created using the standard `v2-1_512-ema-pruned.ckpt`, all with the same prompt: "Portrait of an attractive young lady, flower field background, square ratio". The same seed was used for each image, while StylePile handled the rest.

Jump to the INTRODUCTION section to learn more, or scroll further down to read the MANUAL.

![StylePile 2](https://user-images.githubusercontent.com/17021558/232105621-006ac476-b769-478e-b4fa-bc7e60f35711.svg)

**StylePile 2.1** has arrived, named after the most recent version of the base model used for its testing and development. Plus, it represents a huge leap forward from the previous version. You can find a full description below the installation instructions.

![Middle](https://user-images.githubusercontent.com/17021558/232378508-f4a702ba-6179-4f7c-9cc2-5354030b3875.png)

# Installation
**Important:** If you've used any previous version, make sure to remove it from the scripts or extensions directory to avoid conflicts. Simply delete the **StylePile.py** file and/or the **StylePile** folder there. If you've added your own images, it's a good idea to copy them out and then copy them back in later.

I know you probably don't enjoy scrolling through lengthy descriptions just to find installation instructions. I don't either, so here they are:

### Automatic (pun intended)
If you're using the original AUTOMATIC1111 version:
+ Head to the **Extensions** tab
+ Click **Available**
+ Click **Load from:** and wait a moment for the list to update
+ Scroll down the list or simply use **Ctrl+F - StylePile** and click **Install**
+ If everything went smoothly, it should appear in the Script dropdown for both txt2img and img2img.

### Semi-automatic
If the automatic method didn't work, try this:
+ Go to the **Extensions** tab
+ Choose **Install from URL**
+ Copy this address **https://github.com/some9000/StylePile** into the **URL for extension's git repository** field (or https://github.com/some9000/StylePile/edit/Beta-2.1 for this Beta version)
+ Enter **StylePile** into the **Local directory name** field
+ Click the **Install** button

### Manual
If neither method worked, or you're using a custom version that supports extensions but not auto installation/updating, follow these steps:
+ Click the green **<> Code** button above
+ Click **Download zip**
+ Wait for the download to finish
+ Navigate to **your-sd-folder\extensions**
+ Place the contents of the archive into a **StylePile** folder. It's okay if there's another StylePile folder in there. As long as the README.md is inside your-sd-folder\extensions\StylePile, you're good to go.
+ Launch stable-diffusion-webui, or if it's already open, head to **Settings** and press **Reload UI**.
+ If everything went well, it should appear in the Script dropdown for both txt2img and img2img.

## ANNOYING INTERMISSION
Since we moved the installation instructions up, it's only fair to bump up the important note as well, right? This passion project has consumed a significant amount of time, electricity, and now, ChatGPT subscription costs too. My Python coding skills aren't the best, but ChatGPT has been a huge help (not to mention all the amazing people on GitHub who've helped with my clumsy code). In addition to that I created some custom tools to process the resulting files, prepare the thumbnails etc. So if you've been enjoying StylePile and feel like offering some support:

<a href="https://www.buymeacoffee.com/some9000" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-1.svg" alt="Buy Me A Coffee"></a>

# INTRODUCTION
When I first started learning Stable Diffusion prompting, it felt like a real hassle to change all the keywords just to get a different look. So, I created a basic little script that would just add some values from dropdown menus. Over time, as I learned more about crafting prompts and saw how various elements could significantly impact the outcome, I kept tweaking and refining it. Now, we've arrived at version 2.1, packed with a ton of enhancements, some cool new features, and better results overall. Let's dive into what StylePile has to offer:

![2023-04-16 21 18 59 127 0 0 1 e643003fa46d](https://user-images.githubusercontent.com/17021558/232333485-d8378243-6716-447f-9cff-7112fdb388e7.png)

## Basic
- Quickly put together a specific look for your results by choosing **Presets** for **Concepts, Image types, Execution, Mood, Color**, and easily adjust their intensity.
- A collection of **Visual previews** to give you an idea of what each selection might look like.
- **Random selection** options to explore a diverse range of artistic styles and approaches.
- Easy-to-use tools for creating prompt elements like **Attention/emphasis strength, Morph from-to**, and **Alternating words**. Sure, you could write these yourself, but it's easy to forget the right way to do it.
- A huge library of **Artist names** and **Art movements** hand-tested on thousands of images, all mix-and-matchable with the other selections mentioned above.
- A **Different generation status look** that keeps you informed about the generation process while supporting new features.
## Advanced
- The ability to **Use variables inside your prompt**, including one main variable [X], one sub-variable [Y], and six random variables [A][B][C][D][E][F]. All elements support multiple lines, allowing for the automatic creation of hundreds of prompts. You can also mix in random elements for added variety.
- A **Preset function** that lets you load and save these variables, along with a comment field, so you don't have to fill in all 10 possible prompt fields again. Try out the included presets, create your own, and share them to be included in future versions.
- The prompt sequencing has been revamped to support these features, with the tradeoff of losing how Batches typically work. However, you can now **Create complex loops for discovering new looks**. If a random seed has been entered manually, you can choose if it should increase with each run of Batch size. When a new Batch count loop starts, the seed will reset, enabling extensive automated look testing.

## Customization
- Everything in StylePile 2.1 is read from external sources, allowing you to **Customize all values** as needed. Add or remove base Image Types, modify what's included in Type lists, and add or remove Artists and Art movements.
- Edit the random prompt list with your own entries (for simple prompt insertion instead of the more complex variable preset approach) and change the prompt mixing and matching lists. More details on this below.

# MANUAL
## Main generation parameters
NOTE: Unless specified otherwise, all images are marked as Digital Artwork along with the option they demonstrate. To create your own test images with the same settings, click the Default prompt button, and the setup will replicate the configurations used here.

StylePile offers a versatile collection of image appearance parameters, allowing users to combine, adjust, and apply them to numerous images systematically or randomly. The most critical components are Image type and Execution. Image type is self-explanatory, while Execution may not always perform as described but significantly influences the outcome. Some niche options are included as they yield intriguing results. Combining two Execution selections can create an even more diverse style and lead to impressive outcomes:
![Type and Execution](https://user-images.githubusercontent.com/17021558/233005104-d5c0c865-5bc0-460c-823a-587a5bc385d0.jpg)

Next, we have **Concept/Direction/Adjective**. While not a strong modifier, it still impacts the image:
![Concept](https://user-images.githubusercontent.com/17021558/233006111-1506600d-88c5-48da-931c-ffdef344c640.jpg)

Following this is **Mood/Feeling**, which not only influences facial expressions on humanoid models but also alters the scene's overall appearance and ambiance:
![Mood](https://user-images.githubusercontent.com/17021558/233006642-115165ed-b3bc-470f-ba27-42683adc86a9.jpg)

Finally, there's **Palette/Color influence** that can significantly affect the final result, depending on its type:
![Color](https://user-images.githubusercontent.com/17021558/233007095-382ba754-406b-4896-9979-9f1ea5f42160.jpg)

## Artists and Art movements
Selecting **Artists** and/or **Art movements** can significantly influence your image by incorporating distinct stylistic elements. StylePile allows you to generate images inspired by renowned artists or prominent art movements. The effectiveness of specific selections may vary with different models. However, you are encouraged to experiment with the three available options for each type. This approach promotes creativity, enabling you to create some really unique visuals. Here is an example of selecting an Artist:

![Artists](https://user-images.githubusercontent.com/17021558/233011017-b86d48fd-a231-47b7-bb00-1148941397f5.jpg)

And here an Art style:
![Art Style](https://user-images.githubusercontent.com/17021558/233011066-b7fc2051-094f-4d4b-af90-2af0c17f7336.jpg)

## Advanced automated elements
