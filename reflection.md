# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

-Hint keeps it telling us to go higher only or lower only regardless of guess. For example even when I put a guess of 1, the game tells you to go lower even though the range is 1 - 100.
-Once we guess correctly, stops letting us play. When clicking new game, the message "Game over. Start a new game to try again" instead of startign a new game
-The history doesn't continue adding values

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
When giving it the error of creating new game, it explained how the code made the game frozen instead of starting new game. It then told me where problem was and how to fix it
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When informinng claude about the hint problem, it fixed one bug, but when running the app again the error was still occuring. Then I asked it if that was the only bug for the fix, and it fixed another bug.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
When I ran the app again, the problem stopped occuring no matter what input I put.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  Claude created a pytest to verify both hint bugs were actually fixed. Running all 16 tests with pytest showed me that the logic in check_guess was broken in two independent ways — one corrupted the direction of comparison, and the other corrupted the message displayed — meaning even after fixing one bug, the hints were still wrong until both were resolved.
- Did AI help you design or understand any tests? How?
When creating pytests, Claude would give brief descriptions on what the pytests was. For the previous question, I asked it to describe the pytest it created and what is showed me about the code and it explained it.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Every time someone interacts with the page, the enitre python script runs again. In the original app, secret number was generated with random.randint() call at the top level so every rerun produced a brand new random numbber, making it impossible to guess consistently
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine every button click causes Streamlit to restart your script from line 1. All your local variables get wiped out and recreated fresh. st.session_state is like a sticky notepad that survives those restarts — anything you write to it stays there across reruns. Without it, your app has amnesia after every click.
- What change did you make that finally gave the game a stable secret number?
The fix was wrapping the secret generation in a check before assigning it — seen at app.py:93-94:

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
This means: "only pick a new secret if there isn't one already stored." On the first run it generates one and saves it to session state; on every subsequent rerun it skips that block and reuses the same number.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Having it create pytest for every change made is something I would implement as it makes sure the changes made actually work
- What is one thing you would do differently next time you work with AI on a coding task?
Next time I work with claude, I will be sure to implement to hastags so that claude can see the relationship between the UI and logicc files.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project allowed me to see that although AI may be right, it may not give you the full truth or solution to a problem but rather a fix to part of the problem