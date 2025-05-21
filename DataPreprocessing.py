import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessing:

  def drop_dupicates(self, company_dict, company_data, verbose=True):
    # Validation checks
    if verbose:
      total_rows = sum(len(df) for df in company_dict.values())
      expected_total_datarows = 25*4*200   # Quarterly analysis in 25 years for 200 companies
      print(f"Combined {len(company_dict)} company dataframes")
      print(f"Expected total rows: {expected_total_datarows}")
      print(f"Actual combined rows: {total_rows}")

      if total_rows != expected_total_datarows:
          print("WARNING: Row count mismatch! Some data may be duplicated or missing.")

    for company, df in company_dict.items():
      df.drop_duplicates(subset='Date', keep='first',inplace=True)

    companies_with_unequal_rows = company_data.groupby('Company').size()[company_data.groupby('Company').size()!=100] # 100 because quarterly analysis for 25 years adds to (4*25) = 100
    if not companies_with_unequal_rows.empty:
        print("Companies with rows not equal to 100:")
        print(companies_with_unequal_rows)
    else:
        print("Now all companies have 100 rows.")

    return company_dict

  # It is observed if Price is null, PE ratio is null.
  # Therefore, removing the companies with more than 75% Price value null
  # In this case, companies 091 and 121
  def check_for_75_percent_price_null(self, company_dict):
    company_with_null_price = []
    for company, df in company_dict.items():
      # 1. Quantify the missing data for the companies
      companies_with_nulls = df[df['Price'].isna() & df['PE ratio'].isna()]['Company'].unique()
      if companies_with_nulls:
        print(f"Companies with null Price and PE ratio: {companies_with_nulls}")

        # 2. Check what percentage of each company's data is missing
        for company in companies_with_nulls:
          company_data = df[df['Company'] == company]
          missing_percentage = company_data['Price'].isna().mean() * 100
          print(f"{company}: {missing_percentage:.2f}% of Price values missing")
          if missing_percentage > 75.00:
            company_with_null_price.append(companies_with_nulls[0])
            print("company_with_null_price : ",company_with_null_price)

          # Check if missing values are in specific time periods
          missing_periods = company_data[company_data['Price'].isna()]['Date']
          print(f"Missing periods: {missing_periods.min()} to {missing_periods.max()}")

      # 3. Check if other metrics are also missing for these periods
        for company in companies_with_nulls:
          company_missing_data = df[(df['Company'] == company) & df['Price'].isna()]
          missing_counts = company_missing_data.isna().sum()
          print(f"{company} missing value counts in periods with missing Price:")
          print(missing_counts)

    for company in company_with_null_price:
      print("company with more than 75% Price values as null : ",company)
      try:
        print(f"Delete {company} data from dictionary : ")
        del company_dict[company]
      except KeyError as e:
          print(f"Error: {e}")

    return company_dict

  def impute_missing_values_with_forward_backward_average(self, company_dict, columns_to_impute=None):
    imputed_dict = {}

    for company, df in company_dict.items():
        # Make a copy to avoid modifying the original
        df_copy = df.copy()
        cols = [col for col in columns_to_impute if col in df_copy.columns]

        # For each column with missing values
        for col in cols:
            if df_copy[col].isna().any():
                # Create forward-filled and backward-filled versions
                forward_filled = df_copy[col].fillna(method='ffill')
                backward_filled = df_copy[col].fillna(method='bfill')

                # For values that are still missing after one-directional fill
                # (this happens at the beginning or end of the series)
                forward_filled = forward_filled.fillna(backward_filled)
                backward_filled = backward_filled.fillna(forward_filled)

                # Fill the missing value with Average of the two filled series where original had NaN
                mask = df_copy[col].isna()
                df_copy.loc[mask, col] = (forward_filled[mask] + backward_filled[mask]) / 2

                # Check if any values are still missing
                still_missing = df_copy[col].isna().sum()
                if still_missing > 0:
                    print(f"Warning: {company}, {col} still has {still_missing} missing values")

        imputed_dict[company] = df_copy

    return imputed_dict

  def handle_missing_values(self, company_dict):
    for _, df in company_dict.items():
      # Missing Price
      df.loc[df['Price'].isna() & df['PE ratio'].notna() & df['EPS'].notna(), 'Price'] = df['PE ratio'] * df['EPS']
      # Missing EPS
      df.loc[df['EPS'].isna() & df['Price'].notna() & df['PE ratio'].notna(), 'EPS'] = abs(df['Price']) / df['PE ratio']
      # Missing PE ratio
      mask = df['PE ratio'].isna() & df['Price'].notna() & df['EPS'].notna() & (df['EPS'] != 0)
      df.loc[mask, 'PE ratio'] = abs(df.loc[mask, 'Price']) / df.loc[mask, 'EPS']

    columns_to_impute = ['Price', 'Revenue', 'Free cash flow', 'Total Debt', 'EPS', 'PE ratio', 'ROE']
    company_dict = self.impute_missing_values_with_forward_backward_average(company_dict, columns_to_impute=columns_to_impute)

    return company_dict

  def create_target_column(self, combined_df):
    combined_df['Next_Quarter_Price'] = combined_df.groupby('Company')['Price'].shift(-1)
    combined_df['Return'] = (combined_df['Next_Quarter_Price'] - combined_df['Price']) / combined_df['Price']
    combined_df['Target'] = (combined_df['Return'] > 0).astype(int)
    combined_df.dropna(subset=['Next_Quarter_Price'], inplace=True)
    return combined_df
