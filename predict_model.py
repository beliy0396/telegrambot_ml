import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split #pip install scikit-learn

data = pd.read_csv('apartments.csv')

df = data[['price', 'total_area', 'hot_water', 'floor_max', 'floor', 'extra_area_type_name', 'rooms_count']]
df = df.dropna()

df['extra_area_type_name']=df['extra_area_type_name'].map({'loggia':1,'balcony':0})
df['hot_water']=df['hot_water'].map({'Yes':1,'No':0})

X_train, X_test, y_train, y_test = train_test_split(df[['total_area', 'hot_water', 'floor_max', 'floor', 'extra_area_type_name', 'rooms_count']], df[['price']], test_size=0.2)

model = LinearRegression()
model.fit(X_train.values, y_train)