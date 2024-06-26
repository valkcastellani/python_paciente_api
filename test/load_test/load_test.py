from locust import HttpUser, between, task


class LoadTest(HttpUser):
    """
    Configurando um teste de carga com o Locust
    """

    wait_time = between(1, 3)

    @task
    def add_paciente(self):
        """Fazendo a inserção de pacientes aleatórios."""

        # criando o paciente
        paciente = {
            "cpf": "18866259055",
            "nome": "João da Silva",
            "data_nascimento": str(date.today()),
            "sexo": "M",
            "cep": "22775024",
            "endereco": "Avenida Ator José Wilker",
            "telefone": "2121211234",
            "email": "teste@teste.com",
        }

        # configurando a requisição
        headers = {"Content-Type": "multipart/form-data"}
        response = self.client.post("/paciente", data=paciente, headers=headers)

        # verificando a resposta
        data_response = response.json()
        if response.status_code == 200:
            print("Paciente %s salvo na base" % paciente["nome"])
        elif response.status_code == 409:
            print(data_response["mesage"] + paciente["nome"])
        else:
            print("Falha na rota de inclusão de um paciente")

    @task
    def listagem(self):
        """
        Fazendo uma listagem dos items salvos.
        """
        # configurando a requisição
        response = self.client.get("/paciente")

        # verificando a resposta
        data = response.json()
        if response.status_code == 200:
            print("Total de items salvos: %d" % len(data["pacientes"]))
        else:
            print("Falha na rota /paciente")

    @task
    def get_paciente(self):
        """
        Fazendo uma busca pelo paciente de cpf 18866259055.
        """

        # configurando a requisição
        response = self.client.get("/paciente/18866259055")

        # verificando a resposta
        data = response.json()
        if response.status_code == 200:
            print("Paciente visitado: %s" % data["nome"])
        else:
            print("Falha na rota /paciente/18866259055")
