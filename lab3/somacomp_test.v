`timescale 1ns/1ps

module soma_comp_test;

    localparam TAM=4;

    reg [TAM-1:0] a, b;
    wire [TAM-1:0] s;

    soma_comp DUT(a,b,s);

    initial
    begin
        a <= 4'b1010;
        b <= 4'b0101;
        #10;
        $display("At time %0d a=%b b=%b s=%b",
               $time, a, b, s);

        a <= 4'b0001;
        b <= 4'b0011;
        #10;
        $display("At time %0d a=%b b=%b s=%b",
               $time, a, b, s);
        
    end
endmodule
