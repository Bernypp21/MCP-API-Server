#mcp server that has tools to ensure a website is used
from fastmcp import FastMCP
import requests
import os
import sys

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

mcp = FastMCP("URL Intelligence")


@mcp.tool("virustotal_url_scan")
def virustotal_url_scan(url):
    """
    Scans user url with virustotat url scanner api call, if success you will get an anaylsis ID to use for virustotal_url_report tool

    """
    api_url = "https://www.virustotal.com/api/v3/urls"
    
    headers = {
            "x-apikey":VIRUSTOTAL_API_KEY
    }

    response = requests.post(api_url,headers=headers,data={"url":url})
    
    #extracting the anaysis id that will be needed for report tool
    if response.status_code == 200:
        result = response.json()
        analysis_id = result.get("data").get("id")
        return analysis_id
    else:
        return "error couldnt scan url"

@mcp.tool("virustotal_url_report")
def virustotal_url_report(analysis_id):
     """
        Retrieve anaylsis report from url that was scan using virustotal_url_scan  analysis_id
        You will recieve a response text for successful case, print out the text  and a summary about it
     """

     api_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
     request_headers = {"x-apikey": VIRUSTOTAL_API_KEY,"accept": "application/json"}

     #retrieve results
     response = requests.get(api_url,headers=request_headers)

     #verify that api call went through
     if response.status_code == 200:
         return response.text

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0",port="8080")



