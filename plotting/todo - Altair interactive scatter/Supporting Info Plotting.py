# Supporting Info
# df = solventPlot[['FRMS', 'FRDT', 'Solvent']]
# df.sort_values(by='Solvent', ascending=True, kind='quicksort', inplace=True)
# fig4SI = sns.pairplot(data=df, hue='Solvent', hue_order=None, palette=None, vars=None, x_vars=None, y_vars=None, kind="scatter",
#              diag_kind="auto", markers=None, height=2.5, aspect=1, dropna=True, plot_kws=None, diag_kws=None, grid_kws=None, size=None)

# sns.pairplot(
#     solventPlot,
#     # markers = ["o", "s"],
#     x_vars = ['Z1MS-LWI', 'Z2MS-LWI'],
#     y_vars = ['Z1DT-LWI', 'Z2DT-LWI'],
#     kind='reg',
#     height=6,
#     aspect=1,
#     dropna=True,
#     hue='Solvent',
#     # hue_order= ['Solvent']
#     # xlim=(int(solventPlot['Z2MS-LWI'].min())*-1, int(solventPlot['Z2MS-LWI'].max())*1.1),
#     # ylim=(int(solventPlot['Z2DT-LWI'].min())*-1, int(solventPlot['Z2DT-LWI'].max())*1.1)
# )
# plt.show()

#     # Seaborn
# sns.set(style="ticks")

# # # Show the results of a linear regression within each dataset
# sns.lmplot(x="m/z", y="DT", col="Area", hue="Area", data=plotdf,
#            col_wrap=2, ci=None, palette="muted", height=4,
#            scatter_kws={"s": 50, "alpha": 1})



        # Figure 4 Pairplot to explore data:
#  Seaborn pairplot

figure4pair = sns.pairplot(
    data=solventPlot,
    hue='Solvent',
    # hue_order='Condition',
    # palette='magma',
    palette='magma',
    vars=['FRMS', 'FRDT'],
    kind='reg',
    # diag_kind='hist',
    # markers=None,
    height=3,
    # col='Solvent',
    # col_wrap=3,
    aspect=1,
    dropna=True,
    # size='Condition',
)
plt.tight_layout()


# Save figure

figure4pair.savefig('D:\Programming\SAMM\SAMMplot\Figure 4\Figure4pair.png')
print('Figure4.png Exported')