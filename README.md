## ChyoowAd - Choose your own Adventure
![Person holding Adventure Book](logo_placeholderHD.jpeg)

---

This piece of software helps to tell interactive stories inside Excalidraw, using its feature to link elements and navigate between them.

It basically converts a plain-text story file (where every line is a storypoint) to an .excalidraw sketch-file.

If you have no clue what this may mean, try one of the adventures I created:

(make sure to save your latest sketch before replacing it! Also change to view mode upon opening for the best experience)

[online-version](https://excalidraw.com/#json=MFSyFDRTVKN8CCrfxrCEd,292iLALgxVmApHV5limy8A) (hosted on ecalidraw.com)

[.excalidraw-file](small_demo.excalidraw) (right-click, select "save link as..."; open in excalidraw after download)

---

Current version on master is the minimum viable software, meaning it works, but there is much to improve!
(Maybe you wanna help by contributing?)

- Right now the formatting is made for only one character (mainly an emoji) per Bubble in Excalidraw. It would be nice to be able to add text and have it format automatically to the right size and position for more in-depth stories (even though emoji-stories can be more complex than I expected)
- An option to use a custom font would be nice. I know there is a way to compress a font in base64 and have it inside the excalidraw json. Obsidian has a very feature rich Excalidraw add-on, should look into their codebase to explore this further
- A tutorial page which is optionally visitable at the start seems like a no brainer
- maybe also something like an impressum or just links to this github etc.
- .config file for playing around with settings easily 

---

One feature I really (really, really) would like to have, is that the drawing opens in view mode.
Want to find a way that doesn't use third party apps and doesn't require customizing Excalidraw for this purpose.
(Excalidraw Docs are not what I would call detailed, so maybe i can just set a flag in the json under appstate?)

---