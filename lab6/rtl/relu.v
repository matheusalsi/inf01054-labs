`timescale 1ns/1ps

module relu # (
    parameter WIDTH = 8
)(
    input signed wire [WIDTH-1:0] in,
    output signed wire [WIDTH-1:0] out
);
    always @(*) begin
        if(in < 0) begin
            out <= 0;
        end
        else begin
            out <= in;
        end
    end
endmodule