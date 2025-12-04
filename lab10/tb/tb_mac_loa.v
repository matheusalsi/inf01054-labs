// ============================================
// Testbench para mac_loa (versão aproximada)
// ============================================
`timescale 1ns / 1ps

module tb_mac_loa();

    // Entradas
    reg clk;
    reg rst;
    reg [7:0] A;
    reg [7:0] B;
    reg [15:0] ACC_in;

    // Saída
    wire [15:0] OUT;

    // Instancia o DUT (Device Under Test)
    mac_loa dut (
        .clk(clk),
        .rst(rst),
        .A(A),
        .B(B),
        .ACC_in(ACC_in),
        .OUT(OUT)
    );

    // Geração de clock: período de 10ns (100 MHz)
    always #5 clk = ~clk;

    // Sequência de estímulos
    initial begin
        // Inicialização
        clk = 0;
        rst = 1;
        A = 0;
        B = 0;
        ACC_in = 0;

        // Reset ativo
        #10;
        rst = 0;

        // Teste 1
        A = 8'd5;
        B = 8'd10;
        ACC_in = 16'd0;
        #10;
        $display("Tempo=%0t | A=%d | B=%d | ACC_in=%d | OUT=%d", $time, A, B, ACC_in, OUT);

        // Teste 2
        A = 8'd12;
        B = 8'd3;
        ACC_in = OUT;
        #10;
        $display("Tempo=%0t | A=%d | B=%d | ACC_in=%d | OUT=%d", $time, A, B, ACC_in, OUT);

        // Teste 3
        A = 8'd7;
        B = 8'd15;
        ACC_in = OUT;
        #10;
        $display("Tempo=%0t | A=%d | B=%d | ACC_in=%d | OUT=%d", $time, A, B, ACC_in, OUT);

        // Teste 4
        A = 8'd25;
        B = 8'd4;
        ACC_in = OUT;
        #10;
        $display("Tempo=%0t | A=%d | B=%d | ACC_in=%d | OUT=%d", $time, A, B, ACC_in, OUT);

        #10;
        $display("Simulação finalizada.");
        $finish;
    end

endmodule
