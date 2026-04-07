import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gdp = pd.read_csv("CSE_3104_group_project_xyz_chromosome/data/gdp_pcap.csv")
pov = pd.read_csv("CSE_3104_group_project_xyz_chromosome/data/poverty_rate.csv")
gdp_long = gdp.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="gdp_per_capita"
)
pov_long = pov.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="poverty_rate"
)
gdp_long["year"] = gdp_long["year"].astype(int)
pov_long["year"] = pov_long["year"].astype(int)
gdp_long = gdp_long[(gdp_long["year"] >= 1960) & (gdp_long["year"] <= 2022)]
pov_long = pov_long[(pov_long["year"] >= 1960) & (pov_long["year"] <= 2022)]
df = gdp_long.merge(
    pov_long,
    on=["geo","name","year"],
    how="inner"
)
df.isna().sum()
df = df.dropna()

df["log_gdp"] = np.log(df["gdp_per_capita"])
df["poverty_rate_lag1"] = df.groupby("geo")["poverty_rate"].shift(1)
df[["gdp_per_capita","poverty_rate"]].corr()

print(df.head())

plt.scatter(df["poverty_rate"], df["gdp_per_capita"])

plt.xlabel("Poverty Rate")
plt.ylabel("GDP per capita")
plt.title("Poverty vs GDP per Capita")

plt.show()