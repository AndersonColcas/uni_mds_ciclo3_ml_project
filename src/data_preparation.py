"""Prepare los datos sin procesar en un conjunto de datos Silver para el entrenamiento."""

import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def load_raw_data(input_path: Path) -> pd.DataFrame:
    """Carga archivo raw (.sav, .xlsx, .csv)."""
    if input_path.is_file():
        file_path = input_path
    else:
        # Busca el primer archivo soportado en la carpeta
        files = list(input_path.glob("*.sav")) + list(input_path.glob("*.xlsx")) + list(input_path.glob("*.csv"))
        if not files:
            raise FileNotFoundError(f"No se encontró archivo en {input_path}")
        file_path = files[0]
    
    print(f"Cargando: {file_path}")
    
    if file_path.suffix.lower() == ".sav":
        return pd.read_spss(file_path)
    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    else:
        return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza básica y mapeo de categorías."""
    df = df.copy()
    
    # Limpiar nombres de columnas
    df.columns = [col.strip() for col in df.columns]

    # Dropear columnas sensibles o irrelevantes 
    cols_to_drop = ["CodCli", "CrossSell"]  
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

    return df


def main():
    parser = argparse.ArgumentParser(description="Crear capa silver para training")
    parser.add_argument("--input", type=str, default="data/raw", help="Carpeta o archivo raw")
    parser.add_argument("--output", type=str, default="data/training/propension_silver.csv", help="Archivo CSV de salida")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    # Cargar, limpiar y transformar
    df = load_raw_data(input_path)
    print(f"Registros cargados: {len(df)}")
    
    df = clean_data(df)
    
    # Guardar como CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f" Silver dataset guardado en: {output_path}")
    print(f"  Shape: {df.shape}")


if __name__ == "__main__":
    main()
