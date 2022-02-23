from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#TODO: Instancia de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/apiPython'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#TODO: Creando la tabla de categorias
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))
    
    #TODO: Constructor que inicia la función
    def __init__(self,cat_nom,cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp
        
db.create_all()

#TODO: Esquema de categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')


#TODO: Una sola Respuesta
categoria_schema = CategoriaSchema()

#TODO: Muchas respuestas
categorias_schema = CategoriaSchema(many=True)


#TODO: Metodo GET ##############################
@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#TODO: Metoho GET por ID #######################
@app.route('/categoria/<id>',methods=['GET'])
def get_categoria_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)

#TODO: Metodo POST #############################
@app.route('/insertar',methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    
    nuevoregistro = Categoria(cat_nom,cat_desp)
    
    db.session.add(nuevoregistro)
    db.session.commit()
    return categoria_schema.jsonify(nuevoregistro)

#TODO: Metodo PUT ##############################
@app.route('/modificar/<id>',methods=['PUT'])
def update_categoria(id):
    actualizarcategoria= Categoria.query.get(id)
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    
    actualizarcategoria.cat_nom = cat_nom
    actualizarcategoria.cat_desp = cat_desp
    
    db.session.commit()
    
    return categoria_schema.jsonify(actualizarcategoria)
    
#TODO: METODO DELETE ###########################
@app.route('/eliminar/<id>',methods=['DELETE'])
def delete_categoria(id):
    eliminarcategoria = Categoria.query.get(id)
    db.session.delete(eliminarcategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarcategoria)


#TODO:Mensaje de bienvenida
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido al tutorial API Rest Python'})

if __name__ == '__main__':
    app.run(debug=True)
