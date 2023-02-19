import mygene
import pandas as pd


def symbol_ensg(symbols: list | tuple | set | pd.Series) -> pd.DataFrame:
    """
    Converts an iterable of gene symbols to ensembl gene ids.
    The gene ids are embedded into a list, so that multiple gene ids can be associated with a single gene symbol.
    """

    # Convert set to list
    if isinstance(symbols, set):
        symbols = list(symbols)

    # Convert iterables to pandas Series
    if isinstance(symbols, (list, tuple)):
        symbols = pd.Series(symbols)

    results = mygene.MyGeneInfo().querymany(symbols.dropna(inplace=False), scopes='symbol',
                                            fields='ensembl.gene, symbol', returnall=True, as_dataframe=True)

    out = results["out"]
    out = out[out["ensembl.gene"].notna()]
    out = out[out["ensembl.gene"].str.match("ENSG[0-9]{11}")]

    out = out[["symbol", "ensembl.gene"]]

    # Group by symbol and concatenate the ensembl.gene values to a list
    out = out.groupby("symbol", as_index=True).agg(lambda x: list(x))

    return out

def split_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Splits a list column into multiple columns.
    """
    max_len = df[column].apply(len).max()
    if max_len > 1:
        for i in range(max_len):
            df[f"{column}_{i+1}"] = df[column].apply(lambda x: x[i] if len(x) > i else None)
        df.drop(column, axis=1, inplace=True)
    else:
        df[column] = df[column].apply(lambda x: x[0])

    return df