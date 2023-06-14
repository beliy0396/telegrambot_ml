import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

data = pd.read_csv('apartments.csv')
df = data[['price', 'total_area', 'hot_water', 'floor_max', 'floor', 'extra_area_type_name', 'rooms_count']]
df = df.dropna()

df['extra_area_type_name']=df['extra_area_type_name'].map({'loggia':1,'balcony':0})
df['hot_water']=df['hot_water'].map({'Yes':1,'No':0})



X_train, X_test, y_train, y_test = train_test_split(df[['total_area', 'hot_water', 'floor_max', 'floor', 'extra_area_type_name', 'rooms_count']], df[['price']], test_size=0.2, random_state=42)

model = LinearRegression()
models = DecisionTreeRegressor(random_state=42)
modelss = RandomForestRegressor(random_state=42)

model.fit(X_train, y_train)
models.fit(X_train, y_train)
modelss.fit(X_train, y_train.values.ravel())


y_pred_model = model.predict(X_test)
y_pred_models = models.predict(X_test)
y_pred_modelss = modelss.predict(X_test)

mse_model = mean_squared_error(y_test, y_pred_model)
mse_models = mean_squared_error(y_test, y_pred_models)
mse_modelss = mean_squared_error(y_test, y_pred_modelss)

print('Линейная регрессия MSE: ', mse_model)
print('Дерево решений MSE: ', mse_models)
print('Случайный лес MSE: ', mse_modelss)

if mse_model < mse_models and mse_model < mse_modelss:
    print('Линейная регрессия')
elif mse_models < mse_modelss:
    print('Дерево решений')
else:
    print('Случайный лес')


joblib.dump(model, 'result_model.joblib')