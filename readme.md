#Pandas
## Installing

	1. Install Python, if you don't have it. (It should come with most Linux installations, otherwise go to python.org)
		* I've had trouble getting Pandas to work within a Windows Python environment. I haven't tried very hard; but if you have the choice, I'd recommend doing it in Linux.
	2. Install Pip, if you don't have it. (You should; all new versions ship with it.) You can check by typing `pip list`; if something happens, you have Pip.
	3. Install pandas with `pip install pandas`.
	4. Launch Python with `python`.

## Getting Started

	1. Make sure you're in the same directory as `uplift.py`
	2. `from uplift import *`
	3. Follow the instructions. If you select "Leave Menu", the data will be available as `data`.

## Basics: import and data slicing.

```python

# Importing your CSV
	>>> import pandas
	>>> upliftData = pandas.read_csv("Feb_26.csv", low_memory=False)
	# If you get a warning that the data is of mixed types, type `low_memory = False` again.  

# Extracting specific columns and putting them in a new csv.
	>>> desiredColumns = ["email", "currentSession"]
	>>> finalData = upliftData[desiredColumns]
	>>> finalData.to_csv("finalData.csv")

# Cut off a certain range of rows:
	>>> upliftData.loc[8000:].to_csv('recentRows.csv')
	# reverse, cut off end:
	>>> upliftData.loc[:5000].to_csv('recentRows.csv')

```
## Finding specific or conditional data

```python
	# Find a specific email, for example
		>>> upliftData.loc[upliftData.email == "runawaytrike@gmail.com"]
	# Find out certain info based on someone's email
		>>> upliftData.loc[(upliftData.email == "Hollinsprincess12345@yahoo.com"), 'boughtTrigger']
		# Or, multiple:
		>>> upliftData.loc[(upliftData.email == "Hollinsprincess12345@yahoo.com"), ['boughtTrigger', 'email', 'User', 'name']]
	# Find a specific value by index (which can be obtained from the above)
		>>> upliftData.loc[246, 'currentSession']
	# Set the 'email' value as the index of the dataframe
		>>> upliftData.set_index('email')
	# export all rows which meet certain conditions
		>>> upliftData.loc[(upliftData.boughtTrigger == "fired") & (upliftData['Minutes Spent'] > 100)].to_csv('spentLong.csv')
	# Finding substrings
		>>> testData.loc[testData['boughtTime'].str.contains('February')==True]
```

## Replacing NaN values
	```python
		>>> data = data.fillna("whatever should replace NaN values")
	```

## Dealing with case sensitivity
	The best way to do this seems to be to turn the target column into all lowercase. Try:
		.str.lower()

## Further Resources

* https://www.kaggle.com/learn/pandas
  They have an excellent tutorial; the first two sections cover most of what we need.
	Their Python tutorial is great as well, and can be useful background for working with Pandas.  
