import subprocess

scripts = ["knuth_minimax\mastermind.py", "knuth_minimax\mastermind_no_white.py", "knuth_minimax\mastermind_no_black.py"]

for script in scripts:
    result = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )
    print(f"--- Output of {script} ---")
    print(result.stdout)

    if result.stderr:                       
        print("ERROR:")
        print(result.stderr)
    
