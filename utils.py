import pandas as pd
import numpy as np
from pathlib import Path

class DataPreprocessor:
    def __init__(self):
        self.df = None
        self.file_path = None
        self.columns = None
        self.summary = None
    
    def load_csv(self, file_path):
        """Load CSV file and generate initial summary"""
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.columns = self.df.columns.tolist()
        self.generate_summary()
        return "I've loaded the CSV file. It has {} rows and {} columns. Ask me what you'd like to know about it!".format(
            len(self.df), len(self.columns)
        )
    
    def generate_summary(self):
        """Generate a basic summary of the dataset"""
        self.summary = {
            'rows': len(self.df),
            'columns': len(self.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'numeric_columns': self.df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist()
        }
    
    def get_basic_stats(self):
        """Get basic statistics of numeric columns"""
        if self.df is None:
            return "Please upload a CSV file first."
        
        stats = self.df.describe().to_dict()
        print("get_basics_stats", stats)
        response = "Here are the basic statistics for numeric columns:\n"
        for col in stats:
            response += f"\n{col}:\n"
            response += f"- Mean: {stats[col]['mean']:.2f}\n"
            response += f"- Std: {stats[col]['std']:.2f}\n"
            response += f"- Min: {stats[col]['min']:.2f}\n"
            response += f"- Max: {stats[col]['max']:.2f}\n"
        return response

    def handle_missing_values(self, strategy='info'):
        """Handle missing values in the dataset"""
        if self.df is None:
            return "Please upload a CSV file first."
        
        if strategy == 'info':
            missing = self.df.isnull().sum()
            print("missing values", missing)
            if missing.sum() == 0:
                return "There are no missing values in the dataset."
            
            response = "Here are the columns with missing values:\n"
            for col, count in missing[missing > 0].items():
                response += f"- {col}: {count} missing values\n"
            return response
        
        elif strategy == 'drop':
            initial_rows = len(self.df)
            self.df.dropna(inplace=True)
            dropped = initial_rows - len(self.df)
            return f"Dropped {dropped} rows with missing values. {len(self.df)} rows remaining."
        
        elif strategy == 'fill_mean':
            for col in self.df.select_dtypes(include=[np.number]).columns:
                self.df[col].fillna(self.df[col].mean(), inplace=True)
            return "Filled numeric missing values with mean values."

    def process_command(self, command):
        """Process natural language commands for data preprocessing"""
        command = command.lower()
        print("process_command", command)
        if "show" in command and "missing" in command:
            return self.handle_missing_values('info')
        
        elif "drop" in command and "missing" in command:
            return self.handle_missing_values('drop')
        
        elif "fill" in command and "missing" in command:
            return self.handle_missing_values('fill_mean')
        
        elif "statistics" in command or "stats" in command:
            return self.get_basic_stats()
        
        elif "summary" in command or "describe" in command:
            return f"""
Dataset Summary:
- Total Rows: {self.summary['rows']}
- Total Columns: {self.summary['columns']}
- Numeric Columns: {', '.join(self.summary['numeric_columns'])}
- Categorical Columns: {', '.join(self.summary['categorical_columns'])}
"""
        
        return "I'm not sure how to process that command. Try asking about missing values, statistics, or summary of the data." 