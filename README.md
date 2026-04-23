# 🚀 DevOps CI/CD Dashboard

Dashboard web construido con **Flask**, contenerizado con **Docker** y desplegado automáticamente con **GitHub Actions** en **Render.com**.

---

## 📁 Estructura del Proyecto

```
devops-app/
├── app.py                          # Aplicación Flask principal
├── requirements.txt                # Dependencias Python
├── Dockerfile                      # Multi-stage Docker build
├── .gitignore
├── templates/
│   └── index.html                  # UI del dashboard
├── tests/
│   └── test_app.py                 # Pruebas unitarias (pytest)
└── .github/
    └── workflows/
        └── ci-cd.yml               # GitHub Actions CI/CD pipeline
```

---

## 🏃 Correr localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/devops-dashboard.git
cd devops-dashboard

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr la app
python app.py

# Abrir: http://localhost:5000
```

---

## 🧪 Ejecutar pruebas unitarias

```bash
pytest tests/ -v
```

---

## 🐳 Docker

```bash
# Build
docker build -t devops-dashboard .

# Run
docker run -p 5000:5000 devops-dashboard

# Abrir: http://localhost:5000
```

---

## 🔐 GitHub Secrets requeridos

Ve a tu repo → **Settings → Secrets and variables → Actions** y agrega:

| Secret | Descripción |
|---|---|
| `DOCKERHUB_USERNAME` | Tu usuario de Docker Hub |
| `DOCKERHUB_TOKEN` | Access Token de Docker Hub (no tu password) |
| `RENDER_DEPLOY_HOOK_URL` | URL del Deploy Hook de Render.com |

---

## ⚙️ Cómo obtener cada Secret

### Docker Hub Token
1. Entra a [hub.docker.com](https://hub.docker.com)
2. **Account Settings → Security → New Access Token**
3. Copia el token y agrégalo como `DOCKERHUB_TOKEN`

### Render Deploy Hook
1. Crea un nuevo **Web Service** en [render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. En la configuración del servicio: **Settings → Deploy Hook**
4. Copia la URL y agrégala como `RENDER_DEPLOY_HOOK_URL`

---

## 🔄 Pipeline CI/CD

Cada `git push` a `main` ejecuta automáticamente:

```
Push to main
    │
    ▼
🧪 Job 1: Test
    ├── Checkout código
    ├── Setup Python 3.12
    ├── pip install -r requirements.txt
    └── pytest tests/ -v
    │
    ▼ (si tests pasan)
🐳 Job 2: Docker
    ├── Login a Docker Hub
    ├── Build imagen (multi-stage)
    └── Push :latest y :<sha>
    │
    ▼
🌐 Job 3: Deploy
    └── Trigger Render Deploy Hook → Producción
```

---

## 🌐 API Endpoints

| Endpoint | Descripción |
|---|---|
| `GET /` | Dashboard UI |
| `GET /api/health` | Healthcheck |
| `GET /api/info` | Metadata de la app |
| `GET /api/pipeline` | Etapas del pipeline |
