from functions.run_python_file import run_python_file

def test_run_python_file():
    # should print the calculator's usage instructions
    calc_main_result = run_python_file("calculator", "main.py")
    print(f"Run result of calculator/main.py:\n{calc_main_result}\n")

    # should run the calculator... which gives a kinda nasty rendered result
    calc_with_params_results = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"Run result of calculator/main.py with 3 + 5:\n{calc_with_params_results}\n")

    # should run the calculator's tests successfully
    calc_tests_results = run_python_file("calculator", "tests.py")
    print(f"Run result of calculator/tests.py:\n{calc_tests_results}\n")

    # this should return an error
    outside_workdir_script_result = run_python_file("calculator", "../main.py")
    print(f"Run result of calculator/../main.py:\n{outside_workdir_script_result}\n")

    # this should return an error
    non_existent_script_result = run_python_file("calculator", "nonexistent.py")
    print(f"Run result of calculator/nonexistent.py:\n{non_existent_script_result}\n")

    # this should return an error
    non_python_script_result = run_python_file("calculator", "lorem.txt")
    print(f"Run result of calculator/lorem.txt:\n{non_python_script_result}\n")

test_run_python_file()
