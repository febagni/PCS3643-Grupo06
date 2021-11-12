# Resumo da funcionalidade do Bid Coin

O seguinte projeto em Django implementa o Bid Coin, um site que implementa um sistema de leilões online.

---

# Instalando as bibliotecas auxiliares
Para executar o aplicativo, precisamos de um único pacote Python "Django", ele foi construído e testado com a versão Django 2.x. Para instalá-lo, use o seguinte comando no prompt, entrando na pasta src, onde está o arquivo requirements.txt:

```bash
    pip3 install -r requirements.txt
```

Django 2 requer Python 3, se você precisar de ajuda para configurar Python 3 em sua máquina, você pode consultar a excelente documentação DigitalOcean sobre [Como instalar e configurar um ambiente de programação local para Python 3](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3).

# Setup do banco de dados

No projeto, está sendo usado MySQL (que deve estar rodando). Caso não tenha instalado o MySQL, recomenda-se seguir estes dois tutoriais:
- [MySQL CLI](https://docs.rackspace.com/support/how-to/install-mysql-server-on-the-ubuntu-operating-system/);
- [MySQL Workbench](https://www.edivaldobrito.com.br/como-instalar-o-instalar-mysql-workbench-no-ubuntu-e-derivados/).

Se estiver em um máquina com Ubuntu, o status do MySQL pode ser visto com o comando no terminal:
```bash
sudo systemctl status mysql
```

Para iniciar o MySQL, basta fazer:
```bash
sudo systemctl start mysql
```

Em seguida, deve-se criar um usuário e senha no MySQL CLI, que será usado. Basta seguir estes passos no terminal (trocar `YOUR_SYSTEM_USER` com o username desejado, e o `YOUR_PASSWD` pela senha):

```bash
sudo mysql -u root
```

```SQL
mysql> USE mysql;
mysql> CREATE USER 'YOUR_SYSTEM_USER'@'localhost' IDENTIFIED BY 'YOUR_PASSWD';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'YOUR_SYSTEM_USER'@'localhost';
mysql> UPDATE user SET plugin='caching_sha2_password' WHERE User='YOUR_SYSTEM_USER';
mysql> FLUSH PRIVILEGES;
mysql> exit;
```

```bash
sudo service mysql restart
```

Vale observar que é possível mudar as ocnfigurações de validação de senhas. Para isso, recomenda-se seguir este [link](https://stackoverflow.com/questions/43094726/your-password-does-not-satisfy-the-current-policy-requirements).


Com o MySQL rodando, pode-se abrir o MySQL Workbench e criar uma nova conexão. Nela, deve-se usar o `username` e `password` criados acima, o `hostname` é por padrão `127.0.0.1` e a `port`, por padrão, `3306`. Pode-se testar a conexão com o `Test Connection` e se estiver tudo certo. O setup da conexão do banco de dados foi feito de forma correta.

Assim, deve-se criar propriamente a base de dados com uma query dentro da conexão pelo próprio MySQL Workbench. Para tanto, basta utilizar o comando (onde [DB_NAME] é o nome do banco de dados):
```SQL
CREATE DATABASE [DB_NAME];
```
Ao rodar a query (botão de raio do MySQL Workbench), o banco de dados será criado.

Com isso, devem ser atualizadas as configurações de banco de dados no [`settings.py`](./apps/settings.py), como no exemplo:

```python
DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.mysql',
 'NAME': 'pcs3643g6',
 'USER': 'bidcoin',
 'PASSWORD': 'password',
 'HOST': 'localhost',
 'PORT': '3306',
 }
 } 
```

Alternativamente, é possível realizar a conexão com o MySQL no MySQL Workbench, utilizando credenciais já existentes ou criando uma conexão nova e um novo usuário com privilégios por meio do seguinte script:

```SQL
CREATE USER 'bidcoin'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON * . * TO 'bidcoin'@'localhost';

ALTER USER 'bidcoin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

Para o caso de utilização de credenciais já existentes, é necessária a modificação dos parâmetros do DATABASE em [`settings.py`](./apps/settings.py).



# Executando o aplicativo no localhost

Antes de executar o aplicativo, precisamos criar as tabelas de banco de dados necessárias:

```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
```

Agora você pode executar o servidor de desenvolvimento da web:

```bash
    python3 manage.py runserver
```

Para acessar no aplicativo vá para o URL <http://localhost:8000/>

---

# Criando e gerenciando contas

O BidCoin funciona com um sistema de permissões, onde podemos dividir as interações que um usuário comum consegue fazer e as páginas que consegue acessar no site com base em seu grupo. Superusuários tem permissão completa no site, incluindo a de criar outros usuários comuns e os atribuir à um ou mais grupos.

## Criando Superusuários
você pode criar um usuário usando o seguinte comando:

```bash
    python manage.py createsuperuser
```
Para criar um usuário normal (não superusuário), você deve fazer login na página de administração e criá-lo
: <http://localhost:8000/admin/>

## Criando os grupos de usuários para permissões por conta

Como dito anteriormente, seções do site estão bloqueadas para usuários sem a permissão de vê-los, isto se dá com grupos de autenticação e autorizção. No site, implementamos 3 deles, "auctioneer", "buyer" e "seller".

Cada um deles possui acessos diferentes às páginas do BidCoin, são elas:

- `"auctioneer"` Permissão de CRUD dos leilões criados, CRUD dos Lotes criados.

- `"seller"` CRUD de apenas os Lotes criados pelo próprio usuário.

- `"buyer"` Ainda não implementado métodos adicionais

O superusuário deve criar os grupos e designar as funções para que os outros usuários que não têm a permissão de administrador, isto pode ocorrer durante a sua criação ou posteriormente editando suas informações. Lembrando, para isso o Admin deve fazer login na página de administração: <http://localhost:8000/admin/>

Atenção, os grupos são case sensitive, ao criá-los, atente-se a escrever exatamente como acima.

---

# Testes com Selenium

Para a execução dos testes de interface com o Selenium, é preciso antes realizar sua instalação. O Selenium é uma extensão de navegadores responsável pela interação automatizada com interfaces de páginas web. No Google Chrome, basta procurar pela extensão Selenium IDE e adicioná-la ao navegador.

Concluída a instalação, a próxima etapa é a de abrir o Selenium IDE, criar um novo projeto e um nobo caso de testes e dar início à gravação de tela. Nessa gravação, o usuário realiza as interações com a interface que serão reproduzidas pela extensão na execução de testes.

Caso esse processo já tenha sido feito, basta abrir o arquivo referente aos casos de testes que possui o formato '.side'.

---