import click
import os
import requests
import json

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
            data = edge_config_update_req([{"key": "maintenance", "value": "0"}])
            res = requests.patch(url, json=data, headers=headers)
            if res.ok:
                click.secho("Site now in standard mode.", fg="green")
                print("Raw response:", res.json())
            else:
                print(res.json())
        case "maintenance":
            data = edge_config_update_req([{"key": "maintenance", "value": "1"}])
            res = requests.patch(url, json=data, headers=headers)
            if res.ok:
                click.secho("Site now in maintenance mode.", fg="yellow")
                print("Raw response:", res.json())
            else:
                print(res.json())
        # More modes can go here


if __name__ == "__main__":
    siteutils()
