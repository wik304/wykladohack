colloquium_bank = [
    {
        "task": "Napisz program wypisujący liczby od 1 do 10.",
        "language": "c",
        "variants": [
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    for (int i = 1; i <= 10; i++)",
                    "        printf(\"%d\\n\", i);",
                    "    return 0;",
                    "}"
                ],
                "errors": [2]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    for (int i = 1; i < 10; i++)",
                    "        printf(\"%d\\n\", i)",
                    "    return 0;",
                    "}"
                ],
                "errors": [2, 3]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    for (int i = 1; i < 10 i++)",
                    "        printf(\"%d\\n\", i)",
                    "    return 0",
                    "}"
                ],
                "errors": [2, 3, 4]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    for (int i = 1; i <= 10; i++) {",
                    "        printf(\"%d\\n\", i);",
                    "    }",
                    "    return 0;",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz program wypisujący sumę dwóch liczb.",
        "language": "c",
        "variants": [
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int a, b;",
                    "    scanf(\"%d %d\", &a, &b);",
                    "    printf(\"Suma: %d\\n\", a + b);",
                    "    return 0;",
                    "}"
                ],
                "errors": [3]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int a, b;",
                    "    printf(\"Podaj liczby:\");",
                    "    printf(\"Suma: %d\\n\", a + b);",
                    "    return 0;",
                    "}"
                ],
                "errors": [3, 4]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int a, b;",
                    "    scanf(\"%d %d\", &a, &b)",
                    "    printf(\"%d\\n\", a + b)",
                    "    return 0",
                    "}"
                ],
                "errors": [3, 4, 5]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int a, b;",
                    "    printf(\"Podaj liczby: \");",
                    "    scanf(\"%d %d\", &a, &b);",
                    "    printf(\"Suma: %d\\n\", a + b);",
                    "    return 0;",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz program obliczający silnię liczby n.",
        "language": "c",
        "variants": [
            {
                "code": [
                    "#include <stdio.h>",
                    "int factorial(int n) {",
                    "    if (n == 0) return 1;",
                    "    return n * factorial(n - 1);",
                    "}",
                    "int main() {",
                    "    int n;",
                    "    scanf(\"%d\", &n);",
                    "    printf(\"%d\", factorial(n));",
                    "    return 0;",
                    "}"
                ],
                "errors": [7]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int factorial(int n) {",
                    "    if (n == 0) return 1;",
                    "    return n * factorial(n - 1);",
                    "}",
                    "int main() {",
                    "    int n;",
                    "    printf(\"Podaj liczbę: \");",
                    "    printf(\"%d\", factorial(n));",
                    "    return 0;",
                    "}"
                ],
                "errors": [7, 8]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int factorial(int n) {",
                    "    if n == 0 return 1",
                    "    return n * factorial(n - 1);",
                    "}",
                    "int main() {",
                    "    int n;",
                    "    printf(\"%d\", factorial(n));",
                    "    return 0;",
                    "}"
                ],
                "errors": [2, 7, 8]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int factorial(int n) {",
                    "    if (n == 0) return 1;",
                    "    return n * factorial(n - 1);",
                    "}",
                    "int main() {",
                    "    int n;",
                    "    printf(\"Podaj liczbę: \");",
                    "    scanf(\"%d\", &n);",
                    "    printf(\"%d\", factorial(n));",
                    "    return 0;",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz program, który zamienia dwa elementy tablicy.",
        "language": "c",
        "variants": [
            {
                "code": [
                    "#include <stdio.h>",
                    "void swap(int a, int b) {",
                    "    int temp = a;",
                    "    a = b;",
                    "    b = temp;",
                    "}",
                    "int main() {",
                    "    int arr[2] = {1, 2};",
                    "    swap(arr[0], arr[1]);",
                    "    printf(\"%d %d\", arr[0], arr[1]);",
                    "    return 0;",
                    "}"
                ],
                "errors": [1]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "void swap(int* a, int* b) {",
                    "    int temp = *a;",
                    "    *a = *b;",
                    "    *b = temp;",
                    "}",
                    "int main() {",
                    "    int arr[2] = {1, 2};",
                    "    swap(arr[0], arr[1]);",
                    "    printf(\"%d %d\", arr[0], arr[1]);",
                    "    return 0;",
                    "}"
                ],
                "errors": [8]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "void swap(int* a, int* b) {",
                    "    temp = *a;",
                    "    *a = *b;",
                    "    *b = temp;",
                    "}",
                    "int main() {",
                    "    int arr[2] = {1, 2};",
                    "    swap(&arr[0], &arr[1]);",
                    "    printf(\"%d %d\", arr[0], arr[1]);",
                    "    return 0;",
                    "}"
                ],
                "errors": [2, 4]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "void swap(int* a, int* b) {",
                    "    int temp = *a;",
                    "    *a = *b;",
                    "    *b = temp;",
                    "}",
                    "int main() {",
                    "    int arr[2] = {1, 2};",
                    "    swap(&arr[0], &arr[1]);",
                    "    printf(\"%d %d\", arr[0], arr[1]);",
                    "    return 0;",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz program wypisujący największy element tablicy.",
        "language": "c",
        "variants": [
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int arr[4] = {5, 2, 9, 1};",
                    "    int max = arr[0];",
                    "    for (int i = 1; i < 4; i++) {",
                    "        if (arr[i] > max) max = arr[i];",
                    "    }",
                    "    printf(\"Największy: %d\", max);",
                    "    return 0;",
                    "}"
                ],
                "errors": [7]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int arr[4] = {5, 2, 9, 1};",
                    "    int max = arr[0];",
                    "    for (int i = 1; i < 4; i++)",
                    "        if (arr[i] > max) max = arr[i];",
                    "    printf(\"Największy: %d\", max);",
                    "    return 0;",
                    "}"
                ],
                "errors": [5, 6]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int arr[] = {5, 2, 9, 1};",
                    "    int max;",
                    "    for (int i = 1; i < 4; i++) {",
                    "        if (arr[i] > max) max = arr[i];",
                    "    }",
                    "    printf(\"Największy: %d\", max);",
                    "    return 0;",
                    "}"
                ],
                "errors": [3, 5]
            },
            {
                "code": [
                    "#include <stdio.h>",
                    "int main() {",
                    "    int arr[] = {5, 2, 9, 1};",
                    "    int max = arr[0];",
                    "    for (int i = 1; i < 4; i++) {",
                    "        if (arr[i] > max) max = arr[i];",
                    "    }",
                    "    printf(\"Największy: %d\", max);",
                    "    return 0;",
                    "}"
                ],
                "errors": []
            }
        ]
    },
    {
        "task": "Napisz program wypisujący 'Hello World'.",
        "language": "java",
        "variants": [
            {
                "code": [
                    "public class HelloWorld {",
                    "    public static void main(String args) {",
                    "        System.out.println(\"Hello World\")",
                    "    }",
                    ""  # brak nawiasu zamykającego
                ],
                "errors": [1, 2, 4]
            },
            {
                "code": [
                    "public class HelloWorld {",
                    "    public static void main(String args) {",
                    "        System.out.println(\"Hello World\")",
                    "    }",
                    "}"
                ],
                "errors": [1, 2]
            },
            {
                "code": [
                    "public class HelloWorld {",
                    "    public static void main(String[] args) {",
                    "        System.out.println(\"Hello World\")",
                    "    }",
                    "}"
                ],
                "errors": [2]
            },
            {
                "code": [
                    "public class HelloWorld {",
                    "    public static void main(String[] args) {",
                    "        System.out.println(\"Hello World\");",
                    "    }",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz program obliczający sumę dwóch liczb.",
        "language": "java",
        "variants": [
            {
                "code": [
                    "public class Sum {",
                    "    public static void main(String[] args) {",
                    "        int a = 5;",
                    "        int b = 10;",
                    "        System.out.println(a + b)",  # brak średnika
                    "    }",
                    ""  # brak nawiasu kończącego klasę
                ],
                "errors": [4, 6]
            },
            {
                "code": [
                    "import java.util.Scanner;",
                    "public class Sum {",
                    "    public static void main(String[] args) {",
                    "        Scanner sc = new Scanner(System.in);",
                    "        int a = sc.nextInt()",  # brak średnika
                    "        int b = sc.nextInt();",
                    "        System.out.println(a + b);",
                    "    }",
                    "}"
                ],
                "errors": [4]
            },
            {
                "code": [
                    "import java.util.Scanner;",
                    "public class Sum {",
                    "    public static void main(String[] args) {",
                    "        Scanner sc = new Scanner(System.in);",
                    "        int a = sc.nextInt()",  # brak średnika
                    "        int b = sc.nextInt()",  # brak średnika
                    "        System.out.println(a + b);",
                    "    }",
                    "}"
                ],
                "errors": [4, 5]
            },
            {
                "code": [
                    "import java.util.Scanner;",
                    "public class Sum {",
                    "    public static void main(String[] args) {",
                    "        Scanner sc = new Scanner(System.in);",
                    "        int a = sc.nextInt();",
                    "        int b = sc.nextInt();",
                    "        System.out.println(a + b);",
                    "    }",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz klasę Person z polem name i metodą hello().",
        "language": "java",
        "variants": [
            {
                "code": [
                    "public class Person {",
                    "    string name",  # zła wielkość litery, brak średnika
                    "    void hello() {",
                    "        System.out.println(\"Hi, I'm \" + name)",  # brak średnika
                    "    }"
                ],
                "errors": [1, 3]
            },
            {
                "code": [
                    "public class Person {",
                    "    string name;",  # zła wielkość litery
                    "    void hello() {",
                    "        System.out.println(\"Hi, I'm \" + name);",
                    "    }",
                    "}"
                ],
                "errors": [1]
            },
            {
                "code": [
                    "public class Person {",
                    "    String name;",
                    "    void hello() {",
                    "        System.out.println(\"Hi, I'm \" + name)",  # brak średnika
                    "    }",
                    "}"
                ],
                "errors": [3]
            },
            {
                "code": [
                    "public class Person {",
                    "    String name;",
                    "    void hello() {",
                    "        System.out.println(\"Hi, I'm \" + name);",
                    "    }",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz program z metodą rekurencyjną obliczającą silnię.",
        "language": "java",
        "variants": [
            {
                "code": [
                    "public class Factorial {",
                    "    static int fact(n) {",  # brak typu
                    "        if n == 0 return 1",  # brak nawiasów, średnika
                    "        return n * fact(n - 1);",
                    "    }",
                    "    public static void main(String[] args) {",
                    "        System.out.println(fact(5))",  # brak średnika
                    "    }",
                    "}"
                ],
                "errors": [1, 2, 6]
            },
            {
                "code": [
                    "public class Factorial {",
                    "    static int fact(int n) {",
                    "        if n == 0 return 1;",  # brak nawiasów
                    "        return n * fact(n - 1);",
                    "    }",
                    "    public static void main(String[] args) {",
                    "        System.out.println(fact(5))",  # brak średnika
                    "    }",
                    "}"
                ],
                "errors": [2, 6]
            },
            {
                "code": [
                    "public class Factorial {",
                    "    static int fact(int n) {",
                    "        if n == 0 return 1;",  # brak nawiasów
                    "        return n * fact(n - 1);",
                    "    }",
                    "    public static void main(String[] args) {",
                    "        System.out.println(fact(5));",
                    "    }",
                    "}"
                ],
                "errors": [2]
            },
            {
                "code": [
                    "public class Factorial {",
                    "    static int fact(int n) {",
                    "        if (n == 0) return 1;",
                    "        return n * fact(n - 1);",
                    "    }",
                    "    public static void main(String[] args) {",
                    "        System.out.println(fact(5));",
                    "    }",
                    "}"
                ],
                "errors": []
            }
        ]
    },

    {
        "task": "Napisz klasę licznik inkrementujący wartość.",
        "language": "java",
        "variants": [
            {
                "code": [
                    "public class Counter {",
                    "    int value = 0",
                    "    void increment()",
                    "        value++",
                    "    int get() {",
                    "        return value",
                    "    }",
                    ""
                ],
                "errors": [1, 2, 5]
            },
            {
                "code": [
                    "public class Counter {",
                    "    int value = 0;",
                    "    void increment()",  # brak nawiasów klamrowych
                    "        value++;",
                    "    int get() {",
                    "        return value;",
                    "    }",
                    "}"
                ],
                "errors": [2]
            },
            {
                "code": [
                    "public class Counter {",
                    "    int value = 0;",
                    "    void increment() {",
                    "        value++",  # brak średnika
                    "    }",
                    "    int get() {",
                    "        return value",
                    "    }",
                    "}"
                ],
                "errors": [3, 6]
            },
            {
                "code": [
                    "public class Counter {",
                    "    int value = 0;",
                    "    void increment() {",
                    "        value++;",
                    "    }",
                    "    int get() {",
                    "        return value;",
                    "    }",
                    "}"
                ],
                "errors": []
            }
        ]
    }
]
