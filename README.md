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

### 1. **Frontend**
Developed with **React** and **Vite**, the frontend allows users to:
- **Log in and manage user roles**
- **Upload images and generate fake news**
- **Test detection models**
- **Perform administrative tasks**

### 2. **Backend**
Built with **FastAPI**, the backend handles:
- **User authentication and role-based access**
- **APIs for fake news generation and detection**
- **Database interactions with MongoDB**
- **Integration with ZenML pipelines**

### 3. **Machine Learning Pipelines**
Utilizing **ZenML**, the AI modules function as follows:
- **Fake News Generation Pipeline**:
  - Extracts a description from the uploaded image
  - Generates a fake news article
  - Saves the data in the database
- **Fake News Detection Pipeline**:
  - Analyzes the generated news
  - Evaluates its authenticity using an NLP model
  - Stores the results in the database

### 4. **Database (MongoDB)**
The database is structured into two main collections:
- `users`: Stores user data, including ID, hashed password, and role (`J`, `R`, `A`).
- `fake_news`: Contains images, their descriptions, and generated fake news entries.

---

## Contributing
If you would like to contribute to the project, feel free to open an issue or submit a pull request on [GitHub](https://github.com/S4vGit/AISE-Project).

