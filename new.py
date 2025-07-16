from huggingface_hub import HfApi

api = HfApi(token="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")

# Fetch your own user info
user_info = api.whoami()
print(user_info)