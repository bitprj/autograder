test = {
    "name": "test.py",
    "points": 1,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> mult_add(3, 0)\n0"
                },
                {
                    "code": ">>> mult_add(3, -4)\n-12"
                },
                {
                    "code": ">>> mult_add(3, 4)\n12"
                }
            ],
            "setup": ">>> from thing import *\n>>> from __MACOSX/._thing import *\n",
            "type": "doctest"
        }
    ]
}