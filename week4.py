#%%

import pandas as pd
import datetime

data = pd.read_csv('crash_data.csv')
data.head()

# assertion: Every row has a record type
assert data["Record Type"].isin([1,2,3]).all() == True

#%%

CrashDF = data[data["Record Type"] == 1]
VehicleDF = data[data["Record Type"] == 2]
ParticipantDF = data[data["Record Type"] == 3]
CrashDF = CrashDF.dropna(axis=1, how="all")
VehicleDF = VehicleDF.dropna(axis=1, how="all")
ParticipantDF = ParticipantDF.dropna(axis=1, how="all")
CrashDF.head()

#%%

# Existence assertions
# Validating the existence of unique CrashIDs across the three tables
assert CrashDF["Crash ID"].unique().size == VehicleDF["Crash ID"].unique().size
assert CrashDF["Crash ID"].unique().size == ParticipantDF["Crash ID"].unique().size

# Validating that there is about 90% of Serial # present
assert CrashDF["Serial #"].unique().size >= 0.9 * (CrashDF["Crash ID"].unique().size)

#%%

# Limit Assertions
# Highway no must be 26
assert CrashDF["Highway Number"].unique().size == 1 and CrashDF["Highway Number"].unique()[0] == 26.0
# Date must be between 01/01/2019 and 31/12/2019
dates = pd.concat([CrashDF["Crash Year"], CrashDF["Crash Month"], CrashDF["Crash Day"]], axis=1)
dates.columns = ["year", "month", "day"]
dates = pd.to_datetime(dates)
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2019, 12, 31)
assert dates.isin(pd.date_range(start, end)).all()
#%%
# Valid crash hour values
assert (CrashDF["Crash Hour"].isin(range(24)).sum() + CrashDF["Crash Hour"].isin(range(99,100)).sum() == 508)
assert CrashDF["Crash Type"].isnull().all() == False
assert CrashDF["Collision Type"].isnull().all() == False
# CrashDF["Crash Type"].dtype
CrashDF.groupby(CrashDF["Light Condition"]).count()