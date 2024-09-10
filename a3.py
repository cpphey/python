def maxPlusArea(grid, n, m):
    def calcArmLengths(grid, n, m):
        up = [[0] * m for _ in range(n)]
        down = [[0] * m for _ in range(n)]
        left = [[0] * m for _ in range(n)]
        right = [[0] * m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'G':
                    up[i][j] = (up[i - 1][j] + 1) if i > 0 else 1
                    left[i][j] = (left[i][j - 1] + 1) if j > 0 else 1

        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                if grid[i][j] == 'G':
                    down[i][j] = (down[i + 1][j] + 1) if i < n - 1 else 1
                    right[i][j] = (right[i][j + 1] + 1) if j < m - 1 else 1

        return up, down, left, right

    def findPluses(up, down, left, right, n, m):
        pluses = []
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'G':
                    max_len = min(up[i][j], down[i][j], left[i][j], right[i][j])
                    for k in range(max_len):
                        area = 4 * k + 1
                        pluses.append((area, i, j, k))
        return pluses

    def isOverlap(p1, p2):
        (area1, x1, y1, arm1) = p1
        (area2, x2, y2, arm2) = p2
        # Collect cells for both pluses
        cells1 = set()
        cells2 = set()

        for d in range(arm1 + 1):
            cells1.add((x1 + d, y1))  # down
            cells1.add((x1 - d, y1))  # up
            cells1.add((x1, y1 + d))  # right
            cells1.add((x1, y1 - d))  # left

        for d in range(arm2 + 1):
            cells2.add((x2 + d, y2))  # down
            cells2.add((x2 - d, y2))  # up
            cells2.add((x2, y2 + d))  # right
            cells2.add((x2, y2 - d))  # left

        return len(cells1 & cells2) > 0

    up, down, left, right = calcArmLengths(grid, n, m)
    pluses = findPluses(up, down, left, right, n, m)

    max_product = 0
    for i in range(len(pluses)):
        for j in range(i + 1, len(pluses)):
            if not isOverlap(pluses[i], pluses[j]):
                max_product = max(max_product, pluses[i][0] * pluses[j][0])

    return max_product


# Input Reading
#n, m = map(int, input().split())
#grid = [input().strip() for _ in range(n)]

# Function call
#result = maxPlusArea(grid, n, m)
#print(result)


def twoPluses(grid):
    dim = grid[0]
    bg=grid[1:]
    return maxPlusArea(bg, dim[0], dim[1])


if __name__ == "__main__":
    print("hi")
    g=[]
    g.append([5,6])
    g.append("GGGGGG")
    g.append("GBBBGB")
    g.append("GGGGGG")
    g.append("GGBBGB")
    g.append("GGGGGG")
    ret=twoPluses(g)
    print(ret)

