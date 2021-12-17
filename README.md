# kissmbclient
Kiss (keep it stupid & simple) SMBclient python wrapper

I struggled with verifying files on the windows share from Python. Preferably I would have used an MD5 checksum. Unfortunately, the SMB protocol does not support this. That's why I only made a validation based on filesize.

To copy and verify I made a kiss wrapper. This is because the existing wrappers were not what I was looking for.


