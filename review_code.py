import openai
import os
import subprocess

# Отримання OpenAI API ключа з змінної оточення
openai.api_key = os.getenv("OPENAI_API_KEY")

# Функція для отримання змін у коді
def get_code_changes():
    # Використовуйте git для отримання змін
    try:
        changes = subprocess.check_output(['git', 'diff', 'HEAD^', 'HEAD'], stderr=subprocess.STDOUT)
        return changes.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error obtaining git diff: {e.output.decode('utf-8')}")
        return ""

# Функція для виконання перевірки коду ChatGPT
def review_code(code_changes):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Використовуйте відповідну модель
        messages=[
            {"role": "system", "content": "You are a helpful code review assistant."},
            {"role": "user", "content": f"Please review the following code changes and provide feedback:\n\n{code_changes}"}
        ]
    )
    return response.choices[0].message['content']

# Отримання змін у коді
code_changes = get_code_changes()

# Перевірка коду за допомогою ChatGPT
if code_changes:
    review_feedback = review_code(code_changes)

    # Додавання коментарів з відгуками
    with open("review_feedback.txt", "w") as file:
        file.write(review_feedback)

    # Додавання коментарів до коміту на GitHub
    os.system('git add review_feedback.txt')
    os.system('git commit -m "ChatGPT Review Feedback"')
    os.system('git push')

    print("Review feedback added and committed.")
else:
    print("No code changes detected.")
