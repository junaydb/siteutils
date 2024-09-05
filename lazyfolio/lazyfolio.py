import click
from click_option_group import optgroup, MutuallyExclusiveOptionGroup
import os.path
import re


@click.group()
def lazyfolio():
    pass


@lazyfolio.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False),
)
@optgroup.group("File settings", cls=MutuallyExclusiveOptionGroup)
@optgroup.option(
    "-o",
    "--output",
    help="Specify the generated output file.",
    default="generated.mdx",
    type=click.Path(writable=True),
)
@optgroup.option(
    "-a",
    "--append",
    help="Specify the file to append to.",
    type=click.Path(writable=True),
)
def mdx_with_images(path, output, append):
    """Generate MDX file containing all images in PATH.

    PATH is the path to the directory of images.
    """
    img_paths = os.listdir(path)
    mdx_template = """---
title: placeholder
rows:
  - type: text
    title: placeholder
    items:
      - placeholder
---

import ImageModal from "@components/ImageModal.astro";
export const components = { img: ImageModal };

"""

    target_file = append if append else output
    mode = "a" if append else "w"

    with click.open_file(target_file, mode) as file:
        if not append:
            file.write(mdx_template)
        for img_path in img_paths:
            _, img_name = os.path.split(img_path)
            # Skip dot files
            if img_name[0] == ".":
                continue
            # Replace hypens and underscores with spaces and remove extension
            img_name = re.sub("-|_", " ", img_name)
            img_name = re.sub(r"\.[^.]*$", "", img_name)
            # Capitalise first letter
            img_name = img_name[0].upper() + img_name[1:]
            file.write(f"![{img_name}]({path}{img_path})\n")

    if append:
        click.secho(f"appended to {append}", fg="green")
    else:
        click.secho(f"generated MDX file: {output}", fg="green")


if __name__ == "__main__":
    lazyfolio()
