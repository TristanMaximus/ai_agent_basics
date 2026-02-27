from functions.get_files_info import get_files_info

def test_get_files_info():
    result_current_dir = get_files_info("calculator", ".")
    print(f"Result for current directory:\n{result_current_dir}")
    result_pkg_dir = get_files_info("calculator", "pkg")
    print(f"Result for 'pkg' directory:\n{result_pkg_dir}")
    result_bin_dir = get_files_info("calculator", "/bin")
    print(f"Result for '/bin' directory:\n{result_bin_dir}")
    result_parent_dir = get_files_info("calculator", "../")
    print(f"Result for '../' directory:\n{result_parent_dir}")


test_get_files_info()
