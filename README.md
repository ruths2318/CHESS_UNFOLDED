# ♟️ CHESS_UNFOLDED: The Story of Moves

**Chess_Unfolded** is a Django-based web application for analyzing chess games.  
You can analyze **past games stored in a database** or **upload a new `.pgn` file** to generate a detailed game summary with visualizations and highlights.

---

## 🚀 How to Run the Project Locally

1. **Create a virtual environment**  
   ```
   python -m venv myenv
   ```
2. **Activate the virtual environment**
    ```
    myenv\Scripts\activate
    ```
3. **Install all dependencies**
    ```
    pip install -r requirements.txt
    ```
4. create a .env file in the root directory(inside /CHESS_UNFOLDED folder),to store the API key(.env is submitted on canvas)

5. **Run the development server**
    ```
    python manage.py runserver
    ```
    Then open: http://127.0.0.1:8000/

---

## 🕹️ How to Use the Website

Once the server is running, the homepage gives you **two options** for analysis:

### 1. 🔁 Analyze Past Games
- Use the **dropdown menu** to view games stored in the database.
- Select a game and click **"Analyze Selected Game"**.
- You'll get a summary with:
  - Game summary,highlights,etc
  - Time plot
  - WDL (Win/Draw/Loss) chart
  - Chess.com replay link 

### 2. 📤 Analyze a New Game
- Upload a `.pgn` file (e.g., from `data/sample/`) **or** paste PGN text directly.
- Click **"Summarize New Game"**.
- The app will generate:
  - Game summary,highlights,etc
  - Time plot
  - WDL (Win/Draw/Loss) chart
  - Chess.com replay link    

---
## To Run the tests

  To run the tests execute the command:
    ``` pytest```
