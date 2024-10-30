from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'seu_segredo_aqui'  # Altere para uma chave secreta segura

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_pet = db.Column(db.String(100), nullable=False)
    nome_dono = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    foto = db.Column(db.String(200), nullable=True)
    info_extra = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=False)

# Cria o banco de dados se não existir
if not os.path.exists('pets.db'):
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('cadastrar', pet_id=1))  # Redireciona para a tela de cadastro

@app.route('/cadastrar/<int:pet_id>', methods=['GET', 'POST'])
def cadastrar(pet_id):
    pet = Pet.query.get(pet_id)

    # Se o pet já existe, redireciona para o perfil
    if pet and pet.ativo:
        return redirect(url_for('perfil', pet_id=pet.id))

    if request.method == 'POST':
        foto = request.files['foto']
        filename = None

        if foto:
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if pet is None:
            # Cadastro de novo pet
            pet = Pet(
                nome_pet=request.form['nome_pet'],
                nome_dono=request.form['nome_dono'],
                endereco=request.form['endereco'],
                telefone=request.form['telefone'],
                foto=filename,
                info_extra=request.form['info_extra'],
                ativo=True  # O pet já fica ativo automaticamente
            )
            db.session.add(pet)
            db.session.commit()
        else:
            # Atualização do pet existente
            pet.nome_pet = request.form['nome_pet']
            pet.nome_dono = request.form['nome_dono']
            pet.endereco = request.form['endereco']
            pet.telefone = request.form['telefone']
            if filename:
                pet.foto = filename
            pet.info_extra = request.form['info_extra']
            db.session.commit()

        # Redireciona para o perfil do pet
        return redirect(url_for('perfil', pet_id=pet.id))

    return render_template('cadastrar.html', pet=pet)

@app.route('/perfil/<int:pet_id>')
def perfil(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None or not pet.ativo:
        flash('Perfil não encontrado ou não ativo.')
        return redirect(url_for('cadastrar', pet_id=pet_id))
    return render_template('perfil.html', pet=pet)

@app.route('/admin/ativar/<int:pet_id>')
def ativar_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet:
        pet.ativo = True
        db.session.commit()
        flash('Perfil ativado com sucesso!')
    return redirect(url_for('cadastrar', pet_id=pet_id))

if __name__ == '__main__':
    app.run(debug=True)
