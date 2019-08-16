def gotValue():
	"""This looks at the number of users who purchased in a given month and have at least 2 PHQ9 scores, with a minimum of 15 days in the program.
	"""
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

	inputDate()
	bought = data.loc[data['boughtTime'].between(startDate, endDate)]
	bought = bought.assign[(daysIn = subset.todaysDate - subset.boughtTime)]
	retained = bought.loc[bought.daysIn >= 15]
	bought.MoodScores = bought.MoodScores.apply(parseNumericArray)
	subset = bought.loc[bought.MoodScores.apply(len) > 1]
	firstMoodValues = subset.MoodScores.apply(lambda x: x[0])
	lastMoodValues = subset.MoodScores.apply(lambda x: x[len(x)-1])
	subset = subset.assign(moodChange = lastMoodValues - firstMoodValues)
	subset = subset.assign(moodChangePercent = ((lastMoodValues - firstMoodValues)/firstMoodValues)*100)

	gotValue = subset.loc[subset.daysIn > 15]
	# This is effectively people who have 2 or more PHQ9's and have 15 days between starting the program and most recent use. This is our current definition of getting value.
	effected = subset.loc[(subset.moodChangePercent > 49.9) & ()]

	retainedPercent = retained/bought.shape[0]
	gotValuePercent = gotValue/bought.shape[0]
	effectedPercent = effected/bought.shape[0]

	cols = ["moodChange", "moodChangePercent", "daysIn", "Time Started (UTC)", "todaysDate", "boughtTrigger", "points", "Minutes Spent"]
	subset[cols].to_csv('gotValueData.csv')

	print(bought.shape[0], "bought.")
	print(retainedPercent, "% retained 15 days after purchase (", retained.shape[0], ")")
	print(gotValuePercent, "% got value (", gotValue.shape[0], ")")
	print(effectedPercent, "% for whom UpLift was effective (", effected.shape[0], ")")
	print("Dataset exported to gotValueData.csv")
