# Data Files Information

Data files layout and content

## Data Files layout

    +---metadata-master-lists
    |       md_catchment_locations.csv
    |       md_chvs.csv
    |       md_governorates_districts.csv
    |       md_health_facilities.csv
    |
    +---other-data
    \---routine-data
        +---amd
        +---entomology
        \---malaria_cases
                rd_malaria_cases_2011_2023.csv

## Proj

    mkdocs.yml    # The configuration file.
    - metadata-master-lists/ # Entities master data folder
        md_governorates_districts.csv # Govs and districts list.
        md_hfs.csv  # Health Facilities list.
        md_catchment_locations.csv  # locations list.
        md_chvs.csv  # CHVs list.

    - routine-data/ # Routine data folder.
      - Malaria Cases/ # Cases Routine data folder
            rd_malaria_cases_2011_2023.csv  # Reported through the system and eIDEWS system from 2011.
            rd_chvs_cases.csv  # Cases routine data monthly reported by CHVs from 2018.
      - amd/ # Anti-Malaria-Drug routine data folder.
        rd_amd_supply.csv  # AMD Supply data from 2019.
      - entomology/ # Entomology related routine data
        rd_adult_mosquitoes_collection.csv
        rd_larvae_exploration_investigation.csv
        rd_aedes.csv
    - other-data/ # other data
      idps_data.csv
      ...
