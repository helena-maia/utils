import circlify
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

def get_color(name, number):
    pal = list(sns.color_palette(palette=name, n_colors=number).as_hex())
    return pal

data = pandas.read_csv("insights.csv",sep=";")
data_s = data.sort_values(by='Porcentagem', ascending=False)


# compute circle positions:
circles = circlify.circlify(data_s['Porcentagem'].tolist(), 
                            show_enclosure=False, 
                            target_enclosure=circlify.Circle(x=0, y=0))

circles.reverse()

#pal_vi = get_color('magma_r', len(data_s))
#pal_vi = get_color('Blues_r', len(data_s))
pal_vi = get_color('RdPu_r', len(data_s))
#pal_vi = get_color('YlOrBr_r', len(data_s))
#pal_vi = get_color('RdBu_r', len(data_s))

fig, ax = plt.subplots(figsize=(14, 14), facecolor='white')
fig.set_tight_layout(True)
ax.axis('off')
lim = max(max(abs(circle.x)+circle.r, abs(circle.y)+circle.r,) for circle in circles)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# print circles
for circle, label, emi, color in zip(circles, data_s['Texto'], data_s['Porcentagem'], pal_vi):
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, alpha=0.9, color = color))
    emi_label = "{:.2f}".format(emi).replace(".",",")+"%"
    plt.annotate(emi_label, (x,y+0.02), size=25, va='center', ha='center', weight='bold')
    plt.annotate(label, (x,y-.04), size=18, va='center', ha='center')
plt.xticks([])
plt.yticks([])
plt.savefig("insights.jpg")
#plt.show()
