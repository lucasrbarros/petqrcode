from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
import qrcode

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Adicione uma chave secreta para flashes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

# Rota inicial
@app.route('/')
def index():
    return redirect(url_for('cadastrar', pet_id=1))  # Redireciona para a tela de cadastro

# Rota para cadastro do pet
@app.route('/cadastrar/<int:pet_id>', methods=['GET', 'POST'])
def cadastrar(pet_id):
    pet = Pet.query.get(pet_id)
    
    # Verifica se o pet existe
    if pet is None:
        pet = Pet(
            id=pet_id,  # Define o ID do pet
            nome_pet='',
            nome_dono='',
            endereco='',
            telefone='',
            foto='',
            info_extra='',
            ativo=False
        )
    
    if pet.ativo:
        return redirect(url_for('perfil', pet_id=pet.id))  # Redireciona para o perfil se o pet estiver ativo.

    if request.method == 'POST':
        # Lógica para cadastrar ou atualizar o pet
        pet.nome_pet = request.form['nome_pet']
        pet.nome_dono = request.form['nome_dono']
        pet.endereco = request.form['endereco']
        pet.telefone = request.form['telefone']
        pet.foto = request.form['foto']
        pet.info_extra = request.form['info_extra']

        if not pet.id:  # Se não existir um pet com esse ID, cria um novo
            db.session.add(pet)  # Adiciona um novo pet
            flash('Cadastro realizado com sucesso! Aguarde a aprovação.')
            gerar_qr_code(pet.id)  # Gerar QR Code após cadastro
        else:
            flash('Perfil atualizado com sucesso!')

        db.session.commit()
        return redirect(url_for('perfil', pet_id=pet.id))
    
    return render_template('cadastrar.html', pet=pet)

# Rota para o perfil do pet
@app.route('/perfil/<int:pet_id>')
def perfil(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None or not pet.ativo:
        flash('Perfil não encontrado ou não ativo.')
        return redirect(url_for('cadastrar', pet_id=pet_id))
    return render_template('perfil.html', pet=pet)

# Rota administrativa para ativar o perfil do pet
@app.route('/admin/ativar/<int:pet_id>')
def ativar_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet:
        pet.ativo = True
        db.session.commit()
        flash('Perfil ativado com sucesso!')
        return redirect(url_for('perfil', pet_id=pet.id))  # Redireciona para o perfil após ativar
    return redirect(url_for('index'))  # Redireciona para o índice se o pet não existir

# Função para gerar QR Code
def gerar_qr_code(pet_id):
    url = f'http://127.0.0.1:5000/cadastrar/{pet_id}'
    img = qrcode.make(url)
    img.save(f'static/qrcodes/pet_{pet_id}.png')

if __name__ == '__main__':
    app.run(debug=True)
