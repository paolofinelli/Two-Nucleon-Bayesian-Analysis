
import argparse
import matplotlib as mp
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from src.lowlevel.filenames import *
from src.lowlevel.datafile import DataFile
from matplotlib import rc
from matplotlib import rcParams
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, DrawingArea, HPacker, VPacker, OffsetBox
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.legend_handler import HandlerTuple
from matplotlib.collections import BrokenBarHCollection
from subprocess import call


# rcParams['ps.distiller.res'] = 60000
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 10})
# # for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
mp.rcParams["axes.formatter.useoffset"] = False


class HandlerSquare(HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        center = xdescent + 0.5 * (width - height), ydescent
        p = mpatches.Rectangle(xy=center, width=height,
                               height=height, angle=0.0)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]


def main(
        error_band_dir,
        output_dir,
        indep_var,
        ivar_start,
        ivar_stop,
        ivar_step,
        param_list,
        observable_list,
        Lambda_b,
        lambda_mult,
        p_decimal_list,
        orders,
        ignore_orders,
        interaction,
        X_ref_hash,
        prior_set,
        h,
        cbar_lower,
        cbar_upper,
        sigma,
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
        plt.get_cmap("Oranges")(0.6),
        plt.get_cmap("Greens")(0.6),
        plt.get_cmap("Blues")(0.6),
        plt.get_cmap("Reds")(0.6)
        ]

    fill_transparency = 1
    x = np.arange(ivar_start, ivar_stop, ivar_step)

    kw_list = []
    for i, order in enumerate(orders):
        kw_list.append(
            {
                "edgecolor": color_dict[order](.99),
                "facecolor": color_dict[order](len(p_decimal_list) / (len(p_decimal_list) + 1)),
                # label=order,
                "linewidth": 1
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

    testfig = plt.figure()
    patches_list = []
    # mpatches.Rectangle(
    #                     (0.5, 0.5), 5, 5,
    #                     # color=color_dict[order](len(p_decimal_list) / (len(p_decimal_list) + 1)),
    #                     edgecolor=color_dict[order](.9),
    #                     facecolor=color_dict[order](len(p_decimal_list) / (len(p_decimal_list) + 1)),
    #                     label=order,
    #                     linewidth=1
    #                 )
    patch_width = 7
    patch_height = 13
    patch_x = 2 - patch_width/2
    patch_y = 0
    bar_start = -1
    bar_light_width = 2.2
    bar_dark_width = 1.3
    bar_line_width = 0

    for i, order in enumerate(orders):
        if i == 0:
            lne = plt.Line2D((0, 0), (0, 14), color="black")
            rec = mpatches.Rectangle(
                (patch_x, patch_y),
                patch_width,
                patch_height,
                **kw_list[i]
                )
            # leg = testfig.legend((rec, lne), ("rec", "line"))
            # hndls, labelssss = plt.get_handles_labels()
            hndls = BrokenBarHCollection(
                xranges=(
                         (bar_start, 2*bar_light_width+2*bar_dark_width+bar_line_width),
                         (bar_start+bar_light_width, 2*bar_dark_width),
                         # (bar_start+bar_light_width+bar_dark_width, bar_line_width),
                         # (bar_start+bar_light_width+bar_dark_width+bar_line_width, bar_dark_width),
                         # (bar_start+bar_light_width+2*bar_dark_width+bar_line_width, bar_light_width)
                         ),
                yrange=(0, 14),
                facecolors=(color_dict[order](1 / (len(p_decimal_list) + 1)),
                            color_dict[order](2 / (len(p_decimal_list) + 1)),
                            # color_dict[order](.99),
                            color_dict[order](2 / (len(p_decimal_list) + 1)),
                            color_dict[order](1 / (len(p_decimal_list) + 1))
                            ),
                edgecolor=color_dict[order](.99),
                # edgewidth=.6,
                linewidths=(0.4, 0),
                antialiaseds=True
                )
            # hndls = HandlerTuple(leg)
            patches_list.append(
                # rec
                hndls
            )
        else:
            # patches_list.append(mpatches.Rectangle(
            #     (patch_x, patch_y),
            #     patch_width,
            #     patch_height,
            #     **kw_list[i]
            #     )
            # )
            # hndls = BrokenBarHCollection(
            #     # xranges=((-3, 3), (0, 2), (2, 1), (3, 2), (5, 3))
            #     xranges=(
            #              (bar_start, bar_light_width),
            #              (bar_start+bar_light_width, bar_dark_width),
            #              (bar_start+bar_light_width+bar_dark_width, bar_line_width),
            #              (bar_start+bar_light_width+bar_dark_width+bar_line_width, bar_dark_width),
            #              (bar_start+bar_light_width+2*bar_dark_width+bar_line_width, bar_light_width)
            #              ),
            #     yrange=(0, 14),
            #     facecolors=(color_dict[order](1 / (len(p_decimal_list) + 1)),
            #                 color_dict[order](2 / (len(p_decimal_list) + 1)),
            #                 color_dict[order](.99),
            #                 color_dict[order](2 / (len(p_decimal_list) + 1)),
            #                 color_dict[order](1 / (len(p_decimal_list) + 1))
            #                 ),
            #     linewidths=0,
            #     antialiaseds=True
            #     )
            hndls = BrokenBarHCollection(
                xranges=(
                         (bar_start, 2*bar_light_width+2*bar_dark_width+bar_line_width),
                         (bar_start+bar_light_width, 2*bar_dark_width),
                         # (bar_start+bar_light_width+bar_dark_width, bar_line_width),
                         # (bar_start+bar_light_width+bar_dark_width+bar_line_width, bar_dark_width),
                         # (bar_start+bar_light_width+2*bar_dark_width+bar_line_width, bar_light_width)
                         ),
                yrange=(0, 14),
                facecolors=(color_dict[order](1 / (len(p_decimal_list) + 1)),
                            color_dict[order](2 / (len(p_decimal_list) + 1)),
                            # color_dict[order](.99),
                            color_dict[order](2 / (len(p_decimal_list) + 1)),
                            color_dict[order](1 / (len(p_decimal_list) + 1))
                            ),
                edgecolor=color_dict[order](.99),
                # edgewidth=.6,
                linewidths=(0.4, 0),
                antialiaseds=True
                )
            patches_list.append(
                hndls
            )

    patch_boxes = []
    for patch in patches_list:
        patchbox = DrawingArea(4, 13, 0, 0)
        patchbox.add_artist(patch)
        patch_boxes.append(patchbox)

    all_boxes = []
    for i in range(len(patch_boxes)):
        all_boxes.append(patch_boxes[i])
        all_boxes.append(word_boxes[i])

    # all_boxes.append(TextArea(
    #                  "wwiii",
    #                  textprops=dict(color="None", rotation=-90, size=8)
    #                  ))

    box = VPacker(children=all_boxes,
                  align="center",
                  pad=7, sep=7)


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
        indep_var_label = r"$E$ (MeV)"
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
    width_spacing = 2.5
    height_spacing = .6
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

            is_log = observable == ["t", "t", "t", "t"] or \
                    (observable == ["0", "0", "0", "0"] and indep_var == "energy")
            if is_log:
                ax[obs_index].set_yscale("log", nonposy='clip')
                # axis.ticklabel_format(style="plain")
            else:
                # ax[obs_index].set_yscale("linear")
                pass

            plt.setp(ax[0].get_xticklabels(), visible=False)
            plt.setp(ax[1].get_xticklabels(), visible=False)
            plt.setp(ax[2].get_xticklabels(), visible=False)

            # ax[-1].yaxis.tick_right()
            # ax[-1].yaxis.set_ticks_position('both')
            # ax[-1].yaxis.set_label_position("right")

            # Make small plots have no x tick labels
            # plt.setp([a.get_xticklabels() for a in ax[:-1]], visible=False)

            ax[3].set_xlabel(indep_var_label)
            ax[4].set_xlabel(indep_var_label)
            ax[5].set_xlabel(indep_var_label)

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

            if is_log is False:
                if observable != ['0', '0', '0', '0']:
                    ax[obs_index].ticklabel_format(style='sci', axis='y', scilimits=(-2, 1))
                y_major_locator = MaxNLocator(axis='y', nbins=7, prune="lower")
                y_minor_locator = AutoMinorLocator(n=2)
                ax[obs_index].yaxis.set_major_locator(y_major_locator)
                ax[obs_index].yaxis.set_minor_locator(y_minor_locator)

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
            legend_patches = []

            try:
                npwa_name = npwa_filename(observable, param_var, param)
                npwa_file = DataFile().read(os.path.join("../npwa_data/", npwa_name))
                npwa_plot, = ax[obs_index].plot(npwa_file[0], npwa_file[1],
                                                color="black", linewidth=1,
                                                label="NPWA", zorder=10,
                                                linestyle="--")
            except FileNotFoundError:
                npwa_plot = None

            # First get global min/max of all orders
            for i, order in enumerate(orders):
                # obs_name = observable_filename(
                #     observable, indep_var, ivar_start, ivar_stop,
                #     ivar_step, param_var, param, order)
                # dob_name = dob_filename(p_decimal_list[0], Lambda_b, obs_name)
                dob_name = dob_filename(
                        observable, indep_var, ivar_start, ivar_stop,
                        ivar_step, param_var, param, order, ignore_orders,
                        Lambda_b, lambda_mult, X_ref_hash,
                        p_decimal_list[0], prior_set, h, convention, None,
                        cbar_lower, cbar_upper, sigma,
                        potential_info=None)
                dob_file = DataFile().read(os.path.join(error_band_dir, dob_name))
                if i == 0:
                    obs = dob_file[1]
                    obs_min = np.min(obs)
                    obs_max = np.max(obs)
                else:
                    old_obs = obs
                    obs = dob_file[1]
                    # Probably the worst way to do this.
                    obs_min = min(np.min(np.minimum(old_obs, obs)), obs_min)
                    obs_max = max(np.max(np.maximum(old_obs, obs)), obs_max)

            # Decide the padding above/below the lines
            # This weights values far from 0 more heavily.
            ymin = obs_min - .1 * abs(obs_min)
            ymax = obs_max + .1 * abs(obs_max)

            if observable == ['0', '0', '0', '0'] and indep_var == "energy":
                ymax = 1e2
            ax[obs_index].set_ylim([ymin, ymax])
            ax[obs_index].set_xlim([xmin, xmax])

            # Start layering the plots
            for i, order in enumerate(orders):
                

                dob_name = dob_filename(
                        observable, indep_var, ivar_start, ivar_stop,
                        ivar_step, param_var, param, order, ignore_orders,
                        Lambda_b, lambda_mult, X_ref_hash,
                        p_decimal_list[0], prior_set, h, convention, None,
                        cbar_lower, cbar_upper, sigma,
                        potential_info=None)
                dob_file = DataFile().read(os.path.join(error_band_dir, dob_name))

                # Plot the lines
                obs = dob_file[1]

                # zorder must be <= 2 or else it will cover axes and ticks
                ax[obs_index].plot(x, obs, color=color_dict[order](.99),
                                 zorder=i/5)

                # Plot the error bands
                for band_num, p in enumerate(sorted(p_decimal_list,
                                                    reverse=True)):
                    # dob_name = dob_filename(p, Lambda_b, obs_name)
                    dob_name = dob_filename(
                        observable, indep_var, ivar_start, ivar_stop,
                        ivar_step, param_var, param, order, ignore_orders,
                        Lambda_b, lambda_mult, X_ref_hash,
                        p, prior_set, h, convention, None,
                        cbar_lower, cbar_upper, sigma,
                        potential_info=None)
                    dob_file = DataFile().read(os.path.join(error_band_dir,
                                                            dob_name))
                    obs_lower = dob_file[2]
                    obs_upper = dob_file[3]
                    ax[obs_index].fill_between(
                        x, obs_lower, obs_upper,
                        facecolor=color_dict[order](
                            (band_num + 1) / (len(p_decimal_list) + 1)
                            ),
                        color=color_dict[order](
                            (band_num + 1) / (len(p_decimal_list) + 1)
                            ),
                        alpha=fill_transparency, interpolate=True,
                        zorder=i/5)

                # Use block patches instead of lines
                # Use innermost "dark" color of bands for legend
                legend_patches.append(
                    mpatches.Rectangle(
                        (0.5, 0.5), 0.25, 0.25,
                        # color=color_dict[order](len(p_decimal_list) / (len(p_decimal_list) + 1)),
                        edgecolor=color_dict[order](.9),
                        facecolor=color_dict[order](len(p_decimal_list) / (len(p_decimal_list) + 1)),
                        label=order,
                        linewidth=1
                    ))

            # Legend on main plot
            # ax[-1].legend(loc="best", handles=my_handles)
            extra = Rectangle((0, 0), .1, .1, fc="w", fill=False, edgecolor='none', linewidth=0)
            # leg = ax[-1].legend([extra], [], title=text_str, loc="best", handlelength=0, handletextpad=0, fancybox=True)
            obs_name = indices_to_observable_name(observable)
            if observable == ['0', '0', '0', '0']:
                obs_name += r"\,(mb/sr)"
            if observable == ['t', 't', 't', 't']:
                obs_name += r"\,(mb)"
            leg.append(ax[obs_index].legend([extra], [obs_name], loc='best', handlelength=0, handletextpad=0, fancybox=True, prop={'size': 10}))
            # plt.setp(ax[-1].get_legend_handles_labels()[1], multialignment='center')

        handler_dict = dict(zip(legend_patches, [HandlerSquare() for i in legend_patches]))
        # Legend stuff
        if npwa_plot is None:
            my_handles = legend_patches
        else:
            my_handles = [npwa_plot, *legend_patches]

        text_str = ""
        if observable != ['t', 't', 't', 't']:
            text_str += param_var_label + r" = " + str(param) + param_var_units + ", "
        text_str += r"$\Lambda_b = " + str(Lambda_b*lambda_mult) + r"$\,MeV"

        legend_index = 2

        anchored_box = AnchoredOffsetbox(
         loc=2,
         child=box, pad=0.,
         frameon=True,
         bbox_to_anchor=(1.05, 1),
         bbox_transform=ax[legend_index].transAxes,
         borderpad=0.
         )

        ax[legend_index].add_artist(anchored_box)
        ax[legend_index].add_artist(leg[legend_index])

        # ax[2].text(.5, 1.1, text_str,
        #            horizontalalignment='center',
        #            verticalalignment='bottom',
        #            multialignment='center',
        #            transform=ax[2].transAxes,
        #            # bbox=dict(facecolor='white', alpha=1, boxstyle='round', pad=.3),
        #            zorder=20)

        # Legend below small plots for box plot
        # ax[0].legend(bbox_to_anchor=(-.0, 1.1, 2, 4*aspect_height),
        #              loc=3, ncol=6, mode="expand", borderaxespad=0.,
        #              handles=my_handles, prop={'size': 10},
        #              handletextpad=-.1,
        #              handler_map=handler_dict,
        #              handlelength=1.5)

        # ax[0].add_artist(leg[0])

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
        plot_name = subplot_6_obs_error_bands_filename(
                observable_list, indep_var, ivar_start, ivar_stop, ivar_step,
                param_var, param, orders, ignore_orders, Lambda_b, lambda_mult, X_ref_hash,
                p_decimal_list, prior_set, h, convention, None,
                cbar_lower, cbar_upper, sigma,
                potential_info=None)
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
        "error_band_dir",
        help="The directory in which the observables are stored.")
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
        "prior_set",
        help="The string corresponding to a given prior set.",
        choices=["A", "B", "C"])
    parser.add_argument(
        "h",
        help="The number of coefficients that contribute to \Delta_k.",
        type=int)
    parser.add_argument(
        "cbar_lower",
        help="Lower bound for cbar on sets A and C.",
        type=float)
    parser.add_argument(
        "cbar_upper",
        help="Upper bound for cbar on sets A and C.",
        type=float)
    parser.add_argument(
        "sigma",
        help="Standard deviation for cbar on set B.",
        type=float)
    parser.add_argument(
        "--p_decimals",
        help="The DOB percent divided by 100.",
        type=float, nargs="+",
        required=True)
    parser.add_argument(
        "--orders",
        help="The orders to show on the plots.",
        type=str, nargs="+",
        required=True, choices=["LOp", "LO", "NLO", "N2LO", "N3LO", "N4LO"])
    parser.add_argument(
        "--ignore_orders",
        help="The kth orders (Q^k) to ignore when calculating DoBs.",
        nargs="+", type=int,
        choices=[0, 1, 2, 3, 4, 5])
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

    if arg_dict["prior_set"] == "B":
        cup = 0
        clow = 0
        sigma = arg_dict["sigma"]
    else:
        sigma = 0
        cup = arg_dict["cbar_upper"]
        clow = arg_dict["cbar_lower"]

    if arg_dict["ignore_orders"] is None:
        ignore_orders = []
    else:
        ignore_orders = arg_dict["ignore_orders"]

    main(
        error_band_dir=arg_dict["error_band_dir"],
        output_dir=arg_dict["output_dir"],
        indep_var=arg_dict["indep_var"],
        ivar_start=arg_dict["indep_var_range"][0],
        ivar_stop=arg_dict["indep_var_range"][1],
        ivar_step=arg_dict["indep_var_range"][2],
        param_list=param_lst,
        observable_list=arg_dict["observables"],
        Lambda_b=arg_dict["Lambda_b"],
        lambda_mult=arg_dict["lambda_mult"],
        p_decimal_list=arg_dict["p_decimals"],
        orders=arg_dict["orders"],
        ignore_orders=ignore_orders,
        interaction=arg_dict["interaction"],
        X_ref_hash=arg_dict["X_ref_hash"],
        prior_set=arg_dict["prior_set"],
        h=arg_dict["h"],
        cbar_lower=clow,
        cbar_upper=cup,
        sigma=sigma,
        convention=arg_dict["convention"])
