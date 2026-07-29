from dotenv import load_dotenv
import requests
import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score

load_dotenv()
token = os.environ["HUD_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "https://www.huduser.gov/hudapi/public/fmr/listMetroAreas",
    headers=headers
)

print(response.status_code)
data = response.json()

# for area in data:
#     if("Dallas" in area["area_name"]):
#        print(area)

#use METRO19100M19100 cause that is dallas we now get all the zipcodes from that place

response2 = requests.get(
    "https://www.huduser.gov/hudapi/public/fmr/data/METRO19100M19100",
    headers = headers   
)

data_area = response2.json()


df = pd.read_json("dfw_rent_data.json")

df = df[df['zip_code'] != "MSA level"]

melted_df = df.melt(
    id_vars = ["zip_code"],
    value_vars = ["Efficiency", "One-Bedroom", "Two-Bedroom", "Three-Bedroom", "Four-Bedroom"],
    var_name = 'bedroom_type',
    value_name = 'rent'
)

bedroom_map = {
    "Efficiency" : 0,
    "One-Bedroom" : 1,
    "Three-Bedroom" : 2,
    "Four-Bedroom" : 3
}

melted_df['bedrooms'] = melted_df['bedroom_type'].map(bedroom_map)


#i need zipcode and bedroom type for x 
#i need rent for y

df_encoded = pd.get_dummies(melted_df, columns=["zip_code"])

X = df_encoded.drop(columns=['bedroom_type','rent'])
y = df_encoded['rent']


#this is just standard training
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state = 42)

print(X_train.shape)

print(X_test.shape)

rf_model = RandomForestRegressor(random_state = 42)

#model did the learning
rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

print(rf_predictions)

rf_mae = mean_absolute_error(rf_predictions, y_test)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_predictions))

print(f"Random Forest MAE: {rf_mae}")
print(f"Random Forest RMSE: {rf_rmse}")
rf_r2 = r2_score(y_test, rf_predictions)
print(f"Random Forest R²: {rf_r2}")

#get the new model
xgb_model = XGBRegressor(random_state=42)

#train the model
xgb_model.fit(X_train, y_train)

#get the predictions its able to make with the test data
xgb_predictions = xgb_model.predict(X_test)

xgb_mae = mean_absolute_error(y_test, xgb_predictions)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_predictions))
xgb_r2 = r2_score(y_test, xgb_predictions)

print(f"XGBoost MAE: {xgb_mae}")
print(f"XGBoost RMSE: {xgb_rmse}")
print(f"XGBoost R²: {xgb_r2}")

