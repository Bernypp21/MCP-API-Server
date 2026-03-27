'''
Berny Perez
Final
Gensec

Goal: have a mcp serve that can get geo information about and ip address and then return a list of web cameras based on the coordinates

also have a url and file scanner

'''

import asyncio
from fast_agent.core.fastagent import FastAgent
import questionary

fast = FastAgent("Threat Intelligence")

#allowing user to choose what tools they need
tools = []
for tool in fast.config["mcp"]["servers"]:
    tools.append(tool)

tool = questionary.checkbox(
        "Select the tools to use for the agent:",
        choices=tools,
).ask()


#making fast agent
@fast.agent(
        instruction = f" You are malware and website intelligence agent. Use the tools you have access to answer users quesiton",
        model="gemini2",
        servers=tools,
        use_history=True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())






