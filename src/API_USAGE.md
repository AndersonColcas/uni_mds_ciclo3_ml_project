# API de Predicción de Propensión

Servicio REST para predicción de propensión a contratar Depósitos a Plazo.

## Instalación

```bash
pip install -r requirements.txt
```

## Iniciar el servidor

```bash
python src/serving.py
```

El servidor estará disponible en `http://localhost:5000`

## Endpoints disponibles

### 1. Health Check

**GET** `/health`

Verifica el estado del servicio y modelo cargado.

```bash
curl http://localhost:5000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "model": "logistic_regression",
  "version": "1.0.0"
}
```

---

### 2. Predicción individual

**POST** `/predict`

Predice la propensión de un cliente individual.

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Edad": 45,
    "Ingreso": 5000,
    "Sexo": "M",
    "EstCiv": "Casado",
    "TVidaAño": 8,
    "T_TC": 1,
    "T_Micro": 0,
    "ZONA": "ZONA CENTRO",
    "Region": "LIMA"
  }'
```

**Respuesta:**
```json
{
  "propensity_score": 0.8234,
  "prediction": 1,
  "segment": "Top 5% - Alta prioridad",
  "recommendation": "Contacto telefónico personalizado con ejecutivo dedicado"
}
```

---

### 3. Predicción en lote

**POST** `/predict_batch`

Predice la propensión de múltiples clientes.

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/predict_batch \
  -H "Content-Type: application/json" \
  -d '[
    {
      "Edad": 45,
      "Ingreso": 5000,
      "Sexo": "M",
      "EstCiv": "Casado",
      "TVidaAño": 8,
      "T_TC": 1
    },
    {
      "Edad": 32,
      "Ingreso": 2500,
      "Sexo": "F",
      "EstCiv": "Soltero",
      "TVidaAño": 3,
      "T_TC": 0
    }
  ]'
```

**Respuesta:**
```json
{
  "count": 2,
  "predictions": [
    {
      "index": 0,
      "propensity_score": 0.8234,
      "prediction": 1,
      "segment": "Top 5%"
    },
    {
      "index": 1,
      "propensity_score": 0.3421,
      "prediction": 0,
      "segment": "Low priority"
    }
  ]
}
```

---

### 4. Información del modelo

**GET** `/model_info`

Obtiene información sobre el modelo cargado.

```bash
curl http://localhost:5000/model_info
```

**Respuesta:**
```json
{
  "model_name": "logistic_regression",
  "model_type": "LogisticRegression",
  "features": ["Edad", "Ingreso", "Sexo", ...]
}
```

---

## Segmentación de clientes

| Propensity Score | Segmento | Recomendación |
|------------------|----------|---------------|
| ≥ 0.80 | Top 5% | Contacto telefónico personalizado |
| ≥ 0.70 | Top 10% | Email marketing + SMS |
| ≥ 0.60 | Top 20% | Campaña digital segmentada |
| < 0.60 | Low priority | Campañas masivas generales |

---

## Ejemplo de integración Python

```python
import requests
import json

# URL del API
API_URL = "http://localhost:5000"

# Datos del cliente
cliente = {
    "Edad": 45,
    "Ingreso": 5000,
    "Sexo": "M",
    "EstCiv": "Casado",
    "TVidaAño": 8,
    "T_TC": 1,
    "T_Micro": 0
}

# Hacer predicción
response = requests.post(f"{API_URL}/predict", json=cliente)
resultado = response.json()

print(f"Score de propensión: {resultado['propensity_score']:.2%}")
print(f"Segmento: {resultado['segment']}")
print(f"Recomendación: {resultado['recommendation']}")
```

---

## Despliegue en producción

### Con Docker (recomendado)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY models/ models/
COPY resources/ resources/

EXPOSE 5000

CMD ["python", "src/serving.py", "--host", "0.0.0.0", "--port", "5000"]
```

### Con Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.serving:app
```

---

## Troubleshooting

### Error: "Modelo no cargado"

Asegúrate de que:
1. Existe `models/` con al menos un modelo `.pkl`
2. Existe `resources/metrics_summary.csv`

### Error: "Campos faltantes"

Verifica que el JSON incluya todos los campos requeridos por el modelo.
