# Advanced Pandas

* Rename a column - data.rename({'Unnamed: 1': 'toolboxMetrics'}, axis=1)

* Convert string/number to time - pd.to_datetime

* Convert to just a quantity of time - pd.to_timedelta

* Convert a datetime to just a date - dt.date

* Add time to a datetime = + pd.Timedelta(days=1)

* Cite a timedelta - pd.Timedelta(days=1)

* Count the instances of various values (or a specific value) in a series
  `value_counts()` - returns a pandas series, so values are specified as in a series, not in a list. 

  Example syntax:
  
  `bought.gender.value_counts()`

* Find the values common to or different between two columns:
  ```Python
  list(set(data.colA).difference(set(data.colB)))
  ```
  For common values, replace `.difference` with `&`

* Convert a series (column) to a list: 
  Python: `list(data.colA)`
  Pandas: `data.colA.tolist()`

# Python

Anonymous functions
  lambda inputs: outputs

