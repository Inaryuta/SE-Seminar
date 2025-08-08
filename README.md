# Software Engineer Seminar – General Repository

**Institution**: Francisco José de Caldas District University  
**Program**: Systems Engineering

**Course**: Software Engineer Seminar  
**Professor**: Eng. Carlos Andrés Sierra, M.Sc.

---

## Team Members

- Esteban Villalba Delgadillo - 20212020064  
  eavillalbad@udistrital.edu.co  
- Walter Suarez Fonseca - 20212020107 
  wasuarezf@udistrital.edu.co 

---

## Repository Purpose

This repository serves as a central space for materials, notes, and future developments related to the **Software Engineer Seminar** course. As the semester progresses, the repository will be updated with:

- Workshop summaries  
- Research materials  
- Technical documentation  
- Presentations and reports  

---

## Project Description

**GymFlow** is a graphical user interface (GUI)-based fitness tracking application that enables users to record workout sessions, monitor their performance, and visualize progress through interactive charts and statistics. The main objective is to simplify training data logging and provide meaningful insights to improve personal fitness goals.

The system implements a **modular architecture** with separate components for authentication, routine/session management, and statistical analysis. It is built using **FastAPI** for the backend, **PostgreSQL** for persistent data storage, and a lightweight **HTML/CSS/JavaScript** frontend.

Additionally, the system underwent **Behavior-Driven Development (BDD)** testing, **API functional testing** using Postman, and **load testing** with Apache JMeter to validate performance under concurrent usage.

### Objectives

- Allow secure user registration, login, and logout.
- Enable detailed recording of workout sessions (type, duration, intensity, exercises, etc.).
- Provide access to a full training history per user.
- Display general statistics and interactive charts for performance tracking.
- Ensure system stability under high-concurrency scenarios.

---

## Project Components

### 1. **Authentication & User Management**
- Registration, login, and secure logout.
- Token-based authentication using JWT.
- Access control to ensure users only view their own data.

### 2. **Routine & Session Management**
- Create workout routines and associate them with sessions.
- Record exercises performed in each session.
- View full history of routines and sessions.

### 3. **Statistics & Charts**
- Generate summaries: total hours trained, calories burned, most frequent activities.
- Interactive visualizations (bar and line charts) for progress tracking.

### 4. **Testing & Validation**
- **BDD Testing**: Implemented in Gherkin syntax to validate user flows such as authentication, session logging, and statistics generation.
- **API Testing (Postman)**: Verified CRUD operations for all main modules (User, Exercise, Routine, RoutineExercise, RoutineSession, Auth).
- **Load Testing (JMeter)**: Simulated concurrent usage on critical endpoints (`/routines/user/{id}`, `/exercises/`, `/routine-sessions/`, `/routine-exercises/`, `/auth/login`) to ensure performance stability.

---

## Features

- **User Profiles**: Isolated, secure data per account.
- **Detailed Tracking**: Record complete workout details.
- **History Retrieval**: Chronological list of all training sessions.
- **Filtering Tools**: Analyze performance over specific date ranges.
- **Data Visualization**: Graphs for calories, duration, and activity frequency.
- **High-Performance API**: Tested under simulated high user load with JMeter.

---

## Example API Usage

**Register a new user:**
```json
POST /auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```
## Execution Instructions

1. **Cloning the repository:**
   To work with the ER model and supporting materials, clone the repository using the following command:

```bash
   git clone https://github.com/Inaryuta/SE-Seminar
```

2. **Navigate to the project directory:**
```bash
   cd GymFlow
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```
4. **Run the backend server:**
```bash
   uvicorn main:app --reload
```
## License
License
This project is developed for academic purposes within the course Software Seminar Engineer at the Universidad Distrital Francisco José de Caldas.
