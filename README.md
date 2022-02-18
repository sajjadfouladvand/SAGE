<h1 style="font-size:60px;">1. Extracting case and control cohorts using big query scripts</h1>

Use the following script to extract all patients who have visited neurology department as a new patient and save the results ina big query table ```all_new_patients_in_neurology``` (at the moment 8,496 patients). 

```
WITH
    SP AS
        (
            select enc.anon_id, enc.pat_enc_csn_id_coded as SP_enc, enc.appt_when_jittered as SP_app_datetime --, DX.icd10
            from `mining-clinical-decisions.shc_core.encounter` as enc 
            join `mining-clinical-decisions.shc_core.dep_map` as dep on enc.department_id = dep.department_id    
            where dep.specialty_dep_c = '19' -- dep.specialty like '%NEUROLOGY%'
            AND visit_type like 'NEW PATIENT%' -- Naturally screens to only 'Office Visit' enc_type 
            AND appt_status = 'Completed'
        ),

 COHORT AS
  (
  SELECT SP.*
  FROM SP 
)

SELECT DISTINCT COHORT.anon_id
FROM COHORT 
```
From the cohort generated using the above script, you can select patients who have never had any MCI diagnosis code using:
```
(SELECT DISTINCT A.anon_id
    FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology` A
    )
EXCEPT DISTINCT 
(
SELECT DISTINCT B.anon_id
    FROM `mining-clinical-decisions.shc_core.diagnosis_code` B
    WHERE (B.icd10 = 'G31.84'
        OR B.icd10 = 'F09'
        OR B.icd9 = '331.83'
        OR B.icd9 = '294.9')
GROUP BY B.anon_id )
```
This (at the moment) resulted in 7,875 patients and we saved them under ```all_new_patients_in_neurology_nonmci``` table. Then, use the following scripts to extract mci patients within the cohort of new patients in neurology:
```
(SELECT DISTINCT A.anon_id
    FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology` A
    )
EXCEPT DISTINCT 
(
SELECT DISTINCT B.anon_id
    FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_nonmci` B
)
```
This resulted in 621 patients. The results were saved under ```all_new_patients_in_neurology_mci```. 

Extract diagnosis, medication, procedure and demographic records for non-mci patients in ```all_new_patients_in_neurology_nonmci```:
```
-- Diagnosis saved under all_new_patients_in_neurology_nonmci_diagnosis
SELECT DG.*
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_nonmci` N
INNER JOIN `mining-clinical-decisions.shc_core.diagnosis_code` DG
ON N.anon_id = DG.anon_id

-- Saved under all_new_patients_in_neurology_nonmci_order_med
SELECT *
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_nonmci` N
INNER JOIN `mining-clinical-decisions.shc_core.order_med` M
ON N.anon_id = M.anon_id

-- Saved under all_new_patients_in_neurology_nonmci_order_proc
SELECT *
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_nonmci` N
INNER JOIN `mining-clinical-decisions.shc_core.order_proc` P
ON N.anon_id = P.anon_id

-- Demographics saved under all_new_patients_in_neurology_nonmci_demographic
SELECT *
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_nonmci` N
LEFT JOIN `mining-clinical-decisions.shc_core.demographic` DM
ON N.anon_id = DM.anon_id
```
And similarly for the mci cohort:
```
-- Diagnosis saved under all_new_patients_in_neurology_mci_diagnosis
SELECT DG.*
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_mci` N
INNER JOIN `mining-clinical-decisions.shc_core.diagnosis_code` DG
ON N.anon_id = DG.anon_id

-- Saved under all_new_patients_in_neurology_mci_order_med
SELECT *
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_mci` N
INNER JOIN `mining-clinical-decisions.shc_core.order_med` M
ON N.anon_id = M.anon_id


-- Saved under all_new_patients_in_neurology_mci_order_proc
SELECT *
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_mci` N
INNER JOIN `mining-clinical-decisions.shc_core.order_proc` P
ON N.anon_id = P.anon_id


-- Demographics saved under all_new_patients_in_neurology_mci_demographic
SELECT *
FROM `mining-clinical-decisions.proj_sage_sf.all_new_patients_in_neurology_mci` N
LEFT JOIN `mining-clinical-decisions.shc_core.demographic` DM
ON N.anon_id = DM.anon_id
```
Finally, use the following scripts to find unique ICD10s, ICD9s, medication IDs and procedure IDs and saved them into ```unique_icd10s, unique_icd9s, unique_medication_ids, unique_proc_ids```. These tables will be used later in the feature extraction steps.
```
SELECT DISTINCT A.icd10
FROM `mining-clinical-decisions.shc_core.diagnosis_code` A


SELECT DISTINCT A.icd9
FROM `mining-clinical-decisions.shc_core.diagnosis_code` A


SELECT DISTINCT A.medication_id
FROM `mining-clinical-decisions.shc_core.order_med` A


SELECT DISTINCT A.proc_id
FROM `mining-clinical-decisions.shc_core.order_proc` A
```
<h1 style="font-size:60px;">2. Pre-processing</h1>

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

Now the data is ready to train a classical machine learning model such as random forest:
```
python3 main_ml_models.py
```
<h1 style="font-size:60px;">3. Visualization</h1>
Use the following script to plot tSNE diagram of the stationary features:
```
python3 main_visualization.py --viz_method tsne
python3 main_visualization.py --viz_method pca   
```
