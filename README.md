# WaveAccessTest
## 1.DataFrameSummarizer

## Prerequisites
* Python >= 3.8.2
* pandas >= 1.1.2
* numpy >= 1.21.1

## Installation

```
git clone https://github.com/BaurB/WaveAccessTest.git
cd WaveAccessTest/dataframe_summarizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
Explained in the Jupyter Notebook, but can be duplicated:
from dataframe_summarizer import DataframeSummarizer

```
new_df = StatisticalDescription(iris_df.columns)
new_df.populate_df(iris_df)
new_df.save_dataframe(iris_df, 'iris_dataset_stats')
```

## Run Test
Loads the Iris dataset and check whether it has the right dimensions. Examples of saving the dataframe are in Jupyter Notebook. 
```
pytest . -v --cov=dataframe_summarizer
```

## 2. ML Project 
## Prerequisites
* Python >= 3.8.2
* pandas >= 1.1.2
* numpy >= 1.21.1
* seaborn >= 0.11.1
* catboost >= 1.0.0
* matplotlib >= 3.4.2
* xgboost >= 1.4.2
* sklearn >= 1.0
* lightgbm >= 3.3.0

## Task:
Бинарная классификация: предсказать получает ли определенный человек больше или меньше определенной суммы

## Data:
Исходные данные лежат в директории test_task_ml

Описание:

Название столбца | Тип признака
------------- | -------------
 age  | Numerical
workclass  | Categorical
 final_weight  | Numerical
 education  | Categorical
education-num| Numerical
marital-status| Categorical
 occupation  | Categorical
race  | Categorical
sex| Categorical
cap-gain | Numerical
cap-loss| Numerical
hours-per-week  | Numerical
native-country| Categorical

## Output:
Two output files
`output_catboost.txt`-prediction using the `catboost` model
`output_lgbm.txt`-prediction using the `lgbm` model
