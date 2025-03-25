# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the module
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0  # No toggle, no IO output
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1  # Release reset
    await ClockCycles(dut.clk, 1)

    dut._log.info("Testing Counter Mode")

    # Test counter increments without toggle
    dut.ui_in.value = 0b00  # No toggle, counter output mode
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x01  # Counter increments by 1

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x02  # Counter increments by 2

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x03  # Counter increments by 3

    dut._log.info("Testing Toggle Mode")

    # Enable toggle mode
    dut.ui_in.value = 0b01  # Toggle mode
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x04 & 0xFF  # Inverted counter value

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x05 & 0xFF  # Inverted counter value

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x06 & 0xFF  # Inverted counter value

    dut._log.info("Testing IO Output Mode")

    # Enable IO output mode
    dut.ui_in.value = 0b10  # IO mode enabled
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0x07  # Counter value on IO pins

    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0x08  # Counter value on IO pins

    dut._log.info("Testing Combined Toggle + IO Mode")

    # Enable both toggle + IO mode
    dut.ui_in.value = 0b11  # Toggle + IO mode
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x09 & 0xFF  # Inverted counter on output
    assert dut.uio_out.value == ~0x09 & 0xFF  # Inverted counter on IO

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x0A & 0xFF  # Inverted counter on output
    assert dut.uio_out.value == ~0x0A & 0xFF  # Inverted counter on IO

    dut._log.info("Test complete")
