#PlotGearshifft
#Two inputs
#input arguments: name of the file, #tests, memorymode: Inplace/Outplace, Complexity: Real/Complex, Precision: float/double, Dimension: 1/2/3, Kind: oddshape/powerof2, X: signal size, Y: Time of the selected stage 

#How to run and check the distribution of stages
python plotresults.py Results/2018_09_11-19\:57\:48-gnu_wc.csv,Results/2018_09_13-13:32:01-knl_wc.csv 1 '"Inplace"' '"Real"' '"double"' '"1"' '"powerof2"' nx Time_FFT_ms

#How to plot speedup and time stage
#GPUs (Comparison with P100)
python plotresults.py Results/GPUs/p100_cufft8061_gcc5.3.0_SL7.4.csv,Results/GPUs/k80_cufft8061_gcc5.3.0_RHEL6.8.csv,Results/GPUs/p100_cufft_gcc5.3.0_SL7.4.csv,Results/GPUs/v100_cufft_gcc5.3.0_SL7.4.csv 1 '"Inplace"' '"Real"' '"double"' '"1"' '"powerof2"' nx Time_FFT_ms

#CPUs
python plotresults.py Results/2018_09_11-19:57:48-gnu_nw.csv,Results/2018_09_11-19:57:48-gnu_wc.csv,Results/2018_09_13-13:32:01-knl_nw.csv,Results/2018_09_13-13:32:01-knl_wc.csv 1 '"Inplace"' '"Real"' '"double"' '"1"' '"powerof2"' nx Time_PlanInitInv_m
