import os
import datetime as dt
import pandas as pd
import email_module

max_nastavene = 26
min_nastavene = 15

now = dt.datetime.now()
ago = now - dt.timedelta(days=1)
dff = pd.DataFrame()

for root, dirs, files in os.walk("data"):
    for fname in files:
        path = os.path.join(root, fname)
        st = os.stat(path)
        mtime = dt.datetime.fromtimestamp(st.st_mtime)
        if mtime > ago:
            print("%s modified %s" % (path, mtime))
            df = pd.read_csv(path, index_col=None, header=0)
            dff = dff.append(df, ignore_index=True)

dff.set_index("id", drop=True, inplace=True)
dff.to_csv("data/analyze.csv")

maximum = dff["teplota"].max()
minimum = dff["teplota"].min()

dff_max_alert = dff[dff.teplota > max_nastavene]
dff_min_alert = dff[dff.teplota < min_nastavene]

email_message = f"""
Dobry den...

{dff_max_alert}
"""
email_module.send_email(email_message)

# TODO append to historical data


# dff_min_alert

# if maximum > max_nastavene:
