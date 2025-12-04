`timescale 1ns/1ps


module tb_im2col;


   reg clk;
   reg rst;


   reg  signed [7:0]  PIXEL_0;
   reg  signed [7:0]  PIXEL_1;
   reg  signed [7:0]  PIXEL_2;
   reg  signed [7:0]  PIXEL_3;


   wire signed [31:0] BUFF_0;
   wire signed [31:0] BUFF_1;
   wire signed [31:0] BUFF_2;


   im2col dut (
       .clk(clk),
       .rst(rst),
       .Input0(PIXEL_0),
       .Input1(PIXEL_1),
       .Input2(PIXEL_2),
       .Input3(PIXEL_3),
       .IM2COL_BUFF_0(BUFF_0),
       .IM2COL_BUFF_1(BUFF_1),
       .IM2COL_BUFF_2(BUFF_2)
   );


   `define ASSERT_EQ(name, actual, expected) \
       if ((actual) !== (expected)) begin \
           $display("ASSERT FAILED: %s = %0d, expected %0d", name, actual, expected); \
           $finish; \
       end


   always #5 clk = ~clk;


   initial begin
       $dumpfile("wave.vcd");
       $dumpvars(0, tb_im2col);
   end


   initial begin
       clk = 0;
       rst = 1;
       #10 rst = 0;


       // valores 1
       PIXEL_0 = 8'sd5;
       PIXEL_1 = 8'sd6;
       PIXEL_2 = 8'sd3;
       PIXEL_3 = -8'sd1;
       #10;


       // valores 2
       PIXEL_0 = 8'sd5;
       PIXEL_1 = 8'sd2;
       PIXEL_2 = 8'sd1;
       PIXEL_3 = 8'sd3;
       #10;


       // valores 3
       PIXEL_0 = 8'sd3;
       PIXEL_1 = 8'sd6;
       PIXEL_2 = 8'sd2;
       PIXEL_3 = -8'sd5;
       #10;


       `ASSERT_EQ("BUFF_0", BUFF_0, 32'sb00000101000000100000001100000110);
       `ASSERT_EQ("BUFF_1", BUFF_1, 32'sb00000010000000010000011000000010);
       `ASSERT_EQ("BUFF_2", BUFF_2, 32'sb00000001000000110000001011111011);


       $display("Simulação finalizada.");
       $finish;
   end


endmodule
