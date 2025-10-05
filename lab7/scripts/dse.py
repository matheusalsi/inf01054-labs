import math
import os

os.system("mkdir dse_results")

rtl_path = '../rtl/neuron_intra_Nbits_base.v'
rtl_out_path = '../rtl/neuron_intra_Nbits.v'

rtl_file = open(rtl_path, 'r')
rtl_lines = rtl_file.readlines()
rtl_file.close()

values_N = [8, 16, 64]
values_N_INP = [4, 8, 16] 

for val_N in values_N:
    for val_N_INP in values_N_INP:
        # PASSO 1 - modifica RTL
        for idx,line in enumerate(rtl_lines):
            if 'parameter' in line:
                line = line.strip() # removendo espaco dos dois lados
                print(line.split())

                dummy, param_name, dummy, param_val = line.split(' ')
                param_val = param_val.strip(",")

                if param_name == 'N':
                    param_val = val_N
                elif param_name == 'N_INPUTS':
                    param_val = val_N_INP
                elif param_name == 'LOG_N_INPUTS':
                    param_val = int(math.log2(val_N_INP))

                new_line = f'parameter {param_name} = {param_val}'

                if param_name != 'LOG_N_INPUTS':
                    new_line += ','
                
                rtl_lines[idx] = new_line

        rtl_file_out = open(rtl_out_path, 'w')
        rtl_file_out.writelines(rtl_lines)
        rtl_file_out.close()
        
        # PASSO 2 - roda a síntese

        os.system("genus -f genus_script.tcl")

        # PASSO 3 - coleta resultados

        # catch specific reports (area_opt, power_opt, timing_opt)

        # estimate the best clock



        # post processing (throughput, power, area)

        throughput = (mult / 2) + qnt_sums / best_clock

        # create a csv file that compare the results of different combinations
        
        