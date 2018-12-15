#!/usr/bin/python
#
import psutil

process_name = "process_name"
process_path = "C:\\Foxmail 7.2\\Foxmail.exe"


def get_all_process():
    return [psutil.Process(pid) for pid in psutil.pids()]


def find_process(process_name):
    for process in get_all_process():
        if process.name() == process_name:
            return process
    return None


def main():
    process = find_process(process_name)
    if process:
        process.kill()
    psutil.Popen(process_path)


if __name__ == "__main__":
    main()
