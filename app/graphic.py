import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
df = pd.read_excel("tariff_database_2025.xlsx")

# Keep only the relevant columns and drop rows with missing values
df = df[['brief_description', 'mfn_text_rate']].dropna()

# Clean the tariff rate column (remove % and convert to float)
df['mfn_text_rate'] = (
    df['mfn_text_rate']
    .astype(str)
    .str.replace('%', '')
    .str.strip()
)
df['mfn_text_rate'] = pd.to_numeric(df['mfn_text_rate'], errors='coerce')
df = df.dropna(subset=['mfn_text_rate'])

# Sort by tariff rate descending
df = df.sort_values(by='mfn_text_rate', ascending=False)

# Function to check if new product shares words with already selected ones
def is_unique_product(product, selected_products):
    product_words = set(product.lower().split())
    for selected in selected_products:
        selected_words = set(selected.lower().split())
        # Check if there's any overlap of words (excluding common stopwords if needed)
        if product_words.intersection(selected_words):
            return False
    return True

selected_products = []
selected_rows = []

for idx, row in df.iterrows():
    product = row['brief_description']
    if is_unique_product(product, selected_products):
        selected_products.append(product)
        selected_rows.append(row)
    if len(selected_products) == 10:
        break


unique_df = pd.DataFrame(selected_rows)


unique_df['brief_description'] = unique_df['brief_description'].str.slice(0, 40) + '...'

# Plot
plt.figure(figsize=(10, 6))
plt.barh(unique_df['brief_description'], unique_df['mfn_text_rate'], color='green')
plt.xlabel('Standard Tariff Rate (%)')
plt.title('Top 10 Tariff Rates by Product')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
