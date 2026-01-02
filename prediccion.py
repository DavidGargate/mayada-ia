import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

data = {
    "demanda": [10, 20, 30, 40, 50],
    "calidad": [3, 4, 5, 6, 7],
    "precio": [100, 150, 200, 260, 320]
}

df = pd.DataFrame(data)

X = df[["demanda", "calidad"]]
y = df["precio"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print("Error MAE:", mean_absolute_error(y_test, pred))

nuevo = [[45, 6]]
print("Precio recomendado:", model.predict(nuevo)[0])
