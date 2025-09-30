# API do Projeto Alexandria

## Descrição: 
API de gerenciamento de livros, autores e editoras, construída com Django e Django Rest Framework. 

## Tecnologias: 

- Python 3.14.2
- Django 5.2.4
- Django Rest Framework 3.16.0
- PostgreSQL/ psycopg2 2.9.10
- decouple / envs 3.8

## Como Instalar as dependencias do Projeto ?

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