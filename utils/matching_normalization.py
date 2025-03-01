import pdb
import pandas as pd
from sklearn.model_selection import train_test_split

def matching(mci_stationary_data_path
			,non_mci_stationary_data_path			
			,mci_metadata_path
			,non_mci_metadata_path
			,case_control_ratio
			,matching
			):
	# pdb.set_trace()

	mci_data = pd.read_csv(mci_stationary_data_path)
	non_mci_data = pd.read_csv(non_mci_stationary_data_path)

	# Match based on age and sex
	case_metadata = pd.read_csv(mci_metadata_path)
	control_metadata = pd.read_csv(non_mci_metadata_path)
	control_metadata['matched'] = 0

	control_metadata['byear'] = control_metadata['bdate'].str[:4]
	case_metadata['byear'] = case_metadata['bdate'].str[:4]

	for idx, row in case_metadata.iterrows():
		matched_controls = control_metadata.loc[(control_metadata['sex'] == row['sex']) & (control_metadata['byear'] == row['byear']) & (control_metadata['matched'] ==0)]
		if matched_controls.shape[0] >= case_control_ratio:
			control_metadata.loc[matched_controls.index[:case_control_ratio], 'matched'] = 1
		else:
			pdb.set_trace()
			print('Couldnt find any match!')	
		# print('Test')
	control_metadata_matched = control_metadata[control_metadata['matched']==1]
	control_metadata_matched.to_csv(non_mci_metadata_path[:-4]+'_matched.csv', index=False)
	pdb.set_trace()
	non_mci_data_matched = non_mci_data[non_mci_data['Patient_ID'].isin(control_metadata_matched['anon_id'].values.tolist())]

	all_data = mci_data.append(non_mci_data_matched, ignore_index=True).sample(frac=1).reset_index(drop=True)

	all_data.to_csv('stationary_data/stationary_data_imbratio'+str(case_control_ratio)+'.csv', index=False)

	return 'stationary_data/stationary_data_imbratio'+str(case_control_ratio)+'.csv'

def normalization(data_path
				,test_ratio
				):
	pdb.set_trace()
	epsil = 2.220446049250313e-16
	round_precision = 5
	data = pd.read_csv(data_path)

	mins = data.iloc[:,1:].min()
	maxes = data.iloc[:,1:].max()

	normalized_data=(data.iloc[:,1:] -mins)/((maxes-mins) + epsil)
	normalized_data['Patient_ID'] = data['Patient_ID']
	normalized_data['Label'] = data['Label']
	normalized_data.round(round_precision).to_csv(data_path[:-4]+'_normalized.csv', index=False)

	trainset, testset = train_test_split(normalized_data, test_size = test_ratio, shuffle=False)

	trainset.to_csv(data_path[:-4]+'_normalized_train.csv', index=False)
	testset.to_csv(data_path[:-4]+'_normalized_test.csv', index=False)

