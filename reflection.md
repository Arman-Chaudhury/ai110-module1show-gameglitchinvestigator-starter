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
  
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
