`timescale 1ns/1ps

module half_adder 
(
    input wire a, b,
    output wire sum, cout
);
assign sum = a ^ b;
assign cout = a & b;
endmodule

module full_adder 
(
    input wire a, b, cin,
    output wire sum, cout
);
assign sum = a ^ b ^ cin;
assign cout = (a & b) | (a & cin) | (b & cin);

endmodule

module rca_Nbits #(
    parameter N = 4
)
(
    input wire [N-1:0] A,
    input wire [N-1:0] B,
    output wire [N-1:0] S,
    output wire Cout
);

    wire [N-1:0] c;

    half_adder ha (.a(A[0]),.b(B[0]),.sum(S[0]), .cout(c[0]));
    generate
        genvar i;
        for (i = 1; i < N; i = i + 1)
        begin
            full_adder fa (.a(A[i]), .b(B[i]), .cin(c[i-1]),  .sum(S[i]), .cout(c[i]));
        end
    endgenerate
    assign Cout = c[N-2];


endmodule