import gpsoauth

email = 'jackpanos02@gmail.com'
android_id = '0123456789abcdef'
token = 'oauth2_4/0AdLIrYf5rQ-Zvwha_TUBKr1KpR8VsTo4QGEKSy2lNG1_Qrfj9B5PBU3DlI1JQbiaf3mVog' # insert the oauth_token here

master_response = gpsoauth.exchange_token(email, token, android_id)
master_token = master_response["Token"]  # if there's no token check the response for more details

print(master_token, "Master token here  < ---- -- - ---- ---- -- ")