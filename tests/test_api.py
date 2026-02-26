"""Example client to test the serving API."""

import requests
import json

# Configuration
API_URL = "http://localhost:5000"


def test_health():
    """Test health endpoint."""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_single_prediction():
    """Test single prediction endpoint."""
    print("\n=== Testing Single Prediction ===")
    
    # High propensity customer
    cliente_alto = {
        "Edad": 45,
        "Ingreso": 5000,
        "Sexo": "M",
        "EstCiv": "Casado",
        "TVidaAño": 8,
        "T_TC": 1,
        "T_Micro": 0,
        "T_Convenios": 0,
        "T_EI": 0,
        "ZONA": "ZONA CENTRO",
        "Region": "LIMA",
        "Deu_TOTAL_SBS": 10000,
        "Deu_TCre_SBS": 2000,
        "Lin_TCre_SBS": 5000,
        "Deu_MiViv_SBS": 0,
        "Prov": "LIMA",
        "REdad": 45,
        "Deu_Hipo_SBS": 0,
        "Deu_Micr_SBS": 0,
        "Deu_Vehi_SBS": 0,
        "Deu_Pequ_SBS": 0,
        "Deu_PLD_SBS": 0,
        "Dis": "CENTRO",
        "Deu_Otro_SBS": 0,
        "Deu_Emp_SBS": 0,
        "Deu_ConN_SBS": 0,
        "Deu_Conv_SBS": 0,
        "Deu_HipTrad_SBS": 0,
        "Deu_ConR_SBS": 0
    }
    
    response = requests.post(f"{API_URL}/predict", json=cliente_alto)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_batch_prediction():
    """Test batch prediction endpoint."""
    print("\n=== Testing Batch Prediction ===")
    
    clientes = [
        {
            "Edad": 45,
            "Ingreso": 5000,
            "Sexo": "M",
            "EstCiv": "Casado",
            "TVidaAño": 8,
            "T_TC": 1,
            "T_Micro": 0,
            "T_Convenios": 0,
            "T_EI": 0,
            "ZONA": "ZONA CENTRO",
            "Region": "LIMA",
            "Deu_TOTAL_SBS": 10000,
            "Deu_TCre_SBS": 2000,
            "Lin_TCre_SBS": 5000,
            "Deu_MiViv_SBS": 0,
            "Prov": "LIMA",
            "REdad": 45,
            "Deu_Hipo_SBS": 0,
            "Deu_Micr_SBS": 0,
            "Deu_Vehi_SBS": 0,
            "Deu_Pequ_SBS": 0,
            "Deu_PLD_SBS": 0,
            "Dis": "CENTRO",
            "Deu_Otro_SBS": 0,
            "Deu_Emp_SBS": 0,
            "Deu_ConN_SBS": 0,
            "Deu_Conv_SBS": 0,
            "Deu_HipTrad_SBS": 0,
            "Deu_ConR_SBS": 0
        },
        {
            "Edad": 32,
            "Ingreso": 2500,
            "Sexo": "F",
            "EstCiv": "Soltero",
            "TVidaAño": 3,
            "T_TC": 0,
            "T_Micro": 0,
            "T_Convenios": 0,
            "T_EI": 0,
            "ZONA": "ZONA SUR",
            "Region": "LIMA",
            "Deu_TOTAL_SBS": 5000,
            "Deu_TCre_SBS": 1000,
            "Lin_TCre_SBS": 2000,
            "Deu_MiViv_SBS": 0,
            "Prov": "LIMA",
            "REdad": 32,
            "Deu_Hipo_SBS": 0,
            "Deu_Micr_SBS": 0,
            "Deu_Vehi_SBS": 0,
            "Deu_Pequ_SBS": 0,
            "Deu_PLD_SBS": 0,
            "Dis": "SUR",
            "Deu_Otro_SBS": 0,
            "Deu_Emp_SBS": 0,
            "Deu_ConN_SBS": 0,
            "Deu_Conv_SBS": 0,
            "Deu_HipTrad_SBS": 0,
            "Deu_ConR_SBS": 0
        },
        {
            "Edad": 50,
            "Ingreso": 7000,
            "Sexo": "M",
            "EstCiv": "Casado",
            "TVidaAño": 12,
            "T_TC": 1,
            "T_Micro": 0,
            "T_Convenios": 0,
            "T_EI": 0,
            "ZONA": "ZONA NORTE",
            "Region": "LIMA",
            "Deu_TOTAL_SBS": 15000,
            "Deu_TCre_SBS": 3000,
            "Lin_TCre_SBS": 7000,
            "Deu_MiViv_SBS": 0,
            "Prov": "LIMA",
            "REdad": 50,
            "Deu_Hipo_SBS": 0,
            "Deu_Micr_SBS": 0,
            "Deu_Vehi_SBS": 0,
            "Deu_Pequ_SBS": 0,
            "Deu_PLD_SBS": 0,
            "Dis": "NORTE",
            "Deu_Otro_SBS": 0,
            "Deu_Emp_SBS": 0,
            "Deu_ConN_SBS": 0,
            "Deu_Conv_SBS": 0,
            "Deu_HipTrad_SBS": 0,
            "Deu_ConR_SBS": 0
        }
    ]
    
    response = requests.post(f"{API_URL}/predict_batch", json=clientes)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_model_info():
    """Test model info endpoint."""
    print("\n=== Testing Model Info ===")
    response = requests.get(f"{API_URL}/model_info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    try:
        print("🧪 Testing Propensity API")
        print(f"API URL: {API_URL}")
        
        test_health()
        test_single_prediction()
        test_batch_prediction()
        test_model_info()
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: No se pudo conectar a {API_URL}")
        print("   Asegúrate de que el servidor esté corriendo con: python src/serving.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
