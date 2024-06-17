#!/usr/bin/python3
import re

def get_link(data):
    return data[3]

# def post_link(all_links):
#     pattern = r'(\d+) likes?, (\d+) reposts?, (\d+) views'
#     for item in all_links:
#         if item and isinstance(item, str):
#             match = re.search(pattern, item)
#             if match:
#                 likes, reposts, views = match.groups()
#                 res = f"Likes: {likes}, Reposts: {reposts}, Views: {views}"
#                 data += res
