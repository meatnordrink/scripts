
# To-do: Add try and except blocks so that an incorrect input doesn't crash everything.
# Make defining "bought" (or the variable bought), and the parsing arrays functions global.
# Add input() after outputs, for better UX.
# round %s in behaviorMetrics() to 2
# Replace `Time Started (UTC)` with `REGstartTime`, to eliminate time-difference/datetime vs date inconsistencies.

print("-------------------")
print("")
print("- Make sure you are using python3. You may need to run python with `python3` rather than `python`. (Many systems have both installed.)")
print("")
print("- Pandas is imported by default.")
print("")
print("-------------------")

print("Importing Pandas...")
import pandas as pd
# print some common functions via -help or somthing?

def setup():
	"""imports the pandas module and the csv and sets it as a global value"""
	# import pandas as pd
	print("Enter the filename:")
	csvIn = input()
	print("Please wait while your data is imported...")
	global data
	data = pd.read_csv(csvIn, usecols=['name', 'email', 'name','Run', 'User', 'Time Started (UTC)', 'iosApp', 'currentSession', 'sessionsCompleted', 'boughtTrigger','subscription_status', 'paywallEmail', 'paywallUserID', 'currentlyBrowsingMenus', 'currentlymidsession', 'todaysDate', 'Time Started (UTC)', 'boughtTime', 'payment_plan', 'iosApp', 'programStartTime', 'sessionsCompleted', 'REGstartTime', 'REGduration', 'FFduration', 'MBduration', 'PAduration', 'LIESduration', 'receivingMJprompts','MoodScores', 'MJentriesCompletedEachSession', 'toolboxEngagement'], parse_dates=['todaysDate', 'Time Started (UTC)', 'REGstartTime', 'boughtTime'], converters={"MoodScores": str, "MJentriesCompletedEachSession": str, "toolboxEngagement": str}, low_memory=False)
	if data.shape[0] > 0:
		print("Your data is now imported, and can be referenced as the variable `uplift.data`.")
		print(data.shape[0], "lines imported.")
		print("If you wish to utilize the available functions directly, they may be imported via `import from uplift *`")

	excludedNames = ['Qanielle', 'Johnny Vampire', 'Aislinntesting', 'Spencer', 'Banana']
	mask = data.name.apply(lambda name: name not in excludedNames)
	dataReal = data.loc[mask]
	data = dataReal

setup()
print("--------------------------------------------")

def printToCSV(toPrint):
	print("")
	print("Export to csv? (y/n)")
	answer = input()
	if answer == "y":
		print('Enter a filename (e.g., latestActive.csv)')
		filename = input()
		toPrint.to_csv(filename)
		print("Data exported to", filename)
		#could add a conditional warning here for cutColumns about the wait; it takes a bit.
def inputDate():
	print("What starting date? YYYY-MM-DD")
	startDate = pd.to_datetime(input() + " 00:00:00")
	print("What end date? YYYY-MM-DD")
	endDate = pd.to_datetime(input() + " 23:59:59")
	return startDate, endDate

def cutColumns():
	"""Produces a dataset or csv with all columns after the 1000th removed.
	This is primarily useful for producing a more manageable CSV to open in Excel or LibreOffice.
	Syntax:
	cutColumns()
	"""
	cutData = data.iloc[:,:1000]
	if cutData.shape[0] > 0:
		print("Data cut.")
	printToCSV(cutData)

# Fix this; currently cuts just the rows or something. Applied one fix; test.
def recentRows():
	"""Produces a dataset or csv with all rows (except the headers) prior to the row specified cut.
	This is primarily useful for producing a more manageable CSV to open in Excel or LibreOffice.
	Syntax:
	recentRows(ROWNUMBER)

	Example:
	recentRows(8000)

	will output all rows AFTER row 8000.
	"""
	print("Enter the first row you'd like data from:")
	print("(8000 can be used as a default; it will print all data after Jan 5 2019.)")
	trimParameter = int(input())
	global recentData
	recentData = data.loc[trimParameter:]
	# Single-line execution
	# data.loc[trimParameter:].to_csv('recentRows.csv')
	if recentData.shape[0] > 0:
		print(recentData.shape[0], "lines remaining.")
	print("Data is available via uplift.recentData")
	printToCSV(recentData)

def findUser():
	"""Finds key data about a user, given their email address. Syntax is:
	findUser("USEREMAIL")

	Example:
	findUser("andy@uplift.app")

	Note: If using the menu interface, do not include quotes.
	"""
	print("Please enter the user's email:")
	userEmail = input()
	global userData
	userData = data.loc[(data.email == userEmail), ['name','Run', 'User', 'Time Started (UTC)', 'iosApp', 'currentSession', 'sessionsCompleted', 'boughtTrigger','subscription_status', 'paywallEmail', 'paywallUserID', 'currentlyBrowsingMenus', 'currentlymidsession']]
	print("Name:", userData.name.item())
	print("Run #:", userData.Run.item())
	print("User ID:", userData.User.item())
	print("Time Started (UTC):", userData['Time Started (UTC)'].item())
	print("iosApp:", userData.iosApp.item())
	print("currentSession:", userData.currentSession.item())
	print("sessionsCompleted:", userData.sessionsCompleted.item())
	print("-------------")
	print("PAYWALL VARIABLES")
	print("bought?:", userData.boughtTrigger.item())
	print("subscription_status:", userData.subscription_status.item())
	print("paywallEmail:", userData.paywallEmail.item())
	print("paywallUserID:", userData.paywallUserID.item())
	print("-------------")
	print("RUN DETAILS")
	print("currentlyBrowsingMenus:", userData.currentlyBrowsingMenus.item())
	print("currentlymidsession:", userData.currentlymidsession.item())
	print("---------------------------------------------------")
	printToCSV(userData)

def activeUsers():
	"""Prints out the number of all users for whom `boughtTrigger='fired'` and `todaysDate` is within the specified range.
	Syntax is activeUsers(startDate, endDate). Both startDate and endDate must be enclosed in quotes, separately, and in YYYY-MM-DD format.
	Example:
	activeUsers('2019-03-11', '2019-03-18')
	Notes:
	* Do not add quotes if using the menu interface.
	* THIS CANNOT BE USED RETROACTIVELY; i.e., IT ONLY WORKS IF THE RANGE INCLUDES THE FINAL DATE IN THE CSV, as it is dependent on the `todaysDate` variable, which is overwritten with each new sign-in. In other words, a user will appear to be active only in the latest period in which they were active.

	"""
	print("NOTE: This can only be used to find active users if it includes the final date in the CSV, as the dependent variable, `todaysDate`, is overwritten each time the user signs in.")
	print("What starting date? YYYY-MM-DD")
	startDate = pd.to_datetime(input())
	print("What end date? YYYY-MM-DD")
	endDate = pd.to_datetime(input())
	boughtEver = data.loc[data.boughtTrigger=="fired"]
	#boughtEver.todaysDate = boughtEver.todaysDate.apply(pd.to_datetime) # the .apply is necessary to avoid a chain-indexing warning, "SettingWithCopyWarning". An alternative is to set the relevant columns as dates on import, with pd.read_csv('input.csv', parse_dates=['Time Started (UTC)', 'timeStarted'), though that might mean the metrics() function needs to be adjusted accordingly (no, as I didn't use 'Time Started (UTC)')
	withinRange = boughtEver.loc[boughtEver.todaysDate.between(startDate, endDate)]
	global actives
	actives = withinRange
	print("Between", startDate, "and", endDate, "there were:")
	print(withinRange.shape[0], "active, paying users.")
	printToCSV(withinRange)

def newSignups():
	"""Prints out the number of all users for whom `boughtTrigger='fired'` and `todaysDate` is within the specified range.
	Syntax is newSignups(startDate, endDate). Both startDate and endDate must be enclosed in quotes, separately, and in YYYY-MM-DD format.
	Example:
	newSignups('2019-03-11', '2019-03-18')
	Note: Do not include quotes if using the menu interface.
	"""
	# data['Time Started (UTC)'] = data['Time Started (UTC)'].apply(pd.to_datetime) I believe this worked; the above still seems to have triggered the error. Both obsolete now, but might need to figure out what was happening in the future.
	print("What starting date? YYYY-MM-DD")
	startDate = pd.to_datetime(input())
	print("What end date? YYYY-MM-DD")
	endDate = pd.to_datetime(input())
	withinRange = data.loc[data['Time Started (UTC)'].between(startDate, endDate)]
	print("Between", startDate, "and", endDate, "there were:")
	print(withinRange.shape[0], "new sign-ups.")
	printToCSV(withinRange)

def purchasesByMonth():
	"""Extracts the number of purchases in a given month.
	"""
	startDate, endDate = inputDate()
	boughtThisMonth = data.loc[data['boughtTime'].between(startDate, endDate)]
	print(boughtThisMonth.shape[0], "lines extracted. (= # of purchases.)")
	printToCSV(boughtThisMonth)

def boughtByDay():
	"""Number of purchases in a given day. Based on boughtTrigger = "fired" and boughtTime."""
	print("(Please note that, at the moment, running this function means")
	print("you can't run metrics() unless you reset the library.)")
	print("")
	print("Please enter the date you're looking for (YYYY-MM-DD):")
	startDate = pd.to_datetime(input())
	endDate = startDate + pd.Timedelta(days=1)
	data['boughtTime'] = data.boughtTime.apply(pd.to_datetime)
	bought = data.loc[data.boughtTrigger == 'fired']
	boughtToday = bought.loc[bought.boughtTime.between(startDate, endDate)]
	print("There were", boughtToday.shape[0], "purchases on", startDate)

def boughtByDay30():
	"""The same as boughtByDay(), but lists number of buys for 30 days after the date specified."""
	print("(Please note that, at the moment, running this function means")
	print("you can't run metrics() unless you reset the library.)")
	print("")
	print("Please enter the start day of the 30-day run (YYYY-MM-DD):")
	startDate = pd.to_datetime(input())
	data['boughtTime'] = data.boughtTime.apply(pd.to_datetime)
	bought = data.loc[data.boughtTrigger == 'fired']
	print("Purchases by day:")
	count = 0
	while count <= 30:
		endDate = startDate + pd.Timedelta(days=1)
		boughtToday = bought.loc[bought.boughtTime.between(startDate, endDate)]
		print(startDate, boughtToday.shape[0])
		startDate = startDate + pd.Timedelta(days=1)
		count = count + 1




def metrics():
	"""This function provides an array of revenue and ad-spend metrics for a given month.
	Syntax: metrics("MONTH", TOTAL_AD_SPEND_FOR_MONTH, TOTAL_REVENUE_FOR_MONTH)
	All-caps to be replaced; quotes must be included around the month.

	Example:
	metrics("February", 2221, 4137)
	"""
	print("Please enter the desired month:")
	thisMonth = input()
	print("Please enter the total ad-spend for the month:")
	adSpend = int(input())
	print("Please enter the total revenue for the month:")
	totalRev = int(input())

	startDate, endDate = inputDate()
	boughtThisMonth = data.loc[data.boughtTime.between('startDate', 'endDate')]
	# Check to make sure this `payment_plan` variable is stable.
	quarterlySubs = boughtThisMonth.loc[boughtThisMonth.payment_plan == 'quarterlysub']

	monthlySubs = boughtThisMonth.shape[0] - quarterlySubs.shape[0]

	iosBought = boughtThisMonth.loc[boughtThisMonth.iosApp == 1]

	androidBought = boughtThisMonth.loc[boughtThisMonth.iosApp == 2]

	webBought = boughtThisMonth.loc[boughtThisMonth.iosApp == 0]

	# Find revenue
	quarterlySubRev = quarterlySubs.shape[0] * 45
	monthlySubRev = monthlySubs * 30
	totalNewSubRev = quarterlySubRev + monthlySubRev
	# this may need to get more precise, if we wish to reflect the difference in cut Braintree takes vs the apps. Currently, the idea would be to just * .7 to get our share of this.

	# Find costs

	costPerSubscriber = adSpend/boughtThisMonth.shape[0]

	# Find adspend, revenue per-signup
	starts = data.loc[data.programStartTime.str.contains(thisMonth)==True]
	adSpendPerSignup = adSpend/starts.shape[0]
	revPerSignUp = totalNewSubRev/starts.shape[0]

	# find adspend, revenue per purchase
	revPerBought = totalNewSubRev/boughtThisMonth.shape[0]
	adSpendPerBought = adSpend/boughtThisMonth.shape[0]

	# factor in renewals
	revPerSignUpWRenew = totalRev/starts.shape[0]
	revPerBoughtWRenew = totalRev/boughtThisMonth.shape[0]
	renewalRev = totalRev - totalNewSubRev

	# Round results
	revPerBoughtWRenew=round(revPerBoughtWRenew, 2)
	revPerSignUpWRenew=round(revPerSignUpWRenew, 2)
	adSpendPerBought=round(	adSpendPerBought, 2)
	revPerBought=round(	revPerBought, 2)
	adSpendPerSignup=round(	adSpendPerSignup, 2)
	revPerSignUp=round(	revPerSignUp, 2)


	# Print Results
	print("==============================")
	print(boughtThisMonth.shape[0], "bought subscriptions this month.")
	print("Of these, ", quarterlySubs.shape[0], " were quarterly and ", monthlySubs, " were monthly.")
	print(iosBought.shape[0], " were iOS")
	print(androidBought.shape[0], " were Android")
	print(webBought.shape[0], " were web")

	print("Total new-subscription revenue this month: $", totalNewSubRev)
	print("Total renewal revenue for the month: $", renewalRev)
	print("Revenue per-sign-up: $", revPerSignUp, "(sign-up is the closest proxy for install from the csv)")
	print("Ad spend per-sign-up: $", adSpendPerSignup)
	print("Revenue per purchase: $", revPerBought)
	print("Ad spend per purchase: $", adSpendPerBought)
	print(" ")
	print("If we include renewals:")
	print("Revenue per-sign-up: $", revPerSignUpWRenew)
	print("Revenue per purchase: $", revPerBoughtWRenew)

def behaviorMetrics():
	"""Syntax is:
	useMetrics()
	"""
	print("What starting date? YYYY-MM-DD")
	startDate = pd.to_datetime(input())
	print("What end date? YYYY-MM-DD")
	endDate = pd.to_datetime(input())
	boughtEver = data.loc[data.boughtTrigger == "fired"]
	#boughtEver.todaysDate = boughtEver.todaysDate.apply(pd.to_datetime) # the .apply is necessary to avoid a chain-indexing warning, "SettingWithCopyWarning". An alternative is to set the relevant columns as dates on import, with pd.read_csv('input.csv', parse_dates=['Time Started (UTC)', 'timeStarted'), though that might mean the metrics() function needs to be adjusted accordingly (no, as I didn't use 'Time Started (UTC)')
	withinRange = boughtEver.loc[boughtEver.todaysDate.between(startDate, endDate)]
	actives = withinRange

	# find average number of sessions completed
	avgSessDone = actives.sessionsCompleted.mean()
	avgSessDone = round(avgSessDone, 2)

	# find average time using uplift
	timesStarted = actives.REGstartTime
	lastUsed = actives.todaysDate
	timeIn = lastUsed - timesStarted

	# Find average of time spent in each session
	# This is currently drawn from active purchasers. We might want to switch it to all purchasers.
	columnsWanted = ['REGduration', 'FFduration', 'MBduration', 'PAduration', 'LIESduration']
	durations = actives[columnsWanted]
	durations = durations.apply(pd.to_timedelta)
	#mean tends to be distorted; probably by people who stopped in the middle for days.

	# Find average number of challenges completed
	# - print challenge completed spred
	# actives.NumberOfChallengesCompleted.to_csv("challengeData.csv")
	challCompleted = actives.NumberOfChallengesCompleted.mean()

	# How many users are getting MJ prompts
	gettingPrompts = actives.receivingMJprompts.sum()

	print("==========================")
	print("All results are for paying users active in the time period specified.")
	print("")
	print("Average number of sessions completed:")
	print("----", avgSessDone)
	print("Length of time active users have been using UpLift:")
	print("----Mean:", timeIn.mean())
	print("----Median:", timeIn.median())
	print("Session Time Averages:")
	print("----REG median:", durations.REGduration.median())
	print("----FF median:", durations.FFduration.median())
	print("----MB median:", durations.MBduration.median())
	print("----PA median:", durations.PAduration.median())
	print("----LIES median:", durations.LIESduration.median())
	print("---------# of durations greater than 1 day---------")
	for sess in columnsWanted:
		overOne = durations.loc[durations[sess] > pd.Timedelta(days=1)]
		tempHold = durations[sess]
		totalEntries = tempHold.loc[tempHold.notnull()]
		percentOverOne = ((overOne.shape[0])/(totalEntries.shape[0]))*100
		print("Total", sess, "#:", totalEntries.shape[0])
		print("# over 1 day:", overOne.shape[0])
		print("Percent over one day: %", percentOverOne)
	# regOverOne = durations.loc[durations.REGduration > pd.Timedelta(days=1)]
	print("-----------------------------------------------------")
	print("Mean number of challenges completed:")
	print("----", challCompleted)
	print("Are users using notifications?")
	print("----", gettingPrompts, "of", actives.shape[0], "active users are receiving prompts.")


def phq9Change():
	"""This looks at the average change between the first and last value in a user's PHQ9 scores, for users with more than 4 entries.
	It pulls data from the entire range of the current CSV, for all purchasers.
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

	bought = data.loc[data.boughtTrigger == "fired"]
	bought.MoodScores = bought.MoodScores.apply(parseNumericArray)

	subset = bought.loc[bought.MoodScores.apply(len) > 4]
	firstMoodValues = subset.MoodScores.apply(lambda x: x[0])
	lastMoodValues = subset.MoodScores.apply(lambda x: x[len(x)-1])
	subset = subset.assign(moodChange = lastMoodValues - firstMoodValues)

	subset.moodChange.to_csv("latestMoodChange.csv")
	# If Eddie wants the raw data -
	# subset.MoodScores.to_csv("moodScores.csv")

	print("For all purchasers of UpLift with more than 4 PHQ9 entries:")
	print("median mood change:", subset.moodChange.median())
	print("mean mood change:", subset.moodChange.mean())
	print("This dataset has been exported to latestMoodChange.csv")

	# This is just a demo of how to do this.
	# thirdMoodValues = subset.MoodScores.apply(lambda x: x[2])

	# print("median third mood value:", thirdMoodValues.median())
	# print("mean third mood value:", thirdMoodValues.mean())

def phq9ChangeInput():
	"""This looks at the average change between the first and last value in a user's PHQ9 scores, for users with more than 4 entries.
	It pulls data from the input range.
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

	data.MoodScores = data.MoodScores.apply(parseNumericArray)

	subset = data.loc[data.MoodScores.apply(len) > 1]
	firstMoodValues = subset.MoodScores.apply(lambda x: x[0])
	lastMoodValues = subset.MoodScores.apply(lambda x: x[len(x)-1])
	subset = subset.assign(moodChange = lastMoodValues - firstMoodValues)
	subset = subset.assign(moodChangePercent = ((lastMoodValues - firstMoodValues)/firstMoodValues)*100)
	cols = ['MoodScores', 'moodChange', 'moodChangePercent']
	subset[cols].to_csv('inputMoodChanges.csv')
	# If Eddie wants the raw data -
	# subset.MoodScores.to_csv("moodScores.csv")

	print("median mood change:", subset.moodChange.median())
	print("mean mood change:", subset.moodChange.mean())
	print("median mood change percent:", subset.moodChangePercent.median(), "%")
	print("mean mood change percent:", subset.moodChangePercent.mean(), "%")
	print("This dataset has been exported to inputMoodChanges.csv")
	input()

	# This is just a demo of how to do this.
	# thirdMoodValues = subset.MoodScores.apply(lambda x: x[2])

	# print("median third mood value:", thirdMoodValues.median())
	# print("mean third mood value:", thirdMoodValues.mean())

def mjEntriesCompleted():
	"""For all purchasers, the average number of the MJentriesCompletedEachSession variable. Users with no entries are counted as 0, and included in the average.
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

	# data = pd.read_csv('input.csv', converters = {'MJentriesCompletedEachSession':str}, low_memory=False)
	bought = data.loc[data.boughtTrigger == "fired"]
	bought.MJentriesCompletedEachSession = bought.MJentriesCompletedEachSession.apply(parseNumericArray)

	firstEntries = bought.MJentriesCompletedEachSession.apply(lambda x: x[0])
	firstEntriesNoZeroes = firstEntries.loc[firstEntries > 0]
	firstEntriesPercentZeroes = round((1-((firstEntriesNoZeroes.shape[0])/(firstEntries.shape[0])))*100, 2)

	secondSet = bought.loc[bought.MJentriesCompletedEachSession.apply(len) > 1]
	secondEntries = secondSet.MJentriesCompletedEachSession.apply(lambda x: x[1])
	secondEntriesNoZeroes = secondEntries.loc[secondEntries > 0]
	secondEntriesPercentZeroes = round((1-((secondEntriesNoZeroes.shape[0])/(secondEntries.shape[0])))*100, 2)

	thirdSet = bought.loc[bought.MJentriesCompletedEachSession.apply(len) > 2]
	thirdEntries = thirdSet.MJentriesCompletedEachSession.apply(lambda x: x[2])
	thirdEntriesNoZeroes = thirdEntries.loc[thirdEntries > 0]
	thirdEntriesPercentZeroes = round((1-((thirdEntriesNoZeroes.shape[0])/(thirdEntries.shape[0])))*100, 2)

	fourthSet = bought.loc[bought.MJentriesCompletedEachSession.apply(len) > 3]
	fourthEntries = fourthSet.MJentriesCompletedEachSession.apply(lambda x: x[3])
	fourthEntriesNoZeroes = fourthEntries.loc[fourthEntries > 0]
	fourthEntriesPercentZeroes = round((1-((fourthEntriesNoZeroes.shape[0])/(fourthEntries.shape[0])))*100, 2)

	print("For all purchasers of UpLift:")
	print("-----------------------------")
	print("mean MJentriesCompleted - MB:", round(firstEntries.mean()))
	print("not counting 0's:", round(firstEntriesNoZeroes.mean()))
	print("% with 0 entries: %", firstEntriesPercentZeroes)
	print("*This is fuzzy; it does not distinguish between users who got to the second session and users who didn't, so the majority of 0's are probably users who haven't/never got to the second session. (This could be adjusted to separate for people who actually got to Sess 2.)")
	print("")
	print("*Note that the percent 0 after MB is somewhat fuzzy; only users who completed an entry in a later session have a zero recorded for any given session.")
	print("")
	print("mean MJentriesCompleted - PA:", round(secondEntries.mean(), 1))
	print("not counting 0's:", round(secondEntriesNoZeroes.mean()))
	print("% with 0 entries: %", secondEntriesPercentZeroes)
	print("")
	print("mean MJentriesCompleted - LIES:", round(thirdEntries.mean(), 1))
	print("not counting 0's:", round(thirdEntriesNoZeroes.mean()))
	print("% with 0 entries: %", thirdEntriesPercentZeroes)
	print("")
	print("mean MJentriesCompleted - IMJ:", round(fourthEntries.mean(), 1))
	print("not counting 0's:", round(fourthEntriesNoZeroes.mean()))
	print("% with 0 entries: %", fourthEntriesPercentZeroes)

def toolboxEngagement():
	"""Reports from the collection toolboxEngagement, which measures user use of toolbox functions. This function needs to be updated to take the updated toolbox options into account (as of April 2019)."""
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

	bought = data.loc[data.boughtTrigger == "fired"]
	# bought = bought.toolboxEngagement.fillna("zero")
	noEngagement = bought.loc[bought.toolboxEngagement == ""]
	percentNone = round((noEngagement.shape[0])/(bought.shape[0]), 2)*100
	engaged = bought.loc[bought.toolboxEngagement != ""]
	engaged = engaged.toolboxEngagement.apply(parseNumericArray)

	num3 = engaged.apply(lambda x: x[2])
	num3once = num3.loc[num3 > 0]
	num3twice = num3.loc[num3 > 1]

	num4 = engaged.apply(lambda x: x[3])
	num4once = num4.loc[num4 > 0]
	num4twice = num4.loc[num4 > 1]

	num6 = engaged.apply(lambda x: x[5])
	num6once = num6.loc[num6 > 0]
	num6twice = num6.loc[num6 > 1]

	num7 = engaged.apply(lambda x: x[6])
	num7once = num7.loc[num7 > 0]
	num7twice = num7.loc[num7 > 1]

	num8 = engaged.apply(lambda x: x[7])
	num8once = num8.loc[num8 > 0]
	num8twice = num8.loc[num8 > 1]

	# - #3 session outline, #4 session review, #6 facts/sources, #7 problem solver, #8 contribute to uplift



	print("Percent 0 toolbox engagment: %", percentNone)
	print("")
	print("Session Outline, engaged once or more: %", round((num3once.shape[0]/num3.shape[0])*100, 2))
	print("--, twice or more: %", round((num3twice.shape[0]/num3.shape[0])*100, 2))
	print("")
	print("Session Review, engaged once or more: %", round((num4once.shape[0]/num4.shape[0])*100, 2))
	print("--, twice or more: %", round((num4twice.shape[0]/num4.shape[0])*100, 2))
	print("")
	print("Facts/Sources, engaged once or more: %", round((num6once.shape[0]/num6.shape[0])*100, 2))
	print("--, twice or more: %", round((num6twice.shape[0]/num6.shape[0])*100, 2))
	print("")
	print("Problem Solver, engaged once or more: %", round((num7once.shape[0]/num7.shape[0])*100, 2))
	print("--, twice or more: %", round((num7twice.shape[0]/num7.shape[0])*100, 2))
	print("")
	print("Contribute to UpLift, engaged once or more: %", round((num8once.shape[0]/num8.shape[0])*100, 2))
	print("--, twice or more: %", round((num8twice.shape[0]/num8.shape[0])*100, 2))
	input()

def gotValue():
	"""This returns the number/% of users retained, who got value, and for whom UpLift was effective. The numbers are based on the definitions of these terms set in the Monthly Metrics google doc.
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

	startDate, endDate = inputDate()
	bought = data.loc[data['boughtTime'].between(startDate, endDate)]
	bought = bought.assign(daysIn = bought.todaysDate - bought.boughtTime)
	retained = bought.loc[bought.daysIn >= pd.Timedelta(days=15)]
	bought.MoodScores = bought.MoodScores.apply(parseNumericArray)
	subset = bought.loc[bought.MoodScores.apply(len) > 1]
	gotValue = bought.loc[bought.MoodScores.apply(len) > 1]
	firstMoodValues = subset.MoodScores.apply(lambda x: x[0])
	lastMoodValues = subset.MoodScores.apply(lambda x: x[len(x)-1])
	subset = subset.assign(moodChange = lastMoodValues - firstMoodValues)
	subset = subset.assign(moodChangePercent = ((lastMoodValues - firstMoodValues)/firstMoodValues)*100)

	# gotValue = subset.loc[subset.daysIn > pd.Timedelta(days=15)]
	# This is effectively people who have 2 or more PHQ9's and have 15 days between starting the program and most recent use. This is our current definition of getting value.

	# Repeat for span relevant to effectiveness; from current - 4 months to current - 1 month.
	# effectStartDate = startDate - pd.Timedelta(days=120)
	# effectEndDate = startDate - pd.Timedelta(days=30)
	# inEffectSpan = data.loc[data.boughtTime.between(effectStartDate, effectEndDate)]
	# inEffectSpan = inEffectSpan.assign(daysIn = inEffectSpan.todaysDate - inEffectSpan.boughtTime)
	# inEffectSpan.MoodScores = inEffectSpan.MoodScores.apply(parseNumericArray)
	# subsetE = inEffectSpan.loc[inEffectSpan.MoodScores.apply(len) > 1]
	# firstMoodValuesE = subsetE.MoodScores.apply(lambda x: x[0])
	# lastMoodValuesE = subsetE.MoodScores.apply(lambda x: x[len(x)-1])
	# subsetE = subsetE.assign(moodChange = lastMoodValuesE - firstMoodValuesE)
	# subsetE = subsetE.assign(moodChangePercent = ((lastMoodValuesE - firstMoodValuesE)/firstMoodValuesE)*100)
	#
	# gotValueE = subsetE.loc[subsetE.daysIn > pd.Timedelta(days=15)]
	#
	# effected = gotValueE.loc[(gotValueE.moodChangePercent > 49.9)]

	retainedPercent = (retained.shape[0]/bought.shape[0])*100
	gotValuePercent = (gotValue.shape[0]/bought.shape[0])*100
	#effectedPercent = (effected.shape[0]/inEffectSpan.shape[0])*100

	cols = ["moodChange", "moodChangePercent", "daysIn", "Time Started (UTC)", "todaysDate", "boughtTrigger", "Points", "Minutes Spent"]
	subset[cols].to_csv('gotValueData.csv')

	print(bought.shape[0], "bought.")
	print(retainedPercent, "% retained 15 days after purchase (", retained.shape[0], ")")
	print(gotValuePercent, "% got value (", gotValue.shape[0], ")")
	#print(effectedPercent, "% for whom UpLift was effective (", effected.shape[0], "out of", inEffectSpan.shape[0], " purchasers between 4 and 1 months before period.)")
	print("Dataset exported to gotValueData.csv")
	input()

def effective():
	"""This returns the number/% of users retained, who got value, and for whom UpLift was effective. The numbers are based on the definitions of these terms set in the Monthly Metrics google doc.
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

	startDate, endDate = inputDate()
	bought = data.loc[data.boughtTime.between(startDate, endDate)]

	bought.MoodScores = bought.MoodScores.apply(parseNumericArray)
	subset = bought.loc[bought.MoodScores.apply(len) > 1]
	firstMoodValues = subset.MoodScores.apply(lambda x: x[0])
	lastMoodValues = subset.MoodScores.apply(lambda x: x[len(x)-1])
	subset = subset.assign(moodChange = lastMoodValues - firstMoodValues)
	subset = subset.assign(moodChangePercent = ((lastMoodValues - firstMoodValues)/firstMoodValues)*100)

	effective = subset.loc[subset.moodChangePercent < -49.9]

	cols = ["boughtTime", "MoodScores", "moodChangePercent"]
	subset[cols].to_csv('effectiveData.csv')
	print("Effective for", effective.shape[0], "users during this period.")
	print("Criteria: At least 2 PHQ9 values, PHQ9 change of >= 50% between first and last PHQ9.")
	input()


# FUNCTIONS TO ADD
#
# Make this into a function that selects people who have used the program for a certain amount of time. Add in something from Ace's new data that limits it to people who have signed in more than X times (i.e., their collections of dates signed in is greater than X size.)
# in15 = data.loc[(data.todaysDate - data['Time Started (UTC)']) > pd.Timedelta(days=15)


def leaveMenu():
	global inMenu
	inMenu = False
# setup menu

menuOptions = {
	"cutColumns()" : cutColumns,
	"recentRows()" : recentRows,
	"findUser()" : findUser,
	"activeUsers()" : activeUsers,
	"newSignups()" : newSignups,
	"purchasesByMonth()" : purchasesByMonth,
	"metrics()" : metrics,
	"behaviorMetrics()" : behaviorMetrics,
	"boughtByDay()" : boughtByDay,
	"boughtByDay30() - like above, but for 30 days" : boughtByDay30,
	"phq9Change()" : phq9Change,
	"phq9ChangeInput()" : phq9ChangeInput,
	"mjEntriesCompleted()" : mjEntriesCompleted,
	"toolboxEngagement()" : toolboxEngagement,
	"gotValue()" : gotValue,
	"effective()" : effective,
	"Leave the Menu." : leaveMenu,
}

inMenu = False

options = list(menuOptions.keys())

print("Need a menu? (y/n)")
x = input()
if x == "y" or x == "yes" or x == "Y" or x == "Yes":
	inMenu = True

while inMenu:
	print("======================")
	print("Available functions:")

	for option in options:
		print(str(options.index(option)), ":", option)

	print("Please type the number of the function you wish to run (e.g. 5)")
	print("===========================")
	choice = int(input())
	functionChosen = menuOptions[options[choice]]

	print("========================")
	functionChosen()
	print("")
	print("========================")
