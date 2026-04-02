import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gdp = pd.read_csv("gdp_pcap.csv")
co2 = pd.read_csv("co2_pcap_cons.csv")
gdp_long = gdp.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="gdp_per_capita"
)
co2_long = co2.melt(
    id_vars=["geo","name"],
    var_name="year",
    value_name="co2_per_capita"
)
gdp_long["year"] = gdp_long["year"].astype(int)
co2_long["year"] = co2_long["year"].astype(int)
gdp_long = gdp_long[(gdp_long["year"] >= 1960) & (gdp_long["year"] <= 2022)]
co2_long = co2_long[(co2_long["year"] >= 1960) & (co2_long["year"] <= 2022)]
df = gdp_long.merge(
    co2_long,
    on=["geo","name","year"],
    how="inner"
)
df.isna().sum()
df = df.dropna()

df["log_gdp"] = np.log(df["gdp_per_capita"])
df["co2_lag1"] = df.groupby("geo")["co2_per_capita"].shift(1)
df[["gdp_per_capita","co2_per_capita"]].corr()

print(df.head())

plt.scatter(df["co2_per_capita"], df["gdp_per_capita"])

plt.xlabel("CO2 per capita")
plt.ylabel("GDP per capita")
plt.title("CO2 Emissions vs GDP per Capita")

plt.show()