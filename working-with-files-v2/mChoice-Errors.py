import csv
import os
import datetime as dt

def correct(answer):
    pos = answer.find("correct")
    return pos >= 0

def addAnswer(userDict, user, timestamp, answer):
    answerDict = {}
    userDict[user] = answerDict
    answerDict["timestamp"] = timestamp
    answerDict["correct"] = correct(answer)

def is_earlier(daytime1, daytime2):
    t1 = dt.datetime.strptime(daytime1, "%m/%d/%y %H:%M")
    t2 = dt.datetime.strptime(daytime2, "%m/%d/%y %H:%M")
    latest = max(t1, t2)
    if latest == t1:
        return False
    return True

# function to gather the data on the mchoice questions
def mchoice_worker(inFileName, outFileName):

    # open the output file for writing
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, outFileName), "w")

    # open the input and output files as csv files
    with open(os.path.join(dir, inFileName)) as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # create an empty problem dictionary
        probDict = dict()

        # loop through the data
        for cols in csv_reader:

            # get the event
            event = cols[4]

            # if mChoice
            if event == "mChoice":

                # get the divid, user, timestamp, and answer
                div = cols[6]
                user = cols[3]
                timestamp = cols[2]
                answer = cols[5]

                # if no dictionary for this problem create one and add this user and answer
                if div not in probDict:
                    userDict = {}
                    probDict[div] = userDict
                else:
                    userDict = probDict[div]

                # if user in dictionary
                if user in userDict:

                    # check if answer is earlier and replace if it is
                    answerDict = userDict[user]
                    oldTime = answerDict["timestamp"]
                    if is_earlier(timestamp, oldTime):
                        answerDict["timestamp"] = timestamp
                        answerDict["correct"] = correct(answer)

                else:
                    addAnswer(userDict, user, timestamp, answer)

        # now print out the interesting stuff
        print("The number of unique multiple-choice questions is {}".format(len(probDict)))

        # for each multiple choice question total the number of correct responses
        for prob in probDict:

            total_correct = 0

            # loop through the users
            user_dict = probDict[prob]
            for user in user_dict:

                answerDict = user_dict[user]
                if answerDict["correct"] == True:
                    total_correct += 1

            # write out the problem id and percent who got it correct
            total_attempted = len(user_dict)
            percent_correct = total_correct / total_attempted
            csv_writer.writerow([prob, total_correct, total_attempted, percent_correct])

    outFile.close()

mchoice_worker("mChoiceSmall.csv", "mchoiceResults.csv")
