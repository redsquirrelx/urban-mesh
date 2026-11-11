# Pruebas y contratos

La suite de pruebas utiliza `pytest` y `fastapi.testclient.TestClient`. `tests/test_api.py` contiene recorridos HTTP; `tests/test_workflows.py` valida el ensamblaje de escenarios de usuario; `tests/test_policies.py` verifica valores deterministas y `tests/test_storage.py` el contrato básico del almacenamiento local.

```bash
python -m pip install -e '.[dev]'
pytest -q
pytest tests/test_api.py -q
python -m compileall -q src
```

Las integraciones futuras deben añadir pruebas de sustitución para cada nuevo adaptador. El origen normativo de los resultados esperados es `docs/requirements.md`; los contratos de puertos están en AC-105 y las invariantes en AC-106. Las pruebas HTTP no sustituyen la revisión de reglas estáticas de dependencia.
