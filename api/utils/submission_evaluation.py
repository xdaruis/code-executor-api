import subprocess
import os
import tempfile
import secrets
import shutil
import stat
import ast
import os

RETURN_CODE_TIMEOUT = 124
MAX_TIME_LIMIT = 15

def test_submission_script(language, inputs, code, number_of_testcases, time_limit):
    if time_limit > MAX_TIME_LIMIT:
        time_limit = MAX_TIME_LIMIT
    folder_path = create_temporary_directory()
    random_name = secrets.token_hex(16)
    if language == "python":
        file_extension = "py"
        execute_command = f"python {folder_path}/{random_name}.py"
        try:
            ast.parse(code)
        except SyntaxError as se:
            return ['Failed Compilation!']
    elif language == "cpp":
        file_extension = "cpp"
        compile_command = f"g++ {folder_path}/{random_name}.cpp -o {folder_path}/{random_name}.exe"
        execute_command = f"{folder_path}/{random_name}.exe"
    elif language == "java":
        file_extension = "java"
        random_name = "Main"
        compile_command = f"javac {folder_path}/{random_name}.java"
        execute_command = f"java -classpath {folder_path} {random_name}"
    else:
        return ["Language not supported!"]
    file_path = f"{folder_path}/{random_name}.{file_extension}"
    write_to_file(file_path, code)
    try:
        if language == "cpp" or language == "java":
            subprocess.run(compile_command, shell=True, check=True)
        results = run_tests(number_of_testcases, execute_command, inputs, time_limit, folder_path, random_name)
    except subprocess.CalledProcessError as e:
        results = ['Failed Compilation!']
    remove_directory(folder_path)
    return results

def create_temporary_directory():
    try:
        random_hex_name = secrets.token_hex(16)
        temp_directory_path = os.path.join(tempfile.gettempdir(), random_hex_name)
        os.makedirs(temp_directory_path)
        os.chmod(temp_directory_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        return temp_directory_path
    except:
        return None

def remove_directory(path):
    try:
        shutil.rmtree(path)
    except:
        pass

def run_tests(number_of_testcases, execute_command, inputs, time_limit, folder_path, random_name):
    results = []
    for act_test in range(number_of_testcases):
        write_to_file(f"{folder_path}/input.txt", inputs[act_test])
        try:
            execute_program = f"timeout {time_limit} {execute_command} < {folder_path}/input.txt > {folder_path}/output.txt"
            subprocess.run(execute_program, shell=True, check=True)
            with open(f"{folder_path}/output.txt", 'r') as output_file:
                program_output = output_file.read().strip()
                results.append(program_output)
        except subprocess.CalledProcessError as e:
            if e.returncode == RETURN_CODE_TIMEOUT:
                results.append(f"{act_test + 1}.Time Limit Exceeded")
            else:
                results.append(f"Internal Server Error!")
    return results

def write_to_file(path, text):
    with open(path, 'w') as file:
        file.write(text)

if __name__ == "__main__":

    language = os.environ.get('LANGUAGE', '')
    code = os.environ.get('CODE', '')
    number_of_testcases = os.environ.get('NUMBER_OF_TESTCASES', '')
    time_limit = os.environ.get('TIME_LIMIT', '1')
    inputs = os.environ.get('INPUTS')

    # with open('/app/input.txt', 'r') as input_file:
    #     inputs = input_file.read()

    inputs = ast.literal_eval(inputs)
    time_limit = int(time_limit)
    number_of_testcases = int(number_of_testcases)

    results = test_submission_script(language, inputs, code, number_of_testcases, time_limit)

    for result in results:
        print(result)
