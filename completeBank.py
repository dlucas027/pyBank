import textwrap  # Formatação de blocos de texto, quebra de linhas automática
from abc import ABC, abstractmethod  # Para criar classes e métodos abstratos
from datetime import datetime  # Para lidar com data e hora

class Cliente:          #Criação da classe cliente
    def __init__(self, endereco):   
        self.endereco = endereco     #Armazena o endereço
        self.contas = []           #Lista as contas associadas 
    def realizar_transacao(self, conta, transacao):   #objeto transação, que possui os métodos registrar e adicionar conta
        transacao.registrar(conta)  # Executa o método registrar da transação, passando a conta como parâmetro

    def adicionar_conta(self, conta):
        self.contas.append(conta) # Adiciona uma nova conta à lista de contas do cliente


class PessoaFisica(Cliente):   #classe Pessoa Física filha **HERDA** da classe Cliente (Tem tudo que a classe cliente tem e ainda pode add+ coisas)
    def __init__(self, nome, data_nascimento, cpf, endereco): #Método construtor com os parâmetros do cliente
        super().__init__(endereco)   #super(). chama a classe pai sem precisar reescrever e já define o endereço
        self.nome = nome
        self.data_nascimento = data_nascimento  #atributos do objeto criado a partir da classe cliente
        self.cpf = cpf


class Conta:    #Nova classe CONTA BANCÁRIA
    def __init__(self, numero, cliente): #Construtor da classe, inicializa o "objeto" conta
        self._saldo = 0
        self._numero = numero   #número de conta passado no momento da criação (_numero)
        self._agencia = "0001"
        self._cliente = cliente   #objeto da classe cliente, isso estabelece uma relação de 1 para 1: cada conta tem um cliente.
        self._historico = Historico()   #cada conta recebe um objeto da classe histórico, responsável por armazenar as transações

    @classmethod  #Decorador que permite deifinir um método que pertence somente a classe
    def nova_conta(cls, cliente, numero): #Função de classe, cria uma nova instância da classe Conta
        return cls(numero, cliente) #Referencia a própria classe , para criar um novo objeto usando o contrutor da classe Conta

    @property   #Decorador usado para criar propriedade, usado para permitir acesso simples aos atributos
    def saldo(self): #Permite acessar conta1.saldo como se fosse uma váriavel
        return self._saldo

    @property   
    def numero(self):  #Permissão para acessar os atributos sem chamar a função e métodos explicitamente
        return self._numero

    @property
    def agencia(self):  #Permissão para acessar os atributos sem chamar a função e métodos explicitamente
        return self._agencia

    @property
    def cliente(self):  #Permissão para acessar os atributos sem chamar a função e métodos explicitamente
        return self._cliente

    @property
    def historico(self):  #Permissão para acessar os atributos sem chamar a função e métodos explicitamente
        return self._historico

    def sacar(self, valor):    # Método da classe Conta que recebe o valor a ser sacado
        saldo = self.saldo    # Acessa o saldo da conta através da propriedade saldo
        excedeu_saldo = valor > saldo  # Verifica se o valor de saque é maior que o saldo disponível
        if excedeu_saldo: # Caso o valor do saque seja maior que o saldo
            print("\n Operação falhou! Você não tem saldo suficiente.") # Mensagem de erro

        elif valor > 0:  #se for menor ou = 0 exibe erro
            self._saldo -= valor     #se valor for positivo, reduz do saldo do cliente
            print("\n=== Saque realizado com sucesso! ===")
            return True   #True se for bem sucedida

        else:
            print("\n Operação falhou! O valor informado é inválido.")

        return False  #False se falhar 

    def depositar(self, valor):  #função para depositar, parâmetro valor dessa vez usado para adicionar 
        if valor > 0:
            self._saldo += valor #se maior que zero, adiciona ao saldo
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n Operação falhou! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta):  # ContaCorrente é uma classe que herda da classe Conta
    def __init__(self, numero, cliente, limite=5000, limite_saques=10): # Construtor da ContaCorrente
        super().__init__(numero, cliente)  # Chama o construtor da classe pai (Conta)e os atributos sem precisar reescrever
        self._limite = limite   # Define o limite para a conta corrente (default é 5000)
        self._limite_saques = limite_saques  # Define o número máximo de saques (default é 10)

    def sacar(self, valor):   # Método para sacar dinheiro, substitui o método da classe Conta
        numero_saques = len(   # Conta o número de saques realizados verificando as transações do histórico
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]   #for transacao in self.historico.transacoes percorre todas transações realizadas até agora
        )  # Percorre todas as transações no histórico, contando quantos saques (transações do tipo Saque) foram feitos
    

        excedeu_limite = valor > self._limite   # Verifica se o valor do saque excede o limite da conta
        excedeu_saques = numero_saques >= self._limite_saques # Verifica se o número de saques já ultrapassou o limite permitido

        if excedeu_limite: #Resultados da comparação anterior
            print("\n Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\n Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)  # Chama o método sacar da classe pai (Conta), que já realiza o saque 

        return False  # Retorna False se o saque não foi permitido (limite ou número de saques excedido)

    def __str__(self): #Método de instancia, pertencente a classe ContaCorrente, vai imprimir em string, agencia, numero e nome
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico: #Nova classe Historico
    def __init__(self):   # Inicializa o objeto Historico, criando uma lista vazia para armazenar transações
        self._transacoes = []

    @property
    def transacoes(self):  # Getter para a propriedade 'transacoes', que retorna a lista de transações
        return self._transacoes   #Acesso controlado a lista de transações

    def adicionar_transacao(self, transacao):  # Método para adicionar uma nova transação ao histórico, objeto transacao representa uma transação coo saque ou deposito
        self._transacoes.append(    # Adiciona a transação no final da lista '_transacoes', que armazena todas as transações realizadas
            # Cria um dicionário com os detalhes da transação:
            {
                "tipo": transacao.__class__.__name__,  # O tipo da transação é o nome da classe da transação (ex: 'Saque', 'Deposito', etc.)
                "valor": transacao.valor,  # O valor da transação, acessando o atributo 'valor' do objeto transacao (o valor do saque ou depósito)
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),  # A data e hora da transação, formatada como dia-mês-ano hora:minuto:segundo
            }
        )


class Transacao(ABC):# Define a propriedade valor como abstrata. 
    # Isso significa que qualquer classe filha precisa implementar essa propriedade.
    @property
    @abstractmethod  # Usando @abstractmethod para declarar o método abstrato de valor
    def valor(self):
        pass

    # Método abstrato registrar que precisa ser implementado nas classes filhas.
    # Este método será responsável por registrar uma transação na conta.
    @abstractmethod  # Usando @abstractmethod para registrar a transação
    def registrar(self, conta):
        pass


class Saque(Transacao):
    # Construtor da classe Saque, que inicializa o valor do saque.
    def __init__(self, valor):
        self._valor = valor  # Armazena o valor do saque

    # Propriedade 'valor' que retorna o valor do saque.
    @property
    def valor(self):
        return self._valor

    # Método que registra a transação de saque na conta.
    # Verifica se o saque pode ser realizado e, em caso afirmativo, adiciona a transação ao histórico da conta.
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)  # Tenta realizar o saque

        if sucesso_transacao:  # Se o saque for bem-sucedido
            conta.historico.adicionar_transacao(self)  # Adiciona a transação ao histórico da conta


class Deposito(Transacao):
    # Construtor da classe Deposito, que inicializa o valor do depósito.
    def __init__(self, valor):
        self._valor = valor  # Armazena o valor do depósito

    # Propriedade 'valor' que retorna o valor do depósito.
    @property
    def valor(self):
        return self._valor

    # Método que registra a transação de depósito na conta.
    # Verifica se o depósito pode ser realizado e, em caso afirmativo, adiciona a transação ao histórico da conta.
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)  # Tenta realizar o depósito

        if sucesso_transacao:  # Se o depósito for bem-sucedido
            conta.historico.adicionar_transacao(self)  # Adiciona a transação ao histórico da conta


def menu():  #Define a função Menu para exibir as opções do sistema
    menu = """\n
    ╔════════════════════════════════════════════╗
    ║              SISTEMA BANCÁRIO              ║
    ║════════════════════════════════════════════║
    ║  [1]  - Depositar                          ║
    ║  [2]  - Sacar                              ║
    ║  [3]  - Extrato                            ║
    ║  [4]  - Nova conta                         ║
    ║  [5]  - Listar contas                      ║
    ║  [6]  - Novo usuário                       ║
    ║  [0]  - Sair                               ║
    ╚════════════════════════════════════════════╝
    Escolha uma opção: """
    
    return input(textwrap.dedent(menu))  # A função textwrap.dedent é usada para remover a indentação extra do texto


def filtrar_cliente(cpf, clientes):  # Filtra os clientes pelo CPF, ou seja, compara o CPF passado com os clientes na lista
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf] #Lista clientes tem o atributo CPF, ele percorre essa lista comparando esse atributo
    return clientes_filtrados[0] if clientes_filtrados else None  #Se a lista não estiver vazia ele retorna o usuário com CPF correspondente


def recuperar_conta_cliente(cliente): # Verifica se o cliente não possui contas associadas
    if not cliente.contas: #Verificação de contas associadas
        print("\nCliente não possui conta!")
        return

    # FIXME: upgrade para conta PJ e PF no sistema
    return cliente.contas[0]  # Retorna a primeira conta do cliente, caso o cliente tenha contas


def depositar(clientes): #Função para deposito
    cpf = input("Informe o CPF do cliente: ") # Solicita o CPF do cliente
    cliente = filtrar_cliente(cpf, clientes) # Realiza o filtro na classe Conta para encontrar o cliente

    if not cliente: #Se o cliente não for encontrado
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))  # Solicita o valor do depósito
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente) # Recupera a conta do cliente
    if not conta: # Se o cliente não tiver conta
        return

    cliente.realizar_transacao(conta, transacao)  # Realiza a transação do depósito na conta


def sacar(clientes): #Função sacar
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes) # Filtra a lista de clientes buscando pelo CPF

    if not cliente:
        print("\nCliente não encontrado!")
        return  # Sem o 'return', o código continuaria, mesmo sem o cliente encontrado

    valor = float(input("Informe o valor do saque: ")) # Solicita o valor que o cliente deseja sacar
    transacao = Saque(valor)  # Cria um objeto do tipo Saque, representando a transação

    conta = recuperar_conta_cliente(cliente) # Recupera a conta associada ao cliente
    if not conta:
        return # Interrompe a execução caso o cliente não tenha conta

    cliente.realizar_transacao(conta, transacao)  # Realiza a transação (o saque) na conta do cliente


def exibir_extrato(clientes): # Recebe o parãmetro Clientes
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes) # Filtra a lista de clientes com o CPF fornecido

    if not cliente:
        print("\n Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================") # Exibe o cabeçalho do extrato
    transacoes = conta.historico.transacoes

    extrato = ""  # Inicializa a variável extrato
    if not transacoes:  # Se não houver transações
        extrato = "Não foram realizadas movimentações." # Exibe a mensagem informando a falta de movimentações
    else:
        for transacao in transacoes: # Para cada transação no histórico
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}" # Adiciona detalhes da transação


    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}") # Exibe o saldo da conta
    print("==========================================")


def criar_cliente(clientes): # Solicita o CPF do cliente
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes) # Verifica se já existe um cliente com o CPF informado

    if cliente:  # Se já houver um cliente, exibe mensagem e retorna
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")  # Solicita outros dados do cliente, caso o CPF não exista
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Cria um novo objeto PessoaFisica com os dados fornecidos
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco) 

    clientes.append(cliente) # Adiciona o novo cliente à lista de clientes

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas): # Solicita o CPF do cliente para o qual a conta será criada
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)    # Busca o cliente na lista de clientes com base no CPF

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")  # Se o cliente não for encontrado, exibe mensagem de erro e encerra a função
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)  # Cria uma nova conta corrente associada ao cliente e ao número de conta fornecido
    # Adiciona a nova conta à lista global de contas e à lista de contas do cliente
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    # Inicializando as listas de clientes e contas
    clientes = []
    contas = []

    # Loop infinito que exibe o menu até o usuário escolher sair
    while True:
        # Chama a função menu() que retorna a opção escolhida pelo usuário
        opcao = menu()

        # Verifica qual opção o usuário escolheu e chama a função correspondente
        if opcao == "1":
            depositar(clientes)  # Chama a função de depósito

        elif opcao == "2":
            sacar(clientes)  # Chama a função de saque

        elif opcao == "3":
            exibir_extrato(clientes)  # Chama a função para exibir extrato

        elif opcao == "4":
            criar_cliente(clientes)  # Chama a função para criar um novo cliente

        elif opcao == "5":
            # Gera um número para a conta baseado no tamanho da lista de contas
            # Pode ser melhor usar uma variável separada para o contador de contas
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)  # Chama a função para criar uma nova conta

        elif opcao == "6":
            listar_contas(contas)  # Chama a função para listar as contas

        elif opcao == "0":
            break  # Encerra o loop e sai do programa

        else:
            # Caso o usuário insira uma opção inválida
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

# Chama a função principal
main()
