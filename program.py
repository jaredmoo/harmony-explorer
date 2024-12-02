from scale_label import scale_index
from chord_label import chord_label_index
from relationship import relationships

chord_label_index.dump("chord_labels_chromatic.txt")
for s in scale_index.values():
    chord_label_index.restrict(s).dump("chord_labels_" + s.name + ".txt")

with open("relationships.txt", "w", encoding="utf8") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
