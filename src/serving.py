"""Serving API for propensity model predictions."""

import argparse
import joblib
import pandas as pd
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global model variable
model = None
model_name = None


def load_best_model(models_dir: Path, metrics_path: Path):
    """Load the best model based on ROC AUC score."""
    global model, model_name
    
    # Read metrics to find best model
    metrics_df = pd.read_csv(metrics_path)
    best_row = metrics_df.loc[metrics_df['roc_auc'].idxmax()]
    model_name = best_row['model']
    
    # Load model
    model_path = models_dir / f"{model_name}.pkl"
    model = joblib.load(model_path)
    
    print(f"✓ Modelo cargado: {model_name}")
    print(f"  ROC AUC: {best_row['roc_auc']:.4f}")
    print(f"  Accuracy: {best_row['accuracy']:.4f}")
    
    return model


def validate_input(data: dict) -> tuple:
    """Validate input data format."""
    required_fields = ["Edad", "Ingreso", "Sexo"]  # Ejemplos mínimos
    
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Campos faltantes: {missing}"
    
    return True, None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    if model is None:
        return jsonify({"status": "error", "message": "Modelo no cargado"}), 500
    
    return jsonify({
        "status": "ok",
        "model": model_name,
        "version": "1.0.0"
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Predict propensity for a single customer."""
    try:
        # Get input data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Make prediction
        proba = model.predict_proba(df)[:, 1][0]
        prediction = int(proba > 0.5)
        
        # Determine segment
        if proba >= 0.8:
            segment = "Top 5% - Alta prioridad"
        elif proba >= 0.7:
            segment = "Top 10% - Media prioridad"
        elif proba >= 0.6:
            segment = "Top 20% - Baja prioridad"
        else:
            segment = "Fuera de target"
        
        return jsonify({
            "propensity_score": float(proba),
            "prediction": prediction,
            "segment": segment,
            "recommendation": get_recommendation(proba, data)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Predict propensity for multiple customers."""
    try:
        # Get input data
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Se esperaba una lista de clientes"}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Make predictions
        probas = model.predict_proba(df)[:, 1]
        predictions = (probas > 0.5).astype(int)
        
        # Build results
        results = []
        for i, (proba, pred) in enumerate(zip(probas, predictions)):
            results.append({
                "index": i,
                "propensity_score": float(proba),
                "prediction": int(pred),
                "segment": classify_segment(proba)
            })
        
        return jsonify({
            "count": len(results),
            "predictions": results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/model_info', methods=['GET'])
def model_info():
    """Get information about the loaded model."""
    if model is None:
        return jsonify({"error": "Modelo no cargado"}), 500
    
    return jsonify({
        "model_name": model_name,
        "model_type": str(type(model.named_steps['classifier']).__name__),
        "features": list(model.feature_names_in_) if hasattr(model, 'feature_names_in_') else "N/A"
    })


def classify_segment(proba: float) -> str:
    """Classify customer segment based on propensity score."""
    if proba >= 0.8:
        return "Top 5%"
    elif proba >= 0.7:
        return "Top 10%"
    elif proba >= 0.6:
        return "Top 20%"
    else:
        return "Low priority"


def get_recommendation(proba: float, data: dict) -> str:
    """Get business recommendation based on propensity and customer data."""
    if proba >= 0.8:
        return "Contacto telefónico personalizado con ejecutivo dedicado"
    elif proba >= 0.7:
        return "Email marketing con oferta especial + SMS"
    elif proba >= 0.6:
        return "Campania digital segmentada"
    else:
        return "Incluir en campanias masivas generales"


def main():
    parser = argparse.ArgumentParser(description="Serving API for propensity model")
    parser.add_argument(
        "--models-dir",
        type=str,
        default="models",
        help="Directory with trained models"
    )
    parser.add_argument(
        "--metrics-path",
        type=str,
        default="resources/metrics_summary.csv",
        help="Path to metrics summary CSV"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind"
    )
    args = parser.parse_args()
    
    # Load best model
    models_dir = Path(args.models_dir)
    metrics_path = Path(args.metrics_path)
    
    load_best_model(models_dir, metrics_path)
    
    # Start Flask app
    print(f"\n{'='*50}")
    print("🚀 API de Propensión iniciada")
    print(f"   http://{args.host}:{args.port}")
    print(f"{'='*50}\n")
    
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
