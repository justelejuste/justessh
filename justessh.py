import os
import inquirer
import configparser

CONFIG_FILE = os.path.expanduser("~/.ssh/justessh_config")

def launch_ssh(answers):
    user = answers["user"]
    hostname = answers["hostname"]
    os.system(f"ssh {user}@{hostname}")


def main():
    config = configparser.ConfigParser()

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as config_file:
            config_file.write("# Configuration file for my SSH script\n")

    config.read(CONFIG_FILE)
    hosts = config.sections()

    questions = [
        inquirer.List("action",
                      message="Choose an action",
                      choices=["New host", "Existing host"],
                      ),
    ]

    action = inquirer.prompt(questions)["action"]

    if action == "Nouvel hôte":
        new_host_questions = [
            inquirer.Text("hostname", message="Enter hostname"),
            inquirer.Text("user", message="Enter username"),
            inquirer.Text("alias", message="Enter alias")
        ]

        answers = inquirer.prompt(new_host_questions)
        alias = answers["alias"]
        host_name = answers["hostname"]
        config[alias] = {"User": answers["user"], "HostName": host_name}
        with open(CONFIG_FILE, 'a') as config_file:
            config.write(config_file)

        launch_ssh(answers)

    elif action == "Hôte existant" and hosts:
        existing_host_questions = [
            inquirer.List("hostname",
                          message="Select an existing host",
                          choices=hosts
                          ),
        ]

        answers = inquirer.prompt(existing_host_questions)
        launch_ssh({
            "user": config.get(answers["hostname"], "User"),
            "hostname": config.get(answers["hostname"], "HostName"),
        })

    else:
        print("No existing host. Please add a new host first")

if __name__ == "__main__":
    main()

