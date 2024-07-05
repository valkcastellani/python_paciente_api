from pydantic import BaseModel
from typing import List
from datetime import date
from model.paciente import Paciente
import requests


class PacienteSchema(BaseModel):
    """
    Define como um novo paciente a ser inserido deve ser representado
    """

    cpf: int = 18866259055
    nome: str = "João da Silva"
    data_nascimento: date = date.today()
    sexo: str = "M"
    cep: int = 22775024
    numero: str = "100"
    complemento: str = "Apto 1801"
    telefone: int = 2121211234
    email: str = "teste@teste.com"


class PacienteBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no cpf do paciente.
    """

    cpf: int = 18866259055


class PacienteSchemaComEndereco(BaseModel):
    """
    Define como um novo paciente a ser inserido deve ser representado
    """

    cpf: int = 18866259055
    nome: str = "João da Silva"
    data_nascimento: date = date.today()
    sexo: str = "M"
    cep: int = 22775024
    numero: str = "100"
    complemento: str = "Apto 1801"
    telefone: int = 2121211234
    email: str = "teste@teste.com"
    endereco: str = ""


class ListagemPacientesSchema(BaseModel):
    """
    Define como uma listagem de pacientes será retornada.
    """

    pacientes: List[PacienteSchemaComEndereco]


def apresenta_pacientes(pacientes: List[Paciente]):
    """
    Retorna uma representação do paciente seguindo o schema definido em PacienteViewSchema.
    """

    result = []
    for paciente in pacientes:
        endereco = busca_endereco_paciente(paciente)
        result.append(
            {
                "cpf": paciente.cpf,
                "nome": paciente.nome,
                "data_nascimento": paciente.data_nascimento,
                "sexo": paciente.sexo,
                "cep": paciente.cep,
                "numero": paciente.numero,
                "complemento": paciente.complemento,
                "telefone": paciente.telefone,
                "email": paciente.email,
                "data_insercao": paciente.data_insercao,
                "endereco": endereco,
            }
        )

    return {"pacientes": result}


class PacienteViewSchema(BaseModel):
    """
    Define como um paciente será retornado.
    """

    cpf: int = 18866259055
    nome: str = "João da Silva"
    data_nascimento: date = date.today()
    sexo: str = "M"
    cep: int = 22775024
    numero: str = "100"
    complemento: str = "Apto 1801"
    telefone: int = 2121211234
    email: str = "teste@teste.com"
    data_insercao: date = date.today()


class PacienteDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """

    message: str
    nome: str


def apresenta_paciente(paciente: Paciente):
    """
    Retorna uma representação do paciente seguindo o schema definido em PacienteViewSchema.
    """

    return {
        "cpf": paciente.cpf,
        "nome": paciente.nome,
        "data_nascimento": paciente.data_nascimento,
        "sexo": paciente.sexo,
        "cep": paciente.cep,
        "numero": paciente.numero,
        "complemento": paciente.complemento,
        "telefone": paciente.telefone,
        "email": paciente.email,
        "data_insercao": paciente.data_insercao,
    }


def busca_endereco_paciente(paciente: Paciente):
    api_externa = f"https://viacep.com.br/ws/{paciente.cep}/json/"

    try:
        response = requests.get(api_externa)

        if response.status_code == 200:
            data = response.json()
            if "erro" in data:
                return ""
            endereco = (
                f"{data.get('logradouro')}, {paciente.numero}, {paciente.complemento}, "
                f"{data.get('bairro')}, {data.get('localidade')} - {data.get('uf')} - {data.get('cep')}"
            )
            return endereco
        else:
            return ""

    except:
        return ""