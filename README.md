# Automatic Ticket Classification

The dataset used for the model training: /kaggle/input/automatic-ticket-classification-dataset/Automatic-Ticket-Classification-Dataset/complaints-2021-05-14_08_16.json

Previous art used for the model evaluating: https://www.kaggle.com/code/abhishek14398/automatic-ticket-classification-case-study

RestFull API service that can automatically classify customer complaints based on the products and services that the ticket mentions.

In this project, we improved the classification model of incoming requests to the bank's technical support. As part of the data preprocessing, the clustering of appeals by the most popular categories has already been carried out, the main categories to which the appeal may belong have been identified.

## Results

<table>
<tr>
<th>Base model</th>
<th>Accuracy</th>
</tr>
<tr><td>Sequental</td><td>0.98</td></tr>
<tr><td>Logistic regression</td><td>0.90</td></tr>
</table>

## Authors

* Konstantin Gorbunov
* Ilya Maloglazov