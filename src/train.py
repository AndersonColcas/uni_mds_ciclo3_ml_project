"""Entrenar modelos de propensión para la adopción de depósitos a plazo fijo."""

import argparse
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


def load_silver_data(input_path: Path) -> pd.DataFrame:
    """Cargar dataset silver."""
    print(f"Cargando datos desde: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Datos cargados: {df.shape}")
    return df


def prepare_features_target(df: pd.DataFrame, target_col: str = "T_Plazo"):
    """Separar características y objetivo, identificar tipos de columnas."""
    # Drop columns
    cols_to_drop = [target_col, "CodCli", "CrossSell"]
    cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    
    X = df.drop(columns=cols_to_drop)
    y = df[target_col]
    
    # Identify categorical and numeric columns
    cat_cols = X.select_dtypes(include="object").columns.tolist()
    num_cols = X.select_dtypes(exclude="object").columns.tolist()
    
    print(f"Features: {X.shape[1]} ({len(cat_cols)} categoricas, {len(num_cols)} numericas)")
    print(f"Target distribucion:\n{y.value_counts()}")
    
    return X, y, cat_cols, num_cols


def build_preprocessor(cat_cols, num_cols):
    """Construir pipeline de preprocesamiento."""
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])
    
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, num_cols),
        ("cat", categorical_transformer, cat_cols)
    ])
    
    return preprocessor


def train_models(X_train, y_train, preprocessor):
    """Entrenar todos los modelos."""
    models = {
        "logistic_regression": Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=500, random_state=42))
        ]),
        "decision_tree": Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", DecisionTreeClassifier(max_depth=5, random_state=42))
        ]),
        "svm": Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", SVC(kernel="rbf", probability=True, random_state=42))
        ])
    }
    
    print("\n=== Entrenando modelos ===")
    for name, model in models.items():
        print(f"Entrenando {name}...")
        model.fit(X_train, y_train)
        print(f"   {name} entrenado")
    
    return models


def evaluate_models(models, X_test, y_test, output_dir: Path):
    """Evaluar todos los modelos y guardar métricas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    print("\n=== Evaluación de Modelos ===")
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        
        print(f"\n{name.upper()}:")
        print(f"  Accuracy: {acc:.4f}")
        print(f"  ROC AUC: {auc:.4f}")
        print(f"  Classification Report:\n{classification_report(y_test, y_pred)}")
        
        results.append({"model": name, "accuracy": acc, "roc_auc": auc})
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        fig, ax = plt.subplots(figsize=(6, 5))
        disp.plot(ax=ax, cmap="Blues")
        plt.title(f"Matriz de Confusión - {name}")
        plt.tight_layout()
        plt.savefig(output_dir / f"confusion_matrix_{name}.png", dpi=100)
        plt.close()
    
    # Save metrics summary
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_dir.parent / "metrics_summary.csv", index=False)
    print(f"\n Métricas guardadas en {output_dir.parent / 'metrics_summary.csv'}")
    
    return results_df


def plot_feature_importance(model, output_dir: Path):
    """Graficar la importancia de las características para modelos basados en árboles."""
    if "decision_tree" not in str(type(model)):
        return
    
    importances = model.named_steps["classifier"].feature_importances_
    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    
    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(10, 6))
    feat_imp.plot(kind="barh")
    plt.title("Top 15 Variables Importantes - Árbol de Decisión")
    plt.xlabel("Importancia")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_dir / "feature_importance.png", dpi=100)
    plt.close()
    print(f" Feature importance guardado en {output_dir / 'feature_importance.png'}")


def calculate_lift(model, X_test, y_test, output_dir: Path, percents=[0.05, 0.1, 0.2]):
    """Calcular y graficar la tabla de lift."""
    y_scores = model.predict_proba(X_test)[:, 1]
    results = pd.DataFrame({"y_true": y_test, "y_score": y_scores})
    results = results.sort_values("y_score", ascending=False).reset_index(drop=True)
    
    total_positives = results["y_true"].sum()
    lifts = {}
    
    for p in percents:
        n = int(len(results) * p)
        captured = results.iloc[:n]["y_true"].sum()
        baseline = total_positives / len(results)
        capture_rate = captured / n if n > 0 else 0
        lift = capture_rate / baseline if baseline > 0 else 0
        
        lifts[f"Top {int(p*100)}%"] = {
            "Capturados": int(captured),
            "Rate": f"{capture_rate:.2%}",
            "Lift": f"{lift:.2f}x"
        }
    
    lift_df = pd.DataFrame(lifts).T
    print(f"\n=== Análisis de Lift ===")
    print(lift_df)
    
    lift_df.to_csv(output_dir.parent / "lift_analysis.csv")
    print(f"Análisis de lift guardado en {output_dir.parent / 'lift_analysis.csv'}")
    
    return lift_df


def save_models(models, output_dir: Path):
    """Guardar modelos entrenados."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name, model in models.items():
        model_path = output_dir / f"{name}.pkl"
        joblib.dump(model, model_path)
        print(f" Modelo guardado: {model_path}")


def main():
    parser = argparse.ArgumentParser(description="Entrenar modelos de propensión")
    parser.add_argument(
        "--input",
        type=str,
        default="data/training/propension_silver.csv",
        help="Ruta del dataset silver"
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        default="models",
        help="Directorio de salida para los modelos entrenados"
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        default="resources/images",
        help="Directorio de salida para las visualizaciones"
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.3,
        help="Proporción del conjunto de prueba"
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Estado aleatorio para reproducibilidad"
    )
    args = parser.parse_args()
    
    # Paths
    input_path = Path(args.input)
    models_dir = Path(args.models_dir)
    images_dir = Path(args.images_dir)
    
    # Load data
    df = load_silver_data(input_path)
    
    # Prepare features and target
    X, y, cat_cols, num_cols = prepare_features_target(df)
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )
    print(f"\nConjunto de entrenamiento: {X_train.shape}, Conjunto de prueba: {X_test.shape}")
    
    # Build preprocessor
    preprocessor = build_preprocessor(cat_cols, num_cols)
    
    # Train models
    models = train_models(X_train, y_train, preprocessor)
    
    # Evaluate models
    evaluate_models(models, X_test, y_test, images_dir)
    
    # Feature importance (for decision tree)
    plot_feature_importance(models["decision_tree"], images_dir)
    
    # Lift analysis (using logistic regression)
    calculate_lift(models["logistic_regression"], X_test, y_test, images_dir)
    
    # Save models
    save_models(models, models_dir)
    
    print(f"\n{'='*50}")
    print(" Entrenamiento completado exitosamente")
    print(f"  Modelos guardados en: {models_dir}")
    print(f"  Visualizaciones en: {images_dir}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
