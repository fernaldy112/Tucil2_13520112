import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import datasets
from myConvexHull import myConvexHull

#choose datasets
print("\nDatasets yang tersedia adalah iris, wine, dan breast_cancer")
dataname = input("Masukkan nama datasets yang ingin digunakan: ")
while (dataname!="iris" and dataname!="wine" and dataname!="breast_cancer"):
    dataname = input("Masukkan nama datasets yang tepat (iris, wine, atau breast_cancer): ")
if dataname=="iris":
    data = datasets.load_iris()
elif dataname=="wine":
    data = datasets.load_wine()
elif dataname=="breast_cancer":    
    data = datasets.load_breast_cancer()

#choose x and y
print("\nBerikut adalah atribut yang bisa dijadikan komponen x dan y:")
for a in range(len(data.feature_names)):
    print(f"{a+1}. {data.feature_names[a]}")
x = int(input(f"\nMasukkan nomor atribut yang ingin digunakan sebagai komponen x: "))
while (x<=0 or x>len(data.feature_names)):
    x = int(input(f"Masukkan nomor atribut yang tepat yang ingin digunakan sebagai komponen x: "))
x -= 1
y = int(input(f"\nMasukkan nomor atribut yang ingin digunakan sebagai komponen y: "))
while (y<=0 or y>len(data.feature_names) or y==x+1):
    y = int(input(f"Masukkan nomor atribut yang tepat yang ingin digunakan sebagai komponen y: "))
y -= 1
    
#create a DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)

#visualisasi hasil ConvexHull
plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title(f'{data.feature_names[x]} vs {data.feature_names[y]}')
plt.xlabel(data.feature_names[x])
plt.ylabel(data.feature_names[y])
for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[x,y]].values
    hull = myConvexHull(bucket)
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    for simplex in hull.simplices:
        plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i])
plt.legend()
plt.show()
