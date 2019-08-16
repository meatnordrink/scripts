# Playground for testing, specifically arrays at the moment.

print("Importing Pandas...")
import pandas as pd
import traceback as tb

def setup():
	"""imports the pandas module and the csv and sets it as a global value"""
	# import pandas as pd
	print("Enter the filename:")
	csvIn = input()
	print("Import full? y/n")
	fullImport = input().lower()
	print("Please wait while your data is imported...")
	global data
	if fullImport == "y":
		data = pd.read_csv(csvIn, parse_dates=['todaysDate', 'Time Started (UTC)', 'REGstartTime', 'boughtTime'], converters={"MoodScores": str, "MJentriesCompletedEachSession": str, "toolboxEngagement": str}, low_memory=False)
	if fullImport == "n":
		data = pd.read_csv(csvIn, usecols=['name', 'email', 'name','Run', 'User', 'Time Started (UTC)', 'iosApp', 'currentSession', 'sessionsCompleted', 'boughtTrigger','subscription_status', 'paywallEmail', 'paywallUserID', 'currentlyBrowsingMenus', 'currentlymidsession', 'todaysDate', 'Time Started (UTC)', 'boughtTime', 'payment_plan', 'iosApp', 'programStartTime', 'sessionsCompleted', 'REGstartTime', 'REGduration', 'FFduration', 'MBduration', 'PAduration', 'LIESduration', 'receivingMJprompts','MoodScores', 'MJentriesCompletedEachSession', 'toolboxEngagement', 'daysActiveNb', 'satisfactionFeedbackIntro', 'upliftRatingatFF', 'upliftRatingatTE', 'MJentriesCompletedbyFFstart', 'averageMJsPerDayEachSess'], parse_dates=['todaysDate', 'Time Started (UTC)', 'REGstartTime', 'boughtTime'], converters={"MoodScores": str, "MJentriesCompletedEachSession": str, "toolboxEngagement": str}, low_memory=False)
	excludedNames = ['Qanielle', 'Johnny Vampire', 'Aislinntesting', 'Spencer', 'Banana']
	mask = data.name.apply(lambda name: name not in excludedNames)
	dataReal = data.loc[mask]
	data = dataReal
	# it would be nice to figure out how to make this line not throw an error
	data.email = data.email.str.lower()
	if data.shape[0] > 0:
		print("Your data is now imported, and can be referenced as the variable `uplift.data`.")
		print(data.shape[0], "lines imported; all employee data excluded.")
		print("If you wish to utilize the available functions directly, they may be imported via `import from uplift *`")

def parseArray(arr):
	"""Takes as input a string that looks like an array and returns an array of values. The values in the array are not necessarily of the same type. The function attempts to eval() each value in the array; but if it fails, it leaves the unevaluated string in place."""
	cleaned = arr.replace(" ", "").replace("[", "").replace("]", "")
	vals = cleaned.split(",")

	for i in range(0, len(vals)):
		try:
			vals[i] = eval(vals[i])
		except:
			pass

	return vals

def parseNumericArray(arr):
	"""Takes as input a string that looks like an array and returns an array of numeric values. Any value in the array that can't be evaluated is turned into a zero."""
	out = parseArray(arr)

	for i in range(0, len(out)):
		if isinstance(out[i], str):
			out[i] = 0

	return out

bought = data.loc[data.boughtTime.between('2019-05-01', '2019-05-31')]


setup()
print("--------------------------------------------")
