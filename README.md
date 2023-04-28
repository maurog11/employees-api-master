# Employees API
## Descripcion
API - Python Framework Flask - Angular 15 - DB SQLite    

## Requerimientos

Para ejecutar el api, se requiere tener instalados:

- Python v3.8
- virtualenv
- Gestor de Base de Batos (SQLite)
- NodeJS v18 y npm v9

### Ejecutar backend

`cd backend`

`virtualenv -p python3 bundle_env`

`cd .\bundle_env\Scripts\`
`.\activate`

`pip install -r requirements.txt`

`python manage.py recreate_db`

`python manage.py runserver`

Abrir `http://localhost:3001/` en el navegador.

### Ejecutar frontend

`cd frontend`

`npm install` y `npm start`
Abrir `http://localhost:4200` en el navegador.
