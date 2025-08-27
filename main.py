from classes import Package, Hashtable

packages = Hashtable()
for i in range(0, 41):
    packages.insert(
        Package(
            id=i,
            address=str(i) + " test way",
            city="Salt Lake",
            state="UT",
            zip=123455,
            weight=100,
        )
    )
    print(f"\n{packages.get(i)}, {packages.size}")
