from collections import deque
import os

ARQUIVO_DADOS = "dados_sistema.txt"

lista_internados = []
fila_triagem = deque()
pilha_prontuarios = []
arvore_diagnosticos = {}


def ler_texto(msg, obrigatorio=True):
    while True:
        # troca o | por - senão quebra o arquivo de dados
        texto = input(msg).strip().replace("|", "-")
        if texto or not obrigatorio:
            return texto
        print("Campo obrigatório.")


def menu_principal():
    while True:
        print("\n===== SISTEMA DE GESTÃO HOSPITALAR =====")
        print("1. Pacientes Internados (LISTA)")
        print("2. Triagem de Pacientes (FILA)")
        print("3. Histórico de Prontuários (PILHA)")
        print("4. Especialidades e Diagnósticos (ÁRVORE)")
        print("5. Salvar Dados no Disco")
        print("6. Carregar Dados do Disco")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_lista()
        elif opcao == "2":
            menu_fila()
        elif opcao == "3":
            menu_pilha()
        elif opcao == "4":
            menu_arvore()
        elif opcao == "5":
            salvar_dados()
        elif opcao == "6":
            carregar_dados()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_lista():
    while True:
        print("\n=== [LISTA] PACIENTES INTERNADOS ===")
        print("1. Internar paciente (Inserir)")
        print("2. Listar internados (Ler)")
        print("3. Atualizar leito/estado (Atualizar)")
        print("4. Dar alta / Remover (Deletar)")
        print("0. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            inserir_internado()
        elif op == "2":
            listar_internados()
        elif op == "3":
            atualizar_internado()
        elif op == "4":
            remover_internado()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_fila():
    while True:
        print("\n=== [FILA - FIFO] TRIAGEM DE PACIENTES ===")
        print("1. Adicionar paciente ao fim da fila")
        print("2. Visualizar fila de espera")
        print("3. Atualizar prioridade na fila")
        print("4. Chamar próximo paciente (Remover do início)")
        print("0. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            enfileirar_triagem()
        elif op == "2":
            listar_triagem()
        elif op == "3":
            atualizar_triagem()
        elif op == "4":
            atender_proximo_triagem()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_pilha():
    while True:
        print("\n=== [PILHA - LIFO] HISTÓRICO DE PRONTUÁRIOS ===")
        print("1. Registrar acesso a prontuário (Empilhar no topo)")
        print("2. Visualizar histórico (Topo -> Base)")
        print("3. Atualizar observação do topo")
        print("4. Remover último acesso (Desempilhar do topo)")
        print("0. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            empilhar_prontuario()
        elif op == "2":
            listar_prontuarios()
        elif op == "3":
            atualizar_topo_prontuario()
        elif op == "4":
            desempilhar_prontuario()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_arvore():
    while True:
        print("\n=== [ÁRVORE] ESPECIALIDADES E DIAGNÓSTICOS ===")
        print("1. Cadastrar diagnóstico na hierarquia")
        print("2. Exibir árvore completa")
        print("3. Renomear diagnóstico")
        print("4. Remover diagnóstico")
        print("0. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            cadastrar_diagnostico_arvore()
        elif op == "2":
            listar_arvore()
        elif op == "3":
            atualizar_diagnostico_arvore()
        elif op == "4":
            remover_diagnostico_arvore()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


# ---------- LISTA ----------

def inserir_internado():
    print("\n--- Internar Paciente ---")
    id_pac = ler_texto("ID do paciente (ex: 101): ")

    for p in lista_internados:
        if p["id"] == id_pac:
            print("Erro: Já existe um paciente internado com esse ID.")
            return

    nome = ler_texto("Nome do paciente: ")
    leito = ler_texto("Leito (ex: Leito 04): ")
    estado = ler_texto("Estado clínico (ex: Estavel, Observacao): ")

    lista_internados.append({
        "id": id_pac,
        "nome": nome,
        "leito": leito,
        "estado": estado
    })
    print("Paciente internado com sucesso!")


def listar_internados():
    print("\n--- Pacientes Internados ---")
    if not lista_internados:
        print("Nenhum paciente internado no momento.")
        return

    for p in lista_internados:
        print(f"ID: {p['id']} | Nome: {p['nome']} | {p['leito']} | Estado: {p['estado']}")


def atualizar_internado():
    listar_internados()
    if not lista_internados:
        return

    id_pac = input("\nDigite o ID do paciente que deseja atualizar: ").strip()
    for p in lista_internados:
        if p["id"] == id_pac:
            novo_leito = ler_texto(f"Novo leito (Enter para manter '{p['leito']}'): ", False)
            novo_estado = ler_texto(f"Novo estado (Enter para manter '{p['estado']}'): ", False)

            if novo_leito:
                p["leito"] = novo_leito
            if novo_estado:
                p["estado"] = novo_estado

            print("Cadastro atualizado com sucesso!")
            return

    print("Paciente não encontrado.")


def remover_internado():
    listar_internados()
    if not lista_internados:
        return

    id_pac = input("\nDigite o ID do paciente para dar alta (remover): ").strip()
    for i, p in enumerate(lista_internados):
        if p["id"] == id_pac:
            removido = lista_internados.pop(i)
            print(f"Alta registrada para {removido['nome']} (ID {removido['id']}).")
            return

    print("Paciente não encontrado.")


# ---------- FILA ----------

def enfileirar_triagem():
    print("\n--- Adicionar Paciente à Fila de Triagem ---")
    senha = ler_texto("Número da senha/ID (ex: 205): ")

    for p in fila_triagem:
        if p["id"] == senha:
            print("Erro: Já existe um paciente com esse ID na fila.")
            return

    nome = ler_texto("Nome do paciente: ")
    prioridade = ler_texto("Prioridade (ex: Prioridade Alta, Normal): ")

    # FILA: entra sempre no final
    fila_triagem.append({
        "id": senha,
        "nome": nome,
        "prioridade": prioridade
    })
    print("Paciente inserido no final da fila.")


def listar_triagem():
    print("\n--- Fila de Triagem (Início -> Fim) ---")
    if not fila_triagem:
        print("Fila de triagem vazia.")
        return

    for pos, p in enumerate(fila_triagem, start=1):
        print(f"{pos}º | ID: {p['id']} | Nome: {p['nome']} | {p['prioridade']}")


def atualizar_triagem():
    listar_triagem()
    if not fila_triagem:
        return

    senha = input("\nDigite o ID/senha do paciente para atualizar a prioridade: ").strip()
    for p in fila_triagem:
        if p["id"] == senha:
            nova_prio = ler_texto(f"Nova prioridade (atual: {p['prioridade']}): ", False)
            if nova_prio:
                p["prioridade"] = nova_prio
                print("Prioridade atualizada.")
            return

    print("Paciente não encontrado na fila.")


def atender_proximo_triagem():
    print("\n--- Chamar Próximo Paciente ---")
    if not fila_triagem:
        print("Nenhum paciente aguardando na fila.")
        return

    # FILA: sai sempre do começo (FIFO)
    atendido = fila_triagem.popleft()
    print(f"Chamando: {atendido['nome']} (ID: {atendido['id']} | {atendido['prioridade']})")


# ---------- PILHA ----------

def empilhar_prontuario():
    print("\n--- Registrar Acesso a Prontuário ---")
    codigo = ler_texto("Código do prontuário (ex: PRONT-889): ")
    paciente = ler_texto("Paciente (ex: Paciente 101): ")
    detalhe = ler_texto("Motivo/Procedimento (ex: Consulta Cardiologia): ")

    # PILHA: empilha no topo (último da lista)
    pilha_prontuarios.append({
        "codigo": codigo,
        "paciente": paciente,
        "detalhe": detalhe
    })
    print("Prontuário adicionado ao topo do histórico.")


def listar_prontuarios():
    print("\n--- Histórico de Prontuários (Topo -> Base) ---")
    if not pilha_prontuarios:
        print("Nenhum prontuário no histórico.")
        return

    # percorre de trás pra frente pra mostrar o topo primeiro
    for i in range(len(pilha_prontuarios) - 1, -1, -1):
        pront = pilha_prontuarios[i]
        marcador = " [TOPO]" if i == len(pilha_prontuarios) - 1 else ""
        print(f"{pront['codigo']} | {pront['paciente']} | {pront['detalhe']}{marcador}")


def atualizar_topo_prontuario():
    if not pilha_prontuarios:
        print("\nHistórico vazio. Nada no topo para atualizar.")
        return

    topo = pilha_prontuarios[-1]
    print(f"\nProntuário no topo: {topo['codigo']} | {topo['paciente']} | {topo['detalhe']}")
    novo_detalhe = ler_texto("Novo detalhe/observação: ", False)
    if novo_detalhe:
        topo["detalhe"] = novo_detalhe
        print("Prontuário do topo atualizado.")


def desempilhar_prontuario():
    print("\n--- Remover Último Prontuário Acessado ---")
    if not pilha_prontuarios:
        print("Pilha vazia.")
        return

    # PILHA: só remove o topo (LIFO)
    removido = pilha_prontuarios.pop()
    print(f"Removido do topo: {removido['codigo']} ({removido['paciente']} - {removido['detalhe']})")


# ---------- ÁRVORE ----------

def inserir_na_arvore(area, especialidade, diagnostico):
    if area not in arvore_diagnosticos:
        arvore_diagnosticos[area] = {}
    if especialidade not in arvore_diagnosticos[area]:
        arvore_diagnosticos[area][especialidade] = {}
    arvore_diagnosticos[area][especialidade][diagnostico] = {}


def cadastrar_diagnostico_arvore():
    print("\n--- Cadastrar na Árvore de Diagnósticos ---")
    area = ler_texto("Área médica (ex: Clinica Geral): ")
    especialidade = ler_texto("Especialidade (ex: Cardiologia): ")
    diagnostico = ler_texto("Diagnóstico (ex: Arritmia): ")

    if area in arvore_diagnosticos and especialidade in arvore_diagnosticos[area] \
            and diagnostico in arvore_diagnosticos[area][especialidade]:
        print("Esse diagnóstico já está cadastrado.")
        return

    inserir_na_arvore(area, especialidade, diagnostico)
    print("Diagnóstico indexado na árvore com sucesso.")


def exibir_arvore_recursivo(no_atual, nivel=0):
    for chave, sub_no in no_atual.items():
        prefixo = "  " * nivel + ("└─ " if nivel > 0 else "")
        print(f"{prefixo}{chave}")
        # recursão: se o nó tem filhos, chama a própria função pra eles (nível + 1)
        if sub_no:
            exibir_arvore_recursivo(sub_no, nivel + 1)


def listar_arvore():
    print("\n--- Árvore de Especialidades e Diagnósticos ---")
    if not arvore_diagnosticos:
        print("Árvore vazia.")
        return
    exibir_arvore_recursivo(arvore_diagnosticos)


def atualizar_diagnostico_arvore():
    listar_arvore()
    if not arvore_diagnosticos:
        return

    print("\n--- Renomear Diagnóstico ---")
    area = input("Área médica: ").strip()
    esp = input("Especialidade: ").strip()
    diag_antigo = input("Diagnóstico atual: ").strip()

    if area in arvore_diagnosticos and esp in arvore_diagnosticos[area] and diag_antigo in arvore_diagnosticos[area][esp]:
        diag_novo = ler_texto("Novo nome do diagnóstico: ")
        if diag_novo in arvore_diagnosticos[area][esp]:
            print("Já existe um diagnóstico com esse nome.")
            return
        del arvore_diagnosticos[area][esp][diag_antigo]
        arvore_diagnosticos[area][esp][diag_novo] = {}
        print("Diagnóstico atualizado com sucesso.")
    else:
        print("Caminho não encontrado na árvore.")


def remover_diagnostico_arvore():
    listar_arvore()
    if not arvore_diagnosticos:
        return

    print("\n--- Remover Diagnóstico ---")
    area = input("Área médica: ").strip()
    esp = input("Especialidade: ").strip()
    diag = input("Diagnóstico a remover: ").strip()

    if area in arvore_diagnosticos and esp in arvore_diagnosticos[area] and diag in arvore_diagnosticos[area][esp]:
        del arvore_diagnosticos[area][esp][diag]
        # se o ramo ficou vazio, remove ele também
        if not arvore_diagnosticos[area][esp]:
            del arvore_diagnosticos[area][esp]
        if not arvore_diagnosticos[area]:
            del arvore_diagnosticos[area]
        print("Diagnóstico removido da árvore.")
    else:
        print("Caminho não encontrado na árvore.")


# ---------- ARQUIVO TXT ----------

def salvar_dados():
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            for p in lista_internados:
                f.write(f"LISTA|{p['id']}|{p['nome']}|{p['leito']}|{p['estado']}\n")

            for p in fila_triagem:
                f.write(f"FILA|{p['id']}|{p['nome']}|{p['prioridade']}\n")

            # da base pro topo, assim ao carregar a ordem da pilha continua igual
            for pr in pilha_prontuarios:
                f.write(f"PILHA|{pr['codigo']}|{pr['paciente']}|{pr['detalhe']}\n")

            # uma linha por diagnóstico, com o caminho completo
            for area, especialidades in arvore_diagnosticos.items():
                for esp, diagnosticos in especialidades.items():
                    for diag in diagnosticos:
                        f.write(f"ARVORE|{area}|{esp}|{diag}\n")

        print(f"\nDados salvos com sucesso em '{ARQUIVO_DADOS}'.")
    except OSError as e:
        print(f"Erro ao salvar arquivo: {e}")


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"\nArquivo '{ARQUIVO_DADOS}' não encontrado. Salve dados primeiro.")
        return

    # limpa tudo antes pra não duplicar registros
    lista_internados.clear()
    fila_triagem.clear()
    pilha_prontuarios.clear()
    arvore_diagnosticos.clear()

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                # separa pelo | e o primeiro campo diz qual estrutura é
                partes = linha.split("|")
                tipo = partes[0]

                if tipo == "LISTA" and len(partes) == 5:
                    lista_internados.append({
                        "id": partes[1],
                        "nome": partes[2],
                        "leito": partes[3],
                        "estado": partes[4]
                    })
                elif tipo == "FILA" and len(partes) == 4:
                    fila_triagem.append({
                        "id": partes[1],
                        "nome": partes[2],
                        "prioridade": partes[3]
                    })
                elif tipo == "PILHA" and len(partes) == 4:
                    pilha_prontuarios.append({
                        "codigo": partes[1],
                        "paciente": partes[2],
                        "detalhe": partes[3]
                    })
                elif tipo == "ARVORE" and len(partes) == 4:
                    inserir_na_arvore(partes[1], partes[2], partes[3])

        print(f"\nDados carregados com sucesso de '{ARQUIVO_DADOS}'.")
    except OSError as e:
        print(f"Erro ao ler arquivo: {e}")


if __name__ == "__main__":
    menu_principal()
