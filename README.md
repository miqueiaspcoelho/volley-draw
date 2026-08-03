# Volley Draw

## Docker local

Subir app e PostgreSQL:

```powershell
docker compose up --build
```

Acessar:

```text
http://127.0.0.1:8005
```

Criar primeiro usuario:

```powershell
docker compose exec app python -m app.cli.users create user_name "name" --pin "XXXXX"
```

Parar:

```powershell
docker compose down
```
