<div align="center">

[//]: # (  <img src="frontend/src/assets/images/logo.png" alt="logo" width="150" height="auto" />)
  <h1>Let'EmCook</h1>
  <p>
    The purpose of this project is to promote healthy eating habits by providing users with a transparent view of their nutritional intake and prioritizing home cooking over packaged quick meals.
  </p>
  
<!-- Badges -->
<p>
  <a href="https://github.com/ramz1t/LetEmCook/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/ramz1t/LetEmCook" alt="contributors" />
  </a>
  <a href="https://github.com/ramz1t/LetEmCook/commits/master">
    <img src="https://img.shields.io/github/last-commit/ramz1t/LetEmCook" alt="last update" />
  </a>
</p>
</div>

<!-- Env Variables -->

### :key: Environment Variables

To run this project, you will need to add the following environment variables to your .env file.

.env
```env
MISTRAL_API_KEY=your-api-key
```

<!-- #### Frontend

frontend/.../.env.deploy

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your password>
DB_HOST=db
DB_PORT=5432
``` -->

<!-- Getting Started -->

### :toolbox: Getting Started


Clone the project

```bash
git clone https://github.com/ramz1t/LetEmCook.git
```

### Before first start

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
alembic upgrade head
```

Add dump data to the database

```bash
python app/populate_db.py
```

Don't forget to add your Mistral key if you want to use "Enhance" feature in recipes!