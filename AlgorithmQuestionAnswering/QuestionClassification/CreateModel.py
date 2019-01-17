import warnings

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
from sklearn import metrics
from sklearn import linear_model
from CreateVector import WordVector
import logging
import os
warnings.filterwarnings("ignore", category=DeprecationWarning)
# os.chdir(r'../')


logger = logging.getLogger(__name__)

WHEN_TYPE = 'when'
WHAT_TYPE = 'what'
WHO_TYPE = 'who'
WHICH_TYPE = 'which'
WHY_TYPE = 'why'
HOW_TYPE = 'how'
QUANTITY_TYPE = 'quantity'
AFFIRMATION_TYPE = 'affirmation'
UNKNOWN_TYPE = 'unknown'

ALL_TYPES = [WHEN_TYPE, WHAT_TYPE, WHO_TYPE, WHICH_TYPE, WHY_TYPE, HOW_TYPE, QUANTITY_TYPE, AFFIRMATION_TYPE, UNKNOWN_TYPE]

TRAINING_DATA_PATH = 'data/train.txt'

#print(os.getcwd())
class ModelCreation():

    def __del__(self):
        logger.info("deleted")

    @staticmethod
    def load_data(filename):
        try:
            res = []
            #open the train data
            with open(filename, 'r+') as file:
                for line in file:
                    #parse with the following label
                    question, label = line.split("|", 1)
                    res.append((question.strip(), label.strip()))
        except :
            logger.exception("Error while opening the file")
        return res

    @staticmethod
    def train_vectors(method):
        try:
            train_data = ModelCreation.load_data(TRAINING_DATA_PATH)

            question_vectors = np.asarray([WordVector.create_vector(line[0]) for line in train_data])
            encoder = LabelEncoder()
            encoder.fit(ALL_TYPES)
            train_labels = encoder.transform([line[1] for line in train_data])
            #We use optimized limited memory approach called BFGS
            #Lbfgs method might be used. -- https://stats.stackexchange.com/questions/284712/how-does-the-l-bfgs-work
            """The following method will be tested and we show the result to the end user"""
            if(method == "LogisticRegregressionLBFGS"):
                trainedModel = linear_model.LogisticRegression(multi_class='multinomial', solver='lbfgs')
            elif(method == "LogisticRegressionCV"):
                trainedModel = linear_model.LogisticRegressionCV(cv=7, random_state=0, multi_class='multinomial')
            elif(method == "LogisticRegressionNewton"):
                trainedModel = linear_model.LogisticRegressionCV(multi_class='multinomial', solver='newton-cg')
            trainedModel.fit(question_vectors, train_labels)
            joblib.dump(trainedModel, 'model/LogisticRegressionNew.pkl')
            train_data_prediction = trainedModel.predict([WordVector.create_vector(line[0].lower()) for line in train_data])
            from QuestionClassifier import QuestionAssigner
            assigner = QuestionAssigner()
            print("training error Logistic Regression: ", assigner.training_error(train_labels, train_data_prediction))
            return trainedModel, encoder
        except:
            logger.exception("Train vectors error")

# obj = ModelCreation()
# obj.train_vectors("LogisticRegressionCV")