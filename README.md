
<h1 style="font-size:60px;">Pre-processing</h1>

Run the following python scripts to extract some metadata on both mci and non-mci cohorts. This scripts read from ```all_new_patients_in_neurology_mci_diagnosis```, ```all_new_patients_in_neurology_mci_demographic```,```all_new_patients_in_neurology_nonmci_diagnosis``` and  ```all_new_patients_in_neurology_nonmci_demographic``` tables and create metadata files for both cases and controls under ```intermediate_files``` directory: ```mci_metadata.csv``` and ```nonmci_metadata.csv```.

```
python3 main_create_metadata.py --cohort mci
python3 main_create_metadata.py --cohort nonmci
```
Use the following script to extract diagnosis, medication and procedure codes for mci and non-mci cohorts:
```
python3 main_extract_codes.py --table_type diagnosis --cohort mci
```
In this command:
```
table_type: It defines what type of features to extract and it can be diagnosis, medication or procedure. 
cohort: Can be either mci or nonmci and it defines the cohort to extract table_type features for.
```
Note, change ```table_type``` and ```cohort``` values accordingly to extract all features:
```
python3 main_extract_codes.py --table_type diagnosis --cohort mci
python3 main_extract_codes.py --table_type medication --cohort mci
python3 main_extract_codes.py --table_type procedure --cohort mci

python3 main_extract_codes.py --table_type diagnosis --cohort nonmci
python3 main_extract_codes.py --table_type medication --cohort nonmci
python3 main_extract_codes.py --table_type procedure --cohort nonmci

```
Running the above commands will create diagnosis, medication and procedure files for both mci and nonmci cohorts seperately under ```intermediate_files``` directory. Each line in each file (diagnosis file for example) represent one patient and the format is: PATIENT ID, TIMESTAMP, CODES (diagnosis, procedure or medication codes; depending on which file you are looking into), EOV tocken, .... . In fact, the first entry is patient ID, and then we store timestapm and the codes that occured on that time followed by a 'EOV' tocken. This pattern is repeated for all timestamps. 

After extracting the codes, run the follwoing commands to convert the longitudinal data to stationary data for both mci and nonmci cohorts which is more approperiate for training classical ML models:
```
python3 main_create_stationary.py --cohort mci
python3 main_create_stationary.py --cohort nonmci
```
Here is a list of argument that you can use when running the above commands to change the default settings:
```
prediction_window_size: This is to control how many months prior to the onset of MCI you wantto predict it. Default value is 6 months. 
top_n_med: The number of top-n frequent medication codes you want to use to build the feature matrix (number of medication code predictors). Default is 10.
top_n_proc: The number of top-n frequent procedure codes you want to use to build the feature matrix (number of procedure code predictors). Default is 10.
top_n_icd10: The number of top-n frequent ICD10 codes you want to use to build the feature matrix (number of diagnosis code predictors). Default is 10.
top_n_icd9: The number of top-n frequent ICD9 codes you want to use to build the feature matrix (number of diagnosis code predictors). Default is 0.
```
Note, these command create stationary data for both mci and nonmci cohorts under ```stationary_data``` directory as well as a log file under ```log``` directory. 

Now run the following commands to perform case adn control matching, normalization and creating train and test sets:
```
python3 main_matching_normalization.py
```
You can control the train and tes set size ratios and case to control ratios in training and testing sets using:
```
test_ratio: Default value is 0.3 (meaning that 30 percent of the data will be used for testing and 70 percent for training and validation).
case_control_ratio: The default value is 1 (meaning that for each case 1 control will be matched based on age and sex)
```
<h1 style="font-size:60px;">Model training</h1>
Now the data is ready to train a classical machine learning model such as random forest:

```
python3 main_ml_models.py --ml_model rf
python3 main_ml_models.py --ml_model lr
python3 main_ml_models.py --ml_model xgb
```
Use the following command to test the models using imbalanced test sets:

```
python3 main_ml_models.py --imb_test 1
```

<h1 style="font-size:60px;">3. Visualization</h1>
Use the following script to plot tSNE diagram of the stationary features:

```
python3 main_visualization.py --viz_method tsne
python3 main_visualization.py --viz_method pca   
```
And for computing basic stats:

```
 python3 main_visualization.py --compute_table_1 1
```
<h1 style="font-size:60px;">Recommender system</h1>
First, create stationary data for the recommender system:

```
python3 main_create_stationary.py --recommender for_recommender_ --prediction_window_size 2 --cohort mci
python3 main_create_stationary.py --recommender for_recommender_ --prediction_window_size 2 --cohort nonmci

```

Then
```
python3 main_create_data_treatment_recommendation.py
```


