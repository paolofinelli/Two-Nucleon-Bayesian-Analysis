
import argparse
import matplotlib as mp
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import math
from src.lowlevel.filenames import *
from src.lowlevel.datafile import DataFile
from matplotlib import rc
from matplotlib import rcParams
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, DrawingArea, HPacker, VPacker
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from subprocess import call

# rcParams['ps.distiller.res'] = 60000
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 10})
# # for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
mp.rcParams["axes.formatter.useoffset"] = False


def main(
        coeff_dir,
        output_dir,
        indep_var,
        ivar_start,
        ivar_stop,
        ivar_step,
        param_list,
        observable_list,
        Lambda_b,
        lambda_mult,
        orders,
        interaction,
        X_ref_hash,
        convention
        ):
    """A description. It plots stuff."""

    color_dict = {
        "LOp": plt.get_cmap("Greys"),
        "LO": plt.get_cmap("Purples"),
        "NLO": plt.get_cmap("Oranges"),
        "N2LO": plt.get_cmap("Greens"),
        "N3LO": plt.get_cmap("Blues"),
        "N4LO": plt.get_cmap("Reds")
    }
    color_list = [
        plt.get_cmap("Oranges")(0.4),
        plt.get_cmap("Greens")(0.6),
        plt.get_cmap("Blues")(0.6),
        plt.get_cmap("Reds")(0.6)
        ]
    linestyle_list = [
        "-",                # Solid
        (1, (1, 2, 6, 2)),  # My dashed-dot
        # ":",                # Dotted
        (1, (1.2, 1.3)),    # My dotted
        (1, (3, 2))         # My dashed
    ]
    linewidth_list = [
        .9,
        1,
        1.2,
        1
    ]

    kw_list = []
    for color, ls, lw in zip(color_list, linestyle_list, linewidth_list):
        kw_list.append(
            {
                "color": color,
                "linestyle": ls,
                "linewidth": lw
            }
            )

    word_boxes = []
    orders_list = [r"NLO", r"N$^2$LO", r"N$^3$LO", r"N$^4$LO"]
    for word in orders_list:
        ta = TextArea(
                     word,
                     textprops=dict(color="k",
                                    rotation=-90,
                                    va="bottom",
                                    ha="right",
                                    rotation_mode="anchor",
                                    size=8
                                    ),
                     )
        word_boxes.append(
            ta
        )

    lines = []
    for i in range(len(orders)):
        if i == 0:
            lines.append(plt.Line2D((0, 0), (0, 14), **kw_list[i]))
        else:
            lines.append(plt.Line2D((0, 0), (0, 14), **kw_list[i]))

    line_boxes = []
    for line in lines:
        linebox = DrawingArea(0, 13, 0, 0)
        linebox.add_artist(line)
        line_boxes.append(linebox)

    all_boxes = []
    for i in range(len(line_boxes)):
        all_boxes.append(line_boxes[i])
        all_boxes.append(word_boxes[i])

    # all_boxes.append(TextArea(
    #                  "wwiii",
    #                  textprops=dict(color="None", rotation=-90, size=8)
    #                  ))

    box = VPacker(children=all_boxes,
                  align="center",
                  pad=7, sep=7)


    fill_transparency = 1
    x = np.arange(ivar_start, ivar_stop, ivar_step)

    order_dict = {"LO": 2, "NLO": 3, "N2LO": 4, "N3LO": 5, "N4LO": 6}

    # widths = [1 for i in range(len(orders) - 1)]
    # widths.append(len(orders)+2)
    # fig, ax = plt.subplots(nrows=1, ncols=len(orders),
    #                        sharex=True, sharey=True,
    #                        gridspec_kw={'width_ratios': widths})
    # ax = fig.add_subplot(1, 1, 1)
    # ax[-1].set_zorder(15)
    # ax[-1].set_axisbelow(False)

    if indep_var == "theta":
        param_var = "energy"
        indep_var_label = r"$\theta$ (deg)"
        param_var_label = r"$E_{\mathrm{lab}}"
        param_var_units = r"$\,MeV"
    else:
        param_var = "theta"
        indep_var_label = r"$E_{\mathrm{lab}}$ (MeV)"
        param_var_label = r"$\theta"
        param_var_units = r"^\circ$"

    # =========================================================================
    # 2x2 box by 1 big box

    aspect_width = 2   # integer
    aspect_height = 1  # integer
    aspect_ratio = aspect_width/aspect_height
    paper_width = 7    # inches
    fig = plt.figure(figsize=(paper_width, paper_width/aspect_ratio))
    if aspect_width > aspect_height:
        gs = gridspec.GridSpec(6*aspect_height, 6*aspect_width)
    width_spacing = 2
    height_spacing = .5
    gs.update(left=0.00, right=1,
              wspace=width_spacing, hspace=height_spacing)
    main_ax = plt.subplot(gs[3*aspect_height:, 4*aspect_width:])
    ax = [plt.subplot(gs[0:3*aspect_height, 0:2*aspect_width], sharex=main_ax),
          plt.subplot(gs[0:3*aspect_height, 2*aspect_width:4*aspect_width], sharex=main_ax),
          plt.subplot(gs[0:3*aspect_height, 4*aspect_width:], sharex=main_ax),
          plt.subplot(gs[3*aspect_height:, 0:2*aspect_width], sharex=main_ax),
          plt.subplot(gs[3*aspect_height:, 2*aspect_width:4*aspect_width], sharex=main_ax),
          main_ax]
    # =========================================================================

    for param in param_list:
        leg = []
        for obs_index, observable in enumerate(observable_list):

            plt.setp(ax[0].get_xticklabels(), visible=False)
            plt.setp(ax[1].get_xticklabels(), visible=False)
            plt.setp(ax[2].get_xticklabels(), visible=False)

            # ax[-1].yaxis.tick_right()
            # ax[-1].yaxis.set_ticks_position('both')
            # ax[-1].yaxis.set_label_position("right")

            # Make small plots have no x tick labels
            # plt.setp([a.get_xticklabels() for a in ax[:-1]], visible=False)

            ax[0].set_ylabel(r"$c_n$")
            ax[3].set_ylabel(r"$c_n$")

            ax[3].set_xlabel(indep_var_label)
            ax[4].set_xlabel(indep_var_label)
            ax[5].set_xlabel(indep_var_label)
            # ax.set_ylabel('')

            # Create the description box
            # text_str = r"$C_{" + observable[0] + observable[1] + \
            #     observable[2] + observable[3] + r"}$" + "\n"
            # text_str = indices_to_observable_name(observable) + ", "
            # if observable != ['t', 't', 't', 't']:
            #     text_str += param_var_label + r" = " + str(param) + param_var_units + "\n"
            # text_str += r"$\Lambda_b = " + str(Lambda_b) + r"$\,MeV"
            # ax[-1].text(.95, .95, text_str,
            #             horizontalalignment='right',
            #             verticalalignment='top',
            #             multialignment='center',
            #             transform=ax[-1].transAxes,
            #             bbox=dict(facecolor='white', alpha=1, boxstyle='round', pad=.3),
            #             zorder=20)

            if indep_var == "energy":
                major_ticks = np.arange(0, 351, 100)
                # minor_ticks = np.arange(50, 351, 100)
                x_minor_locator = AutoMinorLocator(n=2)
                xmin = 0
                xmax = 350
            elif indep_var == "theta":
                major_ticks = np.arange(0, 181, 60)
                # minor_ticks = np.arange(30, 181, 60)
                x_minor_locator = AutoMinorLocator(n=3)
                xmin = 0
                xmax = 180
            # [axis.set_xticks(minor_ticks, minor=True) for axis in ax]
            [axis.set_xticks(major_ticks) for axis in ax]
            [axis.xaxis.set_minor_locator(x_minor_locator) for axis in ax]

            for i, axis in enumerate(ax):
                y_major_locator = MaxNLocator(axis='y', nbins=6, prune="lower")
                y_minor_locator = AutoMinorLocator(n=2)
                axis.yaxis.set_major_locator(y_major_locator)
                axis.yaxis.set_minor_locator(y_minor_locator)
            # ylocator_list = [MaxNLocator(axis='y', nbins=7) for axis in ax]
            # [axis.yaxis.set_major_locator(ylocator_list[i]) for i, axis in enumerate(ax)]
            # Set number of ticks
            # [axis.locator_params(axis='y', numticks=6) for axis in ax]
            # plt.locator_params(axis='y', numticks=6)

            if obs_index == 0:
                legend_patches = []

            # First get global min/max of all orders
            for i, order in enumerate(orders):
                # obs_name = observable_filename(
                #     observable, indep_var, ivar_start, ivar_stop,
                #     ivar_step, param_var, param, orders[-1])
                # coeff_name = coeff_filename(Lambda_b, obs_name, X_ref_hash)
                coeff_name = coeff_filename(
                    observable, indep_var, ivar_start, ivar_stop,
                    ivar_step, param_var, param, orders[-1],
                    Lambda_b, lambda_mult, X_ref_hash, convention,
                    potential_info=None)
                coeff_file = DataFile().read(os.path.join(coeff_dir, coeff_name))

                if i == 0:
                    coeff = coeff_file[order_dict[order]]
                    coeff_min = np.nanmin(coeff)
                    coeff_max = np.nanmax(coeff)
                else:
                    old_coeff = coeff
                    coeff = coeff_file[order_dict[order]]
                    # Probably the worst way to do this.
                    coeff_min = min(np.nanmin(np.minimum(old_coeff, coeff)), coeff_min)
                    coeff_max = max(np.nanmax(np.maximum(old_coeff, coeff)), coeff_max)

                # Plot the lines
                ax[obs_index].plot(x, coeff,
                                   # color=color_dict[order](.6),
                                   color=color_list[i],
                                   linewidth=linewidth_list[i],
                                   label=order,
                                   zorder=i/5,
                                   ls=linestyle_list[i])

                # ax[obs_index].plot(x, np.zeros(len(x)), zorder=2,
                #                    ls="-.", color="black")

                # ax[obs_index].axhline(0, linestyle='--', color='k', linewidth=.5)  # horizontal lines

                if obs_index == 0:
                    
                    # Use block patches instead of lines
                    # Use innermost "dark" color of bands for legend
                    # legend_patches.append(
                    #     mpatches.Rectangle(
                    #         (0.5, 0.5), 0.25, 0.25,
                    #         # color=color_dict[order](len(p_decimal_list) / (len(p_decimal_list) + 1)),
                    #         edgecolor=color_dict[order](.9),
                    #         facecolor=color_dict[order](.6),
                    #         label=order,
                    #         linewidth=1
                    #     ))
                    legend_patches.append(ax[obs_index].legend().get_lines()[i])
                    
            # Decide the padding above/below the lines
            # This weights values far from 0 more heavily.
            ymin = coeff_min - .1 * max(abs(coeff_min), abs(coeff_max))
            # ymin = coeff_min
            try:
                ymin_magnitude = min(int(math.floor(math.log10(abs(ymin)))), 0)
                # ymin = round(ymin, -ymin_magnitude)
                ymin = np.sign(ymin) * math.ceil(abs(ymin) / 10**ymin_magnitude) * 10**ymin_magnitude
            except ValueError:
                pass
            # print(ymin)
            ymax = coeff_max + .1 * max(abs(coeff_min), abs(coeff_max))
            # ymax = coeff_max
            try:
                ymax_magnitude = min(int(math.floor(math.log10(abs(ymax)))), 0)
                # ymax = round(ymax, -ymax_magnitude)
                ymax = np.sign(ymax) * math.ceil(abs(ymax) / 10**ymax_magnitude) * 10**ymax_magnitude
            except ValueError:
                pass
            if ymin == 0 and ymax == 0:
                ymin = -1
                ymax = 1
            ax[obs_index].set_ylim([ymin, ymax])
            ax[obs_index].set_xlim([xmin, xmax])

            # Plot the 0-line
            ax[obs_index].plot(
                x, np.zeros(len(x)),
                color=mp.rcParams['xtick.color'],
                linewidth=mp.rcParams['xtick.major.width'],
                zorder=0,
                ls="--"
                )

            # Legend on main plot
            # ax[-1].legend(loc="best", handles=my_handles)
            extra = Rectangle((0, 0), .1, .1, fc="w", fill=False,
                              edgecolor='none', linewidth=0)
            # leg = ax[-1].legend([extra], [], title=text_str, loc="best", handlelength=0, handletextpad=0, fancybox=True)
            obs_name = indices_to_observable_name(observable)
            leg.append(ax[obs_index].legend([extra], [obs_name], loc='best',
                                            handlelength=0, handletextpad=0,
                                            fancybox=True, prop={'size': 10}
                                            )
                       )
            # plt.setp(ax[-1].get_legend_handles_labels()[1], multialignment='center')

        # handler_dict = dict(zip(legend_patches, [HandlerSquare() for i in legend_patches]))

        text_str = ""
        if observable != ['t', 't', 't', 't']:
            text_str += param_var_label + r" = " + str(param) + param_var_units + ", "
        text_str += r"$\Lambda_b = " + str(Lambda_b*lambda_mult) + r"$\,MeV"

        legend_index = 2

        # ax[2].text(.5, 1.1, text_str,
        #             horizontalalignment='center',
        #             verticalalignment='bottom',
        #             multialignment='center',
        #             transform=ax[2].transAxes,
        #             # bbox=dict(facecolor='white', alpha=1, boxstyle='round', pad=.3),
        #             zorder=20)

        # Legend below small plots for box plot
        # ax[0].legend(bbox_to_anchor=(-.0, 1.1, 2, 4*aspect_height),
        #              loc=3,
        #              ncol=4,
        #              # mode="expand",
        #              # borderaxespad=0.,
        #              handles=legend_patches,
        #              prop={'size': 8},
        #              # handletextpad=-.1,
        #              # handler_map=handler_dict,
        #              # handlelength=1
        #              )
        # ax[legend_index].legend(
        #              # bbox_to_anchor=(-.0, 1.1, 2, 4*aspect_height),
        #              bbox_to_anchor=(0, 1.1, 1, 2),
        #              loc="lower center",
        #              ncol=4,
        #              # mode="expand",
        #              borderaxespad=0.,
        #              handles=legend_patches,
        #              prop={'size': 8},
        #              # handletextpad=-.1,
        #              # handler_map=handler_dict,
        #              handlelength=2.15,
        #              handletextpad=.5
        #              )

        anchored_box = AnchoredOffsetbox(
         loc=2,
         child=box, pad=0.,
         frameon=True,
         bbox_to_anchor=(1.05, 1),
         bbox_transform=ax[legend_index].transAxes,
         borderpad=0.
         )

        ax[legend_index].add_artist(anchored_box)
        # ax[2].legend(
        #              # bbox_to_anchor=(-.0, 1.1, 2, 4*aspect_height),
        #              bbox_to_anchor=(1.1, 0, 1.5, 1),
        #              loc="lower left",
        #              # ncol=4,
        #              # nrows=4,
        #              # mode="expand",
        #              borderaxespad=0.,
        #              handles=legend_patches,
        #              prop={'size': 8},
        #              # handletextpad=-.1,
        #              # handler_map=handler_dict,
        #              # handlelength=1
        #              )

        ax[legend_index].add_artist(leg[legend_index])

        # leg = plt.gca().get_legend()

        # Spacing between subplots
        # fig.subplots_adjust(hspace=0, wspace=0)

        # Unnecessary if the fill has a zorder <= 2.
        # for axis in ax:
        #     for k, spine in axis.spines.items():  #ax.spines is a dictionary
        #         spine.set_zorder(10)

        # Squeeze and save it
        # plt.tight_layout()
        # plt.axis('scaled', 'datalim')
        # plot_name = plot_obs_error_bands_filename(
        #         observable, indep_var, ivar_start, ivar_stop,
        #         ivar_step, param_var, param, orders[:i+1],
        #         Lambda_b, p_decimal_list)
        plot_name = subplot_6_coefficients_filename(
                observable_list, indep_var, ivar_start, ivar_stop, ivar_step,
                param_var, param, orders, Lambda_b, lambda_mult, X_ref_hash,
                convention, potential_info=None)
        plt.draw()
        plt.savefig(os.path.join(output_dir, plot_name), bbox_inches="tight")

        # To fix the blurriness issue when pdf is put into a LaTeX doc.
        # Generate .eps file and then change to .pdf
        # I don't know the root problem.
        call(["epstopdf", os.path.join(output_dir, plot_name)])
        call(["rm", os.path.join(output_dir, plot_name)])

        # Clear the axes for the next observable/parameter.
        [axis.cla() for axis in ax]

if __name__ == "__main__":
    ###########################################
    # Start args for running from command line
    ###########################################
    # For help:
    # >> python plot_observables_with_error_bands.py -h
    parser = argparse.ArgumentParser(
        description="Executable script to extract np observable coefficients."
        )
    parser.add_argument(
        "coeff_dir",
        help="The directory in which the coefficients are stored.")
    parser.add_argument(
        "output_dir",
        help="The relative path where output files will be stored")
    parser.add_argument(
        "indep_var",
        help="The variable ([deg] or [MeV]) that varies in a given data file.",
        choices=["theta", "energy"])
    parser.add_argument(
        "Lambda_b",
        help="The breakdown scale of the EFT, given in MeV.",
        type=int)
    parser.add_argument(
        "lambda_mult",
        help="The lambda value that multiplies Lambda_b.",
        type=float)
    parser.add_argument(
        "interaction",
        help="The type of scattering interaction.",
        choices=["nn", "pp", "np"])
    parser.add_argument(
        "--orders",
        help="The orders to show on the plots.",
        type=str, nargs="+",
        required=True, choices=["LOp", "LO", "NLO", "N2LO", "N3LO", "N4LO"])
    parser.add_argument(
        "--indep_var_range", "--irange",
        type=int, nargs=3,
        metavar=("start", "stop", "step"),
        required=True,
        help="Cycle indep_var through [start, stop) in increments of step.")
    param_group = parser.add_mutually_exclusive_group(required=True)
    param_group.add_argument(
        "--param_values", "--pvals",
        type=int, nargs="+",
        help="""The value at which to hold the remaining variable
                (theta [deg] or energy [MeV]) in a given file.""")
    param_group.add_argument(
        "--param_range", "--prange",
        type=int, nargs=3,
        metavar=("start", "stop", "step"),
        help="Cycle param_value through [start, stop) in increments of step.")
    parser.add_argument(
        "--observables",
        metavar="p,q,i,k",
        nargs="+", required=True,
        help="The observables C_{pqik} to calculate.",
        type=lambda s: s.split(","))
    parser.add_argument(
        "--X_ref_hash",
        required=True,
        help="""The way X_ref should be calculated.
            """,
        type=str
        )
    parser.add_argument(
        "--convention",
        required=True,
        help="The Stapp or Blatt phase convention.",
        choices=["stapp", "blatt"])

    args = parser.parse_args()
    arg_dict = vars(args)
    print(arg_dict)

    if arg_dict["param_range"] is not None:
        p0 = arg_dict["param_range"][0]
        pf = arg_dict["param_range"][1]
        ps = arg_dict["param_range"][2]
        param_lst = [i for i in range(p0, pf, ps)]
    else:
        param_lst = arg_dict["param_values"]

    main(
        coeff_dir=arg_dict["coeff_dir"],
        output_dir=arg_dict["output_dir"],
        indep_var=arg_dict["indep_var"],
        ivar_start=arg_dict["indep_var_range"][0],
        ivar_stop=arg_dict["indep_var_range"][1],
        ivar_step=arg_dict["indep_var_range"][2],
        param_list=param_lst,
        observable_list=arg_dict["observables"],
        Lambda_b=arg_dict["Lambda_b"],
        lambda_mult=arg_dict["lambda_mult"],
        orders=arg_dict["orders"],
        interaction=arg_dict["interaction"],
        X_ref_hash=arg_dict["X_ref_hash"],
        convention=arg_dict["convention"])
