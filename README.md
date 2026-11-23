# Sistema de Gestão Hospitalar

Projeto final de **Teoria das Estruturas de Dados** (Tema 1: Sistema de Gestão Hospitalar).

Sistema em Python, rodando no terminal, que usa **Lista, Fila, Pilha e Árvore** para organizar dados de um hospital. Todo o código fica no `main.py` e os dados são salvos em um único arquivo texto, o `dados_sistema.txt`.

## Como executar

Precisa do Python 3 instalado. Não usa nenhuma biblioteca externa.

```bash
python main.py
```

(No Linux/macOS pode ser `python3 main.py`.)

O sistema começa vazio. Pelo menu numérico você cadastra os dados. Use **5** para salvar no disco e **6** para carregar de novo em outra execução. O arquivo `dados_sistema.txt` é criado na mesma pasta do `main.py`.

### Menu principal

| Opção | O que faz |
|-------|-----------|
| 1 | Pacientes internados (Lista) |
| 2 | Triagem de pacientes (Fila) |
| 3 | Histórico de prontuários (Pilha) |
| 4 | Especialidades e diagnósticos (Árvore) |
| 5 | Salvar dados no disco |
| 6 | Carregar dados do disco |
| 0 | Sair |

### Operações de cada estrutura

| Estrutura | Criar | Ler | Atualizar | Deletar |
|-----------|-------|-----|-----------|---------|
| Lista | Interna paciente | Lista os internados | Altera leito e estado (por ID) | Dá alta (remove por ID) |
| Fila | Entra no **fim** | Lista do primeiro ao último | Altera a prioridade (por ID) | Chama o próximo e remove do **início** |
| Pilha | Empilha no **topo** | Lista do topo até a base | Altera só o **topo** | Remove o **topo** |
| Árvore | Cadastra Área → Especialidade → Diagnóstico | Exibe a árvore | Renomeia um diagnóstico | Remove um diagnóstico |

## Por que cada estrutura foi escolhida

### Lista (`list`): pacientes internados e leitos
Os pacientes internados entram e saem a qualquer momento, e o sistema precisa achar um paciente específico pelo ID para consultar, atualizar ou dar alta. A lista permite percorrer e remover qualquer elemento, o que a fila e a pilha não permitem.

### Fila (`collections.deque`): triagem
A triagem atende por ordem de chegada, ou seja, **FIFO**: quem chega primeiro é atendido primeiro. A inserção é sempre no fim (`append`) e a remoção sempre no início (`popleft`). Usei `deque` porque `popleft()` é O(1), enquanto `pop(0)` em uma `list` é O(n), pois move todos os elementos.

### Pilha (`list`): prontuários acessados recentemente
Para revisar rápido, o prontuário mais recente tem que ser o primeiro a aparecer, ou seja, **LIFO**. Uma `list` resolve isso com `append()` para empilhar e `pop()` para desempilhar, os dois no final da lista e em O(1). Como numa pilha só o topo é acessível, só ele pode ser atualizado.

### Árvore (dicionários aninhados): especialidades e diagnósticos
Áreas, especialidades e diagnósticos formam uma hierarquia (Clínica Geral → Cardiologia → Arritmia). Cada nível é uma chave de dicionário e os filhos são o dicionário dentro dela:

```python
{"Clinica Geral": {"Cardiologia": {"Arritmia": {}}, "Ortopedia": {"Fratura": {}}}}
```

Isso permite buscar e verificar duplicidade pela chave e percorrer a árvore com uma **função recursiva** para exibi-la com recuo. Uma lista simples não mostraria a relação entre pai e filho.

## Formato do `dados_sistema.txt`

Cada linha começa com o tipo da estrutura e os campos são separados por `|`:

```
LISTA|101|Carlos Silva|Leito 04|Estavel
FILA|205|Roberto Alves|Prioridade Alta
PILHA|PRONT-889|Paciente 101|Consulta Cardiologia
ARVORE|Clinica Geral|Cardiologia|Arritmia
```

- A fila é salva do primeiro ao último.
- A pilha é salva da base ao topo, então ao carregar o último registro volta a ser o topo.
- Na árvore, cada linha é um diagnóstico com o caminho completo; os outros níveis são recriados ao carregar.
- Como o `|` é o separador, se o usuário digitar `|` em algum campo ele é trocado por `-`.
- Ao carregar, as estruturas em memória são limpas antes de ler o arquivo, para não duplicar registros.
