from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from model.paciente import Paciente


class PacienteSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    cpf: int = 18866259055
    nome: str = "João da Silva"
    data_nascimento: date = date.today()
    sexo: str = "M"
    cep: int = 22775024
    endereco: str = "Avenida Ator José Wilker"
    telefone: int = 2121211234
    email: str = "teste@teste.com"


class PacienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no cpf do paciente.
    """
    cpf: int = 18866259055


class ListagemPacientesSchema(BaseModel):
    """ Define como uma listagem de pacientes será retornada.
    """
    pacientes: List[PacienteSchema]


def apresenta_pacientes(pacientes: List[Paciente]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append({
            "cpf": paciente.cpf,
            "nome": paciente.nome,
            "data_nascimento": paciente.data_nascimento,
            "cep": paciente.cep,
            "endereco": paciente.endereco,
            "telefone": paciente.telefone,
            "email": paciente.email,
            "data_insercao": paciente.data_insercao
        })

    return {"pacientes": result}


class PacienteViewSchema(BaseModel):
    """ Define como um paciente será retornado.
    """
    cpf: int = 18866259055
    nome: str = "João da Silva"
    data_nascimento: date = date.today()
    sexo: str = "M"
    cep: int = 22775024
    endereco: str = "Avenida Ator José Wilker"
    telefone: int = 2121211234
    email: str = "teste@teste.com"
    data_insercao: date = date.today()


class PacienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str


def apresenta_paciente(paciente: Paciente):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    return {
        "cpf": paciente.cpf,
        "nome": paciente.nome,
        "data_nascimento": paciente.data_nascimento,
        "cep": paciente.cep,
        "endereco": paciente.endereco,
        "telefone": paciente.telefone,
        "email": paciente.email,
        "data_insercao": paciente.data_insercao
    }
