import requests
import json


def take_rep(users):
    url = "https://api.github.com/users/" + users + "/repos"
    rep = requests.get(url).json()
    return rep


def write_file(path, rep):
    with open(path, "w") as f:
        json.dump(rep, f, indent=2)


def read_rep_user(path):
    with open(path, "r") as f:
        json_rep = json.load(f)
    return json_rep


if __name__ == "__main__":
    user = "denisded"
    write_file("rep_denisded.json", take_rep(user))
    print("Список репозиториев пользователя " + user + " на GitHUB:")
    for i in read_rep_user("rep_denisded.json"):
        print(i["name"])
