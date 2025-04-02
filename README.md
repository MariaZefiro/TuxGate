# TuxGate

## Descrição

O **TuxGate - Gerenciador de Acesso SSH** é uma aplicação baseada em **PyQt6** que permite gerenciar conexões SSH de forma intuitiva e eficiente.
Com ele, é possível adicionar, editar e remover servidores SSH, além de se conectar rapidamente a qualquer um deles por meio de um terminal integrado.

## Funcionalidades
- Adicionar, editar e remover servidores SSH
- Filtrar servidores por nome ou IP
- Conectar-se a servidores SSH diretamente da interface
- Terminal embutido para interação com o servidor
- Alternar entre tema claro e escuro
- Suporte a autenticação com senha

## Requisitos

- Python 3.9+
- PyQt6

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/MariaZefiro/tuxgate.git
   cd tuxgate
   ```
2. Instale a aplicação:
   ```bash
   chmod +x ./install.sh
   ./install.sh
   ```

## Uso

1. Adicione servidores SSH clicando em "Adicionar Servidor".
2. Para se conectar, clique duas vezes em um servidor na lista.
3. Utilize o terminal embutido para interagir com o servidor.
4. Para sair, clique em "Fechar Conexão".

## Estrutura do Projeto
```
TUXGATE/
│── core/
│   ├── theme_manager.py  # Gerenciador de temas
│── resources/
│   ├── edit_white.svg    # Ícone de edição (tema escuro)
│   ├── edit.svg          # Ícone de edição
│   ├── logo.svg          # Ícone da aplicação 
│   ├── requirements.txt  # Dependências do projeto
│   ├── servers.json      # Lista de servidores salvos
│── ui/
│   ├── ssh_manager.py    # Arquivo principal 
│── install.sh             # Arquivo de instalação
│── main.py               # Arquivo de inicialização
│── README.md             # Este arquivo
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias! Para isso:

1. Fork este repositório.
2. Crie uma branch para sua funcionalidade (git checkout -b minha-feature).
3. Commit suas modificações (git commit -m 'Adiciona minha funcionalidade').
4. Envie para o branch principal (git push origin minha-feature).
5. Abra um Pull Request.


## Autor
- **Maria Zefiro** - https://github.com/MariaZefiro

## Licença
Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
