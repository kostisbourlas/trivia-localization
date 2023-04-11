# transifex_assignment

<b>Setup:</b> <br>
`python3 -m venv venv` <br>
`source venv/bin/activate`<br>
`pip install --upgrade pip` <br>
`pip install -r requirements.txt` <br>

Create an `.env` file containing 2 variables: <br>

1. `TRANSIFEX_SECRET_KEY`: User's auth token
2. `TRANSIFEX_ORG_PROJECT`: in format: `o:organization_slug:p:project_slug`

<b>Example `.env`:</b> <br>

`TRANSIFEX_SECRET_KEY=0934IRGOENRGJENRGREOERNGOERN`
`TRANSIFEX_ORG_PROJECT=o:my_company:p:my_project`

<b>Run command example:</b> <br>
`python manage.py localize_trivias --categories "General Knowledge" "Entertainment: Books" "Science: Computers"`
