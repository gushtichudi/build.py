int max(int n[]);

int max(int n[]) {
    int len = sizeof(n) / sizeof(n[0]);
    int m = n[0];

    for (int i = 0; i < len; ++i)
        if (n[i] > m)
            m = n[0];

    return m;
}
