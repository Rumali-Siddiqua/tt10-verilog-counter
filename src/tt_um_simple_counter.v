/*
 * tt_um_simple_counter.v
 *
 * Simple counter with toggle functionality
 *
 * Author: Rumali Siddiqua
 */

`default_nettype none

module tt_um_simple_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Internal signals
    reg rst_n_i;              // Synchronized reset
    reg [7:0] counter;        // 8-bit counter
    reg toggle;               

    // Reset synchronization
    always @(posedge clk or negedge rst_n)
        if (~rst_n) 
            rst_n_i <= 1'b0;
        else 
            rst_n_i <= 1'b1;

    // Counter and toggle logic
    always @(posedge clk or negedge rst_n_i)
        if (~rst_n_i) begin
            counter <= 8'h00;
            toggle  <= 1'b0;
        end else begin
            counter <= counter + 1;
            if (ui_in[0])          // Toggle mode on ui_in[0] high
                toggle <= ~toggle;
        end

    // Output assignments
    assign uo_out  = toggle ? counter : ~counter;   // Toggle mode: invert or show counter
    assign uio_out = ui_in[1] ? counter : 8'h00;    // Output counter if ui_in[1] is high
    assign uio_oe  = ui_in[1] ? 8'hFF : 8'h00;      // Enable outputs when ui_in[1] is high

    // Avoid linter warnings for unused pins
    wire _unused_pins = ena;

endmodule  // tt_um_simple_counter

