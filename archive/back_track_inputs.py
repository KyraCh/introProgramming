import pandas as pd


def go_back(original_questions: list[str]) -> list[str]:

    # send all the questions you'll ask the user in an input
    questionStack = original_questions
    answerStack = []
    i = 0
    print(
        "/// Write in any helpful code here e.g. ///\n\n type [b] to go back\t type [q] to quit\n")
    while i < len(questionStack):
        answer = input(questionStack[i])

        if answer == 'b':
            if i == 0:
                break
            answerStack.pop()
            i -= 1
            continue
        elif answer == 'q':
            break

        answerStack.append(answer)
        i += 1

    # returns a tuple --> first element will tell you whether or not they answered all the questions
    # ------------------> second element will give you the list of answers you need so you can easily just append it to the end of the dataframe
    return (len(answerStack) == len(questionStack), answerStack)


# global variable
df = pd.read_csv('emergency_database.csv')


def create_user_profile():

    questions = ['Emergency ID: ', 'Location: ', 'Type: ',
                 'Description: ', 'Start date: ', 'Close date: ']
    all_answered, answers = go_back(questions)

    if all_answered:
        df.loc[len(df)] = answers

    print(df)


create_user_profile()
