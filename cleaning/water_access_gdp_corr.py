import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gdp = pd.read_csv("CSE_3104_group_project_xyz_chromosome/data/gdp_pcap.csv")
water_access = pd.read_csv("CSE_3104_group_project_xyz_chromosome/data/at_least_basic_water_source_overall_access_percent.csv")
gdp_long = gdp.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="gdp_per_capita"
)
water_access_long = water_access.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="water_access"
)
gdp_long["year"] = gdp_long["year"].astype(int)
water_access_long["year"] = water_access_long["year"].astype(int)
gdp_long = gdp_long[(gdp_long["year"] >= 1960) & (gdp_long["year"] <= 2022)]
water_access_long = water_access_long[(water_access_long["year"] >= 1960) & (water_access_long["year"] <= 2022)]
df = gdp_long.merge(
    water_access_long,
    on=["geo","name","year"],
    how="inner"
)
df.isna().sum()
df = df.dropna()

df["log_gdp"] = np.log(df["gdp_per_capita"])
df["water_access_lag1"] = df.groupby("geo")["water_access"].shift(1)
df[["gdp_per_capita","water_access"]].corr()

print(df.head())

plt.scatter(df["water_access"], df["gdp_per_capita"])

plt.xlabel("Percent of Population with Access to Basic Water Sources")
plt.ylabel("GDP per capita")
plt.title("Water Source Access vs GDP per Capita")

plt.show()