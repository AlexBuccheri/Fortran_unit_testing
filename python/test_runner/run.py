import subprocess

def run_qcore(input_string: str, exe_type="debug") -> dict:
    """
    Run qcore, get the JSON output via stdout and
    return the results dictionary
    This is my code for qcore but needs adapting

    """
    qcore_exe = _QCORE_EXES[exe_type]
    named_result = get_named_result(input_string)
    qcore_command = [qcore_exe, '--format', 'json', '-s', input_string.replace('\n', ' ')]
    try:
        # Can't write any stderr to stdout as this will mess up the JSON format and hence can't parse
        qcore_json_result = subprocess.check_output(qcore_command, stderr=subprocess.DEVNULL) #, stderr=subprocess.STDOUT).decode("utf-8")
        return json.loads(qcore_json_result)
    except subprocess.CalledProcessError:  # as error:
        #print("subprocess error:", error.returncode, "found:", error.output)
        return {named_result: {}}