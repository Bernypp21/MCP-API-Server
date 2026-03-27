Two MCP servers with different Purpose.

Created Using fastMCP

## URL MCP SERVER
* An MCP server with two custom tool using virusTotal API calls
  -  VirustTotal url scan: scans a given url and determines if it is safe or malicious
  -  VirusTotal url report: gets the report it made of the url given from first tool.

## Webcam MCP SERVER
* An MCP server with two custom tool using IP STACK and Windy
  - IP_stack: uses API calls to ip stack to get geolocation information from a given ip address
  - Windy: with the coordinates from ip stack, this tool will return a list of url to webcams near given coordinates.
 
HOW TO USE:
* Preq: You will need API key from these website
  - windy: https://api.windy.com/
  - ip stack: https://ipstack.com/
  - virusTotal: https://www.virustotal.com/gui/sign-in

 * after setting up keys:
   - uv init --bare
   - uv add -r requirements.txt
   - uv run app.py
