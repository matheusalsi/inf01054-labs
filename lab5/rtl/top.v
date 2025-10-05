`timescale 1ns/1ps

module top # (
    parameter WIDTH = 8
)(
    input wire signed [WIDTH -1: 0] x, w,
    input wire clk, rst, enable,

    output wire signed [WIDTH - 1 :0] out
);
    wire signed [WIDTH*2-1:0] out_mac;
    wire signed [WIDTH*2-1:0] out_relu;

    mac_Nbits #(
      .WIDTH(WIDTH)
    ) mac_inst (
      .clk(clk),
      .rst(rst),
      .enable (enable),
      .w  (w),
      .x  (x),
      .out(out_mac)
    ) ;

    relu #(
      .WIDTH(WIDT*2)
    ) relu_inst (
      .in(out_mac)
      .out(out_relu)
    );


    assign out = out_relu[WIDTH*2-1:WIDTH-1];

endmodule