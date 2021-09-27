from telemanom.ESN import SimpleESN

from telemanom.ESNnoserializzazione import ESNnoser
import pandas as pd
from telemanom.channel import Channel
from telemanom.helpers import Config
import time
from tensorflow.keras.callbacks import History, EarlyStopping
from functools import reduce
import logging
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import tensorflow as tf
tf.autograph.set_verbosity(0)

#logs
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.basicConfig(filename="tests.log", level=logging.INFO)

epochs = 150
units=850
input_scaling=1
spectral_radius=0.99
leaky=0.8
layers=1


def esn_noserializzazione(config):
    model = ESNnoser(config=config,
                      units=units,
                      input_scaling=input_scaling,
                      spectral_radius=spectral_radius,
                      leaky=leaky,
                      layers=layers,
                      circular_law=True,
                      )

    start_time = time.time()
    model.build(input_shape=(channel.X_train.shape[0], channel.X_train.shape[1], channel.X_train.shape[2]))
    end_time = time.time() - start_time
    time_string = secondsToStr(end_time)
    logging.info("Tempo build con circular law: {}".format(time_string))

    model2 = ESNnoser(config=config,
                     units=units,
                     input_scaling=input_scaling,
                     spectral_radius=spectral_radius,
                     leaky=leaky,
                     layers=layers,
                     circular_law = False,
                     )

    start_time = time.time()
    model2.build(input_shape=(channel.X_train.shape[0], channel.X_train.shape[1], channel.X_train.shape[2]))
    end_time = time.time() - start_time
    time_string = secondsToStr(end_time)
    logging.info("Tempo build senza circular law: " + time_string)



def secondsToStr(t):
    return "%dh:%02dm:%02ds.%03dms" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])



import tensorflow as tf

config_path = "config.yaml"
config = Config(config_path)

chan_df = pd.read_csv("labeled_anomalies.csv")

cbs = [History(), EarlyStopping(monitor='val_loss',
                                        patience=config.patience,
                                        min_delta=config.min_delta,
                                        verbose=0)]
columns = ["model", "init time", "build time", "write/read time", "fit time"]
df = pd.DataFrame(columns=columns)

for i, row in chan_df.iterrows():
    chan_id = row.chan_id

    if chan_id != "P-10":
        continue

    channel = Channel(config, row.chan_id)
    channel.load_data()

    logging.info("Channel name: "+chan_id)
    logging.info("Number of sequences: "+str(len(channel.X_train)))

    #si precalcolo no serializzazione
    esn_noserializzazione(config)

    break




