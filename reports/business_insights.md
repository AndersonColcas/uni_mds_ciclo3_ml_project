# Reporte de Negocio: Propensión a Depósitos a Plazo

**Proyecto:** Modelo de Propensión para Productos Pasivos  
**Fecha:** Febrero 2026  

---

## Resumen Ejecutivo

Este reporte presenta las **estrategias de negocio** basadas en el modelo predictivo de propensión a la contratación de Depósitos a Plazo (DP), cuyo objetivo es **aumentar los ingresos en $6MM adicionales**.

El modelo desarrollado alcanza un **AUC > 0.84**, demostrando alta capacidad de discriminación entre clientes propensos y no propensos a contratar un DP.

---

## Resultados Clave

### 1. Análisis de Lift

El modelo permite priorizar clientes con mayor probabilidad de conversión:

| Segmento | Tasa de Conversión | Lift | Interpretación |
|----------|-------------------|------|----------------|
| **Top 5%** | ~80% | 2.35x | 2.3 veces mejor que selección aleatoria |
| **Top 10%** | ~75% | 2.19x | Mantiene alta eficiencia con mayor volumen |
| **Top 20%** | ~70% | 2.04x | Duplica probabilidad respecto al azar |

**Impacto:** Si el presupuesto de marketing alcanza solo para el 5% de la base, este segmento es altamente rentable y preciso.

---

## Estrategias de Negocio Basadas en Resultados

### 1. Campañas Dirigidas por Ingresos

**Hallazgo:** Clientes con mayores ingresos muestran diferencia estadísticamente significativa (p ≈ 0.0).

**Estrategia:**
- Segmentar campañas por nivel de ingreso
- Ofrecer montos más altos o productos premium a top earners
- Diseñar tasas diferenciadas según capacidad de ahorro

**Ejemplo de acción:**
> "Clientes con ingresos >$X reciben oferta de DP con tasa preferencial del Y% para montos >$Z"

---

### 2. Enfoque por Estado Civil

**Hallazgo:** Estado civil es un diferenciador clave (p ≈ 0.0).

**Estrategia:**
- **Casados:** Mensajes enfocados en seguridad familiar y ahorro a largo plazo
  - *"Asegura el futuro de tu familia con nuestros depósitos a plazo"*
- **Solteros/Jóvenes:** Enfoque en flexibilidad y crecimiento patrimonial
  - *"Haz crecer tu dinero con tasas competitivas"*
- **Divorciados/Viudos:** Énfasis en estabilidad financiera

---

### 3. Cross-Selling con Productos Vigentes

**Hallazgo:** Tenencia de productos de crédito (especialmente TC) está fuertemente asociada a mayor propensión (p ≈ 0.0).

**Estrategia:**
- **Trigger automático:** Al aprobar un crédito, ofrecer inmediatamente DP con beneficios adicionales
- Vincular tasas de DP con líneas de crédito existentes
- Programa de fidelización: "Clientes con crédito + DP obtienen X beneficios"

**Ejemplo de acción:**
> "Cliente con TC recibe oferta de DP con tasa +0.5% por 3 meses como bono de vinculación"

---

### 4. Priorización por Modelo de Propensión

**Hallazgo:** El Top 5% tiene 2.3x más probabilidad de contratación.

**Estrategia:**
- **Prioridad 1 (Top 5%):** Contacto telefónico personalizado + ejecutivo dedicado
- **Prioridad 2 (Top 10%):** Email marketing + SMS con oferta especial
- **Prioridad 3 (Top 20%):** Campaña digital masiva

**Optimización de recursos:**
- En campañas con presupuesto limitado → focalizar en Top 5%
- En campañas para escalamiento → ampliar a Top 20%

---

### 5. Optimización de Inversión en Marketing

**Hallazgo:** El Top 20% mantiene Lift >2x, capturando más volumen sin sacrificar demasiada precisión.

**Estrategia:**
- **Presupuesto bajo:** Top 5% (máxima conversión)
- **Presupuesto medio:** Top 10% (balance conversión-volumen)
- **Presupuesto alto:** Top 20% (escalar captación manteniendo eficiencia)

**Cálculo de ROI esperado:**
```
Escenario Conservador (Top 5%):
- Clientes contactados: 5% de base = X clientes
- Conversión esperada: 80%
- Ingresos estimados: [cálculo específico]

Escenario Agresivo (Top 20%):
- Clientes contactados: 20% de base = Y clientes
- Conversión esperada: 70%
- Ingresos estimados: [cálculo específico]
```

---

## Hallazgos Adicionales

### Variables NO Significativas

**Edad:** No resultó estadísticamente significativa como predictor único (p = 0.54).

**Recomendación:** NO usar edad como criterio principal de segmentación. En su lugar, combinar con otras variables (ingresos, estado civil, productos vigentes).

### Variables Clave

1. **Estado Civil** → Muy significativa
2. **Ingresos** → Muy significativa  
3. **Tenencia de Productos de Crédito** → Muy significativa

---

## Plan de Acción Propuesto

### Corto Plazo (1-3 meses)

1. **Implementar campaña piloto** con Top 5% del modelo
   - Medir conversión real vs predicha
   - Ajustar estrategias de contacto
   
2. **Diseñar mensajes segmentados** por estado civil e ingresos
   - A/B testing de contenidos
   
3. **Crear trigger automático** en sistema de créditos
   - Oferta de DP post-aprobación de TC

### Mediano Plazo (3-6 meses)

1. **Escalar a Top 10%** según resultados del piloto
2. **Implementar programa de fidelización** cross-product
3. **Ajustar modelo** con datos reales de conversión

### Largo Plazo (6-12 meses)

1. **Integrar modelo en CRM** para scoring en tiempo real
2. **Automatizar campañas** según score de propensión
3. **Reentrenar modelo** trimestralmente con nueva data

---

## Métricas de Seguimiento

### KPIs Principales

| Métrica | Baseline | Meta |
|---------|----------|------|
| **Tasa de Conversión General** | X% | X + Y% |
| **Ingresos por DP** | $14MM | $20MM |
| **Conversión Top 5%** | - | 75-85% |
| **Conversión Top 10%** | - | 70-80% |
| **ROI Campañas** | - | >3x |

### Métricas Secundarias

- Tiempo promedio hasta conversión
- Monto promedio de DP contratado
- Retención de clientes con DP a 6/12 meses
- Cross-sell adicional post-DP

---

## Conclusiones

1. **Modelo robusto:** AUC > 0.84 demuestra alta capacidad predictiva
   
2. **Drivers claros:** Estado civil, ingresos y tenencia de crédito son factores clave en la decisión de contratación

3. **Lift comprobado:** El modelo permite identificar segmentos 2-2.3x más propensos que la población general

4. **Edad no determinante:** Contrario a la hipótesis inicial, la edad sola NO es un predictor significativo

5. **Oportunidad probada:** Focalizar campañas en Top 5-20% permite optimizar recursos y maximizar conversión

---

## 📎 Anexos

- **Detalles técnicos del modelo:** Ver `notebooks/propension_eda.ipynb`
- **Métricas completas:** Ver `resources/metrics_summary.csv`
- **Análisis de lift:** Ver `resources/lift_analysis.csv`
- **Visualizaciones:** Ver `resources/images/`


