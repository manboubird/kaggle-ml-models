#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import xgboost as xgb
import gc

def load_data_file(pickle_path, csv_file):
    v = None
    if os.path.exists(pickle_path):
        print('Loading pickled file: ' + pickle_path)
        v = pd.read_pickle(pickle_path)
    else:
        print('Loading csv file: ' + csv_file)
        v = pd.read_csv(csv_file)
        for c, dtype in zip(v.columns, v.dtypes):
            if dtype == np.float64:
                print('Convert float64 to float32: ' + c)
                v[c] = v[c].astype(np.float32)
        print('Saveing as pickled file: ' + pickle_path)
        v.to_pickle(pickle_path)
    return v 


INPUT_DIR = './input'

TRAIN_CSV = 'train_2016_v2.csv'
PROP_CSV = 'properties_2016.csv'
SAMPLE_CSV = 'sample_submission.csv'
RESULT_CSV = 'xgb_starter.csv'

print('Loading data ...')
train, prop, sample = [ load_data_file("%s/%s.p" % (INPUT_DIR, x), "%s/%s" % (INPUT_DIR, x)) for x in [TRAIN_CSV, PROP_CSV, SAMPLE_CSV] ]


print('Feature engineering ...')
prop['bedfullbathratio'] = prop['bedroomcnt'] / prop['fullbathcnt']


print('Creating training set ...')
df_train = train.merge(prop, how='left', on='parcelid')

x_train = df_train.drop(['parcelid', 'logerror', 'transactiondate', 'propertyzoningdesc', 'propertycountylandusecode'], axis=1)
y_train = df_train['logerror'].values
print(x_train.shape, y_train.shape)

train_columns = x_train.columns

for c in x_train.dtypes[x_train.dtypes == object].index.values:
    x_train[c] = (x_train[c] == True)

del df_train; gc.collect()

split = 80000
x_train, y_train, x_valid, y_valid = x_train[:split], y_train[:split], x_train[split:], y_train[split:]


print('Building DMatrix...')
d_train = xgb.DMatrix(x_train, label=y_train)
d_valid = xgb.DMatrix(x_valid, label=y_valid)

del x_train, x_valid; gc.collect()


print('Training ...')
params = {}
params['eta'] = 0.02
params['objective'] = 'reg:linear'
params['eval_metric'] = 'mae'
params['max_depth'] = 4
params['silent'] = 1

watchlist = [(d_train, 'train'), (d_valid, 'valid')]
clf = xgb.train(params, d_train, 10000, watchlist, early_stopping_rounds=100, verbose_eval=10)

del d_train, d_valid


print('Building test set ...')
sample['parcelid'] = sample['ParcelId']
df_test = sample.merge(prop, on='parcelid', how='left')

del prop; gc.collect()

x_test = df_test[train_columns]
for c in x_test.dtypes[x_test.dtypes == object].index.values:
    x_test[c] = (x_test[c] == True)

del df_test, sample; gc.collect()

d_test = xgb.DMatrix(x_test)

del x_test; gc.collect()


print('Predicting on test ...')
p_test = clf.predict(d_test)

del d_test; gc.collect()

sub = pd.read_csv("%s/%s" % (INPUT_DIR, SAMPLE_CSV))
for c in sub.columns[sub.columns != 'ParcelId']:
    sub[c] = p_test

print('Writing csv: ' + RESULT_CSV)
sub.to_csv(RESULT_CSV, index=False, float_format='%.4f') # Thanks to @inversion
