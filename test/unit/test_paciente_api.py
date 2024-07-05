import pytest
from datetime import date
from logger import logger
from app import app, Session, Paciente


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            # inicializa o banco de dados
            Session().begin()
            yield client
            Session().rollback()
            Session().close()


def test_0_limpa(client):
    session = Session()
    cpf = "18866259055"
    paciente = session.query(Paciente).filter(Paciente.cpf == cpf).first()
    if paciente:
        session.delete(paciente)
    cpf = "12345678900"
    paciente = session.query(Paciente).filter(Paciente.cpf == cpf).first()
    if paciente:
        session.delete(paciente)
    cpf = "11111111111"
    paciente = session.query(Paciente).filter(Paciente.cpf == cpf).first()
    if paciente:
        session.delete(paciente)
    session.commit()
    paciente = session.query(Paciente).filter(Paciente.cpf == cpf).first()
    assert paciente is None


def test_1_get_pacientes_empty(client):
    response = client.get("/paciente")
    assert response.status_code == 200
    assert response.json == {"pacientes": []}


def test_2_add_paciente_success(client):
    data = {
        "cpf": 18866259055,
        "nome": "João da Silva",
        "data_nascimento": date.today(),
        "sexo": "M",
        "cep": 22775024,
        "numero": "100",
        "complemento": "Apto 1801",
        "telefone": 2121211234,
        "email": "teste@teste.com",
    }
    response = client.post("/paciente/18866259055", data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 200
    assert "cpf" in response.json
    assert response.json["cpf"] == data["cpf"]
    assert response.json["nome"] == data["nome"]


def test_3_get_pacientes_with_data(client):
    response = client.get("/paciente")
    assert response.status_code == 200
    assert "pacientes" in response.json
    assert len(response.json["pacientes"]) == 1
    assert response.json["pacientes"][0]["nome"] == "João da Silva"


def test_4_add_paciente_conflict(client):
    data = {
        "cpf": 18866259055,
        "nome": "João da Silva (Duplicado)",
        "data_nascimento": date.today(),
        "sexo": "M",
        "cep": 22775024,
        "numero": "100",
        "complemento": "Apto 1801",
        "telefone": 2121211234,
        "email": "teste@duplicado.com",
    }
    response = client.post("/paciente/18866259055", data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 409
    assert response.json == {"message": "Paciente de mesmo cpf já salvo na base :/"}


def test_5_get_paciente_not_found(client):
    cpf = "12345678900"
    response = client.get(f"/paciente/{cpf}")
    assert response.status_code == 404
    assert response.json == {"message": "Paciente não encontrado na base :/"}


def test_6_get_paciente_found(client):
    cpf = "18866259055"
    response = client.get(f"/paciente/{cpf}")
    assert response.status_code == 200
    assert "cpf" in response.json
    assert int(response.json["cpf"]) == int(cpf)
    assert response.json["nome"] == "João da Silva"


def test_7_update_paciente_not_found(client):
    cpf = "11111111111"
    data = {
        "cpf": cpf,
        "nome": "Paciente Não Existente",
        "data_nascimento": "2000-01-01",
        "sexo": "M",
        "cep": "12345678",
        "numero": "123",
        "complemento": "",
        "telefone": "123456789",
        "email": "naoexistente@teste.com",
    }
    response = client.put(f"/paciente/{cpf}", data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 404
    assert response.json == {"message": f"Paciente com CPF #'{cpf}' não encontrado."}


def test_8_update_paciente_success(client):
    cpf = "18866259055"
    data = {
        "cpf": cpf,
        "nome": "Paciente Atualizado",
        "data_nascimento": "2000-01-01",
        "sexo": "M",
        "cep": "12345678",
        "numero": "456",
        "complemento": "Apto 101",
        "telefone": "987654321",
        "email": "atualizado@teste.com",
    }
    response = client.put(f"/paciente/{cpf}", data=data, content_type='application/x-www-form-urlencoded')
    logger.debug(response)
    logger.debug(response.json)
    assert response.status_code == 200
    assert "cpf" in response.json
    assert int(response.json["cpf"]) == int(cpf)
    assert response.json["nome"] == data["nome"]
    assert response.json["numero"] == data["numero"]
    assert response.json["complemento"] == data["complemento"]
    assert int(response.json["telefone"]) == int(data["telefone"])
    assert response.json["email"] == data["email"]


def test_9_delete_paciente_not_found(client):
    cpf = "12345678900"
    response = client.delete(f"/paciente/{cpf}")
    assert response.status_code == 404
    assert response.json == {"message": "Paciente não encontrado na base :/"}


def test_10_delete_paciente_success(client):
    cpf = "18866259055"
    response = client.delete(f"/paciente/{cpf}")
    assert response.status_code == 200
    assert response.json == {
        "message": "Paciente removido com sucesso",
        "cpf": int(cpf),
    }

    # Verifica se o paciente foi realmente removido do banco de dados
    session = Session()
    paciente_deletado = session.query(Paciente).filter(Paciente.cpf == cpf).first()
    assert paciente_deletado is None
