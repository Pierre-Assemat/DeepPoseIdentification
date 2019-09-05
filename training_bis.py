import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from keras import Sequential
from keras.layers import Dense, Dropout
from keras.regularizers import l2
from keras.constraints import unit_norm

class Training():

	def __init__(self, name_pickle=None, data=None):

		if name_pickle is not None :
			dataset = pd.read_pickle(name_pickle)
			data = pd.DataFrame(dataset)
		self.data = data.sample(frac=1)


	def split_data(self, nb_features=54):
		# creating input features and target variables
		X = self.data.iloc[:, :nb_features]
		y = self.data.iloc[:, -1]

		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3)
		
		return self.X_train, self.X_test, self.y_train, self.y_test

	def buildDNN(self, hidden_layers=2):

		self.classifier = Sequential()

		#First Hidden Layer
		self.classifier.add(Dense(12, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01), activation='relu',kernel_constraint=unit_norm(), kernel_initializer='random_normal', input_dim=54))
		self.classifier.add(Dropout(0.2))

		for nbLayer in range(hidden_layers - 1):
			self.classifier.add(Dense(12, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01), activation='relu', kernel_initializer='random_normal'))
			self.classifier.add(Dropout(0.2))
		
		#Output Layer
		self.classifier.add(Dense(1, activation='sigmoid', kernel_initializer='random_normal'))
		#Compiling the neural network
		self.classifier.compile(optimizer ='adam', loss='binary_crossentropy', metrics =['accuracy'])


	def train(self):	
		#Fitting the data to the training dataset
		self.history = self.classifier.fit(self.X_train, self.y_train, validation_split=0.33, batch_size=10, epochs=50)

		return self.history

	def plot_acc(self, all=None):
		
		# summarize history for accuracy
		plt.plot(self.history.history['acc'])
		plt.plot(self.history.history['val_acc'])
		plt.title('model accuracy')
		plt.ylabel('accuracy')
		plt.xlabel('epoch')
		plt.legend(['train', 'test'], loc='upper left')

		if not all:
			plt.show()

	def plot_loss(self):
		# summarize history for loss
		plt.plot(self.history.history['loss'])
		plt.plot(self.history.history['val_loss'])
		plt.title('model loss')
		plt.ylabel('loss')
		plt.xlabel('epoch')
		plt.legend(['train', 'test'], loc='upper left')
		plt.show()

	def plot_all(self):
		plt.figure()
		plt.subplot(1,2,1)
		self.plot_acc(True)
		plt.subplot(1,2,2)
		self.plot_loss()

if __name__ == '__main__':
	training = Training(name_pickle='openPoseDataset.pkl')
	training.split_data()
	training.buildDNN()
	training.train()
	training.plot_all()

