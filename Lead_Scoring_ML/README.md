# Introduction
This project was completed in response to a prompt that needed to be addressed as a part of a job application.

This directory contains the code that is a prototype of one core component of the AI-Automated lead generation system proposed. The prototype included is the training and inference using a machine learning model that calculate lead scores.

**Note:** The data used to train the machine learning model is totally randomly generated. This is because I did not have access to relevant data. The prototype is merely used to show how we would go about implementing a lead scoring machine learning model. Since the data is randomly generated, this is why the machine learning model is not able to attain a high accuracy. Machine learning models looks for relationships between the Predictor Variables and the Target Variables. However, since out data is totally randomly generated, there is no significant relationship between them. This is why the accuracy is so low. In practical life, with data obtained from real life scenarios, the accuracy is expected to be much more.

# Runing the code
Runing the code is very simple. Just ensure you have python 3.12.3 or make a virtual environment with this version of python. If you have conda installed you can do this using the following code:
```
conda create --name myenv python=3.12.3
```
Once you have correct version of python installed, you can just run  the following line in you terminal (command prompt for windows):
```
pip install -r requirements.txt
```
This would install all the required libraries and you can run the code now. 
Note: Before runing the code, ensure that the current working directory is the directory in which the python script, the requirements.txt file, the README file and the dataset are stored.