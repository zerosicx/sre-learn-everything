# Learnings

Transform Your Project Into a Package
Packages are useful for structuring Python code into logical groupings for large programs. Because your web project can grow large, too, transforming your project into a package makes sense. Since you’re just at the start of the project, your to-do list to create the package has only three tasks:

1. Creating a package folder named board/
2. Moving app.py into board/
2. Renaming app.py to __init__.py

Which can be done with the following commands:
```
(venv) $ mkdir board
(venv) $ mv app.py board/__init__.py
```

To run the application,
```
python3 -m flask --app board
```