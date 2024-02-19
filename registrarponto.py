import datetime

def calcular_banco_horas(hora_chegada_manha, hora_saida_manha, hora_chegada_tarde, hora_saida_tarde):
    # Definir horários de referência
    turno_manha_inicio = datetime.time(8, 30)
    turno_tarde_fim = datetime.time(18, 0)

    # Inicializar variáveis
    extra = 0
    atraso = 0

    # Calcular minutos de atraso ou horas extras na chegada pela manhã
    if hora_chegada_manha < turno_manha_inicio:
        extra += (turno_manha_inicio.hour - hora_chegada_manha.hour) * 60 + turno_manha_inicio.minute - hora_chegada_manha.minute
    else:
        atraso += (hora_chegada_manha.hour - turno_manha_inicio.hour) * 60 + hora_chegada_manha.minute - turno_manha_inicio.minute

    # Calcular minutos de atraso ou horas extras na saída pela tarde
    if hora_saida_tarde < turno_tarde_fim:
        atraso += (turno_tarde_fim.hour - hora_saida_tarde.hour) * 60 + turno_tarde_fim.minute - hora_saida_tarde.minute
    else:
        extra += (hora_saida_tarde.hour - turno_tarde_fim.hour) * 60 + hora_saida_tarde.minute - turno_tarde_fim.minute

    # Calcular a diferença entre a saída da manhã e a entrada da tarde
    diferenca_manha_tarde = (hora_chegada_tarde.hour - hora_saida_manha.hour) * 60 + hora_chegada_tarde.minute - hora_saida_manha.minute

    # Se a diferença for maior que 60 minutos, adicionar ao atraso
    if diferenca_manha_tarde > 60:
        atraso += diferenca_manha_tarde - 60

    # Calcular saldo total de minutos de banco de horas
    if extra > atraso:
        saldo_banco_horas = extra - atraso
    else:
        saldo_banco_horas = -(atraso - extra)

    return saldo_banco_horas

def minutos_para_horas_e_minutos(minutos):
    # Converter minutos para horas e minutos
    horas = minutos // 60
    minutos_restantes = minutos % 60
    return horas, minutos_restantes

def ler_saldo_banco_horas():
    try:
        with open("registro_ponto.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            if linhas:
                for linha in reversed(linhas):
                    if linha.startswith("Banco de horas:"):
                        partes = linha.split(": ")[1].split(" horas e ")
                        horas = int(partes[0])
                        minutos = int(partes[1].split(" minutos")[0])
                        saldo_anterior = horas * 60 + minutos
                        return saldo_anterior
    except FileNotFoundError:
        pass
    return 0

def obter_data():
    data_input = input("Digite a data no formato dd/mm/aaaa (deixe em branco para data atual): ")
    
    if not data_input:  # Se o usuário não inserir uma data
        return datetime.datetime.now().strftime("%d/%m/%Y")  # Retornar a data atual no formato dd/mm/aaaa
    else:
        return data_input

def registrar_ponto():
    data = obter_data()
    hora_chegada_manha = datetime.datetime.strptime(input("Digite a hora de chegada pela manhã (HH:MM): "), '%H:%M').time()
    hora_saida_manha = datetime.datetime.strptime(input("Digite a hora de saída pela manhã (HH:MM): "), '%H:%M').time()
    hora_chegada_tarde = datetime.datetime.strptime(input("Digite a hora de chegada pela tarde (HH:MM): "), '%H:%M').time()
    hora_saida_tarde = datetime.datetime.strptime(input("Digite a hora de saída pela tarde (HH:MM): "), '%H:%M').time()

    # Calcular saldo anterior do banco de horas
    saldo_anterior = ler_saldo_banco_horas()

    # Calcular banco de horas
    saldo_atual = calcular_banco_horas(hora_chegada_manha, hora_saida_manha, hora_chegada_tarde, hora_saida_tarde)
    
    # Somar saldo atual ao saldo anterior
    saldo_total = saldo_anterior + saldo_atual

    # Converter saldo do banco de horas para horas e minutos
    if abs(saldo_total) >= 60:
        horas, minutos = minutos_para_horas_e_minutos(abs(saldo_total))
        if saldo_total < 0:
            horas *= -1  # Se o saldo for negativo, ajustar o sinal das horas
        print("Banco de horas:", horas, "horas e", minutos, "minutos")
    else:
        if saldo_total < 0:
            print("Banco de horas: -", abs(saldo_total), "minutos")
        else:
            print("Banco de horas:", saldo_total, "minutos")

    with open("registro_ponto.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Data: {data}\n")
        arquivo.write(f"Manhã: {hora_chegada_manha.strftime('%H:%M')} - {hora_saida_manha.strftime('%H:%M')}\n")
        arquivo.write(f"Tarde: {hora_chegada_tarde.strftime('%H:%M')} - {hora_saida_tarde.strftime('%H:%M')}\n")
        if abs(saldo_total) >= 60:
            arquivo.write(f"Banco de horas: {horas} horas e {minutos} minutos\n")  # Saldo do banco de horas em horas e minutos
        else:
            if saldo_total < 0:
                arquivo.write(f"Banco de horas: -{abs(saldo_total)} minutos\n")
            else:
                arquivo.write(f"Banco de horas: {saldo_total} minutos\n")
        arquivo.write("-" * 30 + "\n")

    print("Registro de ponto realizado com sucesso!")

def main():
    registrar_ponto()

if __name__ == "__main__":
    main()
