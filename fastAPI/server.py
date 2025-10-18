import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from file_management_tool import mcp as file_mcp
from stock_data_resource import mcp as stock_mcp
from creative_writing_prompt import mcp as prompt_mcp
import os


# Create a combined lifespan to manage session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(file_mcp.session_manager.run())
        await stack.enter_async_context(stock_mcp.session_manager.run())
        await stack.enter_async_context(prompt_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/file", file_mcp.streamable_http_app())
app.mount("/stock", stock_mcp.streamable_http_app())
app.mount("/prompt", prompt_mcp.streamable_http_app())

PORT = os.environ.get("PORT", 10000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)