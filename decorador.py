usuarios = []  # Lista para armazenar os usuários
numero_conta = 1  # Contador de contas (a conta vai subindo conforme os usuários são criados)
LIMITE_SAQUES = 3
saldo = 0
limite = 500
extrato = ""
numero_saques = 0

def exibir_menu():  # Menu
    print("="*40)
    print(" " * 5 + "BANCO PYTHON - MENU PRINCIPAL" + " " * 10)
    print("="*40)
    print("[1] - Depositar")
    print("[2] - Sacar")
    print("[3] - Extrato")
    print("[4] - Criar Conta")
    print("[5] - Sair")
    print("="*40)
    opcao = input("Para prosseguir, escolha uma opção válida: ")
    return opcao


def validar_cpf(cpf): #Validação no CPF
    return len(cpf) == 11 and cpf.isdigit()

from datetime import datetime

def validar_data(data): #Validação no formato data
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validar_nome(nome):  #Validação no formato de nome
    return not any(char.isdigit() for char in nome)

while True:  # Loop Principal
    opcao = exibir_menu()

    if opcao == "1":  # Área de Depósito
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito efetuado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":  # Área de Saque
        valor = float(input("Informe o valor do saque: "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("Saque efetuado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":  # Área de Extrato
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "4":  # Criar conta
        nome = input("Digite seu nome completo: ")
        if not validar_nome(nome):
            print("Erro: O nome não pode conter números.")
            continue
        data_de_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
        if not validar_data(data_de_nascimento):
            print("Erro: A data de nascimento é inválida. Use o formato DD/MM/AAAA.")
            continue
        cpf = input("Digite seu CPF, sem traço e ponto: ")
        if not validar_cpf(cpf):
            print("Erro: O CPF deve ter 11 dígitos numéricos.")
            continue
        estado = input("Digite o estado onde mora: ")

        # Verificar se o CPF já existe
        cpf_existente = any(user["cpf"] == cpf for user in usuarios)
        if cpf_existente:
            print("Erro: Este CPF já está cadastrado!")
        else:
            usuario = {
                "nome": nome,
                "data_de_nascimento": data_de_nascimento,
                "cpf": cpf,
                "estado": estado,
                "agencia": "0001",  # Agência fixa
                "conta": numero_conta  # Conta do usuário
            }
            usuarios.append(usuario)
            print(f"Usuário {nome} cadastrado com sucesso! Conta: {numero_conta}")
            numero_conta += 1  # Incrementa para o próximo número de conta

    elif opcao == "5":  # Sair
        print("Saindo do sistema... Até logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
