# Stock-Forecasting
Given a dataset of a fictional universe of companies with quarterly financial data, build a model to predict whether the stock of a given company will generate a positive return in the next quarter (i.e. whether the stock price will rise or fall).

## Methodology

#### Data Exploration : DataExploration.ipynb

1.Investigated correlation between features

2.Visualized features for each company to observe anomalies and patterns. Examined company-specific characteristics and market-wide patterns.

3.Identified data quality issues (missing values, anomalies)

4.Checked the stationarity of the data.

The jupyter notebook contains detailed results and comments


**Data Preprocessing**: DataPreprocessing.py, Utils.py, Preprocessing.ipynb

**Original dataset**: dataset.csv

**Preporcessed dataset**: dataset_preprocessed.csv

1.Handled missing values using forward-backward averaging

2.Corrected anomalies (e.g., negative prices)

3.Created the target variable (binary indicator of price increase/decrease)

The jupyter notebook contains detailed results and comments

### Modeling Approaches
1. **Random Forest**  : RandomForest.ipynb
2. **Temporal Fusion Transformer (TFT)**  : TFTModel.ipynb
3. **LSTM**  : LSTMModel.ipynb

All descriptions, reasonings and comments in TFTModel.ipynb, LSTMModel.ipynb, RandomForest.ipynb files

### Evaluation approaches used:
Confusion matrix
Accuracy
Precision, Recall anf F1-score

#### Comparative Analysis:
The best results were obtained with TFT and LSTM. Although the accuracy remains very similar in all the 3 cases.
But since the data is not balanced (rise in stocks is almost double then the fall in stocks).
Therefore, confusion matrix is used for comparison purpose. 


