# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EH_sFCCnTH3K1ysuR1u2urGbXteB8R-E
"""

#from google.colab import drive
#drive.mount('/content/drive')

import pandas as pd

file_path = 'global_food_wastage_dataset.csv'
df = pd.read_csv(file_path)
df.head()

df.info()

df.shape

df.describe()

# Eksik değerleri tespit et
missing_values = df.isnull().sum()

# Eksik veri içeren sütunları filtreleyerek sadece eksik değerleri gösterelim
missing_values = missing_values[missing_values > 0]

# Sonucu daha düzenli görüntüleyelim
print("Eksik Değer Sayıları:\n")
print(missing_values)

import seaborn as sns
import matplotlib.pyplot as plt

category_waste = df.groupby("Food Category")["Total Waste (Tons)"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=category_waste.values, y=category_waste.index, palette="pastel")
plt.title("En Çok İsraf Edilen Gıda Kategorileri (Toplam Ton)")
plt.xlabel("Toplam İsraf (Ton)")
plt.ylabel("Gıda Kategorisi")
plt.tight_layout()
plt.show()

country_loss = df.groupby("Country")["Economic Loss (Million $)"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=country_loss.values, y=country_loss.index, palette="pastel")
plt.title("Ülkelere Göre Ortalama Ekonomik Kayıp (İlk 10)")
plt.xlabel("Ekonomik Kayıp (Milyon $)")
plt.ylabel("Ülke")
plt.tight_layout()
plt.show()

# Kişi başına en çok israf yapan ilk 10 ülke
top10_capita = df.groupby("Country")["Avg Waste per Capita (Kg)"].mean().sort_values(ascending=False).head(10).index

# Pivot table (Capita)
pivot_capita = df[df["Country"].isin(top10_capita)].pivot_table(
    index="Country",
    columns="Food Category",
    values="Avg Waste per Capita (Kg)",
    aggfunc="mean"
)

# Grafik
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_capita, cmap="BuPu", annot=True, fmt=".1f", linewidths=0.5)
plt.title("Ülke-Gıda Kategorisi Bazında Kişi Başına Ortalama Gıda İsrafı (Kg)")
plt.xlabel("Gıda Kategorisi")
plt.ylabel("Ülke")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["Household Waste (%)"], bins=30, kde=True, color="yellow")
plt.title("Hane Halkı İsraf Oranlarının Dağılımı")
plt.xlabel("Hane Halkı İsraf Oranı (%)")
plt.ylabel("Frekans")
plt.tight_layout()
plt.show()

#korelasyon matrisi
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Sayısal Değişkenler Arası Korelasyon")
plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="Food Category", hue="Year", palette="pastel")

plt.title("Gıda Kategorisine Göre Yıllık Veri Dağılımı", fontsize=14)
plt.xlabel("Gıda Kategorisi", fontsize=12)
plt.ylabel("Kayıt Sayısı", fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="Yıl")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

# Veri setini oku
df = pd.read_csv("/content/drive/MyDrive/veri seti/global_food_wastage_dataset.csv")

# Hedef değişkeni kontrol et
print("Hedef değişken (Economic Loss):")
print(df["Economic Loss (Million $)"].describe())

# Boş değer var mı kontrol et
print("\nBoş değer sayısı:")
print(df.isnull().sum())

# Label Encoding: Ülke ve gıda kategorisi
df_encoded = df.copy()
label_cols = ["Country", "Food Category"]
for col in label_cols:
    df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col])

# Girdi (X) ve hedef (y)
X = df_encoded.drop(columns=["Economic Loss (Million $)"])
y = df_encoded["Economic Loss (Million $)"]

# Eğitim/test ayrımı
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ölçekleme (bazı algoritmalar için gerekli)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model başarı skorlarını saklamak için sözlük
results = {}

# 1️⃣ Linear Regression
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
results["Linear Regression"] = r2_score(y_test, y_pred_lr)

# 2️⃣ Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
results["Random Forest"] = r2_score(y_test, y_pred_rf)

# 3️⃣ XGBoost
xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
results["XGBoost"] = r2_score(y_test, y_pred_xgb)

# 4️⃣ KNN
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)
results["KNN"] = r2_score(y_test, y_pred_knn)

# R2 skorlarını yazdır
print("Model Başarıları (R² Skoru):")
for model, score in results.items():
    print(f"{model}: {score:.4f}")

# Grafikle karşılaştır
plt.figure(figsize=(8,5))
sns.barplot(x=list(results.keys()), y=list(results.values()), palette="pastel")
plt.ylabel("R² Skoru")
plt.title("Modellere Göre Başarı Karşılaştırması")
plt.ylim(0, 1)
plt.grid(True)
plt.tight_layout()
plt.show()

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

# Veri setini oku
df = pd.read_csv("/content/drive/MyDrive/veri seti/global_food_wastage_dataset.csv")

# Label Encoding
df['Country'] = LabelEncoder().fit_transform(df['Country'])
df['Food Category'] = LabelEncoder().fit_transform(df['Food Category'])

# Girdi ve hedef
X = df.drop(columns=['Economic Loss (Million $)'])
y = df['Economic Loss (Million $)']

# Ölçekleme
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Eğitim - test ayrımı
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(random_state=42)
rf_param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt']
}

grid_rf = GridSearchCV(rf, rf_param_grid, cv=3, scoring='r2', n_jobs=-1, verbose=1)
grid_rf.fit(X_train, y_train)
print("RF Best Params:", grid_rf.best_params_)
print("RF Test R²:", grid_rf.best_estimator_.score(X_test, y_test))

from xgboost import XGBRegressor

xgb = XGBRegressor(random_state=42, objective='reg:squarederror')
xgb_param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [3, 6],
    'learning_rate': [0.05, 0.1],
    'subsample': [0.8, 1.0]
}

grid_xgb = GridSearchCV(xgb, xgb_param_grid, cv=3, scoring='r2', n_jobs=-1, verbose=1)
grid_xgb.fit(X_train, y_train)
print("XGB Best Params:", grid_xgb.best_params_)
print("XGB Test R²:", grid_xgb.best_estimator_.score(X_test, y_test))

from sklearn.neighbors import KNeighborsRegressor

knn = KNeighborsRegressor()
knn_param_grid = {
    'n_neighbors': [3, 5, 7, 9],
    'weights': ['uniform', 'distance'],
    'p': [1, 2]  # p=1 → Manhattan, p=2 → Euclidean
}

grid_knn = GridSearchCV(knn, knn_param_grid, cv=3, scoring='r2', n_jobs=-1, verbose=1)
grid_knn.fit(X_train, y_train)
print("KNN Best Params:", grid_knn.best_params_)
print("KNN Test R²:", grid_knn.best_estimator_.score(X_test, y_test))

from sklearn.linear_model import Ridge

ridge = Ridge()
ridge_param_grid = {
    'alpha': [0.01, 0.1, 1.0, 10.0]
}

grid_ridge = GridSearchCV(ridge, ridge_param_grid, cv=3, scoring='r2', n_jobs=-1)
grid_ridge.fit(X_train, y_train)
print("Ridge Best Params:", grid_ridge.best_params_)
print("Ridge Test R²:", grid_ridge.best_estimator_.score(X_test, y_test))

from sklearn.metrics import mean_absolute_error, mean_squared_error

def print_metrics(y_true, y_pred, model_name):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"{model_name}:\nR2: {r2:.4f} | RMSE: {rmse:.2f} | MAE: {mae:.2f}\n")

print_metrics(y_test, y_pred_lr, "Linear Regression")
print_metrics(y_test, y_pred_rf, "Random Forest")
print_metrics(y_test, y_pred_xgb, "XGBoost")
print_metrics(y_test, y_pred_knn, "KNN")

# Grafikle hata karşılaştırması
import matplotlib.pyplot as plt

models = ["Linear Regression", "Random Forest", "XGBoost", "KNN"]
rmse_values = [3336.50, 3501.70, 3539.21, 5022.63]
mae_values = [2512.92, 2614.13, 2623.69, 3885.23]

x = np.arange(len(models))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x - width/2, rmse_values, width, label='RMSE')
plt.bar(x + width/2, mae_values, width, label='MAE')

plt.ylabel('Hata Değeri')
plt.title('Modellere Göre Hata Karşılaştırması')
plt.xticks(x, models, rotation=15)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Linear Regression zaten lr olarak fit edilmiş
print_metrics(y_train, lr.predict(X_train_scaled), "Linear Regression - Train")

# GridSearch ile fit edilen en iyi Random Forest
print_metrics(y_train, grid_rf.best_estimator_.predict(X_train), "Random Forest - Train")

# XGBoost (GridSearch sonucu en iyi)
print_metrics(y_train, grid_xgb.best_estimator_.predict(X_train), "XGBoost - Train")

# KNN (GridSearch sonucu en iyi)
print_metrics(y_train, grid_knn.best_estimator_.predict(X_train_scaled), "KNN - Train")