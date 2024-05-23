def format_template(template: str, *args, **kwargs):
    """
        Formats the template string with variables passed as arguments.

        Args:
            template (str): The template string to format.
            *args: Positional arguments to format the template.
            **kwargs: Keyword arguments to format the template.

        Returns:
            str: The formatted template string.
    """

    return template.format(*args, **kwargs)
