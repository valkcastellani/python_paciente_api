# Descrição do MVP Clínicas

Este projeto foi criado com o objetivo de oferecer uma solução para a gestão da agenda de uma amiga fisioterapeuta. Desenvolvido como parte do currículo do curso de Pós-Graduação em Engenharia de Software da PUC-Rio, seu desenvolvimento inicial ocorreu no módulo de Desenvolvimento Full Stack Básico. Atualmente, o projeto inclui implementações realizadas para o módulo de Arquitetura de Software.

Este é o repositório da API de Pacientes do MVP de Clínicas. O MVP é dividido em quatro componentes principais: dois componentes internos e dois componentes externos.

![Diagrama do MVP](https://github.com/valkcastellani/mvp_clinica_frontend_react/blob/master/img/esquema_mvp.png)

## Componentes Internos

1.  **Frontend:**

    - Desenvolvido com React, TypeScript, PrimeReact, PrimeFlex e PrimeIcons.
    - Realiza a comunicação com o Auth0 para autenticação de usuários.
    - Após a autenticação, o frontend se conecta com a API de Pacientes.
    - Permite ao usuário:
      - Buscar todos os pacientes (GET).
      - Buscar um paciente específico pelo CPF (GET).
      - Deletar um paciente (DELETE).
      - Incluir um novo paciente (POST).
      - Alterar informações de um paciente (PUT).
    - Realiza consultas ao VIACEP para obter informações de endereço com base no CEP informado pelo usuário.

   Apesar de conseguir utilizar a API através de linha de comando ou algum aplicativo, o frontend deste MVP foi disponibilizado no endereço [https://github.com/valkcastellani/mvp_clinica_frontend_react](https://github.com/valkcastellani/mvp_clinica_frontend_react).


2.  **API de Pacientes:**

    - Desenvolvida com a linguagem Python e o framework web Flask.
    - Expõe endpoints para operações CRUD (Create, Read, Update, Delete) de pacientes.
    - Não inclui a autenticação do token do Auth0 por fins didáticos.
    - Nas consultas, a API também realiza chamadas ao VIACEP para retornar dados de endereço.
    - A documentação desta API é fornecida seguindo o padrão OpenAPI através do Swagger.

## Componentes Externos

1.  **Auth0:**

    - Responsável pela autenticação de usuários.
    - O frontend se comunica com este serviço para autenticar os usuários antes de permitir o acesso à API de Pacientes.

2.  **VIACEP:**

    - Serviço externo utilizado para obter informações de endereço com base no CEP.
    - Tanto o frontend quanto a API de Pacientes realizam chamadas a este serviço para obter dados de endereço.

## Fluxo da Aplicação

1.  O usuário acessa o frontend e é redirecionado para o Auth0 para autenticação.
2.  Após a autenticação, o frontend se conecta à API de Pacientes.
3.  O usuário pode realizar operações CRUD na API de Pacientes.
4.  Ao informar um CEP, o frontend consulta o VIACEP para obter os dados de endereço.
5.  A API de Pacientes também consulta o VIACEP ao retornar dados de endereço nas suas respostas.

---

# Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
pip3 install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta executar:

```
flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---

# Executando a API em Contêineres Docker

## Docker Build e Run

Para construir e executar uma imagem Docker a partir de um Dockerfile, siga os passos abaixo:

1. Construindo a imagem com Docker Build:

   Primeiro, navegue até o diretório onde está localizado o Dockerfile e execute o seguinte comando para construir a imagem:

   ```bash
   docker build -t python_paciente_api:latest .
   ```

   - **python_paciente_api** é o nome da imagem. Nesse caso, foi utilizado no nome da nossa API.
   - **latest** é a tag de identificação da versão da imagem. Nessa caso, foi utilizado latest, pois é a versão mais recente disponibilizada da API.
   - **.** indica que o Dockerfile está no diretório atual.

2. Iniciando a Imagem com Docker Run:

   Após construir a imagem, você pode iniciar um contêiner a partir dessa imagem com o comando:

   ```bash
   docker run -d -p 5000:5000 -v ./database:/app/database python_paciente_api:latest
   ```

   - **-d** inicia o contêiner em modo _detached_ (em segundo plano).
   - **-p 5000:5000** mapeia a porta do host para a porta do contêiner, no formato _porta-do-host:porta-do-contêiner_.
   - **-v ./database:/app/database** monta um volume (mapeando caminhos no formato _/caminho/no/host:/caminho/no/contêiner_), permitindo que dados sejam persistentes no diretório `./database` do host e `/app/database` do contêiner.
   - **python_paciente_api:latest** é a imagem que criamos com o comando _docker build_ no item 1, no format _nome-da-imagem:tag_.

3. Verificando o Contêiner em Execução:

   Para verificar se o contêiner está em execução, use:

   ```bash
   docker ps
   ```

   Ou

   ```bash
   docker container ls -a
   ```

   Isso mostrará uma lista dos contêineres em execução.

## Docker Compose

O Docker Compose simplifica a definição e execução de aplicativos Docker de múltiplos contêineres. Ele usa um arquivo docker-compose.yml para configurar os serviços da sua aplicação.

1. Criando e Iniciando os Serviços:

   Para construir e iniciar todos os serviços definidos no arquivo `docker-compose.yml`, use:

   ```bash
   docker-compose up --build -d
   ```

   - **--build** reconstrói as imagens se necessário.
   - **-d** inicia os contêineres em segundo plano (_detached mode_).

2. Parando os Serviços:

   Para parar e remover os contêineres definidos no arquivo `docker-compose.yml`, execute:

   ```bash
   docker-compose down
   ```

   Isso irá parar todos os contêineres e remover os recursos criados pelo _docker-compose up_.

---

# Testando a API de Pacientes com PyTest (Testes Unitários)

## Como Rodar os Testes

Para rodar os testes unitários da aplicação, siga os passos abaixo:

1. **Instale as dependências necessárias:**

   Certifique-se de que você possui o `pytest` instalado. Se não tiver, você pode instalá-lo utilizando o pip:

   ```bash
   pip3 install pytest
   ```

2. **Execute os testes:**

   Na raiz do seu projeto, execute o seguinte comando para rodar todos os testes:

   ```bash
   pytest
   ```

3. **Verifique os resultados:**

   O `pytest` exibirá os resultados dos testes no terminal. Cada teste que passar será marcado com um ponto (`.`), enquanto os testes que falharem serão detalhados com informações sobre os erros.

## Cobertura dos Testes

Os testes unitários cobrem as seguintes funcionalidades da API:

1. **Listagem de Pacientes (`GET /paciente`):**

   - Verifica se a rota retorna uma lista de pacientes quando existem pacientes cadastrados.
   - Verifica se a rota retorna uma lista vazia quando não existem pacientes cadastrados.

2. **Busca de Paciente por CPF (`GET /paciente/<cpf>`):**

   - Verifica se a rota retorna os dados do paciente corretamente quando o CPF existe no banco de dados.
   - Verifica se a rota retorna um erro 404 quando o CPF não é encontrado no banco de dados.

3. **Adição de Novo Paciente (`POST /paciente/<cpf>`):**

   - Verifica se um novo paciente é adicionado com sucesso.
   - Verifica se a rota retorna um erro 409 quando há duplicidade de CPF.

4. **Atualização de Paciente (`PUT /paciente/<cpf>`):**

   - Verifica se um paciente existente é atualizado com sucesso.
   - Verifica se a rota retorna um erro 404 quando o CPF não é encontrado no banco de dados.

5. **Deleção de Paciente (`DELETE /paciente/<cpf>`):**
   - Verifica se um paciente é deletado com sucesso.
   - Verifica se a rota retorna um erro 404 quando o CPF não é encontrado no banco de dados.

# Testando a API de Pacientes com Locust (Teste de Carga)

Este projeto inclui um arquivo de teste para realizar testes de carga na API usando o Locust. Siga as instruções abaixo para configurar e executar o teste.

## Pré-requisitos

Antes de começar, você precisa ter o Locust instalado. Você pode instalá-lo usando pip:

```bash
pip3 install locust
```

## Executando o teste de carga

O arquivo de teste está localizado na pasta `test` e seu nome é `load_test.py`. Para executar o teste de carga, siga os passos abaixo:

1.  Certifique-se de que a aplicação a ser testada está rodando no **`localhost`** na porta **`5000`**.
2.  Navegue até o diretório raiz do projeto:

```bash
cd caminho/para/o/projeto
```

3.  Execute o Locust apontando para o arquivo de teste:

```bash
locust -f test/load_test.py -H http://localhost:5000
```

4.  Abra o navegador e acesse o seguinte endereço para abrir a interface web do Locust:

```bash
http://localhost:8089
```

5.  Na interface web do Locust, configure o número de usuários simultâneos (Number of total users to simulate) e a taxa de geração de novos usuários (Spawn rate).
6.  Clique no botão "Start swarming" para iniciar o teste de carga.

### Configurações do `load_test.py`

O arquivo **`load_test.py`** contém a definição das tarefas que serão executadas durante o teste de carga. Você pode personalizar este arquivo para atender às necessidades específicas do seu teste.

### Analisando os resultados

Após iniciar o teste de carga, a interface web do Locust exibirá gráficos e estatísticas em tempo real, permitindo que você monitore o desempenho da sua API. Você pode usar essas informações para identificar possíveis gargalos e otimizar o desempenho da sua API.

---

# Contribuindo

Se você encontrar qualquer problema ou tiver sugestões para melhorar a API, os testes unitários, os testes de carga, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.
