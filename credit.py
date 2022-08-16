#--------------------------------------------------#
#    Problem Set 1 - Linguagens de Programação     #
#              Algoritmo de Luhn                   #
#--------------------------------------------------#
# Aluno: Nélio Espíndula Junior                    #
# Turma: CC3M                                      #
# Professor: Abrantes Araújo Silva Filho           #
#--------------------------------------------------#


def card_flag(ccNumber):

    # FUNÇÃO PRA DESCOBRIR DE QUAL BANDEIRA É O CARTÃO.
    # SEGUINDO A TABELA DE Issuer identification number (IIN) DISPONÍVEL EM: https://en.wikipedia.org/wiki/Payment_card_number
    # FIZ UMA COMBINAÇÕES DE IF's

    str_ccNumber = str(ccNumber)

    if str_ccNumber[0:2] == "34" or str_ccNumber[0:2] == "37":
        return print("AMEX")
    elif 2221 <= int(str_ccNumber[0:4]) <= 2720 or 51 <= int(str_ccNumber[0:2]) <= 55:
        return print("MASTERCARD")
    elif str_ccNumber[0] == "4" or str_ccNumber[0:4] == "4026" or str_ccNumber[0:4] == "4508" or str_ccNumber[0:4] == "4844" or str_ccNumber[0:4] == "4913" or str_ccNumber[0:4] == "4917" or str_ccNumber[0:5] == "417500":
        return print("VISA")
    else:
        return print("INVALID")


def card_validator(card_number):

    string_param = str(card_number)

    # CONDICIONAL PARA ATESTAR SE O NÚMERO DO CARTÃO É INVÁLIDO ANTES MESMO
    # DE VALIDAR. QUANTIDADE DE CARACTERES PEQUENA, PRESENÇA DE HÍFES, UNDERLINES
    # OU ESPAÇOS VAZIOS SÃO DETIDOS AQUI.
    if len(string_param) <= 11:
        print('INVALID')
        return 'INVALID'
    elif '-' in string_param or ' ' in string_param or '_' in string_param:
        print('INVALID')
        return 'INVALID'

    sum_db = 0
    dn_sum = 0

    for i in range(len(string_param)-2, -1, -2):
        # ESSE FOR SERVE PARA PERCORRER DE 2 EM 2, DE TRAZ PRA FRENTE
        # A PARTIR DO ÍNDICE DE NÚMERO -2, QUE EM QUALQUER CONJUNTO
        # DE CARACTERES SERÁ O PENÚLTIMO ITEM.
        doubled_number = int(string_param[i]) * 2
        # SEGUINDO O ALGORITMO, MULTIPLIQUEI OS VALORES QUE O
        # LOOP ME TROUXE POR 2 E ARMAZENEI NA VARIÁVEL doubled_number
        if doubled_number >= 10:
            # CONDICIONAL SIMPLES, SE O NÚMERO FOR MAIOR OU IGUAL A 10
            # (OU SEJA TER MAIS QUE UM DÍGITO) ELE CAI AQUI DENTRO.

            # CONVERTO O NÚMERO PRA UMA STRING
            str_dn = str(doubled_number) 
            # DIVIDO A STRING EM DUAS PARTES E AS SOMO
            dn_sum = int(str_dn[0]) + int(str_dn[1])
            # ADICIONO O VALOR SOMADO NA MINHA VARIÁVEL DE SOMA TOTAL
            sum_db += dn_sum

        else:
            sum_db += doubled_number
            # SE O NÚMERO NÃO TIVER DOIS DÍGITOS, ELE SIMPLESMENTE É SOMADO NO TOTAL.

    for z in range(len(string_param)-1, -1, -2):
        # SEMELHANTE AO PRIMEIRO LOOP, PORÉM, ELE COMEÇA A PARTIR DO ANTEPENÚLTIMO
        # ITEM. DESSA FORMA, ELE PEGA APENAS OS QUE NÃO FORAM SOMADOS AINDA
        sum_db += int(string_param[z])
        # E AQUI ELES SÃO SOMADOS NO TOTAL.

    if sum_db % 10 == 0:
        # SEGUINDO O ALGORITMO DE Luhn, SE O MÓDULO DA DIVISÃO DESSA SOMA
        # TOTAL FOR IGUAL A ZERO, O NÚMERO DO CARTÃO É VÁLIDO.
        return card_flag(card_number)

    else:
        print("INVALID")
        # CASO CONTRÁRIO, INVÁLIDO.
        return "INVALID"


#------------ ZONA DE EXECUÇÃO DO PROGRAMA ------------#
#                                                      #
card = input("Digite o número do seu cartão: ")        #
card_validator(card)                                   #
#                                                      #
#------------------------------------------------------#
