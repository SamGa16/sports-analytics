import pandas as pd

class DataCleaningPipeline:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.cleaned_data = None
    
    def remove_duplicates(self):
        self.cleaned_data = self.raw_data.drop_duplicates()
    
    def handle_missing_values(self):
        self.cleaned_data.fillna(method='ffill', inplace=True)
        self.cleaned_data.fillna(method='bfill', inplace=True)
    
    def convert_time_format(self, time_column):
        if time_column in self.cleaned_data.columns:
            self.cleaned_data[time_column] = pd.to_datetime(self.cleaned_data[time_column], errors='coerce')
    
    def normalize_column_names(self):
        self.cleaned_data.columns = [col.strip().lower().replace(" ", "_") for col in self.cleaned_data.columns]
    
    def filter_relevant_columns(self, relevant_columns):
        self.cleaned_data = self.cleaned_data[relevant_columns]
    
    def standardize_numeric_columns(self, numeric_columns):
        for col in numeric_columns:
            if col in self.cleaned_data.columns:
                self.cleaned_data[col] = pd.to_numeric(self.cleaned_data[col], errors='coerce')
    
    def execute_pipeline(self, time_column=None, relevant_columns=None, numeric_columns=None):
        self.remove_duplicates()
        self.handle_missing_values()
        if time_column:
            self.convert_time_format(time_column)
        self.normalize_column_names()
        if relevant_columns:
            self.filter_relevant_columns(relevant_columns)
        if numeric_columns:
            self.standardize_numeric_columns(numeric_columns)
        return self.cleaned_data