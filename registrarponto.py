# -*- coding: utf-8 -*-

import datetime

def calcular_horas_trabalhadas(entrada_manha, saida_manha, entrada_tarde, saida_tarde):
    hora_inicio_manha = datetime.datetime.strptime(entrada_manha, "%H:%M")
    hora_fim_manha = datetime.datetime.strptime(saida_manha, "%H:%M")
    hora_inicio_tarde = datetime.datetime.strptime(entrada_tarde, "%H:%M")
    hora_fim_tarde = datetime.datetime.strptime(saida_tarde, "%H:%M")

    total_horas_manha = (hora_fim_manha - hora_inicio_manha).total_seconds() / 3600
    total_horas_tarde = (hora_fim_tarde - hora_inicio_tarde).total_seconds() / 3600

    horas_trabalhadas = total_horas_manha + total_horas_tarde
    return horas_trabalhadas

def calcular_banco_de_horas(horas_trabalhadas):
    horas_desejadas = 8.5
    diferenca = horas_trabalhadas - horas_desejadas
    horas = int(diferenca)
    minutos = round((diferenca - horas) * 60)  # Arredonda para o minuto mais próximo
    if diferenca > 0:
        return f"+{horas:02}:{minutos:02}"
    elif diferenca < 0:
        return f"-{abs(horas):02}:{abs(minutos):02}"
    else:
        return "+ 00:00"

def salvar_registro(registro):
    with open("registro_ponto.txt", "a", encoding="utf-8") as file:
        file.write(registro + "\n")

def main():
    data = input("Digite a data (dd/mm/aaaa) ou pressione Enter para usar a data atual: ")
    if not data:  # Se nenhum valor for fornecido, use a data atual
        data = datetime.datetime.now().strftime("%d/%m/%Y")
    entrada_manha = input("Digite a hora de entrada da manhã (HH:MM): ")
    saida_manha = input("Digite a hora de saída da manhã (HH:MM): ")
    entrada_tarde = input("Digite a hora de entrada da tarde (HH:MM): ")
    saida_tarde = input("Digite a hora de saída da tarde (HH:MM): ")

    horas_trabalhadas = calcular_horas_trabalhadas(entrada_manha, saida_manha, entrada_tarde, saida_tarde)
    saldo_horas = calcular_banco_de_horas(horas_trabalhadas)

    registro = f"Data: {data}\nManhã: {entrada_manha} - {saida_manha}\nTarde: {entrada_tarde} - {saida_tarde}\nBanco de horas: {saldo_horas}\n------------------------------"
    salvar_registro(registro)

    print(f"Banco de horas para o dia {data}: {saldo_horas}")

    print("Registro salvo com sucesso!")

if __name__ == "__main__":
    main()
