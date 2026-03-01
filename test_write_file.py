from functions.write_file import write_file

def test_write_file():
    result_not_lorem = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"Result of writing to lorem.txt:\n{result_not_lorem}\n")
    result_morelorem = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"Result of writing to pkg/morelorem.txt:\n{result_morelorem}\n")
    result_temp = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"Result of writing to /tmp/temp.txt:\n{result_temp}\n")

test_write_file()
