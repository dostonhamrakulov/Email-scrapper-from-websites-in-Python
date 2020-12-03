This is an automated python script to search for domain emails inside one website.

Follow the next steps to set up the program locally.

1. Install python3+
2. Install dependencies
    pip3 install -r requirements.txt

To run the program you first need to make sure your input data meets the
following conditions:

1. It is in csv format
2. Has only 1 column with a Header named website
3. Every following row contains urls

You run the program with the following command line command

python3 extract_from_csv.py websites.csv

What does the script do?

The script will go through each of the urls and it will extract the homepage
and save it as base_url. Then it will check if the base_url has already been
scrapped for emails in the email_db.csv . If it the base_url has been scrapped
it will return the scrapped email address. If the base_url has not been scrapped,
it will start looking in the base_url for emails, going through every website of the
domain until it finds either a couple emails or it has visited more than 30 subpages
of the domain. It will then save the result in the email_db.csv. After it has gone
through all the websites in the file, it will save the results in a new file.


