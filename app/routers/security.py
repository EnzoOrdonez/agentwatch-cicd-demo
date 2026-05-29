from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/security",
    tags=["Security"]
)


@router.get("/reports")
def list_security_reports():
    return {
        "reports": [
            {
                "id": "sec-001",
                "herramienta": "Semgrep",
                "paquete": "app/routers/agents.py",
                "version_vulnerable": "N/A",
                "version_segura": "N/A",
                "severidad": "Medium",
                "descripcion": "Posible validación insuficiente en endpoint de creación de agentes.",
                "estado": "Completado",
                "bloquea_merge": False,
                "tiempo": "1 min 12 s"
            },
            {
                "id": "sec-002",
                "herramienta": "OWASP Dependency-Check",
                "paquete": "fastapi",
                "version_vulnerable": "0.136.3",
                "version_segura": "0.136.4",
                "severidad": "High",
                "descripcion": "Dependencia con vulnerabilidad conocida simulada para demostración.",
                "estado": "Completado",
                "bloquea_merge": True,
                "tiempo": "2 min 34 s"
            },
            {
                "id": "sec-003",
                "herramienta": "Quality Gate",
                "paquete": "pipeline",
                "version_vulnerable": "N/A",
                "version_segura": "N/A",
                "severidad": "High",
                "descripcion": "El merge queda bloqueado por hallazgos High/Critical.",
                "estado": "Bloqueado",
                "bloquea_merge": True,
                "tiempo": "5 s"
            }
        ]
    }