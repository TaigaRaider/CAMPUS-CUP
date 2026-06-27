# Testing Guide for CAMPUS-CUP

This guide explains how to write test cases for different levels of the system and details the **Test Driven Development (TDD)** approach.

---

## 1. Testing Levels

### A. Function/Unit Testing
**What it is:** Testing the smallest parts of the application in isolation (individual functions or methods).
**Why:** To ensure that each component logic is correct before it interacts with others.

**Example: Testing `check_admin` function**
```python
import unittest
from classes import User, check_admin

class TestUtils(unittest.TestCase):
    def test_check_admin_returns_true_for_admin(self):
        admin = User(user_name="Boss", is_admin=True)
        self.assertTrue(check_admin(admin))

    def test_check_admin_returns_false_for_non_admin(self):
        user = User(user_name="Guest", is_admin=False)
        self.assertFalse(check_admin(user))
```

**Example: Testing `Team.add_player`**
```python
class TestTeam(unittest.TestCase):
    def test_add_player_success(self):
        admin = User("Admin", True)
        team = Team("Alpha FC")
        player = Player("John", "ST")
        team.add_player(admin, player)
        self.assertIn(player, team.players)
```

---

### B. Integration Testing
**What it is:** Testing how different units or modules work together.
**Why:** To identify bugs that arise when components interact (e.g., data passing, state changes across classes).

**Example: League and Match Interaction**
Testing if creating a Match correctly references the League and if the League can validate officials for that match.
```python
class TestIntegration(unittest.TestCase):
    def test_match_league_integration(self):
        admin = User("Admin", True)
        league = League("Campus Cup", 10, "Football", admin)
        team1 = Team("Team A")
        team2 = Team("Team B")
        match = league.Match(team1, team2, league)
        
        self.assertEqual(match.container_league.league_name, "Campus Cup")
```

---

### C. System Testing
**What it is:** Testing the complete, integrated system to verify it meets requirements.
**Why:** To ensure the whole "business flow" works from start to finish.

**Example: Full Tournament Setup Flow**
1. Create Admin.
2. Create League.
3. Create Teams and add Players.
4. Add Teams to League.
5. Create and Schedule a Match.
6. Verify the Match status and ID generation.

---

## 2. Test Driven Development (TDD) Approach

TDD is a software development process where you write tests **before** you write the actual code. It follows the **Red-Green-Refactor** cycle.

### The Cycle:
1.  **🔴 RED (Write a failing test):** 
    Write a test for a small bit of functionality that doesn't exist yet. Run it and watch it fail.
    *   *Why?* To define exactly what the code should do.
2.  **🟢 GREEN (Make it pass):** 
    Write the *minimum* amount of code necessary to make the test pass.
    *   *Why?* To avoid over-engineering and focus on requirements.
3.  **🔵 REFACTOR (Clean up):** 
    Clean up the code you just wrote. Ensure it follows coding standards, remove duplication, but keep the tests passing.
    *   *Why?* To maintain high code quality without breaking functionality.

### Why use TDD?
-   **Reduced Bugs:** You catch errors immediately.
-   **Better Design:** It forces you to think about the interface and usage before implementation.
-   **Documentation:** Tests serve as live documentation of how the code is expected to behave.
-   **Confidence:** You can change code later knowing the tests will catch any regressions.

---

## 3. Summary of "Why" We Test

| Level | Main Goal | Focus |
| :--- | :--- | :--- |
| **Unit** | Correctness | Logic, Math, Edge Cases |
| **Integration** | Communication | API, Data Flow, Dependencies |
| **System** | Functionality | User Journeys, End-to-End Requirements |
| **TDD** | Reliability/Design | Maintainability, Specification, Confidence |
