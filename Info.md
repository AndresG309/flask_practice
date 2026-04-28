# Comandos de terminal

## Para activar el entorno virtual de python:

1. Establecer políticas de ejecución de scripts:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

2. Correr script de activación de venv:
   .venv\Scripts\Activate.ps1

## Activar modo Debug de flask (Cambios en tiempo real)
```powershell
# En Windows CMD
SET FLASK_DEBUG=1
# En powershell
$env:FLASK_DEBUG = "1"

flask run
```

## Crear Secret Key
Se puede usar el propio python para generar una clave secreta bastante extensa en la terminal y de manera sencilla
```python
python -c "import secrets; print(secrets.token_hex())"
```