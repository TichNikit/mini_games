# uvicorn main:app --reload
# http://localhost:8000
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random

from fastapi import status

from lists import prediction, party, words, max_attempts, list_answer

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get("/")
async def get_welcome(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('welcome.html', {"request": request})


@app.get("/heads_and_tails")
async def get_welcome(request: Request) -> HTMLResponse:
    list_ = ["Орёл", "Решка"]
    answer = random.choice(list_)
    return templates.TemplateResponse('heads_and_tails.html', {"request": request, 'answer': answer})


@app.get("/cube")
async def get_welcome(request: Request) -> HTMLResponse:
    list_ = [1, 2, 3, 4, 5, 6]
    answer = random.choice(list_)
    return templates.TemplateResponse('cube.html', {"request": request, 'answer': answer})


@app.get("/prediction")
async def get_welcome(request: Request) -> HTMLResponse:
    list_ = prediction
    answer = random.choice(list_)
    return templates.TemplateResponse('prediction.html', {"request": request, 'answer': answer})


@app.get("/cube_for_party")
async def get_welcome(request: Request) -> HTMLResponse:
    list_ = party
    answer = random.choice(list_)
    return templates.TemplateResponse('cube_for_party.html', {"request": request, 'answer': answer})


@app.get("/guess_number")
async def get_welcome(request: Request) -> HTMLResponse:
    global number
    number = random.randint(1, 100)
    print(number)
    return templates.TemplateResponse('guess_number.html', {"request": request, 'number': number})


@app.post("/guess_number")
async def get_welcome(request: Request, number_user: int = Form(...)) -> HTMLResponse:
    if not number:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    if number < number_user:
        error = "Ваша число слишком большое, попробуйте ещё раз"
    elif number > number_user:
        error = "Ваша число слишком маленькое, попробуйте ещё раз"
    else:
        error = "Вы отгадали"
    return templates.TemplateResponse('guess_number.html', {"request": request, 'error': error})


@app.get("/body_weight")
async def get_welcome(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('body_weight.html', {"request": request})


@app.post("/body_weight")
async def get_welcome(request: Request, weight: int = Form(...), height: int = Form(...)) -> HTMLResponse:
    body_index = weight / (height/100) ** 2
    body_index = round(body_index, 2)
    if body_index < 16:
        error = "Вы отгадали"
    elif 16 < body_index < 18.5:
        error = "Недостаток массы тела"
    elif 18.5 < body_index < 24.99:
        error = "Норма"
    elif 25 < body_index < 30:
        error = "Избыток массы тела"
    elif 30 < body_index < 35:
        error = "Ожирение первой степени"
    elif 35 < body_index < 40:
        error = "Ожирение второй степени"
    else:
        error = "Ожирение третьей степени"
    return templates.TemplateResponse('body_weight.html', {"request": request, "body_index": body_index,
                                                            "error": error})

@app.get("/hangman")
async def get_hangman(request: Request) -> HTMLResponse:
    global word_to_guess, displayed_word, remaining_attempts, wrong_letters
    word_to_guess = random.choice(words)
    displayed_word = "_" * len(word_to_guess)
    remaining_attempts = max_attempts
    wrong_letters = ""
    return templates.TemplateResponse("hangman.html", {
        "request": request,
        "displayed_word": displayed_word,
        "remaining_attempts": remaining_attempts,
        "wrong_letters": wrong_letters,
        "message": ""
    })

@app.post("/hangman")
async def post_hangman(request: Request, letter: str = Form(...)):
    global word_to_guess, displayed_word, remaining_attempts, wrong_letters

    if letter in wrong_letters or letter in displayed_word:
        message = "Вы уже угадывали эту букву."
        return templates.TemplateResponse("hangman.html", {
            "request": request,
            "displayed_word": displayed_word,
            "remaining_attempts": remaining_attempts,
            "wrong_letters": wrong_letters,
            "message": message
        })

    if letter in word_to_guess:
        displayed_word = "".join([letter if word_to_guess[i] == letter else displayed_word[i]
                                   for i in range(len(word_to_guess))])
    else:
        wrong_letters += letter
        remaining_attempts -= 1

    if remaining_attempts == 0:
        message = "Вы проиграли! Загаданное слово: " + word_to_guess
        return templates.TemplateResponse("hangman.html", {
            "request": request,
            "displayed_word": displayed_word,
            "remaining_attempts": remaining_attempts,
            "wrong_letters": wrong_letters,
            "message": message
        })
    elif "_" not in displayed_word:
        message = "Вы выиграли!"
        return templates.TemplateResponse("hangman.html", {
            "request": request,
            "displayed_word": displayed_word,
            "remaining_attempts": remaining_attempts,
            "wrong_letters": wrong_letters,
            "message": message
        })

    message = ""
    return templates.TemplateResponse("hangman.html", {
        "request": request,
        "displayed_word": displayed_word,
        "remaining_attempts": remaining_attempts,
        "wrong_letters": wrong_letters,
        "message": message
    })

@app.get("/hangman/reset")
async def reset_hangman(request: Request) -> HTMLResponse:
    global word_to_guess, displayed_word, remaining_attempts, wrong_letters
    word_to_guess = random.choice(words)
    displayed_word = "_" * len(word_to_guess)
    remaining_attempts = max_attempts
    wrong_letters = ""
    return templates.TemplateResponse("hangman.html", {
        "request": request,
        "displayed_word": displayed_word,
        "remaining_attempts": remaining_attempts,
        "wrong_letters": wrong_letters,
        "message": ""
    })


@app.get("/magic_ball")
async def magic(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("magic_ball.html", {"request": request})


@app.post("/magic_ball")
async def magic(request: Request, your_question: str = Form(...)) -> HTMLResponse:
    if your_question.isdigit():
        answer = "Это точно вопрос? Или это шифр?"
    elif len(your_question) <= 3:
        answer = "Короткий вопрос..."
    else:
        answer = random.choice(list_answer)
    return templates.TemplateResponse("magic_ball.html", {"request": request, "answer": answer})