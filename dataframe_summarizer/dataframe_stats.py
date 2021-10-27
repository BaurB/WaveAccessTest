import numpy as np
import pandas as pd


class StatisticalDescription:
    '''Statistical Summarizer for inputted dataframe'''
    def __init__(self, columns):
        '''
        Creates Output DataFrame structure. The structure is based on column names and desired statistics
        '''
        stats = ['column type', 'count', 'min', 'max', 'mean', 'median', 'mode', 'percent of zero (or nan) rows', 'variance', 'std', 'IQR', 'coefficient of variation', 'number of distinct values']
        self.df = pd.DataFrame([], stats, columns)

    def standard_deviation(self, series, ddof=False):
        '''calculates std of an array'''
        x = (abs(series - series.mean())**2)
        N = len(series)
        if ddof:
            mean = x.sum() / (N - ddof) # In standard stats practice, Pandas.std() uses ddof=1
        else:
            mean = x.sum() / N
        std = np.sqrt(mean)
        return std

    def min_max(self, pandas_series):
        '''
        Gets min and max values of each column of inputted DataFrame
        '''
        maximum = pandas_series.max()
        minimum = pandas_series.min()
        return maximum, minimum

    def calculate_iqr(self, series, percentile_range_1=None, percentile_range_2=None):
        '''
        Calculates Interquartile range for each column of inputted DataFrame
        Works faster than using scipy.stats.iqr function (checked with timeit)
        '''
        if percentile_range_1 and percentile_range_2:
            q3,q1 = np.percentile(series, [percentile_range_2, percentile_range_1])
        else:
            q3,q1 = np.percentile(series, [75, 25])
        iqr = q3 - q1
        return iqr

    def infer_df(self, df, hard_mode=False, float_to_int=False):
        '''
        Infers the type of a column. Main aim is to reduce the dtype of pandas column.
        The change in dtype helps to reduce memory. For example, reduction from 'float64' type
        to 'float16' will save 4x memory when using the dataframe
        '''
        result = {}

        # set multiplication factor
        mf = 0.5

        # set supported datatypes
        integers = ['int8', 'int16', 'int32', 'int64']
        floats = ['float16', 'float32', 'float64']
        strings = ['str']

        # calculate all numerical ranges for each supported datatype
        ranges_integers = [(np.iinfo(_int).min, np.iinfo(_int).max, _int) for _int in integers]
        ranges_floats = [(np.finfo(_float).min, np.finfo(_float).max, _float) for _float in floats]

        for column in df.columns:
            _type = df[column].dtype
    #         print(_type)

            # float numerical column could also be int (without any decimals)
            if float_to_int and np.issubdtype(_type, np.floating):
                if np.sum(np.remainder(df[column], 1)) == 0:
                    df[column] = df[column].astype('int64')
                    _type = df[column].dtype

            # convert type of column to smallest possible
            if np.issubdtype(_type, np.integer) or np.issubdtype(_type, np.floating):
                borders = ranges_integers if np.issubdtype(_type, np.integer) else ranges_floats

                _min = df[column].min()
                _max = df[column].max()

                for b in borders:
                    if b[0] * mf < _min and _max < b[1] * mf:
                        result[column] = b[2]
                        break

            if _type == 'object':
                result[column] = 'categorical data (str or mixed)'

        return result

    def populate_df(self, df):
        '''Populates created dataframe with statistics'''

        # Use double for loop to iterate through every row of every column in dataframe
        for column in (df.columns):
            # Identify column type
            self.df[column]['column type'] = self.infer_df(df)[column]

            # For Numerical Columns
            if self.infer_df(df)[column] != 'categorical data (str or mixed)':
                count, count_nans_zeros = 0, 0
                summation = 0
                for row in (df[column]):
        #             print(type(row))
                    if pd.isna(row) == False and (row!= 0) and (type(row)==int or type(row)==float):
                        count += 1
                        summation += row
                    elif pd.isna(row) == True or row == 0:
                        count_nans_zeros += 1

    #         output_df[column]['column type'] = infer_df(df)[column]
                self.df[column]['count'] = count
                self.df[column]['max'], self.df[column]['min'] = self.min_max(df[column])

                # Mean, Median,  Mode and percentage of zero numbers
    #             print('column', df[column])
                mean = summation/count
                self.df[column]['mean'] = mean
                self.df[column]['median'] = df[column].median()
                self.df[column]['mode'] = df[column].mode()[0] # or df[column].value_counts()[0]
                self.df[column]['percent of zero (or nan) rows'] = (count_nans_zeros/len(df[column])) * 100

                # Variance, std
                std = self.standard_deviation(df[column], ddof=1)
                self.df[column]['std'] = std
                self.df[column]['variance'] =pow(std, 2)

                # IQR,Coefficient of variation and Number of distinct values
                self.df[column]['IQR'] = self.calculate_iqr(df[column])
                self.df[column]['coefficient of variation'] = std/mean

            # For Categorical
            else:
                self.df[column]['count'] = df[column].count()
                self.df[column]['percent of zero (or nan) rows'] = df[column].count()/len(df[column]) * 100
                self.df[column]['mode'] = df[column].mode()



            # May be include in-house mode function
            self.df[column]['number of distinct values'] = df[column].nunique()

        return self.df


    def save_dataframe(self, df, saved_filename):
        df = self.populate_df(df)
        df.to_csv(f'{saved_filename}.csv')
