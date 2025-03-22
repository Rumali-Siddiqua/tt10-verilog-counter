`default_nettype none
`timescale 1ns / 1ps

/* 
 * Testbench for tt_um_simple_counter
 * This testbench just instantiates the module and makes some convenient wires 
 * that can be driven / tested by the cocotb `test.py`.
 */
module tb ();

  // Dump the signals to a VCD file for waveform analysis
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;  // Allow some time for initialization
  end

  // Wire up the inputs and outputs
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;      // Power supply for gate-level simulation
  wire VGND = 1'b0;      // Ground
`endif

  // Instantiate the `tt_um_simple_counter` module
  tt_um_simple_counter user_project (
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (0=input, 1=output)
      .ena    (ena),      // Always high when powered
      .clk    (clk),      // Clock signal
      .rst_n  (rst_n)     // Active low reset
  );

endmodule
