# Function to get info about the filename
def get_info_from_name(text: str, metrics: bool = False):
    """
    Get the information of the profile from the filename.

    Filenames formats:
        - Profile objects filenames: profile_<culture>_<num_alternatives>_<num_voters>_<mallow_disp>.obj
        - Metrics csv filenames: metrics_profile_<culture>_<num_alternatives>_<num_voters>_<mallow_disp>.obj

    Parameters
    ----------
    text : str
        The filename.
    metrics : bool
        True if the filename is one of a metrics file, False otherwise.
    """
    text = text.replace(".obj", "")

    # Remove the extension
    text_without_ext = ".".join(text.split(".")[:-1])

    # Split the text by the underscores (which are the info dividers)
    result = text_without_ext.split("_")

    # If the filename is a metrics file, the first rwo elements are "metrics" and "profile".
    # If not, the first element is "profile".
    init_index = 2 if metrics else 1

    dictionary = {
        "culture": result[init_index],
        "num_alternatives": result[init_index + 1],
        "num_voters": result[init_index + 2],
    }

    if dictionary["culture"] == "mallow":
        dictionary.update({"mallow_disp": result[init_index + 3]})

    return dictionary
