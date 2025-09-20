// src/inverter.v
`default_nettype none

module inverter (
    input  wire in,
    output wire out
);
    assign out = ~in;
endmodule

`default_nettype wire
