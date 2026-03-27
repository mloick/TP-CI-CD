# EdTech Startup Student Directory API

![CI Pipeline](https://github.com/VOTRE_COMPTE/nom-du-repo/actions/workflows/ci.yml/badge.svg)

This repository contains a RESTful API for a student directory, built avec Python (Flask).

## API Documentation

### 1. Obtenir tous les étudiants (GET `/students`)
Supporte un système de **pagination** et de **tri** :
```http
GET /students?page=1&limit=10&sort=grade&order=desc
```
- Retourne le tableau JSON des étudiants.

### 2. Statistiques (GET `/students/stats`)
```http
GET /students/stats
```
- Renvoie statistiques totales (`totalStudents`, `averageGrade`, `studentsByField`, `bestStudent`).

### 3. Recherche (GET `/students/search?q=...`)
```http
GET /students/search?q=alice
```
- Renvoie tous ceux correspondant au terme dans le prénom ou le nom de famille.

### 4. Obtenir un étudiant par son ID (GET `/students/:id`)
```http
GET /students/1
```

### 5. Créer un étudiant (POST `/students`)
```http
POST /students
Content-Type: application/json

{
    "firstName": "John",
    "lastName": "Doe",
    "email": "johndoe@example.com",
    "grade": 15.5,
    "field": "informatique"
}
```

### 6. Mettre à jour un étudiant (PUT `/students/:id`)
```http
PUT /students/1
Content-Type: application/json

{
    "firstName": "Alice",
    "lastName": "Martin",
    "email": "alice2@example.com",
    "grade": 18,
    "field": "mathématiques"
}
```

### 7. Supprimer un étudiant (DELETE `/students/:id`)
```http
DELETE /students/1
```

## Lancer le Projet Localement
```bash
# 1. Installer les dépendances
make install

# 2. Lancer le serveur (Port 5000)
make start

# 3. Lancer les tests et voir le code coverage
make test

# 4. Lancer le linter et formateur
make format
make lint
```
