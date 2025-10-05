`timescale 1ns/1ps

module tb_rca_NBits;

    parameter N = 8;

    reg  signed [N-1:0] A, B;
    wire signed [N-1:0] Sum;
    wire Cout;

    integer i;
    integer errors;

    // DUT
    rca_Nbits #(.N(N)) uut (
        .A(A),
        .B(B),
        .S(Sum),
        .Cout(Cout)
    );

    reg signed [N:0] exp_out;

    initial begin
        $display("Starting RCA random test with %0d-bit inputs", N);
        errors = 0;

        for (i = 0; i < 10; i = i + 1) begin
            // Gerar valores aleatórios (truncados para N bits)
            A = $random;
            B = $random;

            #5; // Espera propagação
            exp_out = A + B;

            if (Sum !== exp_out[N-1:0]) begin
                errors = errors + 1;
                $display("TEST FAILED");
                $display("A=%b B=%b Sum=%b. Sum should be %b", A, B, Sum, exp_out[N-1:0]);
            end
            else begin 
                $display("TEST PASSED");
                $display("A=%b B=%b Sum=%b.", A, B, Sum);
            end
        end

        if (errors == 0)
            $display("ALL TESTS PASSED ✅");
        else
            $display("TESTS FAILED ❌ (%0d errors)", errors);

        $finish;
    end
endmodule
