import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
import sys
import os
import logging
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

logger = logging.getLogger(__name__)

#This module provides mainly test and train data sets manipulation

class featureEngineering():
    def question_to_dict(self, question):
        dict={}
        for lat in question['LAT']:
            if(lat['type'] != "WordnetLAT"):
                dict['lat/' + lat['text'] + '/' + lat['type']] = 1
        for sv in question['SV']:
            dict['sv'] = sv
        if(len(question['SV']) == 0):
            dict['sv_not_present'] = 1
        return dict
    #The method will logistic regression
    def openTestAndTraining(self):
        try:
            print(os.getcwd())
            with open('data/train-data.json', 'r') as outFile:
                dict = [self.question_to_dict(question) for question in json.load(outFile)]
                vectorDict = DictVectorizer()
                trainVector = vectorDict.fit_transform(dict)
            with open('data/train-data.json', 'r') as outFile:
                dict = [self.question_to_dict(question) for question in json.load(outFile)]
                testVector = vectorDict.transform(dict)
            with open('data/train-data.tsv', 'r') as file:
                #open labeled data
                trainY = [line.split("\t")[3].replace("\n", "") for line in file]
                #get all labeled data such as ABBR, HUM, NUM, ENTY, DESC
                #print(trainY)
            with open('data/test-data.tsv', 'r') as file:
                testY = [line.split("\t")[3].replace("\n", "") for line in file]
                #Get all test data
                #print(testY)

            logResult = LogisticRegression(solver='lbfgs', multi_class='multinomial')
            logResult.fit(trainVector, trainY)
            print(logResult.score(trainVector, trainY))
            resultCross = cross_validation.cross_val_score(logResult, trainVector, trainY, cv=10)
            print("10 fold cross validation accuracy:")
            print(resultCross)
            print("Average over folds")
            print(sum(resultCross) / float(len(resultCross)))
            #print("Accuracy on test data set")
            #print(logResult.score(testVector, testY))

            #Error analysis
            testVector[0]
            s = set()
            [s.add(e) for e in trainY]
            print(sorted(s))
            with open('data/test-data.tsv', 'r') as file:
                for i, line in enumerate(file):
                    if(logResult.predict(testVector) != testY[i]):
                        splitted = line.replace("\n", "").split("\t")
                        idxs = []
                        for key in dict[i]:
                            if(key == 'sv'):
                                key = key + "=" + dict[i][key]
                                idxs.append(vectorDict.feature_names_.index(key) if key in vectorDict.feature_names_ else 'Not present')
                        coefs = [[c[idx] for c in logResult.coef_] if idx != 'Not present' else 'Not present' for idx in idxs]

                        print(splitted[0], splitted[2], splitted[3], logResult.predict(testVector[i]), dict[i])
                        print("Class coefficients for LATs and SV:" + str(coefs))
                        print()
        except:
            logger.exception("Error Analysis Error")


# obj = featureEngineering()
# obj.openTestAndTraining()

