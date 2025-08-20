# Wrecks

Data Wrangling for a geoviz project.

Data Sources are the [Wrecks and Obstructions dataset](https://data.admiralty.co.uk/portal/home/item.html?id=60c0908526b844a68494c038a457e1a7) from the [Admirality Marine Data Portal](https://datahub.admiralty.co.uk/portal/home/) and the [marine region polygon of the north sea](https://marineregions.org/gazetteer.php?p=details&id=2350) which is based on a [IHO](https://iho.int/) sea area.

The wrecks were filtered by their location in the north sea. This required converting degrees minutes direction to signed decimal degree coordinates.

Furthermore, the text columns were stripped of spaces.