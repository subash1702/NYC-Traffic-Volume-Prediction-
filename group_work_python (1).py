#!/usr/bin/env python
# coding: utf-8

# In[4]:


# === Step 1: Import Required Libraries ===
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set(style='whitegrid')

# === Step 2: Define Data Cleaning and Loading Function ===
def load_and_clean_data(traffic_path, events_path):
    traffic_df = pd.read_csv(traffic_path)
    events_df = pd.read_csv(events_path)

    # Convert timestamp
    traffic_df['timestamp'] = pd.to_datetime(dict(
        year=traffic_df['Yr'],
        month=traffic_df['M'],
        day=traffic_df['D'],
        hour=traffic_df['HH'],
        minute=traffic_df['MM']
    ), errors='coerce')

    traffic_df['event_day'] = traffic_df['timestamp'].dt.date
    traffic_df['hour_of_day'] = traffic_df['timestamp'].dt.hour
    traffic_df['day_of_week'] = traffic_df['timestamp'].dt.dayofweek
    traffic_df['is_weekend'] = traffic_df['day_of_week'] >= 5
    traffic_df['Boro'] = traffic_df['Boro'].str.strip().str.title()
    traffic_df.dropna(subset=['timestamp', 'Vol'], inplace=True)

    # Parse event datetime safely
    events_df['event_datetime'] = pd.to_datetime(events_df['Start Date/Time'], errors='coerce')
    events_df['event_day'] = events_df['event_datetime'].dt.date
    events_df['Event Borough'] = events_df['Event Borough'].str.strip().str.title()
    events_df.dropna(subset=['event_day', 'Event Borough'], inplace=True)

    # Sample for performance
    traffic_sample = traffic_df.sample(n=25000, random_state=42)
    events_sample = events_df.sample(n=2500, random_state=42)

    # Merge datasets
    merged_df = pd.merge(
        traffic_sample,
        events_sample,
        how='left',
        left_on=['event_day', 'Boro'],
        right_on=['event_day', 'Event Borough']
    )
    merged_df['is_event_time'] = ~merged_df['event_datetime'].isna()

    return merged_df

# === Step 3: Define EDA Plotting Function ===
def run_eda_plots(df):
    # Plot 1: Average Volume by Hour of Day
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=df.groupby('hour_of_day')['Vol'].mean().reset_index(),
        x='hour_of_day', y='Vol', marker='o'
    )
    plt.title('Average Traffic Volume by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Volume')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 2: Average Volume by Day of Week
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df.groupby('day_of_week')['Vol'].mean().reset_index(),
        x='day_of_week', y='Vol'
    )
    plt.title('Average Traffic Volume by Day of Week (0=Mon, 6=Sun)')
    plt.xlabel('Day of Week')
    plt.ylabel('Average Volume')
    plt.tight_layout()
    plt.show()

    # Plot 3: Event vs Non-Event Volume (Boxplot)
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='is_event_time', y='Vol', data=df)
    plt.title('Traffic Volume During Events vs Non-Events')
    plt.xlabel('Is Event Time (True/False)')
    plt.ylabel('Traffic Volume')
    plt.tight_layout()
    plt.show()

    # Plot 4: Total Volume by Borough
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df.groupby('Boro')['Vol'].sum().reset_index(),
        x='Boro', y='Vol'
    )
    plt.title('Total Traffic Volume by Borough')
    plt.xlabel('Borough')
    plt.ylabel('Total Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot 5: Heatmap of Day of Week vs Hour
    df['DateTime'] = pd.to_datetime(df['timestamp'])
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.day_name()

    heatmap_data = df.pivot_table(
        index='DayOfWeek', columns='Hour', values='Vol', aggfunc='mean'
    )
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(ordered_days)

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.5, linecolor='gray')
    plt.title('Average Traffic Volume by Hour and Day of Week')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.tight_layout()
    plt.show()



# In[14]:


# Provide your correct file paths
traffic_path = "C:/Users/hp/Downloads/Automated_Traffic_Volume_Counts.csv"
events_path = "C:/Users/hp/Downloads/NYC_Permitted_Event_Information_-_Historical.csv"

# Load and clean merged dataset
merged_df = load_and_clean_data(traffic_path, events_path)

# Generate all EDA plots
run_eda_plots(merged_df)



# In[1]:


# --- Import Libraries ---
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Seaborn style
sns.set(style='whitegrid')

# --- Define Function to Load and Clean Data ---
def load_and_clean_data(traffic_path, events_path):
    # Load datasets
    traffic_df = pd.read_csv(traffic_path)
    events_df = pd.read_csv(events_path)

    # Convert timestamp
    traffic_df['timestamp'] = pd.to_datetime(dict(
        year=traffic_df['Yr'],
        month=traffic_df['M'],
        day=traffic_df['D'],
        hour=traffic_df['HH'],
        minute=traffic_df['MM']
    ), errors='coerce')

    # Clean traffic data
    traffic_df['event_day'] = traffic_df['timestamp'].dt.date
    traffic_df['hour_of_day'] = traffic_df['timestamp'].dt.hour
    traffic_df['day_of_week'] = traffic_df['timestamp'].dt.dayofweek
    traffic_df['is_weekend'] = traffic_df['day_of_week'] >= 5
    traffic_df['Boro'] = traffic_df['Boro'].str.strip().str.title()
    traffic_df.dropna(subset=['timestamp', 'Vol'], inplace=True)

    # Clean event data
    events_df['event_datetime'] = pd.to_datetime(
        events_df['Start Date/Time'], errors='coerce'
    )
    events_df['event_day'] = events_df['event_datetime'].dt.date
    events_df['Event Borough'] = events_df['Event Borough'].str.strip().str.title()
    events_df.dropna(subset=['event_day', 'Event Borough'], inplace=True)

    # Sample for memory efficiency
    traffic_sample = traffic_df.sample(n=25000, random_state=42)
    events_sample = events_df.sample(n=2500, random_state=42)

    # Merge
    merged_df = pd.merge(
        traffic_sample,
        events_sample,
        how='left',
        left_on=['event_day', 'Boro'],
        right_on=['event_day', 'Event Borough']
    )
    merged_df['is_event_time'] = ~merged_df['event_datetime'].isna()
    return merged_df

# --- Define EDA Plot Function ---
def run_eda_plots(merged_df):
    # 1. Average traffic volume by hour
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=merged_df.groupby('hour_of_day')['Vol'].mean().reset_index(),
        x='hour_of_day', y='Vol', marker='o'
    )
    plt.title('Average Traffic Volume by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Volume')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Average traffic volume by day of week
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=merged_df.groupby('day_of_week')['Vol'].mean().reset_index(),
        x='day_of_week', y='Vol'
    )
    plt.title('Average Volume by Day of Week (0 = Mon, 6 = Sun)')
    plt.xlabel('Day of Week')
    plt.ylabel('Average Volume')
    plt.tight_layout()
    plt.show()

    # 3. Boxplot: Event vs Non-event
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='is_event_time', y='Vol', data=merged_df)
    plt.title('Traffic Volume: Event vs Non-Event Times')
    plt.xlabel('Is Event Time')
    plt.ylabel('Traffic Volume')
    plt.tight_layout()
    plt.show()

    # 4. Barplot: Total volume by borough
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=merged_df.groupby('Boro')['Vol'].sum().reset_index(),
        x='Boro', y='Vol'
    )
    plt.title('Total Volume by Borough')
    plt.xlabel('Borough')
    plt.ylabel('Total Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 5. Heatmap: Hour vs Day of Week
    merged_df['day_name'] = merged_df['timestamp'].dt.day_name()
    pivot = merged_df.pivot_table(index='day_name', columns='hour_of_day', values='Vol', aggfunc='mean')
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = pivot.reindex(ordered_days)

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap='YlOrRd', linewidths=0.5)
    plt.title('Heatmap: Avg Volume by Hour & Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.tight_layout()
    plt.show()

# --- Run Everything ---
traffic_path = "C:/Users/hp/Downloads/Automated_Traffic_Volume_Counts.csv"
events_path = "C:/Users/hp/Downloads/NYC_Permitted_Event_Information_-_Historical.csv"

merged_df = load_and_clean_data(traffic_path, events_path)
run_eda_plots(merged_df)


# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, roc_curve, roc_auc_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error

sns.set(style='whitegrid')

# === 1. Load & Clean Data ===
def load_and_clean_data(traffic_path, event_path):
    traffic_df = pd.read_csv(traffic_path)
    events_df = pd.read_csv(event_path)

    traffic_df['timestamp'] = pd.to_datetime(dict(
        year=traffic_df['Yr'],
        month=traffic_df['M'],
        day=traffic_df['D'],
        hour=traffic_df['HH'],
        minute=traffic_df['MM']
    ), errors='coerce')

    traffic_df['event_day'] = traffic_df['timestamp'].dt.date
    traffic_df['hour_of_day'] = traffic_df['timestamp'].dt.hour
    traffic_df['day_of_week'] = traffic_df['timestamp'].dt.dayofweek
    traffic_df['is_weekend'] = traffic_df['day_of_week'] >= 5
    traffic_df['Boro'] = traffic_df['Boro'].str.strip().str.title()
    traffic_df.dropna(subset=['timestamp', 'Vol'], inplace=True)

    events_df['event_datetime'] = pd.to_datetime(events_df['Start Date/Time'], errors='coerce')
    events_df['event_day'] = events_df['event_datetime'].dt.date
    events_df['Event Borough'] = events_df['Event Borough'].str.strip().str.title()
    events_df.dropna(subset=['event_day', 'Event Borough'], inplace=True)

    return traffic_df, events_df

# === 2. Merge Data ===
def merge_data(traffic_df, events_df):
    traffic_sample = traffic_df.sample(n=25000, random_state=42)
    events_sample = events_df.sample(n=2500, random_state=42)
    merged_df = pd.merge(
        traffic_sample,
        events_sample,
        how='left',
        left_on=['event_day', 'Boro'],
        right_on=['event_day', 'Event Borough']
    )
    merged_df['is_event_time'] = ~merged_df['event_datetime'].isna()
    merged_df['is_event_day'] = ~merged_df['Event Borough'].isna()
    merged_df['Boro_code'] = merged_df['Boro'].astype('category').cat.codes
    return merged_df

# === 3. GBR Model for Predicting Traffic Volume ===
def model_gbr(merged_df):
    df = merged_df[['Vol', 'is_event_time', 'hour_of_day', 'day_of_week']].dropna()
    X = df[['is_event_time', 'hour_of_day', 'day_of_week']]
    y = df['Vol']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("R2 Score:", r2_score(y_test, y_pred))
    print("MSE:", mean_squared_error(y_test, y_pred))

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.3)
    plt.title(f"GBR Prediction: R² = {r2_score(y_test, y_pred):.2f}")
    plt.xlabel("Actual Volume")
    plt.ylabel("Predicted Volume")
    plt.tight_layout()
    plt.show()

# === 4. Heatmap by Street and Direction ===
def volume_heatmap(merged_df):
    heatmap_df = merged_df.groupby(['street', 'Direction'])['Vol'].sum().unstack().fillna(0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_df, cmap='coolwarm')
    plt.title("Traffic Volume by Street and Direction")
    plt.xlabel("Direction")
    plt.ylabel("Street")
    plt.tight_layout()
    plt.show()

# === 5. Classification Models for Weekday/Weekend ===
def model_classifiers(merged_df):
    X = merged_df[['Vol', 'hour_of_day', 'Boro_code']].dropna()
    y = merged_df['is_weekend'].loc[X.index]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        'Logistic Regression': LogisticRegression(),
        'Random Forest': RandomForestClassifier(random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    }

    for name, model in models.items():
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_probs = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_probs = model.predict_proba(X_test)[:, 1]

        print(f"\n=== {name} Classification Report ===")
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        ConfusionMatrixDisplay(cm, display_labels=['Weekday', 'Weekend']).plot(cmap='Blues')
        plt.title(f"{name} - Confusion Matrix")
        plt.grid(False)
        plt.show()

        fpr, tpr, _ = roc_curve(y_test, y_probs)
        auc = roc_auc_score(y_test, y_probs)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.2f})")

    plt.plot([0, 1], [0, 1], 'k--')
    plt.title("ROC Curve: Weekend vs Weekday")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.show()


