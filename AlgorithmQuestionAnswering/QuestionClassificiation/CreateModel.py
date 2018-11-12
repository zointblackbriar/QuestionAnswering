import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
from sklearn import metrics
from sklearn import linear_model
from CreateVector import WordVector
import logging

logger = logging.getLogger(__name__)

categories = ['when', 'what', 'who', 'affirmation', 'unknown']

training_data_path = 'data/train.txt'

class ModelCreation():
    def load_data(self, filename):
        try:
            res = []
            #open the train data
            with open(filename, 'r') as file:
                for line in file:
                    #parse with the following label
                    question, label = line.split("|", 1)
                    res.append((question.strip(), label.strip()))
        except :
            logger.exception("Error while opening the file")
        return res

    def trainVectorsProperly(self):
        try:
            train_data = self.load_data(training_data_path)
            print_train_data = (line[0] for line in train_data)
            print(print_train_data)
            question_vectors = np.asarray([WordVector.create_vector(line[0]) for line in train_data])
            encoder = LabelEncoder()
            encoder.fit(categories)
            train_labels = encoder.transform([line[1] for line in train_data])
            clf = linear_model.LogisticRegression(multi_class='multinomial', solver='lbfgs')
            clf.fit(question_vectors, train_labels)
            joblib.dump(clf, 'model/modelCreated.model')
            print("Saved to disk")
        except:
            logger.exception("Train vectors error")

