from datasets import load_dataset
import pandas as pd
import itertools
import os

os.makedirs("../amelia", exist_ok=True)

print("Streaming first 20k rows...")

ds = load_dataset(
    "AmeliaCMU/Amelia42-Mini",
    split="train",
    streaming=True
)

sample=list(itertools.islice(ds,20000))

df=pd.DataFrame(sample)

df.to_csv("../amelia/amelia42_sample_20k.csv",index=False)

print("Done")