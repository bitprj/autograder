test = {
    "name": "test.py",
    "points": 1,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> square(2)\n4\n"
                },
                {
                    "code": ">>> subtract(1, 2)\n-1\n>>> subtract(4, 3)\n1\n>>> print(\"Hi\")\nHi"
                },
                {
                    "code": ">>> print(\"a\")\nb\n"
                },
                {
                    "code": ">>> square(2)\n4\n"
                }
            ],
            "setup": ">>> from src1 import *\n>>> from src2 import *\n>>> from doMath import *\n",
            "type": "doctest"
        }
    ]
}