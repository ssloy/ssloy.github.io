import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter



plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=24)
plt.rcParams['hatch.color'] = 'white'
plt.rcParams['hatch.linewidth'] = 20.0
plt.rcParams['figure.autolayout'] = True
plt.rcParams["legend.framealpha"] = 1.

plt.figure(figsize=(16, 4))

ax = plt.gca()
for spine in ["top", "left", "right"]:
    ax.spines[spine].set_visible(False)
ax.yaxis.set_visible(False)

def plot_values(vals, xlim=None, title=None, color='C0', linewidth=1, linestyle='-'):
    vals_clip = vals #vals[(vals > lo) & (vals <= hi)]
    plt.vlines(vals_clip, 0.0, 1.0, color=color, linewidth=linewidth, linestyle=linestyle)
    if xlim:
        plt.xlim(*xlim)
    plt.yticks([])
    if title:
        plt.title(title)
    plt.tight_layout()

'''
numbers = np.array([m / 256 for m in range(256)])
plot_values(None, numbers, xlim=(0,2.0), title=f"fixed (0,1)")
plt.show()

numbers = np.array([m / 128 for m in range(256)])
plot_values(None, numbers, xlim=(0,2.0), title=f"fixed (0,1)")
plt.show()
'''

exponent_bits = 2
mantissa_bits = 7 - exponent_bits
subnormal = False

anchors = [0]
for e in range(-2**(exponent_bits-1)+1, 2**(exponent_bits-1)+1):
    anchors.append(2**e)
numbers = []
for i in range(len(anchors)-1):
    for m in range(2**mantissa_bits):
        v = anchors[i] + m/2**mantissa_bits * (anchors[i+1]-anchors[i])
        numbers.append(v)



'''
for e in range(-2**(exponent_bits-1), 2**(exponent_bits-1)):
    if subnormal and e == -2**(exponent_bits-1):
        anchors.append(0)
    else:
        anchors.append(2**e)
    for m in range(2**mantissa_bits):
        if subnormal:
            if e == -2**(exponent_bits-1):
                v = (0 + m/2**mantissa_bits) * 2**(e+1)
            else:
                v = (1 + m/2**mantissa_bits) * 2**e
        else:
            v = (1 + m/2**mantissa_bits) * 2**e

        numbers.append(v)
        print(e, m, numbers[-1])
'''

plot_values(np.array(numbers), xlim=(-0.01,16.01), title=f"fixed (0,1)", color='teal')
#plot_values(np.array(anchors[:-1]), xlim=(-0.01,16.01), title=f"{exponent_bits} exponent bits $\Rightarrow {2**exponent_bits} + 1$ anchors", color='orangered', linewidth=2)
#plot_values(np.array(anchors[:-1]), xlim=(-0.01,16.01), title="$2^{n_e} \cdot 2^{n_m}$ floating point numbers", color='orangered', linewidth=2)
plot_values(np.array(anchors[:-1]), xlim=(-0.01,16.01), title="The first interval contains \\textbf{subnormal} numbers" , color='orangered', linewidth=2)
plot_values(np.array([2**(2**(exponent_bits-1))]), color='tomato', linewidth=2, linestyle='--')

#print(v)
#print(len(v))

v = sorted(set(numbers))
print(v)
print(len(v))

print(numbers)
print(len(numbers))

plt.savefig("anchors.png")

plt.show()

plt.figure(figsize=(16, 4))
ax = plt.gca()
for spine in ["top", "left", "right"]:
    ax.spines[spine].set_visible(False)
ax.yaxis.set_visible(False)

'''
numbers = np.array([m / 128*16 for m in range(128)])
print(numbers)
plot_values(numbers, xlim=(-.01, 16.01), title=f"Even distribution of 128 numbers")
plt.savefig("fixed-point.png")
plt.show()

plt.figure(figsize=(16, 4))
ax = plt.gca()
for spine in ["top", "left", "right"]:
    ax.spines[spine].set_visible(False)
ax.yaxis.set_visible(False)


print(-2**(exponent_bits-1),  2**(exponent_bits))
numbers = np.array([2**( (-2**(exponent_bits-1) + 2**(exponent_bits)*i/128 ))  for i in range(128)])
plt.xscale('log')

#for axis in [ax.xaxis, ax.yaxis]:
#    formatter = ScalarFormatter()
#    formatter.set_scientific(False)
#    axis.set_major_formatter(formatter)

#ticks = [1, 2, 5, 10, 16]  # Choose your desired tick positions
#ax.set_xticks(ticks)

plot_values(numbers, xlim=(0.06,16.01), title='``Ideal\'\' logarithmic distribution of 128 numbers', color='green')


print(numbers)
plt.savefig("ideal-distribution.png")
plt.show()
'''
