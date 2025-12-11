# Entrega Automation Testing Balbiano

Proyecto de entrega final que combina pruebas de UI (Selenium + Page Object Model) y pruebas de API (Requests) ejecutadas con `pytest`.

## Requisitos
- Python 3.10+
- Google Chrome (o Chromium) instalado
- Drivers gestionados automáticamente por Selenium Manager (incluido en Selenium 4)

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura
- `tests/ui/pages/`: Page Objects para saucedemo.com.
- `tests/ui/data/`: Datos de prueba (JSON/CSV) usados en parametrización.
- `tests/ui/test_ui_flows.py`: Casos de UI end-to-end (+ escenario negativo).
- `tests/api/test_api_reqres.py`: Casos de API públicos (ReqRes).
- `utils/`: Utilidades compartidas (driver, logging, data loading).
- `artifacts/screenshots/`: Capturas automáticas cuando falla una prueba.
- `pytest.ini`: Configuración de Pytest + reporte HTML.

## Ejecutar pruebas
UI (requiere navegador):
```bash
pytest tests/ui --html=artifacts/report-ui.html --self-contained-html
```

API:
```bash
pytest tests/api --html=artifacts/report-api.html --self-contained-html
```

Todas las pruebas:
```bash
pytest --html=artifacts/report.html --self-contained-html
```

## Notas
- Los Page Objects encapsulan la interacción con cada página y mantienen las pruebas limpias.
- El hook de Pytest en `conftest.py` captura pantalla y adjunta al reporte HTML cuando hay fallos.
- Los datos de pruebas UI usan parametrización con JSON y CSV de `tests/ui/data/`.
