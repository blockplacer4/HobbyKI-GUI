import pandas as pd

data = pd.read_csv('train.csv')
samples = []

for row in data['text']:
    sample = {
        "inputs": row
    }
    samples.append(sample)
