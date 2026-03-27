#the purpose of this server is to utilze and ip geolaction server and then used the coordinates from it to access webcams near it
import json
import requests
import os
import sys
from fastmcp import FastMCP

IPSTACK_API_KEY = os.getenv("IPSTACK_API_KEY")
WINDY_API_KEY = os.getenv("WINDY_API_KEY")

mcp = FastMCP("webcam")

@mcp.tool("IP_geolocation")
def ip_location(ip_address):
    """
        Use this tool to get the physical coordinates of a public IP address
    """

    url = f"http://api.ipstack.com/{ip_address}?access_key={IPSTACK_API_KEY}"

    #getting data from ipstack url
    response = requests.get(url,timeout=10)
    response.raise_for_status()
    data = response.json()

    lat = data.get("latitude")
    lon = data.get("longitude")
    city = data.get("city","Unknown City")
    
    #location need for next tool not found
    if lat is None or lon is None:
        return f"could not get location need for {ip_address}"
    
    #result that llm will use to get data need
    result = {
            "ip" : ip_address,
            "city" : city,
            "latitude" : lat,
            "longitude" : lon
    }

    return json.dumps(result,indent=2)

            
        
        

@mcp.tool("get_webcam_list")
def get_webcam_list(latitude:float,longitude:float):
    '''
        Get a list of viewable webcams near a specific latitude and longitude.
        
        Args:
        str containing information about ip
    '''

    url = "https://api.windy.com/webcams/api/v3/webcams"
    radius_km = 50
    limit = 5
    params = {
        "nearby": f"{latitude},{longitude},{radius_km}", 
        "limit": limit,
        "include": "location,images,player"
    }
    headers = {
        "x-windy-api-key": WINDY_API_KEY
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    webcams = data.get("webcams", [])
    
    if not webcams:
        return f"No webcams found within {radius_km}km of coordinates ({latitude}, {longitude})."
        
    result = [f"Found {len(webcams)} webcams near ({latitude}, {longitude}):\n"]
    
    for cam in webcams:
        title = cam.get("title", "Unknown Location")
        distance = cam.get("location", {}).get("distance", "Unknown")

        webcam_id = cam.get("webcamId")
        if webcam_id:
            url = f"https://www.windy.com/webcams/{webcam_id}"
        else:
            url = "No link available"
        
        result.append(f"- **{title}** ({distance} km away)")
        result.append(f"  Webcam URL: {url}\n")
        
    return "\n".join(result)
        


if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http",host="0.0.0.0",port=8080)

