PetQRCode - Sistema de Cadastro de Pets 🐾
Este projeto é uma aplicação web para cadastro e gestão de informações de pets. O sistema permite cadastrar, visualizar perfis e editar informações dos pets, tudo isso em uma interface simples e estilizada. O backend é desenvolvido com Flask, utilizando SQLite como banco de dados.

Estrutura do Projeto

📁 petqrcode/
│
├── 📂 static/
│   ├── 📂 css/
│   │   └── styles.css   # Estilos personalizados
│   └── 📂 uploads/      # Imagens dos pets (enviadas pelo usuário)
│
├── 📂 templates/
│   ├── cadastrar.html   # Página de cadastro do pet
│   ├── perfil.html      # Página de perfil do pet
│   └── admin.html       # Área administrativa para listar cadastros
│
├── app.py               # Arquivo principal do backend (Flask)
├── pets.db              # Banco de dados SQLite
└── README.md            # Instruções para rodar o projeto

*Pré-requisitos*
Antes de rodar o projeto, você precisará ter o seguinte instalado em sua máquina:

Python 3.8+: Instalar Python
Pip: Vem com a instalação do Python
Virtualenv (opcional, mas recomendado):


```pip install virtualenv```

Instruções para Rodar o Projeto
1. Clonar o Repositório
Abra o terminal e clone o repositório do projeto:



```
git clone <URL_DO_REPOSITORIO>
cd petqrcode
```

2. Criar Ambiente Virtual (Opcional)

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar Dependências
Execute o comando abaixo para instalar as dependências necessárias:

```
pip install -r requirements.txt
```

Dependências principais:

Flask
Flask-SQLAlchemy

Se você não tiver o arquivo requirements.txt, instale manualmente:

```pip install Flask Flask-SQLAlchemy```

4. Configurar Diretórios
Crie os diretórios necessários para as imagens e o banco de dados:

```mkdir static/uploads```
5. Inicializar o Banco de Dados
Se ainda não existir o banco de dados pets.db, crie-o executando o comando:

```
>>> from app import db
>>> db.create_all()
>>> exit()
```

6. Executar o Servidor
Agora, rode o servidor Flask:


```python app.py```

O servidor estará disponível em http://127.0.0.1:5000.

7. Funcionalidades do Sistema
Cadastro: Preencher informações do pet e anexar uma foto.
Perfil do Pet: Exibe detalhes do pet cadastrado.
Edição: Permite alterar as informações de um pet.
Área Administrativa: Lista todos os pets cadastrados.
Problemas Conhecidos
Certifique-se de que o diretório static/uploads/ tem permissões corretas para salvar imagens.
Use versões compatíveis do Flask-SQLAlchemy e SQLAlchemy para evitar erros de importação.
Tecnologias Utilizadas
Python: Linguagem de programação.
Flask: Framework web.
SQLite: Banco de dados leve e embutido.
HTML/CSS: Estrutura e design das páginas.
Contribuições
Sinta-se à vontade para contribuir com melhorias para o projeto. Crie um fork e envie seu pull request!

Licença
Este projeto é de uso livre sob a licença MIT.

Contato
Caso tenha dúvidas ou sugestões, entre em contato:

Desenvolvedor: Lucas Barros
Email: lucasrbarros9@gmail.com