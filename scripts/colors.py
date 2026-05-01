pallete = ["a"]

# ------- Przypisanie kolorów dla konkretnych trybów -------

inner_colors = []
outer_colors = []
cage_colors = []
roll_colors = []
shaft_colors = []

l = len(pallete)
for i in range(0, l):
    inner_colors.append(f"#{pallete[0]}{pallete[0]}0000")

for i in range(0, l):
    outer_colors.append(f"#00{pallete[0]}{pallete[0]}00")

for i in range(0, l):
    cage_colors.append(f"#0000{pallete[0]}{pallete[0]}")

for i in range(0, l):
    roll_colors.append(f"#{pallete[0]}{pallete[0]}00{pallete[0]}{pallete[0]}")

for i in range(0, l):
    shaft_colors.append(f"#{pallete[0]}{pallete[0]}0{pallete[0]}{pallete[0]}0")
