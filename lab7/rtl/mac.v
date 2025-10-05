`timescale 1ns/1ps

module mac_Nbits # (
    parameter WIDTH = 8
)(
    input wire signed [WIDTH-1:0] w,
    input wire signed [WIDTH-1:0] x,
    input wire clk,
    input wire rst,
    input wire enable,

    output wire signed [WIDTH*2-1:0] out
);
    reg signed [WIDTH*2-1:0] acc;

    always @(posedge clk) begin
        if (rst) begin
            acc <= 0;
        end
        else if (enable) begin
            acc <= acc + w * x;
        end  
    end

    assign out = acc;

endmodule