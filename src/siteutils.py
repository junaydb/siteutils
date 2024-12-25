import click
import os
import requests
import json
import subprocess

try:
    VERCEL_ACCESS_TOKEN = os.environ["VERCEL_ACCESS_TOKEN"]
except:
    click.secho("$VERCEL_ACCESS_TOKEN not found.", fg="red")
    exit(1)

try:
    VERCEL_EDGE_CONFIG_ID = os.environ["VERCEL_EDGE_CONFIG_ID"]
except:
    click.secho("$VERCEL_EDGE_CONFIG_ID not found.", fg="red")
    exit(1)

try:
    SITE_GIT_URL = os.environ["SITE_GIT_URL"]
except:
    click.secho("$SITE_GIT_URL not found.", fg="red")
    exit(1)


try:
    POSTS_DIR = os.environ["POSTS_DIR"]
except:
    click.secho("$POSTS_DIR not found.", fg="red")
    exit(1)


def edge_config_update_req(props):
    data = {"items": []}
    for prop in props:
        item = {"operation": "update", "key": prop["key"], "value": prop["value"]}
        data["items"].append(item)
    return data


@click.group()
def siteutils():
    pass


@siteutils.command()
@click.argument(
    "mode",
    type=click.Choice(["standard", "maintenance"], case_sensitive=False),
)
def mode(mode):
    """Set the website's mode."""

    url = f"https://api.vercel.com/v1/edge-config/{VERCEL_EDGE_CONFIG_ID}/items?teamId=junaydb"
    headers = {"Authorization": f"Bearer {VERCEL_ACCESS_TOKEN}"}

    match mode:
        case "standard":
            data = edge_config_update_req([{"key": "maintenance", "value": False}])
            res = requests.patch(url, json=data, headers=headers)
            if res.ok:
                click.secho("Site now in standard mode.", fg="green")
                print("Raw response:", res.json())
            else:
                print(res.json())
        case "maintenance":
            data = edge_config_update_req([{"key": "maintenance", "value": True}])
            res = requests.patch(url, json=data, headers=headers)
            if res.ok:
                click.secho("Site now in maintenance mode.", fg="yellow")
                print("Raw response:", res.json())
            else:
                print(res.json())
        # More modes can go here


@siteutils.command()
@click.argument(
    "target",
    type=click.Choice(["main", "preview"], case_sensitive=False),
)
def deploy(target):
    match target:
        case "main":
            subprocess.run(
                f"""cd {POSTS_DIR}\\
                    && git add .\\
                    && git commit -m '(automated): update posts'\\
                    && git push\\
                    && git clone {SITE_GIT_URL}\\
                    && cd website\\
                    && git checkout staging\\
                    && git submodule update --init --recursive --remote\\
                    && git add .\\
                    && git commit -m '(automated): update posts'\\
                    && git checkout main\\
                    && git merge staging\\
                    && git push""",
                shell=True,
            )
            subprocess.run("sudo rm -r website", shell=True)
        case "preview":
            subprocess.run(
                f"""cd {POSTS_DIR}\\
                    && git add .\\
                    && git commit -m '(automated): update posts'\\
                    && git push\\
                    && git clone --depth=1 --branch staging  {SITE_GIT_URL}\\
                    && cd website\\
                    && git submodule update --init --recursive --remote\\
                    && git add .\\
                    && git commit -m '(automated): update posts'\\
                    && git push""",
                shell=True,
            )
            subprocess.run("sudo rm -r website", shell=True)


if __name__ == "__main__":
    siteutils()
