# mic - 300

To create the forensics 300 problem, run the following

```
cd src
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
bash generate.sh
```

A file named `scans.tar.gz` will be assembled, compressed, and placed in the `distFiles` directory.

Provide `distFiles/scans.tar.gz` and summary.

## Summary

There were some papers lying on the printer with random lines on them. I scanned them in. I think there is information hidden in one of the papers. Can you find out what it is?

flag: BSidesPDX{d0t}
