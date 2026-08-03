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
docker compose exec app python -m app.cli.users create miq "Miqueias" --pin 123456
```

Parar:

```powershell
docker compose down
```
