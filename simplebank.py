def exibir_menu(): #Menu
    print("="*40)
    print(" " * 5 + "BANCO PYTHON - MENU PRINCIPAL" + " " * 10)
    print("="*40)
    print("[1] - Depositar")
    print("[2] - Sacar")
    print("[3] - Extrato")
    print("[4] - Sair")
    print("="*40)
    opcao = input("Para prosseguir, escolha uma opção válida: ")
    return opcao

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:   #Loop Principal

    opcao = exibir_menu()

    if opcao == "1":  #Área de Depósito
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito efetuado com sucesso!")

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":  #Área de Saque
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

    elif opcao == "3":  #Área de Extrato
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "4":  #Sair
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")