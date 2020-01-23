test = {
    "name": "test.py",
    "points": 1,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> add(1, 2)\n3\n>>> add(3, 4)\n7\n"
                },
                {
                    "code": ">>> subtract(1, 2)\n-1\n>>> subtract(4, 3)\n1\n>>> print(\"Hi\")\nHi"
                }
            ],
            "setup": ">>> from src1 import *\n>>> from src2 import *\n",
            "type": "doctest"
        }
    ]
}