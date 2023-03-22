import random
import requests

def otp(phone):
    otp_number = random.randint(1001,9999)
    
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = f"variables_values={otp_number}&route=otp&numbers={phone}"
    headers = {
        'authorization': "LzDfy8EGHOTJwIxZB2WM9YbmFkcp0avodP3jg5CVitX4elqQh1zgl5y4rbwAYfDGJxcetus8T1aHWROS",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)


    import http.client

    conn = http.client.HTTPSConnection("d7sms.p.rapidapi.com")

    headers = {
        'Token': "undefined",
        'X-RapidAPI-Key': "151ad70285msh597648138d24f0ep187c02jsn57c0c507846e",
        'X-RapidAPI-Host': "d7sms.p.rapidapi.com"
        }

    conn.request("POST", "/messages/v1/balance", headers=headers)
    
    def otpsend():
        return otp_number
        
    return otpsend

