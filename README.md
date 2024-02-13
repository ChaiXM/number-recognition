# Number-Recognition
A small project of character recognition. This project is to show another way of handwritting recognition.
## Library used 
tkinter
numpy
scipy
matplotlib.pyplot
torch
## Features
- Write single number
- predict what is that number
- show graph of the data used to predict the number

## Method
This number recognition use the value of X and Y only to predict the written number.
1. First, record XY value and every 8 pixels distance moved.
2. The angle of movement is also recorded and resample to list with 16 length.
   - the angle is applied with sin and cos function
3. All the angle number is counted and normalizated to 1.
4. Starting point is also used to calculate the distance from all XY value and resample to list with 16 length
5. All 56 data is inputed to simple neural network to predict the output.

When turn the list into graph, every number have their own characteristic that differentiate from each other.
Therefore, it is possible to use Neural network to predict.

<img width="439" alt="image" src="https://github.com/ChaiXM/number-recognition/assets/68574901/1f8b6dda-c757-4506-8db6-6806622a2a02">

However, different writting styles will effect the prediction and currently haven't figure out the implementation for character that need to written in more than single stroke.

## Neural network model
The image below shows the network model.
![network](https://github.com/ChaiXM/number-recognition/assets/68574901/ee556480-1814-439d-a307-0343582fcd05)


## Usage
1. Download all the files
2. Run paint.py (I used python 3.8)
3. This is the user interface
   ![Screenshot 2024-02-09 160200](https://github.com/ChaiXM/number-recognition/assets/68574901/81d2c8d7-616f-4327-920d-cb391f1339bf)
4. On the left there will be two button **Enter** and **Show Graph**
   -  **Enter** when being clicked will show **Start**
      - **Start** needed to be click again, and then, you can start writing at the blank space on the right
      - click **OK**, then the predicted number will show below the button  
   -  **Show Graph** when being clicked will show **Not showing**, the button show current state
      - click **Not Showing** to show graph
      - click **Now Showing** to not show the graph
5. Only one writting styles are being trained for each number in `savemodel.txt`, therefore you need to follow the writting styles show in the `gif` below for accurate number prediction.
   
   ![example](https://github.com/ChaiXM/number-recognition/assets/68574901/462e19f2-a34a-4e45-900e-809cc6ed4278)

## Credit
I have used [pickry](https://github.com/pickry/Tkinter/blob/main/paint.py) code for the Tkinter painting application to show this implementation.


