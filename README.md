# StylePile
A simple helper script for AUTOMATIC1111/stable-diffusion-webui

Basically a mix and match of keywords to quickly get different results without wasting a lot of time writing prompts. Currently has four main categories that affect your results. As well as some more detailed presets for different styles. Hopefully these can be improved with ideas from the users. Basic interface looks like this (at the bottom):
![MainScreen](https://user-images.githubusercontent.com/17021558/196465434-4bfe463b-f1c3-4bce-8860-842cb5bedb72.png)
You (currently) have 4 columns to set up a certain look quickly. And below there are style presets.
For example, you can set the image you like to img2img and use a preset to get a different look quickly:
![img2img](https://user-images.githubusercontent.com/17021558/196466057-f7e3f1fb-596b-459d-b5a5-f5d68ba101d6.png)

And then the bottom **Focus on** option adds a much larger amount of elements to the prompt thus strongly affecting the results.

# Examples
Prompt of **Bearded man** without any input:
![00000-3368790946-Bearded man-tile](https://user-images.githubusercontent.com/17021558/196467191-36f6117d-edee-425a-a268-dd9d1136982c.jpg)
With **Portrait** focus:
![00005-1360169829-Bearded man-tile](https://user-images.githubusercontent.com/17021558/196467384-294eac30-3483-4a55-be40-fb7a10972062.png)
With **Pretty people** focus:
![00004-4115990192-Bearded man, Norman Rockwell, Franz Xaver Winterhalter, Jeremy Mann, Artgerm, Ilya Kuvshinov, Anges Cecile, Michael Garmash-tile](https://user-images.githubusercontent.com/17021558/196467546-0f0f32a7-9b55-498f-ab08-37a9de0db163.png)
And with **Monsters** focus for some repulsive results:
![00007-3600129258-Bearded man, monster, ugly, surgery, morbid, cut, open, rotten, mutilated, deformed, disfigured, malformed, missing limbs, extra-tile](https://user-images.githubusercontent.com/17021558/196467721-b959d54d-a0b8-4581-b7ba-fd164570fe92.png)

# Installation
Just download **StylePile.py** from above (either click **Code - Download ZIP** and then extract from there OR right click the file name and pick **Save link as**) and drop it into your **stable-diffusion-webui/scripts** folder. Upon next launch it should be available at the bottom **Script** dropdown.
