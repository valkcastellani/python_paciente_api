from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Paciente(Base):
    __tablename__ = 'paciente'

    cpf = Column("pk_paciente", Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    sexo = Column(String(1))
    cep = Column(Integer)
    endereco = Column(String(200))
    telefone = Column(Integer)
    email = Column(String(50))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, cpf: int, nome: str, data_nascimento: DateTime,
                 sexo: str, cep: int, endereco: str, telefone: int,
                 email: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria um Paciente

        Arguments:
            cpf: Número do CPF
            nome: Nome do Paciente
            data_nascimento: Data de Nascimento do Paciente
            sexo: Sexo declarado do Paciente
            cep: Cep do endereço do Paciente
            endereco: Endereço do Paciente
            telefone: Telefone do Paciente
            email: Email do Paciente
            data_insercao: data de quando o paciente foi inserido à base
        """
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.cep = cep
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
