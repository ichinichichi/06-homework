#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np

pd.set_option("display.max_columns",100)
pd.set_option("display.max_rows",100)


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx")
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[3]:


len(df)


# In[4]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# The dataset describes dog licensing data in New York City along with the dog name under  `Animal Name `, the gender of the dog under  `Animal Gender `. The column  `Vaccinated ` answers the questions whether the dog got vaccinated with a **Yes** or **No**.
# 
# Each row describes a single dog and its data.

# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# 1. What dog breed is the most populat one?
# 2. What are the most popular dog names in New York City?
# 3. Which breed of dogs are spayed or neutered the most?
# 4. Were do most dog owners live?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[5]:


df["Primary Breed"].value_counts().head(10).plot(kind='bar')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[6]:


df[df["Primary Breed"]!="Unknown"]["Primary Breed"].value_counts().head(10).plot(kind='bar')


# ## What are the most popular dog names?

# In[7]:


df[df["Animal Name"]!="UNKNOWN"]["Animal Name"].value_counts().head(10).plot(kind='bar')


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[8]:


df[df["Animal Name"].str.contains("^MAX$", case=False,na= False)]["Animal Name"].count()


# 652 dogs have the name Max.

# In[9]:


df[df["Animal Name"].str.contains("^MAXWELL$", case=False,na= False)]["Animal Name"].count()


# 37 dogs have the name Maxwell.

# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[10]:


df["Guard or Trained"].value_counts(normalize=True)


# 0,1029% od the dogs are guard dogs.

# ## What are the actual numbers?

# In[11]:


df["Guard or Trained"].value_counts()


# 51 dogs are guard dogs.

# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[12]:


df["Guard or Trained"].value_counts(dropna=False)


# It is less than the numbers of rows since there are also missing values.

# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[13]:


df["Guard or Trained"]=df["Guard or Trained"].replace( np.nan, 'No')


# In[14]:


df["Guard or Trained"].value_counts(dropna=False)


# ## What are the top dog breeds for guard dogs? 

# In[15]:


df[df["Guard or Trained"]=='Yes']["Primary Breed"].value_counts()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[16]:


df['year']=df['Animal Birth'].apply(lambda birth: birth.year)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[17]:


df['age']=2021-df.year


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[18]:


df_zip= pd.read_csv('zipcodes-neighborhoods.csv')
df= df.merge(df_zip, left_on="Owner Zip Code", right_on="zip", how="outer")
df=df.drop(columns=['zip'])
df.sample(5)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[19]:


df[df.borough=='Bronx']["Animal Name"].value_counts().head(1)


# The most popular dog name in the Bronx is Rocky.

# In[20]:


df[df.borough=='Brooklyn']["Animal Name"].value_counts()


# The most popular dog name in Brooklyn is Max.

# In[21]:


df[df.neighborhood=="Upper East Side"]["Animal Name"].value_counts().head(1)


# The most popular dog name in the Upper East Side is Lucy.

# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[22]:


df[df["Primary Breed"]!="Unknown"] .groupby(by="neighborhood")["Primary Breed"] .value_counts().groupby(by='neighborhood').nlargest(1)


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[23]:


df[df["Spayed or Neut"]=="Yes"]["Primary Breed"].value_counts().tail(20)


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[24]:



df["Monochrome"]= (   
(df['Animal Dominant Color'].str.lower().isin(['black', 'white' ,'grey', 'gray']) | df['Animal Dominant Color'].isna() ) & 
(df['Animal Secondary Color'].str.lower().isin(['black', 'white' ,'grey','gray']) | df['Animal Secondary Color'].isna() ) & 
(df['Animal Third Color'].str.lower().isin(['black', 'white' ,'grey','gray'])  | df['Animal Third Color'].isna() )
)


# In[25]:


df.sample(5)


# loc is used to Access a group of rows and columns by label(s) or a boolean array
# 
# As an input to label you can give a single label or it’s index or a list of array of labels
# 
# Enter all the conditions and with & as a logical operator between them

# ## How many dogs are in each borough? Plot it in a graph.

# In[26]:


df.borough.value_counts(dropna=False).plot(kind='barh',title='Dog Count in each borough')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[27]:


df_pop=pd.read_csv("boro_population.csv")


# In[28]:


dogcount=df.groupby(by='borough').size().reset_index()
dogcount=dogcount.merge(df_pop, on='borough',how='outer')


# In[29]:


dogcount["Dogs per-capita"]=dogcount[0]/dogcount["population"]


# In[30]:


dogcount.sort_values(by="Dogs per-capita", ascending= False).head(1).borough


# Manhattan has the highest number of dogs per-capita.

# `size` includes **NaN** values, `count` does not.

# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[31]:


top5= df[df["Primary Breed"]!="Unknown"] .groupby(by="borough")["Primary Breed"] .value_counts().groupby(level=0, group_keys=False).nlargest(5) .to_frame(name='breed counts').reset_index()
top5


# `group_keys=False` to avoid the double columns. `to_frame(name='breed counts').reset_index()`

# In[32]:



pivot_df = top5.pivot(index='borough', columns='Primary Breed', values='breed counts')
pivot_df

pivot_df.plot.bar(stacked=True, figsize=(10,7))


# ## What percentage of dogs are not guard dogs?

# In[33]:


df["Guard or Trained"].value_counts(dropna=False, normalize= True)


# 99,9% of the dogs are not guard or trained dogs.
