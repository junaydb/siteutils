import click
import os.path
import re
import shutil


def write_md_img_links(dir, img_paths, file):
    for img_path in img_paths:
        # Skip dot files
        if img_path[0] == ".":
            continue
        # Replace hypens and underscores with
        img_name = re.sub("-|_", " ", img_path)
        # Remove extension
        img_name = re.sub(r"\.[^.]*$", "", img_name)
        # Capitalise first letter
        img_name = img_name[0].upper() + img_name[1:]

        file.write(f"![{img_name}]({dir}{img_path})\n")


CONTEXT_SETTINGS = dict(max_content_width=120)


@click.group()
def website_utils():
    pass


@website_utils.group(context_settings=CONTEXT_SETTINGS)
def markdown():
    pass


@markdown.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False),
)
@click.option(
    "-o",
    "--output",
    help="Specify the generated output file name.",
    default="generated",
    show_default=True,
    type=click.Path(writable=True),
)
@click.option(
    "-t",
    "--template",
    help="'Copy and paste the content of this file before the images.",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--md",
    default=False,
    is_flag=True,
    help="Output .md files",
)
def create_with_images(path, output, template, md):
    """Create .md|.mdx file with all images from a directory as markdown links.

    PATH is the path to the directory of images.
    """
    img_paths = os.listdir(path)
    ext = ".md" if md else ".mdx"
    click.echo(f"Using {ext}")

    with click.open_file(f"{output}{ext}", "w") as output_file:
        if template:
            # Copy template file contents into output file
            with click.open_file(template, "r") as template_file:
                shutil.copyfileobj(template_file, output_file)
                click.secho(f"Copied '{template}' content to '{output}'", fg="green")

        write_md_img_links(path, img_paths, output_file)

    click.secho(f"Generated {ext} file '{output}{ext}'", fg="green")


@markdown.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False),
)
@click.argument(
    "target",
    type=click.Path(writable=True),
)
def append_images(path, target):
    """Append all images from a directory to a file in markdown syntax.

    PATH is the path to the directory of images.
    TARGET is the file to append to.
    """
    img_paths = os.listdir(path)

    with click.open_file(target, "a") as file:
        write_md_img_links(path, img_paths, file)

    click.secho(f"Appended images to '{target}'", fg="green")


if __name__ == "__main__":
    website_utils()
