## How it works

The tt_um_simple_counter module is an 8-bit counter with a toggle functionality. It operates in two primary modes based on the input pins:

Counter mode:
The counter increments on each clock cycle.
The output pins (uo_out) display either the counter value or its inverted value based on the toggle mode.
Toggle mode:
When the toggle enable pin (ui[0]) is high, the counter toggles between its normal and inverted value on the output pins.
The counter output enable pin (ui[1]) controls whether the counter value is displayed on the bidirectional pins (uio).

## How to test

1. Basic Counter Mode:

Set ui[0] = 0 and ui[1] = 0.
The output pins (uo_out) display the normal counter value, incrementing on each clock cycle.
The bidirectional pins (uio) remain in High-Z state.

2. Counter Output Mode:

Set ui[0] = 0 and ui[1] = 1.
The output pins display the counter value.
The bidirectional pins output the counter value as well.

3. Toggle Mode (Inverted):

Set ui[0] = 1 and ui[1] = 0.
The counter toggles between normal and inverted values on each clock cycle.
The bidirectional pins remain in High-Z state.

4. Toggle + Output Mode:

Set ui[0] = 1 and ui[1] = 1.
The output pins display the inverted counter value.
The bidirectional pins output the normal counter value.
