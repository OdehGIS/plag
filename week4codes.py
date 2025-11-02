# =============================================================================
# WEEK 4: MODEL COMPARISON - RANDOM FOREST vs XGBOOST
# =============================================================================

print("WEEK 4: Comparing Multiple Models for SSH Attack Prediction")
print("=" * 70)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import warnings
import time
from tqdm import tqdm

warnings.filterwarnings("ignore")

# =============================================================================
# STEP 1: Load and prepare the enhanced dataset from Week 2-3
# =============================================================================

print("\n1. Loading and preparing Week 2-3 enhanced dataset...")

# Use the enhanced dataset from Week 3 that includes behavioral features
try:
    # Load the cleaned and enhanced data
    df_enhanced = pd.read_csv('ids_week2_parsed_cleaned.csv')
    final_features = pd.read_csv('ids_week2_features_scaled_by_ip.csv')
    
    # Recreate the enhanced dataset structure from Week 3
    df_enhanced['timestamp_parsed'] = pd.to_datetime(df_enhanced['timestamp_parsed'])
    df_sorted = df_enhanced.sort_values('timestamp_parsed').reset_index(drop=True)
    
    # Encode IP addresses for ML (same as Week 3)
    le_ip = LabelEncoder()
    df_sorted['src_ip_encoded'] = le_ip.fit_transform(df_sorted['src_ip'])
    
    # Create target: predict next IP that will appear
    df_sorted['next_ip_encoded'] = df_sorted['src_ip_encoded'].shift(-1)
    df_sorted = df_sorted.dropna(subset=['next_ip_encoded'])
    df_sorted['next_ip_encoded'] = df_sorted['next_ip_encoded'].astype(int)
    
    # Merge with Week 2 behavioral features
    df_enhanced_final = pd.merge(df_sorted, final_features, left_on='src_ip', right_on='ip', how='left')
    
    # Define features (temporal + behavioral - same as Week 3)
    df_enhanced_final['hour'] = df_enhanced_final['timestamp_parsed'].dt.hour
    df_enhanced_final['minute'] = df_enhanced_final['timestamp_parsed'].dt.minute
    
    basic_features = ['hour', 'minute', 'src_ip_encoded']
    behavioral_features = [col for col in final_features.columns if col.endswith('_scaled') and col != 'ip']
    all_features = basic_features + behavioral_features
    
    X = df_enhanced_final[all_features].fillna(0)
    y = df_enhanced_final['next_ip_encoded']
    
    print(f"   ✓ Dataset prepared: {len(X)} samples, {len(all_features)} features")
    print(f"   ✓ Target classes: {len(np.unique(y))} unique IP addresses")
    
except Exception as e:
    print(f"   ✗ Error loading saved files: {e}")
    print("   Creating enhanced dataset from Week 3 structure...")
    
    # Fallback: Recreate the Week 3 dataset structure
    df_sorted = df.sort_values('timestamp_parsed').reset_index(drop=True)
    
    # Encode IP addresses for ML
    le_ip = LabelEncoder()
    df_sorted['src_ip_encoded'] = le_ip.fit_transform(df_sorted['src_ip'])
    
    # Create target: predict next IP that will appear
    df_sorted['next_ip_encoded'] = df_sorted['src_ip_encoded'].shift(-1)
    df_sorted = df_sorted.dropna(subset=['next_ip_encoded'])
    df_sorted['next_ip_encoded'] = df_sorted['next_ip_encoded'].astype(int)
    
    # Create basic features (simplified version)
    df_sorted['hour'] = df_sorted['timestamp_parsed'].dt.hour
    df_sorted['minute'] = df_sorted['timestamp_parsed'].dt.minute
    
    # Use event-based features
    event_mapping = {
        'cowrie.session.connect': 1, 'cowrie.session.closed': 0,
        'cowrie.login.success': 2, 'cowrie.login.failed': 3,
        'cowrie.command.input': 4, 'cowrie.client.version': 5
    }
    df_sorted['event_encoded'] = df_sorted['eventid'].map(lambda x: event_mapping.get(x, 0))
    
    all_features = ['hour', 'minute', 'src_ip_encoded', 'event_encoded']
    X = df_sorted[all_features].fillna(0)
    y = df_sorted['next_ip_encoded']
    
    print(f"   ✓ Fallback dataset created: {len(X)} samples, {len(all_features)} features")

# =============================================================================
# STEP 2: Data preprocessing
# =============================================================================

print("\n2. Preprocessing data for model comparison...")

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"   ✓ Training set: {X_train_scaled.shape[0]} samples")
print(f"   ✓ Testing set: {X_test_scaled.shape[0]} samples")
print(f"   ✓ Feature dimension: {X_train_scaled.shape[1]} features")

# =============================================================================
# STEP 3: Define models for comparison
# =============================================================================

print("\n3. Initializing models for comparison...")

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100, 
        random_state=42, 
        class_weight='balanced'
    ),
    "XGBoost": XGBClassifier(
        n_estimators=100,
        random_state=42,
        eval_metric='mlogloss',
        use_label_encoder=False
    )
}

print("   ✓ Models initialized: Random Forest, XGBoost")

# =============================================================================
# STEP 4: Model training and evaluation with progress tracking
# =============================================================================

print("\n4. Training and evaluating models...")

results = {}
training_times = {}

for model_name, model in tqdm(models.items(), desc="Evaluating models"):
    start_time = time.time()
    
    # Cross-validation scores
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
    
    # Train on full training set
    model.fit(X_train_scaled, y_train)
    
    # Predict on test set
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    test_accuracy = accuracy_score(y_test, y_pred)
    
    end_time = time.time()
    training_time = end_time - start_time
    
    results[model_name] = {
        'cv_mean_accuracy': cv_scores.mean(),
        'cv_std_accuracy': cv_scores.std(),
        'test_accuracy': test_accuracy,
        'training_time': training_time,
        'model': model
    }
    
    training_times[model_name] = training_time

# =============================================================================
# STEP 5: Results comparison and analysis
# =============================================================================

print("\n" + "=" * 70)
print("WEEK 4 MODEL COMPARISON RESULTS")
print("=" * 70)

# Display results
print("\nMODEL PERFORMANCE COMPARISON:")
print("-" * 50)

for model_name, result in results.items():
    print(f"\n{model_name}:")
    print(f"  Cross-validation Accuracy: {result['cv_mean_accuracy']:.4f} (±{result['cv_std_accuracy']:.4f})")
    print(f"  Test Set Accuracy: {result['test_accuracy']:.4f}")
    print(f"  Training Time: {result['training_time']:.2f} seconds")

# Determine best model
best_model_name = max(results.keys(), key=lambda x: results[x]['test_accuracy'])
best_result = results[best_model_name]

print("\n" + "=" * 50)
print(f"BEST PERFORMING MODEL: {best_model_name}")
print(f"Test Accuracy: {best_result['test_accuracy']:.4f}")
print(f"Cross-validation Accuracy: {best_result['cv_mean_accuracy']:.4f}")
print("=" * 50)

# =============================================================================
# STEP 6: Feature importance analysis
# =============================================================================

print("\nFEATURE IMPORTANCE ANALYSIS:")
print("-" * 30)

# Get feature importance from both models
feature_importance_df = pd.DataFrame({
    'feature': all_features,
    'RandomForest_importance': results['Random Forest']['model'].feature_importances_,
    'XGBoost_importance': results['XGBoost']['model'].feature_importances_
})

# Display top features for each model
print("\nTop 5 Features - Random Forest:")
rf_top = feature_importance_df.nlargest(5, 'RandomForest_importance')[['feature', 'RandomForest_importance']]
for _, row in rf_top.iterrows():
    print(f"  {row['feature']}: {row['RandomForest_importance']:.4f}")

print("\nTop 5 Features - XGBoost:")
xgb_top = feature_importance_df.nlargest(5, 'XGBoost_importance')[['feature', 'XGBoost_importance']]
for _, row in xgb_top.iterrows():
    print(f"  {row['XGBoost_importance']:.4f}")

# =============================================================================
# STEP 7: Make prediction with best model (consistent with Week 3)
# =============================================================================

print("\n" + "=" * 70)
print("PREDICTION WITH BEST MODEL")
print("=" * 70)

# Use best model to make prediction (same format as Week 3)
best_model = results[best_model_name]['model']

# Predict on most recent event (same logic as Week 3)
if 'df_enhanced_final' in locals():
    recent_data = df_enhanced_final.iloc[-1]
    sample_features = np.array([recent_data[all_features].fillna(0).values])
    sample_features_scaled = scaler.transform(sample_features)
    
    predicted_ip_encoded = best_model.predict(sample_features_scaled)[0]
    probabilities = best_model.predict_proba(sample_features_scaled)[0]
    confidence = probabilities[predicted_ip_encoded]
    
    # Get predicted IP
    predicted_ip = le_ip.inverse_transform([predicted_ip_encoded])[0]
    
    print(f"PREDICTED NEXT ATTACKING IP: {predicted_ip}")
    print(f"PREDICTION CONFIDENCE: {confidence:.2%}")
    print(f"USING BEST MODEL: {best_model_name}")

# =============================================================================
# STEP 8: Save comparison results
# =============================================================================

print("\n8. Saving comparison results...")

# Create results summary
comparison_summary = {
    'best_model': best_model_name,
    'best_test_accuracy': best_result['test_accuracy'],
    'best_cv_accuracy': best_result['cv_mean_accuracy'],
    'total_training_time': sum(training_times.values()),
    'models_tested': list(models.keys()),
    'dataset_size': len(X),
    'feature_count': len(all_features),
    'unique_targets': len(np.unique(y))
}

# Save to DataFrame
results_df = pd.DataFrame([comparison_summary])
results_df.to_csv('week4_model_comparison_results.csv', index=False)

# Save detailed results
detailed_results = []
for model_name, result in results.items():
    detailed_results.append({
        'model': model_name,
        'test_accuracy': result['test_accuracy'],
        'cv_accuracy_mean': result['cv_mean_accuracy'],
        'cv_accuracy_std': result['cv_std_accuracy'],
        'training_time': result['training_time']
    })

detailed_df = pd.DataFrame(detailed_results)
detailed_df.to_csv('week4_detailed_model_results.csv', index=False)

print("   ✓ Results saved to 'week4_model_comparison_results.csv'")
print("   ✓ Detailed results saved to 'week4_detailed_model_results.csv'")

print("\n" + "=" * 70)
print("WEEK 4 MODEL COMPARISON COMPLETED SUCCESSFULLY")
print("=" * 70)
