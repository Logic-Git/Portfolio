# Markets-NLP:
This project is made to solve few problems using Natural Language Processing. In short, the project uses a dataset that contains several comments. The objective was to find whether the words 'gold' and 'silver' were used in the comments in the context of tradeable commodities. So for example if a sentence uses the phrase 'silver lining' then the solution must detect that the words 'gold' or 'silver have not been used as tradedable commodity in the sentence. The project uses a Recurrent Neural Network to solve the problem.

## Describing what is contained in the files:
* The task_description file contains information about the first problem. 
* The task_description_2 file contains infromation about the second problem.
* The sample.txt is the data that was provided by MarketPsych in relation to the first problem.
* The NLP_Task.ipynb file contains the solution to both the problems provided. 
* The articles_unlabelled.csv file contains the comtent of the sample.txt file written into a csv file.
* The articles_labelled.csv file contains data of the sample.txt file that was labelled using ChatGPT.
* The rnn.pth file is a Pytorch model that was trained by me for the task at hand explained in the Jupyter Notebook. This is given for the convinience of the evaluator if they want to evaluate the model without waiting for the entire training process.
* Further information of the approach used to solve all the tasks is given in the Jupyter Notebook
