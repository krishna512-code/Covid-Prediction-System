
```markdown
# 🦠 COVID Prediction System

This project is a machine learning–powered web application that predicts whether a user is at risk of COVID-19 based on symptoms and input data. The application uses a trained model and provides real-time predictions through a user-friendly interface built with Flask.

> 🔗 Live Demo: [https://covid-prediction-system.onrender.com]  
> 🧠 Built with: Python, Flask, scikit-learn, HTML/CSS

---

## 🚀 Features

- Accepts input from users through a web form
- Predicts COVID risk using a trained machine learning model
- Displays risk result instantly on the same page
- Lightweight and easy to deploy on cloud platforms like Render or Heroku

---

## 🛠 Tech Stack

- **Frontend**: HTML, CSS (Jinja2 Templates)
- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn
- **Deployment**: Render
- **Model**: Pre-trained `.pkl` file using Logistic Regression / Random Forest

---

## 📁 Project Structure

```

Covid-Prediction-System/
├── app.py                  # Main Flask app
├── model.pkl               # Trained ML model
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main UI template

````

---

## ⚙️ Installation & Running Locally

1. **Clone the repository**  
```bash
git clone https://github.com/krishna512-code/Covid-Prediction-System.git
cd Covid-Prediction-System
````

2. **Create a virtual environment & install dependencies**

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the Flask app**

```bash
python app.py
```

4. Open your browser and go to:
   `http://localhost:5000`

---

## 🧠 How It Works

* The user inputs symptoms (e.g., fever, cough, tiredness).
* The data is passed to a trained ML model loaded from `model.pkl`.
* The model returns a prediction (e.g., `Likely`, `Not likely`).
* The result is displayed in the browser instantly.

---

## 📦 Deployment on Render

1. Push your project to GitHub
2. Create a new **Web Service** on [Render](https://render.com/)
3. Use the following settings:

   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
4. Ensure your `app.py` uses dynamic port:

```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

---

## 📝 License

This project is licensed for educational purposes and open-source contributions.

---

## 🙋‍♂️ Author

**Krishna Kant Narayan**
📧 [krishna.kant.2136@gmail.com](mailto:krishna.kant.2136@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/krishna-kant-narayan)

---

Happy coding! 🚀
