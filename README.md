# Search Engine MCP Server

A collection of MCP (Model Context Protocol) servers providing search engine functionality, file management, stock data access, and creative writing prompts. These servers can be used with various MCP-compatible clients including AI applications, Claude Desktop, and custom FastAPI applications.

## MCP Servers Overview

This project includes four MCP servers, each providing different functionality:

### 1. Web Search Server (`server.py`)
**Type:** MCP Tool
- **Description:** Provides web search capabilities using Tavily API
- **Usage:** `web_search(query)` - Search the web for information
- **Features:** Real-time web search with structured results
- **Transport:** Streamable HTTP (runs on port 10000)
- **Requirements:** TAVILY_API_KEY environment variable

### 2. File Management Tool (`file_management_tool.py`)
**Type:** MCP Tool
- **Description:** Creates text files with specified content in designated directories
- **Usage:** `create_text_file(directory_path, file_name, content)`
- **Transport:** STDIO (for AI applications) / HTTP (for FastAPI)

### 3. Stock Data Resource (`stock_data_resource.py`)
**Type:** MCP Resource
- **Description:** Provides real-time stock market data using Yahoo Finance API
- **Usage:** Access via `stock://{ticker_symbol}` resource URI
- **Features:** Current price, daily high/low, company summary
- **Transport:** STDIO (for AI applications) / HTTP (for FastAPI)

### 4. Creative Writing Prompt (`creative_writing_prompt.py`)
**Type:** MCP Prompt
- **Description:** Generates creative story starters based on genre, character, and setting
- **Usage:** `generate_story_starter(genre, main_character_trait, setting)`
- **Features:** Supports multiple genres (Sci-Fi, Fantasy, Horror, Mystery)
- **Transport:** STDIO (for AI applications) / HTTP (for FastAPI)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SearchEngineMCP
   ```

2. **Install dependencies:**
   ```bash
   uv install
   ```

3. **Install additional requirements:**
   ```bash
   pip install yfinance tavily python-dotenv  # Required for stock data, web search, and environment variables
   ```

4. **Set up environment variables:**
   ```bash
   # Create .env file with required API keys
   echo "TAVILY_API_KEY=your_tavily_api_key_here" > .env
   ```

## Usage Options

### Option 1: Web Search Server (Tavily API)

Run the web search server individually:

```bash
uv run server.py
```

This starts the web search server on `http://localhost:10000` with MCP endpoint at `/mcp/`.

**MCP Configuration:**
```json
{
  "tavily": {
    "url": "http://localhost:10000/mcp/"
  }
}
```

### Option 2: Combined FastAPI HTTP Server (File, Stock, Prompt)

Run the file management, stock data, and creative writing servers through a single FastAPI application:

```bash
uv run fastAPI/server.py
```

This starts a FastAPI server on `http://localhost:10000` with the following endpoints:
- `/file` - File management operations
- `/stock` - Stock data access
- `/prompt` - Creative writing prompts

### Option 3: Individual HTTP Servers

Run each MCP server individually with HTTP transport:

```bash
# File management
uv run fastAPI/file_management_tool.py

# Stock data
uv run fastAPI/stock_data_resource.py

# Creative writing
uv run fastAPI/creative_writing_prompt.py
```

### Option 4: AI Application STDIO Servers (Recommended for Desktop AI Integration)

For use with AI applications that support STDIO transport:

```bash
# File management
uv run LocalAIuse/file_management_tool.py

# Stock data
uv run LocalAIuse/stock_data_resource.py

# Creative writing
uv run LocalAIuse/creative_writing_prompt.py
```

## AI Application Integration

For AI applications, configure the servers in your application configuration file:

```yaml
mcp_servers:
  - name: "tavily"
    cmd: "C:\\Users\\GIGO PETER\\.local\\bin\\uv.EXE"
    args: ["run", "D:\\D DRIVE\\Projects\\SearchEngineMCP\\server.py"]
    env: []

  - name: "file-ops"
    cmd: "C:\\Users\\GIGO PETER\\.local\\bin\\uv.EXE"
    args: ["run", "D:\\D DRIVE\\Projects\\SearchEngineMCP\\LocalAIuse\\file_management_tool.py"]
    env: []

  - name: "stock-data"
    cmd: "C:\\Users\\GIGO PETER\\.local\\bin\\uv.EXE"
    args: ["run", "D:\\D DRIVE\\Projects\\SearchEngineMCP\\LocalAIuse\\stock_data_resource.py"]
    env: []

  - name: "creative-prompts"
    cmd: "C:\\Users\\GIGO PETER\\.local\\bin\\uv.EXE"
    args: ["run", "D:\\D DRIVE\\Projects\\SearchEngineMCP\\LocalAIuse\\creative_writing_prompt.py"]
    env: []
```

**Important:** After updating MCP configuration files, you must restart the AI application for changes to take effect:
1. Close the AI application completely
2. Open Task Manager and end any remaining processes (search for the app name)
3. Restart the application

### Option 5: Testing MCP Servers

For development and testing:

```bash
uv run mcp dev server.py
```

**Server URLs for Testing:**
- **File Management Server:** `http://127.0.0.1/file/mcp`
- **Stock Data Server:** `http://127.0.0.1/stock/mcp`
- **Creative Writing Server:** `http://127.0.0.1/prompt/mcp`

## API Examples

### Web Search
```python
# Perform web search
results = await mcp_client.call_tool(
    "web_search",
    query="latest news on artificial intelligence"
)
# Returns: Structured search results from Tavily API
```

### File Management
```python
# Create a text file
result = await mcp_client.call_tool(
    "create_text_file",
    directory_path="/path/to/documents",
    file_name="notes.txt",
    content="This is my note content"
)
```

### Stock Data
```python
# Access stock information
stock_info = await mcp_client.read_resource("stock://AAPL")
# Returns: current price, daily high/low, company summary
```

### Creative Writing
```python
# Generate a story starter
story = await mcp_client.call_prompt(
    "generate_story_starter",
    genre="Sci-Fi",
    main_character_trait="A skeptical detective",
    setting="A city where it never stops raining"
)
```

## Development

### Project Structure
```
SearchEngineMCP/
├── server.py                   # Web search server (Tavily API)
├── fastAPI/
│   ├── server.py               # Combined FastAPI server
│   ├── file_management_tool.py
│   ├── stock_data_resource.py
│   └── creative_writing_prompt.py
├── LocalAIuse/                 # STDIO server implementations
│   ├── file_management_tool.py
│   ├── stock_data_resource.py
│   └── creative_writing_prompt.py
└── claude_desktop_config.json  # Claude Desktop configuration example
```

### Adding New MCP Servers

1. Create your MCP server in both `fastAPI/` and `LocalAIuse/` directories
2. Update the main `server.py` to include the new server
3. Update configuration files (Claude Desktop, LocalAI)
4. Update this README

### Transport Modes

- **STDIO:** Standard input/output transport for direct process communication
- **HTTP:** Web-based transport for network access
- **Streamable HTTP:** Stateless HTTP transport for serverless deployments

## Dependencies

- `mcp` - Model Context Protocol library
- `fastmcp` - FastMCP server implementation
- `yfinance` - Yahoo Finance API client (for stock data)
- `tavily` - Tavily API client (for web search)
- `python-dotenv` - Environment variable management
- `uvicorn` - ASGI server (for FastAPI)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Create an issue in the repository
- Check the MCP documentation for protocol details
- Review AI application documentation for integration guides
- Explore [MCP Clients](https://modelcontextprotocol.io/clients) for compatible applications
- Browse [MCP Examples](https://modelcontextprotocol.io/examples) for implementation references
