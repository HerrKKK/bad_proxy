import hmac

digest = hmac.new('test uuid'.encode(), 'test msg'.encode(), 'sha256').digest()
print(len(digest))
