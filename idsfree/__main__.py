def main():
    import os
    import sys

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import idsfree

    __package__ = str("idsfree")

    # Run the cmd
    from idsfree.actions.cli import cli

    cli()

if __name__ == "__main__":  # pragma no cover
    main()
