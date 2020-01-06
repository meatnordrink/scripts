# Once live, incorporate `platformPurchased` variable (set in Introduction) to Metrics() to allow revenue calculation. 
# make parseArray() setting a function, replace in functions
# add a function that takes the start, end points, and makes them variables, so you can just enter `start`, `end`.
# figure out if I can do something similar to `usecols` but with rows, so that, if I want to import the full csv, I can cut out a lot of the old columns, so it will actually load. 


print("-------------------")
print("")
print("- Make sure you are using python3. You may need to run python with `python3` rather than `python`. (Many systems have both installed.)")
print("")
print("- Pandas is imported by default.")
print("Please note that: ")
print(" - all email addresses are converted to lowercase on import; you'll need to search for them as lowercase.")
print(" - some functions (any based on `todaysDate`) require the input range to include the most recent date in the CSV to be accurate. Which input is required is noted for each function.")
print("")
print("-------------------")

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
		data = pd.read_csv(csvIn, parse_dates=['todaysDate', 'Time Started (UTC)', 'REGstartTime', 'pricingTime', 'boughtTime'], converters={"MoodScores": str, "MJentriesCompletedEachSession": str, "toolboxEngagement": str}, low_memory=False)
	if fullImport == "n":
		data = pd.read_csv(csvIn, usecols=['pricingTime','utm_source', 'couponCode', 'name', 'email', 'name','Run', 'User', 'Time Started (UTC)', 'iosApp', 'currentSession', 'sessionsCompleted', 'boughtTrigger','subscription_status', 'paywallEmail', 'paywallUserID', 'currentlyBrowsingMenus', 'currentlymidsession', 'todaysDate', 'Time Started (UTC)', 'boughtTime', 'payment_plan', 'iosApp', 'programStartTime', 'sessionsCompleted', 'REGstartTime', 'REGduration', 'FFduration', 'MBduration', 'PAduration', 'LIESduration','NumberOfChallengesCompleted', 'receivingMJprompts','MoodScores', 'MJentriesCompletedEachSession', 'toolboxEngagement', 'daysActiveNb', 'satisfactionFeedbackIntro', 'upliftRatingatFF', 'upliftRatingatTE', 'MJentriesCompletedbyFFstart', 'averageMJsPerDayEachSess', 'toolboxMetrics', 'homeMetrics', 'settingsMetrics', 'LearnTabMetrics', 'bugsByMB', 'bugsByIMJ', 'bugsByMBdescription', 'bugsByIMJdescription', 'cancellationReason', "Points", "Minutes Spent", "subscriptionCreated", 'subscription_start_date', 'platform'], parse_dates=['todaysDate', 'Time Started (UTC)', 'REGstartTime', 'pricingTime', 'boughtTime', 'subscription_start_date'], converters={"MoodScores": str, "MJentriesCompletedEachSession": str, "toolboxEngagement": str}, low_memory=False)
	excludedNames = ['Qanielle', 'Johnny Vampire', 'Aislinntesting', 'SpencerTest', 'Banana']
	# Could exclude some data based on emails as well; Spencer has one willfind@gmail.com that keeps slipping in.
	mask = data.name.apply(lambda name: name not in excludedNames)
	dataReal = data.loc[mask]
	data = dataReal
	# it would be nice to figure out how to make this line not throw an error
	data.email = data.email.str.lower()
	if data.shape[0] > 0:
		print("Your data is now imported, and can be referenced as the variable `uplift.data`.")
		print(data.shape[0], "lines imported; all employee data excluded.")
		print("If you wish to utilize the available functions directly, they may be imported via `import from uplift *`")



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

def findActives():
	"""Finds active users, defined as users who have purchased the program (ever) and used it between the dates selected. 
	Returns `actives`. 
	"""
	print("Input: Last 30 days.")
	startDate, endDate = inputDate()
	boughtEver = data.loc[data.boughtTrigger == "fired"]
	withinRange = boughtEver.loc[boughtEver.todaysDate.between(startDate, endDate)]
	actives = withinRange
	return actives

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
	userData = data.loc[(data.email == userEmail), ['name','Run', 'User', 'Time Started (UTC)', 'REGstartTime', 'iosApp', 'currentSession', 'sessionsCompleted', 'boughtTrigger','subscription_status', 'paywallEmail', 'paywallUserID', 'currentlyBrowsingMenus', 'currentlymidsession']]
	print("Name:", userData.name.item())
	print("Run #:", userData.Run.item())
	print("User ID:", userData.User.item())
	print("Time Started (UTC):", userData['Time Started (UTC)'].item())
	print("REGstartTime", userData.REGstartTime.item())
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

def activeUsersAndSpread():
	"""Prints out the number of all users for whom `boughtTrigger='fired'` and `todaysDate` is within the specified range.
	Syntax is activeUsersAndSpread(startDate, endDate). Both startDate and endDate must be enclosed in quotes, separately, and in YYYY-MM-DD format.
	Example:
	activeUsersAndSpread('2019-03-11', '2019-03-18')
	Notes:
	* Do not add quotes if using the menu interface.
	* THIS CANNOT BE USED RETROACTIVELY; i.e., IT ONLY WORKS IF THE RANGE INCLUDES THE FINAL DATE IN THE CSV, as it is dependent on the `todaysDate` variable, which is overwritten with each new sign-in. In other words, a user will appear to be active only in the latest period in which they were active.

	"""
	print("Input: Last 30 days.")
	startDate, endDate = inputDate()
	boughtEver = data.loc[data.boughtTrigger=="fired"]
	#boughtEver.todaysDate = boughtEver.todaysDate.apply(pd.to_datetime) # the .apply is necessary to avoid a chain-indexing warning, "SettingWithCopyWarning". An alternative is to set the relevant columns as dates on import, with pd.read_csv('input.csv', parse_dates=['Time Started (UTC)', 'timeStarted'), though that might mean the metrics() function needs to be adjusted accordingly (no, as I didn't use 'Time Started (UTC)')
	withinRange = boughtEver.loc[boughtEver.todaysDate.between(startDate, endDate)]
	global actives
	actives = withinRange
	print("Between", startDate, "and", endDate, "there were:")
	print(withinRange.shape[0], "active, paying users.")
	spread = withinRange.currentSession.value_counts() 
	for x in range(0, len(spread)):
		print(spread.index[x], spread[x])
	printToCSV(withinRange)


def newSignups():
	"""Prints out the number of all users for whom `REGstartTime` is within the specified range.
	Syntax is newSignups(startDate, endDate). Both startDate and endDate must be enclosed in quotes, separately, and in YYYY-MM-DD format.
	Example:
	newSignups('2019-03-11', '2019-03-18')
	Note: Do not include quotes if using the menu interface.
	"""
	# data['Time Started (UTC)'] = data['Time Started (UTC)'].apply(pd.to_datetime) I believe this worked; the above still seems to have triggered the error. Both obsolete now, but might need to figure out what was happening in the future.
	print("Input: Period desired.")
	startDate, endDate = inputDate()
	withinRange = data.loc[data['REGstartTime'].between(startDate, endDate)]
	print("Between", startDate, "and", endDate, "there were:")
	print(withinRange.shape[0], "new sign-ups.")
	printToCSV(withinRange)

def purchasesByTime():
	"""Extracts the number of purchases in a given period.
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
	boughtThisMonth = data.loc[data.boughtTime.between(startDate, endDate)]
	# Check to make sure this `payment_plan` variable is stable.
	quarterlySubs = boughtThisMonth.loc[boughtThisMonth.payment_plan == 'quarterlysub']

	monthlySubs = boughtThisMonth.shape[0] - quarterlySubs.shape[0]

	iosBought = boughtThisMonth.loc[boughtThisMonth.iosApp == 1]

	androidBought = boughtThisMonth.loc[boughtThisMonth.iosApp == 2]

	webBought = boughtThisMonth.loc[boughtThisMonth.iosApp == 0]

	# Find revenue
	# This needs to be adjusted to reflect net revenue (see below) - Danielle gets gross figures. platform specific rates: Android/iOS - .3. Braintree - .02. Platform specific variable is coming/may be live already. 
	quarterlySubRev = quarterlySubs.shape[0] * 45
	monthlySubRev = monthlySubs * 30
	totalNewSubRev = quarterlySubRev + monthlySubRev
	# this may need to get more precise, if we wish to reflect the difference in cut Braintree takes vs the apps. Currently, the idea would be to just * .7 to get our share of this.

	# REDO THIS TO REFLECT `platformPurchased` AND REV LOST TO PLATFORMS. Note that `totalRev` is gross; but anything based on `monthlySubRev` or `totalNewSubRev` is inflated, as anyone on an app platform generates less than 30/45 (*.7).

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
	input()

def behaviorMetrics():
	"""Syntax is:
	useMetrics()
	"""
	print("Input: Last 30 days")
	print("===============================")
	print("What starting date? YYYY-MM-DD")
	startDate = pd.to_datetime(input())
	print("What end date? YYYY-MM-DD")
	endDate = pd.to_datetime(input())
	boughtEver = data.loc[data.boughtTrigger == "fired"]
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
	input()

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
	It pulls data for users who purchased within the input range.
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

	print("Input: Target month.")
	print("========================")
	startDate, endDate = inputDate()
	bought = data.loc[data.boughtTime.between(startDate, endDate)]

	bought.MoodScores = bought.MoodScores.apply(parseNumericArray)

	subset = bought.loc[bought.MoodScores.apply(len) > 1]
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
	"""For active users, the average number of the MJentriesCompletedEachSession variable. Users with no entries are counted as 0, and included in the average.
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

	actives = findActives()
	actives.MJentriesCompletedEachSession = actives.MJentriesCompletedEachSession.apply(parseNumericArray)

	firstEntries = actives.MJentriesCompletedEachSession.apply(lambda x: x[0])
	firstEntriesNoZeroes = firstEntries.loc[firstEntries > 0]
	firstEntriesPercentZeroes = round((1-((firstEntriesNoZeroes.shape[0])/(firstEntries.shape[0])))*100, 2)

	secondSet = actives.loc[actives.MJentriesCompletedEachSession.apply(len) > 1]
	secondEntries = secondSet.MJentriesCompletedEachSession.apply(lambda x: x[1])
	secondEntriesNoZeroes = secondEntries.loc[secondEntries > 0]
	secondEntriesPercentZeroes = round((1-((secondEntriesNoZeroes.shape[0])/(secondEntries.shape[0])))*100, 2)

	thirdSet = actives.loc[actives.MJentriesCompletedEachSession.apply(len) > 2]
	thirdEntries = thirdSet.MJentriesCompletedEachSession.apply(lambda x: x[2])
	thirdEntriesNoZeroes = thirdEntries.loc[thirdEntries > 0]
	thirdEntriesPercentZeroes = round((1-((thirdEntriesNoZeroes.shape[0])/(thirdEntries.shape[0])))*100, 2)

	fourthSet = actives.loc[actives.MJentriesCompletedEachSession.apply(len) > 3]
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
	input()

# def toolboxEngagement():
# 	"""Reports from the collection toolboxEngagement, which measures user use of toolbox functions. This function needs to be updated to take the updated toolbox options into account (as of April 2019).
# 	NOTE: THIS FUNCTION IS OBSOLETE AS OF 04/19"""
# 	def parseArray(arr):
# 		"""Takes as input a string that looks like an array and returns an array of values. The values in the array are not necessarily of the same type. The function attempts to eval() each value in the array; but if it fails, it leaves the unevaluated string in place."""
# 		cleaned = arr.replace(" ", "").replace("[", "").replace("]", "")
# 		vals = cleaned.split(",")

# 		for i in range(0, len(vals)):
# 			try:
# 				vals[i] = eval(vals[i])
# 			except:
# 				pass

# 		return vals

# 	def parseNumericArray(arr):
# 		"""Takes as input a string that looks like an array and returns an array of numeric values. Any value in the array that can't be evaluated is turned into a zero."""
# 		out = parseArray(arr)

# 		for i in range(0, len(out)):
# 			if isinstance(out[i], str):
# 				out[i] = 0

# 		return out

# 	bought = data.loc[data.boughtTrigger == "fired"]
# 	# bought = bought.toolboxEngagement.fillna("zero")
# 	noEngagement = bought.loc[bought.toolboxEngagement == ""]
# 	percentNone = round((noEngagement.shape[0])/(bought.shape[0]), 2)*100
# 	engaged = bought.loc[bought.toolboxEngagement != ""]
# 	engaged = engaged.toolboxEngagement.apply(parseNumericArray)

# 	num3 = engaged.apply(lambda x: x[2])
# 	num3once = num3.loc[num3 > 0]
# 	num3twice = num3.loc[num3 > 1]

# 	num4 = engaged.apply(lambda x: x[3])
# 	num4once = num4.loc[num4 > 0]
# 	num4twice = num4.loc[num4 > 1]

# 	num6 = engaged.apply(lambda x: x[5])
# 	num6once = num6.loc[num6 > 0]
# 	num6twice = num6.loc[num6 > 1]

# 	num7 = engaged.apply(lambda x: x[6])
# 	num7once = num7.loc[num7 > 0]
# 	num7twice = num7.loc[num7 > 1]

# 	num8 = engaged.apply(lambda x: x[7])
# 	num8once = num8.loc[num8 > 0]
# 	num8twice = num8.loc[num8 > 1]

# 	# - #3 session outline, #4 session review, #6 facts/sources, #7 problem solver, #8 contribute to uplift



# 	print("Percent 0 toolbox engagment: %", percentNone)
# 	print("")
# 	print("Session Outline, engaged once or more: %", round((num3once.shape[0]/num3.shape[0])*100, 2))
# 	print("--, twice or more: %", round((num3twice.shape[0]/num3.shape[0])*100, 2))
# 	print("")
# 	print("Session Review, engaged once or more: %", round((num4once.shape[0]/num4.shape[0])*100, 2))
# 	print("--, twice or more: %", round((num4twice.shape[0]/num4.shape[0])*100, 2))
# 	print("")
# 	print("Facts/Sources, engaged once or more: %", round((num6once.shape[0]/num6.shape[0])*100, 2))
# 	print("--, twice or more: %", round((num6twice.shape[0]/num6.shape[0])*100, 2))
# 	print("")
# 	print("Problem Solver, engaged once or more: %", round((num7once.shape[0]/num7.shape[0])*100, 2))
# 	print("--, twice or more: %", round((num7twice.shape[0]/num7.shape[0])*100, 2))
# 	print("")
# 	print("Contribute to UpLift, engaged once or more: %", round((num8once.shape[0]/num8.shape[0])*100, 2))
# 	print("--, twice or more: %", round((num8twice.shape[0]/num8.shape[0])*100, 2))
# 	input()

def gotValue():
	"""This returns the number/% of users retained, who got value, defined as having 15 days between first and most recent use of the program, and having completed at least 2 PHQ9's (which is a proxy for two sessions).
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

	print("Input: Last 30 days")
	print("======================")
	startDate, endDate = inputDate()
	bought = data.loc[data['boughtTime'].between(startDate, endDate)]
	bought = bought.assign(daysIn = bought.todaysDate - bought.boughtTime)
	retained = bought.loc[bought.daysIn >= pd.Timedelta(days=15)]
	bought.MoodScores = bought.MoodScores.apply(parseNumericArray)
	subset = bought.loc[bought.MoodScores.apply(len) > 1]
	gotValue = bought.loc[bought.MoodScores.apply(len) > 1]
	
	# I believe I can comment these 4 lines below out; I believe they go with the next function. 
	# firstMoodValues = subset.MoodScores.apply(lambda x: x[0])
	# lastMoodValues = subset.MoodScores.apply(lambda x: x[len(x)-1])
	# subset = subset.assign(moodChange = lastMoodValues - firstMoodValues)
	# subset = subset.assign(moodChangePercent = ((lastMoodValues - firstMoodValues)/firstMoodValues)*100)

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

	cols = ["daysIn", "Time Started (UTC)", "todaysDate", "boughtTrigger", "Points", "Minutes Spent"]
	subset[cols].to_csv('gotValueData.csv')

	print(bought.shape[0], "bought.")
	print(retainedPercent, "% retained 15 days after purchase (", retained.shape[0], ")")
	print(gotValuePercent, "% got value (", gotValue.shape[0], ")")
	#print(effectedPercent, "% for whom UpLift was effective (", effected.shape[0], "out of", inEffectSpan.shape[0], " purchasers between 4 and 1 months before period.)")
	print("Dataset exported to gotValueData.csv")
	input()

def effective():
	"""This returns the number/% of users retained, who got value, and for whom UpLift was effective, based on users who purchased during the input time period. The numbers are based on the definitions of these terms set in the Monthly Metrics google doc.
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

	print("Input: Last 30 days")
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
# Make this into a function that selects people who have used the program for a certain amount of time. Add in something from Ace's new data tha limits it to people who have signed in more than X times (i.e., their collections of dates signed in is greater than X size.)
# in15 = data.loc[(data.todaysDate - data['Time Started (UTC)']) > pd.Timedelta(days=15)

def daysActive():
	""" This function tells you the average number of days users who purchased within a certain period have been active since that period.
	"""
	print("Please enter the date range for purchasers:")
	startDate, endDate = inputDate()
	bought = data.loc[data.boughtTime.between(startDate, endDate)]

	averageDaysActive = bought.daysActiveNb.mean()
	print("Average days active:", round(averageDaysActive, 1))

	# The rest of this was an attempt to output average # of days/wk. In the final line, `timeIn` would need to be converted to an integer to make this work.
	# I'm not actually sure this is a useful metric, so I'm abandoning it for the moment.
	# bought = bought.assign(timeIn = bought.todaysDate - bought.REGstartTime)
	# bought = bought.where(bought.timeIn > pd.Timedelta(days=1), pd.Timedelta(days=1))
	# bought = bought.assign(avgDays = bought.daysActiveNb/timeIn)
	# print("Average number of days active/week:")
	print("Please note that this function is no longer actively recorded.")
	input()

def satisfactionMetrics():
	"""For purchasers during a given period, gives average satisfaction metrics at three different points in the program. Note that this data exists only since May 2019.
	"""
	print("For purchasers in what period?")
	startDate, endDate = inputDate()
	bought = data.loc[data.boughtTime.between(startDate, endDate)]

	meanReg = bought.satisfactionFeedbackIntro.mean()
	FFsubset = bought.loc[bought.upliftRatingatFF.notnull() == True]
	meanFF = FFsubset.upliftRatingatFF.mean()
	TEsubset = bought.loc[bought.upliftRatingatTE.notnull() == True]
	if bought.upliftRatingatTE.notnull().sum() ==  0:
		meanTE = 0
	else:
		meanTE = TEsubset.upliftRatingatTE.mean()

	print("Mean Satisfaction Scores (Intro 1-5, others 1-10)")
	print("1:", round(meanReg))
	print("2:", round(meanFF), "(", FFsubset.shape[0], "total entries)")
	print("8:", round(meanTE), "(", TEsubset.shape[0], "total entries)")

	input()

def whatsBeingUsed():
	"""Various metrics relating to what parts of UpLift are being used by how many users. Metrics are for purchasers of UpLift in the period specified. Note that these metrics were added in May 2019, and are not accessible before that period."""

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

	print("Note that this function does not exist prior to April 2019.")
	print("Dates - purchase range.")
	startDate, endDate = inputDate()

	print("Free only? y/n")
	free = input().lower()
	if free == "y":
		bought = data.loc[data.REGstartTime.between(startDate, endDate)]
		bought = bought.loc[bought.boughtTrigger != "fired"]
		print("Active > 1 day? y/n")
		wantActive = input().lower()
		if wantActive == "y":
			bought = bought.loc[(bought.todaysDate - bought.REGstartTime) > pd.Timedelta(days=1)]
	else:
		bought = data.loc[data.boughtTime.between(startDate, endDate)]

	# Avg MJentriesCompletedbyFFstart
	bought.MJentriesCompletedbyFFstart = bought.MJentriesCompletedbyFFstart.fillna(0)
	avgMJbyFF = bought.MJentriesCompletedbyFFstart.mean()

	# averageMJsPerDayEachSess - validated 6/2019
	arrayData = bought.loc[bought.averageMJsPerDayEachSess.notnull() == True]
	arrayData.averageMJsPerDayEachSess = arrayData.averageMJsPerDayEachSess.apply(parseNumericArray)
	lengths = arrayData.averageMJsPerDayEachSess.apply(lambda x : len(x))
	max = lengths.max()
	averages = []
	counts = []
	for i in range(0, max):
		subset = arrayData.averageMJsPerDayEachSess.loc[lengths > i]
		vals = subset.apply(lambda x: x[i])
		counts.append(vals.count())
		averages.append(vals.mean())
	print("==========(begin)=======================")
	print("**Avg Mood Journal Entries**")
	print("")
	print("avgMJbyFF", round(avgMJbyFF, 2))
	print("--averageMJsPerDayEachSess--")
	print("MB, # entries:", counts[0],"AVG:", round(averages[0], 2))
	print("PA, # entries:", counts[1], "AVG", round(averages[1], 2))
	print("LIES, # entries:", counts[2], "AVG", round(averages[2], 2))
	print("IMJ, # entries:", counts[3], "AVG", round(averages[3], 2))
	print("SUCC, # entries:", counts[4], "AVG", round(averages[4], 2))
	print("TE, # entries:", counts[5], "AVG", round(averages[5], 2))
	print("")

	#toolboxMetrics
	empty = bought.toolboxMetrics.isnull().sum()
	bought.toolboxMetrics = bought.toolboxMetrics.fillna("[0,0,0,0,0,0,0,0,0,0,0]")
	bought.toolboxMetrics = bought.toolboxMetrics.apply(parseNumericArray)
	zeroes = []
	means = []
	medians = []
	for i in range(0, 10):
		vals = bought.toolboxMetrics.apply(lambda x : x[i])
		val = 0
		zeroes.append(vals.apply(lambda x: 1 if x == val else 0).sum())
		means.append(vals.mean())
		medians.append(vals.median())


	print("=====================================================")
	print("**Toolbox Metrics**")
	print("")
	print("Never visited Toolbox:", empty, "of", bought.shape[0])

	toolboxTitles = ['Mood Boosters', 'Positive Activities', 'Trigger Plan', 'Noticing Successes', 'Goal Trainer', 'Thought Errors', 'Reframe a Struggle', 'Balanced Belief', 'Problem Solver', 'Find Support', 'Contribute to UpLift']
	for i in range (0, 10):
		print("")
		print(toolboxTitles[i])
		print("Average visits to, mean:", round(means[i], 2))
		print("Average visits to, median:", medians[i])
		print("Of", bought.shape[0], "total", zeroes[i], "never visited.")

	#homeMetrics
	empty = bought.homeMetrics.isnull().sum()
	bought.homeMetrics = bought.homeMetrics.fillna("[0,0,0,0,0]")
	bought.homeMetrics = bought.homeMetrics.apply(parseNumericArray)
	zeroes = []
	means = []
	medians = []
	for i in range(0, 4):
		vals = bought.homeMetrics.apply(lambda x : x[i])
		val = 0
		zeroes.append(vals.apply(lambda x: 1 if x == val else 0).sum())
		means.append(vals.mean())
		medians.append(vals.median())


	print("=====================================================")
	print("**Home Metrics**")
	print("")
	print("Never visited Home menu:", empty, "of", bought.shape[0])

	titles = ['Daily Tasks', 'Community Lounge', 'Contact UpLift', 'Refer a Friend', 'Account/Settings']
	for i in range (0, 4):
		print("")
		print(titles[i])
		print("Average visits to, mean:", round(means[i], 2))
		print("Average visits to, median:", medians[i])
		print("Of", bought.shape[0], "total", zeroes[i], "never visited.")

	#LearnTabMetrics
	empty = bought.LearnTabMetrics.isnull().sum()
	bought.LearnTabMetrics = bought.LearnTabMetrics.fillna("[0,0,0,0,0,0,0,0]")
	bought.LearnTabMetrics = bought.LearnTabMetrics.apply(parseNumericArray)
	zeroes = []
	means = []
	medians = []
	for i in range(0, 7):
		vals = bought.LearnTabMetrics.apply(lambda x : x[i])
		val = 0
		zeroes.append(vals.apply(lambda x: 1 if x == val else 0).sum())
		means.append(vals.mean())
		medians.append(vals.median())


	print("=====================================================")
	print("**Learn Tab Metrics**")
	print("")
	print("Never visited Learn menu:", empty, "of", bought.shape[0])

	titles = ['Depression Basics', 'Anxiety', 'Food and Mood', 'Sleep', 'Anger and Irritability', 'Review a previous session', 'Facts and Sources', 'Session Outline']
	for i in range (0, 7):
		print("")
		print(titles[i])
		print("Average visits to, mean:", round(means[i], 2))
		print("Average visits to, median:", medians[i])
		print("Of", bought.shape[0], "total", zeroes[i], "never visited.")

	#settingsMetrics
	# empty = bought.settingsMetrics.isnull().sum()
	# bought.settingsMetrics = bought.settingsMetrics.fillna("[0,0,0,0,0,0,0,0,0,0,0]")
	# bought.settingsMetrics = bought.settingsMetrics.apply(parseNumericArray)
	# zeroes = []
	# means = []
	# medians = []
	# for i in range(0, 10):
	# 	vals = bought.settingsMetrics.apply(lambda x : x[i])
	# 	val = 0
	# 	zeroes.append(vals.apply(lambda x: 1 if x == val else 0).sum())
	# 	means.append(vals.mean())
	# 	medians.append(vals.median())
	#
	#
	# print("=====================================================")
	# print("**Settings Metrics**")
	# print("")
	# print("Never visited Settings menu:", empty, "of", bought.shape[0])
	#
	# titles = ['add counselor', 'add friends', 'adjust checkins', 'adjust session summary emails', 'change email address', 'change name', 'unsubscribe from checkins', 'manage subscription', 'change narrator', 'read ToU or PP', 'delete account']
	# for i in range (0, 10):
	# 	print("")
	# 	print(titles[i])
	# 	print("Average visits to, mean:", round(means[i], 2))
	# 	print("Average visits to, median:", medians[i])
	# 	print("Of", bought.shape[0], "total", zeroes[i], "never visited.")

	print("settingsMetrics are ready, and will probably have data by the end of July 2019.")
	input()

def bugs():

	startDate, endDate = inputDate()
	bought = data.loc[data.boughtTime.between(startDate, endDate)]

	# pull - Some vs None; exclude NA. Offer qualitative.
	#bugsByMB
	mbValues = bought.bugsByMB.value_counts()
	imjValues = bought.bugsByIMJ.value_counts()

	print("**MB Bugs**")
	print("Had bugs:", mbValues[1])
	print("No bugs:", mbValues[0])
	print("**IMJ bugs**")
	try:
		print("Had bugs:", imjValues[1])
	except(KeyError):
		print("No values.")
	except:
		tb.print_exc()
	try:
		print("No bugs:", imjValues[0])
	except(KeyError):
		print("No values.")
	except:
		tb.print_exc()

	print("Print out bug descriptions? y/n")
	printYN = input()
	if printYN == 'y':
		cols = ["iosApp", "Run", "bugsByMBdescription", "bugsByIMJdescription"]
		bought[cols].to_csv('MBandIMJbugsDescription.csv')
	
	hadMBBugs = bought.loc[bought.bugsByMBdescription.notnull()]
	MBbugs = hadMBBugs['bugsByMBdescription']
	hadIMJBugs = bought.loc[bought.bugsByIMJdescription.notnull()]
	IMJbugs = hadIMJBugs['bugsByIMJdescription']
	print(MBbugs.values)
	print(IMJbugs.values)
	input()


def test():
	"""Various metrics relating to what parts of UpLift are being used by how many users. Metrics are for purchasers of UpLift in the period specified. Note that these metrics were added in May 2019, and are not accessible before that period."""

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

	print("Note that this function does not exist prior to April 2019.")
	#startDate, endDate = inputDate()
	bought = data.loc[data.boughtTime.between('2019-05-01', '2019-05-31')]
	empty = bought.toolboxMetrics.isnull().sum()
	bought.toolboxMetrics = bought.toolboxMetrics.fillna("[0,0,0,0,0,0,0,0,0,0,0]")
	bought.toolboxMetrics = bought.toolboxMetrics.apply(parseNumericArray)
	# 11 positions [10], get %0 for each, mean() and median(), and count !=0
	# Try parsing with NaN's; if that messes things up, get rid of them first.
	zeroes = []
	means = []
	medians = []
	for i in range(0, 10):
		vals = bought.toolboxMetrics.apply(lambda x : x[i])
		val = 0
		zeroes.append(vals.apply(lambda x: 1 if x == val else 0).sum())
		means.append(vals.mean())
		medians.append(vals.median())


	print("=====================================================")
	print("**Toolbox Metrics**")
	print("")
	print("Never visited toolbox:", empty, "of", bought.shape[0])

	toolboxTitles = ['Mood Boosters', 'Positive Activities', 'Trigger Plan', 'Noticing Successes', 'Goal Trainer', 'Thought Errors', 'Reframe a Struggle', 'Balanced Belief', 'Problem Solver', 'Find Support', 'Contribute to UpLift']
	for i in range (0, 10):
		print("")
		print(toolboxTitles[i])
		print("Average visits to, mean:", round(means[i], 2))
		print("Average visits to, median:", medians[i])
		print("Of", bought.shape[0], "total", zeroes[i], "never visited.")

	input()




	# arrayData = bought.loc[bought.averageMJsPerDayEachSess.notnull() == True]
	# arrayData.averageMJsPerDayEachSess = arrayData.averageMJsPerDayEachSess.apply(parseNumericArray)
	# arrayData.averageMJsPerDayEachSess.to_csv('beforeTransformation.csv')
	# lengths = arrayData.averageMJsPerDayEachSess.apply(lambda x : len(x))
	# max = lengths.max()
	# averages = []
	# counts = []
	# for i in range(0, max):
	# 	subset = arrayData.averageMJsPerDayEachSess.loc[lengths > i]
	# 	vals = subset.apply(lambda x: x[i])
	# 	counts.append(vals.count())
	# 	averages.append(vals.mean())
	# print("MB, # entries:", counts[0],"AVG:", round(averages[0], 2))
	# print("PA, # entries:", counts[1], "AVG", round(averages[1], 2))
	# print("LIES, # entries:", counts[2], "AVG", round(averages[2], 2))
	# print("IMJ, # entries:", counts[3], "AVG", round(averages[3], 2))
	# print("SUCC, # entries:", counts[4], "AVG", round(averages[4], 2))
	# print("TE, # entries:", counts[5], "AVG", round(averages[5], 2))

	input()

def leaveMenu():
	global inMenu
	inMenu = False
# setup menu (as this gets longer, consider breaking things down into categories. Could also string a number of them together so that I can call all the monthly metrics, for example, with a single function; though that could get confusing.)

menuOptions = {
	"cutColumns()" : cutColumns,
	"recentRows()" : recentRows,
	"findUser()" : findUser,
	"activeUsersAndSpread()" : activeUsersAndSpread,
	"newSignups()" : newSignups,
	"purchasesByTime()" : purchasesByTime,
	"metrics()" : metrics,
	"behaviorMetrics()" : behaviorMetrics,
	"boughtByDay()" : boughtByDay,
	"boughtByDay30() - like above, but for 30 days" : boughtByDay30,
	"phq9Change()" : phq9Change,
	"phq9ChangeInput()" : phq9ChangeInput,
	"mjEntriesCompleted()" : mjEntriesCompleted,
	# "toolboxEngagement() - deprecated" : toolboxEngagement,
	"gotValue()" : gotValue,
	"effective()" : effective,
	"daysActive()" : daysActive,
	"satisfactionMetrics()" : satisfactionMetrics,
	"whatsBeingUsed()" : whatsBeingUsed,
	"bugs()" : bugs,
	"test()" : test,
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
	try:
		functionChosen = menuOptions[options[choice]]
	except:
		print("that's not a menu option. Please try again.")
	print("========================")
	try:
		functionChosen()
	except:
		print("ERROR! Details:")
		tb.print_exc()
	print("")
	print("========================")
