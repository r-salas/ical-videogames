#
#
#   Populate games
#
#

import typer

from app.tasks import update_game_releases


def main(data_dir: str):
    update_game_releases(data_dir)


if __name__ == "__main__":
    typer.run(main)
