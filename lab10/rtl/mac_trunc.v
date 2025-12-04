`timescale 1ns / 1ps

module mac_trunc (
    input  wire         clk,       // clock
    input  wire         rst,       // reset síncrono
    input  wire [7:0]   A,         // operando A
    input  wire [7:0]   B,         // operando B
    input  wire [15:0]  ACC_in,    // acumulador atual
    output reg  [15:0]  OUT        // saída truncada
);

    // Multiplicação exata
    wire [15:0] mult_result;
    assign mult_result = A * B;

    localparam TRUNC_BITS = 4; // número de bits ignorados (parte inferior) quanto maior o número mais impreciso o resultado fica


    wire [15-TRUNC_BITS:0] mult_trunc = mult_result[15:TRUNC_BITS];   // (15-TRUNC_BITS) bits superiores
    wire [15-TRUNC_BITS:0] acc_trunc  = ACC_in[15:TRUNC_BITS];        // (15-TRUNC_BITS) bits superiores

    wire [15-TRUNC_BITS:0] sum_trunc = mult_trunc + acc_trunc;
    // Acumulação síncrona
    always @(posedge clk or posedge rst) begin
        if (rst)
            OUT <= 16'd0;
        else
            // Reconstrói a saída para 16 bits, preenchendo os bits inferiores com zeros
            OUT <= {sum_trunc, {TRUNC_BITS{1'b0}}};
    end
    
endmodule
