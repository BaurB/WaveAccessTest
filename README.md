# WaveAccessTest
## DataFrameSummarizer

## Prerequisites
* Python >= 3.8.2
* pandas >= 1.1.2
* numpy >= 1.21.1

## Installation
git clone https://github.com/BaurB/WaveAccessTest.git
cd WaveAccessTest/dataframe_summarizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Usage
Explained in the Jupyter Notebook, but can be duplicated:
from dataframe_summarizer import DataframeSummarizer

new_df = StatisticalDescription(iris_df.columns)
new_df.populate_df(iris_df)
new_df.save_dataframe(iris_df, 'iris_dataset_stats')

## Run Test
Will include pytest
