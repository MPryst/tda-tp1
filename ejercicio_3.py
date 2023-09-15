import sys

def merge_count(A, B):
    L = []
    inv = 0
    i = 0
    j = 0

    while i < len(A) and j < len(B):
        a = A[i]
        b = B[j]
        if a > b:
            L.append(b)
            j += 1
            inv += len(A) - i
        else:
            L.append(a)
            i += 1

    for k in range(i, len(A)):
        L.append(A[k])

    for k in range(j, len(B)):
        L.append(B[k])

    return inv, L

def sort_count(L):
    n = len(L)
    if n == 1:
        return 0, L
    
    A = L[:n//2]
    B = L[n//2:]

    ra, A = sort_count(A)
    rb, B = sort_count(B)

    r, L = merge_count(A, B)

    return r + ra + rb, L

def main():
    if len(sys.argv) != 3:
        sys.exit(f"usage: python {__file__} <nombre del archivo> <posición del capitán>")

    file_path = sys.argv[1]
    captain_index = int(sys.argv[2])

    with open(file_path) as file_handler:
        data = []

        for line in file_handler:
            splitted = line.split(",")
            name = splitted[0]
            categories = [int(c) for c in splitted[1:]]

            data.append({"name": name, "categories": categories})
    
    captain = data[captain_index]
    captain_name = captain["name"]
    category_mappings = {c: i for i, c in enumerate(captain["categories"])}

    data_mapped = [{**e, "categories": [category_mappings[c] for c in e["categories"]]} for e in data]

    solution = None
    solution_n_inv = 0

    # Para cada participante, calculamos el número de inversiones relativo al capitán.
    # El que tenga más inversiones será el mejor complemento.
    for element in data_mapped:
        name = element["name"]
        categories = element["categories"]
        n_inv, _ = sort_count(categories)
        if n_inv >= solution_n_inv:
            solution_n_inv = n_inv
            solution = name

    print(f"{captain_name},{solution}")

if __name__ == "__main__":
    main()
