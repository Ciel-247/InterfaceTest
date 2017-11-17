# -*- coding:utf-8 -*-
import requests,redis,json,rsa,binascii,selenium

# 请求部分
s = requests
# a = s.get("http://192.168.149.135:8082/login-web/base/getRsaPublicKey.do") # 获取公钥
# publicKey =  rsa.PublicKey.load_pkcs1("-----BEGIN RSA PUBLIC KEY-----\n"+a.json()["data"]["pk"] + "\n-----END RSA PUBLIC KEY-----")
publicKey_str = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDbyk6iFh3Ovd+E3KM0bqDPVN/apRaa4Xki0a0lcGSdI0PjoAvlCBwcD04XY3Cv6E1rkva/qxk6RB/wSf/i+U/UR6XRUXySvqr8KdIaLCNOAyqik8E9Lv6M7zkahourIFo0OYLZ9dpZCHd5B3m2KcbhKj/+q7ntvMKRTvH4QGTxwIDAQAB
-----END PUBLIC KEY-----
'''
publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicKey_str)
print (publicKey)
userName = '330100194704074447'
passWord = 'aa12345678'
rsa_userName = binascii.b2a_hex(rsa.encrypt(userName,publicKey))
rsa_passWord = binascii.b2a_hex(rsa.encrypt(passWord,publicKey))
print ('rsa_username : ' + rsa_userName)
print ("rsa_password" + rsa_passWord)
r = s.get('http://192.168.149.135:8082/login-web/captcha.jpg?0.35607815636114215') # 通过调用这个接口，来得到DZSWJ_TGC和JSESSIONID
# 从cookies去获取DZSWJ_TGC和JSESSIONID
DZSWJ_TGC = r.cookies['DZSWJ_TGC']
JSESSIONID = r.cookies['JSESSIONID']
# 用dict格式存入cookies，供后面post使用
cookies = {"DZSWJ_TGC":DZSWJ_TGC,"JSESSIONID":JSESSIONID}
print ('DZSWJ_TGC : ' + DZSWJ_TGC)

# 连接redis，来拿到服务器的验证码（后面可以做成可配置的）
re = redis.Redis(host='192.168.149.93',port=6379,db=0,password='servyou')
# redis的key值是前面获得的DZSWJ_TGC + '@sessionCache'
redis_key = DZSWJ_TGC + '@sessionCache'
sessionCache = re.get(redis_key)
# 把str转为dict
sessionCache_dict = (json.loads(sessionCache))
# 单独取出验证码，因为本身得到的验证码是前后有双引号的，所以切割了[1:5]
kaptcha = sessionCache_dict["attributes"]["KAPTCHA_SESSION_KEY"].decode("unicode_escape").encode("utf8")[1:5]

# ————————————————————————下面是尝试使用post方式登录，但是用户名加解密失败，暂时放弃———————————————————————————————

# login_data = {"userName":rsa_userName,"passWord":rsa_passWord,"authencationHandler":"UsernamePasswordAuthencationHandler","lt":"LT-3692-XXiPdxofkAXFhETyMvbT-hzdzswj","_eventId":"submit","execution":"916aacf4-751b-434f-a31a-a068561cad41_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuVDNGUGJXeFRZMVZIUXpoVE5FZzFTWFJIYVZWS2JFUjJiVlE1ZDNkWlpVMUZPSGxHVnl0RFlXWkpRVXgxYVRSUFNFTkJaQ3N5VERoWmNGSTJVSEZ4Tm5aUksxRk1VV1pJWlRsTWNYWnVUV2RtTHpRNFJXSXlibkZ6UzNGQ1ozSnVUV2Q2VVZOWWRuUXZVMWwzVkVsUmVuRk9lVkZ0TVVNemNVcGtNM1YyYlVJMldHZFdNek5JVG5reFdscFhibEJ2YjNoeWVFdFRRbUpyVjNoMmRrZFZSMVZwT1U4d2JYWmthWFJEVWt4NFQxcGpaVEZ1TTJaVFowUkdXVkpWVkhSUE5WWmplazlHY1RoblpWbE9XV2hZYVZsb1VXUTVRM292UkVVNGFVaFBjMGR6VEUxcU5VdzRRWGhzUWt0TlVIbHVUSHBNUTFoeFZGUTNlVzU0WmpCcGVHbFpSVUprTVhOTVJIVkRhVEUxU1dSdlUyODNZWEpVTVRoc2JpOHpjREZtT0ZGTlVIUkNhMlEwSzNWaWJGWlVSMWt4ZEVaeWFGWlpTMVYxZEhkSk9GUXpWREkxYVdGU2MwcE5UVm9yVUZCd1UwaElZVTl2VGpkdGRqQmtMekV4WlU5ak1FcHhaRTlYWm1GNlJsSjFaMlZOTjFSdmMzVkJOalowV0V0a1dWWmphbUpUV25WT1IyRk1hbEJZYmtJeWJEUXdjM1pEZUhCdlptaGlaVEZNT1RKeE5HeGFXbXhuTTBsdllYcFdUVzV6UjNad2JqQkxkR0ZQZVhwa1lVOXhhMVp3VGprelZsTkdWVTFqWjFaa1NIUkZlbXhMWTBKNU0zVnhjVFF5YjJoek1rUlRNV2swTVZoSVpIVmFXVGR1Ympjd2Mwa3hkalZJUmtaV1NGTnpOME5vY2pGTGJXdElLMWxsVWtGaVVHSlJUMHBMUlZGTVYzUkpUSFZ2ZFdkRWRtbE5TRmh6WjBOM1FuQjZNRkpDZUZCUVNYazFhRnBOY25WWWIzVXpjMUppTUM5dE9DOXdXR1pzYkROUVUxRjJSa2czUXpabFlrdEtaR0ZDWTNwYU9UZzFVV3R6WkhsbFkzRk9kR3h5U2t4VlZFVmFhRVpSU0VKU1MySkhjM3BvYmxaS1dVeDNPR1p1ZG1oMFoyVkJPRXc1WVd0elYzYzFhWGxOTm1aRlEwaEJibkJNUlZwTFYyaHhkblpJTVRRNGN6RldiMVZrVW5KTGMxVkVSM2RESzNOeGIyZDJORzAzVDB3NVIwZEdSSFpXU1dwQ1JESkNVVmswYnpSbVEwSkdlWGREVVVjMVR6UjRZWGszUm1kQlZEUk5XVzA0ZUVGeWVtUk9aMjQ1TkV0cmNXMUZWVzFyU0c5dmFHUndSMlphUlVVdmJWZHFlbUpDUjFoak5HUjZZbWgwU0hSWk9FdzVWVXg1VG1oMVRFVXpVMWxtWlVOVU1GbG1kREp5TmpsWFlWVTNNMHRSWm5wSVQzTXhhRGM0Y2l0T1ZVVldiRE01YUZWeVNFWldXVlF6WkhoaGNFMUdhVlZDWm1aYWJXeDJTbkZ0VlZKbGNVSXlkRUpDVFhjM1ozWmpVblpXVWtRNGFXUklNM0YxU1RoTFJFbHViMGgzZWpWWlpVeDZNa0p3TjNNM2RVYzFUemxXYVZka1dFaHJOVGRSY0RCcVdFMVNXV1UwZUhsS1ZqY3llbk5KYkVkU1QyWlFOVkpsVDBWVU9VSk1URmN6Vlc1Tkx5dHVXRlJDTVhkdk9VeFdiMHBLVTNNcmVXTlFiRmx1TDA5ek1XcElWbGxNZVVKTFVHVnNiWFYzUWxsTFptSldjV1JpZGsxNU9GRTJURk5zT1ZKUlZYbEdSWHBGVDJOTVlWVmpSa1EzUlVKNGVUQk1VMGx4Ym1OdWNrVjZSVVo0YVd4eWVtMDJiM1lyYURKTk0wZE1lRGRDVm5rM1RrOU9NRGt6WTNZMk1rTlFPV3BUVEVsUmExaEpkemhyZDJkVmRuVlZQUS5HdFJZNks4RmFGeHg5TEhpR3M4dklERGFyVmFiRU44Mm9ycmcyUkRuaExiWjJhNHIzcU1TMS1oTEhWSzI5QXVHQl9pNUotNVM4bU1RTE1waDRwRWJRUQ==","captchCode":kaptcha}

login_data = "userName=" + rsa_userName + "&passWord=" + rsa_passWord + "&authencationHandler=UsernamePasswordAuthencationHandler&lt=LT-3692-XXiPdxofkAXFhETyMvbT-hzdzswj&_eventId=submit&execution=916aacf4-751b-434f-a31a-a068561cad41_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuVDNGUGJXeFRZMVZIUXpoVE5FZzFTWFJIYVZWS2JFUjJiVlE1ZDNkWlpVMUZPSGxHVnl0RFlXWkpRVXgxYVRSUFNFTkJaQ3N5VERoWmNGSTJVSEZ4Tm5aUksxRk1VV1pJWlRsTWNYWnVUV2RtTHpRNFJXSXlibkZ6UzNGQ1ozSnVUV2Q2VVZOWWRuUXZVMWwzVkVsUmVuRk9lVkZ0TVVNemNVcGtNM1YyYlVJMldHZFdNek5JVG5reFdscFhibEJ2YjNoeWVFdFRRbUpyVjNoMmRrZFZSMVZwT1U4d2JYWmthWFJEVWt4NFQxcGpaVEZ1TTJaVFowUkdXVkpWVkhSUE5WWmplazlHY1RoblpWbE9XV2hZYVZsb1VXUTVRM292UkVVNGFVaFBjMGR6VEUxcU5VdzRRWGhzUWt0TlVIbHVUSHBNUTFoeFZGUTNlVzU0WmpCcGVHbFpSVUprTVhOTVJIVkRhVEUxU1dSdlUyODNZWEpVTVRoc2JpOHpjREZtT0ZGTlVIUkNhMlEwSzNWaWJGWlVSMWt4ZEVaeWFGWlpTMVYxZEhkSk9GUXpWREkxYVdGU2MwcE5UVm9yVUZCd1UwaElZVTl2VGpkdGRqQmtMekV4WlU5ak1FcHhaRTlYWm1GNlJsSjFaMlZOTjFSdmMzVkJOalowV0V0a1dWWmphbUpUV25WT1IyRk1hbEJZYmtJeWJEUXdjM1pEZUhCdlptaGlaVEZNT1RKeE5HeGFXbXhuTTBsdllYcFdUVzV6UjNad2JqQkxkR0ZQZVhwa1lVOXhhMVp3VGprelZsTkdWVTFqWjFaa1NIUkZlbXhMWTBKNU0zVnhjVFF5YjJoek1rUlRNV2swTVZoSVpIVmFXVGR1Ympjd2Mwa3hkalZJUmtaV1NGTnpOME5vY2pGTGJXdElLMWxsVWtGaVVHSlJUMHBMUlZGTVYzUkpUSFZ2ZFdkRWRtbE5TRmh6WjBOM1FuQjZNRkpDZUZCUVNYazFhRnBOY25WWWIzVXpjMUppTUM5dE9DOXdXR1pzYkROUVUxRjJSa2czUXpabFlrdEtaR0ZDWTNwYU9UZzFVV3R6WkhsbFkzRk9kR3h5U2t4VlZFVmFhRVpSU0VKU1MySkhjM3BvYmxaS1dVeDNPR1p1ZG1oMFoyVkJPRXc1WVd0elYzYzFhWGxOTm1aRlEwaEJibkJNUlZwTFYyaHhkblpJTVRRNGN6RldiMVZrVW5KTGMxVkVSM2RESzNOeGIyZDJORzAzVDB3NVIwZEdSSFpXU1dwQ1JESkNVVmswYnpSbVEwSkdlWGREVVVjMVR6UjRZWGszUm1kQlZEUk5XVzA0ZUVGeWVtUk9aMjQ1TkV0cmNXMUZWVzFyU0c5dmFHUndSMlphUlVVdmJWZHFlbUpDUjFoak5HUjZZbWgwU0hSWk9FdzVWVXg1VG1oMVRFVXpVMWxtWlVOVU1GbG1kREp5TmpsWFlWVTNNMHRSWm5wSVQzTXhhRGM0Y2l0T1ZVVldiRE01YUZWeVNFWldXVlF6WkhoaGNFMUdhVlZDWm1aYWJXeDJTbkZ0VlZKbGNVSXlkRUpDVFhjM1ozWmpVblpXVWtRNGFXUklNM0YxU1RoTFJFbHViMGgzZWpWWlpVeDZNa0p3TjNNM2RVYzFUemxXYVZka1dFaHJOVGRSY0RCcVdFMVNXV1UwZUhsS1ZqY3llbk5KYkVkU1QyWlFOVkpsVDBWVU9VSk1URmN6Vlc1Tkx5dHVXRlJDTVhkdk9VeFdiMHBLVTNNcmVXTlFiRmx1TDA5ek1XcElWbGxNZVVKTFVHVnNiWFYzUWxsTFptSldjV1JpZGsxNU9GRTJURk5zT1ZKUlZYbEdSWHBGVDJOTVlWVmpSa1EzUlVKNGVUQk1VMGx4Ym1OdWNrVjZSVVo0YVd4eWVtMDJiM1lyYURKTk0wZE1lRGRDVm5rM1RrOU9NRGt6WTNZMk1rTlFPV3BUVEVsUmExaEpkemhyZDJkVmRuVlZQUS5HdFJZNks4RmFGeHg5TEhpR3M4dklERGFyVmFiRU44Mm9ycmcyUkRuaExiWjJhNHIzcU1TMS1oTEhWSzI5QXVHQl9pNUotNVM4bU1RTE1waDRwRWJRUQ==" + "&captchCode=" + kaptcha

print (login_data)
r_login = s.post('http://192.168.149.135:8082/login-web/login',data = login_data,cookies=cookies)
DZSWJ_TGC_LOGIN = r_login.cookies
print (DZSWJ_TGC_LOGIN)

print (r_login.status_code)
print (r_login.headers['content-type'])
print (r_login.encoding)
print (r_login.text)

# cookies = {"DZSWJ_TGC": DZSWJ_TGC, "JSESSION": JSESSIONID}
# swjg_dm = "13301089100"
# getSwjgMc_url = "http://192.168.149.135:8082" + "/sbzx-web/api/baseCode/get/getBaseCodeValueByName/DM_GY_SWJG?dm=" + swjg_dm
# getSwjgMc = requests.get(getSwjgMc_url,cookies = cookies)
#
# print getSwjgMc.text
# ——————————————————————————————————————————————————————————————————————————————————————

# headers = {"Cookie":"JSESSIONID=5E20ADE5B51D7F5B4B843273FA92F806; UM_distinctid=15e2cf64858155-05b3e1abba5ca9-3a3e5e06-100200-15e2cf64859a3; DZSWJ_TGC=6828a254bc31413680601eb24d2c6785; CNZZDATA1261635656=2138288276-1503988153-%7C1504599140; TGC=TGT-2503-sHI990Msl7c6ziAdQ5e5WM1MIMfAtuuYErnf7Xx5xnfCENAVde-hzdzswj","Host":"192.168.149.135:8082"}
# r = s.get('http://192.168.149.135:8082/sbzx-web/api/baseCode/get/getBaseCodeValueByName/DM_GY_SWJG?dm=13301089100&_=1504601039291',headers=headers)
