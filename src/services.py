import httpx

tempo_limite = 10.0

def checar_status_servicos():
    """Verifica rapidamente a disponibilidade das APIs externas."""
    try:
        # Verifica o IBGE e o Open-Meteo com um timeout mais curto (3 segundos)
        r_ibge = httpx.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados/CE/municipios", timeout=3.0)
        r_meteo = httpx.get("https://geocoding-api.open-meteo.com/v1/search?name=Fortaleza&count=1", timeout=3.0)
        
        if r_ibge.status_code == 200 and r_meteo.status_code == 200:
            return True
        return False
    except Exception:
        return False

def buscar_clima(cidade: str):
    try:
        geo = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": cidade,
                "count": 1,
                "language": "pt",
                "format": "json"
            },
            timeout=tempo_limite
        )
        geo.raise_for_status()
        resultados = geo.json().get("results")

        if not resultados:
            return None

        item = resultados[0]
        latitude = item["latitude"]
        longitude = item["longitude"]

        clima = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "temperature_2m_max,temperature_2m_min",
                "current_weather": "true",
                "timezone": "auto"
            },
            timeout=tempo_limite
        )
        clima.raise_for_status()
        dados_clima = clima.json()

        return {
            "cidade": item["name"],
            "estado": item.get("admin1", ""),
            "temperatura_min": dados_clima["daily"]["temperature_2m_min"][0],
            "temperatura_max": dados_clima["daily"]["temperature_2m_max"][0],
            "weathercode": dados_clima["current_weather"].get("weathercode", 0)
        }

    except (httpx.RequestError, httpx.HTTPStatusError):
        return {"error_type": "503", "servico": "Open-Meteo"}
    except Exception:
        return None


def listar_cidades(uf: str, limite: int):
    try:
        resposta = httpx.get(
            f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios",
            timeout=tempo_limite
        )
        if resposta.status_code != 200:
            return {"error_type": "503", "servico": "IBGE"}

        lista = resposta.json()
        nomes_cidades = [cidade["nome"] for cidade in lista]
        return nomes_cidades[:limite]

    except (httpx.RequestError, httpx.HTTPStatusError):
        return {"error_type": "503", "servico": "IBGE"}
    except Exception:
        return None
