`timescale 1ns / 1ps

module im2col (
    input wire clk,
    input wire rst,
    input wire signed [7:0] Input0,
    input wire signed [7:0] Input1,
    input wire signed [7:0] Input2,
    input wire signed [7:0] Input3,

    output reg signed [31:0] IM2COL_BUFF_0,
    output reg signed [31:0] IM2COL_BUFF_1,
    output reg signed [31:0] IM2COL_BUFF_2

);

reg signed [3:0] kernel [7:0];
// wire stride = 1'd1;


localparam LW_WEIGHTS = 2'd0, FIRST_HALF = 2'd1, SECOND_HALF = 2'd2;

reg [1:0] state;

always @(posedge clk)
    if(rst)
        state <= LW_WEIGHTS;
    else
        case (state)
        LW_WEIGHTS: begin
            kernel [0] <= Input0;
            kernel [1] <= Input1;
            kernel [2] <= Input2;
            kernel [3] <= Input3;

            state <= FIRST_HALF;
        end
        FIRST_HALF: begin
          IM2COL_BUFF_0 [31:24] <= Input0 [7:0];
          IM2COL_BUFF_1 [31:24] <= Input1 [7:0];
          IM2COL_BUFF_2 [31:24] <= Input2 [7:0];

          IM2COL_BUFF_0 [23:16] <= Input1 [7:0];
          IM2COL_BUFF_1 [23:16] <= Input2 [7:0];
          IM2COL_BUFF_2 [23:16] <= Input3 [7:0];

            state <= SECOND_HALF;
        end
        SECOND_HALF: begin
          IM2COL_BUFF_0 [15:8] <= Input0 [7:0];
          IM2COL_BUFF_1 [15:8] <= Input1 [7:0];
          IM2COL_BUFF_2 [15:8] <= Input2 [7:0];

            IM2COL_BUFF_0 [7:0] <= Input1 [7:0];
            IM2COL_BUFF_1 [7:0] <= Input2 [7:0];
            IM2COL_BUFF_2 [7:0] <= Input3 [7:0];

            state <= FIRST_HALF;
        end
        endcase

endmodule
