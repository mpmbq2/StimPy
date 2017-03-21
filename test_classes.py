import pandas as pd
import db_classes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


df = pd.read_csv('/home/matt/Data/patch_data/dyn1/170221/meta.csv')

db_classes.NeuronPair(file_list=df['file'][df['pair'] == 2],
                   file_path='/home/matt/Data/patch_data/dyn1/170221/',
                   genotypes=('wt', 'wt'),
                   transmitters=('gaba', 'gaba'))
