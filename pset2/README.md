# ling_prog_cc3m

Aluno: Nélio Espíndula Junior

Disciplina: Linguagens de programação

Professor: Abrantes Araújo Silva Filho

## PSET2

### Questões:
> Vamos começar com uma imagem 4×1 que é definida com os seguintes parâmetros: \
> altura: 1 \
>• largura: 4 \
>• pixels: [29, 89, 136, 200] \
>
> **QUESTÃO 01:** se você passar essa imagem pelo filtro de inversão, qual seria o output esperado? Justifique sua resposta.

R: Sabendo que os pixels podem ser representados em cores nos valores de 0 até 255, sendo o 0 preto e o 255 o branco, e que o inverso de branco é preto (isto é, se invertermos o branco (valor 0) teremos o valor invertido como preto (valor 255), e vice versa). Podemos deduzir que o inverso de preto é o valor máximo que um pixel pode ter, menos o valor da cor preta:

: 255 [valor maximo] - 0 [preto] = 255 => Branco.

Portanto, os valores inversos da imagem 4x1 dada no enunciado são, respectivamente:

• pixels: [226, 166, 119, 155]

> QUESTÃO 02: faça a depuração e, quando terminar, seu código deve conseguir passar em todos os testes do grupo de teste TestInvertido (incluindo especificamente o que você acabou de criar). Execute seu filtro de inversão na imagem imagens_teste/peixe.png, salve o resultado como uma imagem PNG e salve a imagem em seu repositório GitHub

No arquivo pset2.py, é possível encontrar no final do arquivo o código que executa esta tarefa. E, na pasta question_answers_images é possível ver a imagem peixe.png com o filtro invertido aplicado.

