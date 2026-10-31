from mcp.server import MCPServer
from movies import find

mcp = MCPServer("movies-mcp")
registrar = mcp.tool()

registrar(find)

if __name__ == "__main__":
	mcp.run()
