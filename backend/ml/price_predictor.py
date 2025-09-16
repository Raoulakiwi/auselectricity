import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import joblib
import logging

logger = logging.getLogger(__name__)

class PricePredictor:
    """
    Machine learning model for predicting electricity prices based on dam levels and historical data
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = None
        
    def prepare_features(self, electricity_data: pd.DataFrame, dam_data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for the prediction model
        """
        try:
            # Merge electricity and dam data on timestamp
            merged_data = pd.merge(
                electricity_data, 
                dam_data, 
                on='timestamp', 
                how='inner'
            )
            
            # Create time-based features
            merged_data['hour'] = merged_data['timestamp'].dt.hour
            merged_data['day_of_week'] = merged_data['timestamp'].dt.dayofweek
            merged_data['month'] = merged_data['timestamp'].dt.month
            merged_data['is_weekend'] = merged_data['day_of_week'].isin([5, 6]).astype(int)
            
            # Create peak hour indicator
            merged_data['is_peak_hour'] = (
                (merged_data['hour'] >= 6) & (merged_data['hour'] <= 9) |
                (merged_data['hour'] >= 17) & (merged_data['hour'] <= 20)
            ).astype(int)
            
            # Create seasonal indicators
            merged_data['is_summer'] = merged_data['month'].isin([12, 1, 2]).astype(int)
            merged_data['is_winter'] = merged_data['month'].isin([6, 7, 8]).astype(int)
            
            # Create dam level features
            merged_data['avg_dam_capacity'] = merged_data.groupby('timestamp')['capacity_percentage'].transform('mean')
            merged_data['max_dam_capacity'] = merged_data.groupby('timestamp')['capacity_percentage'].transform('max')
            merged_data['min_dam_capacity'] = merged_data.groupby('timestamp')['capacity_percentage'].transform('min')
            
            # Create lagged features (previous day's price)
            merged_data = merged_data.sort_values(['region', 'timestamp'])
            merged_data['price_lag_1'] = merged_data.groupby('region')['price'].shift(1)
            merged_data['price_lag_7'] = merged_data.groupby('region')['price'].shift(7)  # Weekly lag
            
            # Create rolling averages
            merged_data['price_ma_7'] = merged_data.groupby('region')['price'].rolling(7).mean().reset_index(0, drop=True)
            merged_data['price_ma_30'] = merged_data.groupby('region')['price'].rolling(30).mean().reset_index(0, drop=True)
            
            # Create demand/supply ratio
            merged_data['demand_supply_ratio'] = merged_data['demand'] / merged_data['supply']
            
            return merged_data
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return pd.DataFrame()
    
    def train(self, electricity_data: pd.DataFrame, dam_data: pd.DataFrame) -> Dict:
        """
        Train the price prediction model
        """
        try:
            # Prepare features
            features_df = self.prepare_features(electricity_data, dam_data)
            
            if features_df.empty:
                return {"error": "No data available for training"}
            
            # Define feature columns
            feature_columns = [
                'hour', 'day_of_week', 'month', 'is_weekend', 'is_peak_hour',
                'is_summer', 'is_winter', 'avg_dam_capacity', 'max_dam_capacity', 
                'min_dam_capacity', 'price_lag_1', 'price_lag_7', 'price_ma_7', 
                'price_ma_30', 'demand_supply_ratio', 'demand', 'supply'
            ]
            
            # Remove rows with NaN values
            features_df = features_df.dropna(subset=feature_columns + ['price'])
            
            if len(features_df) == 0:
                return {"error": "No valid data after cleaning"}
            
            # Prepare X and y
            X = features_df[feature_columns]
            y = features_df['price']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            # Get feature importance
            self.feature_importance = dict(zip(feature_columns, self.model.feature_importances_))
            
            self.is_trained = True
            
            return {
                "status": "success",
                "metrics": {
                    "mse": mse,
                    "rmse": rmse,
                    "r2_score": r2
                },
                "feature_importance": self.feature_importance,
                "training_samples": len(X_train),
                "test_samples": len(X_test)
            }
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return {"error": str(e)}
    
    def predict(self, features: Dict) -> Dict:
        """
        Make price predictions for given features
        """
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        try:
            # Convert features to DataFrame
            features_df = pd.DataFrame([features])
            
            # Ensure all required features are present
            required_features = [
                'hour', 'day_of_week', 'month', 'is_weekend', 'is_peak_hour',
                'is_summer', 'is_winter', 'avg_dam_capacity', 'max_dam_capacity', 
                'min_dam_capacity', 'price_lag_1', 'price_lag_7', 'price_ma_7', 
                'price_ma_30', 'demand_supply_ratio', 'demand', 'supply'
            ]
            
            # Fill missing features with default values
            for feature in required_features:
                if feature not in features_df.columns:
                    features_df[feature] = 0
            
            # Scale features
            features_scaled = self.scaler.transform(features_df[required_features])
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            
            # Calculate confidence based on feature similarity to training data
            confidence = self._calculate_confidence(features_df[required_features])
            
            return {
                "predicted_price": round(prediction, 2),
                "confidence": round(confidence, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": str(e)}
    
    def _calculate_confidence(self, features: pd.DataFrame) -> float:
        """
        Calculate prediction confidence based on feature values
        """
        try:
            # Simple confidence calculation based on feature ranges
            # In a real implementation, this would be more sophisticated
            
            confidence = 0.8  # Base confidence
            
            # Adjust confidence based on feature values
            if features['hour'].iloc[0] in [6, 7, 8, 9, 17, 18, 19, 20]:
                confidence += 0.1  # Higher confidence during peak hours
            
            if 0.3 <= features['avg_dam_capacity'].iloc[0] <= 0.9:
                confidence += 0.1  # Higher confidence for normal dam levels
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    def save_model(self, filepath: str):
        """Save the trained model"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, filepath)
            logger.info(f"Model saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def load_model(self, filepath: str):
        """Load a trained model"""
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_importance = model_data['feature_importance']
            self.is_trained = model_data['is_trained']
            logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")

# Utility functions for data preparation
def prepare_training_data(electricity_data: List[Dict], dam_data: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare training data from database records
    """
    try:
        # Convert to DataFrames
        electricity_df = pd.DataFrame(electricity_data)
        dam_df = pd.DataFrame(dam_data)
        
        # Convert timestamp columns
        electricity_df['timestamp'] = pd.to_datetime(electricity_df['timestamp'])
        dam_df['timestamp'] = pd.to_datetime(dam_df['timestamp'])
        
        return electricity_df, dam_df
        
    except Exception as e:
        logger.error(f"Error preparing training data: {e}")
        return pd.DataFrame(), pd.DataFrame()
