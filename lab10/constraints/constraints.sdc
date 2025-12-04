# SDC File for ULA Circuit

# ---------------------------------------------------------
# Define the primary clock
# ---------------------------------------------------------

# Define clock "clk" with a period of 2 ns (500 MHz)
create_clock -name clock -period 0.86 [get_ports clk]