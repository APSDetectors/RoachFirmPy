gui_open_window Wave
gui_sg_create testclk_group
gui_list_add_group -id Wave.1 {testclk_group}
gui_sg_addsignal -group testclk_group {testclk_tb.test_phase}
gui_set_radix -radix {ascii} -signals {testclk_tb.test_phase}
gui_sg_addsignal -group testclk_group {{Input_clocks}} -divider
gui_sg_addsignal -group testclk_group {testclk_tb.CLK_IN1}
gui_sg_addsignal -group testclk_group {{Output_clocks}} -divider
gui_sg_addsignal -group testclk_group {testclk_tb.dut.clk}
gui_list_expand -id Wave.1 testclk_tb.dut.clk
gui_sg_addsignal -group testclk_group {{Counters}} -divider
gui_sg_addsignal -group testclk_group {testclk_tb.COUNT}
gui_sg_addsignal -group testclk_group {testclk_tb.dut.counter}
gui_list_expand -id Wave.1 testclk_tb.dut.counter
gui_zoom -window Wave.1 -full
