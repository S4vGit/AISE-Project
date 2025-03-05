# AISE Project

## Overview
AISE Project is a platform designed to generate, analyze, and detect fake news from images.
The system is divided into three main sections:
- **Journalists Section**: Allows users to generate fake news based on uploaded images.
- **Researchers Section**: Enables testing the reliability of fake news detection models.
- **Administrators Section**: Manages users, images, and fake news entries.

The architecture consists of:
- **Frontend**: Developed with React and Vite.
- **Backend**: Built using FastAPI .
- **Machine Learning Pipelines**: Managed with ZenML to generate and detect fake news.
- **Mongo Database**

---

## Deployment
The project can be deployed in two ways: using Docker or manually in a local environment.

### 1. Deploy with Docker
#### Requirements
- **Docker** installed on your system
- **Docker Compose**

#### Start the project
Run the following commands in the project root:
```sh
# Build and start the containers
docker-compose up --build
```
The system will be accessible to localhost through the ports specified in "docker-compose.yml".

### 2. Deploy locally
#### Requirements
- **Python 3.8+**
- **Node.js + npm**
- **MongoDB** running locally or on a remote server
- **ZenML** installed and configured

#### Installation and Startup
1. **Clone the repository**
```sh
git clone https://github.com/S4vGit/AISE-Project.git
cd AISE-Project
```
2. **Set up backend dependencies**
```sh
cd backend
pip install -r requirements.txt
```
3. **Configure MongoDB**
Ensure that MongoDB is running and properly configured creating the `.env` file inside the `backend` folder:
```
MONGO_URI=mongodb://localhost:27017
```

4. **Start ZenML**
```sh
zenml init
```

5. **Set up frontend dependencies**
```sh
cd ../frontend
npm install
```

6. **Run the backend**
```sh
uvicorn main:app --reload
```

7. **Run the frontend**
 ```
npm run dev
```
The frontend will be accessible at `http://localhost:4173`.

## Setting Up the Administrator Account

To fully utilize the system, an administrator account must be created:

1. Open http://localhost:8000/docs in your browser.

2. Use the user registration endpoint.

3. Set the role field to A (Administrator) — the other two fields (ID and password) are arbitrary.

4. Submit the request.

Once registered, the admin can log in using the frontend and create new journalist (J) and researcher (R) accounts.

---

## System Components
The system architecture is divided into four main components: **Frontend, Backend, Machine Learning Pipelines**, and **Database**. These components work together to allow users to generate, analyze, and detect fake news based on images.

### 1. **Frontend (React + Vite)**
The frontend is a web interface developed with **React** and **Vite**, responsible for user interaction with the system.
### Features
- **User authentication and management:**
  - Allows login and registration with distinct user roles (`J`, `R`, `A`).
  - Administrators can create new accounts and manage users.
- **Image upload for fake news generation(`J`)**
  - Journalists can upload images, triggering the AI pipeline to generate fake news.
- **Image upload for fake news detection (`R`)**
  - Researchers can will able to access to the probability of being fake of a generated news.
- **Administrative management:**
  - Administrator can access a dashboard to view users, uploaded images, and fake news detection reports.

### 2. **Backend**
Built with **FastAPI**, the backend handles:
- **User authentication and role-based access**
  - Supports login and registration with password-based authentication.
  - Implements role-based access control (`J`, `R`, `A`).
- **Fake news management:**
  - Provides APIs for image uploads, fake news generation (`J`) and fake news detection (`R`) requests.
  - Allows retrieval of generated fake news and its analysis by researchers.
- **Integration with ZenML pipelines:**
  - Triggers pipelines for fake news generation and detection.
  - Retrieves AI model outputs and updates the database.

### 3. **Machine Learning Pipelines**
The ML pipelines are the core AI system responsible for fake news generation and detection. They are managed using **ZenML** to ensure modularity and traceability of the artifacts' output and pipelines.
**Fake News Generation Pipeline**:
- **Input:** An image uploaded by the user.
- **Steps:**
  1. **Image Captioning:** The AI model extracts a textual description of the image.
  2. **Text Generation:** The description is passed to an NLP fine-tuned model, which generates a fake news article.
  3. **Database Update:** The generated fake news is stored in the database and made available to the user.
**Fake News Detection Pipeline**:
- **Input:** An image uploaded by the user.
- **Steps:**
  1. **Image Captioning:** The AI model extracts a textual description of the image.
  2. **Text Generation:** The description is passed to an NLP fine-tuned model, which 
  3. **Oracle:** An Oracle analyzes the generated text and determines the probability that it is fake news through a weighted sum of the results of each of three detector which the oracle consists.
  4. **Database Update:** The generated fake news and detection result are stored in the database and made available to the user.

### 4. **Database (MongoDB)**
The database is structured into two main collections:
- `users`: Stores user data, including ID, hashed password, and role (`J`, `R`, `A`).
- `fake_news`: Contains images, their descriptions, generated fake news entries and detection result (in case of `R`).
