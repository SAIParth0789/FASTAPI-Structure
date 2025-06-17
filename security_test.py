import json

def get_config():
    """
    This function contains different hardcoded credentials that
    should be detected by Amazon CodeGuru.
    """
    # Using different patterns for fake credentials
    config = {
        "api_key": "zaCELgL.0imfnc8mVLWwsAawjYr4Rx-Af50DDqtlx",
        "api_secret": "26422219-4a7b-45b7-a365-802526543210",
        "db_connection_string": "mongodb+srv://user_test:MyTestPassword123@cluster-test.mongodb.net/test?retryWrites=true"
    }

    print("Using hardcoded API key and secret for connection!!")
    return json.dumps(config)

if __name__ == "__main__":
    get_config()
