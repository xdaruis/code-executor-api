import subprocess
import os
import tempfile
import secrets
import shutil
import stat

RETURN_CODE_TIMEOUT = 124
MAX_TIME_LIMIT = 15

def test_submission_script(inputs, code, number_of_testcases, time_limit):
    if time_limit > MAX_TIME_LIMIT:
        time_limit = MAX_TIME_LIMIT
    folder_path = create_temporary_directory()
    random_name = secrets.token_hex(16)
    file_path = f"{folder_path}/{random_name}.cpp"
    write_to_file(file_path, code)
    try:
        compile_program = f"g++ {file_path} -o {folder_path}/{random_name}.exe"
        subprocess.run(compile_program, shell=True, check=True)
        results = run_tests(number_of_testcases, file_path, inputs, time_limit, folder_path, random_name)
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

def run_tests(number_of_testcases, file_path, inputs, time_limit, folder_path, random_name):
    results = []
    for act_test in range(number_of_testcases):
        write_to_file(file_path, inputs[act_test])
        try:
            execute_program = f"timeout {time_limit} {folder_path}/{random_name}.exe < {file_path} > {folder_path}/{random_name}.out"
            subprocess.run(execute_program, shell=True, check=True)
            with open(f"{folder_path}/{random_name}.out", 'r') as output_file:
                program_output = output_file.read().strip()
                results.append(program_output)
        except subprocess.CalledProcessError as e:
            if e.returncode == RETURN_CODE_TIMEOUT:
                results.append(f"{act_test + 1}.Time Limit Exceeded")
            else:
                results.append("Internal Server Error!")
    return results

def write_to_file(path, text):
    with open(path, 'wb') as file:
        file.write(text.encode('utf-8'))