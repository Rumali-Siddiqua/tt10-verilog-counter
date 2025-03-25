# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting test...")

    # Set up clock
    clock = Clock(dut.clk, 10, units="us")  # 100 kHz clock
    cocotb.start_soon(clock.start())

    # Reset the module
    dut.ena.value = 1
    dut.ui_in.value = 0  # No toggle, counter mode
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)  # Hold reset for 10 cycles

    # Release reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Check counter increments correctly
    dut._log.info("Testing Counter Mode")

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x01, f"Counter mismatch: {dut.uo_out.value} != 0x01"

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x02, f"Counter mismatch: {dut.uo_out.value} != 0x02"

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x03, f"Counter mismatch: {dut.uo_out.value} != 0x03"

    # Test toggle mode
    dut._log.info("Testing Toggle Mode")
    dut.ui_in.value = 0b01  # Enable toggle mode

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x04 & 0xFF, f"Toggle mismatch: {dut.uo_out.value} != ~0x04"

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x05 & 0xFF, f"Toggle mismatch: {dut.uo_out.value} != ~0x05"

    # Test IO output mode
    dut._log.info("Testing IO Output Mode")
    dut.ui_in.value = 0b10  # Enable IO output mode

    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0x06, f"IO mismatch: {dut.uio_out.value} != 0x06"

    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0x07, f"IO mismatch: {dut.uio_out.value} != 0x07"

    # Test combined toggle + IO mode
    dut._log.info("Testing Combined Mode")
    dut.ui_in.value = 0b11  # Enable both toggle and IO output

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x08 & 0xFF, f"Combined mode mismatch: {dut.uo_out.value} != ~0x08"
    assert dut.uio_out.value == ~0x08 & 0xFF, f"Combined IO mismatch: {dut.uio_out.value} != ~0x08"

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == ~0x09 & 0xFF, f"Combined mode mismatch: {dut.uo_out.value} != ~0x09"
    assert dut.uio_out.value == ~0x09 & 0xFF, f"Combined IO mismatch: {dut.uio_out.value} != ~0x09"

    dut._log.info("Test completed successfully!")
