# freehand-zxcalculus-recognition
Recognition algorithm for freehand zx-calculus diagrams


## Prerequisites

The inputs should be drawn by Inkscape. Download Inkscape if you want to recognise your own diagrams.
Third-party libraries used in this program: shapely, sklearn. If you do not have these two libraries, use command below to install them: 

```
pip install sklearn
pip install shapely
```

## Running the program

Run the main.py and the program will begin to do the recognition for a test file. There are 3 existing test files in test_set folder named "zx1.svg", "zx2.svg" and "zx3.svg". 
Modify the test_file in config.py if you want to recognise your own SVG file. 
```
test_file = 'your_input.svg'
```
## Visualise outputs
- Check the "output.svg" in outputs folder for the SVG visualisation output. 
- The LaTeX code ouput is printed by the main program. Copy the code into the "tikz-examples.tex" in latex_diagram folder and compile. 

## Evaluate the performance 

Run the evaluate.py and it will print out the accuracy of the classifier. 

## Tips for users

- When drawing your own diagrams in Inkscape, use the freehand stroke tool with the smoothness of 20 (on the top-left corner) and do NOT use snapping. Snapping can be set at document properties.
- If you can not load the svm_clf.pkl classifier, run the evaluate.py first. It'll train a new classifier and cover the original one. 
- To be continued (•ิ_•ิ)


