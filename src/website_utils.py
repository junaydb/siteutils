import click
import os.path
import re
import shutil


def get_image_paths(dir):
    """Get all file paths in the given directory (excluding dot files)."""
    return [
        f
        for f in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, f)) and not f.startswith(".")
    ]


def write_md_img_links(dir, file):
    """
    Write all paths in the given directory as markdown image links.
    File names are used as alt text.
    """
    paths = get_image_paths(dir)
    for path in paths:
        # Replace hypens and underscores with
        alt_text = re.sub("-|_", " ", path)
        # Remove extension
        alt_text = re.sub(r"\.[^.]*$", "", alt_text)
        # Capitalise first letter
        alt_text = alt_text[0].upper() + alt_text[1:]

        file.write(f"![{alt_text}]({dir}{path})\n")


CONTEXT_SETTINGS = dict(max_content_width=120)


@click.group()
def website_utils():
    pass


@website_utils.group(context_settings=CONTEXT_SETTINGS)
def markdown():
    pass


@markdown.command()
@click.argument(
    "dir",
    nargs=-1,
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
    help="Output .md files (instead of the default .mdx)",
)
def create_with_images(dir, output, template, md):
    """Create .md|.mdx file with all images from one or more directories as markdown syntax.

    DIR is the path to a directory of images. You can pass multiple directories (separated by spaces).
    """
    ext = ".md" if md else ".mdx"
    click.echo(f"Using {ext}")

    with click.open_file(f"{output}{ext}", "w") as output_file:
        if template:
            # Copy template file contents into output file
            with click.open_file(template, "r") as template_file:
                shutil.copyfileobj(template_file, output_file)
                click.secho(f"Copied '{template}' content to '{output}'", fg="green")

        for d in dir:
            write_md_img_links(d, output_file)

    click.secho(f"Generated {ext} file '{output}{ext}'", fg="green")


@markdown.command()
@click.argument(
    "dir",
    nargs=-1,
    type=click.Path(exists=True, file_okay=False),
)
@click.argument(
    "target",
    type=click.Path(writable=True),
)
def append_images(dir, target):
    """Append all images from one or more directories to a file as markdown syntax.

    DIR is the path to a directory of images. You can pass multiple directories (separated by spaces).
    TARGET is the file to append to.
    """

    for d in dir:
        with click.open_file(target, "a") as file:
            write_md_img_links(d, file)

    click.secho(f"Appended images to '{target}'", fg="green")


if __name__ == "__main__":
    website_utils()
