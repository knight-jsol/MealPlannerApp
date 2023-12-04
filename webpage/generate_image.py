# import requests
#
# api_key = "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"
# endpoint = "https://api.openai.com/v1/images/generations"
#
# headers = {
#    "Authorization": f"Bearer {api_key}",
#    "Content-Type": "application/json",
# }
#
# data = {
#    "prompt": "blueberries"
# }
#
# response = requests.post(endpoint, headers=headers, json=data)
#
# if response.status_code == 200:
#     result = response.json()
#     if isinstance(result, dict) and "data" in result:
#         image_data_list = result["data"]
#         for image_data in image_data_list:
#             if "url" in image_data:
#                 image_url = image_data["url"]
#                 print("Generated image URL:", image_url)
#             else:
#                 print("No image URL found for one of the images.")
#     else:
#         print("No images generated.")
# else:
#     print("Error:", response.status_code, response.text)
