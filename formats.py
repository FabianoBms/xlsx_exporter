

formatar_cnpj = lambda cnpj: "{}.{}.{}/{}-{}".format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
formatar_string_para__cpf = lambda x: f"{x[:3]}.{x[3:6]}.{x[6:9]}-{x[9:]}"