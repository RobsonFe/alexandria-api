# API do Projeto Alexandria

## Descrição

API de gerenciamento de livros, autores e editoras, construída com Django e Django Rest Framework.

## Objetivo

- Fornecer uma interface RESTful relacionado a livros, autores e editoras. Funcionará como backend para um sistema de biblioteca ou livraria como rede social para usuários criarem suas listas de livros favoritos e interagirem uns com os outros.
- A ideia é criar uma plataforma onde os amantes de livros possam compartilhar suas opiniões, descobrir novos títulos e conectar-se com outros leitores.
- O projeto visa facilitar a gestão de uma coleção de livros, permitindo que os usuários adicionem, editem e removam livros, autores e editoras, além de fornecer funcionalidades para avaliação e recomendação de livros.
- O objetivo é criar uma comunidade de leitores engajada, onde os usuários possam compartilhar suas experiências literárias e encontrar inspiração para novas leituras.
- A API será projetada para ser escalável e fácil de usar, com uma documentação clara e exemplos de uso para desenvolvedores.
- A segurança e a privacidade dos dados dos usuários serão prioridades, garantindo que as informações pessoais sejam protegidas e que apenas usuários autorizados possam acessar determinadas funcionalidades.
- A API será desenvolvida com boas práticas de desenvolvimento de software, incluindo testes automatizados, controle de versão e integração contínua, para garantir a qualidade e a confiabilidade do código.

## Inspiração

- O nome alexandria é uma homenagem à antiga Biblioteca de Alexandria, que foi uma das maiores e mais importantes bibliotecas do mundo antigo. A biblioteca era conhecida por sua vasta coleção de livros e manuscritos, e por ser um centro de conhecimento e aprendizado.
- O projeto é inspirado no sistema de bibliotecas online, como o Goodreads, onde os usuários podem explorar livros, autores e editoras, criar listas de leitura e interagir com outros leitores.

## Tecnologias

- Python 3.14.2
- Django 5.2.6
- Django Rest Framework 3.16.1
- PostgreSQL/ psycopg2 2.9.10

## Como Instalar as dependencias do Projeto

- inicie Ambiente Virtual `venv`

```bash
python -m venv venv
```

**Ative o ambiente virtual**:

- No Windows (cmd.exe):

  ```sh
  venv\Scripts\activate.bat
  ```

- No Windows (PowerShell):

  ```sh
  venv\Scripts\Activate.ps1
  ```

- No Git Bash ou Linux/Mac:

  ```sh
  source venv/Scripts/activate
  ```

Para instalar todas as ferramentas necessárias, basta utilizar o `requirements.txt`.

```python
pip install -r requirements.txt
```
