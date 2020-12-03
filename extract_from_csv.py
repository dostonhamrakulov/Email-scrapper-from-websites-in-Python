from core import email_finder_from_base_url, extract_base_url
import sys
import pandas as pd
from datetime import datetime

assert '.csv'  in sys.argv[1], "Needs to be a csv file"

file = sys.argv[1]

df = pd.read_csv(file)
assert 'website' in df.columns, "The name of the column with links has to be: website"

df['base_url'] = df.website.apply(lambda x:extract_base_url(x))

df['Email'] = df.base_url.apply(lambda x:email_finder_from_base_url(x))

df.to_csv(f'{file.replace(".csv","")}_{str(datetime.today()).split(" ")[0]}.csv', index = False)



