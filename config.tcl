# --- inverter/config.tcl ---

set ::env(DESIGN_NAME) "inverter"
set ::env(VERILOG_FILES) "$::env(DESIGN_DIR)/src/inverter.v"

# Clock settings (required for STA)
set ::env(CLOCK_PORT) "clk"
set ::env(CLOCK_PERIOD) 10.0

# Use absolute sizing (Option A)
set ::env(FP_SIZING) "absolute"
set ::env(DIE_AREA) "0 0 200 200"

# PDN settings
set ::env(FP_PDN_CORE_RING) 0
set ::env(FP_PDN_AUTO_ADJUST) 1
