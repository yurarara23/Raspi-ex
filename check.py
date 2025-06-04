
import time
import subprocess
import sys
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout.strip()

def GetCpuFreq():
    output = run_cmd('vcgencmd measure_clock arm')
    return int(output.split('=')[1])  # Hz単位

def GetGpuFreq():
    output = run_cmd('vcgencmd measure_clock core')
    return int(output.split('=')[1])  # Hz単位

def GetCpuTemp():
    output = run_cmd('vcgencmd measure_temp')
    return output.split('=')[1]

def GetGpuTemp():
    output = run_cmd('vcgencmd measure_temp')
    return output.split('=')[1]

def GetDevVolt():
    return run_cmd('vcgencmd measure_volts')

def GetGpuVolt():
    return run_cmd('vcgencmd measure_volts core')

def GetMemUsage():
    mem_info = run_cmd("free -m").splitlines()
    mem_values = mem_info[1].split()
    total, used, free = int(mem_values[1]), int(mem_values[2]), int(mem_values[3])
    return total, used, free

def GetCpuStat():
    lines = run_cmd("cat /proc/stat | grep '^cpu'").splitlines()
    TckList = []
    for line in lines:
        items = line.split()
        TckIdle = int(items[4])
        TckBusy = sum(map(int, items[1:4]))
        TckAll  = TckBusy + TckIdle
        TckList.append([TckBusy, TckAll])
    return TckList

class CpuUsage:
    def __init__(self):
        self._TckList = GetCpuStat()

    def get(self):
        TckListPre = self._TckList
        TckListNow = GetCpuStat()
        self._TckList = TckListNow
        CpuRateList = []
        for (TckNow, TckPre) in zip(TckListNow, TckListPre):
            TckDiff = [Now - Pre for (Now, Pre) in zip(TckNow, TckPre)]
            TckBusy = TckDiff[0]
            TckAll = TckDiff[1]
            CpuRate = int(TckBusy * 100 / TckAll) if TckAll > 0 else 0
            CpuRateList.append(CpuRate)
        return CpuRateList

if __name__ == '__main__':
    gCpuUsage = CpuUsage()

    for _ in range(10000):
        time.sleep(1)

        cpu_rates = gCpuUsage.get()
        total_cpu = cpu_rates[0]
        core_cpus = cpu_rates[1:]

        cpu_temp = GetCpuTemp()
        cpu_freq = GetCpuFreq() // 1_000_000
        gpu_freq = GetGpuFreq() // 1_000_000
        cpu_volt = GetDevVolt()
        gpu_volt = GetGpuVolt()
        total_mem, used_mem, free_mem = GetMemUsage()

        print(f"[CPU] {cpu_volt} {cpu_freq:>4}MHz {cpu_temp}  CPU使用率: {total_cpu:>3}%")
        print(f"[GPU] {gpu_volt} {gpu_freq:>4}MHz")
        print(f"[MEM] Total: {total_mem}MB  Used: {used_mem}MB  Free: {free_mem}MB")
        print(f"[CORES] {' '.join([f'Core{i}:{v}%' for i, v in enumerate(core_cpus)])}")
        print("-" * 60)
