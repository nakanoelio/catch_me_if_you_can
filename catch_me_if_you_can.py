# -*- coding: utf-8 -*-
"""Catch me if you can.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SmQFDRG5GlY2udS_HAPGNKgfOeYXMHhy

Exercício I2A2 - K-Means/K-NN - "Catch Me If You Can" dataset (https://www.kaggle.com/danielkurniadi/catch-me-if-you-can)


O exercício envolve a utilização dos dados de teste do dataset "Catch Me If You Can" (test_sessions.csv) 
e a aplicação do da metodologia K-Means sobre os dados de teste para clusterização com 2 K's (clusters) com a finalidade de identificar
o target Alice (0 ou 1, conforme indetificado nos dados de treino).

Após a aplicação do K-Means, treina-se a metodlogia o K-Nearest Neighbors sobre os dados de treino e aplica-se sobre os mesmos dados de treino.

Compara-se com os resultados obtidos com o K-Means.
"""

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

train_df = pd.read_csv('train_sessions.csv')
data_train_df = train_df.dropna()

test_df = pd.read_csv('test_sessions.csv')
data_test_df = test_df.dropna()

"""Para fins da aplicação do K-Means e do K-NN optou-aw por não utilizar os dados temporais visando analisar apenas os dados relativos aos sites visitados.
Adicionalmente, somente foram analisado os casos em que houve 10 (visitados) sites visitados.
Os sites visitados são identificados com números únicos, de forma que cada site possui uma numeração, e salvo engano, podem ser representado, para fins destas metodologias pelos números que lhe são atribuídos ocupando uma localização única dentro do espaço analisado.

Inicialmente, realizou-se o tratamento dos dados de teste para fins da aplicação da metodologia K-Means.
"""

times = ['time%s' % i for i in range(1, 11)]

km_data_test_df = data_test_df.drop(times,axis=1)
km_data_test_df = km_data_test_df.drop('session_id',axis=1)

kmeans = KMeans(n_clusters=2,random_state=0)
kmeans.fit(km_data_test_df)

km_labels = kmeans.labels_

print('{0} e {1} instâncias foram classificados nos clusters 0 e 1, respectivamente, do total de {2} instâncias'.format(len(km_labels)-sum(km_labels), sum(km_labels), len(km_labels)))

km_data_test_df_final = pd.concat([km_data_test_df,  pd.DataFrame(km_labels)], axis=1)

km_data_test_df_final.to_csv('kmeans_result.csv')

"""Realizou-se o tratamento dos dados de treino para fins da aplicação da metodologia K-NN."""

knn_data_train_df_stimes = data_train_df.drop(times,axis=1)
knn_data_train_df = knn_data_train_df_stimes.drop(['session_id', 'target'],axis=1)
knn_data_train_df_target = knn_data_train_df_stimes['target']

knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(knn_data_train_df, knn_data_train_df_target)

knn_target = knn.predict(km_data_test_df)

print('{0} e {1} instâncias foram classificados nos clusters 0 e 1, respectivamente, do total de {2} instâncias'.format(len(knn_target)-sum(knn_target), sum(knn_target), len(knn_target)))

knn_data_test_df_final = pd.concat([km_data_test_df,  pd.DataFrame(knn_target)], axis=1)

knn_data_test_df_final.to_csv('knn_result.csv')

"""Realizamos uma simples comparação entres as duas metodologias, tendo em vista que para o K-Means K-NN obtivemos  as instâncias foram classificados nos clusters 0 e 1.
A classificação nos clusters 0 e 1 é realizada de forma arbitrária pelos algoritmos, de forma que para fins de comparação pode se fazer necessária a troca inversão da classificação, para que ambos o resultado reflitam as mesmas categorias. Não obstante, em razão dos resultados obtidos entendemos que não é necessária a realização da inversão.
"""

comparison = knn_target == km_labels
print('{0}% dos resultados são consistentes entre as metodologias'.format(sum(comparison)/len(comparison)*100))

"""Para fins da escolha do K do K-NN utilizamos a iteração abaixo."""

from sklearn.model_selection import train_test_split
knn_train, knn_test = train_test_split(knn_data_train_df_stimes, test_size=0.2, random_state=10)
i = 1
knn_training = knn_train.drop(['session_id', 'target'],axis=1)
knn_training_target = knn_train['target']

knn_testing = knn_test.drop(['session_id', 'target'],axis=1)
knn_testing_target = knn_test['target']

while i <= 10:
  
  k_testing = KNeighborsClassifier(n_neighbors=i)
  k_testing.fit(knn_training, knn_training_target)
  
  k_score = k_testing.score(knn_testing, knn_testing_target, sample_weight=None)
  print('k = {0}, score = {1}'.format(i, k_score))
  
  i += 1