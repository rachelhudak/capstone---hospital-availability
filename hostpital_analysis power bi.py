#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


hospitals = pd.read_csv("Data/cleaned_tennessee_hospitals_final.csv")


# In[3]:


hospitals.head()


# In[4]:


pulse = pd.read_csv("Data/cleaned_pulse_data_final.csv")


# In[5]:


pulse.head()


# In[6]:


# 1.)	Do lower-income Tennessee counties have fewer hospitals per capita than higher-income counties?


# In[7]:


hospital_counts = hospitals.groupby("county").size().reset_index(name="hospital_count")


# In[8]:


hospital_counts.head()


# In[9]:


pulse["county"] = pulse["county"].str.replace("County", "", regex=False)


# In[10]:


pulse["county"] = pulse["county"].str.replace("County", "", regex=False).str.strip()


# In[11]:


pulse.head()


# In[12]:


merged = pulse.merge(hospital_counts, on="county", how="left")


# In[13]:


merged.head()


# In[14]:


merged["hospital_count"] = merged["hospital_count"].fillna(0)


# In[15]:


merged.describe()


# In[16]:


merged["income_group"] = pd.qcut(
    merged["value_dollars"],
    q=4,
    labels=["low", "Lower-Mid", "Upper-Mid", "High"]
)


# In[17]:


merged[["county", "value_dollars", "income_group"]].head()


# In[18]:


merged.groupby("income_group")["hospital_count"].mean()


# In[19]:


import matplotlib.pyplot as plt

merged.groupby("income_group")["hospital_count"].mean().plot(kind="bar")
plt.title("Average Number of Hospitals by County Income Level")
plt.xlabel("Income Group")
plt.ylabel("Average Hospitals per County")

plt.show()


# In[20]:


merged["value_dollars"].corr(merged["hospital_count"])


# In[21]:


# 2.) Are lower-income? counties more likely to be served by for-profit hospitals than non-profit hospitals?


# In[22]:


hospitals["hospital_ownership"].value_counts()


# In[23]:


hospitals["ownership_type"] = hospitals["hospital_ownership"].replace({
    "Proprietary": "For-Profit",
    "Voluntary Non-Profit - Private": "Non-Profit",
    "Voluntary Non-Profit - Other": "Non-Profit",
    "Voluntary Non-Profit - Church": "Non-Profit"
})


# In[24]:


hospitals["ownership_type"].value_counts()


# In[25]:


ownership_counts = hospitals.groupby(["county", "ownership_type"]).size().reset_index(name="count")


# In[26]:


ownership_counts.head()


# In[27]:


ownership_merged = pulse.merge(ownership_counts, on="county", how="left")


# In[28]:


ownership_merged.head()


# In[29]:


ownership_merged["income_group"] = pd.qcut(
    ownership_merged["value_dollars"],
    4,
    labels=["Low", "Lower-Mid", "Upper-Mid", "High"]
)


# In[30]:


ownership_merged[["county","value_dollars","income_group"]].head()


# In[31]:


ownership_summary = ownership_merged.groupby(["income_group", "ownership_type"])["count"].sum()


# In[32]:


ownership_summary


# In[33]:


ownership_table = ownership_summary.unstack()
ownership_table


# In[34]:


import matplotlib.pyplot as plt

ownership_table[["For-Profit", "Non-Profit"]].plot(kind="bar")

plt.title("For-Profit vs Non-Profit Hospitals by County Income Group")
plt.xlabel("Income Group")
plt.ylabel("Number of Hospitals")

plt.show()


# In[35]:


# 3.) Do rural Tennessee counties have fewer emergency-capable hospitals than metropolitan counties??


# In[36]:


hospitals["emergency_services"].value_counts()


# In[37]:


emergency_counts = hospitals[hospitals["emergency_services"] == "Yes"].groupby("county").size().reset_index(name="emergency_hospitals")


# In[38]:


emergency_counts.head()


# In[39]:


emergency_merged = pulse.merge(emergency_counts, on="county", how="left")


# In[40]:


emergency_merged.head()


# In[41]:


emergency_merged["emergency_hospitals"] = emergency_merged["emergency_hospitals"].fillna(0)


# In[42]:


emergency_merged["emergency_hospitals"].describe()


# In[43]:


emergency_merged["income_group"] = pd.qcut(
    emergency_merged["value_dollars"],
    4,
    labels=["Low", "Lower-Mid", "Upper-Mid", "High"]
)


# In[44]:


emergency_merged[["county","value_dollars","income_group","emergency_hospitals"]].head()


# In[45]:


emergency_by_income = emergency_merged.groupby("income_group")["emergency_hospitals"].mean()
emergency_by_income


# In[46]:


import matplotlib.pyplot as plt

emergency_by_income.plot(kind="bar")

plt.title("Average Emergency-Capable Hospitals by County Income Level")
plt.xlabel("Income Group")
plt.ylabel("Average Emergency Hospitals per County")

plt.show()


# In[47]:


hospitals["government_hospital"] = hospitals["ownership_type"].str.contains("Government|Veterans")


# In[48]:


hospitals[["ownership_type","government_hospital"]].head()


# In[59]:


# 4.) Are lower-income counties more likely to rely on government-run hospitals?


# In[49]:


government_counts = hospitals[hospitals["government_hospital"] == True].groupby("county").size().reset_index(name="government_hospitals")


# In[50]:


government_counts.head()


# In[51]:


government_merged = pulse.merge(government_counts, on="county", how="left")


# In[52]:


government_merged.head()


# In[53]:


government_merged["government_hospitals"] = government_merged["government_hospitals"].fillna(0)


# In[54]:


government_merged["government_hospitals"].describe()


# In[55]:


government_merged["income_group"] = pd.qcut(
    government_merged["value_dollars"],
    4,
    labels=["Low", "Lower-Mid", "Upper-Mid", "High"]
)


# In[56]:


government_by_income = government_merged.groupby("income_group")["government_hospitals"].mean()
government_by_income


# In[57]:


summary_table = {
    "Analysis": [
        "Hospitals vs Income Correlation",
        "For-Profit vs Non-Profit Pattern",
        "Emergency Hospitals vs Income",
        "Government Hospitals vs Income"
    ],
    "Key Result": [
        "Moderate positive correlation (≈0.33)",
        "Non-profits slightly more common in lower-income counties",
        "Higher-income counties have more emergency hospitals",
        "Government hospitals slightly more common in higher-income counties"
    ]
}

import pandas as pd
pd.DataFrame(summary_table)


# In[ ]:




