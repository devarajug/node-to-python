# import urllib3
# import os
# username = 'sample'
# password = "sample"
# headers = urllib3.make_headers(basic_auth=username+':'+password)
#
# print(headers)
#
# customHeaders = {
#     'Authorization': {
#         'username':os.environ.get('jenkinsUsername', 'sample'),
#         'password':os.environ.get('jenkinsPassword', 'sample')
#     },
#     "Content-Type": "application/xml",
#     'Accept': "application/xml"
# }
#
# print("before update", customHeaders)
# if customHeaders.get('Authorization', None):
#     usename = customHeaders.get('Authorization').get('usename')
#     password = customHeaders.get('Authorization').get('password')
#     authentication_header = urllib3.make_headers(basic_auth=username+':'+password)
#     del customHeaders['Authorization']
#     customHeaders.update(authentication_header)
#
# print("after update", customHeaders)


#urllib3.response.HTTPResponse
