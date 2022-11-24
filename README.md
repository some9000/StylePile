![StylePile](https://user-images.githubusercontent.com/17021558/202690454-cc31a9b9-ba48-484c-89b2-cdfd8bad247c.svg)

**Note** This manual is somewhat incomplete at the moment, it does not explain the variable functions, but those should be reasonably self explanatory. Will be finalized later.

**StylePile**[^1] is an extension for https://github.com/AUTOMATIC1111/stable-diffusion-webui for mixing and matching elements to prompts that affect the style of the result. Hence the name. By default, these elements are placed in a specific order and given strength values. Which means the result sort-of evolves. I have generated thousands of images for each main **Image type** and tweaked the keywords to attempt giving expected results most of the time. Here are some examples on what you can get with a couple of clicks:

![F](https://user-images.githubusercontent.com/17021558/199468444-99e78027-1889-4bec-b97b-25f801e33c0a.jpg)
![A](https://user-images.githubusercontent.com/17021558/199458710-efc7520d-70a1-475b-8ca0-dbdc3182b865.jpg)
![C](https://user-images.githubusercontent.com/17021558/199459334-8fcd6f9a-0125-4b9f-bc38-e9048adf798b.jpg)
![B](https://user-images.githubusercontent.com/17021558/199458741-61e00c9f-d3bd-472e-9fef-ff0dd8061605.jpg)
![D](https://user-images.githubusercontent.com/17021558/199462277-a6c25028-96a4-4508-8577-cd79f9e6afd9.jpg)
![E](https://user-images.githubusercontent.com/17021558/199465943-c69ea9c3-61db-4bc5-ae59-2d95b0c5d979.jpg)
I left the less successful results in on purpose, to show that this isn't some magical tool that overcomes all the difficulties that Stable Diffusion currently has. But it does help you go on that artistic journey way easier. So let's begin.

## Installation
In theory you should be able to use the **Install from URL** feature:
* Copy the main address (https://github.com/some9000/StylePile) of this repository,
* In SDUI go to **Extensions tab**,
* Select **Install from URL** and paste that URL into the **URL for extension's git repository field,
* Press Install.

If all goes well the necessary directories will be automatically created and all the files downloaded into them. After which the extension should be available under the **Scripts** dropdown in both **txt2img** and **img2img**. If you get error messages or it does not show up even after a full SD restart try this:
* Click the green **Code** button at the top of the page,
* Select the **Download ZIP** option,
* When done extract everything from there and drop it into your **stable-diffusion-webui\extensions\StylePile** folder.

Basically you should have a **scripts** and **StylePile** folder inside that folder. It is ok to have another StylePile folder inside the main one. This is what should show up when it loads (without the cyborg knight, though, you will have to render that on your own):
![2022-11-24 10 01 18 127 0 0 1 265a839a8e2b](https://user-images.githubusercontent.com/17021558/203726455-7f5fe73d-58fc-472a-b3c8-bb9fbb80fd16.png)

## Base workflow
As you can see in the above image, the prompt seems fairly simple, but the result has a distinct look. That is thanks to the selections from the StylePile dropdowns below. Main workflow is - come up with a interesting theme, then easily mix and match style elements to get it closer to desired result.
For example, if you select the **Painting** image type, then almost all results will look like Paintings. Selecting **Mood** will have a certain influence on the overall look in some way (if it's something humanoid it may show emotion, but also colors and overall feel may change). Setting **Colors** will change the general tonality of the result. And setting **View** will attempt to change how the subject is viewed. Attempt, because view appears to be the least reliable keyword. These elements are placed in order of influence and supported by certain strength values. These basic settings produce very quick results close to the general look you want.

Moving on, adding a **Visual style** will combine with **Image type** to influence how the result generally looks. These styles are based on classic and modern Painting/Art/design movements (which I picked after hours and thousands of samples of testing) and can have a strong influence on the end result. Either it will be more realistic or artistic, or look like a comic book etc. In general, this is a really strong element for getting the look you want. Its influence can be adjusted with the slider above. Experiment with the values, keeping in mind that anything above 1.5 will start becoming a mess. In a similar way, but more focused, you can select an **Artist** and, of course, that will have a very visible effect on the result as well. Currently there are 135 artists, 55 art styles and 25 emotions available for selection and represented with preview images.

Strength of these settings has been preset at 1.3, as that appears to be the golden ratio for getting good results. Sometimes very low settings have an interesting result as well. You can, and should, freely mix and match these settings to get different results. Classic Painting styles affected or affecting 3D look quite interesting. Photography can look cool with some of the brighter, more artistic styles etc. Sometimes raising CFG scale to 15,20 or more also helps to REALLY push the style onto the image.

## Advanced workflow
![2022-11-02 11 04 02 127 0 0 1 b49227fa903f](https://user-images.githubusercontent.com/17021558/199448363-0e61f273-6321-40d2-bcf2-544956de6b87.png)

StylePile can overtake the generation process, allowing you to generate a large amount of different results with very little extra work. There are two types of variables you can use: [X] and [R]. When you add an [X] to your prompt, it sequentially takes values from the **Sequential prompts** text area. You can have dozens of lines there and they will be processed in sequence. When you add [R] to the prompt a value from the **Random prompts** text area will be inserted in its place. By combining these a huge variety in prompts is very easy to do.

When using this, **Batch count** will move through the prompts and **Batch size** will set how many copies with the given prompt to make. If the seed is not random, it will increase with each batch size step. Any random elements will still be picked randomly. Here are the results from the demo above:

![Demo](https://user-images.githubusercontent.com/17021558/199448928-73b93a35-8c5c-42d9-ab78-6b3f32a6a86f.jpg)
## Tips and tricks
If you add your own Artist, I would recommend having "by Artist" in front of their name. Depending on Artist's popularity (or lack thereof) this appears to have a very tangible influence on the result.

Parenthesis can be added to make pArts of the prompt stronger. So **((cute kitten))** will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: **((promt))**. A strength modifier value can also be used, like this **(prompt:1.1)**. To save some typing you can select the line you want to make stronger and use **Ctrl+Shift+Arrow keys up** or **down** to add these parenthesis and change the value. As you can see by default values on most sliders, 1.3 seems like a good stArting point if you want to see some impact.

Prompts can be split like **[A|B]** to sequentially use terms, one after another on each step. For example **[cat|dog]** will produce a hybrid catdog.

Using **[A:B:0.4]** will switch to other terms after the first one has been active for a certain percentage of steps. So **[cat:dog:0.4]** will build a cat 40% of the time and then stArt turning it into a dog. Usually this needs more steps to work properly.

Additionally the command line will also share more information than by default so you can get a better idea on the progress of your artworks:

![image](https://user-images.githubusercontent.com/17021558/199454650-c0859776-0bbb-4ad1-b037-6ad4b4b75cd3.png)
## In conclusion
I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute[^2] in some way do get in touch.





## Focus on (partially implemented)
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

# With img2img
For example, you liked that lady knight example from above, but would prefer it as a painting. Just transfer it to img2img, mix styles with Focus and get a pleasant result quickly (but, preferrably do a batch, Stable Diffusion still doesn't magically make every result great). 

![2022-10-21 09 56 57 127 0 0 1 8469e9f6d637](https://user-images.githubusercontent.com/17021558/197132497-f5d6b9cb-7ac1-4c83-94ba-4b0b13fc90ef.png)

[^1]: Pun intended.
[^2]: Hey, if you have a 12Gb graphics card just laying around I'm happy to take it (:
