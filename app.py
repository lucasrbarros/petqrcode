from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
import qrcode

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_pet = db.Column(db.String(100), nullable=False)
    nome_dono = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    foto = db.Column(db.String(200), nullable=True)
    info_extra = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=False)

# Criação do banco de dados, se não existir
if not os.path.exists('pets.db'):
    db.create_all()

# Rota para cadastrar ou redirecionar para perfil
@app.route('/cadastrar/<int:pet_id>', methods=['GET', 'POST'])
def cadastrar(pet_id):
    pet = Pet.query.get(pet_id)

    # Se o pet já estiver ativo, redireciona para o perfil
    if pet and pet.ativo:
        return redirect(url_for('perfil', pet_id=pet_id))

    if request.method == 'POST':
        # Se não existir, cria um novo pet
        if not pet:
            pet = Pet(
                nome_pet=request.form['nome_pet'],
                nome_dono=request.form['nome_dono'],
                endereco=request.form['endereco'],
                telefone=request.form['telefone'],
                foto=request.form.get('foto', ''),
                info_extra=request.form.get('info_extra', ''),
                ativo=True  # Ativa o pet no momento do cadastro
            )
            db.session.add(pet)
        else:
            # Se o pet existir, atualiza os dados
            pet.nome_pet = request.form['nome_pet']
            pet.nome_dono = request.form['nome_dono']
            pet.endereco = request.form['endereco']
            pet.telefone = request.form['telefone']
            pet.foto = request.form.get('foto', '')
            pet.info_extra = request.form.get('info_extra', '')
            pet.ativo = True  # Ativa o pet ao atualizar

        db.session.commit()  # Salva no banco
        gerar_qr_code(pet.id)  # Gera o QR Code
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('perfil', pet_id=pet.id))

    return render_template('cadastrar.html', pet=pet)

# Rota para exibir o perfil do pet
@app.route('/perfil/<int:pet_id>')
def perfil(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet or not pet.ativo:
        flash('Perfil não encontrado ou não ativo.')
        return redirect(url_for('cadastrar', pet_id=pet_id))
    return render_template('perfil.html', pet=pet)

# Função para gerar QR Code
def gerar_qr_code(pet_id):
    url = f'http://127.0.0.1:5000/perfil/{pet_id}'
    img = qrcode.make(url)
    img.save(f'static/qrcodes/pet_{pet_id}.png')

# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)
