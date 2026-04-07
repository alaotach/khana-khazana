import uuid
from flask import Flask, render_template, request, jsonify, url_for, session
from db import Database
import os
import time
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "khana_khazana"

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

limiter = Limiter(get_remote_address, app=app, default_limits=["500 per day", "100 per hour"])

db = Database("recipes.db")
os.makedirs("static/uploads", exist_ok=True)

def clean():
    try:
        with db:
            db.execute("CREATE TABLE IF NOT EXISTS recipes (id TEXT PRIMARY KEY, name TEXT, ing TEXT, ins TEXT)")
            recipes = db.fetchall("SELECT ing, ins FROM recipes")
        htmll = "".join([(r[0] or "") + (r[1] or "") for r in recipes])
        curr = time.time()
        for file in os.listdir("static/uploads"):
            filepath = os.path.join("static", "uploads", file)
            if os.path.isfile(filepath):
                fage = curr - os.path.getmtime(filepath)
                if fage > 1800 and file not in htmll:
                    os.remove(filepath)
    except Exception as e:
        print(e)

@app.route('/')
def home():
    clean()
    return render_template('index.html')

@app.route("/recipes")
def recipes():
    with db:
        db.execute("CREATE TABLE IF NOT EXISTS recipes (id TEXT PRIMARY KEY, name TEXT, ing TEXT, ins TEXT)")
        recipes_from_db = db.fetchall("SELECT id, name, ing, ins FROM recipes")
    
    recipes_list = [{"id": r[0], "name": r[1], "ing": r[2], "ins": r[3]} for r in recipes_from_db]
    return render_template('recipes.html', recipes=recipes_list)

@app.route("/recipe/<id>")
def recipe(id):
    with db:
        recipe = db.fetchone("SELECT id, name, ing, ins FROM recipes WHERE id = ?", (id,))
    if not recipe:
        return "Recipe not found", 404
    
    recipe_dict = {"id": recipe[0], "name": recipe[1], "ing": recipe[2], "ins": recipe[3]}
    return render_template('recipe.html', recipe=recipe_dict)

@app.route("/create", methods=["GET", "POST"])  
@limiter.limit("1 per minute", methods=["POST"])
def create_recipe():
    if request.method == "POST":
        with db:
            name = request.form.get("name")
            ing = request.form.get("ing")
            ins = request.form.get("ins")
            if not name or not ing or not ins:
                return "All fields are required", 400
            
            recipe_id = str(uuid.uuid4())
            db.execute("INSERT INTO recipes (id, name, ing, ins) VALUES (?, ?, ?, ?)",
                       (recipe_id, name, ing, ins))
            session.pop('temps', None)
    else:
        timgs = session.get('temps', [])
        for img in timgs:
            filepath = os.path.join("static", "uploads", img)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
        session['temps'] = []
        
    return render_template('create.html')

@app.route("/upload", methods=["POST"])
@limiter.limit("5 per minute")
def upload():
    if 'upload' not in request.files:
        return "No file part", 400
    file = request.files['upload']
    if file.filename == '':
        return "No selected file", 400

    f = secure_filename(file.filename)
    filepath = os.path.join("static", "uploads", f)
    file.save(filepath)
    timgs = session.get('temps', [])
    timgs.append(f)
    session['temps'] = timgs
    session.modified = True

    return jsonify({"uploaded": 1, "fileName": f, "url": url_for('static', filename=f'uploads/{f}')})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3459)