import logging
import argparse

from typing import Tuple
from utils import configure_logging, constants
from flow_tools import PropertiesManager
from script_runner import PythonVersion, PythonScriptRunner


def main():
    # Configure the logger
    configure_logging()

    # Create command line argument parser and add program supported arguments
    parser = argparse.ArgumentParser()

    # Add development mode positional argument
    parser.add_argument("--dev",
                        action="store_true",
                        help="enable development mode",
                        dest="dev_enabled")

    # Parse the arguments
    args = parser.parse_args()

    # Update root logger logging level if development mode is enabled
    if args.dev_enabled:
        logging.getLogger().setLevel(logging.DEBUG)

    # Read flow task input properties
    input_props = None

    if args.dev_enabled:
        input_props = PropertiesManager.shared.get_properties_from_file(
            constants.DEV_INPUT_FILE_PATH)
    else:
        input_props = PropertiesManager.shared.task_input_properties

    # Convert python version from string to python version enum
    python_version = (PythonVersion.PYTHON_3_9 if "python 2"
                      in input_props.get(constants.INPUT_VERSION_KEY,
                                         "") else PythonVersion.PYTHON_2_7)

    # Check required task input properties
    if not input_props.get(constants.INPUT_SCRIPT_KEY):
        raise ValueError("Python script not provided or empty!")

    # Run the script
    result, output = run_script(
        python_version=python_version,
        additional_packages=input_props.get(constants.INPUT_PACKAGES_KEY, ""),
        script=input_props.get(constants.INPUT_SCRIPT_KEY, ""),
        cmd_args=input_props.get(constants.INPUT_ARGUMENTS_KEY, ""))

    # Program execution successful
    exit(result)


def run_script(python_version: PythonVersion, additional_packages: str,
               script: str, cmd_args: str) -> Tuple[int, str]:
    logger = logging.getLogger(__name__)

    logger.info("Input properties:")
    logger.info(f"🔢Python Version: {python_version}")
    logger.info(f"📦Python Packages:\n{additional_packages}")
    logger.info(f"📣Python Arguments: {cmd_args}")
    logger.info(f"🚀Python Script:\n{script}")

    # Create a new python script runner and execute the script
    python_script_runner = PythonScriptRunner(python_version=python_version,
                                              script=script,
                                              cmd_args=cmd_args)

    logger.debug("Start python script runner activity...")

    python_script_runner.run()

    logger.info(f"🗳Python script runner result: {python_script_runner.result}")
    logger.info(
        f"📝Python script runner output:\n{python_script_runner.output}")

    # print(os.system("echo $PATH"))

    # print(PropertiesManager())
    # print(PropertiesManager.shared_instance)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(f"fere")

    # py_script_str = ("print(\"Hello World2\")\n"
    #                  "x = 3\n"
    #                  "y = 7\n"
    #                  "result = (x + y) ** 2\n"
    #                  "print(result)\n")

    # fifo_path = "fifo_file"

    # print(os.path.exists(fifo_path))

    # # if stat.S_ISFIFO(os.stat(fifo_path).st_mode):
    # if not os.path.exists(fifo_path):
    #     os.mkfifo(fifo_path)

    # with open(fifo_path, "w", encoding="utf-8") as fifo:
    #     fifo.write(py_script_str)

    return (0, None)


if __name__ == "__main__":
    main()
