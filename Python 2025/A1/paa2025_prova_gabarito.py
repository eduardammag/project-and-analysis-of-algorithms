

def question_1():
    """
    Determine uma função f(n) para o código a seguir tal que
    T(n)=θ(f(n)). Explique como a solução foi encontrada.

    int compute(int v[], int left, int right) {
        int n = right - left + 1;
        if (n <= 1) return 0;
        int mid = (left + right) / 2;
        int sum = 0;
        sum += compute(v, left, mid);
        sum += compute(v, mid + 1, right);
        sum += compute(v, left + n/4, mid + n/4);
        sum += compute(v, mid - n/4, right - n/4);
        int temp[n];
        int tempSize = 0;
        for (int i = left; i <= right; i++) {
            int pos = 0;
            while (pos < tempSize && temp[pos] < v[i]) {
                pos++;
            }
            for (int j = tempSize; j > pos; j--) {
                temp[j] = temp[j-1];
            }            
            temp[pos] = v[i];
            tempSize++;
            sum++;
        }
        for (int i = 0; i < n; i++) {
            v[left + i] = temp[i];
        }
        return sum;
    }
    
    (1) ANALISE DO CÓDIGO:

    Este algoritmo realiza chamadas recursivas com as seguintes características:
    - Caso base: quando n <= 1, retorna 0
    - Fase recursiva: realiza 4 chamadas recursivas com tamanho ~n/2.
    - Fase de conquista: apos as chamadas recursivas, executa:
        * Um loop de inserção ordenada que insere cada elemento do intervalo [left, right]
        em um array temporário mantendo-o ordenado
        * No pior caso (array em ordem decrescente), cada inserção do i-esimo elemento
        requer i movimentações, resultando em 0+1+2+...+(n-1) = n(n-1)/2 operações
        * Copia o array temporário de volta para o array original (n operações)
        * Total da fase de conquista: θ(n^2)

    (2) EQUACÃO DE RECORRÊNCIA:

    T(n) = 4*T(n/2) + θ(n^2)

    com T(1) = θ(1)

    (3) RESOLUÇÃO DA RECORRÊNCIA:

    Aplicando o Teorema Mestre:
    - a = 4 (número de subproblemas)
    - b = 2 (fator de divisão da entrada)
    - f(n) = n^2 (complexidade do trabalho não-recursivo)

    Calculando log_b(a):
    log_2(4) = 2

    Comparando f(n) com n^(log_b(a)):
    f(n) = n^2
    n^(log_b(a)) = n^2

    Como f(n) = θ(n^(log_b(a))), estamos no Caso 2 do Teorema Mestre.

    Portanto:
    T(n) = θ(n^(log_b(a)) * log(n))
    T(n) = θ(n^2 * log(n))

    RESPOSTA FINAL: T(n) = θ(n^2 * log(n))
    
    """
    pass
    

def question_2(products: list[int], k: int) -> int:
    """
    Uma empresa de logística mantém produtos em um armazém circular organizados em 
    ordem crescente. Cada produto é identificado por um código numérico. Quando o 
    armazém sofre rotação para otimização de espaço, a sequência ordenada é 
    "rotacionada" - alguns elementos do final vão para o início, mantendo a ordem 
    relativa. Por exemplo, a sequência [10, 20, 30, 40, 50] após rotação de 2 
    posições se torna [40, 50, 10, 20, 30]. Desenvolva um algoritmo eficiente para 
    encontrar um produto específico neste armazém rotacionado, retornando a sua 
    posição ou -1 caso não exista. O algoritmo deverá ter complexidade O(log n).
    """
    left, right = 0, len(products) - 1
    while left <= right:
        mid = (left + right) // 2
        if products[mid] == k:
            return mid
        # Left partition sorted
        if products[left] <= products[mid]:
            if products[left] <= k < products[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right partition sorted
        else:
            if products[mid] < k <= products[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
    

def question_3(events: list[int], k: int) -> list[tuple[int, int]]:
    """
    Um serviço de streaming precisa manter atualizado em tempo real um ranking com 
    as k músicas mais tocadas. A cada nova reprodução de uma música, um evento é 
    gerado para atualizar o ranking. Como o volume de eventos é imenso, manter todas 
    as músicas disponíveis ordenadas é inviável. Projete um algoritmo que processe 
    um stream com n eventos, contendo em cada um o identificador numérico da música, 
    e produza o ranking de k posições em O(nlogk), onde k≪n.
    
    ERRATA: você pode considerar o caso médio de algoritmos auxiliares.
    """
    if not events or k <= 0:
        return []

    # Count how many times each music was reproduced
    count = {}
    for music_id in events:
        count[music_id] = count.get(music_id, 0) + 1

    def heapify(heap, i):
        n = len(heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
        
            if left < n and heap[left][1] < heap[smallest][1]:
                smallest = left
        
            if right < n and heap[right][1] < heap[smallest][1]:
                smallest = right
        
            if smallest != i:
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
            else:
                break

    # Build the heap inserting or replacing based on the number of elements
    heap = []
    for music_id, play_count in count.items():
        if len(heap) < k:
            heap.append((music_id, play_count))
            i = len(heap) - 1
            while i > 0:
                parent = (i - 1) // 2
                if heap[i][1] < heap[parent][1]:
                    heap[i], heap[parent] = heap[parent], heap[i]
                    i = parent
                else:
                    break
        elif play_count > heap[0][1]:
            heap[0] = (music_id, play_count)
            heapify(heap, 0)

    # Create the ranking
    result = []
    while heap:
        result.append(heap[0])
        heap[0] = heap[-1]
        del heap[-1]
        if heap:
            heapify(heap, 0)
    result.reverse()

    return result


def question_4(v) -> list[int]:
    """
    Considerando a tabela hash com endereçamento aberto, responda as perguntas 
    a seguir:
    a)	Explique como é a sua estrutura de dados, e como funcionam os algoritmos 
        de busca, inserção e remoção.
    b)	Compare as estratégias de hash duplo e sondagem quadrática.
    c)	Explique o que é o processo de resize e re-hashing, e avalie a sua 
        complexidade.
    
    a)
    Estrutura de dados:
        Array de tamanho fixo onde cada posição armazena diretamente uma chave-valor. Essa abordagem 
        resolve colisões buscando uma próxima posição livre no array utilizando uma sequência de  
        sondagem.
    
    Algoritmo de busca:        
        Dada uma chave k, calcula-se a posição esperada através de uma função de espalhamento. Caso a 
        chave não se encontre nessa posição, a próxima posição da sequência de sondagem é verificada;
        até encontrar o elemento ou determinar que o o mesmo não está presente na tabela.
                
    Algoritmo de inserção:
        Dada uma chave k e um valor v, utiliza o algoritmo de busca para encontrar o elemento. Caso 
        exista o valor é alterado para v; caso contrário o mesmo é inserido na primeira posição vazia 
        da sequência de sondagem. 
                
    Algoritmo de remoção:
        Dada uma chave k, utiliza o algoritmo de busca para encontrar o elemento. Caso a busca tenha 
        sucesso, marca a posição como reciclada e remove o elemento. Posições recicladas devem ser 
        consideradas como ocupadas na busca, e vazias na inserção.
        
    b)
    Sondagem quadrática: h(k, i) = (h1(k) + c1·i + c2·i^2) mod m
    - Reduz clustering primário, mas sofre de clustering secundário.
    - Chaves com mesma hash inicial seguem mesma sequência de sondagem.
    - Pode não visitar todas as posições da tabela (depende de m).
    
    Hash Duplo:        
    - h(k, i) = (h1(k) + i·h2(k)) mod m
    - Utiliza uma segunda função hash h2(k) para determinar o passo.
    - Elimina clustering primário e secundário.
    - Aproxima-se de hashing uniforme (melhor distribuição).
    - Vantagem: desempenho superior em tabelas com alta carga.
    - Desvantagem: custo computacional ligeiramente maior (duas funções hash)
    
    c)
    Processo:
        Cria nova tabela com tamanho maior (ex: dobra o tamanho) e reinsere todos elementos da 
        tabela antiga na nova usando a nova função de hash. A operação costuma ser executada quando o 
        fator de carga é considerado alto (ex: α = n/m > 0.7), e é crítico para manter o desempendo O(1).
    
    Complexidade:
        Considerando uma tabela com n elementos, ocorreram:
         - n operações de inserção com custo O(1)
         - k operações de resize & re-hashing
            Custo total: somatório de 2^i, de i=1 até log(n) = O(n),
            Considerando que a cada operação a tabela dobrou de tamanho. 
        Portanto, a análise amortizada é:
            (n * O(1) + O(n))/n = O(1)
    """
    pass
