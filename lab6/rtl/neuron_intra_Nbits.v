`timescale 1ns/1ps

module neuron_intra_Nbits # (
    parameter WIDTH = 8, N_INPUTS = 4
)(
   input reg signed [N_INPUTS*WIDTH-1:0] w
   input reg signed [N_INPUTS*WIDTH-1:0] x
   
   output reg signed [WIDTH-1:0] out
);

    wire signed [(N_INPUTS*WIDTH)*2 - 1:0] mult;
    wire signed [1:0] soma;


    generate
        genvar i;
        for (i = 0; i < N_INPUTS; i = i + 1)
        begin
            mult[i] = x[N_INPUTS*(i+1)-1:N_INPUTS*(i)] * w[N_INPUTS*(i+1)-1:N_INPUTS*(i)];
        end
    endgenerate

    assign soma[0] = mult [0] + mult[1];
    assign soma[1] = mult [2] + mult[3];

    assign out = soma[0] + soma[1];

    /*
    generate
        genvar i;
        genvar j;
        genvar k;
        for (i = 0; i < N_INPUTS; i = i + 1)
        begin
            mult[i] = x[N_INPUTS*(i+1)-1:N_INPUTS*(i)] * w[N_INPUTS*(i+1)-1:N_INPUTS*(i)];
        end
        for(i = clogb2(N_INPUTS) - 1; i >= 0 ; i = i-1)     // layer
        begin
            j = 2 ** (i-1)
            for(k = 0 ; k < j ; k = k+2)
            begin
                soma[k] = mult[k] + mult[k+1]
            end
        end
    endgenerate
    */

endmodule

