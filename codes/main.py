from VRP_double_depot import *
import subprocess

program = r'C:\Programmieren\AUFSTIEG\Tum-solver\uav_trajectory_planner_0d82111.exe'
command = [program, 'plan', 'instance', r'C:\Programmieren\AUFSTIEG\codes\instance.json',
           r'C:\Programmieren\AUFSTIEG\codes\missions.json']
commandtest = [program, 'plan', 'instance', r'C:\Programmieren\AUFSTIEG\Tum-solver\instance.json',
           r'C:\Programmieren\AUFSTIEG\Tum-solver\missions.json']

try:
    # Führe das Programm aus und fange die Ausgabe ein
    result = subprocess.run(commandtest, text=True, capture_output=True)

    # Gib die Ausgabe des Programms aus
    print("Program output:\n", result.stdout)
    if result.stderr:
        print("Program error output:\n", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
