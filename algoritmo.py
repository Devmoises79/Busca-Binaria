# Sistema com busca binária, menu interativo e separação de responsabilidades com desfazer e log

log_acoes = []
historico_remocoes = []


def busca_binaria(lista, alvo, inicio=0, fim=None):
    if fim is None:
        fim = len(lista) - 1

    if inicio > fim:
        return -1

    meio = (inicio + fim) // 2

    if lista[meio] == alvo:
        return meio
    elif lista[meio] < alvo:
        return busca_binaria(lista, alvo, meio + 1, fim)
    else:
        return busca_binaria(lista, alvo, inicio, meio - 1)


def mostrar_nomes(lista):
    print("\n📃 Lista de nomes:")
    for idx, nome in enumerate(lista, start=1):
        print(f"{idx} - {nome}")


def desfazer_remocao(nomes, nome_atual):
    if historico_remocoes:
        nome_restaurado, posicao = historico_remocoes[-1]  # Não remove ainda
        if nome_restaurado == nome_atual:
            historico_remocoes.pop()
            nomes.insert(posicao, nome_restaurado)
            nomes.sort()  # Reordena a lista após restauração
            log_acoes.append(f"Nome restaurado: {nome_restaurado}")
            print(f"↩️ Nome '{nome_restaurado}' foi restaurado à lista!")
            mostrar_nomes(nomes)
        else:
            print(f"⚠️ Não é possível desfazer. O último nome removido foi '{nome_restaurado}', não '{nome_atual}'.")
    else:
        print("⚠️ Nenhuma remoção para desfazer.")


def salvar_log():
    with open("log_acoes.txt", "w", encoding="utf-8") as f:
        for acao in log_acoes:
            f.write(acao + "\n")
    print("📝 Log salvo em 'log_acoes.txt'.")


def menu_operacoes(nome, nomes):
    while True:
        print(f"\n🔍 Nome selecionado: {nome}")
        print("O que deseja fazer?")
        print("1 - Buscar índice (posição)")
        print("2 - Remover nome")
        print("3 - Mostrar lista atualizada")
        print("4 - Desfazer última remoção")
        print("5 - Salvar log de ações")
        print("0 - Voltar ao menu principal")

        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                indice = busca_binaria(nomes, nome)
                print(f"📍 O nome '{nome}' está na posição: {indice}")
                log_acoes.append(f"Buscou índice do nome: {nome}")
            elif opcao == 2:
                indice_removido = nomes.index(nome)
                nomes.remove(nome)
                historico_remocoes.append((nome, indice_removido))
                print(f"❌ Nome '{nome}' removido da lista com sucesso!")
                log_acoes.append(f"Nome removido: {nome}")
                mostrar_nomes(nomes)
                return  # Volta ao menu principal após remoção
            elif opcao == 3:
                mostrar_nomes(nomes)
            elif opcao == 4:
                desfazer_remocao(nomes, nome)
            elif opcao == 5:
                salvar_log()
            elif opcao == 0:
                return
            else:
                print("⚠️ Opção inválida.")
        except ValueError:
            print("⚠️ Por favor, digite um número válido.")


def menu_principal():
    nomes = ["Ana", "Bruno", "João", "Lucas", "Luiz", "Maria", "Pedro"]
    nomes.sort()

    while True:
        print("\n------ Bem-vindo ao Search Names ------")
        mostrar_nomes(nomes)

        try:
            escolha = int(input("\nDigite o número do nome que deseja selecionar (0 para sair): "))
            if escolha == 0:
                print("\n👋 Encerrando o programa. Salvando log...")
                salvar_log()
                break
            elif 1 <= escolha <= len(nomes):
                nome_escolhido = nomes[escolha - 1]
                menu_operacoes(nome_escolhido, nomes)
            else:
                print("⚠️ Número fora do intervalo.")
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número.")


if __name__ == "__main__":
    menu_principal()
