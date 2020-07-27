import os
os.environ["MKL_NUM_THREADS"]="1"
print(os.environ["MKL_NUM_THREADS"])

import numpy as np
import turbofats
import pickle
import sys
from pathlib import Path
import pandas as pd
#from joblib import Parallel, delayed, dump

#result = Parallel(n_jobs=10)(delayed(compute_fats_features)(batch_names) for batch_names in split_list_in_chunks(file_list, 100))


def compute_fats_features(df_data):
    """
    Receives a dataframe with the detections
    
    Returns a dataframe with the features
    """
    # TODO: STUDY BIASED FEATURES
    feature_list = ['Amplitude', 'AndersonDarling', 'Autocor_length',
            'Beyond1Std',
            'Con', 'Eta_e',
            'Gskew',
            'MaxSlope', 'Mean', 'Meanvariance', 'MedianAbsDev',
            'MedianBRP', 'PairSlopeTrend', 'PercentAmplitude', 'Q31',
            'PeriodLS_v2',
            'Period_fit_v2', 'Psi_CS_v2', 'Psi_eta_v2', 'Rcs',
            'Skew', 'SmallKurtosis', 'Std',
            'StetsonK', 'Harmonics',
            'Pvar', 'ExcessVar',
            'GP_DRW_sigma', 'GP_DRW_tau', 'SF_ML_amplitude', 'SF_ML_gamma',
            'IAR_phi',
            'LinearTrend',
            'PeriodPowerRate']
    
    lc_ids = df_data.index.unique()
    feature_space = turbofats.NewFeatureSpace(feature_list=feature_list, 
                                              data_column_names=["mag", "mjd", "err"])
    features_all = []
    for k, lc_id in enumerate(lc_ids):
        if np.mod(k, 1000):
            print(k, len(lc_ids), k/len(lc_ids))
            
        df_lc = df_data.loc[lc_id]
        df_lc = df_lc.rename(columns={"flux": "mag", "flux_err": "err"}, errors="raise")
        features = []
        for fid in range(6):
            df_lc_fid = df_lc.loc[df_lc.passband == fid]
            #print(df_lc_fid.shape[0])
            #if df_lc_fid.shape[0] > 60: # Adjust this
            df_features_single_band = feature_space.calculate_features(df_lc_fid[["mag", "mjd", "err"]])
            #else:
            #    df_features_single_band = pd.DataFrame(np.nan, 
            #                                           index=[lc_id], 
            #                                           columns=feature_list)
            #print(df_features_single_band)
                
            df_features_single_band = df_features_single_band.rename(lambda x: x+"_"+str(fid), axis='columns')
            features.append(df_features_single_band)                
            
        features_all.append(pd.concat(features, axis=1, sort=True))
    features_all = pd.concat(features_all, axis=0, sort=True)
    features_all.index.name = 'object_id'
    return features_all
            



def populate_feature_folder(path):
    print(f"Looking for plasticc data at {path}")
    p = Path(path)    
    data_paths = sorted(p.glob('plasticc_test_set_batch*.csv'))
    data_paths = list(p.glob('plasticc_train_lightcurves.csv')) + data_paths
    print(f"Found {len(data_paths)} csv files at given path")
    
    
    if len(data_paths) > 0:
        # Create light_curves folder if it does not exist
        (p / 'features').mkdir(parents=True, exist_ok=True)
    

    for data_path in data_paths:
        print(f"Creating features from {data_path.name}")
        df_data = pd.read_csv(data_path).set_index("object_id")        
        
        df_features = compute_fats_features(df_data)
        feature_file = p / 'features' / f'{data_path.name}.pkl'
        with open(feature_file, 'wb') as f:
            pickle.dump(df_features, f, protocol=4)
        break
                    
                    
if __name__ == "__main__":
    assert len(sys.argv) == 2, "Please give the path to the uncompressed plasticc CSVs"
    path = sys.argv[1] #"/home/shared/astro/PLAsTiCC/"
    populate_feature_folder(path)