# Iris flower variety and wine quality prediction

**Course:** Scalable Machine Learning and Deep Learning - Lab 1

**Team Limoncello**: Iga Pawlak, Julien Horvat

## 1. Iris flower pipeline

This part was already entirely coded. We created a Hopsworks shared project and ran the dataset creation notebook and the training notebook, managing the Hopsworks secret key. Then we add the key on github and set up the daily routines with github action. They are both working on this directory and triggered once a day. 
Finally, we launched two `huggingface` apps : 
* [Iris prediction app](https://huggingface.co/spaces/PiJul/Iris_prediction), which import the model from hopsworks and infer on the set of values chosen by the user on the web interface.
* [Iris inference monitor](https://huggingface.co/spaces/PiJul/Iris-monitor), which summarize the latest predictions made by the batch routine, as well as ploting a confusion matrix.

## 2. Wine quality prediction 
### 2.1. Feature group creation and feature engineering 

In the first phase it was necessary to load and prepare the data for training. A few operations were performed on the data
* the `NaN` values have been replaced with random numbers
* the *white* and *red* values for `type` were replaced with `0.0` and `1.0` respectively

**2.1.1. Feature selection**

To limit the number of features used for prediction we have used methods provided in `sklearn` library. We have tested two functions and evaluated them in terms of model accuracy 
* `SelectKBest` - an univariate method which drops all features but one and tests prediction results on the basis of only this one feature. Then selects $K$ best ones. 
* `RFE` - drops subsets of features, tests how the prediction works using each combination $K$ features and selects the best subsets. 

We ran the experiments for both methods for the number of features $K = 2, ..., 9$. The results are visible in the table below.

| Features \ Method | `RFE` | `SelectKBest` |  
 | :---: | :---: | :---: |
| 2 | 0.8859229413246034 | 0.8627549735582977 | 
| 3 | 0.9060690002518257 | 0.9100982120372703 | 
| 4 | 0.9148829010324855 | 0.9098463863006799 | 
| 5 | 0.91891211281793 | 0.9176529841349786 | 
| 6 | 0.9209267187106522 | 0.9211785444472425 | 
| 7 | 0.9320070511206245 | 0.9224376731301939 | 
| 8 | 0.9257114077058676 | 0.9151347267690758 | 
| 9 | 0.9277260135985897 | 0.9347771342231176 | 

We can see that from $3$ features we already get an accuracy of over $90\%$. We have decided to use `RFE` with $7$ features. 

**2.1.3 Uploading to a Feature Group**

The data frame has been uploaded to a `wine` Feature Group in our Hopsworks project. 
### 2.2 Feature daily pipeline
Generates random samples of wine of a given quality. The quality is randomly chosen from the values present in the data, from $3$ to $9$. Then the value in each column is also randomly selected from the values in this column present for existing samples with a given quality. 
### 2.3 Training pipeline 
**2.3.1 Over sampling the dataset**

Looking at the number of samples for each quality present in the original dataset we can see that some classes are severely under sampled. The most numerous class is $6$ with $2836$ samples, while class $9$ is only represented by $9$ samples. 
Therefore, to provide for effective training we used a `RandomOverSampler` that samples for  the underrepresented classes more times and randomly to achieve a more even number of training examples. 

**2.3.2. Model selection**

We have tested three models - `KNeighborsClassifier`, `RandomForestClassifier` and `AdaBoostClassifier` and found that the second one provides the best results.  This was the model trained on the dataset and achieving around 90% accuracy on the test set. 

**2.3.3. Uploading the model**

The model has been uploaded to the model registry as `wine_model` in our Hopsworks project. 

### 2.3 Batch inference pipeline 

### 2.4 Wine quality prediction app 

We have created an app on `Huggingface` available [here](https://huggingface.co/spaces/PiJul/Wine_quality_prediction) similar to the one for the Iris flower prediction. The user can input a value for each feature and the default values are simply averages for each column in the entire data frame. 
Upon prediction a picture with the result is displayed. ![obraz|400](https://github.com/Seyoooo/SMLlab/assets/36933957/ce568bc8-a466-4844-9fd4-e1507da721e3)

### 2.5 Wine prediction monitor app

