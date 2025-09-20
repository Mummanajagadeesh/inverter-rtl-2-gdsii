`timescale 1ns/1ps
`default_nettype none

module inverter_tb;

    // Testbench signals
    reg in;
    wire out;

    // Instantiate the inverter
    inverter uut (
        .in(in),
        .out(out)
    );

    // Test stimulus
    initial begin
        $display("Time\tin\tout");
        $monitor("%0t\t%b\t%b", $time, in, out);

        // Initialize input
        in = 0;
        #10 in = 1;
        #10 in = 0;
        #10 in = 1;
        #10;

        $display("Testbench finished");
        $finish;
    end

endmodule

`default_nettype wire
