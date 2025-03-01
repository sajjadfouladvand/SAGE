import pdb
import argparse
import sys
import os
import utils.extract_codes as ext_cd
import logging

sys.path.append(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument("--table_type", type=str, default='diagnosis', choices = ['diagnosis', 'medication', 'procedure', 'demographic'])    
parser.add_argument("--cohort", type=str, default='mci', choices = ['mci', 'non_mci'])    

parser.add_argument("--med_patient_id_field_name", type=str, default='anon_id')    
parser.add_argument("--med_code_field_name", type=str, default='medication_id')    
parser.add_argument("--med_time_field_name", type=str, default='order_time_jittered') 

parser.add_argument("--proc_patient_id_field_name", type=str, default='anon_id')    
parser.add_argument("--proc_time_field_name", type=str, default='ordering_date_jittered')    
parser.add_argument("--proc_code_field_name", type=str, default='proc_id')    

parser.add_argument("--icd10_field_name", type=str, default='icd10')    
parser.add_argument("--icd9_field_name", type=str, default='icd9')    
parser.add_argument("--diag_time_field_name", type=str, default='start_date_utc')    
parser.add_argument("--diag_patient_id_field_name", type=str, default='anon_id')    




parser.add_argument("--display_step", type=int, default=100000)    

client_name ="mining-clinical-decisions"
# parser.add_argument("--logging_milestone", type=int, default=1000)    
# logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', level = logging.INFO, filename = 'log/logfile_extract_streams.log', filemode = 'a')

if  parser.parse_args().table_type == "diagnosis" and parser.parse_args().cohort == 'mci':
    query_string = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.mci_all_diagnosis` A ORDER BY A.anon_id, A.start_date_utc LIMIT 10000"
    unique_icd10_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_icd10s` A WHERE A.icd10 is not NULL"
    unique_icd9_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_icd9s` A WHERE A.icd9 is not NULL"
    ext_cd.extract_diagnosis(client_name
                            , query_string
                            , unique_icd10_query
                            , unique_icd9_query
                            , parser.parse_args().cohort
                            , parser.parse_args().icd10_field_name
                            , parser.parse_args().icd9_field_name
                            , parser.parse_args().diag_time_field_name
                            , parser.parse_args().diag_patient_id_field_name                            
                            , parser.parse_args().display_step)
elif  parser.parse_args().table_type == "medication" and parser.parse_args().cohort == 'mci':
    query_string = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.mci_all_order_med` A ORDER BY A.anon_id, A.order_time_jittered LIMIT 10000"
    unique_medication_id_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_medication_ids` A WHERE A.medication_id is not NULL"
    ext_cd.extract_medication(client_name
                            , query_string
                            , unique_medication_id_query
                            , parser.parse_args().cohort
                            , parser.parse_args().med_code_field_name
                            , parser.parse_args().med_time_field_name
                            , parser.parse_args().med_patient_id_field_name                                                        
                            , parser.parse_args().display_step)

elif  parser.parse_args().table_type == "procedure" and parser.parse_args().cohort == 'mci':
    query_string = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.mci_all_order_proc` A ORDER BY A.anon_id, A.ordering_date_jittered LIMIT 100000"
    unique_proc_id_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_proc_ids` A WHERE A.proc_id is not NULL"    
    ext_cd.extract_procedure(client_name
                            , query_string
                            , unique_proc_id_query
                            , parser.parse_args().cohort
                            , parser.parse_args().proc_code_field_name
                            , parser.parse_args().proc_time_field_name
                            , parser.parse_args().proc_patient_id_field_name                             
                            , parser.parse_args().display_step)


elif  parser.parse_args().table_type == "diagnosis" and parser.parse_args().cohort == 'non_mci':
    query_string = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.non_mci_all_visited_neurology_diagnosis` A ORDER BY A.anon_id, A.start_date_utc LIMIT 100000"
    unique_icd10_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_icd10s` A WHERE A.icd10 is not NULL"
    unique_icd9_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_icd9s` A WHERE A.icd9 is not NULL"    
    ext_cd.extract_diagnosis(client_name
                            , query_string
                            , unique_icd10_query
                            , unique_icd9_query
                            , parser.parse_args().cohort
                            , parser.parse_args().icd10_field_name
                            , parser.parse_args().icd9_field_name
                            , parser.parse_args().diag_time_field_name
                            , parser.parse_args().diag_patient_id_field_name                            
                            , parser.parse_args().display_step)


elif  parser.parse_args().table_type == "medication" and parser.parse_args().cohort == 'non_mci':
    query_string = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.non_mci_all_visited_neurology_order_med` A ORDER BY A.anon_id, A.order_time_jittered LIMIT 10000"
    unique_medication_id_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_medication_ids` A WHERE A.medication_id is not NULL"    
    ext_cd.extract_medication(client_name
                            , query_string
                            , unique_medication_id_query
                            , parser.parse_args().cohort
                            , parser.parse_args().med_code_field_name
                            , parser.parse_args().med_time_field_name
                            , parser.parse_args().med_patient_id_field_name                                                        
                            , parser.parse_args().display_step)

elif  parser.parse_args().table_type == "procedure" and parser.parse_args().cohort == 'non_mci':
    query_string = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.non_mci_all_visited_neurology_order_proc` A ORDER BY A.anon_id, A.ordering_date_jittered LIMIT 100000"
    unique_proc_id_query = "SELECT * FROM `mining-clinical-decisions.proj_sage_sf.unique_proc_ids` A WHERE A.proc_id is not NULL"        
    ext_cd.extract_procedure(client_name
                            , query_string
                            , unique_proc_id_query
                            , parser.parse_args().cohort
                            , parser.parse_args().proc_code_field_name
                            , parser.parse_args().proc_time_field_name
                            , parser.parse_args().proc_patient_id_field_name                             
                            , parser.parse_args().display_step)