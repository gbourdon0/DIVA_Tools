"""
from an internet source, I'll custom it
"""
import matplotlib.pyplot as plt
import os
import pickle as pk
from matplotlib.colors import ListedColormap
cmap = ListedColormap(["#7FFF00", # vert chartreuse
                       "#007dbc", #bleu decathlon
                       "#d50000", #rouge drapeau alsace
                       "#fbec8f", #jaune post-it
                       "tab:brown",
                       "tab:purple",
                       "tab:gray",
                        "k"
                       ])

def set_size(width="thesis", fraction=1, ratio="golden", subplots=(1, 1)):
    """Set figure dimensions to avoid scaling in LaTeX.
    Parameters
    ----------
    width: float or string, optional
        Document textwidth or columnwidth in pts. Predefines 'thesis' and 'beamer' widths.
        Use \showthe\textwidth in .tex file to get your width.
    fraction: float, optional
        Fraction of the width which you wish the figure to occupy.
    ratio: 'golden' or '4:3', optional
        Scale figure by this factor.
    subplots: array-like, optional
        The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
        Dimensions of figure in inches.
    References
    ----------
    https://jwalton.info/Embed-Publication-Matplotlib-Latex/
    """
    if width == "thesis":
        width = 426.79134
    elif width == "beamer":
        width = 307.28987
    else:
        width = width

    fig_width_pt = width * fraction
    inches_per_pt = 1 / 72.27

    if ratio == "golden":
        ratio_ = (5 ** 0.5 - 1) / 2
    elif ratio == "4:3":
        ratio_ = 3 / 4
    else:
        raise ValueError

    fig_width_in = fig_width_pt * inches_per_pt
    fig_height_in = fig_width_in * ratio_ * (subplots[0] / subplots[1])

    return fig_width_in, fig_height_in


def configure_latex(style="default", plot_font=11.0, label_font=9.0, global_save_path=None):
    """Sets up LaTeX in matplotlib.
    Parameters
    ----------
    style: str or None, optional
        If None return all options
    plot_font: float, optional
        General fontsize
    label_font: float
        Legend and tick fontsize
    global_save_path: str or None, optional
        If not None set global save path as save_path = global_save_path
    References
    ----------
    https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
    https://matplotlib.org/stable/tutorials/text/usetex.html
    https://www.youtube.com/watch?v=xAoljeRJ3lU
    """
    if style is None:
        style_list = ["default", "classic"] + sorted(style for style in plt.style.available if style != "classic")
    else:
        style_list = None
        plt.style.use(style)

    tex_fonts = {
        "text.usetex": True,
        "font.family": "serif",
        "axes.titlesize": plot_font,
        "axes.labelsize": plot_font,
        "font.size": plot_font,
        "legend.fontsize": label_font,
        "xtick.labelsize": label_font,
        "ytick.labelsize": label_font,
    }

    plt.rcParams.update(tex_fonts)
    if global_save_path is not None:
        global save_path
        save_path = global_save_path

    return style_list


def savefig(file_name, format="pdf", pickle=None, **save_kwargs):
    """Saves figure. Use instead of plt.savefig().
    Parameters
    ----------
    file_name: str
        File path with name if global save_path not set, else only file name.
    format: str, optional
        Output file format.
    save_kwargs: optional
        plt.savefig(**kwargs)
    References
    ----------
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
    """
    global save_path

    try:
        if file_name[-1] == "/":
            file_name = file_name[:-1]
        if save_path[-1] != "/":
            save_path += "/"

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_location = f"{save_path}{file_name}.{format}"
        save_pickle = f"{save_path}{file_name}"
    except:
        save_location = f"{file_name}.{format}"
        save_pickle = f"{file_name}"

    #plt.tight_layout()
    plt.savefig(save_location, format=format, bbox_inches="tight", **save_kwargs)

    if pickle != None:
        # Save plot in .pickle format, that allows to modify afterwards
        pk.dump(pickle, open(save_pickle + ".pickle", "wb"))


def generate_tex_figures(subplots=(1, 1)):
    """Generates and prints LaTex string for figure or subfigure.
    Parameters
    ----------
    subplots: array-like, optional
        The number of rows and columns of subplots.
    Returns
    -------
    tex_figure: str
        Figure string.
    References
    ----------
    https://www.overleaf.com/learn/latex/How_to_Write_a_Thesis_in_LaTeX_(Part_3):_Figures,_Subfigures_and_Tables
    """
    base = lambda t: "\n{}\\centering\n{}\\includegraphics{{< >}}\n{}\\caption{{< >}}\n{}\\label{{fig: < >}}\n".format(
        *(4 * ["    " * t])
    )

    tex_figure = ""

    if subplots[0] == subplots[1] == 1:
        tex_figure += "\\begin{{figure}}[h!]{}\\end{{figure}}".format(base(1))
        print(tex_figure)
        return tex_figure

    tex_figure += "\\begin{figure}[h!]\n    \\centering\n"

    for i in range(subplots[0]):
        for j in range(subplots[1]):
            tex_figure += "    \\begin{{subfigure}}[b]{{{:.2f}\\textwidth}}".format(1 / subplots[1] - 0.01)
            tex_figure += "{}    \\end{{subfigure}}\n    \\hfill\n".format(base(2))

    tex_figure = tex_figure[:-7]
    tex_figure += "\\caption{}\n    \\label{fig: < >}"
    tex_figure += "\n\\end{figure}"

    print(tex_figure)
    return tex_figure
