from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
access_key = 'mMQxjyif6Uk8nSGIn9ZD3I19MBMEK3IUGngcX8_p'
secret_key = 'J5gFhdpQ-1O1rkCnlqYnzPiH3XTst2Szlv9GlmQM'
q = qiniu.Auth(access_key, secret_key)
bucket_name = 'cxsj'
key = 'DIYdataV1.zip'
token = q.upload_token(bucket_name, key, 3600)
localfile = 'DIYdataV1.zip'
ret, info = put_file(token, key, localfile)

print(info)
print("ok")