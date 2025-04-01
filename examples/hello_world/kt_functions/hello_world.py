from kube_transform import fsutil as fs


def prepend_hello_world_directory(input_directory, output_directory):
    filenames = fs.listdir(input_directory)
    function_name = "hello_world.prepend_hello_world_file"
    spec = [
        {
            "type": "static",
            "tasks": [
                {
                    "function": function_name,
                    "args": {
                        "input_file": fs.join(input_directory, filename),
                        "output_file": fs.join(output_directory, filename),
                    },
                }
                for filename in filenames
            ],
            "memory": "1Gi",
            "cpu": "1",
        }
    ]
    return spec


def prepend_hello_world_file(input_file, output_file):
    print("Executing hello_world...")
    contents = fs.read(input_file)
    contents = prepend_hello_world(contents)
    fs.write(output_file, contents)
    print("hello_world execution complete.")


def prepend_hello_world(s):
    return "\n".join([f"Hello World: {line}" for line in s.split("\n")])
