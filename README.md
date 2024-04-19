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
