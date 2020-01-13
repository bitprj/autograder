test = {
    "name": "test.py",
    "points": 1,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> # This is all inside a file called test1.test; the comments are not necessary and for documentation\n>>> # You MUST type >>> like in the Python command prompt since okpy will run this character by character\n>>> num_sides(3)\n'triangle'\n>>> # okpy compares outputs when there is no leading >>>, the 'triangle' with the source's output\n>>> # okpy will append code to import all the source files' functions so no need to import num_sides() in the test file\n"
                }
            ],
            "setup": ">>> from a import *\n",
            "type": "doctest"
        }
    ]
}