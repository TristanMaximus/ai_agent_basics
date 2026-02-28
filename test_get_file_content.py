from functions.get_file_content import get_file_content
from config import MAX_CHARS

def test_get_file_content():
    lorem_content = get_file_content("calculator", "lorem.txt")
    truncated = "truncated at" in lorem_content and str(MAX_CHARS) in lorem_content and "characters" in lorem_content
    print(f"Result for lorem.txt:\nContent length: {len(lorem_content)}. Content truncated: {truncated}. Max content length to read: {MAX_CHARS}\n")
    main_content = get_file_content("calculator", "main.py")
    print(f"main.py content:\n{main_content}\n")
    calculator_content = get_file_content("calculator", "pkg/calculator.py")
    print(f"pkg/calculator.py content:\n{calculator_content}\n")
    error_cat_content = get_file_content("calculator", "/bin/cat") # (this should return an error string)
    print(f"/bin/cat content (error):\n{error_cat_content}\n")
    error_does_not_exist_content = get_file_content("calculator", "pkg/does_not_exist.py") # (this should return an error string)
    print(f"pkg/does_not_exist.py content (error):\n{error_does_not_exist_content}\n")


test_get_file_content()
