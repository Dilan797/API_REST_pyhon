from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu-resturant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Añadido para evitar warnings

#Create SQLAlchemy instance
db = SQLAlchemy(app)

#Modelo que define la estructura de la base de datos,
#especificamente una fila de menú de un restaurante.
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
#Metodo para inicializar la base de datos.
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }


with app.app_context():
    # Create the database tables
    db.create_all()



#Create Routes
#Esta parte del código define las rutas de la aplicación web.
@app.route('/')
def home():
    return jsonify({"perra":"Hello, Grandisimo conchaetumadre!"})


#Creamos una ruta para obtener todos los elementos del menú.
@app.route('/menu', methods=['GET'])
def get_menu():
    menu_items = MenuItem.query.all()
    #Devolvemos los datos en formato JSON.
    return jsonify([item.to_dict() for item in menu_items])

#Consultar un elemento del menú por su ID.
@app.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        return jsonify(item.to_dict())
    else:
        return jsonify({"error": "Item not found"}), 404
    

#Solicitud de publicación para agregar un nuevo elemento al menú.
@app.route('/menu', methods=['POST'])
def add_menu_item():
    data = request.get_json()#Toma los datos y los analiza.
    
    #Creamos un nuevo objeto
    new_item = MenuItem(name=data['name'],
                        description=data.get('description', ''),
                        price=data['price'])
    
    db.session.add(new_item)  # Agrega el nuevo elemento a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return jsonify(new_item.to_dict()), 201

#Usamos PUT para actualizar un elemento del menú.
@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    data = request.get_json()
    
    item = MenuItem.query.get(item_id)
    if item:
        item.name = data.get('name', item.name)  # CORREGIDO: era data.get['name']
        item.description = data.get('description', item.description)
        item.price = data.get('price', item.price)  # CORREGIDO: era data.get['price']
        
        db.session.commit()
        return jsonify(item.to_dict())
    else:
        return jsonify({"error": "Item not found"}), 404
    
#Usamos DELETE para eliminar un elemento del menú.
@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({"message":"Item deleted succesfully"}), 200
    else: 
        return jsonify({"error": "Item not found"}), 404
        
    
    
    
    
# Se actualiza la base de datos
if __name__ == "__main__":
    app.run(debug=True)



