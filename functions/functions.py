import requests

async def scan_all_backlinks(url, target_url):
    response = requests.get(url)
    if response.status_code == 200:
        if target_url in response.text:
            return True
            # get da and pa (WIP)
        else:
            return False
    else:
        return await False



