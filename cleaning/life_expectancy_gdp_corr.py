import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gdp = pd.read_csv("CSE_3104_group_project_xyz_chromosome/data/gdp_pcap.csv")
le = pd.read_csv("CSE_3104_group_project_xyz_chromosome/data/life_expectancy_at_birth.csv")
gdp_long = gdp.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="gdp_per_capita"
)
le_long = le.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="life_expectancy_at_birth"
)
gdp_long["year"] = gdp_long["year"].astype(int)
le_long["year"] = le_long["year"].astype(int)
gdp_long = gdp_long[(gdp_long["year"] >= 1960) & (gdp_long["year"] <= 2022)]
le_long = le_long[(le_long["year"] >= 1960) & (le_long["year"] <= 2022)]
df = gdp_long.merge(
    le_long,
    on=["geo","name","year"],
    how="inner"
)
df.isna().sum()
df = df.dropna()

df["log_gdp"] = np.log(df["gdp_per_capita"])
df["le_lag1"] = df.groupby("geo")["life_expectancy_at_birth"].shift(1)
df[["gdp_per_capita","life_expectancy_at_birth"]].corr()

print(df.head())

plt.scatter(df["life_expectancy_at_birth"], df["gdp_per_capita"])

plt.xlabel("Average Life Expectancy")
plt.ylabel("GDP per capita")
plt.title("Average Life Expectancy vs GDP per Capita")

plt.show()