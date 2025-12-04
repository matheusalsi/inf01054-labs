module ha (
    input  wire a,
    input  wire b,
    output wire s,
    output wire c
);
    assign s = a ^ b;
    assign c = a & b;
endmodule

module fa (
    input  wire a,
    input  wire b,
    input  wire cin,
    output wire s,
    output wire cout
);
    wire p = a ^ b;
    assign s    = p ^ cin;
    assign cout = (a & b) | (p & cin);
endmodule

module add16_rca (
    input  wire [15:0] a,
    input  wire [15:0] b,
    output wire [15:0] s
);
    wire c0;
    ha u_ha0 (.a(a[0]), .b(b[0]), .s(s[0]), .c(c0));

    wire [13:0] c; // carries for bits 1..14
    genvar i;
    generate
        for (i = 1; i < 15; i = i + 1) begin : GEN_FA
            fa u_fa (
                .a   (a[i]),
                .b   (b[i]),
                .cin (i == 1 ? c0 : c[i-2]),
                .s   (s[i]),
                .cout(c[i-1])
            );
        end
    endgenerate

    // MSB (bit 15)
    fa u_fa15 (.a(a[15]), .b(b[15]), .cin(c[13]), .s(s[15]), .cout(/*unused*/));
endmodule

module mult_array_exato (
    input  wire [7:0]  a,
    input  wire [7:0]  b,
    output wire [15:0] p
);
    // partial products (rows)
    wire [7:0] pp0 = a & {8{b[0]}};
    wire [7:0] pp1 = a & {8{b[1]}};
    wire [7:0] pp2 = a & {8{b[2]}};
    wire [7:0] pp3 = a & {8{b[3]}};
    wire [7:0] pp4 = a & {8{b[4]}};
    wire [7:0] pp5 = a & {8{b[5]}};
    wire [7:0] pp6 = a & {8{b[6]}};
    wire [7:0] pp7 = a & {8{b[7]}};

    // Shifts para manter a escala
    wire [15:0] r0 = {8'b0,         pp0                    }; // <<0
    wire [15:0] r1 = {7'b0,         pp1, 1'b0             }; // <<1
    wire [15:0] r2 = {6'b0,         pp2, 2'b0             }; // <<2
    wire [15:0] r3 = {5'b0,         pp3, 3'b0             }; // <<3
    wire [15:0] r4 = {4'b0,         pp4, 4'b0             }; // <<4
    wire [15:0] r5 = {3'b0,         pp5, 5'b0             }; // <<5
    wire [15:0] r6 = {2'b0,         pp6, 6'b0             }; // <<6
    wire [15:0] r7 = {1'b0,         pp7, 7'b0             }; // <<7

    // acumulação com RCA adders em cascata
    wire [15:0] s01;
    wire [15:0] s012;
    wire [15:0] s0123;
    wire [15:0] s01234;
    wire [15:0] s012345;
    wire [15:0] s0123456;
    wire [15:0] s01234567;

    add16_rca A01      (.a(r0),     .b(r1),     .s(s01));
    add16_rca A012     (.a(s01),    .b(r2),     .s(s012));
    add16_rca A0123    (.a(s012),   .b(r3),     .s(s0123));
    add16_rca A01234   (.a(s0123),  .b(r4),     .s(s01234));
    add16_rca A012345  (.a(s01234), .b(r5),     .s(s012345));
    add16_rca A0123456 (.a(s012345),.b(r6),     .s(s0123456));
    add16_rca A01234567(.a(s0123456),.b(r7),    .s(s01234567));

    assign p = s01234567; // resultado final (exato)
endmodule
