import pandas as pd
import pyodbc
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.stats import f_oneway



# Connect to the SQL Server database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-D8F848M;'
    'DATABASE=PokemonDB;'
    'UID=david_vega;' #Needed to specify user ID even with Windows Authentication
    'Trusted_Connection=yes;'
)

# Read the data from the Pokemon table
query = """
SELECT name, hp, attack, defense, sp_atk, sp_def, speed
FROM Pokemon
WHERE legendary = 0
AND name NOT LIKE '%Mega %';
"""

df = pd.read_sql(query, conn)

# Standardize the data

# Select the features for scaling
features = ['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']
X = df[features]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Clustering using KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)
'''
labels = {0: 'Balanced', 1: 'Tank', 2: 'Glass Cannon', 3: 'Bulky Tank'}
df['cluster'] = df['cluster'].map(labels)
'''

# Add cluster labels to the DataFrame
cluster_summary = df.groupby('cluster')[features].mean().round(0)
print(cluster_summary)

# Visualize the clusters using a pairplot

sns.pairplot(df, hue='cluster', vars=features, palette='tab10')
plt.suptitle("K-Means Clustering of Pokémon Stats", y=1.02)
plt.tight_layout()
plt.show()

# Perform ANOVA to test for significant differences between clusters
for feature in features:
    groups = [group[feature].values for _, group in df.groupby('cluster')]
    stat, p = f_oneway(*groups)
    print(f"{feature}: F-statistic = {stat:.2f}, p-value = {p:.4f}")

# Close the database connection
conn.close()