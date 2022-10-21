# StylePile
A simple helper script for AUTOMATIC1111/stable-diffusion-webui

Basically a mix and match of keywords to quickly get different results without wasting a lot of time writing prompts. Currently has four main categories that affect your results. As well as some more detailed presets for different styles. Hopefully these can be improved with ideas from the users. Basic interface looks like this (at bottom left):

![2022-10-21 09 18 01 127 0 0 1 e54ff6f17319](https://user-images.githubusercontent.com/17021558/197129750-92ce8e86-c154-4c28-9224-548f4e0df418.png)

As you can see there aren't that many keywords in the prompt fields yet the result has a reasonably distinct look. You (currently) have 4 columns to set up a certain look quickly. And below there are style presets. I am doing my best to improve the way it works and expand the keyword selection. There is still plenty of work to be done, but the system does work quite nicely and produces a more creative workflow.

# Usage example
Ok, let's imagine you would like to generate a **Lady knight in medieval armor**. Let's use that as a prompt:

![00324-1348758302-lady knight in medieval armor](https://user-images.githubusercontent.com/17021558/197111727-29c9e389-d871-48f6-b7d0-a97aa5c14775.png)

It does represent the main idea. But, it is boring and probably not what we had in mind. Let's load **StylePile** from the dropdown on the bottom left, hit Generate and see what happens.

![00325-1348758302-lady knight in medieval armor](https://user-images.githubusercontent.com/17021558/197112034-733c672a-0a9e-40e4-90fd-3409ff354cdf.png)

Nothing is selected and the prompt is the same so why did it change? Well, there are some default keywords always in use that try to prevent text, low image quality etc. But this is boring, let's set **Image style** to **Photography**:

![00326-1348758302-A photograph of  lady knight in medieval armor, ((analog photo)), (detailed), ZEISS, studio quality, 8k, 4k, uhd](https://user-images.githubusercontent.com/17021558/197112225-906a9cb1-86ea-48a5-a21a-5b8dd095875b.png)

Ok, that is quite the difference. What happens when we add a **Visual style**? Here are all the possible results at the time of writing this:

![Styles](https://user-images.githubusercontent.com/17021558/197112781-26e05e01-9da9-4775-a224-41b1eb613eb6.png)

As you can see, even the painting-oriented styles do not have a huge impact, because that first choice is the most important. Still, there is a visible difference so you can play around and find out what works best. Now, what happens when we go back and change **Image type**?

![Types](https://user-images.githubusercontent.com/17021558/197113389-f256c97a-f26a-4a8f-9219-977344a612f0.png)

Quite a lot. So remember - type is most important, then style, then color. And, for now, view commands barely work, this seems to be a limitation of Stable Diffusion. But you can try to play around and see what works or doesn't.
Here's our final result with **Desaturated** color selection for a more dramatic look (you can see that the armor also became smoother which just shows how things are a little unpredictable with Stable Diffusion) and **Restore faces** in main interface selected:

![00343-1348758302-A photograph of  lady knight in medieval armor, ((analog photo)), (detailed), ZEISS, studio quality, 8k, 4k, uhd, (((realistic))](https://user-images.githubusercontent.com/17021558/197114973-499addaf-de7f-44f1-8069-1b3d0b9f36bf.png)

# Focus on
At the bottom the **Focus on** option adds a much larger amount of elements to the prompt with a single click. And that greatly affects the final result. Currently there are not too many presets but, hopefully, with your help that will change soon. So here is how it works:

Prompt of **Knight in armor** without any input:

![Default](https://user-images.githubusercontent.com/17021558/196643976-f7409711-ee6e-4a27-9524-a03827384c34.png)

A little boring, a little random. Let's try **Feminine and extra attractive**:

![KnightLadies](https://user-images.githubusercontent.com/17021558/196644475-596e7c05-bed4-47cd-9afc-56ff70a4ca8c.png)

And now **Masculine and extra attractive**:

![KnightMen](https://user-images.githubusercontent.com/17021558/196644706-2df9e416-c6f5-4247-8129-3f2ce3f66cc2.png)

There are also more artistic adjustments, such as **Monsters**. A trick was used in this example - if you use just the Monsters focus the result will be mostly chaotic and horrifying as a monster should be. But if, as in this case, you pick a style from the menu above that can greatly affect the result. In this case it was Photography and brought a little balance into those results:

![MonsterKnights](https://user-images.githubusercontent.com/17021558/196644813-7f3184b0-1b81-4a16-a078-c8f3d7a8c419.png)

Also, not all adjustments will work with all prompts, such as this **Robots** one having a hard time with knights:

![Robots](https://user-images.githubusercontent.com/17021558/196645673-17d24ea2-bb9a-4089-9863-d5d0f6deac2e.png)

So you should just mix and match and experiment to find out which styles work well together. Or don't, that also produces interesting results.

#With img2img
For example, you liked that lady knight example from above, but would prefer it as a painting. Just transfer it to img2img, mix styles with Focus and get a pleasant result quickly (but, preferrably do a batch, Stable Diffusion still doesn't magically make every result great). 

![2022-10-21 09 56 57 127 0 0 1 8469e9f6d637](https://user-images.githubusercontent.com/17021558/197132497-f5d6b9cb-7ac1-4c83-94ba-4b0b13fc90ef.png)

# Installation
Click the green **Code** button at the top of the page, select the **Download ZIP** option. When done extract the **StylePile.py** file from there and drop it into your **stable-diffusion-webui/scripts** folder. Upon next launch it should be available at the bottom **Script** dropdown.
