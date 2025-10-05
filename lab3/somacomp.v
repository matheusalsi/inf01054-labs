`timescale 1ns/1ps
// Code your design here
module soma_comp #(
	parameter TAM = 4
)
(
	input wire [TAM-1:0]a, 
	input wire [TAM-1:0]b,
	output reg [TAM-1:0]sum
);

	always @(*) begin
		sum = a + b;
	end

endmodule