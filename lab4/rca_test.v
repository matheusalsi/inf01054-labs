`timescale 1ns/1ps

module tb_rca_4bits();

  reg  [3:0] a, b;
  reg        cin;
  wire [3:0] s;
  wire       cout;

  // Instantiate the DUT (Device Under Test)
  rca_4bits dut (
    .a(a),
    .b(b),
    .cin(cin),
    .s(s),
    .cout(cout)
  );

  initial begin

    // Apply test vectors
    $display("Time | a    b    cin | sum   cout");
    $display("-----------------------------------");

    a = 4'b0000; b = 4'b0000; cin = 0; #10;
    $display("%4t | %b %b %b | %b %b", $time, a, b, cin, s, cout);

    a = 4'b0101; b = 4'b0011; cin = 0; #10;
    $display("%4t | %b %b %b | %b %b", $time, a, b, cin, s, cout);

    a = 4'b1111; b = 4'b0001; cin = 0; #10;
    $display("%4t | %b %b %b | %b %b", $time, a, b, cin, s, cout);

    a = 4'b1010; b = 4'b0101; cin = 1; #10;
    $display("%4t | %b %b %b | %b %b", $time, a, b, cin, s, cout);

    a = 4'b1111; b = 4'b1111; cin = 1; #10;
    $display("%4t | %b %b %b | %b %b", $time, a, b, cin, s, cout);

    $finish;
  end

endmodule