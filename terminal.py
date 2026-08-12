from cliente.cliente import fazer_request_tmdb, fazer_request_tmdb_sem_params
from dotenv import load_dotenv
import os
from database.database import engine, criar_banco_de_dados
from sqlmodel import Session, select, update
from modelos.modelos import Filme, Usuario, FilmeBase, UsuarioBase
from uuid import UUID
from seguranca import gerar_hash_senha, verificar_senha

load_dotenv()
def listar_generos():

    url_tmdb_genders = 'https://api.themoviedb.org/3/genre/movie/list'
    token = os.getenv("TMDB_TOKEN")
    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    lista_generos = []
    resposta = fazer_request_tmdb_sem_params(url=url_tmdb_genders, header=header)
    if resposta:
        print("Gêneros obtidos com sucesso!")
        for valores in resposta['genres']:
            lista_generos.append(valores['name'])
        return lista_generos

    else:
        print("Ocorreu um erro!")

def pesquisar_filme(nome_filme):

    url_tmdb_filmes = 'https://api.themoviedb.org/3/search/movie'
    token = os.getenv("TMDB_TOKEN")
    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "query": nome_filme,
        "language": "pt-BR"
    }
    resposta = fazer_request_tmdb(url=url_tmdb_filmes, params=params, header=header)
    if resposta and (resposta['total_results'] > 0):
        for resultado in resposta["results"]:
            if resultado['title'] == nome_filme:
                return {
                    "titulo": resultado['title'],
                    "nota_media": resultado['vote_average'],
                    "sinopse": resultado['overview'],
                    "popularidade": resultado['popularity'],
                    "ano": resultado["release_date"]
                }

    else:
        print("Nenhum filme encontrado!")

def adicionar_filme_banco_de_dados():

    nome_filme = input("Digite o nome do filme que você deseja adicionar: ").strip()
    dados = pesquisar_filme(nome_filme=nome_filme)
    if dados:
        try:
            with Session(engine) as session:
                add_filme = FilmeBase(**dados)
                querie_filme = session.exec(select(Filme).where(Filme.titulo == add_filme.titulo)).first()

                if not querie_filme:
                    session.add(Filme(**dados))
                    session.commit()
                    print("Filme adicionado com sucesso!")
                    
                elif add_filme.ano != querie_filme.ano:
                    session.add(Filme(**dados))
                    session.commit()
                    print("Filme adicionado com sucesso!")

                else:
                    print("Esse filme já existe no Banco de Dados!")
        except Exception:
            print("Não foi possível adicionar ao Banco de Dados")

def deleta_filme():

    uuid_hex = input("Digite a uuid do filme que você quer remover: ").strip()
    if uuid_hex:
        uuid_hex = UUID(uuid_hex)
        with Session(engine) as session:
            resultado = session.exec(select(Filme).where(Filme.uuid == uuid_hex))
            filme = resultado.one()
            session.delete(filme)
            session.commit()

def get_filme_sinopse():

    uuid_obj = input("Digite a uuid do filme que você quer verificar: ").strip()
    try:
        uuid_obj = UUID(uuid_obj)
        with Session(engine) as session:
            querie = session.exec(select(Filme.sinopse).where(Filme.uuid == uuid_obj))
            filme = querie.one()
            print(f"Filme encontrado -> {filme}")
            session.commit()
    except ValueError as error:
        print("O valor deve ser um uuid!")
        print(error)

def get_filme_completo():

    uuid_obj = input("Digite a uuid do filme que você quer verificar: ").strip()
    try:
        uuid_obj = UUID(uuid_obj)
        with Session(engine) as session:
            querie = session.exec(select(Filme).where(Filme.uuid == uuid_obj))
            filme = querie.one()
            print(f"Filme encontrado -> {filme}")
            session.commit()
    except ValueError as error:
        print("O valor deve ser um uuid!")
        print(error)

def atualizar_filme():
    uuid_filme = input("Digite o uuid do filme que deseja atualizar: ").strip()
    nota_media = input("Nota media: ").strip()
    sinopse = input("Sinopse: ").strip()
    popularidade = input("Popularidade: ").strip()
    ano = input("Ano: ").strip()

    payload = {}

    if nota_media:
        payload["nota_media"] = float(nota_media)

    if sinopse:
        payload["sinopse"] = sinopse

    if popularidade:
        payload["popularidade"] = float(popularidade)

    if ano:
        payload["ano"] = ano

    if not payload:
        print("Nenhum dado adicionado ao payload!")
        return

    try:
        uuid_filme = UUID(uuid_filme)
        with Session(engine) as session:
            filme_update = session.exec(update(Filme).where(Filme.uuid == uuid_filme).values(**payload))
            session.commit()
            if filme_update.rowcount > 0:
              print("Filme atualizado no banco de dados!")
            else:
              print("Nenhum filme encontrado com esse UUID!")

    except Exception as erro:
        print(erro)

def criar_usuario():
    print("="*20 + " CRIAR USUÁRIO " + "="*20)
    email = input("Digite um email válido: ").strip()
    username = input("Digite um nome de usuário: ").strip()
    senha = input("Digite uma senha válida: ")
    payload = {}

    if email:
        payload["email"] = email

    if username:
        payload["username"] = username

    if senha:
        senha_hash = gerar_hash_senha(senha_texto=senha)
        payload["senha"] = senha_hash

    if not payload:
        print("Nenhum dado sendo enviado...")
        return

    try:
        with Session(engine) as session:
            nome = UsuarioBase(**payload)
            query_nome = session.exec(select(Usuario).where(Usuario.username == nome.username)).first()
            if not query_nome:
                session.add(Usuario(**payload))
                session.commit()
                print("Usuário cadastrado com sucesso!")

            else:
                print("Usuário já existe")
    except ValueError as erro:
        print(f"Erro ao cadastrar usuário -> {erro}")

def fazer_login():
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    if not senha:
        print("Senha não digitada!")
        return

    elif not email:
        print("Email não digitado!")
        return

    try:
        with Session(engine) as session:
            check_email = session.exec(select(Usuario).where(Usuario.email == email)).first()
            if check_email:
                if verificar_senha(senha, check_email.senha):
                    print("Login realizado com sucesso!")
                    return check_email
                else:
                    return "Email ou senha incorretos!"
            return "Email não encontrado!"
    except Exception as erro:
        print(f"Erro -> {erro}")
        return None
    
criar_banco_de_dados()
    


def menu():
    while True:
        print('='*25 + " TERMINAL " + '='*25)
        print('1. Adicionar filme ao banco de dados')
        print('2. Pesquisar filme')
        print('3. Deletar um filme')
        print('4. Procurar sinopse de um filme no banco de dados')
        print('5. Atualizar um filme')
        print('6. Fazer Login')
        print('7. Não tem uma conta ainda? Crie uma aqui!')
        print('0. Sair')
        print('='*25 + " ======== " + '='*25)

        escolha = input("Escolha o que deseja fazer: ")

        if escolha == '1':
            adicionar_filme_banco_de_dados()

        elif escolha == '2':
            film = input("Digite o nome do filme a ser pesquisado: ").strip()
            dados = pesquisar_filme(film)
            print(dados)

        elif escolha == '3':
            deleta_filme()

        elif escolha == '4':
            get_filme_sinopse()

        elif escolha == '5':
            atualizar_filme()

        elif escolha == '6':
            fazer_login()

        elif escolha == '7':
            criar_usuario()

        else:
            break

if __name__=="__main__":
    menu()

    