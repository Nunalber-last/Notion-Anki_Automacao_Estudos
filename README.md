# Integração Notion → Anki

Este projeto automatiza a criação de flashcards no **Anki** com base em dados armazenados em uma **base de dados do Notion**.  
As imagens também são baixadas automaticamente e enviadas para o Anki via **AnkiConnect**.

---

## Funcionalidades

- Conecta ao **Notion** via API.
- Extrai campos personalizados (como `titulo`, `frente`, `verso`, `imagem`, `data`).
- Faz **upload automático de imagens** para a pasta de mídia do Anki.
- Cria **notas no baralho Anki** usando o modelo especificado.
- Pode ser **agendado automaticamente** no Windows (via Agendador de Tarefas).

---

## Requisitos

### Softwares necessários
- [Python 3.10+](https://www.python.org/)
- [Anki](https://apps.ankiweb.net/)
- [AnkiConnect (código 2055492159)](https://ankiweb.net/shared/info/2055492159)
- [Notion API](https://developers.notion.com/)

### Bibliotecas Python
Instale os pacotes necessários:
```bash
pip install requests notion-client
```

## Configuração

Edite as variáveis no início do arquivo `main.py`:

```python
NOTION_API_KEY = "sua_chave_api_notion"
DATABASE_ID = "id_da_base_notion"
ANKI_CONNECT_URL = "http://localhost:8765"
```


## Estrutura esperada da base no Notion

A base de dados deve conter as seguintes colunas:
| Campo     | Tipo        | Descrição                              |
| --------- | ----------- | -------------------------------------- |
| titulo    | Título      | Nome ou identificação do card.         |
| frente    | Texto       | Texto exibido na frente do card.       |
| verso     | Texto       | Texto exibido no verso do card.        |
| imagem    | Arquivo/URL | Imagem associada ao card (opcional).   |
| data_prop | Data        | Data de criação ou revisão (opcional). |

## Modelo no Anki

Crie um modelo chamado "NotionBasic" no Anki com os seguintes campos:

- titulo  
- frente  
- verso  
- imagem  
- data  

Exemplo de template da frente:
```bash
<h2>{{titulo}}</h2>
<hr>
{{frente}}
{{imagem}}
```

Exemplo de template do verso:
```bash
{{FrontSide}}
<hr>
{{verso}}

```

##Execução automática (Windows)

Você pode agendar a execução automática do script via Agendador de Tarefas do Windows:
- Abra o Agendador de Tarefas.
- Clique em Criar Tarefa.
- Marque Executar mesmo que o usuário não esteja conectado.

No campo Ação, selecione:
```bash
Programa/script: python  O
Argumentos: "C:\caminho\para\main.py"
```

Configure o disparo (por exemplo, diariamente) e conclua ação. 
Depois de tudo configurado, você pode acionar manualmente o gatilho em Agendamento de tarefas para confirmar se está tudo funcionando.

💡 Dica: Habilite a opção de armazenar senha para o script rodar sem interrupções.

Sinta-se livre para sugerir melhorias, abrir issues ou enviar pull requests.
Este projeto é simples, mas poderoso para quem quer sincronizar o estudo entre Notion e Anki 🔁
