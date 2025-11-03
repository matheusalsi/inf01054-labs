"""
Design Space Exploration Automation Script.

Este módulo executa automaticamente a exploração de espaço de projeto (DSE)
para o módulo neuron_intra_Nbits. Ele realiza as seguintes etapas:

1. Modifica o RTL base para diferentes parâmetros de N e N_INPUTS.
2. Executa a síntese usando o Cadence Genus.
3. Faz o parsing dos relatórios de área, potência e timing.
4. Registra os resultados em um arquivo CSV.

Cada passo está modularizado para permitir testes independentes.
"""

import os
import math
import csv
import re


def modify_clock_constraint(sdc_path, period_ns):
    """
    Modifica o arquivo SDC para alterar o período do clock.

    Parameters
    ----------
    sdc_path : str
        Caminho para o arquivo SDC.
    period_ns : float
        Período do clock em nanossegundos.
    """
    with open(sdc_path, 'r', encoding='utf-8') as sdc_file:
        sdc_content = sdc_file.read()
    
    # Substitui o período do clock no arquivo SDC
    sdc_content = re.sub(
        r'create_clock -name clock -period \d+\.?\d* \[get_ports clk\]',
        f'create_clock -name clock -period {period_ns} [get_ports clk]',
        sdc_content
    )
    
    with open(sdc_path, 'w', encoding='utf-8') as sdc_file:
        sdc_file.write(sdc_content)
    
    print(f"[OK] Clock period modificado para {period_ns} ns")


def find_minimum_period(sdc_path, initial_period=0.1):
    """
    Encontra o menor período de clock sintetizável através de busca iterativa.
    
    Parameters
    ----------
    sdc_path : str
        Caminho para o arquivo SDC.
    initial_period : float
        Período inicial em nanossegundos (bem baixo para começar).
        
    Returns
    -------
    float
        Menor período sintetizável em nanossegundos.
    """
    period = initial_period
    max_iterations = 20
    iteration = 0
    
    print(f"[INFO] Iniciando busca do período mínimo a partir de {period} ns...")
    
    while iteration < max_iterations:
        iteration += 1
        print(f"[INFO] Iteração {iteration}: testando período {period:.3f} ns")
        
        # Modifica o período no SDC
        modify_clock_constraint(sdc_path, period)
        
        # Executa síntese
        run_synthesis()
        
        # Verifica o slack
        _, _, _, slack = parse_reports('reports', 1)  # N_INPUTS não importa aqui para slack
        
        print(f"[INFO] Slack obtido: {slack:.3f} ps")
        
        if slack >= 0:
            print(f"[OK] Período mínimo encontrado: {period:.3f} ns")
            return period
        else:
            # Slack negativo: adiciona o valor absoluto do slack ao período
            # Slack está em ps, período em ns, então dividir por 1000
            period += abs(slack) / 1000.0
            print(f"[INFO] Slack negativo, aumentando período para {period:.3f} ns")
    
    print(f"[WARN] Período mínimo não encontrado após {max_iterations} iterações")
    return period


def modify_rtl(rtl_in_path, rtl_out_path, N, N_INPUTS):
    """
    Modifica o arquivo RTL base substituindo os parâmetros de design.

    Parametersa
    ----------
    rtl_in_path : str
        Caminho para o arquivo RTL base (ex: neuron_intra_Nbits_base.v).
    rtl_out_path : str
        Caminho de saída para o arquivo RTL modificado.
    N : int
        Valor do parâmetro N.
    N_INPUTS : int
        Valor do parâmetro N_INPUTS.
    """
    with open(rtl_in_path, 'r', encoding='utf-8') as rtl_file:
        rtl_lines = rtl_file.readlines()

    for idx, line in enumerate(rtl_lines):
        if 'parameter' in line:
            line = line.strip()
            _, param_name, _, param_val = line.split(' ')
            param_val = param_val.strip(",")

            if param_name == 'N':
                param_val = N
            elif param_name == 'N_INPUTS':
                param_val = N_INPUTS
            elif param_name == 'LOG_N_INPUTS':
                param_val = int(math.log2(N_INPUTS))

            new_line = f'    parameter {param_name} = {param_val}'
            if param_name != 'LOG_N_INPUTS':
                new_line += ','
            new_line += '\n'

            rtl_lines[idx] = new_line

    with open(rtl_out_path, 'w', encoding='utf-8') as rtl_file_out:
        rtl_file_out.writelines(rtl_lines)

    print(f"[OK] RTL modificado: N={N}, N_INPUTS={N_INPUTS}")


def run_synthesis():
    """
    Executa o script de síntese utilizando o Cadence Genus.

    Returns
    -------
    None
    """
    print("[INFO] Executando síntese com Genus...")
    result = os.system("genus -f genus_script.tcl")
    if result != 0:
        print("[ERRO] Execução do Genus falhou!")
    else:
        print("[OK] Síntese concluída.")


def parse_reports(report_dir, N_INPUTS):
    """Lê os relatórios de área, timing e potência e calcula throughput.

    Args:
        report_dir (str): Caminho para a pasta com os relatórios.
        N_INPUTS (int): Número de entradas (usado apenas para throughput).

    Returns:
        tuple: (area, power, throughput, slack)
    """
    area = 0.0
    power = 0.0
    throughput = 0.0
    slack = 0.0

    # Relatório de área
    area_path = os.path.join(report_dir, 'report_area_opt.rpt')
    try:
        with open(area_path, 'r') as f:
            for line in f:
                if line.strip().startswith('neuron_intra_Nbits'):
                    tokens = line.split()
                    try:
                        area = float(tokens[-3])
                        break
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        print("[WARN] report_area_opt.rpt não encontrado.")

   # Relatório de timing
    timing_path = os.path.join(report_dir, 'report_timing_opt.rpt')
    real_clk = 0.0
    slack = 0.0
    try:
        with open(timing_path, 'r') as f:
            content = f.read()
            
            # Busca por Required Time na linha que contém "Required Time:="
            required_match = re.search(r'Required Time:=\s*([+-]?\d+\.?\d*)', content)
            if required_match:
                real_clk = float(required_match.group(1))
            
            # Busca por Slack na linha que contém "Slack:="
            slack_match = re.search(r'Slack:=\s*([+-]?\d+\.?\d*)', content)
            if slack_match:
                slack = float(slack_match.group(1))
                # Considera slack muito próximo de zero como positivo (tolerância de 0.1 ps)
                if abs(slack) < 0.1:
                    slack = 0.0
                
    except FileNotFoundError:
        print("[WARN] report_timing_opt.rpt não encontrado.")

    # Relatório de potência
    power_path = os.path.join(report_dir, 'report_power_opt.rpt')
    try:
        with open(power_path, 'r') as f:
            for line in f:
                if line.strip().startswith('Subtotal'):
                    tokens = line.split()
                    try:
                        power = float(tokens[-2])  # Total power (W)
                        break
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        print("[WARN] report_power_opt.rpt não encontrado.")

    # Throughput não é calculado aqui mais, será calculado na main com o período real
    throughput = 0.0  # Será calculado posteriormente

    return area, power * 10**3, throughput, slack


def write_result_to_csv(csv_path, N, N_INPUTS, area, power, throughput, slack, min_period):
    """
    Adiciona uma linha com os resultados no arquivo CSV de exploração.

    Parameters
    ----------
    csv_path : str
        Caminho para o arquivo CSV de saída.
    N : int
        Valor do parâmetro N.
    N_INPUTS : int
        Valor do parâmetro N_INPUTS.
    area : float
        Área obtida da síntese.
    power : float
        Potência obtida da síntese.
    throughput : float
        Vazão calculada com base no período mínimo.
    slack : float
        Slack final obtido.
    min_period : float
        Menor período sintetizável em nanossegundos.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['N', 'N_INPUTS', 'Area(um^2)', 'Power(mW)', 'Throughput(Gops/s)', 'Slack(ps)', 'Min_Period(ns)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'N': N,
            'N_INPUTS': N_INPUTS,
            'Area(um^2)': area,
            'Power(mW)': power,
            'Throughput(Gops/s)': throughput,
            'Slack(ps)': slack,
            'Min_Period(ns)': min_period
        })


def main():
    """
    Executa o fluxo completo de Design Space Exploration (DSE).

    1. Modifica o RTL para diferentes valores de N e N_INPUTS.
    2. Encontra o menor período sintetizável para cada configuração.
    3. Executa a síntese final com o período otimizado.
    4. Faz parsing dos relatórios.
    5. Escreve os resultados no CSV.

    Returns
    -------
    None
    """
    rtl_path = '../rtl/neuron_intra_Nbits_base.v'
    rtl_out_path = '../rtl/neuron_intra_Nbits.v'
    sdc_path = '../constraints/constraints.sdc'
    csv_path = 'dse_results/results.csv'

    values_N = [8, 16, 64] 
    values_N_INP = [4, 8, 16]  

    os.makedirs("dse_results", exist_ok=True)

    for N in values_N:
        for N_INPUTS in values_N_INP:
            print(f"\n=== Sintetizando para N={N}, N_INPUTS={N_INPUTS} ===")

            # Etapa 1: Modifica o RTL
            modify_rtl(rtl_path, rtl_out_path, N, N_INPUTS)

            # Etapa 2: Encontra o menor período sintetizável
            min_period = find_minimum_period(sdc_path)

            # Etapa 3: Executa síntese final com período otimizado (para garantir)
            modify_clock_constraint(sdc_path, min_period)
            run_synthesis()

            # Etapa 4: Coleta resultados
            area, power, _, slack = parse_reports('reports', N_INPUTS)

            # Etapa 5: Calcula throughput com período real encontrado
            # Throughput = N_INPUTS operações / período (em segundos)
            # Convertendo para Gops/s: operações / (período_ns * 1e-9) / 1e9
            throughput = N_INPUTS / (min_period * 1e-9) / 1e9

            # Etapa 6: Salva resultados no CSV
            write_result_to_csv(csv_path, N, N_INPUTS, area, power, throughput, slack, min_period)

            print(f"[OK] Configuração concluída - Área: {area:.2f}, Potência: {power:.3f} mW, "
                  f"Throughput: {throughput:.3f} Gops/s, Período mín: {min_period:.3f} ns")

    print("\n[OK] Design Space Exploration concluída!")
    print(f"Resultados salvos em {csv_path}")


if __name__ == "__main__":
    main()