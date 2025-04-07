import pandas as pd 
import numpy as np

df = pd.read_csv(r'D:\pythonProject4\netflix_titles.csv')

print(df.head())

print(df.info())

print(df.dtypes)

print(df.describe())

print(df.isnull().sum())

print(df.duplicated().sum())

print(df.drop_duplicates())

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('[^a-z0-9_]', '', regex=True)
)


df['date_added'] = pd.to_datetime(df['date_added'], dayfirst=True, errors='coerce')

df['date_added'] = df['date_added'].dt.strftime('%d-%m-%Y')

# Step 1: Standardize text
df['country'] = df['country'].astype(str).str.strip().str.lower()

# Step 2: Replace known variations
country_map = {
    'united states': 'united states',
    'usa': 'united states',
    'u.s.': 'united states',
    'us': 'united states',
    'england': 'united kingdom',
    'uk': 'united kingdom',
    'united kingdom': 'united kingdom',
    'south korea': 'south korea',
    'republic of korea': 'south korea',
    'russia': 'russian federation',
    'viet nam': 'vietnam',
    'iran, islamic republic of': 'iran',
    'egypt, arab rep.': 'egypt'
}

# Function to standardize multiple countries in one string
def standardize_countries(entry):
    if entry == 'nan' or pd.isna(entry):
        return None
    countries = [country.strip() for country in entry.split(',')]
    standardized = [country_map.get(c, c) for c in countries]
    return ', '.join(sorted(set(standardized)))  # Remove duplicates & sort alphabetically

df['country'] = df['country'].apply(standardize_countries)

unique_countries = set()
df['country'].dropna().apply(lambda x: unique_countries.update(x.split(', ')))
print(sorted(unique_countries))
