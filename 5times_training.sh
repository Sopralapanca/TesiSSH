#!/bin/bash
for i in {1..5}; do CUDA_VISIBLE_DEVICES=2 python example.py -l labeled_anomalies.csv; done