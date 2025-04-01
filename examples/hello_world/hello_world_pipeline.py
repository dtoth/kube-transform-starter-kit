def hello_world_pipeline(input_directory, output_directory):
    return {
        "name": "hello-world",
        "jobs": [
            {
                "name": "prepend-hello-world",
                "function": "hello_world.prepend_hello_world_directory",
                "args": {
                    "input_directory": input_directory,
                    "output_directory": output_directory,
                },
                "type": "dynamic",
                "dependencies": [],
            },
        ],
    }
