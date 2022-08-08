#--------------------------------------------------#
#    Problem Set 1 - Linguagens de Programação     #
#              Algoritmo de Luhn                   #
#--------------------------------------------------#
# Aluno: Nélio Espíndula Junior                    #
# Turma: CC3M                                      #
# Professor: Abrantes Araújo Silva Filho           #
#--------------------------------------------------#

def card_validator(card_number):
    string_param = str(card_number)
    sum_db = 0
    dn_sum = 0

    for i in range(len(string_param)-2,-2,-2):
        # ESSE FOR SERVE PARA PERCORRER DE 2 EM 2, DE TRAZ PRA FRENTE
        # A PARTIR DO ÍNDICE DE NÚMERO -2, QUE EM QUALQUER CONJUNTO
        # DE CARACTERES SERÁ O PENÚLTIMO ITEM.
        doubled_number = int(string_param[i])* 2 
        # SEGUINDO O ALGORITMO, MULTIPLIQUEI OS VALORES QUE O 
        # LOOP ME TROUXE POR 2 E ARMAZENEI NA VARIÁVEL doubled_number
        if doubled_number >= 10:
            # CONDICIONAL SIMPLES, SE O NÚMERO FOR MAIOR QUE 10
            # (OU SEJA TER MAIS QUE UM DÍGITO) ELE CAI AQUI DENTRO.

            str_dn = str(doubled_number) # CONVERTO O NÚMERO PRA UMA STRING
            dn_sum = int(str_dn[0]) + int(str_dn[1]) # DIVIDO A STRING EM DUAS PARTES E AS SOMO
            
            sum_db += dn_sum 
            # ADICIONO O VALOR SOMADO NA MINHA VARIÁVEL DE SOMA TOTAL DECLARADA NA LINHA 12
            
        else:
            sum_db += doubled_number
            # SE O NÚMERO NÃO TIVER DOIS DÍGITOS, ELE SIMPLESMENTE É SOMADO NO TOTAL.


    for z in range(len(string_param)-3,-2,-2):
        # SEMELHANTE AO PRIMEIRO LOOP, PORÉM, ELE COMEÇA A PARTIR DO ANTEPENÚLTIMO
        # ITEM. DESSA FORMA, ELE PEGA APENAS OS QUE NÃO FORAM SOMADOS AINDA
        
        sum_db += int(string_param[z])
            #E AQUI ELES SÃO SOMADOS NO TOTAL.
    
    if sum_db % 10 == 0:
        # SEGUINDO O ALGORITMO DE Luhn, SE O MÓDULO DA DIVISÃO DESSA SOMA
        # TOTAL FOR IGUAL A ZERO, O NÚMERO DO CARTÃO É VÁLIDO.
        return print("VALID")
    else:
        # CASO CONTRÁRIO, INVÁLIDO.
        return print("INVALID")


     

card_validator(1)