import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la extensión de SQLAlchemy con nuestra aplicación Flask
db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "dirtylittlesecret"  # Cambia esto en producción
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# --- 2. Configuración de CORS (Permitir comunicación con tu Frontend) ---
# Necesitas especificar el "origen" (origin) de tu frontend.
# Por ahora, estamos asumiendo que tu frontend se ejecuta en http://localhost:8000
# Si tu frontend se ejecuta en otro puerto local (ej. 3000 o 5500), cámbialo aquí.
# En producción, esto sería el dominio real de tu página web.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

# --- 3. Modelo de Base de Datos para Proyectos ---
class Project(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    shortDescription = db.Column(db.Text, nullable=False)
    fullDescription = db.Column(db.Text, nullable=False)
    imageUrl = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'shortDescription': self.shortDescription,
            'fullDescription': self.fullDescription,
            'imageUrl': self.imageUrl,
            'category': self.category,
            'location': self.location,
            'year': self.year
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# --- 4. Rutas de la API (Endpoints) ---

# GET: Obtener todos los proyectos
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

# GET: Obtener un proyecto por ID
@app.route('/api/projects/<string:project_id>', methods=['GET'])
def get_project(project_id):
    project = db.session.get(Project, project_id) # Usa db.session.get para buscar por PK
    if project:
        return jsonify(project.to_dict())
    return jsonify({"message": "Project not found"}), 404

# POST: Crear un nuevo proyecto
@app.route('/api/projects', methods=['POST'])
@jwt_required()
def add_project():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    required_fields = ['id', 'title', 'shortDescription', 'fullDescription', 'imageUrl', 'category', 'location', 'year']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
    
    # Verificar si el proyecto ya existe antes de intentar añadirlo
    if Project.query.get(data['id']):
        return jsonify({"message": "Project with this ID already exists"}), 409 # 409 Conflict

    new_project = Project(
        id=data['id'],
        title=data['title'],
        shortDescription=data['shortDescription'],
        fullDescription=data['fullDescription'],
        imageUrl=data['imageUrl'],
        category=data['category'],
        location=data['location'],
        year=data['year']
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

# PUT: Actualizar un proyecto existente
@app.route('/api/projects/<string:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    project = db.session.get(Project, project_id) # Usa db.session.get
    if project is None:
        return jsonify({"message": "Project not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    project.title = data.get('title', project.title)
    project.shortDescription = data.get('shortDescription', project.shortDescription)
    project.fullDescription = data.get('fullDescription', project.fullDescription)
    project.imageUrl = data.get('imageUrl', project.imageUrl)
    project.category = data.get('category', project.category)
    project.location = data.get('location', project.location)
    project.year = data.get('year', project.year)
    
    db.session.commit()
    return jsonify(project.to_dict())

# DELETE: Eliminar un proyecto
@app.route('/api/projects/<string:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    project = db.session.get(Project, project_id) # Usa db.session.get
    if project is None:
        return jsonify({"message": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200

# --- 5. Función para cargar datos iniciales directamente ---
def load_initial_data_direct():
    """
    Carga los datos iniciales de los proyectos directamente en la base de datos
    sin pasar por la API REST. Esto es para propósitos de inicialización en desarrollo.
    """
    initial_portfolio_items = [
        {
            "id": "res_depto_providencia",
            "title": "Departamento Luminoso en Providencia",
            "shortDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
            "fullDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quibusdam, accusamus! Earum ullam harum facere voluptas. Delectus ullam, nulla deleniti amet, porro deserunt expedita aperiam cupiditate ducimus distinctio vel dolorum magni.",
            "imageUrl": "https://i.ytimg.com/vi/z-ARZWQ2ccw/maxresdefault.jpg",
            "category": "Residencial",
            "location": "Providencia, Santiago",
            "year": 2023
        },
        {
            "id": "com_oficina_moderna",
            "title": "Oficina Colaborativa - Centro",
            "shortDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
            "fullDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quibusdam, accusamus! Earum ullam harum facere voluptas. Delectus ullam, nulla deleniti amet, porro deserunt expedita aperiam cupiditate ducimus distinctio vel dolorum magni.",
            "imageUrl": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "category": "Comercial",
            "location": "Santiago Centro, Santiago",
            "year": 2022
        },
        {
            "id": "rem_bano_minimalista",
            "title": "Remodelación Baño Minimalista",
            "shortDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
            "fullDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quibusdam, accusamus! Earum ullam harum facere voluptas. Delectus ullam, nulla deleniti amet, porro deserunt expedita aperiam cupiditate ducimus distinctio vel dolorum magni.",
            "imageUrl": "https://img.freepik.com/fotos-premium/bano-minimalista-moderno-impresionante-ducha-blanca-lujo-resolucion-4k-como-pieza-central_1189966-2709.jpg?w=1380",
            "category": "Remodelación",
            "location": "Vitacura, Santiago",
            "year": 2024
        },
        # !!! ES MUY IMPORTANTE QUE COPIES Y PEGUES AQUÍ EL RESTO DE TUS PROYECTOS DE portfolioItems.js !!!
        # Asegúrate de que la sintaxis de cada diccionario sea correcta (comas al final de cada par clave-valor,
        # excepto el último en cada diccionario, y sin comas extra al final de la URL si es el último campo).
    ]

    print("Cargando datos iniciales directamente en la base de datos...")
    for item_data in initial_portfolio_items:
        existing_project = db.session.get(Project, item_data['id'])
        if not existing_project:
            try:
                new_project = Project(
                    id=item_data['id'],
                    title=item_data['title'],
                    shortDescription=item_data['shortDescription'],
                    fullDescription=item_data['fullDescription'],
                    imageUrl=item_data['imageUrl'],
                    category=item_data['category'],
                    location=item_data['location'],
                    year=item_data['year']
                )
                db.session.add(new_project)
                db.session.commit()
                print(f"  [OK] Proyecto '{item_data['title']}' añadido.")
            except Exception as e:
                db.session.rollback()
                print(f"  [ERROR] No se pudo añadir '{item_data['title']}': {e}")
        else:
            print(f"  [INFO] Proyecto '{item_data['title']}' ya existe, saltando.")
    print("Carga de datos iniciales finalizada.")

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

from flask_jwt_extended import create_access_token

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

# --- 6. Ejecutar la Aplicación ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crea las tablas si no existen
        load_initial_data_direct() # ¡Llama a la función de carga de datos aquí!
    app.run(debug=True, port=5000)