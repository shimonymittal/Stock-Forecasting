import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class Utils:

  def read_csv(self):
    df = pd.read_csv('dataset.csv')  # hard coded, change to variable
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(['Company', 'Date'], inplace=True)
    return df

  # function to get all the information needed
  def information_func(self, df):
    print("Unique companies in dataset:", df['Company'].nunique())
    print("----"*20)

    # metadata of dataset
    print("Metadata of the dataset:\n")
    df.info()
    print("----"*20)

    # missing values
    null = df.isnull().sum()
    print(null)
    print("----"*20)

  def create_dict_of_dataframes_for_each_company(self, df):
      company_dict = {}
      for company in df['Company'].unique():
        company_dict[company] = df[df['Company']== company]
      return company_dict

  # The data contains duplicates in Date column, since the stocks are recorded quarterly for 25 years,
  # the data per company should be 25*4 = 100, therefore removing duplicates
  def plot_size_histogram_of_company(self, df):
      df.groupby('Company').size().plot.hist()
      plt.xlabel("Rows / Dataframe")
      plt.ylabel("Frequency")
      plt.legend(loc='upper right')
      fig = plt.gcf()

  def combine_dict_dataframes(self, company_dict):
    dfs_to_combine = []
    for company, df in company_dict.items():
      dfs_to_combine.append(df)
    combined_df = pd.concat(dfs_to_combine, ignore_index=True)

    # Sort by Company and Date if Date column exists
    if 'Date' in combined_df.columns:
        combined_df = combined_df.sort_values(['Company', 'Date'])

    return combined_df

  def check_if_any_column_value_null(self, company_dict):
    for _, df in company_dict.items():
      columns_with_nan = df.columns[df.isnull().any()].tolist()
    print("The list of columns having null values : ",columns_with_nan)
