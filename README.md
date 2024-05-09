# About

This is the computational experiment associated with my final project for ISYE 4803-CIF (nonlinear optimization with applications to machine learning and engineering) investigating geometric programming. I included the presentation in the repository.

# How to Use

The requirements to run the code are matplotlib, networkx, and cvxpy. Additionally, I used Python version 3.11.7.

To run the first example on my slides simply run

```bash
python main.py
```

**Please note** that when you run the code, three figures will appear. **DO NOT** attempt to close these figures using the GUI exit box (red box top left corner on Mac system). Instead you need to ctrl+c in the terminal. If you do attempt to use the GUI exit button, your Python process will freeze and you must force quit out of it. This appears to be a matplotlib problem.

**You can also use this code to solve your own floor planning problems.** In the main.py file you will find the problem construction for the two problems that I demoed for my presentation. Simply use these as a template for your problem. However, please ensure that you create **valid directed acyclic graphs.** My code does not check the validity of the provided graphs, so providing an invalid graph will lead to undefined behavior. 

Also, I again refer you to the associated presentation to see what constraints I implemented in this floor planning problem. For real-world problems more factors will most likely need to be taken into account. However, this codebase should serve as a good starting point for any more realistic problem.