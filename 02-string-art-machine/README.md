

> Note: Some parts of this project and its underlying know-how are not publicly available, as they are intended for future commercial use.


## String Art Machine

A machine that automates drilling and winding processes to create physical string art pieces. Self developed for engineering thesis at AGH university. 


<img src="pictures/winding_gif.gif" height="500"/>

The porject could be split to four parts: 
Design / Electrical scheme & parts/ microcontroler software & control / managing workflow 

---

**Design**
The designing part was one of the most difficult one. First i had to come up with general concept. I was watching videos of people who built such machines themselves and inspired myself by their creations and solutions. Even with that it was really difficult to come up with my own design. Everything had to work, be cheap and possible to assemble. the last part is crucial as i struck myself sometimes creating solutions that look great on the screen but arent really possuble to assemble in real life. I had to CAD design every part with barring in mind that they will be manufactured using 3D printing or CNC milling technologies. A lot of mistakes were made in this journey but this is how i learned the hardships of coming up with design. Here is full assembly of a model:

fota modelu



---

**Electrical scheme & parts**

There were a bunch of different elements that needed to be bought and i had to come up with what i need 





**First method**

This approach was the first thing I came up with while thinking of a solution. I use a different approach right now, but it still has potential, after further optimizations and modifications, to give results for photos that the second algorithm wouldn’t be able to recreate. Either way, it was massively useful to develop, as I learned a whole bunch of practical knowledge about time and space optimizations using different methods like parallel computing on GPUs, broadcasting, precomputing, compressing arrays to sparse matrices and decompressing, and more. Here are some of the outputs:

<img src="pictures/dog.png" height="400"/> <img src="pictures/cat.png" height="400"/>

The basic idea is to have a blank canvas and create points that are equally spaced on the circumference of a circle. Then one point is chosen as the starting point, and a line is drawn to every possible connection with that point. The best one is selected by comparing the current canvas to the original photo using MSE. As one can see, this means a huge number of comparisons are made during a run. For a 3000-line piece with 200 points, there are 600,000 MSE comparisons on high-resolution images.

At first, iterations of the algorithm would take days, then hours, and I was finally able to reduce it to about 20 minutes on my computer — which is still quite slow, but at least usable. This improvement was mostly thanks to performing the comparison in the inner loop, where we check for the best line from 200 possibilities. Instead of checking them iteratively, all 200 possibilities are evaluated at once using the GPU. So instead of performing 200 calculations sequentially on the CPU in each iteration, they are done roughly in parallel on the GPU.

This method requires a setup phase. All possible line images need to be precomputed so they can be quickly used in the main loop. It is best described by the diagram below:

<img src="pictures/setup.png" height="800"/>

Now, in the main loop, new lines are easily accessible, enabling parallel addition of potential lines to the canvas and comparison with the original image. The parallel computation was actually split into two batches because I didn’t have enough GPU memory to compute everything at once.

---
**Second method**

With the second developed approach, I was able to reduce computation time to around 2–3 minutes while achieving much better results. There is still a lot of room for improvement, which I am currently working on. Here are some of the outputs:

<img src="pictures/eye.png" height="300"/> <img src="pictures/pearl.png" height="300"/> <img src="pictures/Einstein.PNG" height="300"/>

---
**GUI**

A simple GUI was made to make it easier for user to experiment with different pictures and parameters. It was made using Tkinter library. The timelapse effect was achieved using a custom callback function triggered from the main algorithm loop. Every few iterations (e.g. every 10 lines), the current state of the image is passed to the GUI, which updates the display.

<img src="pictures/GUI.png" height="700"/>

