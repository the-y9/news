from urllib.parse import urlparse, parse_qs

url = """

https://www.youtube.com/watch?v=BPcBX5bWBxM&list=PLDnIeUIsbmQsN2Nt59WGRGyirDO3zWccZ

"""
print(url.strip() == "https://www.youtube.com/watch?v=BPcBX5bWBxM&list=PLDnIeUIsbmQsN2Nt59WGRGyirDO3zWccZ")
# parsed_url = urlparse(url)
# query_params = parse_qs(parsed_url.query)

# video_id = query_params.get("v", [None])[0]

# print(video_id)
