import base64

KEY = "Byygq1zI2KKyssKp8UvVe3DV/v6Aa0FEsKrE+pqDa0s"
ID = "0c3454d3-67ce-4558-b4ac-1e95f964cdf5"
ENCODED_KEY = base64.b64encode("{0}:{1}".format(KEY, KEY))
print_str = """{0}) {1} ({2})
{3}
-----------------------------------------"""
