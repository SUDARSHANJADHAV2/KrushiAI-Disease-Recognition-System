"""
Create a minimal dummy model for testing the disease recognition system.
This creates a model that can classify common plant diseases.
"""
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import joblib

# Common plant diseases based on the README
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___healthy',
]

def create_minimal_model():
    """Create a minimal trained model for testing."""
    print("Creating minimal model with common plant disease classes...")
    
    # Create synthetic training data (24 features from color histogram)
    n_samples_per_class = 20
    n_features = 24  # 8 bins * 3 channels
    
    X_synthetic = []
    y_synthetic = []
    
    for class_name in DISEASE_CLASSES:
        # Generate random features for this class
        # Add some class-specific patterns
        class_seed = hash(class_name) % 10000
        np.random.seed(class_seed)
        
        for _ in range(n_samples_per_class):
            # Random feature vector normalized
            features = np.random.rand(n_features).astype(np.float32)
            features = features / (np.linalg.norm(features) + 1e-8)
            X_synthetic.append(features)
            y_synthetic.append(class_name)
    
    X = np.array(X_synthetic)
    
    # Create label encoder
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_synthetic)
    
    # Create pipeline with classifier
    clf = RandomForestClassifier(
        n_estimators=50,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', clf),
    ])
    
    print(f"Training model on {len(X)} synthetic samples across {len(DISEASE_CLASSES)} classes...")
    pipeline.fit(X, y)
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'model.joblib')
    
    model_data = {
        'pipeline': pipeline,
        'label_encoder': label_encoder,
    }
    
    joblib.dump(model_data, model_path)
    print(f"✓ Model saved to: {model_path}")
    print(f"✓ Classes: {list(label_encoder.classes_)}")
    print("\nModel is ready for testing!")
    return model_path

if __name__ == '__main__':
    create_minimal_model()
