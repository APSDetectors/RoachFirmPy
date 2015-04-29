gui_open_window Wave
gui_sg_create mmcm_mkid_group
gui_list_add_group -id Wave.1 {mmcm_mkid_group}
gui_sg_addsignal -group mmcm_mkid_group {mmcm_mkid_tb.test_phase}
gui_set_radix -radix {ascii} -signals {mmcm_mkid_tb.test_phase}
gui_sg_addsignal -group mmcm_mkid_group {{Input_clocks}} -divider
gui_sg_addsignal -group mmcm_mkid_group {mmcm_mkid_tb.CLK_IN1}
gui_sg_addsignal -group mmcm_mkid_group {{Output_clocks}} -divider
gui_sg_addsignal -group mmcm_mkid_group {mmcm_mkid_tb.dut.clk}
gui_list_expand -id Wave.1 mmcm_mkid_tb.dut.clk
gui_sg_addsignal -group mmcm_mkid_group {{Status_control}} -divider
gui_sg_addsignal -group mmcm_mkid_group {mmcm_mkid_tb.LOCKED}
gui_sg_addsignal -group mmcm_mkid_group {{Counters}} -divider
gui_sg_addsignal -group mmcm_mkid_group {mmcm_mkid_tb.COUNT}
gui_sg_addsignal -group mmcm_mkid_group {mmcm_mkid_tb.dut.counter}
gui_list_expand -id Wave.1 mmcm_mkid_tb.dut.counter
gui_zoom -window Wave.1 -full
