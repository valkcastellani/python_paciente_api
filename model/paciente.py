from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base     
#, Comentario


class Paciente(Base):
    __tablename__ = 'paciente'

    cpf = Column("pk_paciente", Integer, primary_key=True)
    nome = Column(String(50))
#    quantidade = Column(Integer)
#    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
#    comentarios = relationship("Comentario")

    def __init__(self, cpf:int, nome:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Paciente

        Arguments:
            nome: nome do paciente.
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
#        self.quantidade = quantidade
#        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

#    def adiciona_comentario(self, comentario:Comentario):
#        """ Adiciona um novo comentário ao Produto
#        """
#        self.comentarios.append(comentario)

