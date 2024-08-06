# Introduction
This directory stores all the code that I wrote during some machine leraning courses I took from Kaggle. After we learnined Machine Learning skills in the courses, we had to use them to make submissions to a Kaggle Competition about building a model to predict prices of houses. 

As you go through the course and learn new concepts, and apply them to the competition, you see your score in the competition improve. Each notebook in this directory reflect code that was used to make a submission to the competition. Moreover, they are ordered, with the number in brackets reflecting when they were submitted compared to other notebooks. So for example, **Intro to ML Kaggle (1)** was the first submission to the competition, while **exercise-missing-values (2)** was the second submission to the competition and resulted in an immprovement in score. This can be seen from the numbers **(1)** and **(2)** respectivevly.

In this way, anyone interested in the code can view how scores in Kaggle competitions (or how accuracies of machine learning models in general) are improved. Moreover, they can just directly jump to the file with the highest number to see my highest scoring code if they are interested in that.

**Note: Not all the code written in the notebooks was written by me. The notebooks were made by course instructors with blank parts at various places. Therefore, they already contained code for simple things like importing libraries and I had to fill in the code for more involved parts of the notebook where we had to apply the machine learning concpts taught in the course.** 

**Note: Also, the viewer cannot download this code and run it directly on their computer. This is because the repository does not contain the data that was read at the start of the code to run the preprocessing commands on it or train the machine learning model. Therefore, if trying to download these notebooks and run on your local machine, they would give an error at the very start. The purpose of this is to only help the viewer learn different techniques that are used to build machine learning models. If you want to experiment with this code, you will have to obtain approporiate data and then modify the code to read it using the notebook and then experiment with the techniques.**

More information about the code in each notebook is given below.

## Intro to ML Kaggle (1):
This notebook reflects the code resulting from the learnings from the first, introductory, course on Kaggle. The code employs conccepts like simpley using a **Random Forrest Regressor** to make predictions and using metrics like **Mean Absolute Error** to check if the model is working well or not.

## exercise-missing-values (2):
In the code in this notebook, I tested different ways to deal with missing values in the data before training a machine learning model on it. Then, I chose the method of dealing with missing values that gave the best result to make a submission to the competition. 

## exercise-categorical-variables (3):
This notebook experiments with different ways to deal with categorical variable while training machine learning models. 

## exercise-pipelines (4):
This notebook experiments with using pipelines in sciki-learn to make the code for training a Random Forrest Regressor on the data simpler.

## exercise-cross-validation (5):
In this code, I demonstrate using cross-validation while training a machine learning model.

## exercise-xgboost (6):
In this notebook, I implement the Extreme Gradient Boosting algorithm to train a machine learning model ont he same data I have been using in all the other tutorials. This algorithm provides state-of-the-art accuracy in most machine leraning competitions and applications. The notebook also demonstrates experimenting with the hyper-parameters that are set before running the algorithm. In this way, it can give the reader idea as to how to set the hyper-parameters when they want to maximize accuracy because doing this can greatly improve the accuraacy of the final model compared to if you just run the algorithm on default hyper-parameter and settings.

