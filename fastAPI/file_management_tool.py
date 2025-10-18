from mcp.server.fastmcp import FastMCP
from typing import Annotated
import os


mcp = FastMCP(name="FileOps", stateless_http=True)


@mcp.tool(description="Create a text file with the given content. If the directory doesn't exist, it is created.")
def create_text_file(
    directory_path: Annotated[str, "Absolute or relative directory path where the file should be created"],
    file_name: Annotated[str, "File name to create, e.g., 'notes.txt'"],
    content: Annotated[str, "Content to write into the file"],
) -> str:
    """
    Create a text file with provided content on the local filesystem.

    Arguments:
        directory_path: Directory where the file will be created. Created if it doesn't exist.
        file_name: Name of the file to create (e.g., 'example.txt').
        content: The text content to write into the new file.

    Returns:
        A confirmation message including the full path to the created file.
    """
    if not directory_path:
        raise ValueError("directory_path must be provided")
    if not file_name:
        raise ValueError("file_name must be provided")

    os.makedirs(directory_path, exist_ok=True)
    full_path = os.path.join(directory_path, file_name)

    # Write content to the specified file path
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content or "")

    return f"Successfully created file at '{os.path.abspath(full_path)}'"


if __name__ == "__main__":
    # Expose over stateless HTTP for easy testing
    mcp.run(transport="streamable-http")


