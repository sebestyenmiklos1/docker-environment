import os

try:
    import pwd
except ImportError:
    pwd = None


def preprocess(line):
    variables = {"USER_NAME": None, "USER_ID": None, "JENKINS_USER_ID": None}
    if pwd:
        variables["USER_NAME"] = pwd.getpwuid(os.getuid()).pw_name
        variables["USER_ID"] = str(os.getuid())
        try:
            variables["JENKINS_USER_ID"] = str(pwd.getpwnam("jenkins").pw_uid)
        except KeyError:
            pass
    else:
        # Fallback for Windows
        variables["USER_NAME"] = os.environ.get("USERNAME", "unknown")
        variables["USER_ID"] = str(os.getuid()) if hasattr(os, "getuid") else "0"
        variables[
            "JENKINS_USER_ID"
        ] = None  # Jenkins user likely doesn't exist on Windows

    if len(line) > 0 and line[0] == "?":
        # ?variable - only do the line if variable is defined
        parts = line.split(" ")
        check_variable = parts[0][1:]
        if variables[check_variable] is None:
            line = ""
        else:
            line = line[len(check_variable) + 2 :]

    for k, v in variables.items():
        if v:
            line = line.replace("$%s" % k, v)

    return line


def make_dockerfile(target):
    dockerfile_in_path = os.path.join(target, "Dockerfile.in")
    dockerfile_out_path = os.path.join(target, "Dockerfile")
    try:
        with open(dockerfile_in_path, "r") as in_file, open(
            dockerfile_out_path, "w"
        ) as out_file:
            for in_line in in_file.readlines():
                if in_line.startswith("include"):
                    include_path = in_line.split()[1]
                    try:
                        with open(include_path, "r") as include_file:
                            for include_line in include_file.readlines():
                                print(preprocess(include_line.strip()), file=out_file)
                    except FileNotFoundError as e:
                        print(f"Warning: Include file not found: {include_path} ({e})")
                        continue
                else:
                    print(preprocess(in_line.strip()), file=out_file)
        print(f"Successfully generated Dockerfile for target '{target}'.")
    except FileNotFoundError as e:
        print(f"Warning: Dockerfile.in not found for target '{target}': {e}")
