test = {
    "name": "test.py",
    "points": 1,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> num_sides(\"triangle\")\n3\n"
                },
                {
                    "code": ">>> num_sides = 3\n>>> shape_name(num_sides)\n'triangle'"
                }
            ],
            "setup": ">>> from a import *\n>>> from b import *\n",
            "type": "doctest"
        }
    ]
}