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
