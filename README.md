# 🦉 RavenCode – Módulo de Aprendizaje

Este repositorio forma parte del proyecto **RavenCode**, una plataforma de aprendizaje interactiva diseñada para enseñar 
programación a adolescentes de 12 a 16 años. Aquí se encuentra exclusivamente el **módulo de Aprendizaje**, que gestiona 
los contenidos temáticos, el editor de código, las evaluaciones automáticas y la retroalimentación interactiva.

---

## 🚀 ¿Cómo ejecutar el módulo?

### 🧠 Backend – FastAPI

1. Ir a la carpeta del backend:
```bash
   cd ravencode-backend-learning
```
2. Crear entorno virtual:
```bash
   python -m venv venv
```
3. Activar enorno
* En Windows
```bash
   venv\Scripts\activate
```
* En Mac/Linux
```bash
   source venv/bin/activate
```
4. Instalar dependencias
```bash
   pip install -r requirements.txt
```
5. Ejecutar el servidor
```bash
   uvicorn app.main:app --reload --port 8002
```
6. Verificar en el navegador:

   http://localhost:8002

7. Documentacion Swagger Endpoints

   http://localhost:8002/docs

## Observabilidad📊📈

### **Prerrequisitos**⚙️

Antes de comenzar, asegúrate de tener las siguientes herramientas instaladas:

Prometheus📡 - Para la recolección de métricas.

Grafana💻 - Para la visualización de métricas.

### **Configuración Prometheus** 🔧

Tu archivo prometheus.yml de configuración debe verse asi:
```bash
global:
scrape_interval: 15s  # Set the scrape interval to every 15 seconds.
evaluation_interval: 15s  # Evaluate rules every 15 seconds.

# Scrape configuration for Prometheus itself.
scrape_configs:
- job_name: "prometheus"
   static_configs:
   - targets: ["localhost:9090"]
      labels:
         app: "prometheus"

# Scrape configuration for FastAPI service
- job_name: "fastapi-service"
   static_configs:
   - targets: ["localhost:8002"]  # Replace with your FastAPI service URL and port
      labels:
         app: "fastapi"
```

#### **Iniciar Prometheus** 🚀
1. Abre una terminal (cmd o PowerShell).
2. Navega hasta la carpeta donde descomprimiste Prometheus.
3. Ejecuta el siguiente comando para iniciar Prometheus:
```bash
   prometheus.exe --config.file=prometheus.yml
```

#### **Acceder a Prometheus** 🖥️

1. Una vez iniciado, abre un navegador y accede a: 

   http://localhost:9090 

2. Puedes usar la pestaña Status > Targets para verificar que Prometheus esté recolectando las métricas de tu aplicación.


### **Configuración Grafana** 📊

1. Abre una terminal (cmd o PowerShell).

2. Navega a la carpeta bin dentro de la carpeta de Grafana 

   ```bash
      cd C:\grafana\bin
   ```

3. Ejecuta el siguiente comando para iniciar Grafana:
   ```bash
      grafana-server.exe
   ```
   #### **Acceder a Grafana** 🖥️
   1. Abre un navegador y accede a:
   
       http://localhost:3000 

   2. El usuario y la contraseña por defecto son admin.

Despues de tener los pasos anteirores, solo debes configurar Prometheus como fuente de datos en grafana y crea un Dashboard para visualizar tus consultas PromQL.

### 🔐 Funcionalidades del módulo
* Acceso progresivo a módulos temáticos de programación.

* Visualización estructurada del contenido (teoría, ejemplos, retos).

* Editor de código interactivo con resaltado de sintaxis.

* Evaluación automática de ejercicios mediante test cases.

* Retroalimentación inmediata y detallada al usuario.

### 👥 Equipo de desarrollo
Proyecto desarrollado por el equipo Cuervos en el curso Ingeniería de Software II – Universidad Nacional de Colombia.

* Diego Felipe Solorzano Aponte

* Laura Valentina Pabon Cabezas

* Diana Valentina Chicuasuque Rodríguez

* Carlos Arturo Murcia Andrade

* Sergio Esteban Rendon Umbarila

* Mateo Andrés Vivas Acosta

* Jorge Andrés Torres Leal

#### Docente: Ing. Camilo Ernesto Vargas Romero
#### Semestre: 2025-1
