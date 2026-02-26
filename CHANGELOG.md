# CHANGELOG

## v1.0.0

Versión inicial del proyecto final de MLOps.

### Características principales:
- Estructura modular del repositorio siguiendo el ciclo de vida de ML.
- Script de preparación de datos (`src/data_preparation.py`) para transformar datos crudos a capa silver.
- Script de entrenamiento y evaluación de modelos (`src/train.py`) con selección automática del mejor modelo.
- Serialización y almacenamiento de modelos entrenados en `models/`.
- API REST para servir el modelo usando Flask (`src/serving.py`) con endpoints de salud, predicción individual, por lotes e información del modelo.
- Notebooks de análisis exploratorio y experimentación en `notebooks/`.
- Reportes técnicos y de negocio en `reports/`.
- Scripts de prueba de la API en `tests/`.
- Imágenes de resultados y respuestas del API en `resources/images/`.
- Documentación centralizada en `README.md` y manual de uso de la API en `src/API_USAGE.md`.
