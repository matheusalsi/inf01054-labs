# SDC File for ULA Circuit

# ---------------------------------------------------------
# Define the primary clock
# ---------------------------------------------------------

# Define clock "clk" with a period of 2 ns (500 MHz)
create_clock -name CLK -period 1.75 [get_ports clk]
set_input_delay 0.1 -clock CLK [all_inputs]
set_output_delay 0.1 -clock CLK [all_outputs]