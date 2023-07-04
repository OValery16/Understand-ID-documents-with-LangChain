# Understand-IDs-with-LangChain
The goal of this project is to connect docteller API with LangChain to analyze ID documents.

The first step is to go to [docteller](https://www.docteller.com/?v=1) and [huggingface](https://huggingface.co/) 
website and create an account. Then, you can get your API key and use it in the code. (create .env 
file and add your API key to it)

We first use docteller API to extract the text from the ID document (`docteller_parsing`). Then, 
we create a custom prompt and use LangChain to send a request to huggingface API and get the
result (`ask_HuggingFace_model`).

The output of the following code should be:

```
The person's name is Maelys Gaëlle Marie Martin. She is a woman and was born on July 13th, 1990 in
Paris. She is currently 32 years old and her date of birth is July 13th, 1990. She is a French
citizen and her date of birth is July 13th, 1990.
```

# Important remark

If you like you like this project, feel free to leave a star. (it is my only reward ^^)

