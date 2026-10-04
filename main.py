from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Put the downloaded IMDb CSV in the same folder as this script.
data_folder = Path(__file__).resolve().parent
csv_files = sorted(data_folder.glob("*.csv"))
if not csv_files:
	raise FileNotFoundError(f"No CSV dataset found in {data_folder}")

preferred_names = {"imdb.csv", "imdb-movie-data.csv", "imdb_movies.csv"}
dataset_path = next(
	(path for path in csv_files if path.name.lower() in preferred_names), csv_files[0]
)
movies = pd.read_csv(dataset_path)

print("First three rows:")
print(movies.head(3))
print("\nLast three rows:")
print(movies.tail(3))

print("\nDataset information:")
movies.info()
print("\nNull values by column:")
print(movies.isnull().sum())
print("Are any null values present?", movies.isnull().values.any())

# Use one-based row numbers: rows 41 through 75 correspond to iloc[40:75].
subset = movies.iloc[40:75]
print("\nRows 41 to 75:")
print(subset)

votes_column = next(
	(name for name in ("No_of_Votes", "Votes", "Number_of_Votes") if name in movies.columns),
	None,
)
if votes_column is None:
	raise KeyError("Votes column not found; expected No_of_Votes or Votes.")
votes = pd.to_numeric(
	movies[votes_column].astype(str).str.replace(",", "", regex=False), errors="coerce"
)
print("\nMovie with the highest number of votes:")
print(movies.loc[votes.idxmax()])

plot_data = movies.copy()
for column in ("IMDB_Rating", "Runtime"):
	if column not in plot_data.columns:
		raise KeyError(f"Required column not found: {column}")
	# Handles runtimes recorded as either numbers or strings such as "142 min".
	numeric_values = plot_data[column].astype(str).str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
	plot_data[column] = pd.to_numeric(numeric_values, errors="coerce")

plot_data[["IMDB_Rating", "Runtime"]].plot(
	kind="box", subplots=True, layout=(1, 2), figsize=(10, 5)
)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(plot_data["Runtime"], plot_data["IMDB_Rating"], alpha=0.6)
plt.xlabel("Runtime (minutes)")
plt.ylabel("IMDB Rating")
plt.title("IMDB Rating vs Runtime")
plt.tight_layout()
plt.show()

plot_data[["IMDB_Rating", "Runtime"]].hist(bins=20, figsize=(10, 4))
plt.tight_layout()
plt.show()

if "Rating" not in movies.columns:
	raise KeyError("Required column not found: Rating")
plt.figure(figsize=(10, 5))
sns.countplot(data=movies, x="Rating", order=movies["Rating"].value_counts().index)
plt.xticks(rotation=45, ha="right")
plt.title("Number of Movies by Rating")
plt.tight_layout()
plt.show()
