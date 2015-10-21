library IEEE;
use IEEE.std_logic_1164.all;

entity pfbfft_core is
  port (
    ce_1: in std_logic; 
    clk_1: in std_logic; 
    pol1: in std_logic_vector(23 downto 0); 
    pol2: in std_logic_vector(23 downto 0); 
    pol3: in std_logic_vector(23 downto 0); 
    pol4: in std_logic_vector(23 downto 0); 
    shift: in std_logic_vector(8 downto 0); 
    sync: in std_logic; 
    of_x0: out std_logic_vector(1 downto 0); 
    out0: out std_logic_vector(35 downto 0); 
    out1: out std_logic_vector(35 downto 0); 
    out2: out std_logic_vector(35 downto 0); 
    out3: out std_logic_vector(35 downto 0); 
    sync_out: out std_logic
  );
end pfbfft_core;

architecture structural of pfbfft_core is
begin
end structural;

