from bicon import data_preprocessing, BiCoN, results_analysis
import pandas as pd
from collections import defaultdict
import os

def bicon(output_dir: str, entrez_counts: pd.DataFrame, biogrid_path: str, existing_labels=None):
    """
    Run BiCoN on the given data.

    Parameters
    ----------
    output_dir : str
        The directory to save the output to.
    entrez_counts : pd.DataFrame
        The data to run BiCoN on.
        The header has to be "entrez," + the sample names.
        The first column has to be the entrez IDs.
        The rest of the columns have to be the expression values.
    existing_labels : list, optional
        The labels of the samples in the data, by default None
    """

    if existing_labels is not None and len(existing_labels) != 2:
        raise ValueError("Can only have two labels!")
    
    os.makedirs(output_dir, exist_ok=True)

    out_expression = os.path.join(output_dir, "expression.csv")
    out_plot = os.path.join(output_dir, "bicon_plot.png")

    entrez_counts.to_csv(out_expression, index=False)
    GE, G, labels, _ = data_preprocessing(out_expression, biogrid_path)
    L_g_min = 10
    L_g_max = 15

    model = BiCoN(GE, G, L_g_min, L_g_max, )
    solution, scores = model.run_search(verbose=False, max_iter=50)

    results = results_analysis(
        solution, labels, convert=True, origID='entrezgene')

    if existing_labels != None:
        label_sample_dict = defaultdict(list)

        for col in entrez_counts.columns:
            for label in existing_labels:
                if label in col:
                    label_sample_dict[label].append(col)
                    break

        true_labels = [label_sample_dict[label] for label in existing_labels]
    else:
        true_labels = None

    results.show_clustermap(
        GE, G, output=out_plot, true_labels=true_labels, class_names=existing_labels)

    results.enrichment_analysis(
        library='KEGG_2021_Human', output=os.path.join(output_dir, "enrichment"))
    try:
        results.show_networks(GE, G, output=os.path.join(output_dir, "networks.png"))
    except Exception:
        return
