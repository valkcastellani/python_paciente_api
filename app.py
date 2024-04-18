from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente
from logger import logger
from schemas import *
from flask_cors import CORS

from datetime import datetime

info = Info(title="Pacientes API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Documentação: Swagger")
paciente_tag = Tag(
    name="Paciente", description="Adição, Alteração, visualização e remoção de pacientes à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, apresentando assim a documentação criada pelo Swagger.
    """
    return redirect('/openapi/swagger')


@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_paciente(form: PacienteSchema):
    """Adiciona um novo Paciente à base de dados

    Retorna uma representação do paciente.
    """
    paciente = Paciente(
        cpf=form.cpf,
        nome=form.nome,
        data_nascimento=form.data_nascimento,
        sexo=form.sexo,
        cep=form.cep,
        endereco=form.endereco,
        telefone=form.telefone,
        email=form.email
    )
    logger.debug(f"Adicionando paciente de nome: '{paciente.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando paciente
        session.add(paciente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado paciente de nome: '{paciente.nome}'")
        return apresenta_paciente(paciente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Paciente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
        return {"message": error_msg}, 400


# @app.put('/paciente', tags=[paciente_tag],
#           responses={"200": PacienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
# def alter_paciente(form: PacienteSchema):
#     """Altera os dados de um Paciente na base de dados

#     Retorna uma representação do paciente.
#     """
#     cpf_paciente = form.cpf
#     logger.debug(f"Coletando dados sobre paciente de CPF #{cpf_paciente}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     paciente_to_update = session.query(Paciente).filter(Paciente.cpf == cpf_paciente).first();
#     if (paciente_to_update): 
#         try:
#             # alterando paciente
#             paciente = session.scalars(paciente_to_update).one();
#             paciente.nome=form.nome,
#             paciente.data_nascimento=form.data_nascimento,
#             paciente.sexo=form.sexo,
#             paciente.cep=form.cep,
#             paciente.endereco=form.endereco,
#             paciente.telefone=form.telefone,
#             paciente.email=form.email
        
#             logger.debug(f"Alterando paciente de nome: '{paciente.nome}'")
#             # efetivando a alteração do paciente na tabela
#             session.commit()
#             logger.debug(f"paciente de nome: '{paciente.nome}' alterado.")
#             return apresenta_paciente(paciente), 200

#         except IntegrityError as e:
#             # como a duplicidade do nome é a provável razão do IntegrityError
#             error_msg = "Paciente de mesmo nome já salvo na base :/"
#             logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
#             return {"message": error_msg}, 409

#         except Exception as e:
#             # caso um erro fora do previsto
#             error_msg = "Não foi possível salvar novo item :/"
#             logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
#             return {"message": error_msg}, 400
#     else:
#         # caso um erro fora do previsto
#         error_msg = "Não foi possível alterar os dados do paciente :/"
#         logger.warning(f"Erro ao alterar o paciente '{paciente.nome}', {error_msg}")
#         return {"message": error_msg}, 400

@app.put('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def atualizar_paciente(form: PacienteSchema):
    """Atualiza um Paciente existente na base de dados.

    O paciente a ser atualizado é identificado pelo 'paciente_cpf' na URL.
    A representação atualizada do paciente é retornada.
    """

    # criando conexão com a base
    session = Session()
    paciente = session.query(Paciente).filter(Paciente.cpf == form.cpf).first();

    if not paciente:
        # Paciente não encontrado
        return {"message": f"Paciente com CPF #'{form.cpf}' não encontrado."}, 404

    # Atualizando os campos do paciente
    paciente.cpf = form.cpf
    paciente.nome = form.nome
    paciente.data_nascimento = form.data_nascimento
    paciente.sexo = form.sexo
    paciente.cep = form.cep
    paciente.endereco = form.endereco
    paciente.telefone = form.telefone
    paciente.email = form.email

    logger.debug(f"Atualizando paciente de CPF #'{paciente.cpf}'")

    try:
        # efetivando a atualização do paciente
        session.commit()
        logger.debug(f"Paciente de CPF #'{paciente.cpf}' atualizado com sucesso.")
        return apresenta_paciente(paciente), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar o paciente."
        logger.warning(f"Erro ao atualizar paciente de CPF #'{paciente.cpf}', {error_msg}")
        return {"message": error_msg}, 400
        

@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": ListagemPacientesSchema, "404": ErrorSchema})
def get_pacientes():
    """Faz a busca por todos os Paciente cadastrados

    Retorna uma representação da listagem de pacientes.
    """
    logger.debug(f"Coletando pacientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pacientes = session.query(Paciente).all()

    if not pacientes:
        # se não há pacientes cadastrados
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d Pacientes encontrados" % len(pacientes))
        # retorna a representação de paciente
        print(pacientes)
        return apresenta_pacientes(pacientes), 200


@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Faz a busca por um Paciente a partir do id do paciente

    Retorna uma representação dos pacientes e comentários associados.
    """
    cpf_paciente = query.cpf
    logger.debug(f"Coletando dados sobre paciente de CPF #{cpf_paciente}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.cpf == cpf_paciente).first()

    if not paciente:
        # se o paciente não foi encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao buscar paciente de CPF #'{cpf_paciente}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Paciente encontrado: '{paciente.nome}'")
        # retorna a representação de paciente
        return apresenta_paciente(paciente), 200


@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteDelSchema, "404": ErrorSchema})
def del_paciente(query: PacienteBuscaSchema):
    """Deleta um Paciente a partir do cpf informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cpf_paciente = query.cpf
    logger.debug(f"Deletando dados do paciente de cpf #{cpf_paciente}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Paciente).filter(Paciente.cpf == cpf_paciente).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Paciente deletetado. CPF #{cpf_paciente}")
        return {"message": "Paciente removido com sucesso", "cpf": cpf_paciente}
    else:
        # se o paciente não foi encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar o paciente de CPF #'{cpf_paciente}', {error_msg}")
        return {"message": error_msg}, 404
