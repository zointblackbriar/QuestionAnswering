from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.externals import joblib
import numpy as np
from sklearn import linear_model
import warnings
from time import time
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)
from  CreateModel import ModelCreation

from CreateVector import WordVector
TRAINING_DATA_PATH = 'data/train.txt'



WHEN_TYPE = 'when'
WHAT_TYPE = 'what'
WHO_TYPE = 'who'
WHICH_TYPE = 'which'
WHY_TYPE = 'why'
HOW_TYPE= 'how'
QUANTITY_TYPE = 'quantity'
AFFIRMATION_TYPE = 'affirmation'
UNKNOWN_TYPE = 'unknown'

ALL_TYPES = [WHEN_TYPE, WHAT_TYPE, WHO_TYPE, WHICH_TYPE, WHY_TYPE, HOW_TYPE, QUANTITY_TYPE, AFFIRMATION_TYPE, UNKNOWN_TYPE]

class QuestionAssigner():

    def precision(self, y_test, y_pred, strategy = 'weighted'):
        return metrics.precision_score(y_test, y_pred, average=strategy, labels=np.unique(y_pred))

    def recall(self, y_test, y_pred, strategy='weighted'):
        return metrics.recall_score(y_test, y_pred, average=strategy, labels=np.unique(y_pred))

    def f1_score(self, y_test, y_pred, strategy='weighted'):
        return metrics.f1_score(y_test, y_pred, average=strategy, labels=np.unique(y_pred))

    def training_error(self, y_test, y_pred):
        prec = self.precision(y_test, y_pred)
        rec = self.recall(y_test, y_pred)
        f1 = self.f1_score(y_test, y_pred)
        return {"precision":prec, "recall":rec, "f1-score":f1}


    @staticmethod
    def predictQuestion(question):
        model_loader = joblib.load('model/LogisticRegressionNew.pkl')
        encoder = LabelEncoder()
        encoder.fit(ALL_TYPES)
        if(model_loader == None):
            print("model is loaded before")
            model_loader, encoder = ModelCreation.train_vectors("LogisticRegressionCV")
        question = question.lower()
        predicted_cat = encoder.inverse_transform(model_loader.predict([WordVector.create_vector(question)]))
        print("Predicted Category:", predicted_cat[0])
        return predicted_cat[0]

# print(os.getcwd())
# start_time = time()
# obj = QuestionAssigner()
# obj.predictQuestion("how many members of linkedfactory?")
# end_time = time()
# print("Total prediction time: ", end_time - start_time)