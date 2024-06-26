# API do MVP de Clínicas

Este projeto surge com o propósito de oferecer uma solução para a gestão da agenda de uma amiga, fisioterapeuta. Concebido como parte integrante do currículo do curso de Pós-Graduação em Engenharia de Software da PUC-Rio, o desenvolvimento foi realizado como projeto do módulo de Desenvolvimento Full Stack Básico.

Utilizando a linguagem Python com o framework web Flask, este MVP visa proporcionar uma experiência exemplar no controle de pacientes, demonstrando de maneira clara e concisa as operações essenciais de um sistema CRUD (Create, Read, Update and Delete) no contexto do cadastro de pacientes via endpoints que podem ser consultados via documentação Swagger.

---

## Frontend do MVP de Clínicas

Apesar de conseguir utilizar a API através de linha de comando ou algum aplicativo, no âmbito deste MVP foi disponibilizado o frontend no endereço [https://github.com/valkcastellani/mvp_clinica_frontend](https://github.com/valkcastellani/mvp_clinica_frontend).

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.


# Testando a API de Pacientes com Locust

Este projeto inclui um arquivo de teste para realizar testes de carga na API usando o Locust. Siga as instruções abaixo para configurar e executar o teste.

## Pré-requisitos

Antes de começar, você precisa ter o Locust instalado. Você pode instalá-lo usando pip:

```bash
pip3 install locust
```

## Executando o teste de carga

O arquivo de teste está localizado na pasta `test` e seu nome é `load_test.py`. Para executar o teste de carga, siga os passos abaixo:

 1. Certifique-se de que a aplicação a ser testada está rodando no **`localhost`** na porta **`5000`**.
 2. Navegue até o diretório raiz do projeto: 
```bash
cd caminho/para/o/projeto
```
 3. Execute o Locust apontando para o arquivo de teste:
```bash
locust -f test/load_test.py -H http://localhost:5000
```
 4. Abra o navegador e acesse o seguinte endereço para abrir a interface web do Locust:
```bash
http://localhost:8089
```
 5. Na interface web do Locust, configure o número de usuários simultâneos (Number of total users to simulate) e a taxa de geração de novos usuários (Spawn rate).
 6. Clique no botão "Start swarming" para iniciar o teste de carga.

### Configurações do `load_test.py`

O arquivo **`load_test.py`** contém a definição das tarefas que serão executadas durante o teste de carga. Você pode personalizar este arquivo para atender às necessidades específicas do seu teste.

### Analisando os resultados

Após iniciar o teste de carga, a interface web do Locust exibirá gráficos e estatísticas em tempo real, permitindo que você monitore o desempenho da sua API. Você pode usar essas informações para identificar possíveis gargalos e otimizar o desempenho da sua API.

### Contribuindo

Se você encontrar qualquer problema ou tiver sugestões para melhorar os testes de carga, sinta-se à vontade para abrir uma issue ou enviar um pull request.
