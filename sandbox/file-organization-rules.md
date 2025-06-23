# File Organization Rules

`./src/resma/cli.py` will always be the main entry point for the CLI to initialize.

every module for `resma` will have a `cli.py` file as it's entry point.

The project should tend to follow (as much as possible) clean architecture principles and [design patterns](https://refactoring.guru/design-patterns/catalog) so every dev could easily follow the code. It's about striking a balance between structure and flexibility.

every `cli.py` will have a `main` function that would be the entry point for the CLI to initialize.



