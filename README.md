# AgentWatch · CI/CD (Módulo 2: Despliegue)

![módulo](https://img.shields.io/badge/m%C3%B3dulo-despliegue%20(CI%2FCD)-1f6feb?style=flat)
![coverage](https://img.shields.io/badge/coverage-99%25-2ea043?style=flat)
![quality gate](https://img.shields.io/badge/quality%20gate-ruff%20%2B%20pytest%20%2B%20Semgrep-8957e5?style=flat)
![canary](https://img.shields.io/badge/canary-10%2F50%2F100-orange?style=flat)
![rollback](https://img.shields.io/badge/rollback-auto%20%3C%202%25-red?style=flat)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

Pipeline de integración y entrega continua del backend de AgentWatch, una plataforma de gobernanza de agentes de IA. Acá vive mi parte del proyecto, el módulo de despliegue (RF05 a RF08). Todo el pipeline está como código en `.github/workflows/`, sin pasos manuales fuera del repo.

El backend es una API en FastAPI. Mi módulo suma los routers de `deployments`, `versions` y `environments`, y la maquinaria de CI/CD que los lleva a producción sin que nadie toque un botón de más.

## El flujo

```
PR ─► ci.yml ─► merge a develop ─► deploy-staging.yml ─► (tag) ─► deploy-prod-canary.yml
      lint · tests · Semgrep · build                             10% ─► 50% ─► 100%
                                                                 Prometheus vigila el error rate
                                                                 rollback automático si pasa de 2%
```

## Qué hace cada workflow

`ci.yml` es el quality gate y corre en cada PR. Pasa `ruff` para lint, `pytest` con un piso de cobertura del 70% sobre los módulos de despliegue, y `semgrep`, que frena el merge si aparece algo Critical o High. Si todo pasa, construye la imagen Docker. Está configurado como *required status check*, así que un PR roto no entra a la rama protegida.

`deploy-staging.yml` despliega a staging cuando algo llega a `develop`, usando el *environment* `staging` de GitHub para dejar traza.

`deploy-prod-canary.yml` es el despliegue a producción con estrategia canary. Enruta el tráfico en tres fases, 10%, 50% y 100%, con ventanas de 5 minutos entre cada una. En cada fase Prometheus mira el error rate de la revisión nueva. Si se pasa del 2%, salta el rollback automático a la revisión anterior. Requiere aprobación en el *environment* `production`.

## Stack

FastAPI · Docker · GitHub Actions · ruff · pytest + pytest-cov · Semgrep · Prometheus · Azure Container Apps (target)

## Correr local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload          # API en http://127.0.0.1:8000
pytest tests/ --cov=app.routers.deployments --cov-fail-under=70
```

## Alcance

Prototipo académico. La estructura del pipeline y los quality gates son reales y ejecutables. Los pasos de despliegue a Azure quedan como placeholders porque piden credenciales de una suscripción. La lógica de orquestación, versionado y rollback se demuestra en el backend FastAPI.
