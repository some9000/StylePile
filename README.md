# StylePile
A simple helper script for AUTOMATIC1111/stable-diffusion-webui

Basically a mix and match of keywords to quickly get different results without wasting a lot of time writing prompts. Currently has four main categories that affect your results. As well as some more detailed presets for different styles. Hopefully these can be improved with ideas from the users. Basic interface looks like this (at the bottom):
![MainScreen](https://user-images.githubusercontent.com/17021558/196465434-4bfe463b-f1c3-4bce-8860-842cb5bedb72.png)
You (currently) have 4 columns to set up a certain look quickly. And below there are style presets.
For example, you can set the image you like to img2img and use a preset to get a different look quickly:
![img2img](https://user-images.githubusercontent.com/17021558/196466057-f7e3f1fb-596b-459d-b5a5-f5d68ba101d6.png)

# Focus on
At the bottom the **Focus on** option adds a much larger amount of elements to the prompt with a single click. And that greatly affects the final result. Currently there are not too many presets but, hopefully, with your help that will change soon. So here is how it works:

Prompt of **Knight in armor** without any input:
![Default](https://user-images.githubusercontent.com/17021558/196643976-f7409711-ee6e-4a27-9524-a03827384c34.png)
A little boring, a little random. Let's try **Ladies** which is aimed at attractive feminine features:
![KnightLadies](https://user-images.githubusercontent.com/17021558/196644475-596e7c05-bed4-47cd-9afc-56ff70a4ca8c.png)
And now **Gentlemen** which does the same, but adjusted for male models:
![KnightMen](https://user-images.githubusercontent.com/17021558/196644706-2df9e416-c6f5-4247-8129-3f2ce3f66cc2.png)
There are also more artistic adjustments, such as the **Monsters**. A trick was used in this example - if you use just the Monsters focus the result will be mostly chaotic and horrifying as a monster should be. But if, as in this case, you pick a style from the menu above that can greatly affect the result. In this case it was Photography and brought a little balance into those results:
![MonsterKnights](https://user-images.githubusercontent.com/17021558/196644813-7f3184b0-1b81-4a16-a078-c8f3d7a8c419.png)
Also, not all adjustments will work with all prompts, such as this **Robots** one having a hard time with knights:
![Robots](https://user-images.githubusercontent.com/17021558/196645673-17d24ea2-bb9a-4089-9863-d5d0f6deac2e.png)
So you should just mix and match and experiment to find out which styles work well together. Or don't, that also produces interesting results.

# Installation
Click the green **Code** button at the top of the page, select the **Download ZIP** option. When done extract the **StylePile.py** file from there and drop it into your **stable-diffusion-webui/scripts** folder. Upon next launch it should be available at the bottom **Script** dropdown.
