# Eli5NearTx
An AI tool for explaining the operations, involved parties, and overall purpose of a NEAR transaction

---

### Development

#### Quick start

##### Install dependencies

```sh
pip install flask openai python-dotenv requests
```

##### Get OpenAI API key
This project uses OpenAI API to interact with the `gpt-4o` model. An API key is required, and must be placed in the `.env` file. An example file structure can be found at `.env.example`.

##### Run development server
```sh
flask run
```

