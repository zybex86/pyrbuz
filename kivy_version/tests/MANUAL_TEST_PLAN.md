# Manual Test Plan for Suika Game

| Test Case                              | Steps                                                                 | Expected Result                         |
|-----------------------------------------|-----------------------------------------------------------------------|-----------------------------------------|
| **Game Launch**                        | Start the game                                                        | Game window opens, UI is visible        |
| **Drop Fruit**                         | Click/tap inside play area                                            | Fruit drops at clicked position         |
| **Move Preview**                       | Touch and drag preview fruit horizontally                             | Preview moves with touch                |
| **Drop Large Fruit**                   | Drop a large fruit near the top                                       | Game does not end unless fruit crosses line |
| **Merge Fruits**                       | Drop two same fruits so they collide                                  | Fruits merge, score increases           |
| **Game Over**                          | Stack fruits so one crosses the red line                              | "GAME OVER" message appears             |
| **Restart Button**                     | Click the Restart button                                              | Game resets, score is zero, UI updates  |
| **Score Updates**                      | Merge fruits or restart game                                          | Score label updates correctly           |
| **Window Resize**                      | Resize the game window                                                | Play area and UI adjust responsively    |
| **Touch Outside Play Area**            | Click/tap outside play area (on button)                               | Button responds, fruit is not dropped   |
| **Preview Image**                      | Start game, observe preview fruit                                     | Preview is correct, not a white square  |

---

**Instructions:**
- Perform each test case and verify the expected result.
- Report any failures or unexpected behavior.
- Update this plan as new features are added.
